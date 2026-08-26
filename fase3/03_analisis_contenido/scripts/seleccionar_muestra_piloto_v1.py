"""Construye muestras de lectura y planillas de revision para los pilotos M4."""

import argparse
import csv
import hashlib
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


ANALISIS_DIR = Path(__file__).resolve().parents[1]
FASE3_DIR = ANALISIS_DIR.parent
DEFAULT_DB = FASE3_DIR / "02_eda" / "salidas" / "fase3_analitica_v1.sqlite"
DEFAULT_PACKAGES_DIR = ANALISIS_DIR / "salidas"
PERIODS = (
    ("P1", 2015, 2018),
    ("P2", 2019, 2022),
    ("P3", 2023, 2026),
)


def period_for_year(year: int) -> str | None:
    for period_id, start, end in PERIODS:
        if start <= year <= end:
            return period_id
    return None


def stable_key(*values: object) -> str:
    text = "|".join(str(value) for value in values)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def evidence_quality(evidence: dict) -> tuple[int, list[str]]:
    quote = (evidence.get("quote") or "").casefold()
    words = re.findall(r"\w+", quote)
    signals = []
    score = 0
    if 20 <= len(words) <= 140:
        score += 2
        signals.append("quote_length_20_140_words")
    elif len(words) >= 12:
        score += 1
        signals.append("quote_length_12_plus_words")
    if evidence.get("page"):
        score += 1
        signals.append("page_present")
    if any(marker in quote for marker in (".", ";", ":")):
        score += 1
        signals.append("propositional_punctuation")
    keywords = {
        "propuestas_politica": ("polit", "estrateg", "instrument", "recom", "plan", "debe", "financi"),
        "tendencias": ("tend", "aument", "dismin", "evolu", "entre", "desde", "proye"),
        "diagnostico_estructural": ("estruct", "institu", "product", "desigual", "capacidad", "territ", "financi"),
        "brechas_implementacion": ("brecha", "falta", "limit", "obstac", "reto", "insuf"),
        "desafios": ("desafi", "reto", "riesgo", "obstac", "limit", "urgente"),
        "avances_implementacion": ("avance", "implement", "logr", "progreso", "adopta", "ejecut"),
    }
    matches = [keyword for keyword in keywords.get(evidence["dimension"], ()) if keyword in quote]
    if matches:
        score += 2
        signals.append("dimension_keywords:" + ",".join(matches))
    return score, signals


def choose_coverage_evidence(package: dict) -> list[dict]:
    groups: dict[tuple[str, str], list[dict]] = {}
    for evidence in package["evidence_candidates"]:
        period_id = period_for_year(evidence["anio"])
        groups.setdefault((period_id, evidence["dimension"]), []).append(evidence)

    selected = []
    used_documents: set[str] = set()
    for period_id, dimension in sorted(groups):
        candidates = groups[(period_id, dimension)]
        ranked = sorted(
            ((item, *evidence_quality(item)) for item in candidates),
            key=lambda item: (-item[1], stable_key(package["package_id"], period_id, dimension, item[0]["document_id"], item[0]["dimension_id"])),
        )
        candidates = [item[0] for item in ranked]
        candidate = next((item for item in candidates if item["document_id"] not in used_documents), candidates[0])
        quality_score, quality_signals = evidence_quality(candidate)
        used_documents.add(candidate["document_id"])
        selected.append({
            "selection_id": f"{package['package_id']}:dimension:{period_id}:{dimension}",
            "selection_type": "dimension_coverage",
            "stratum": {"period_id": period_id, "dimension": dimension},
            "selection_rule": "Una cita por celda periodo-dimension; se prioriza puntaje de calidad textual, despues un documento no usado y finalmente hash estable.",
            "selection_quality": {"score": quality_score, "signals": quality_signals},
            "evidence": candidate,
        })
    return selected


def evidence_for_document(package: dict, document_id: str, limit: int = 1) -> list[dict]:
    candidates = [item for item in package["evidence_candidates"] if item["document_id"] == document_id]
    return sorted(candidates, key=lambda item: stable_key(package["package_id"], document_id, item["dimension_id"]))[:limit]


def choose_interpellation_cases(connection: sqlite3.Connection, package: dict) -> list[dict]:
    criteria = package["selection"]["interpellation_criteria"]
    if not criteria:
        return []
    placeholders = ",".join("?" for _ in criteria)
    rows = connection.execute(f"""
         SELECT d.document_id, d.title, d.anio, d.source_path, d.source_sha256,
             i.criterion, i.verdict, i.evidence AS interpellation_evidence
        FROM interpellation i
        JOIN documents d ON d.document_id = i.document_id
        WHERE d.anio BETWEEN 2015 AND 2026
          AND i.criterion IN ({placeholders})
    """, criteria).fetchall()
    groups: dict[tuple[str, str, str], list[sqlite3.Row]] = {}
    for row in rows:
        groups.setdefault((period_for_year(row["anio"]), row["criterion"], row["verdict"]), []).append(row)

    selected = []
    for period_id, criterion, verdict in sorted(groups):
        row = min(groups[(period_id, criterion, verdict)], key=lambda item: stable_key(package["package_id"], period_id, criterion, verdict, item["document_id"]))
        selected.append({
            "selection_id": f"{package['package_id']}:interpellation:{period_id}:{criterion}:{verdict}",
            "selection_type": "interpellation_contrast",
            "stratum": {"period_id": period_id, "criterion": criterion, "verdict": verdict},
            "selection_rule": "Un documento por celda periodo-criterio-veredicto; desempate con hash estable.",
            "document": dict(row),
            "related_evidence": evidence_for_document(package, row["document_id"]),
        })
    return selected


def choose_multilevel_cases(connection: sqlite3.Connection, package: dict) -> list[dict]:
    if package["package_id"] != "gobernanza_multinivel":
        return []
    rows = connection.execute("""
        SELECT document_id, title, anio, source_path, source_sha256, application_levels_json
        FROM documents
        WHERE anio BETWEEN 2015 AND 2026
    """).fetchall()
    groups: dict[str, list[sqlite3.Row]] = {}
    for row in rows:
        levels = json.loads(row["application_levels_json"] or "{}")
        if any(candidate.get("id") == "multinivel" for candidate in levels.get("candidatos") or []):
            groups.setdefault(period_for_year(row["anio"]), []).append(row)

    selected = []
    for period_id, candidates in sorted(groups.items()):
        row = min(candidates, key=lambda item: stable_key(package["package_id"], period_id, "multinivel", item["document_id"]))
        selected.append({
            "selection_id": f"{package['package_id']}:multinivel:{period_id}",
            "selection_type": "multilevel_candidate",
            "stratum": {"period_id": period_id, "application_level_id": "multinivel"},
            "selection_rule": "Un documento con candidato multinivel por periodo; desempate con hash estable.",
            "document": {key: row[key] for key in ("document_id", "title", "anio", "source_path", "source_sha256")},
            "related_evidence": evidence_for_document(package, row["document_id"]),
            "classification": "candidate_v1",
        })
    return selected


def build_sample(connection: sqlite3.Connection, package: dict) -> dict:
    selections = choose_coverage_evidence(package)
    selections.extend(choose_interpellation_cases(connection, package))
    selections.extend(choose_multilevel_cases(connection, package))
    return {
        "version": "muestra-lectura-v1",
        "package_id": package["package_id"],
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base_version": package["base_version"],
        "source_package": f"paquete_{package['package_id']}_v1.json",
        "purpose": "Muestra de cobertura para lectura humana; no es una muestra estadistica ni evidencia seleccionada para el informe.",
        "selection_counts": {
            "dimension_coverage": sum(item["selection_type"] == "dimension_coverage" for item in selections),
            "interpellation_contrast": sum(item["selection_type"] == "interpellation_contrast" for item in selections),
            "multilevel_candidate": sum(item["selection_type"] == "multilevel_candidate" for item in selections),
            "total": len(selections),
        },
        "selections": selections,
    }


def review_rows(sample: dict) -> list[dict]:
    output = []
    for item in sample["selections"]:
        evidence = item.get("evidence")
        document = item.get("document") or evidence or {}
        related = item.get("related_evidence") or ([] if evidence is None else [evidence])
        if not related:
            related = [{}]
        for index, reference in enumerate(related, start=1):
            output.append({
                "review_id": f"{item['selection_id']}:{index}",
                "package_id": sample["package_id"],
                "selection_type": item["selection_type"],
                "stratum": json.dumps(item["stratum"], ensure_ascii=False),
                "document_id": document.get("document_id", reference.get("document_id", "")),
                "title": document.get("title", reference.get("title", "")),
                "anio": document.get("anio", reference.get("anio", "")),
                "dimension_id": reference.get("dimension_id", ""),
                "dimension": reference.get("dimension", ""),
                "page": reference.get("page", ""),
                "quote": reference.get("quote", ""),
                "source_path": document.get("source_path", reference.get("source_path", "")),
                "source_sha256": document.get("source_sha256", reference.get("source_sha256", "")),
                "interpellation_evidence": document.get("interpellation_evidence", ""),
                "review_status": "pending",
                "literal_verified": "",
                "relevance": "",
                "recommended_action": "",
                "reviewer_note": "",
                "reviewer": "",
                "reviewed_at": "",
            })
    return output


def write_markdown(sample: dict, path: Path) -> None:
    counts = sample["selection_counts"]
    lines = [
        f"# Muestra de lectura - {sample['package_id']}\n",
        f"**Generada:** `{sample['generated_at']}`  \n**Base:** `{sample['base_version']}`  \n**Paquete fuente:** `{sample['source_package']}`\n",
        sample["purpose"],
        "## Cobertura\n",
        f"- Cobertura periodo-dimension: {counts['dimension_coverage']} selecciones.",
        f"- Contrastes de interpelacion: {counts['interpellation_contrast']} selecciones.",
        f"- Casos multinivel candidatos: {counts['multilevel_candidate']} selecciones.",
        f"- Total de selecciones: {counts['total']}.",
        "\nLa planilla CSV asociada es el registro de revision. Una seleccion no equivale a un hallazgo y puede descartarse o reemplazarse con justificacion.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_csv(rows: list[dict], path: Path) -> None:
    fields = list(rows[0]) if rows else []
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--packages-dir", type=Path, default=DEFAULT_PACKAGES_DIR)
    parser.add_argument("--package", choices=("evolucion_enfoques", "gobernanza_multinivel", "all"), default="all")
    args = parser.parse_args()

    package_ids = ("evolucion_enfoques", "gobernanza_multinivel") if args.package == "all" else (args.package,)
    connection = sqlite3.connect(args.db)
    connection.row_factory = sqlite3.Row
    outputs = []
    for package_id in package_ids:
        package_path = args.packages_dir / f"paquete_{package_id}_v1.json"
        package = json.loads(package_path.read_text(encoding="utf-8"))
        sample = build_sample(connection, package)
        json_path = args.packages_dir / f"muestra_lectura_{package_id}_v1.json"
        markdown_path = args.packages_dir / f"muestra_lectura_{package_id}_v1.md"
        csv_path = args.packages_dir / f"revision_humana_{package_id}_v1.csv"
        json_path.write_text(json.dumps(sample, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        write_markdown(sample, markdown_path)
        write_csv(review_rows(sample), csv_path)
        outputs.append({"package_id": package_id, "selections": sample["selection_counts"], "json": json_path.as_posix(), "csv": csv_path.as_posix()})
    connection.close()
    print(json.dumps({"outputs": outputs}, ensure_ascii=False))


if __name__ == "__main__":
    main()