"""Perfila metadatos textuales del corpus activo para diseñar su normalización."""

import argparse
import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


FASE3_DIR = Path(__file__).resolve().parents[2]
REPO_DIR = FASE3_DIR.parent
DEFAULT_INVENTORY = FASE3_DIR / "00_control" / "inventario" / "inventario_corpus_v1.json"
DEFAULT_EXCLUSIONS = FASE3_DIR / "00_control" / "inventario" / "exclusiones_corpus_v1.csv"
DEFAULT_OUTPUT = FASE3_DIR / "01_normalizacion" / "salidas" / "perfil_metadatos_v1.json"

FIELD_PATHS = {
    "autoria": ("documento", "autoria"),
    "tipo_documento": ("documento", "tipo_documento"),
    "idioma": ("documento", "idioma"),
    "ambito_aplicacion": ("resumen_enriquecido", "alcance", "ambito_aplicacion"),
    "referentes_dependencias": ("resumen_enriquecido", "alcance", "referentes_dependencias"),
    "sectorial": ("resumen_enriquecido", "alcance", "sectorial"),
    "temporal": ("resumen_enriquecido", "alcance", "temporal"),
    "nivel_aplicacion": ("tipologia", "nivel_aplicacion"),
    "tipo_documento_climatico": ("tipologia", "tipo_documento_climatico"),
}


def load_exclusions(path: Path) -> set[str]:
    with path.open(encoding="utf-8-sig", newline="") as file:
        return {
            row["handle"]
            for row in csv.DictReader(file)
            if row.get("decision") == "excluir" and row.get("estado") == "aplicado"
        }


def get_nested(data: dict, path: tuple[str, ...]):
    value = data
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def clean_value(value) -> str | None:
    if value is None:
        return None
    value = re.sub(r"\s+", " ", str(value)).strip()
    return value or None


def separator_signals(value: str) -> list[str]:
    signals = []
    if "•" in value:
        signals.append("bullet")
    if ";" in value:
        signals.append("semicolon")
    if " | " in value:
        signals.append("pipe")
    if re.search(r"\s+y\s+", value, flags=re.IGNORECASE):
        signals.append("and")
    if re.search(r",\s+", value):
        signals.append("comma")
    return signals


def profile_field(values: list[str | None]) -> dict:
    present = [value for value in values if value is not None]
    counts = Counter(present)
    separator_counts = Counter(
        signal
        for value in present
        for signal in separator_signals(value)
    )
    return {
        "present": len(present),
        "missing": len(values) - len(present),
        "distinct": len(counts),
        "separator_signals": dict(sorted(separator_counts.items())),
        "values": [
            {"value": value, "count": count}
            for value, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        ],
    }


def build_profile(inventory_path: Path, exclusions_path: Path) -> dict:
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    exclusions = load_exclusions(exclusions_path)
    records = [
        record for record in inventory["documentos"] if record["handle"] not in exclusions
    ]
    values_by_field = {field: [] for field in FIELD_PATHS}
    for record in records:
        data = json.loads((REPO_DIR / record["ruta_json"]).read_text(encoding="utf-8"))
        for field, path in FIELD_PATHS.items():
            values_by_field[field].append(clean_value(get_nested(data, path)))

    return {
        "version": "perfil-metadatos-v1",
        "generado_en": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "fuentes": {
            "inventario": inventory_path.relative_to(REPO_DIR).as_posix(),
            "exclusiones": exclusions_path.relative_to(REPO_DIR).as_posix(),
        },
        "denominador": {
            "historico": len(inventory["documentos"]),
            "exclusiones_aplicadas": len(exclusions),
            "activo": len(records),
        },
        "campos": {
            field: profile_field(values)
            for field, values in values_by_field.items()
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--exclusions", type=Path, default=DEFAULT_EXCLUSIONS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    profile = build_profile(args.inventory, args.exclusions)
    args.output.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": args.output.as_posix(), **profile["denominador"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()