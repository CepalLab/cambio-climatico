"""Construye el paquete documental para la primera sintesis global del corpus."""

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ANALISIS_DIR = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ANALISIS_DIR / "salidas" / "matriz_documental_candidata_v1.json"
DEFAULT_PROFILES = ANALISIS_DIR / "salidas" / "perfiles_documentales_v1.json"
DEFAULT_JSON = ANALISIS_DIR / "salidas" / "paquete_panoramico_documental_v1.json"
DEFAULT_MARKDOWN = ANALISIS_DIR / "salidas" / "paquete_panoramico_documental_v1.md"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def aggregate_primary(matrix: list[dict]) -> list[dict]:
    counts = Counter((item["period_id"], item["candidate_assignments"]["primary_object"] or "sin_asignacion") for item in matrix)
    return [{"period_id": period, "primary_object": object_id, "documents": count} for (period, object_id), count in sorted(counts.items())]


def aggregate_territory(matrix: list[dict]) -> list[dict]:
    counts = Counter(
        (item["period_id"], candidate["id"])
        for item in matrix
        for candidate in item["document_profile_summary"]["territorial_scope"]["normalized_candidates"]
        if candidate.get("id")
    )
    return [{"period_id": period, "territorial_scope": scope, "documents": count, "status": "candidate_v1"} for (period, scope), count in sorted(counts.items())]


def aggregate_typology(matrix: list[dict]) -> list[dict]:
    counts = Counter(
        (item["period_id"], (item["document_profile_summary"]["existing_typology"].get("transformacion_primaria") or {}).get("nombre") or "Sin clasificar")
        for item in matrix
    )
    return [{"period_id": period, "primary_transformation": transformation, "documents": count} for (period, transformation), count in sorted(counts.items())]


def representatives(matrix: list[dict], profiles: dict[str, dict]) -> list[dict]:
    groups: dict[tuple[str, str], list[dict]] = {}
    for item in matrix:
        primary = item["candidate_assignments"]["primary_object"]
        if primary:
            groups.setdefault((item["period_id"], primary), []).append(item)
    selected = []
    for (period_id, primary), candidates in sorted(groups.items()):
        item = max(
            candidates,
            key=lambda candidate: next(assignment["score"] for assignment in candidate["candidate_assignments"]["objects"] if assignment["id"] == primary),
        )
        profile = profiles[item["document_id"]]
        selected.append({
            "period_id": period_id,
            "primary_object_candidate": primary,
            "selection_rule": "Mayor puntaje ponderado del objeto primario dentro de la celda periodo-objeto.",
            "document": profile,
        })
    return selected


def markdown_table(rows: list[dict], columns: list[tuple[str, str]], heading: str) -> str:
    lines = [heading, "", "| " + " | ".join(label for label, _ in columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
    lines.extend("| " + " | ".join(str(row.get(key, "")) for _, key in columns) + " |" for row in rows)
    return "\n".join(lines)


def build_markdown(package: dict) -> str:
    aggregates = package["aggregates"]
    parts = [
        "# Paquete panoramico documental v1", "",
        "Este paquete es la entrada para la primera sintesis global. Los objetos son candidatos calibrados; territorio normalizado y tipologia son ejes complementarios. Las citas quedan fuera de este paquete y se recuperan para verificar hallazgos concretos.", "",
        markdown_table(aggregates["primary_objects"], [("Periodo", "period_id"), ("Objeto principal candidato", "primary_object"), ("Documentos", "documents")], "## Objetos principales candidatos"), "",
        markdown_table(aggregates["territorial_scope"], [("Periodo", "period_id"), ("Ambito", "territorial_scope"), ("Documentos", "documents")], "## Ambitos territoriales candidatos"), "",
        markdown_table(aggregates["primary_typology"], [("Periodo", "period_id"), ("Transformacion primaria", "primary_transformation"), ("Documentos", "documents")], "## Tipologia existente"), "",
        "## Documentos representativos", "",
    ]
    for item in package["representatives"]:
        document = item["document"]
        profile = document["document_profile"]
        typology = profile["existing_typology"]
        parts.extend([
            f"### {item['period_id']} - {item['primary_object_candidate']}: {document['metadata']['title']}", "",
            f"- **Pregunta:** {profile['research_question']}",
            f"- **Ambito:** {(profile['scope'] or {}).get('ambito_aplicacion', '')}",
            f"- **Conclusion de tipologia:** {(typology.get('transformacion_primaria') or {}).get('nombre', '')} / {(typology.get('transformacion_secundaria') or {}).get('nombre', '')}",
            f"- **Tension dialectica:** {((typology.get('razonamiento_5_pasos') or {}).get('tension_dialectica') or '')}",
            f"- **Conclusiones:** {' | '.join(profile['conclusions'][:2])}",
            f"- **Recomendaciones:** {' | '.join(profile['recommendations'][:2])}",
            "",
        ])
    return "\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--profiles", type=Path, default=DEFAULT_PROFILES)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    matrix_source = json.loads(args.matrix.read_text(encoding="utf-8"))
    profile_source = json.loads(args.profiles.read_text(encoding="utf-8"))
    matrix = matrix_source["matrix"]
    profiles = {item["document_id"]: item for item in profile_source["profiles"]}
    if len(matrix) != 238 or len(profiles) != 238 or set(item["document_id"] for item in matrix) != set(profiles):
        raise ValueError("Matriz y perfiles no conservan el mismo universo activo.")
    package = {
        "version": "paquete-panoramico-documental-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base_version": matrix_source["base_version"],
        "source": {
            "matrix_path": args.matrix.as_posix(),
            "matrix_sha256": sha256_file(args.matrix),
            "profiles_path": args.profiles.as_posix(),
            "profiles_sha256": sha256_file(args.profiles),
            "documents_active": 238,
            "exclusions_applied": 6,
        },
        "limitations": [
            "Los objetos principales provienen de una matriz candidata calibrada, no de codificacion experta exhaustiva.",
            "Los ambitos territoriales son candidatos normalizados v1.",
            "La tipologia y tension dialectica se conservan como clasificacion complementaria ya adjudicada.",
        ],
        "aggregates": {
            "primary_objects": aggregate_primary(matrix),
            "territorial_scope": aggregate_territory(matrix),
            "primary_typology": aggregate_typology(matrix),
        },
        "representatives": representatives(matrix, profiles),
    }
    args.json.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.markdown.write_text(build_markdown(package), encoding="utf-8")
    print(json.dumps({"json": args.json.as_posix(), "markdown": args.markdown.as_posix(), "representatives": len(package["representatives"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()