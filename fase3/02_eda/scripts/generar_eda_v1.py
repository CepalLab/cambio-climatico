"""Genera un EDA descriptivo reproducible desde la base SQLite de Fase 3."""

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


FASE3_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DB = FASE3_DIR / "02_eda" / "salidas" / "fase3_analitica_v1.sqlite"
DEFAULT_JSON = FASE3_DIR / "02_eda" / "salidas" / "eda_descriptivo_v1.json"
DEFAULT_MD = FASE3_DIR / "02_eda" / "salidas" / "eda_descriptivo_v1.md"


def grouped(connection: sqlite3.Connection, query: str) -> list[dict]:
    return [dict(row) for row in connection.execute(query).fetchall()]


def build_report(db_path: Path) -> dict:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    report = {
        "version": "eda-descriptivo-v1",
        "generado_en": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "fuente": db_path.name,
        "denominador": {"documentos_activos": connection.execute("SELECT COUNT(*) FROM documents").fetchone()[0]},
        "documentos_por_tipo": grouped(connection, """
            SELECT COALESCE(type_normalized_name, 'Sin clasificar') AS tipo, COUNT(*) AS documentos
            FROM documents GROUP BY tipo ORDER BY documentos DESC, tipo
        """),
        "dimensiones": grouped(connection, """
            SELECT dimension, COUNT(*) AS citas
            FROM dimensions GROUP BY dimension ORDER BY citas DESC, dimension
        """),
        "transformaciones_primarias": grouped(connection, """
            SELECT COALESCE(primary_name, 'Sin clasificar') AS transformacion, COUNT(*) AS documentos
            FROM typology GROUP BY transformacion ORDER BY documentos DESC, transformacion
        """),
        "transformaciones_secundarias": grouped(connection, """
            SELECT COALESCE(secondary_name, 'Sin clasificar') AS transformacion, COUNT(*) AS documentos
            FROM typology GROUP BY transformacion ORDER BY documentos DESC, transformacion
        """),
        "paises": grouped(connection, """
            SELECT entity_name AS pais, COUNT(DISTINCT document_id) AS documentos, COUNT(*) AS relaciones
            FROM relations WHERE field = 'paises' GROUP BY entity_name
            ORDER BY documentos DESC, pais
        """),
        "sectores": grouped(connection, """
            SELECT entity_name AS sector, COUNT(DISTINCT document_id) AS documentos, COUNT(*) AS relaciones
            FROM relations WHERE field = 'sectores' GROUP BY entity_name
            ORDER BY documentos DESC, sector
        """),
        "subregiones": grouped(connection, """
            SELECT entity_name AS subregion, COUNT(DISTINCT document_id) AS documentos
            FROM relations WHERE field = 'subregiones' GROUP BY entity_name
            ORDER BY documentos DESC, subregion
        """),
        "interpelacion": grouped(connection, """
            SELECT criterion AS criterio, verdict AS veredicto, COUNT(*) AS documentos
            FROM interpellation GROUP BY criterion, verdict ORDER BY criterion, documentos DESC, verdict
        """),
        "documentos_por_anio": grouped(connection, """
            SELECT substr(publication_date, 1, 4) AS anio, COUNT(*) AS documentos
            FROM documents WHERE publication_date IS NOT NULL
            GROUP BY anio ORDER BY anio
        """),
    }
    connection.close()
    return report


def markdown_table(rows: list[dict], columns: list[tuple[str, str]], limit: int = 15) -> str:
    lines = ["| " + " | ".join(label for label, _ in columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
    for row in rows[:limit]:
        lines.append("| " + " | ".join(str(row.get(key, "")) for _, key in columns) + " |")
    return "\n".join(lines)


def write_markdown(report: dict, path: Path) -> None:
    sections = [
        f"# EDA descriptivo v1\n\nGenerado: `{report['generado_en']}`\n\n",
        f"Denominador: **{report['denominador']['documentos_activos']} documentos activos**. Fuente: `{report['fuente']}`. Las relaciones geográficas y sectoriales son candidatas v1.\n",
        "## Tipos documentales\n\n" + markdown_table(report["documentos_por_tipo"], [("Tipo", "tipo"), ("Documentos", "documentos")]),
        "## Dimensiones\n\n" + markdown_table(report["dimensiones"], [("Dimensión", "dimension"), ("Citas", "citas")]),
        "## Transformaciones primarias\n\n" + markdown_table(report["transformaciones_primarias"], [("Transformación", "transformacion"), ("Documentos", "documentos")]),
        "## Países más abordados\n\n" + markdown_table(report["paises"], [("País", "pais"), ("Documentos", "documentos"), ("Relaciones", "relaciones")]),
        "## Sectores más frecuentes\n\n" + markdown_table(report["sectores"], [("Sector", "sector"), ("Documentos", "documentos"), ("Relaciones", "relaciones")]),
        "## Subregiones\n\n" + markdown_table(report["subregiones"], [("Subregión", "subregion"), ("Documentos", "documentos")]),
        "## Interpelación\n\n" + markdown_table(report["interpelacion"], [("Criterio", "criterio"), ("Veredicto", "veredicto"), ("Documentos", "documentos")]),
    ]
    path.write_text("\n\n".join(sections) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()
    report = build_report(args.db)
    args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, args.markdown)
    print(json.dumps({"json": args.json.as_posix(), "markdown": args.markdown.as_posix(), **report["denominador"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()