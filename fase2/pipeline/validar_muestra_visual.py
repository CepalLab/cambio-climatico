"""Valida una muestra acotada de transcripciones leídas visualmente desde un PDF."""

import argparse
import json
import re
import sys
from pathlib import Path

from validar_citas import citation_quality


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sample", type=Path)
    parser.add_argument("--document", required=True, help="Handle esperado; por ejemplo: 11362/37910")
    parser.add_argument(
        "--pages",
        required=True,
        help="Páginas impresas esperadas, separadas por coma; por ejemplo: 7,15,25",
    )
    arguments = parser.parse_args()

    expected_pages = {int(value) for value in arguments.pages.split(",") if value.strip()}
    payload = json.loads(arguments.sample.read_text(encoding="utf-8"))
    errors = []

    if set(payload) != {"documento", "metodo", "muestras"}:
        errors.append("las claves raíz deben ser documento, metodo y muestras")
    if payload.get("documento") != arguments.document:
        errors.append(f"documento debe ser '{arguments.document}'")
    if payload.get("metodo") != "lectura visual directa del PDF":
        errors.append("metodo debe ser 'lectura visual directa del PDF'")
    samples = payload.get("muestras")
    if not isinstance(samples, list):
        errors.append("muestras debe ser una lista")
        samples = []

    seen_pages = []
    for index, sample in enumerate(samples, 1):
        prefix = f"muestra[{index}]"
        if not isinstance(sample, dict) or set(sample) != {"pagina_impresa", "cita"}:
            errors.append(f"{prefix}: debe ser {{pagina_impresa, cita}}")
            continue
        page, quotation = sample["pagina_impresa"], sample["cita"]
        if not isinstance(page, int):
            errors.append(f"{prefix}: pagina_impresa debe ser entero")
        else:
            seen_pages.append(page)
        if not isinstance(quotation, str):
            errors.append(f"{prefix}: cita debe ser texto")
            continue
        if not 80 <= len(quotation.strip()) <= 280:
            errors.append(f"{prefix}: cita debe tener entre 80 y 280 caracteres")
        quality_error = citation_quality(quotation)
        if quality_error:
            errors.append(f"{prefix}: {quality_error}")
        if not re.search(r"[.!?…][\"”»')\]]*$", quotation.strip()):
            errors.append(f"{prefix}: debe terminar en puntuación de oración")

    actual_pages = set(seen_pages)
    if len(seen_pages) != len(actual_pages):
        errors.append("hay páginas impresas duplicadas")
    if actual_pages != expected_pages:
        errors.append(
            f"páginas esperadas {sorted(expected_pages)}, encontradas {sorted(actual_pages)}"
        )

    if errors:
        print(f"Muestra visual no conforme ({len(errors)} observaciones):")
        for error in errors:
            print(f" - {error}")
        return 1
    print(f"Muestra visual conforme: {len(samples)} transcripciones limpias y completas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
