"""Extrae tensiones dialécticas canónicas para la expansión analítica v2."""

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ANALISIS_DIR = Path(__file__).resolve().parents[1]
FASE3_DIR = ANALISIS_DIR.parent
REPO_DIR = FASE3_DIR.parent
INPUT_PATH = FASE3_DIR / "01_normalizacion" / "salidas" / "corpus_activo_normalizado_v1.json"
OUTPUT_JSON = ANALISIS_DIR / "salidas" / "tensiones_dialecticas_v1.json"
OUTPUT_MD = ANALISIS_DIR / "salidas" / "tensiones_dialecticas_v1.md"


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


def main() -> None:
    normalized = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    tensions = []
    for document in normalized["documentos"]:
        canonical = json.loads((REPO_DIR / document["ruta_json"]).read_text(encoding="utf-8"))
        typology = canonical.get("tipologia") or {}
        tension = (typology.get("razonamiento_5_pasos") or {}).get("tension_dialectica")
        tensions.append({
            "document_id": document["documento_id"],
            "title": document.get("titulo"),
            "year": document.get("anio"),
            "period_id": period_for_year(document.get("anio")),
            "source_path": document["ruta_json"],
            "source_sha256": document["sha256_json"],
            "primary_transformation": (typology.get("transformacion_primaria") or {}).get("nombre"),
            "secondary_transformation": (typology.get("transformacion_secundaria") or {}).get("nombre"),
            "tension_dialectica": tension,
        })
    if len(tensions) != 238 or len({item["document_id"] for item in tensions}) != 238:
        raise ValueError("El derivado debe conservar los 238 documentos activos únicos.")
    coverage = Counter(item["period_id"] or "sin_fecha" for item in tensions if item["tension_dialectica"])
    output = {
        "version": "tensiones-dialecticas-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base_version": "fase3-analitica-v1",
        "source": {"normalized_path": INPUT_PATH.as_posix(), "documents_active": 238, "exclusions_applied": 6},
        "limitations": ["Las tensiones son texto canónico de la tipología y no una taxonomía agregada automática.", "Una tensión formula un problema que el documento procesa; no demuestra que se resuelva."],
        "coverage": {"documents_with_tension": sum(bool(item["tension_dialectica"]) for item in tensions), "by_period": dict(sorted(coverage.items()))},
        "tensions": tensions,
    }
    OUTPUT_JSON.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Tensiones dialécticas v1", "", "**Fuente:** JSON canónicos de Fase 2.  ", f"**Cobertura:** {output['coverage']['documents_with_tension']} de 238 documentos activos.", "", "Las tensiones se leen como problemas que el corpus procesa, no como desenlaces resueltos ni categorías automáticas.", "", "| Período | Documentos con tensión |", "| --- | ---: |"]
    lines.extend(f"| {period} | {count} |" for period, count in output["coverage"]["by_period"].items())
    lines.extend(["", "El JSON hermano conserva documento, título, período, tipología, tensión, ruta y hash de fuente para seleccionar anclas narrativas.", ""])
    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"json": OUTPUT_JSON.as_posix(), "markdown": OUTPUT_MD.as_posix(), **output["coverage"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()