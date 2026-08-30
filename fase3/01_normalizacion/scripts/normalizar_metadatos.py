"""Genera candidatos normalizados de metadatos para una muestra o corpus activo."""

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


FASE3_DIR = Path(__file__).resolve().parents[2]
REPO_DIR = FASE3_DIR.parent
NORMALIZACION_DIR = FASE3_DIR / "01_normalizacion"
DEFAULT_INVENTORY = FASE3_DIR / "00_control" / "inventario" / "inventario_corpus_v1.json"
DEFAULT_EXCLUSIONS = FASE3_DIR / "00_control" / "inventario" / "exclusiones_corpus_v1.csv"
DEFAULT_DICTIONARY = NORMALIZACION_DIR / "salidas" / "diccionario_normalizacion_v1.json"
DEFAULT_OUTPUT = NORMALIZACION_DIR / "salidas" / "muestra_normalizacion_metadatos_v1.json"
DEFAULT_REVIEW_OUTPUT = NORMALIZACION_DIR / "revision" / "cola_revision_metadatos_muestra_v1.csv"
DEFAULT_LIMIT = 20


def load_exclusions(path: Path) -> set[str]:
    import csv

    with path.open(encoding="utf-8-sig", newline="") as file:
        return {
            row["handle"]
            for row in csv.DictReader(file)
            if row.get("decision") == "excluir" and row.get("estado") == "aplicado"
        }


def nested(data: dict, *keys: str):
    value = data
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def find_matches(value: str | None, entries: list[dict]) -> list[dict]:
    if not value:
        return []
    lowered = value.casefold()
    matches = []
    for entry in entries:
        aliases = sorted(entry["alias"], key=len, reverse=True)
        matched_aliases = [
            alias for alias in aliases
            if re.search(r"(?<!\w)" + re.escape(alias) + r"(?!\w)", value, re.IGNORECASE)
        ]
        if matched_aliases:
            matches.append({"id": entry["id"], "nombre": entry["nombre"], "aliases": matched_aliases})
    return matches


def find_type_matches(value: str | None, entries: list[dict]) -> list[dict]:
    matches = find_matches(value, entries)
    if len(matches) < 2:
        return matches
    longest_alias = max(
        (alias for match in matches for alias in match["aliases"]),
        key=len,
    )
    return [match for match in matches if longest_alias in match["aliases"]]


def split_authorship(value: str | None) -> dict:
    if not value:
        return {"original": value, "candidatos": [], "requiere_revision": False, "metodo": None}
    candidates = [
        part.strip(" ,;.")
        for part in re.split(r"\s*[•|;]\s*|,\s*|\s+(?:y|e)\s+", value)
        if part.strip()
    ]
    requires_review = bool(re.search(r"compil|editorial|autores de|funcionarios|consultores|direcci[oó]n|coordinaci[oó]n|encabezad|supervisi[oó]n|colaboraci[oó]n", value, re.IGNORECASE))
    return {
        "original": value,
        "candidatos": candidates,
        "requiere_revision": requires_review,
        "metodo": "delimitadores_conservadores",
    }


def infer_application_levels(value: str | None, entries: list[dict]) -> dict:
    matches = find_matches(value, entries)
    lowered = (value or "").casefold()
    has_national = bool(re.search(r"\bnacional\b|a nivel de pa[ií]s|por pa[ií]s", lowered))
    has_subnational = bool(re.search(r"subnacional|ciudad|municipio|municipal|provincia|provincial|departamento|departamental|cuenca|local|urbano|rural|comunal|metropolitana|insular", lowered))
    has_multinational = bool(re.search(r"\b\d+\s+pa[ií]ses\b|pa[ií]ses de am[eé]rica latina|pa[ií]ses miembros", lowered))
    has_regional_scope = bool(re.search(r"\bregional\b", lowered)) and not bool(re.search(r"serie regional|metodolog[ií]a.*regional", lowered))
    if has_regional_scope and not any(match["id"] == "regional" for match in matches):
        matches.append({"id": "regional", "nombre": "Regional", "aliases": ["inferencia: alcance regional"]})
    if has_multinational and not any(match["id"] in {"regional", "subregional"} for match in matches):
        matches.append({"id": "regional", "nombre": "Regional", "aliases": ["inferencia: múltiples países"]})
    if has_national and has_subnational and not any(match["id"] == "multinivel" for match in matches):
        matches.append({"id": "multinivel", "nombre": "Multinivel", "aliases": ["inferencia: nacional + subnacional"]})
    return {
        "original": value,
        "candidatos": matches,
        "detalle_subnacional": [
            term for term in ("ciudad", "municipio", "municipal", "provincia", "provincial", "departamento", "departamental", "cuenca", "cuencas", "local", "urbano", "rural", "comunal", "metropolitana", "insular")
            if re.search(r"\b" + term + r"\b", lowered)
        ],
        "requiere_revision": bool(matches),
        "metodo": "alias_y_regla_multinivel",
    }


def normalize_record(record: dict, dictionary: dict) -> dict:
    data = json.loads((REPO_DIR / record["ruta_json"]).read_text(encoding="utf-8"))
    document = data["documento"]
    scope = nested(data, "resumen_enriquecido", "alcance") or {}
    type_override = dictionary.get("tipo_documental_overrides", {}).get(record["handle"])
    explicit_values = dictionary.get("tipo_documental_valores_explicitos", {})
    original_type = document.get("tipo_documento")
    explicit_type = explicit_values.get(original_type)
    if explicit_type is None and original_type:
        explicit_type = next(
            (entry_type for value, entry_type in explicit_values.items() if value.casefold() == original_type.casefold()),
            None,
        )
    if type_override:
        type_candidates = [
            {
                "id": entry["id"],
                "nombre": entry["nombre"],
                "aliases": ["override explícito de muestra"],
            }
            for entry in dictionary["tipos_documentales"]
            if entry["id"] == type_override
        ]
    elif explicit_type:
        type_candidates = [
            {
                "id": entry["id"],
                "nombre": entry["nombre"],
                "aliases": ["adjudicacion explicita del diccionario"],
            }
            for entry in dictionary["tipos_documentales"]
            if entry["id"] == explicit_type
        ]
    else:
        type_candidates = find_type_matches(document.get("tipo_documento"), dictionary["tipos_documentales"])
    return {
        "documento_id": record["handle"],
        "handle": record["handle"],
        "ruta_json": record["ruta_json"],
        "sha256_json": record["sha256_json"],
        "titulo": document.get("titulo"),
        "fecha": document.get("fecha"),
        "autoria": split_authorship(document.get("autoria")),
        "tipo_documento": {
            "original": document.get("tipo_documento"),
            "candidatos": type_candidates,
        },
        "ambito_aplicacion_original": scope.get("ambito_aplicacion"),
        "referentes_dependencias_original": scope.get("referentes_dependencias"),
        "ambito_aplicacion": infer_application_levels(scope.get("ambito_aplicacion"), dictionary["niveles_aplicacion"]),
        "paises": find_matches(scope.get("ambito_aplicacion"), dictionary["paises"]),
        "subregiones": find_matches(scope.get("ambito_aplicacion"), dictionary["subregiones"]),
        "sectores": {
            "original": scope.get("sectorial"),
            "candidatos": find_matches(scope.get("sectorial"), dictionary["sectores"]),
        },
        "organizaciones": find_matches(
            " ".join(str(scope.get(key) or "") for key in ("referentes_dependencias", "sectorial")),
            dictionary["organizaciones"],
        ),
        "trazabilidad": {
            "fuente": "fase2_json_canonico",
            "nivel": "documento",
            "estado": "candidato_no_adjudicado",
        },
    }


def build_output(inventory_path: Path, exclusions_path: Path, dictionary_path: Path, limit: int) -> dict:
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    dictionary = json.loads(dictionary_path.read_text(encoding="utf-8"))
    exclusions = load_exclusions(exclusions_path)
    active = [record for record in inventory["documentos"] if record["handle"] not in exclusions]
    records = active if limit == 0 else active[:limit]
    return {
        "version": "muestra-normalizacion-metadatos-v1" if limit else "normalizacion-corpus-activo-v1",
        "generado_en": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "fuentes": {
            "inventario": inventory_path.relative_to(REPO_DIR).as_posix(),
            "exclusiones": exclusions_path.relative_to(REPO_DIR).as_posix(),
            "diccionario": dictionary_path.relative_to(REPO_DIR).as_posix(),
        },
        "denominador": {"historico": len(inventory["documentos"]), "activo": len(active), "muestra": len(records)},
        "documentos": [normalize_record(record, dictionary) for record in records],
    }


def review_rows(output: dict) -> list[dict]:
    rows = []
    for document in output["documentos"]:
        fields = {
            "autoria": document["autoria"],
            "tipo_documento": document["tipo_documento"],
            "ambito_aplicacion": document["ambito_aplicacion"],
            "paises": {"original": document["ambito_aplicacion_original"], "candidatos": document["paises"]},
            "subregiones": {"original": document["ambito_aplicacion_original"], "candidatos": document["subregiones"]},
            "sectores": document["sectores"],
            "organizaciones": {"original": document["referentes_dependencias_original"], "candidatos": document["organizaciones"]},
        }
        for field, payload in fields.items():
            candidates = payload.get("candidatos", [])
            if candidates and isinstance(candidates[0], dict):
                candidate_text = " | ".join(
                    f"{candidate['id']}:{candidate['nombre']}"
                    for candidate in candidates
                )
            else:
                candidate_text = " | ".join(str(candidate) for candidate in candidates)
            rows.append({
                "documento_id": document["documento_id"],
                "titulo": document["titulo"],
                "campo": field,
                "valor_original": payload.get("original", ""),
                "candidatos": candidate_text,
                "requiere_revision": payload.get("requiere_revision", bool(not candidates)),
                "decision": "",
                "observacion": "",
                "estado": "pendiente",
            })
    return rows


def write_review_queue(output: dict, path: Path) -> None:
    rows = review_rows(output)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = __import__("csv").DictWriter(file, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--exclusions", type=Path, default=DEFAULT_EXCLUSIONS)
    parser.add_argument("--dictionary", type=Path, default=DEFAULT_DICTIONARY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--review-output", type=Path, default=DEFAULT_REVIEW_OUTPUT)
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="Cantidad de documentos; 0 procesa todo el corpus activo")
    args = parser.parse_args()
    if args.limit < 0:
        parser.error("--limit debe ser mayor o igual que cero")
    output = build_output(args.inventory, args.exclusions, args.dictionary, args.limit)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_review_queue(output, args.review_output)
    print(json.dumps({"output": args.output.as_posix(), "review_output": args.review_output.as_posix(), **output["denominador"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()