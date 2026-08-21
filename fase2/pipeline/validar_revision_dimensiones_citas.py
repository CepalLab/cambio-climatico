"""Valida la matriz de revisión semántica dimensión–cita antes de promoción."""

import argparse
import json
import sys
from pathlib import Path


VEREDICTOS = {"directa", "parcial", "no_sustenta"}


def validate(path: Path) -> list[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return ["la matriz debe ser un objeto JSON"]
    entries = payload.get("entradas")
    if not isinstance(entries, list) or not entries:
        return ["la matriz no contiene entradas revisadas"]
    errors = []
    for index, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            errors.append(f"entrada {index}: no es objeto")
            continue
        missing = [key for key in ("ruta_seccion", "dimension", "pagina", "veredicto", "justificacion") if not entry.get(key)]
        if missing:
            errors.append(f"entrada {index}: faltan {', '.join(missing)}")
        verdict = entry.get("veredicto")
        if verdict not in VEREDICTOS:
            errors.append(f"entrada {index}: veredicto inválido {verdict!r}")
        elif verdict == "no_sustenta":
            errors.append(f"entrada {index}: no_sustenta bloquea promoción")
        elif verdict == "parcial" and not str(entry.get("decision_humana") or "").strip():
            errors.append(f"entrada {index}: parcial requiere decision_humana documentada")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("matriz", type=Path)
    arguments = parser.parse_args()
    try:
        errors = validate(arguments.matriz)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        errors = [str(error)]
    if errors:
        print("REVISIÓN DIMENSIÓN–CITA: ERROR")
        for error in errors:
            print(f" - {error}")
        return 1
    print("REVISIÓN DIMENSIÓN–CITA: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
