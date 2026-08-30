"""Verifica ejes analiticos directamente contra los JSON canonicos activos."""

import argparse
import hashlib
import json
import re
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ANALISIS_DIR = Path(__file__).resolve().parents[1]
FASE3_DIR = ANALISIS_DIR.parent
REPO_DIR = FASE3_DIR.parent
DEFAULT_NORMALIZED = FASE3_DIR / "01_normalizacion" / "salidas" / "corpus_activo_normalizado_v1.json"
DEFAULT_JSON = ANALISIS_DIR / "salidas" / "verificacion_ejes_canonicos_v1.json"
DEFAULT_MARKDOWN = ANALISIS_DIR / "salidas" / "verificacion_ejes_canonicos_v1.md"
BASE_VERSION = "fase3-analitica-v1"

CONCEPTS = {
    "perdidas_danos": {
        "label": "Pérdidas y daños",
        "pattern": re.compile(r"\b(?:p[eé]rdidas?\s+y\s+da[nñ]os?|da[nñ]os?\s+y\s+p[eé]rdidas?)\b", re.IGNORECASE),
    },
    "transicion_justa": {
        "label": "Transición justa",
        "pattern": re.compile(r"\btransici[oó]n\s+justa\b", re.IGNORECASE),
    },
    "responsabilidades_diferenciadas": {
        "label": "Responsabilidades comunes pero diferenciadas",
        "pattern": re.compile(r"\bresponsabilidades?\s+comunes?\s+pero\s+diferenciadas?\b", re.IGNORECASE),
    },
}

POLICY_TERMS = ("fondo", "mecanismo", "cop", "financ", "negoci", "derech", "acceso", "acuerdo")
DAMAGE_TERMS = ("hurac", "torment", "desastr", "impact", "evaluaci", "reconstru", "infraestructura", "riesgo")


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


def normalized_text(value: str) -> str:
    return "".join(
        character
        for character in unicodedata.normalize("NFD", value.lower())
        if unicodedata.category(character) != "Mn"
    )


def nearest_page(value: object, inherited: object | None) -> object | None:
    if isinstance(value, dict) and value.get("pagina") is not None:
        return value["pagina"]
    return inherited


def string_values(value: object, path: str = "$", page: object | None = None, context: str = ""):
    if isinstance(value, dict):
        page = nearest_page(value, page)
        context = json.dumps(value, ensure_ascii=False)
        for key, nested in value.items():
            yield from string_values(nested, f"{path}.{key}", page, context)
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            yield from string_values(nested, f"{path}[{index}]", page, context)
    elif isinstance(value, str):
        yield path, value, page, context


def excerpt(value: str, match: re.Match[str], width: int = 440) -> str:
    start = max(match.start() - width // 2, 0)
    end = min(match.end() + width // 2, len(value))
    prefix = "..." if start else ""
    suffix = "..." if end < len(value) else ""
    return f"{prefix}{value[start:end].strip()}{suffix}"


def classify_loss_and_damage(context: str) -> str:
    normalized = normalized_text(context)
    has_policy = any(term in normalized for term in POLICY_TERMS)
    has_damage = any(term in normalized for term in DAMAGE_TERMS)
    if has_policy and not has_damage:
        return "politica_financiamiento_candidata"
    if has_damage and not has_policy:
        return "evaluacion_danos_candidata"
    return "requiere_revision"


def matches_for_document(document: dict, canonical: dict) -> list[dict]:
    evidence = []
    seen = set()
    for path, text, page, context in string_values(canonical):
        for concept_id, concept in CONCEPTS.items():
            match = concept["pattern"].search(text)
            if not match:
                continue
            key = (concept_id, normalized_text(text), str(page))
            if key in seen:
                continue
            seen.add(key)
            evidence.append(
                {
                    "concept_id": concept_id,
                    "path": path,
                    "page": page,
                    "quote": excerpt(text, match),
                    "candidate_sense": classify_loss_and_damage(context) if concept_id == "perdidas_danos" else None,
                }
            )
    return evidence


def build_output(normalized: dict, normalized_path: Path) -> dict:
    documents = []
    concept_documents = {concept_id: [] for concept_id in CONCEPTS}
    for document in normalized["documentos"]:
        canonical_path = REPO_DIR / document["ruta_json"]
        canonical = json.loads(canonical_path.read_text(encoding="utf-8"))
        evidence = matches_for_document(document, canonical)
        record = {
            "document_id": document["documento_id"],
            "title": document.get("titulo"),
            "year": document.get("anio"),
            "period_id": period_for_year(document.get("anio")),
            "source_path": document["ruta_json"],
            "source_sha256": document["sha256_json"],
            "evidence": evidence,
        }
        documents.append(record)
        for concept_id in CONCEPTS:
            if any(item["concept_id"] == concept_id for item in evidence):
                concept_documents[concept_id].append(record)

    if len(documents) != 238 or len({document["document_id"] for document in documents}) != 238:
        raise ValueError("La verificacion debe recorrer exactamente 238 documentos activos unicos.")

    summaries = {}
    for concept_id, concept in CONCEPTS.items():
        matching_documents = concept_documents[concept_id]
        evidence = [item for document in matching_documents for item in document["evidence"] if item["concept_id"] == concept_id]
        summaries[concept_id] = {
            "label": concept["label"],
            "documents": len(matching_documents),
            "documents_by_period": dict(sorted(Counter(document["period_id"] or "sin_fecha" for document in matching_documents).items())),
            "evidence_candidates": len(evidence),
            "candidate_senses": dict(sorted(Counter(item["candidate_sense"] for item in evidence if item["candidate_sense"]).items())),
        }

    return {
        "version": "verificacion-ejes-canonicos-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base_version": BASE_VERSION,
        "method": {
            "input": normalized_path.as_posix(),
            "input_sha256": sha256_file(normalized_path),
            "documents_active": len(documents),
            "exclusions_applied": 6,
            "matching": "Regex sobre todos los valores de texto de cada JSON canonico activo; conteo por documento con al menos una coincidencia.",
            "loss_and_damage_classification": "Clasificacion candidata por terminos de contexto; requiere revision humana antes de informar sentidos sustantivos.",
        },
        "summaries": summaries,
        "documents": documents,
    }


def markdown_report(output: dict) -> str:
    parts = [
        "# Verificacion de ejes canonicos v1",
        "",
        f"**Base:** `{output['base_version']}`  ",
        f"**Universo:** {output['method']['documents_active']} documentos activos; {output['method']['exclusions_applied']} exclusiones aplicadas.",
        "",
        "La busqueda recorre todos los valores de texto de los JSON canonicos activos. Los conteos son por documento con al menos una coincidencia; no prueban por si solos importancia sustantiva.",
        "",
        "| Eje | Documentos | P1 | P2 | P3 | Sin fecha | Candidatos de evidencia |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for summary in output["summaries"].values():
        periods = summary["documents_by_period"]
        parts.append(
            f"| {summary['label']} | {summary['documents']} | {periods.get('P1', 0)} | {periods.get('P2', 0)} | {periods.get('P3', 0)} | {periods.get('sin_fecha', 0)} | {summary['evidence_candidates']} |"
        )
    loss_summary = output["summaries"]["perdidas_danos"]
    parts.extend(
        [
            "",
            "## Perdidas y danos: clasificacion candidata",
            "",
            "La distincion entre evaluacion de danos y marco politico-financiero se genera como candidata por contexto. Debe revisarse documento por documento antes de afirmarla en el informe.",
            "",
            "| Sentido candidato | Coincidencias |",
            "|---|---:|",
        ]
    )
    for sense, count in loss_summary["candidate_senses"].items():
        parts.append(f"| {sense} | {count} |")
    parts.extend(
        [
            "",
            "## Trazabilidad",
            "",
            "El JSON hermano conserva, por candidato de evidencia, `document_id`, periodo, ruta y hash de fuente, ruta interna, pagina cuando existe y extracto textual. La seleccion para la sintesis v2 requiere recuperacion y revision de la cita completa.",
            "",
        ]
    )
    return "\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_NORMALIZED)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    normalized = json.loads(args.input.read_text(encoding="utf-8"))
    output = build_output(normalized, args.input)
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.markdown.write_text(markdown_report(output), encoding="utf-8")
    print(json.dumps({"json": args.json.as_posix(), "markdown": args.markdown.as_posix(), "summaries": output["summaries"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()