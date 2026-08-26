"""Genera paquetes reproducibles de evidencia para los pilotos de Fase 3.3."""

import argparse
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


ANALISIS_DIR = Path(__file__).resolve().parents[1]
FASE3_DIR = ANALISIS_DIR.parent
DEFAULT_DB = FASE3_DIR / "02_eda" / "salidas" / "fase3_analitica_v1.sqlite"
DEFAULT_OUTPUT_DIR = ANALISIS_DIR / "salidas"
BASE_VERSION = "fase3-analitica-v1"
PERIODS = (
    ("P1", "2015-2018", 2015, 2018),
    ("P2", "2019-2022", 2019, 2022),
    ("P3", "2023-2026", 2023, 2026),
)

PACKAGES = {
    "evolucion_enfoques": {
        "title": "Evolucion de enfoques CEPAL sobre cambio climatico, 2015-2025",
        "question_ids": ["P6"],
        "dimensions": (
            "propuestas_politica",
            "tendencias",
            "diagnostico_estructural",
            "brechas_implementacion",
            "desafios",
        ),
        "interpellation_criteria": (),
        "include_application_levels": False,
        "limitations": [
            "P3 es un periodo abierto: el corpus disponible llega hasta 2025.",
            "Las frecuencias describen presencia e intensidad de codificacion; no miden importancia sustantiva.",
            "Las citas candidatas requieren seleccion y lectura cualitativa antes de convertirse en hallazgo.",
        ],
    },
    "gobernanza_multinivel": {
        "title": "Gobernanza multinivel, capacidades e implementacion",
        "question_ids": ["P3", "P5", "P7"],
        "dimensions": (
            "propuestas_politica",
            "avances_implementacion",
            "brechas_implementacion",
            "desafios",
        ),
        "interpellation_criteria": (
            "articulacion_actores",
            "como_hacerlo_concreto",
        ),
        "include_application_levels": True,
        "limitations": [
            "Los niveles de aplicacion son candidatos normalizados v1 y no codificacion experta definitiva.",
            "Los veredictos de interpelacion se aplican a documentos completos; no prueban mecanismos en cada cita individual.",
            "La presencia de una dimension o veredicto no permite inferir eficacia de politicas ni causalidad.",
        ],
    },
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def period_for_year(year: int | None) -> str | None:
    if year is None:
        return None
    for period_id, _, start, end in PERIODS:
        if start <= year <= end:
            return period_id
    return None


def rows(connection: sqlite3.Connection, query: str, parameters: tuple = ()) -> list[dict]:
    return [dict(row) for row in connection.execute(query, parameters).fetchall()]


def document_counts(connection: sqlite3.Connection) -> list[dict]:
    counts = {row["period_id"]: row["documents"] for row in rows(connection, """
        SELECT CASE
            WHEN anio BETWEEN 2015 AND 2018 THEN 'P1'
            WHEN anio BETWEEN 2019 AND 2022 THEN 'P2'
            WHEN anio BETWEEN 2023 AND 2026 THEN 'P3'
        END AS period_id, COUNT(*) AS documents
        FROM documents
        WHERE anio BETWEEN 2015 AND 2026
        GROUP BY period_id
    """)}
    return [
        {"period_id": period_id, "period_name": name, "documents": counts.get(period_id, 0)}
        for period_id, name, _, _ in PERIODS
    ]


def dimension_metrics(connection: sqlite3.Connection, dimensions: tuple[str, ...], denominators: dict[str, int]) -> list[dict]:
    placeholders = ",".join("?" for _ in dimensions)
    aggregated = rows(connection, f"""
        SELECT CASE
            WHEN d.anio BETWEEN 2015 AND 2018 THEN 'P1'
            WHEN d.anio BETWEEN 2019 AND 2022 THEN 'P2'
            WHEN d.anio BETWEEN 2023 AND 2026 THEN 'P3'
        END AS period_id,
        dim.dimension,
        COUNT(DISTINCT dim.document_id) AS documents_with_dimension,
        COUNT(*) AS citations
        FROM dimensions dim
        JOIN documents d ON d.document_id = dim.document_id
        WHERE d.anio BETWEEN 2015 AND 2026
          AND dim.dimension IN ({placeholders})
        GROUP BY period_id, dim.dimension
    """, dimensions)
    lookup = {(row["period_id"], row["dimension"]): row for row in aggregated}
    metrics = []
    for period_id, period_name, _, _ in PERIODS:
        denominator = denominators[period_id]
        for dimension in dimensions:
            row = lookup.get((period_id, dimension), {})
            documents = row.get("documents_with_dimension", 0)
            citations = row.get("citations", 0)
            metrics.append({
                "period_id": period_id,
                "period_name": period_name,
                "dimension": dimension,
                "documents_with_dimension": documents,
                "document_proportion": round(documents / denominator, 6) if denominator else None,
                "citations": citations,
                "citations_per_document": round(citations / documents, 6) if documents else None,
            })
    return metrics


def interpellation_metrics(connection: sqlite3.Connection, criteria: tuple[str, ...]) -> list[dict]:
    if not criteria:
        return []
    placeholders = ",".join("?" for _ in criteria)
    aggregated = rows(connection, f"""
        SELECT CASE
            WHEN d.anio BETWEEN 2015 AND 2018 THEN 'P1'
            WHEN d.anio BETWEEN 2019 AND 2022 THEN 'P2'
            WHEN d.anio BETWEEN 2023 AND 2026 THEN 'P3'
        END AS period_id,
        i.criterion,
        i.verdict,
        COUNT(*) AS documents
        FROM interpellation i
        JOIN documents d ON d.document_id = i.document_id
        WHERE d.anio BETWEEN 2015 AND 2026
          AND i.criterion IN ({placeholders})
        GROUP BY period_id, i.criterion, i.verdict
        ORDER BY period_id, i.criterion, i.verdict
    """, criteria)
    return [{
        "period_id": row["period_id"],
        "criterion": row["criterion"],
        "verdict": row["verdict"],
        "documents": row["documents"],
    } for row in aggregated]


def application_level_metrics(connection: sqlite3.Connection) -> list[dict]:
    level_documents: dict[tuple[str, str], set[str]] = {}
    review_documents: dict[str, set[str]] = {period_id: set() for period_id, _, _, _ in PERIODS}
    for row in rows(connection, """
        SELECT document_id, anio, application_levels_json
        FROM documents
        WHERE anio BETWEEN 2015 AND 2026
    """):
        period_id = period_for_year(row["anio"])
        levels = json.loads(row["application_levels_json"] or "{}")
        if levels.get("requiere_revision"):
            review_documents[period_id].add(row["document_id"])
        for candidate in levels.get("candidatos") or []:
            level_documents.setdefault((period_id, candidate["id"]), set()).add(row["document_id"])
    metrics = [
        {
            "period_id": period_id,
            "application_level_id": level_id,
            "documents": len(document_ids),
            "classification": "candidate_v1",
        }
        for (period_id, level_id), document_ids in sorted(level_documents.items())
    ]
    metrics.extend({
        "period_id": period_id,
        "application_level_id": "requiere_revision",
        "documents": len(document_ids),
        "classification": "candidate_v1",
    } for period_id, document_ids in review_documents.items())
    return metrics


def evidence_candidates(connection: sqlite3.Connection, dimensions: tuple[str, ...]) -> list[dict]:
    placeholders = ",".join("?" for _ in dimensions)
    return rows(connection, f"""
        SELECT
            dim.dimension_id,
            dim.document_id,
            d.anio,
            d.title,
            dim.section_id,
            s.title AS section_title,
            dim.dimension,
            dim.quote,
            dim.page,
            d.source_path,
            d.source_sha256
        FROM dimensions dim
        JOIN documents d ON d.document_id = dim.document_id
        LEFT JOIN sections s ON s.section_id = dim.section_id
        WHERE d.anio BETWEEN 2015 AND 2026
          AND dim.dimension IN ({placeholders})
        ORDER BY dim.dimension, d.anio, dim.document_id, dim.dimension_id
    """, dimensions)


def build_package(connection: sqlite3.Connection, db_path: Path, package_id: str) -> dict:
    config = PACKAGES[package_id]
    documents_by_period = document_counts(connection)
    denominators = {row["period_id"]: row["documents"] for row in documents_by_period}
    package = {
        "version": "paquete-evidencia-v1",
        "package_id": package_id,
        "title": config["title"],
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base_version": BASE_VERSION,
        "source": {
            "database": db_path.as_posix(),
            "database_sha256": sha256_file(db_path),
            "documents_active": sum(denominators.values()),
            "exclusions_applied": 6,
        },
        "question_ids": config["question_ids"],
        "selection": {
            "dimensions": list(config["dimensions"]),
            "interpellation_criteria": list(config["interpellation_criteria"]),
            "year_range": [2015, 2025],
            "periods": [{"period_id": period_id, "name": name, "start": start, "end": end} for period_id, name, start, end in PERIODS],
        },
        "limitations": config["limitations"],
        "metrics": {
            "documents_by_period": documents_by_period,
            "dimensions_by_period": dimension_metrics(connection, config["dimensions"], denominators),
            "interpellation_by_period": interpellation_metrics(connection, config["interpellation_criteria"]),
            "application_levels_by_period": application_level_metrics(connection) if config["include_application_levels"] else [],
        },
        "evidence_candidates": evidence_candidates(connection, config["dimensions"]),
    }
    return package


def markdown_table(rows_: list[dict], columns: list[tuple[str, str]]) -> str:
    if not rows_:
        return "Sin datos para este paquete."
    lines = ["| " + " | ".join(label for label, _ in columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
    for row in rows_:
        lines.append("| " + " | ".join(str(row.get(key, "")) for _, key in columns) + " |")
    return "\n".join(lines)


def write_markdown(package: dict, path: Path) -> None:
    metrics = package["metrics"]
    sections = [
        f"# {package['title']}\n",
        f"**Paquete:** `{package['package_id']}`  \n**Generado:** `{package['generated_at']}`  \n**Base:** `{package['base_version']}`  \n**Denominador:** {package['source']['documents_active']} documentos activos; 6 exclusiones aplicadas.\n",
        "## Seleccion\n\n" + json.dumps(package["selection"], ensure_ascii=False, indent=2),
        "## Documentos por periodo\n\n" + markdown_table(metrics["documents_by_period"], [("Periodo", "period_id"), ("Nombre", "period_name"), ("Documentos", "documents")]),
        "## Dimensiones por periodo\n\n" + markdown_table(metrics["dimensions_by_period"], [("Periodo", "period_id"), ("Dimension", "dimension"), ("Documentos", "documents_with_dimension"), ("Proporcion", "document_proportion"), ("Citas", "citations"), ("Citas por documento", "citations_per_document")]),
    ]
    if metrics["interpellation_by_period"]:
        sections.append("## Interpelacion por periodo\n\n" + markdown_table(metrics["interpellation_by_period"], [("Periodo", "period_id"), ("Criterio", "criterion"), ("Veredicto", "verdict"), ("Documentos", "documents")]))
    if metrics["application_levels_by_period"]:
        sections.append("## Niveles de aplicacion candidatos\n\n" + markdown_table(metrics["application_levels_by_period"], [("Periodo", "period_id"), ("Nivel", "application_level_id"), ("Documentos", "documents"), ("Estado", "classification")]))
    sections.extend([
        f"## Citas candidatas\n\nSe exportaron **{len(package['evidence_candidates'])}** citas candidatas con `dimension_id`, pagina, ruta y hash de origen en el JSON homonimo. No son evidencia seleccionada ni hallazgos aprobados.\n",
        "## Limitaciones\n\n" + "\n".join(f"- {item}" for item in package["limitations"]),
    ])
    path.write_text("\n".join(sections) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--package", choices=(*PACKAGES, "all"), default="all")
    args = parser.parse_args()

    selected = PACKAGES.keys() if args.package == "all" else (args.package,)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(args.db)
    connection.row_factory = sqlite3.Row
    outputs = []
    for package_id in selected:
        package = build_package(connection, args.db, package_id)
        json_path = args.output_dir / f"paquete_{package_id}_v1.json"
        markdown_path = args.output_dir / f"paquete_{package_id}_v1.md"
        json_path.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        write_markdown(package, markdown_path)
        outputs.append({"package_id": package_id, "json": json_path.as_posix(), "markdown": markdown_path.as_posix(), "evidence_candidates": len(package["evidence_candidates"])})
    connection.close()
    print(json.dumps({"base_version": BASE_VERSION, "outputs": outputs}, ensure_ascii=False))


if __name__ == "__main__":
    main()