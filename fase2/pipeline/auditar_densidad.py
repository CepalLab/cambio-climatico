"""Reporta densidad de dimensiones para detectar sobrecodificación antes de revisión."""

import argparse
import json
import sys
from pathlib import Path


def dimensions(sections: list[dict]):
    for section in sections:
        yield from section.get("dimensiones", [])
        yield from dimensions(section.get("subsecciones", []))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result", type=Path)
    parser.add_argument("--warning-per-page", type=float, default=0.55)
    parser.add_argument("--minimum-warning-per-page", type=float, default=0.12)
    parser.add_argument("--strict", action="store_true")
    arguments = parser.parse_args()

    document = json.loads(arguments.result.read_text(encoding="utf-8"))
    pages = document["documento"].get("paginas_cuerpo", 0)
    count = sum(1 for _ in dimensions(document.get("resumen_secciones", [])))
    density = count / max(1, pages)
    print(f"Dimensiones: {count}; páginas de cuerpo: {pages}; densidad: {density:.2f}/página.")
    if pages >= 80 and density > arguments.warning_per_page:
        print(
            f"ALERTA: densidad superior a {arguments.warning_per_page:.2f}/página en documento largo; "
            "revisar si varias dimensiones describen el mismo hallazgo."
        )
        return 1 if arguments.strict else 0
    if pages >= 80 and density < arguments.minimum_warning_per_page:
        print(
            f"ALERTA: densidad inferior a {arguments.minimum_warning_per_page:.2f}/página en documento largo; "
            "revisar cobertura porque podría haber subextracción."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
