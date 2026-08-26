"""Genera paneles analiticos para los dos frentes de la sintesis Fase 3.3."""

import argparse
import hashlib
import json
import sqlite3
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ANALISIS_DIR = Path(__file__).resolve().parents[1]
FASE3_DIR = ANALISIS_DIR.parent
DEFAULT_CORPUS = ANALISIS_DIR / "salidas" / "corpus_sintesis_documental_v1.json"
DEFAULT_DB = FASE3_DIR / "02_eda" / "salidas" / "fase3_analitica_v1.sqlite"
DEFAULT_JSON = ANALISIS_DIR / "salidas" / "paneles_analiticos_v1.json"
DEFAULT_MARKDOWN = ANALISIS_DIR / "salidas" / "paneles_analiticos_v1.md"
DEFAULT_FIGURES = ANALISIS_DIR / "PLAN_CUADROS_GRAFICOS_v1.md"

PERIODS = ("P1", "P2", "P3")
QUESTION_DIMENSIONS = {
    "P1": ("estado_de_situacion", "contexto_antecedentes"),
    "P2": ("diagnostico_estructural",),
    "P3": ("propuestas_politica",),
    "P4": ("contexto_antecedentes", "propuestas_politica"),
    "P5": ("avances_implementacion", "brechas_implementacion"),
    "P6": ("tendencias",),
    "P7": ("desafios", "brechas_implementacion"),
    "P8": ("oportunidades",),
    "P9": ("propuestas_politica", "contexto_antecedentes"),
}
INTERPELLATION_CRITERIA = (
    "gran_impulso_ambiental_concreto",
    "oportunidades_productivas_sostenibles",
    "articulacion_actores",
    "como_hacerlo_concreto",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def period_case(column: str) -> str:
    return f"""CASE
        WHEN {column} BETWEEN 2015 AND 2018 THEN 'P1'
        WHEN {column} BETWEEN 2019 AND 2022 THEN 'P2'
        WHEN {column} BETWEEN 2023 AND 2026 THEN 'P3'
    END"""


def table(rows: list[dict], columns: list[tuple[str, str]], heading: str) -> str:
    lines = [heading, "", "| " + " | ".join(label for label, _ in columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
    lines.extend("| " + " | ".join(str(row.get(key, "")) for _, key in columns) + " |" for row in rows)
    return "\n".join(lines)


def analytical_modes(corpus: dict, connection: sqlite3.Connection) -> list[dict]:
    documents = corpus["documents"]
    denominators = Counter(document["period_id"] for document in documents)
    function_counts = Counter(
        (document["period_id"], item["id"])
        for document in documents
        for item in document["candidate_assignments"]["functions"]
    )
    direct_counts = {
        "conclusiones_explicitas": Counter(document["period_id"] for document in documents if document["document_profile"]["conclusions"]),
        "recomendaciones_explicitas": Counter(document["period_id"] for document in documents if document["document_profile"]["recommendations"]),
    }
    rows = []
    for period in PERIODS:
        for mode in ("diagnostica", "analiza", "prospecta", "evalua_implementacion", "propone_intervenir"):
            count = function_counts[(period, mode)]
            rows.append({"period_id": period, "mode": mode, "documents": count, "proportion": round(count / denominators[period], 6), "evidence_type": "candidate_weighted_taxonomy"})
        for mode, counts in direct_counts.items():
            count = counts[period]
            rows.append({"period_id": period, "mode": mode, "documents": count, "proportion": round(count / denominators[period], 6), "evidence_type": "direct_canonical_field"})
    query = f"""
        SELECT {period_case('d.anio')} AS period_id, COUNT(*) AS documents
        FROM interpellation i JOIN documents d ON d.document_id = i.document_id
        WHERE i.criterion = ? AND i.verdict = ?
        GROUP BY period_id
    """
    concrete = {row["period_id"]: row["documents"] for row in connection.execute(query, ("como_hacerlo_concreto", "Sí")).fetchall()}
    for period in PERIODS:
        count = concrete.get(period, 0)
        rows.append({"period_id": period, "mode": "politica_concreta", "documents": count, "proportion": round(count / denominators[period], 6), "evidence_type": "direct_interpellation_rubric"})
    return rows


def interpellation_panel(corpus: dict, connection: sqlite3.Connection) -> list[dict]:
    denominators = Counter(document["period_id"] for document in corpus["documents"])
    placeholders = ",".join("?" for _ in INTERPELLATION_CRITERIA)
    query = f"""
        SELECT {period_case('d.anio')} AS period_id, i.criterion, i.verdict, COUNT(*) AS documents
        FROM interpellation i JOIN documents d ON d.document_id = i.document_id
        WHERE i.criterion IN ({placeholders})
        GROUP BY period_id, i.criterion, i.verdict
        ORDER BY period_id, i.criterion, i.verdict
    """
    return [
        {**dict(row), "proportion": round(row["documents"] / denominators[row["period_id"]], 6), "evidence_type": "direct_interpellation_rubric"}
        for row in connection.execute(query, INTERPELLATION_CRITERIA).fetchall()
    ]


def question_coverage(corpus: dict, connection: sqlite3.Connection) -> list[dict]:
    denominators = Counter(document["period_id"] for document in corpus["documents"])
    rows = []
    for question, dimensions in QUESTION_DIMENSIONS.items():
        placeholders = ",".join("?" for _ in dimensions)
        query = f"""
            SELECT {period_case('d.anio')} AS period_id, COUNT(DISTINCT d.document_id) AS documents
            FROM dimensions dim JOIN documents d ON d.document_id = dim.document_id
            WHERE dim.dimension IN ({placeholders})
            GROUP BY period_id
        """
        counts = {row["period_id"]: row["documents"] for row in connection.execute(query, dimensions).fetchall()}
        for period in PERIODS:
            count = counts.get(period, 0)
            rows.append({"question_id": question, "period_id": period, "source_dimensions": list(dimensions), "documents": count, "proportion": round(count / denominators[period], 6), "evidence_type": "direct_dimension_coverage"})
    return rows


def write_figures(path: Path) -> None:
    content = """# Plan de cuadros y graficos v1

## Cuadro 1. Cobertura y corpus

Documentos por periodo, tipo documental, escala territorial y transformacion primaria. Fuente: perfiles directos y tipologia existente.

## Grafico 1. Evolucion del objeto de estudio

Barras normalizadas por periodo para objetos principales candidatos. Nota metodologica obligatoria: clasificacion candidata calibrada, no codificacion experta exhaustiva.

## Grafico 2. Modos analiticos por periodo

Barras agrupadas para diagnostica, analiza, prospecta, evalua implementacion, propone intervenir, conclusiones explicitas, recomendaciones explicitas y politica concreta. Distinguir visualmente evidencia candidata, campo canonico directo y rubrica directa de interpelacion.

## Grafico 3. Panel Big Push Ambiental

Barras 100 por ciento apiladas de Si, Parcial y No por periodo para gran impulso ambiental, oportunidades productivas sostenibles, articulacion de actores y como hacerlo concreto.

## Cuadro 2. Cobertura de preguntas de investigacion

Matriz P1-P9 por periodo con documentos cubiertos por dimensiones directas. Aclarar que es cobertura de evidencia, no respuesta final a cada pregunta.

## Grafico 4. Territorio, tipologia y objeto

Sankey o small multiples que relacionen escala territorial candidata, transformacion primaria existente y objeto principal candidato. Mantener los solapamientos territoriales visibles.

## Cuadro 3. Conclusiones y recomendaciones transversales

Sintesis cualitativa con patron, periodos, documentos ancla, limite y cita a recuperar en fase de trazabilidad.
"""
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--figures", type=Path, default=DEFAULT_FIGURES)
    args = parser.parse_args()

    corpus = json.loads(args.corpus.read_text(encoding="utf-8"))
    connection = sqlite3.connect(args.db)
    connection.row_factory = sqlite3.Row
    panels = {
        "analytical_modes": analytical_modes(corpus, connection),
        "interpellation_big_push": interpellation_panel(corpus, connection),
        "research_question_coverage": question_coverage(corpus, connection),
    }
    connection.close()
    output = {
        "version": "paneles-analiticos-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base_version": corpus["base_version"],
        "source": {"corpus_path": args.corpus.as_posix(), "corpus_sha256": sha256_file(args.corpus), "db_path": args.db.as_posix(), "db_sha256": sha256_file(args.db), "documents_active": 238, "exclusions_applied": 6},
        "limitations": [
            "Los modos de taxonomia son candidatos ponderados; conclusiones y recomendaciones son campos canonicos directos.",
            "La politica concreta y el panel Big Push usan la rubrica de interpelacion documental directa.",
            "La cobertura de preguntas mide presencia de dimensiones, no una respuesta final a la pregunta de investigacion.",
        ],
        "panels": panels,
    }
    args.json.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    markdown = "\n\n".join([
        "# Paneles analiticos v1\n\nLos tres paneles distinguen entre contenido canonico directo, clasificacion candidata y rubrica directa de interpelacion.",
        table(panels["analytical_modes"], [("Periodo", "period_id"), ("Modo", "mode"), ("Documentos", "documents"), ("Proporcion", "proportion"), ("Fuente", "evidence_type")], "## Modos analiticos"),
        table(panels["interpellation_big_push"], [("Periodo", "period_id"), ("Criterio", "criterion"), ("Veredicto", "verdict"), ("Documentos", "documents"), ("Proporcion", "proportion")], "## Big Push e interpelacion"),
        table(panels["research_question_coverage"], [("Pregunta", "question_id"), ("Periodo", "period_id"), ("Documentos", "documents"), ("Proporcion", "proportion"), ("Dimensiones", "source_dimensions")], "## Cobertura de preguntas"),
    ]) + "\n"
    args.markdown.write_text(markdown, encoding="utf-8")
    write_figures(args.figures)
    print(json.dumps({"json": args.json.as_posix(), "markdown": args.markdown.as_posix(), "figures": args.figures.as_posix()}, ensure_ascii=False))


if __name__ == "__main__":
    main()