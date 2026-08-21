"""Audita higiene de títulos y cobertura antes de promover un JSON analítico.

La cobertura es una alerta por defecto para permitir la migración gradual de
lotes históricos; ``--strict-coverage`` la convierte en compuerta bloqueante.
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

MOJIBAKE = ("â€", "\ufffd")
MOJIBAKE_UTF8 = re.compile(r"Ã(?:[\x80-\xBF]|[¡©®±º¿])")
KEYWORDS_CLIMA = re.compile(
    r"cambio clim[áa]tico|clim[áa]tic[oa]s?|calentamiento|carbono|efecto invernadero|"
    r"precipitaci[oó]n|temperatura|mitigaci[oó]n|adaptaci[oó]n|sostenibilidad ambiental|"
    r"ambiental|ambientales|environmental|ecol[oó]gico|ecological|sequ[ií]a|drought|inundaci[oó]n|flood|"
    r"biodiversidad|biodiversity|bioma|biome|ecosistema|ecosystem|greenhouse gas|emissions?",
    re.I,
)
SIN_SENAL_CLIMATICA = re.compile(
    r"(?:no (?:hay|contiene|menciona)|no se detect[oó]|sin (?:ninguna )?(?:menci[oó]n|desarrollo|vinculaci[oó]n|contenido|calificar))"
    r".{0,100}(?:cambio clim[áa]tico|variabilidad clim[áa]tica|señal clim[áa]tica|clim[áa]tic[oa])|"
    r"menci[oó]n.{0,120}(?:solo|gen[eé]rica|sin desarrollo)|"
    r"remit\w*.{0,100}(?:tema )?clim[áa]tic",
    re.I | re.S,
)


def sections(items, path=""):
    for item in items or []:
        current = f"{path}/{item.get('seccion', '?')}"
        yield item, current
        yield from sections(item.get("subsecciones"), current)


def title_errors(title):
    if not isinstance(title, str) or not title:
        return ["vacío o no textual"]
    errors = []
    if title != title.strip(): errors.append("espacios en bordes")
    if re.search(r"\s{2,}", title): errors.append("espacios repetidos")
    if any(unicodedata.category(char).startswith("C") for char in title): errors.append("carácter de control")
    if any(marker in title for marker in MOJIBAKE) or MOJIBAKE_UTF8.search(title):
        errors.append("mojibake o carácter de reemplazo")
    return errors


def climate_relevant_leaves(leaves):
    """Leaves that require dimensions under esquema_json_v1.md rule 6bis."""
    return [
        (section, path)
        for section, path in leaves
        if (summary := str(section.get("resumen") or "").strip())
        and KEYWORDS_CLIMA.search(summary)
        and not SIN_SENAL_CLIMATICA.search(summary)
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("documento", type=Path)
    parser.add_argument("--strict-coverage", action="store_true")
    parser.add_argument("--minimum-leaf-coverage", type=float, default=0.50)
    arguments = parser.parse_args()
    data = json.loads(arguments.documento.read_text(encoding="utf-8"))
    all_sections = list(sections(data.get("resumen_secciones")))
    title_issues = [(path, issue) for section, path in all_sections for issue in title_errors(section.get("seccion"))]
    leaves = [(section, path) for section, path in all_sections if not section.get("subsecciones")]
    substantive = climate_relevant_leaves(leaves)
    covered = [(section, path) for section, path in substantive if section.get("dimensiones")]
    ratio = len(covered) / len(substantive) if substantive else 1.0
    if title_issues:
        print("TÍTULOS: ERROR")
        for path, issue in title_issues:
            print(f" - {path}: {issue}")
    else:
        print("TÍTULOS: OK")
    coverage_label = f"{ratio:.2%}" if substantive else "no aplicable (0 hojas detectadas)"
    print(f"COBERTURA CLIMÁTICA: {len(covered)}/{len(substantive)} hojas con señal climática/ambiental ({coverage_label}).")
    low = ratio < arguments.minimum_leaf_coverage
    if low:
        print(f"ALERTA: cobertura inferior a {arguments.minimum_leaf_coverage:.0%}; revisar hojas sin dimensión antes de promover.")
    if title_issues or (arguments.strict_coverage and low):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
