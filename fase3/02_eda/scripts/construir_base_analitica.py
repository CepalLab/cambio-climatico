"""Construye una base SQLite para EDA a partir del canon y sus derivados."""

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


FASE3_DIR = Path(__file__).resolve().parents[2]
REPO_DIR = FASE3_DIR.parent
DEFAULT_NORMALIZED = FASE3_DIR / "01_normalizacion" / "salidas" / "corpus_activo_normalizado_v1.json"
DEFAULT_OUTPUT = FASE3_DIR / "02_eda" / "salidas" / "fase3_analitica_v1.sqlite"


SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE run_metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE documents (
    document_id TEXT PRIMARY KEY,
    handle TEXT NOT NULL UNIQUE,
    title TEXT,
    publication_date TEXT,
    source_path TEXT NOT NULL,
    source_sha256 TEXT NOT NULL,
    type_original TEXT,
    type_normalized_id TEXT,
    type_normalized_name TEXT,
    type_normalized_state TEXT,
    application_levels_json TEXT NOT NULL
);
CREATE TABLE relations (
    relation_id INTEGER PRIMARY KEY,
    document_id TEXT NOT NULL REFERENCES documents(document_id),
    field TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    entity_name TEXT NOT NULL,
    source_value TEXT,
    status TEXT NOT NULL,
    method TEXT NOT NULL
);
CREATE INDEX idx_relations_field_entity ON relations(field, entity_id);
CREATE INDEX idx_relations_document ON relations(document_id);
CREATE TABLE sections (
    section_id TEXT PRIMARY KEY,
    document_id TEXT NOT NULL REFERENCES documents(document_id),
    parent_section_id TEXT REFERENCES sections(section_id),
    title TEXT NOT NULL,
    level INTEGER,
    pages TEXT,
    summary TEXT
);
CREATE TABLE dimensions (
    dimension_id INTEGER PRIMARY KEY,
    document_id TEXT NOT NULL REFERENCES documents(document_id),
    section_id TEXT REFERENCES sections(section_id),
    dimension TEXT NOT NULL,
    quote TEXT,
    page TEXT,
    subtype_brecha TEXT
);
CREATE INDEX idx_dimensions_dimension ON dimensions(dimension);
CREATE TABLE interpellation (
    document_id TEXT NOT NULL REFERENCES documents(document_id),
    criterion TEXT NOT NULL,
    verdict TEXT,
    evidence TEXT,
    PRIMARY KEY(document_id, criterion)
);
CREATE TABLE typology (
    document_id TEXT PRIMARY KEY REFERENCES documents(document_id),
    primary_number INTEGER,
    primary_name TEXT,
    secondary_number INTEGER,
    secondary_name TEXT,
    application_level_original TEXT
);
"""


def walk_sections(document_id: str, sections: list[dict], parent_id: str | None = None):
    for index, section in enumerate(sections):
        section_id = f"{document_id}#section-{index + 1}" if parent_id is None else f"{parent_id}.{index + 1}"
        yield section_id, parent_id, section
        yield from walk_sections(document_id, section.get("subsecciones") or [], section_id)


def build_database(normalized_path: Path, output_path: Path) -> dict:
    source = json.loads(normalized_path.read_text(encoding="utf-8"))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        output_path.unlink()
    connection = sqlite3.connect(output_path)
    connection.executescript(SCHEMA)
    connection.executemany(
        "INSERT INTO run_metadata VALUES (?, ?)",
        [("version", "fase3-analitica-v1"), ("generated_at", datetime.now(timezone.utc).isoformat(timespec="seconds")), ("source", normalized_path.name)],
    )
    documents = source["documentos"]
    connection.executemany(
        "INSERT INTO documents VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [(
            document["documento_id"], document["handle"], document["titulo"], document.get("fecha"), document["ruta_json"],
            document["sha256_json"], document["tipo_documento_original"],
            (document.get("tipo_documento_normalizado") or {}).get("id"),
            (document.get("tipo_documento_normalizado") or {}).get("nombre"),
            (document.get("tipo_documento_normalizado") or {}).get("estado"),
            json.dumps(document.get("ambito_aplicacion") or {}, ensure_ascii=False),
        ) for document in documents],
    )
    connection.executemany(
        "INSERT INTO relations(document_id, field, entity_id, entity_name, source_value, status, method) VALUES (?, ?, ?, ?, ?, ?, ?)",
        [(
            relation["documento_id"], relation["campo"], relation["entidad_id"], relation["nombre"],
            relation.get("valor_original"), relation["estado"], relation["metodo"],
        ) for relation in source["relaciones"]],
    )
    for document in documents:
        canonical = json.loads((REPO_DIR / document["ruta_json"]).read_text(encoding="utf-8"))
        for section_id, parent_id, section in walk_sections(document["documento_id"], canonical.get("resumen_secciones") or []):
            pages = section.get("paginas")
            if isinstance(pages, (dict, list)):
                pages = json.dumps(pages, ensure_ascii=False)
            connection.execute(
                "INSERT INTO sections VALUES (?, ?, ?, ?, ?, ?, ?)",
                (section_id, document["documento_id"], parent_id, section.get("seccion", ""), section.get("nivel"), pages, section.get("resumen")),
            )
            for dimension in section.get("dimensiones") or []:
                quote = dimension.get("cita")
                if isinstance(quote, dict):
                    quote, page = quote.get("cita"), quote.get("pagina")
                else:
                    page = dimension.get("pagina")
                connection.execute(
                    "INSERT INTO dimensions(document_id, section_id, dimension, quote, page, subtype_brecha) VALUES (?, ?, ?, ?, ?, ?)",
                    (document["documento_id"], section_id, dimension.get("dimension"), quote, str(page) if page is not None else None, dimension.get("subtipo_brecha")),
                )
        for criterion, value in (canonical.get("interpelacion") or {}).items():
            connection.execute(
                "INSERT INTO interpellation VALUES (?, ?, ?, ?)",
                (document["documento_id"], criterion, value.get("veredicto"), value.get("evidencia")),
            )
        typology = canonical.get("tipologia") or {}
        primary = typology.get("transformacion_primaria") or {}
        secondary = typology.get("transformacion_secundaria") or {}
        connection.execute(
            "INSERT INTO typology VALUES (?, ?, ?, ?, ?, ?)",
            (document["documento_id"], primary.get("numero"), primary.get("nombre"), secondary.get("numero"), secondary.get("nombre"), typology.get("nivel_aplicacion")),
        )
    connection.commit()
    counts = {
        table: connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        for table in ("documents", "relations", "sections", "dimensions", "interpellation", "typology")
    }
    connection.close()
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_NORMALIZED)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(json.dumps({"output": args.output.as_posix(), **build_database(args.input, args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()