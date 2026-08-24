"""Ledger operativo recuperable para el procesamiento del corpus de fase 2.

Solo administra ejecución, checkpoints y costos. Los resultados analíticos continúan
siendo los JSON canónicos de ``fase2/corpus/resultados``.
"""

import argparse
import csv
import hashlib
import json
import sqlite3
import sys
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path


FASE2_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = FASE2_DIR.parent
DEFAULT_DB = FASE2_DIR / "estado" / "pipeline.sqlite"
DEFAULT_CSV = REPO_DIR / "documentos_definitivos_trazabilidad.csv"
DEFAULT_MANIFEST_DIR = FASE2_DIR / "corpus" / "lotes"
SCHEMA_PATH = Path(__file__).with_name("ledger_schema.sql")
FREEZE_VERSION = "pre-batch-v1"
STAGES = ("acquisition", "extraction", "enrichment", "validation", "review")
STAGE_INDEX = {stage: index for index, stage in enumerate(STAGES)}
TERMINAL_BATCH_STATUSES = ("processed", "review", "approved", "error")


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize_handle(value: str) -> str:
    value = value.strip().rstrip("/")
    if value.startswith("https://hdl.handle.net/"):
        return value
    if value.startswith("http://hdl.handle.net/"):
        return "https://" + value.removeprefix("http://")
    if value.startswith("11362/"):
        return f"https://hdl.handle.net/{value}"
    raise ValueError(f"Handle no reconocido: {value}")


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_DIR.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path, timeout=30)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 30000")
    connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    return connection


def event(
    connection: sqlite3.Connection,
    event_type: str,
    handle: str | None = None,
    batch_id: int | None = None,
    from_status: str | None = None,
    to_status: str | None = None,
    detail: str | None = None,
) -> None:
    connection.execute(
        """INSERT INTO events
           (handle, batch_id, event_type, from_status, to_status, detail, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (handle, batch_id, event_type, from_status, to_status, detail, now()),
    )


def canonical_results() -> dict[str, str]:
    results = {}
    paths = sorted((FASE2_DIR / "pilot").glob("doc*.json"))
    paths += sorted((FASE2_DIR / "corpus" / "resultados" / "json").glob("doc_*.json"))
    for path in paths:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            handle = normalize_handle(data["documento"]["handle"])
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
            continue
        results[handle] = display_path(path)
    return results


def read_corpus(csv_path: Path) -> list[dict[str, str | int]]:
    rows = []
    seen = set()
    with csv_path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required = {"dc.identifier.uri", "dc.title", "dc.date.issued"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"El CSV no contiene las columnas requeridas: {sorted(required)}")
        for position, source in enumerate(reader, 1):
            handle = normalize_handle(source["dc.identifier.uri"])
            if handle in seen:
                raise ValueError(f"Handle duplicado en el corpus: {handle}")
            seen.add(handle)
            rows.append(
                {
                    "handle": handle,
                    "corpus_order": position,
                    "title": source["dc.title"].strip(),
                    "publication_year": (
                        source.get("dc.year", "").strip()
                        or source["dc.date.issued"].strip()[:4]
                    ),
                }
            )
    return rows


def initialize(connection: sqlite3.Connection, csv_path: Path, max_retries: int) -> None:
    rows = read_corpus(csv_path)
    accepted = canonical_results()
    timestamp = now()
    csv_display = display_path(csv_path)
    with connection:
        for row in rows:
            connection.execute(
                """INSERT INTO documents
                   (handle, corpus_order, title, publication_year, source_csv,
                    max_retries, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(handle) DO UPDATE SET
                       corpus_order = excluded.corpus_order,
                       title = excluded.title,
                       publication_year = excluded.publication_year,
                       source_csv = excluded.source_csv,
                       max_retries = excluded.max_retries,
                       updated_at = excluded.updated_at""",
                (
                    row["handle"],
                    row["corpus_order"],
                    row["title"],
                    row["publication_year"],
                    csv_display,
                    max_retries,
                    timestamp,
                    timestamp,
                ),
            )
        handles = {row["handle"] for row in rows}
        missing = sorted(set(accepted) - handles)
        if missing:
            raise ValueError(f"Resultados canónicos fuera del corpus: {missing}")
        for handle, result_path in accepted.items():
            previous = connection.execute(
                "SELECT status FROM documents WHERE handle = ?", (handle,)
            ).fetchone()["status"]
            connection.execute(
                """UPDATE documents SET status = 'approved', current_stage = 'completed',
                   result_path = ?, freeze_version = ?, completed_at = COALESCE(completed_at, ?),
                   lease_expires_at = NULL, last_error = NULL, updated_at = ?
                   WHERE handle = ?""",
                (result_path, FREEZE_VERSION, timestamp, timestamp, handle),
            )
            if previous != "approved":
                event(connection, "canonical_result_detected", handle, None, previous, "approved", result_path)
        for batch in connection.execute("SELECT id FROM batches WHERE status = 'open'").fetchall():
            maybe_close_batch(connection, batch["id"])
    print(f"Corpus inicializado: {len(rows)} documentos; {len(accepted)} aprobados; {len(rows) - len(accepted)} pendientes.")


def status_summary(connection: sqlite3.Connection, as_json: bool) -> None:
    counts = {
        row["status"]: row["total"]
        for row in connection.execute(
            "SELECT status, COUNT(*) AS total FROM documents GROUP BY status ORDER BY status"
        )
    }
    batches = [
        dict(row)
        for row in connection.execute(
            """SELECT b.code, b.name, b.status, b.created_at,
                      COUNT(bd.handle) AS documents
               FROM batches b LEFT JOIN batch_documents bd ON bd.batch_id = b.id
               GROUP BY b.id ORDER BY b.id DESC LIMIT 10"""
        )
    ]
    payload = {"total": sum(counts.values()), "documents": counts, "recent_batches": batches}
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    print(f"Total: {payload['total']}")
    for key in ("pending", "queued", "in_progress", "error_retryable", "error", "processed", "review", "approved"):
        if key in counts:
            print(f"  {key:17} {counts[key]}")
    if batches:
        print("Lotes recientes:")
        for batch in batches:
            print(f"  {batch['code']}  {batch['status']:9}  {batch['documents']:3} docs  {batch['name'] or ''}")


def next_batch(
    connection: sqlite3.Connection,
    size: int,
    name: str | None,
    freeze_version: str,
    include_retries: bool,
    manifest_dir: Path,
) -> None:
    if not 1 <= size <= 100:
        raise ValueError("El tamaño del lote debe estar entre 1 y 100")
    eligible = ("pending", "error_retryable") if include_retries else ("pending",)
    placeholders = ",".join("?" for _ in eligible)
    timestamp = now()
    manifest_dir.mkdir(parents=True, exist_ok=True)
    connection.execute("BEGIN IMMEDIATE")
    try:
        rows = connection.execute(
            f"""SELECT handle, corpus_order, title, status, current_stage
                FROM documents WHERE status IN ({placeholders})
                ORDER BY CASE status WHEN 'error_retryable' THEN 0 ELSE 1 END, corpus_order
                LIMIT ?""",
            (*eligible, size),
        ).fetchall()
        if not rows:
            connection.rollback()
            print("No hay documentos elegibles para un nuevo lote.")
            return
        cursor = connection.execute(
            """INSERT INTO batches (name, requested_size, freeze_version, created_at)
               VALUES (?, ?, ?, ?)""",
            (name, size, freeze_version, timestamp),
        )
        batch_id = cursor.lastrowid
        code_number = batch_id
        code = f"L{code_number:04d}"
        while (manifest_dir / f"{code}.json").exists():
            code_number += 1
            code = f"L{code_number:04d}"
        connection.execute("UPDATE batches SET code = ? WHERE id = ?", (code, batch_id))
        for position, row in enumerate(rows, 1):
            connection.execute(
                """INSERT INTO batch_documents (batch_id, handle, position, assigned_at)
                   VALUES (?, ?, ?, ?)""",
                (batch_id, row["handle"], position, timestamp),
            )
            connection.execute(
                """UPDATE documents SET status = 'queued', active_batch_id = ?,
                   freeze_version = ?, updated_at = ? WHERE handle = ?""",
                (batch_id, freeze_version, timestamp, row["handle"]),
            )
            event(connection, "batch_assigned", row["handle"], batch_id, row["status"], "queued")
        connection.commit()
    except Exception:
        connection.rollback()
        raise

    manifest_path = manifest_dir / f"{code}.json"
    manifest = {
        "batch_id": code,
        "name": name,
        "created_at": timestamp,
        "freeze_version": freeze_version,
        "documents": [
            {
                "position": position,
                "corpus_order": row["corpus_order"],
                "handle": row["handle"],
                "title": row["title"],
                "resume_from": row["current_stage"],
            }
            for position, row in enumerate(rows, 1)
        ],
    }
    temporary = manifest_path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(manifest_path)
    with connection:
        connection.execute(
            "UPDATE batches SET manifest_path = ? WHERE id = ?",
            (display_path(manifest_path), batch_id),
        )
    print(f"{code}: {len(rows)} documentos reservados en {display_path(manifest_path)}")


def get_document(connection: sqlite3.Connection, handle: str) -> sqlite3.Row:
    row = connection.execute("SELECT * FROM documents WHERE handle = ?", (handle,)).fetchone()
    if row is None:
        raise ValueError(f"Documento no registrado: {handle}")
    return row


def start_document(
    connection: sqlite3.Connection,
    handle: str,
    model: str | None,
    prompt_version: str | None,
    lease_minutes: int,
) -> None:
    timestamp = now()
    lease = (datetime.now(timezone.utc) + timedelta(minutes=lease_minutes)).isoformat(timespec="seconds")
    connection.execute("BEGIN IMMEDIATE")
    try:
        document = get_document(connection, handle)
        if document["status"] == "approved":
            raise ValueError(
                "Reprocesamiento bloqueado: el documento ya fue aprobado. "
                "Use el estado vivo del ledger, no el manifiesto histórico del lote."
            )
        canonical_path = canonical_results().get(handle)
        if canonical_path:
            raise ValueError(
                "Reprocesamiento bloqueado: existe un resultado canónico para el documento "
                f"en {canonical_path}. Reconcilie el ledger con `ledger.py init` antes de continuar."
            )
        if document["status"] not in ("queued", "pending", "error_retryable"):
            raise ValueError(f"No se puede iniciar desde estado {document['status']}")
        attempt_no = connection.execute(
            "SELECT COALESCE(MAX(attempt_no), 0) + 1 FROM attempts WHERE handle = ?", (handle,)
        ).fetchone()[0]
        connection.execute(
            """INSERT INTO attempts
               (handle, batch_id, attempt_no, status, model, prompt_version, started_at)
               VALUES (?, ?, ?, 'running', ?, ?, ?)""",
            (handle, document["active_batch_id"], attempt_no, model, prompt_version, timestamp),
        )
        connection.execute(
            """UPDATE documents SET status = 'in_progress', model = COALESCE(?, model),
               prompt_version = COALESCE(?, prompt_version), started_at = ?,
               lease_expires_at = ?, last_error = NULL, updated_at = ? WHERE handle = ?""",
            (model, prompt_version, timestamp, lease, timestamp, handle),
        )
        event(connection, "started", handle, document["active_batch_id"], document["status"], "in_progress", f"attempt={attempt_no}")
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    print(f"Iniciado {handle} (intento {attempt_no}, lease hasta {lease}).")


def current_attempt(connection: sqlite3.Connection, handle: str) -> sqlite3.Row:
    attempt = connection.execute(
        "SELECT * FROM attempts WHERE handle = ? AND status = 'running' ORDER BY attempt_no DESC LIMIT 1",
        (handle,),
    ).fetchone()
    if attempt is None:
        raise ValueError(f"No hay un intento activo para {handle}")
    return attempt


def checkpoint(
    connection: sqlite3.Connection,
    handle: str,
    stage: str,
    artifact: str | None,
    metadata: str | None,
    lease_minutes: int,
) -> None:
    document = get_document(connection, handle)
    if document["status"] != "in_progress":
        raise ValueError(f"Checkpoint inválido desde estado {document['status']}")
    attempt = current_attempt(connection, handle)
    current_stage = document["current_stage"]
    current_index = STAGE_INDEX.get(current_stage, -1)
    stage_index = STAGE_INDEX[stage]
    if stage_index > current_index + 1:
        raise ValueError(
            f"Checkpoint {stage} fuera de orden; la etapa actual es {current_stage or 'pending'}"
        )
    metadata_data = json.loads(metadata) if metadata else None
    if stage != "review":
        validate_artifact_exists(stage, artifact)
    if stage == "extraction":
        source = metadata_data.get("source") if isinstance(metadata_data, dict) else None
        validate_extraction_artifact(artifact, source)
    metadata_json = None
    if metadata_data is not None:
        metadata_json = json.dumps(metadata_data, ensure_ascii=False, sort_keys=True)
    lease = (datetime.now(timezone.utc) + timedelta(minutes=lease_minutes)).isoformat(timespec="seconds")
    timestamp = now()
    with connection:
        connection.execute(
            """INSERT INTO checkpoints
               (handle, batch_id, attempt_no, stage, artifact_path, metadata_json, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(handle, attempt_no, stage) DO UPDATE SET
                   artifact_path = excluded.artifact_path,
                   metadata_json = excluded.metadata_json,
                   created_at = excluded.created_at""",
            (handle, document["active_batch_id"], attempt["attempt_no"], stage, artifact, metadata_json, timestamp),
        )
        connection.execute(
            "UPDATE documents SET current_stage = ?, lease_expires_at = ?, updated_at = ? WHERE handle = ?",
            (stage, lease, timestamp, handle),
        )
        event(connection, "checkpoint", handle, document["active_batch_id"], "in_progress", "in_progress", stage)
    print(f"Checkpoint {stage} guardado para {handle}.")


def validate_artifact_exists(stage: str, artifact: str | None) -> None:
    if not artifact:
        raise ValueError(f"El checkpoint {stage} requiere --artifact")
    artifact_path = Path(artifact)
    if not artifact_path.is_absolute():
        artifact_path = REPO_DIR / artifact_path
    if not artifact_path.is_file():
        raise ValueError(f"El artefacto de {stage} no existe: {artifact}")


def validate_extraction_artifact(artifact: str | None, source: str | None = None) -> None:
    if not artifact:
        raise ValueError("El checkpoint extraction requiere --artifact")
    artifact_path = Path(artifact)
    if not artifact_path.is_absolute():
        artifact_path = REPO_DIR / artifact_path
    if not artifact_path.is_file():
        raise ValueError(f"La extracción no existe: {artifact}")
    if source == "pdf_chunks":
        validate_chunk_manifest(artifact_path)
        return
    try:
        text = artifact_path.read_bytes().decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"La extracción no es UTF-8 válido: {error}") from error
    mojibake = ("Ã¡", "Ã©", "Ã­", "Ã³", "Ãº", "Ã±", "â€™", "â€œ", "â€")
    if "\ufffd" in text or any(marker in text for marker in mojibake):
        raise ValueError("La extracción contiene caracteres de reemplazo o mojibake; normalizar a UTF-8")
    useful_length = len(text.strip())
    if useful_length < 5_000:
        raise ValueError(
            f"Extracción demasiado breve ({useful_length} caracteres); requiere OCR o lectura nativa del PDF"
        )
    if source == "endpoint" and 99_000 <= useful_length <= 100_100:
        raise ValueError(
            f"Extracción del endpoint probablemente truncada en su límite ({useful_length} caracteres); "
            "usar el PDF"
        )
    controls = sum(
        unicodedata.category(character).startswith("C") and character not in "\n\r\t"
        for character in text
    )
    if controls / max(1, len(text)) > 0.02:
        raise ValueError(
            f"Extracción con codificación ilegible ({controls} caracteres de control); requiere OCR o lectura nativa del PDF"
        )


def validate_chunk_manifest(manifest_path: Path) -> None:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"El manifiesto de tramos no es JSON válido: {manifest_path}") from error
    quality = manifest.get("quality", {})
    if quality.get("usable") is not True:
        raise ValueError("El manifiesto de tramos no acredita una extracción utilizable")
    chunks = manifest.get("chunks")
    if not isinstance(chunks, list) or not chunks:
        raise ValueError("El manifiesto de tramos no contiene bloques")
    missing = [chunk.get("path") for chunk in chunks if not (manifest_path.parent / str(chunk.get("path"))).is_file()]
    if missing:
        raise ValueError(f"Faltan bloques declarados en el manifiesto: {missing}")


def update_attempt_usage(
    connection: sqlite3.Connection,
    attempt_id: int,
    input_tokens: int | None,
    output_tokens: int | None,
    cost_usd: float | None,
) -> None:
    connection.execute(
        """UPDATE attempts SET input_tokens = COALESCE(?, input_tokens),
           output_tokens = COALESCE(?, output_tokens), cost_usd = COALESCE(?, cost_usd)
           WHERE id = ?""",
        (input_tokens, output_tokens, cost_usd, attempt_id),
    )


def maybe_close_batch(connection: sqlite3.Connection, batch_id: int | None) -> None:
    if batch_id is None:
        return
    active = connection.execute(
        f"""SELECT COUNT(*) FROM batch_documents bd JOIN documents d ON d.handle = bd.handle
            WHERE bd.batch_id = ? AND d.status NOT IN ({','.join('?' for _ in TERMINAL_BATCH_STATUSES)})""",
        (batch_id, *TERMINAL_BATCH_STATUSES),
    ).fetchone()[0]
    if active == 0:
        connection.execute(
            "UPDATE batches SET status = 'completed', completed_at = ? WHERE id = ? AND status = 'open'",
            (now(), batch_id),
        )


def complete_document(
    connection: sqlite3.Connection,
    handle: str,
    result_path: str,
    review_required: bool,
    input_tokens: int | None,
    output_tokens: int | None,
    cost_usd: float | None,
) -> None:
    document = get_document(connection, handle)
    if document["status"] != "in_progress":
        raise ValueError(f"No se puede completar desde estado {document['status']}")
    if document["current_stage"] not in ("validation", "review"):
        raise ValueError("El documento debe alcanzar el checkpoint validation antes de completarse")
    result_file = Path(result_path)
    if not result_file.is_absolute():
        result_file = REPO_DIR / result_file
    if not result_file.is_file():
        raise ValueError(f"El resultado no existe: {result_path}")
    result = json.loads(result_file.read_text(encoding="utf-8"))
    try:
        result_handle = normalize_handle(result["documento"]["handle"])
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("El resultado no contiene documento.handle válido") from error
    if result_handle != handle:
        raise ValueError(f"El resultado pertenece a {result_handle}, no a {handle}")
    expected_name = f"doc_{handle.rsplit('/', 1)[-1]}.json"
    if result_file.name != expected_name:
        raise ValueError(f"Nombre de resultado inválido: se esperaba {expected_name}")
    certificate = result_file.parent.parent / "certificados" / f"{result_file.stem}.validation.json"
    if not certificate.is_file():
        raise ValueError(
            f"Falta certificado de promoción: {display_path(certificate)}. "
            "Ejecute certificar_promocion.py sobre el borrador final y copie el certificado a resultados/certificados/."
        )
    try:
        sealed = json.loads(certificate.read_text(encoding="utf-8"))
        result_hash = hashlib.sha256(result_file.read_bytes()).hexdigest()
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Certificado de promoción ilegible: {error}") from error
    if sealed.get("ok") is not True or sealed.get("result_sha256") != result_hash:
        raise ValueError("El certificado no corresponde al resultado actual o contiene compuertas fallidas")
    attempt = current_attempt(connection, handle)
    target = "review" if review_required else "processed"
    timestamp = now()
    with connection:
        update_attempt_usage(connection, attempt["id"], input_tokens, output_tokens, cost_usd)
        connection.execute(
            "UPDATE attempts SET status = 'completed', finished_at = ? WHERE id = ?",
            (timestamp, attempt["id"]),
        )
        connection.execute(
            """UPDATE documents SET status = ?, current_stage = ?, result_path = ?,
               lease_expires_at = NULL, completed_at = ?, updated_at = ? WHERE handle = ?""",
            (target, "review" if review_required else "completed", result_path, timestamp, timestamp, handle),
        )
        event(connection, "completed", handle, document["active_batch_id"], "in_progress", target, result_path)
        maybe_close_batch(connection, document["active_batch_id"])
    print(f"{handle}: {target} ({result_path}).")


def fail_document(
    connection: sqlite3.Connection,
    handle: str,
    message: str,
    retryable: bool,
    input_tokens: int | None,
    output_tokens: int | None,
    cost_usd: float | None,
) -> None:
    document = get_document(connection, handle)
    if document["status"] != "in_progress":
        raise ValueError(f"No se puede registrar fallo desde estado {document['status']}")
    attempt = current_attempt(connection, handle)
    retries = document["retry_count"] + 1
    target = "error_retryable" if retryable and retries <= document["max_retries"] else "error"
    timestamp = now()
    with connection:
        update_attempt_usage(connection, attempt["id"], input_tokens, output_tokens, cost_usd)
        connection.execute(
            """UPDATE attempts SET status = 'failed', error_message = ?, finished_at = ?
               WHERE id = ?""",
            (message, timestamp, attempt["id"]),
        )
        connection.execute(
            """UPDATE documents SET status = ?, retry_count = ?, last_error = ?,
               lease_expires_at = NULL, updated_at = ? WHERE handle = ?""",
            (target, retries, message, timestamp, handle),
        )
        event(connection, "failed", handle, document["active_batch_id"], "in_progress", target, message)
        maybe_close_batch(connection, document["active_batch_id"])
    print(f"{handle}: {target} (reintento {retries}/{document['max_retries']}).")


def retry_document(connection: sqlite3.Connection, handle: str) -> None:
    document = get_document(connection, handle)
    if document["status"] not in ("error", "error_retryable"):
        raise ValueError(f"No se puede reintentar desde estado {document['status']}")
    target = "queued" if document["active_batch_id"] else "pending"
    timestamp = now()
    with connection:
        connection.execute(
            "UPDATE documents SET status = ?, last_error = NULL, updated_at = ? WHERE handle = ?",
            (target, timestamp, handle),
        )
        if document["active_batch_id"]:
            connection.execute(
                "UPDATE batches SET status = 'open', completed_at = NULL WHERE id = ?",
                (document["active_batch_id"],),
            )
        event(connection, "manual_retry", handle, document["active_batch_id"], document["status"], target)
    print(f"{handle}: {target}.")


def approve_document(connection: sqlite3.Connection, handle: str) -> None:
    document = get_document(connection, handle)
    if document["status"] not in ("processed", "review"):
        raise ValueError(f"No se puede aprobar desde estado {document['status']}")
    timestamp = now()
    with connection:
        connection.execute(
            """UPDATE documents SET status = 'approved', current_stage = 'completed',
               completed_at = COALESCE(completed_at, ?), updated_at = ? WHERE handle = ?""",
            (timestamp, timestamp, handle),
        )
        event(connection, "approved", handle, document["active_batch_id"], document["status"], "approved")
        maybe_close_batch(connection, document["active_batch_id"])
    print(f"{handle}: approved.")


def reject_document(
    connection: sqlite3.Connection,
    handle: str,
    reason: str,
    resume_from: str,
) -> None:
    document = get_document(connection, handle)
    if document["status"] not in ("processed", "review"):
        raise ValueError(f"No se puede rechazar desde estado {document['status']}")
    retries = document["retry_count"] + 1
    target = "error_retryable" if retries <= document["max_retries"] else "error"
    timestamp = now()
    with connection:
        connection.execute(
            """UPDATE documents SET status = ?, current_stage = ?, retry_count = ?,
               result_path = NULL, last_error = ?, completed_at = NULL, updated_at = ?
               WHERE handle = ?""",
            (target, resume_from, retries, reason, timestamp, handle),
        )
        connection.execute(
            "UPDATE batches SET status = 'open', completed_at = NULL WHERE id = ?",
            (document["active_batch_id"],),
        )
        event(
            connection,
            "review_rejected",
            handle,
            document["active_batch_id"],
            document["status"],
            target,
            reason,
        )
    print(f"{handle}: {target}; retomar desde {resume_from}.")


def recover_expired(connection: sqlite3.Connection) -> int:
    timestamp = now()
    expired = connection.execute(
        """SELECT * FROM documents WHERE status = 'in_progress'
           AND lease_expires_at IS NOT NULL AND lease_expires_at < ?""",
        (timestamp,),
    ).fetchall()
    with connection:
        for document in expired:
            retries = document["retry_count"] + 1
            target = "error_retryable" if retries <= document["max_retries"] else "error"
            attempt = connection.execute(
                """SELECT id FROM attempts WHERE handle = ? AND status = 'running'
                   ORDER BY attempt_no DESC LIMIT 1""",
                (document["handle"],),
            ).fetchone()
            if attempt:
                connection.execute(
                    """UPDATE attempts SET status = 'interrupted', error_message = ?, finished_at = ?
                       WHERE id = ?""",
                    ("Lease vencido; ejecución interrumpida", timestamp, attempt["id"]),
                )
            connection.execute(
                """UPDATE documents SET status = ?, retry_count = ?, last_error = ?,
                   lease_expires_at = NULL, updated_at = ? WHERE handle = ?""",
                (target, retries, "Lease vencido; ejecución interrumpida", timestamp, document["handle"]),
            )
            event(connection, "lease_expired", document["handle"], document["active_batch_id"], "in_progress", target)
            maybe_close_batch(connection, document["active_batch_id"])
    return len(expired)


def resume(connection: sqlite3.Connection, batch_code: str | None, limit: int) -> None:
    recovered = recover_expired(connection)
    parameters = []
    batch_filter = ""
    if batch_code:
        batch_filter = "AND b.code = ?"
        parameters.append(batch_code)
    parameters.append(limit)
    rows = connection.execute(
        f"""SELECT d.handle, d.status, d.current_stage, d.retry_count, d.max_retries,
                   d.last_error, b.code AS batch_code
            FROM documents d LEFT JOIN batches b ON b.id = d.active_batch_id
            WHERE d.status IN ('queued', 'error_retryable', 'in_progress') {batch_filter}
            ORDER BY CASE d.status WHEN 'error_retryable' THEN 0 WHEN 'in_progress' THEN 1 ELSE 2 END,
                     d.corpus_order LIMIT ?""",
        parameters,
    ).fetchall()
    if recovered:
        print(f"Leases vencidos recuperados: {recovered}")
    if not rows:
        print("No hay ejecuciones para retomar.")
        return
    for row in rows:
        error = f" — {row['last_error']}" if row["last_error"] else ""
        print(
            f"{row['batch_code'] or '-':5} {row['status']:17} {row['current_stage']:11} "
            f"{row['handle']} [{row['retry_count']}/{row['max_retries']}]{error}"
        )


def export_snapshot(connection: sqlite3.Connection, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    csv_path = output_dir / f"documents_{stamp}.csv"
    json_path = output_dir / f"summary_{stamp}.json"
    rows = connection.execute("SELECT * FROM documents ORDER BY corpus_order").fetchall()
    with csv_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys() if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(dict(row) for row in rows)
    counts = {
        row["status"]: row["total"]
        for row in connection.execute("SELECT status, COUNT(*) total FROM documents GROUP BY status")
    }
    costs = connection.execute(
        """SELECT COUNT(*) attempts, COALESCE(SUM(input_tokens), 0) input_tokens,
                  COALESCE(SUM(output_tokens), 0) output_tokens, COALESCE(SUM(cost_usd), 0) cost_usd
           FROM attempts"""
    ).fetchone()
    payload = {"created_at": now(), "documents": counts, "usage": dict(costs)}
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Snapshot: {display_path(csv_path)} y {display_path(json_path)}")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument("--db", type=Path, default=DEFAULT_DB, help=f"SQLite (default: {DEFAULT_DB})")
    commands = root.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="Inicializa o reconcilia el corpus y resultados canónicos")
    init.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    init.add_argument("--max-retries", type=int, default=3)

    status = commands.add_parser("status", help="Muestra estados y lotes recientes")
    status.add_argument("--json", action="store_true")

    batch = commands.add_parser("next-batch", help="Reserva el siguiente lote y crea su manifiesto")
    batch.add_argument("--size", type=int, default=20)
    batch.add_argument("--name")
    batch.add_argument("--freeze-version", default=FREEZE_VERSION)
    batch.add_argument("--include-retries", action="store_true")
    batch.add_argument("--manifest-dir", type=Path, default=DEFAULT_MANIFEST_DIR)

    start = commands.add_parser("start", help="Inicia un intento y abre un lease")
    start.add_argument("handle")
    start.add_argument("--model")
    start.add_argument("--prompt-version")
    start.add_argument("--lease-minutes", type=int, default=60)

    point = commands.add_parser("checkpoint", help="Guarda etapa y artefacto recuperable")
    point.add_argument("handle")
    point.add_argument("stage", choices=STAGES)
    point.add_argument("--artifact")
    point.add_argument("--metadata", help="Objeto JSON compacto")
    point.add_argument("--lease-minutes", type=int, default=60)

    complete = commands.add_parser("complete", help="Cierra un intento exitoso")
    complete.add_argument("handle")
    complete.add_argument("--result", required=True)
    complete.add_argument("--review-required", action="store_true")
    add_usage_arguments(complete)

    fail = commands.add_parser("fail", help="Registra un fallo y decide si admite reintento")
    fail.add_argument("handle")
    fail.add_argument("--error", required=True)
    fail.add_argument("--no-retry", action="store_true")
    add_usage_arguments(fail)

    retry = commands.add_parser("retry", help="Reencola manualmente un error")
    retry.add_argument("handle")

    approve = commands.add_parser("approve", help="Aprueba un resultado procesado o revisado")
    approve.add_argument("handle")

    reject = commands.add_parser("reject", help="Rechaza una revisión y conserva el punto de reanudación")
    reject.add_argument("handle")
    reject.add_argument("--reason", required=True)
    reject.add_argument(
        "--resume-from",
        choices=("pending", "acquisition", "extraction", "enrichment", "validation"),
        default="extraction",
    )

    resume_parser = commands.add_parser("resume", help="Recupera leases vencidos y lista trabajo retomable")
    resume_parser.add_argument("--batch")
    resume_parser.add_argument("--limit", type=int, default=50)

    export = commands.add_parser("export", help="Exporta estado legible a CSV y JSON")
    export.add_argument("--output-dir", type=Path, default=FASE2_DIR / "estado" / "snapshots")
    return root


def add_usage_arguments(command: argparse.ArgumentParser) -> None:
    command.add_argument("--input-tokens", type=int)
    command.add_argument("--output-tokens", type=int)
    command.add_argument("--cost-usd", type=float)


def main() -> int:
    arguments = parser().parse_args()
    try:
        connection = connect(arguments.db)
        if arguments.command == "init":
            initialize(connection, arguments.csv, arguments.max_retries)
        elif arguments.command == "status":
            status_summary(connection, arguments.json)
        elif arguments.command == "next-batch":
            next_batch(
                connection,
                arguments.size,
                arguments.name,
                arguments.freeze_version,
                arguments.include_retries,
                arguments.manifest_dir,
            )
        elif arguments.command == "start":
            start_document(connection, normalize_handle(arguments.handle), arguments.model, arguments.prompt_version, arguments.lease_minutes)
        elif arguments.command == "checkpoint":
            checkpoint(connection, normalize_handle(arguments.handle), arguments.stage, arguments.artifact, arguments.metadata, arguments.lease_minutes)
        elif arguments.command == "complete":
            complete_document(connection, normalize_handle(arguments.handle), arguments.result, arguments.review_required, arguments.input_tokens, arguments.output_tokens, arguments.cost_usd)
        elif arguments.command == "fail":
            fail_document(connection, normalize_handle(arguments.handle), arguments.error, not arguments.no_retry, arguments.input_tokens, arguments.output_tokens, arguments.cost_usd)
        elif arguments.command == "retry":
            retry_document(connection, normalize_handle(arguments.handle))
        elif arguments.command == "approve":
            approve_document(connection, normalize_handle(arguments.handle))
        elif arguments.command == "reject":
            reject_document(connection, normalize_handle(arguments.handle), arguments.reason, arguments.resume_from)
        elif arguments.command == "resume":
            resume(connection, arguments.batch, arguments.limit)
        elif arguments.command == "export":
            export_snapshot(connection, arguments.output_dir)
        connection.close()
        return 0
    except (OSError, ValueError, sqlite3.Error, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
