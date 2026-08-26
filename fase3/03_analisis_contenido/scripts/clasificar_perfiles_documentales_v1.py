"""Genera una matriz candidata de objetos, dominios y funciones documentales."""

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ANALISIS_DIR = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ANALISIS_DIR / "salidas" / "perfiles_documentales_v1.json"
DEFAULT_JSON = ANALISIS_DIR / "salidas" / "matriz_documental_candidata_v1.json"
DEFAULT_MARKDOWN = ANALISIS_DIR / "salidas" / "panorama_documental_candidato_v1.md"
BASE_VERSION = "fase3-analitica-v1"

OBJECT_RULES = {
    "impactos_vulnerabilidad": ("impacto", "vulnerabil", "riesgo", "desastre", "evento extremo"),
    "adaptacion_resiliencia": ("adaptaci", "resilien", "gestión del riesgo", "gestion del riesgo"),
    "mitigacion_descarbonizacion": ("mitigaci", "emisiones", "descarbon", "energía renovable", "energia renovable", "carbono", "gei"),
    "transicion_productiva": ("transformación productiva", "transformacion productiva", "cambio estructural", "bioeconom", "economía circular", "economia circular", "empleo verde", "innovaci"),
    "gobernanza_capacidades": ("gobernanza", "institucional", "capacidad estatal", "regulaci", "participaci", "coordinaci", "escazú", "escazu"),
    "financiamiento_inversion": ("financiam", "inversi", "fiscal", "presupuesto", "bonos verdes", "impuesto al carbono"),
    "igualdad_proteccion_social": ("pobreza", "desigualdad", "género", "genero", "cuidados", "protección social", "proteccion social"),
    "territorio_ciudad": ("territorial", "territorio", "ciudad", "urbano", "municip", "subnacional", "vivienda", "infraestructura"),
    "ecosistemas_recursos": ("biodivers", "agua", "agrícola", "agricol", "bosque", "costa", "marino", "ecosistema", "alimentari"),
    "informacion_prospectiva": ("escenario", "proyecci", "indicador", "datos", "monitoreo", "estadíst", "estadist", "modelo"),
}

DOMAIN_RULES = {
    "ambiental": ("clima", "ambient", "emisiones", "ecosistema", "biodivers", "agua", "bosque"),
    "social": ("pobreza", "desigualdad", "género", "genero", "salud", "cuidados", "empleo", "protección social", "proteccion social"),
    "productivo": ("productiv", "industria", "innovaci", "cadena de valor", "agricultura", "agropecuari"),
    "macroeconomico": ("pib", "crecimiento", "deuda", "comercio", "macroecon", "inflaci"),
    "financiero": ("financiam", "inversi", "fiscal", "presupuesto", "bono", "impuesto"),
    "institucional": ("institucional", "gobernanza", "regulaci", "capacidad", "coordinaci", "participaci"),
    "territorial": ("territorio", "subnacional", "municip", "ciudad", "urbano", "vivienda", "infraestructura"),
    "sectorial": ("energ", "transporte", "agric", "agua", "salud", "industria", "vivienda", "pesca"),
    "informacion_prospectiva": ("escenario", "proyecci", "indicador", "datos", "monitoreo", "estadíst", "estadist", "modelo"),
}

FUNCTION_RULES = {
    "diagnostica": ("diagnóstico", "diagnostico", "brecha", "vulnerabil", "condicion", "limitaci"),
    "analiza": ("analiza", "análisis", "analisis", "estudia", "evalúa", "evalua"),
    "prospecta": ("proyecci", "escenario", "horizonte", "futuro", "trayectoria"),
    "evalua_implementacion": ("implementaci", "avance", "evaluación", "evaluacion", "cumplimiento"),
    "propone_intervenir": ("se recomienda", "recomendaci", "se propone", "debe", "debería", "deberia"),
}

FIELD_WEIGHTS = {
    "title": 6,
    "research_question": 5,
    "scope_sectorial": 3,
    "narrative_summary": 3,
    "main_findings": 1,
    "conclusions": 1,
    "recommendations": 1,
    "abstract": 1,
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stringify_items(items: list) -> str:
    return " ".join(item if isinstance(item, str) else json.dumps(item, ensure_ascii=False) for item in items)


def profile_text(profile: dict) -> dict[str, str]:
    document = profile["document_profile"]
    metadata = profile["metadata"]
    fields = {
        "title": metadata.get("title"),
        "abstract": metadata.get("abstract"),
        "research_question": document.get("research_question"),
        "scope_sectorial": (document.get("scope") or {}).get("sectorial"),
        "narrative_summary": document.get("narrative_summary"),
        "main_findings": stringify_items(document.get("main_findings") or []),
        "conclusions": stringify_items(document.get("conclusions") or []),
        "recommendations": stringify_items(document.get("recommendations") or []),
    }
    return {name: str(value).casefold() for name, value in fields.items() if value}


def apply_rules(fields: dict[str, str], rules: dict[str, tuple[str, ...]], minimum_score: int) -> list[dict]:
    assignments = []
    for identifier, terms in rules.items():
        matches_by_field = {
            field: [term for term in terms if term in text]
            for field, text in fields.items()
        }
        matches_by_field = {field: matches for field, matches in matches_by_field.items() if matches}
        score = sum(FIELD_WEIGHTS[field] * len(matches) for field, matches in matches_by_field.items())
        if score >= minimum_score:
            assignments.append({"id": identifier, "score": score, "matched_terms_by_field": matches_by_field})
    return sorted(assignments, key=lambda item: (-item["score"], item["id"]))


def classify_profile(profile: dict) -> dict:
    fields = profile_text(profile)
    objects = apply_rules(fields, OBJECT_RULES, minimum_score=5)
    domains = apply_rules(fields, DOMAIN_RULES, minimum_score=5)
    functions = apply_rules(fields, FUNCTION_RULES, minimum_score=4)
    return {
        "document_id": profile["document_id"],
        "period_id": profile["period_id"],
        "source": profile["source"],
        "metadata": {"title": profile["metadata"]["title"], "year": profile["metadata"]["year"], "division": profile["metadata"]["division"]},
        "document_profile_summary": {
            "research_question": profile["document_profile"]["research_question"],
            "scope": profile["document_profile"]["scope"],
            "territorial_scope": profile["document_profile"]["territorial_scope"],
            "existing_typology": profile["document_profile"]["existing_typology"],
            "conclusions": profile["document_profile"]["conclusions"],
            "recommendations": profile["document_profile"]["recommendations"],
        },
        "candidate_assignments": {
            "objects": objects,
            "primary_object": objects[0]["id"] if objects else None,
            "domains": domains,
            "functions": functions,
            "source_fields": sorted(fields),
            "status": "candidate_weighted_keyword_v1",
        },
    }


def markdown_table(rows: list[tuple[str, str, int]], heading: str) -> str:
    lines = [heading, "", "| Periodo | Categoria | Documentos |", "|---|---|---:|"]
    lines.extend(f"| {period} | {category} | {count} |" for period, category, count in rows)
    return "\n".join(lines)


def aggregate(matrix: list[dict], key: str) -> list[tuple[str, str, int]]:
    counts = Counter()
    for profile in matrix:
        values = profile["candidate_assignments"][key]
        for value in values:
            counts[(profile["period_id"], value["id"])] += 1
    return [(period, category, count) for (period, category), count in sorted(counts.items())]


def build_panorama(matrix: list[dict]) -> str:
    primary = Counter((profile["period_id"], profile["candidate_assignments"]["primary_object"] or "sin_asignacion") for profile in matrix)
    primary_rows = [(period, category, count) for (period, category), count in sorted(primary.items())]
    coverage = Counter(profile["period_id"] for profile in matrix)
    territorial_levels = Counter(
        (profile["period_id"], candidate.get("id"))
        for profile in matrix
        for candidate in profile["document_profile_summary"]["territorial_scope"]["normalized_candidates"]
        if candidate.get("id")
    )
    typology_primary = Counter(
        (profile["period_id"], (profile["document_profile_summary"]["existing_typology"].get("transformacion_primaria") or {}).get("nombre") or "Sin clasificar")
        for profile in matrix
    )
    parts = [
        "# Panorama documental candidato v1", "",
        f"**Base:** `{BASE_VERSION}`  ",
        f"**Universo:** {len(matrix)} documentos activos; 6 exclusiones aplicadas.", "",
        "Las asignaciones de este panorama son candidatas generadas por reglas lexicas transparentes. No son codificacion experta ni relaciones causales.", "",
        markdown_table([(period, "documentos", count) for period, count in sorted(coverage.items())], "## Cobertura por periodo"), "",
        markdown_table(primary_rows, "## Objeto principal candidato"), "",
        markdown_table(aggregate(matrix, "domains"), "## Dominios candidatos (multi-etiqueta)"), "",
        markdown_table(aggregate(matrix, "functions"), "## Funciones analiticas candidatas (multi-etiqueta)"), "",
        markdown_table([(period, category, count) for (period, category), count in sorted(territorial_levels.items())], "## Ambitos territoriales candidatos (normalizacion v1)"), "",
        markdown_table([(period, category, count) for (period, category), count in sorted(typology_primary.items())], "## Tipologia existente: transformacion primaria"), "",
        "## Uso correcto", "",
        "Este archivo sirve para detectar patrones y seleccionar casos de calibracion. Toda conclusion sobre cambios de foco, variables o relaciones debe revisarse contra los perfiles directos antes de promoverse a hallazgo.",
    ]
    return "\n".join(parts) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    profiles = json.loads(args.input.read_text(encoding="utf-8"))
    matrix = [classify_profile(profile) for profile in profiles["profiles"]]
    if len(matrix) != profiles["source"]["documents_active"]:
        raise ValueError("La matriz no conserva el denominador del perfil directo.")
    output = {
        "version": "matriz-documental-candidata-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base_version": BASE_VERSION,
        "source": {"profiles_path": args.input.as_posix(), "profiles_sha256": sha256_file(args.input), "documents_active": len(matrix), "exclusions_applied": 6},
        "rule_set": "weighted_keyword_rules_v1",
        "limitations": [
            "Las reglas lexicas detectan presencia de terminos, no prioridad conceptual ni causalidad.",
            "Los documentos pueden tener multiples objetos, dominios y funciones.",
            "La asignacion requiere calibracion humana antes de usarse como conclusion agregada.",
        ],
        "matrix": matrix,
    }
    args.json.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.markdown.write_text(build_panorama(matrix), encoding="utf-8")
    print(json.dumps({"json": args.json.as_posix(), "markdown": args.markdown.as_posix(), "documents": len(matrix)}, ensure_ascii=False))


if __name__ == "__main__":
    main()