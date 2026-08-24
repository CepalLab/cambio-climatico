"""Aplica adjudicaciones estructuralmente seguras a un derivado normalizado."""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


NORMALIZACION_DIR = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = NORMALIZACION_DIR / "salidas" / "muestra_normalizacion_metadatos_v1.json"
DEFAULT_OUTPUT = NORMALIZACION_DIR / "salidas" / "muestra_normalizada_v1.json"


def relation_rows(document: dict) -> list[dict]:
    rows = []
    for field in ("paises", "subregiones", "sectores", "organizaciones"):
        payload = document[field]
        candidates = payload.get("candidatos", []) if isinstance(payload, dict) else payload
        original = payload.get("original") if isinstance(payload, dict) else None
        for candidate in candidates:
            rows.append({
                "documento_id": document["documento_id"],
                "campo": field,
                "entidad_id": candidate["id"],
                "nombre": candidate["nombre"],
                "valor_original": original,
                "estado": "pendiente_revision",
                "metodo": "coincidencia_de_alias",
            })
    return rows


def apply(input_path: Path) -> dict:
    source = json.loads(input_path.read_text(encoding="utf-8"))
    documents = []
    relations = []
    pending = []
    for document in source["documentos"]:
        type_candidates = document["tipo_documento"]["candidatos"]
        type_decision = None
        if len(type_candidates) == 1:
            is_override = "override explícito de muestra" in type_candidates[0].get("aliases", [])
            type_decision = {
                "id": type_candidates[0]["id"],
                "nombre": type_candidates[0]["nombre"],
                "estado": "adjudicado_explicito" if is_override else "adjudicado_automaticamente",
                "metodo": "override_por_handle" if is_override else "alias_especifico_unico",
            }
        else:
            pending.append({
                "documento_id": document["documento_id"],
                "campo": "tipo_documento",
                "valor_original": document["tipo_documento"]["original"],
                "candidatos": type_candidates,
            })

        document_id = document["documento_id"]
        documents.append({
            "documento_id": document_id,
            "handle": document["handle"],
            "ruta_json": document["ruta_json"],
            "sha256_json": document["sha256_json"],
            "titulo": document["titulo"],
            "fecha": document.get("fecha"),
            "tipo_documento_original": document["tipo_documento"]["original"],
            "tipo_documento_normalizado": type_decision,
            "ambito_aplicacion": document["ambito_aplicacion"],
        })
        document_relations = relation_rows(document)
        relations.extend(document_relations)
        pending.extend(document_relations)
        pending.append({
            "documento_id": document_id,
            "campo": "ambito_aplicacion",
            "valor_original": document["ambito_aplicacion"]["original"],
            "candidatos": document["ambito_aplicacion"]["candidatos"],
            "detalle_subnacional": document["ambito_aplicacion"]["detalle_subnacional"],
        })
        if document["autoria"]["requiere_revision"] or not document["autoria"]["candidatos"]:
            pending.append({
                "documento_id": document_id,
                "campo": "autoria",
                "valor_original": document["autoria"]["original"],
                "candidatos": document["autoria"]["candidatos"],
            })

    return {
        "version": "muestra-normalizada-v1",
        "generado_en": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "fuente": input_path.name,
        "denominador": {
            "historico": source["denominador"]["historico"],
            "activo": source["denominador"]["activo"],
            "muestra": source["denominador"]["muestra"],
        },
        "documentos": documents,
        "relaciones": relations,
        "pendientes_revision": pending,
        "criterio_adjudicacion": "Solo se adjudica un tipo documental cuando existe un único alias específico; las relaciones y autorías permanecen pendientes.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = apply(args.input)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": args.output.as_posix(),
        "documents": len(result["documentos"]),
        "relations": len(result["relaciones"]),
        "pending": len(result["pendientes_revision"]),
        "types_adjudicated": sum(bool(document["tipo_documento_normalizado"]) for document in result["documentos"]),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()