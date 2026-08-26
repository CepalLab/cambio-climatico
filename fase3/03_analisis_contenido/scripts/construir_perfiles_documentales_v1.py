"""Construye perfiles documentales trazables desde los JSON canonicos de Fase 2."""

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ANALISIS_DIR = Path(__file__).resolve().parents[1]
FASE3_DIR = ANALISIS_DIR.parent
REPO_DIR = FASE3_DIR.parent
DEFAULT_NORMALIZED = FASE3_DIR / "01_normalizacion" / "salidas" / "corpus_activo_normalizado_v1.json"
DEFAULT_JSON = ANALISIS_DIR / "salidas" / "perfiles_documentales_v1.json"
DEFAULT_MARKDOWN = ANALISIS_DIR / "salidas" / "panorama_perfiles_documentales_v1.md"
BASE_VERSION = "fase3-analitica-v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def period_for_year(year: int | None) -> str | None:
    if year is None:
        return None
    if 2015 <= year <= 2018:
        return "P1"
    if 2019 <= year <= 2022:
        return "P2"
    if 2023 <= year <= 2026:
        return "P3"
    return None


def conclusions_and_recommendations(enriched: dict) -> tuple[list, list, str | None]:
    value = enriched.get("conclusiones_recomendaciones")
    if isinstance(value, dict):
        return value.get("conclusiones") or [], value.get("recomendaciones") or [], value.get("nota")
    if isinstance(value, list):
        return value, [], "Formato legado de lista plana."
    return [], [], "Campo ausente."


def build_profile(normalized_document: dict) -> dict:
    canonical_path = REPO_DIR / normalized_document["ruta_json"]
    canonical = json.loads(canonical_path.read_text(encoding="utf-8"))
    document = canonical.get("documento") or {}
    enriched = canonical.get("resumen_enriquecido") or {}
    typology = canonical.get("tipologia") or {}
    application_levels = normalized_document.get("ambito_aplicacion") or {}
    conclusions, recommendations, note = conclusions_and_recommendations(enriched)
    if document.get("handle") != normalized_document["documento_id"]:
        raise ValueError(f"Handle inconsistente en {canonical_path}")
    return {
        "document_id": normalized_document["documento_id"],
        "period_id": period_for_year(normalized_document.get("anio")),
        "source": {"source_path": normalized_document["ruta_json"], "source_sha256": normalized_document["sha256_json"]},
        "metadata": {
            "title": normalized_document.get("titulo"),
            "year": normalized_document.get("anio"),
            "publication_date": normalized_document.get("fecha"),
            "division": normalized_document.get("division"),
            "document_type": normalized_document.get("tipo_documento_normalizado"),
            "topics": normalized_document.get("topic_spa") or [],
            "sdg": normalized_document.get("sdg") or [],
            "application_levels": application_levels,
            "abstract": normalized_document.get("abstract"),
            "body_pages": document.get("paginas_cuerpo"),
            "language": document.get("idioma"),
        },
        "document_profile": {
            "research_question": enriched.get("pregunta_investigacion"),
            "scope": enriched.get("alcance") or {},
            "narrative_summary": enriched.get("resumen_narrativo"),
            "main_findings": enriched.get("hallazgos_principales") or [],
            "conclusions": conclusions,
            "recommendations": recommendations,
            "conclusions_recommendations_note": note,
            "territorial_scope": {
                "normalized_candidates": application_levels.get("candidatos") or [],
                "requires_review": application_levels.get("requiere_revision"),
                "normalization_method": application_levels.get("metodo"),
                "original_normalized_scope": application_levels.get("original"),
                "typology_application_level": typology.get("nivel_aplicacion"),
            },
            "existing_typology": typology,
        },
        "analysis_status": "direct_canonical_profile",
    }


def table(rows: list[tuple[str, int]], heading: str) -> str:
    lines = [heading, "", "| Categoria | Documentos |", "|---|---:|"]
    lines.extend(f"| {label} | {count} |" for label, count in rows)
    return "\n".join(lines)


def build_panorama(profiles: list[dict], source_path: Path) -> str:
    by_period = Counter(profile["period_id"] for profile in profiles)
    by_division = Counter(profile["metadata"]["division"] or "Sin division" for profile in profiles)
    by_type = Counter((profile["metadata"]["document_type"] or {}).get("nombre") or "Sin clasificar" for profile in profiles)
    by_territorial_level = Counter(
        candidate.get("id")
        for profile in profiles
        for candidate in profile["document_profile"]["territorial_scope"]["normalized_candidates"]
        if candidate.get("id")
    )
    by_primary_transformation = Counter(
        (profile["document_profile"]["existing_typology"].get("transformacion_primaria") or {}).get("nombre") or "Sin clasificar"
        for profile in profiles
    )
    coverage = {
        "pregunta_investigacion": sum(bool(profile["document_profile"]["research_question"]) for profile in profiles),
        "ambito_aplicacion": sum(bool(profile["document_profile"]["scope"].get("ambito_aplicacion")) for profile in profiles),
        "resumen_narrativo": sum(bool(profile["document_profile"]["narrative_summary"]) for profile in profiles),
        "hallazgos_principales": sum(bool(profile["document_profile"]["main_findings"]) for profile in profiles),
        "conclusiones": sum(bool(profile["document_profile"]["conclusions"]) for profile in profiles),
        "recomendaciones": sum(bool(profile["document_profile"]["recommendations"]) for profile in profiles),
    }
    parts = [
        "# Panorama de perfiles documentales v1", "",
        f"**Base:** `{BASE_VERSION}`  ", f"**Fuente:** `{source_path.name}`  ",
        f"**Universo:** {len(profiles)} documentos activos; 6 exclusiones aplicadas.", "",
        "Este panorama describe campos directos de los JSON canonicos. Todavia no aplica una taxonomia inferida de objetos, variables o relaciones.", "",
        table(sorted(by_period.items()), "## Documentos por periodo"), "",
        table(sorted(by_type.items(), key=lambda item: (-item[1], item[0])), "## Tipos documentales"), "",
        table(sorted(by_division.items(), key=lambda item: (-item[1], item[0])), "## Divisiones"), "",
        table(sorted(by_territorial_level.items(), key=lambda item: (-item[1], item[0])), "## Ambitos territoriales candidatos"), "",
        table(sorted(by_primary_transformation.items(), key=lambda item: (-item[1], item[0])), "## Tipologia existente: transformacion primaria"), "",
        table(sorted(coverage.items()), "## Cobertura de campos enriquecidos"), "",
        "## Siguiente capa", "",
        "La taxonomia documental se aplicara sobre preguntas, resumenes, hallazgos, conclusiones y recomendaciones. Las citas de seccion se usan despues para verificar los hallazgos agregados.",
    ]
    return "\n".join(parts) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_NORMALIZED)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    normalized = json.loads(args.input.read_text(encoding="utf-8"))
    profiles = [build_profile(document) for document in normalized["documentos"]]
    if len(profiles) != 238 or len({profile["document_id"] for profile in profiles}) != len(profiles):
        raise ValueError("El perfil documental no conserva 238 identificadores unicos.")
    output = {
        "version": "perfiles-documentales-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base_version": BASE_VERSION,
        "source": {"normalized_path": args.input.as_posix(), "normalized_sha256": sha256_file(args.input), "documents_active": len(profiles), "exclusions_applied": 6},
        "profiles": profiles,
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.markdown.write_text(build_panorama(profiles, args.input), encoding="utf-8")
    print(json.dumps({"json": args.json.as_posix(), "markdown": args.markdown.as_posix(), "documents": len(profiles)}, ensure_ascii=False))


if __name__ == "__main__":
    main()