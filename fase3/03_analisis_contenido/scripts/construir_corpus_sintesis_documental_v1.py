"""Construye el corpus completo para la sintesis documental de Fase 3.3."""

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ANALISIS_DIR = Path(__file__).resolve().parents[1]
DEFAULT_PROFILES = ANALISIS_DIR / "salidas" / "perfiles_documentales_v1.json"
DEFAULT_MATRIX = ANALISIS_DIR / "salidas" / "matriz_documental_candidata_v1.json"
DEFAULT_JSON = ANALISIS_DIR / "salidas" / "corpus_sintesis_documental_v1.json"
DEFAULT_MARKDOWN = ANALISIS_DIR / "salidas" / "cobertura_sintesis_documental_v1.md"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profiles", type=Path, default=DEFAULT_PROFILES)
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    profiles_source = json.loads(args.profiles.read_text(encoding="utf-8"))
    matrix_source = json.loads(args.matrix.read_text(encoding="utf-8"))
    matrix_by_id = {item["document_id"]: item for item in matrix_source["matrix"]}
    profiles = profiles_source["profiles"]
    if len(profiles) != 238 or set(matrix_by_id) != {item["document_id"] for item in profiles}:
        raise ValueError("Perfiles y matriz no representan el mismo universo activo.")

    documents = []
    conclusions = []
    recommendations = []
    for profile in profiles:
        matrix = matrix_by_id[profile["document_id"]]
        document = {
            "document_id": profile["document_id"],
            "period_id": profile["period_id"],
            "source": profile["source"],
            "metadata": profile["metadata"],
            "document_profile": profile["document_profile"],
            "candidate_assignments": matrix["candidate_assignments"],
        }
        documents.append(document)
        context = {
            "document_id": document["document_id"],
            "period_id": document["period_id"],
            "title": document["metadata"]["title"],
            "primary_object_candidate": document["candidate_assignments"]["primary_object"],
            "territorial_scope": document["document_profile"]["territorial_scope"],
            "existing_typology": document["document_profile"]["existing_typology"],
        }
        conclusions.extend({**context, "text": text} for text in document["document_profile"]["conclusions"])
        recommendations.extend({**context, "text": text} for text in document["document_profile"]["recommendations"])

    by_period = Counter(item["period_id"] for item in documents)
    output = {
        "version": "corpus-sintesis-documental-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base_version": profiles_source["base_version"],
        "source": {
            "profiles_path": args.profiles.as_posix(),
            "profiles_sha256": sha256_file(args.profiles),
            "matrix_path": args.matrix.as_posix(),
            "matrix_sha256": sha256_file(args.matrix),
            "documents_active": len(documents),
            "exclusions_applied": 6,
        },
        "limitations": [
            "Los campos documentales son directos de los JSON canonicos.",
            "Los objetos, dominios y funciones son candidatos calibrados, no codificacion experta exhaustiva.",
            "Las conclusiones y recomendaciones no estan presentes en todos los documentos y su ausencia es informativa.",
        ],
        "coverage": {
            "documents_by_period": dict(sorted(by_period.items())),
            "documents_with_conclusions": sum(bool(item["document_profile"]["conclusions"]) for item in documents),
            "documents_with_recommendations": sum(bool(item["document_profile"]["recommendations"]) for item in documents),
            "conclusion_items": len(conclusions),
            "recommendation_items": len(recommendations),
        },
        "documents": documents,
        "conclusions": conclusions,
        "recommendations": recommendations,
    }
    args.json.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    markdown = "\n".join([
        "# Cobertura de sintesis documental v1", "",
        f"- Documentos activos: {len(documents)}.",
        f"- P1/P2/P3: {by_period['P1']}/{by_period['P2']}/{by_period['P3']}.",
        f"- Documentos con conclusiones: {output['coverage']['documents_with_conclusions']}.",
        f"- Documentos con recomendaciones: {output['coverage']['documents_with_recommendations']}.",
        f"- Items de conclusiones: {len(conclusions)}.",
        f"- Items de recomendaciones: {len(recommendations)}.",
        "",
        "El JSON asociado contiene los 238 perfiles completos con clasificacion candidata, conclusiones y recomendaciones para la sintesis a escala total.",
    ]) + "\n"
    args.markdown.write_text(markdown, encoding="utf-8")
    print(json.dumps({"json": args.json.as_posix(), "markdown": args.markdown.as_posix(), **output["coverage"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()