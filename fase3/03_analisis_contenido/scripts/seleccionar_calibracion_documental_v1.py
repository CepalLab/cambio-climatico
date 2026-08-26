"""Selecciona perfiles documentales diversos para calibrar la taxonomia v1."""

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ANALISIS_DIR = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ANALISIS_DIR / "salidas" / "matriz_documental_candidata_v1.json"
DEFAULT_OUTPUT = ANALISIS_DIR / "salidas" / "calibracion_documental_taxonomia_v1.json"
DEFAULT_MARKDOWN = ANALISIS_DIR / "salidas" / "calibracion_documental_taxonomia_v1.md"


def stable_key(*values: object) -> str:
    return hashlib.sha256("|".join(str(value) for value in values).encode("utf-8")).hexdigest()


def select_profiles(matrix: list[dict]) -> list[dict]:
    by_object: dict[str, list[dict]] = {}
    for profile in matrix:
        primary = profile["candidate_assignments"]["primary_object"]
        if primary:
            by_object.setdefault(primary, []).append(profile)

    period_counts: Counter = Counter()
    selected = []
    for object_id in sorted(by_object):
        candidates = by_object[object_id]
        profile = min(
            candidates,
            key=lambda item: (period_counts[item["period_id"]], stable_key(object_id, item["document_id"])),
        )
        period_counts[profile["period_id"]] += 1
        selected.append(profile)
    return selected


def write_markdown(selected: list[dict], path: Path) -> None:
    parts = [
        "# Calibracion documental de taxonomia v1", "",
        "Esta muestra cubre un perfil candidato por objeto principal y distribuye los casos entre periodos cuando es posible. No valida las asignaciones: sirve para corregir la taxonomia antes de agregar resultados.", "",
    ]
    for index, profile in enumerate(selected, start=1):
        assignments = profile["candidate_assignments"]
        document = profile["document_profile_summary"]
        parts.extend([
            f"## Caso {index}: {profile['metadata']['title']}", "",
            f"- **Periodo:** {profile['period_id']} ({profile['metadata']['year']})",
            f"- **Objeto principal candidato:** `{assignments['primary_object']}`",
            f"- **Objetos candidatos:** {', '.join(item['id'] for item in assignments['objects'])}",
            f"- **Dominios candidatos:** {', '.join(item['id'] for item in assignments['domains'])}",
            f"- **Funciones candidatas:** {', '.join(item['id'] for item in assignments['functions'])}",
            f"- **Pregunta:** {document['research_question']}",
            f"- **Ambito:** {(document['scope'] or {}).get('ambito_aplicacion', '')}",
            f"- **Sectorial:** {(document['scope'] or {}).get('sectorial', '')}",
            "",
            "**Revision solicitada:** confirmar o corregir el objeto principal, los dominios realmente centrales y la funcion dominante. No se revisan citas en esta etapa.",
            "",
        ])
    path.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--json", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    source = json.loads(args.input.read_text(encoding="utf-8"))
    selected = select_profiles(source["matrix"])
    output = {
        "version": "calibracion-documental-taxonomia-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base_version": source["base_version"],
        "source_matrix": args.input.as_posix(),
        "purpose": "Calibrar la taxonomia documental antes de usar asignaciones candidatas en agregados.",
        "profiles": selected,
    }
    args.json.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(selected, args.markdown)
    print(json.dumps({"json": args.json.as_posix(), "markdown": args.markdown.as_posix(), "documents": len(selected)}, ensure_ascii=False))


if __name__ == "__main__":
    main()