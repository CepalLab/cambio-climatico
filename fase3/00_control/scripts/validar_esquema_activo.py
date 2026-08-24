"""Ejecuta validar_esquema.py sobre todos los JSON del corpus activo."""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parents[3]
CONTROL_DIR = REPO_DIR / "fase3" / "00_control"
DEFAULT_INVENTORY = CONTROL_DIR / "inventario" / "inventario_corpus_v1.json"
DEFAULT_EXCLUSIONS = CONTROL_DIR / "inventario" / "exclusiones_corpus_v1.csv"
DEFAULT_OUTPUT = CONTROL_DIR / "auditorias" / "validacion_esquema_activo_v1.json"
VALIDATOR = REPO_DIR / "fase2" / "pipeline" / "validar_esquema.py"


def load_exclusions(path: Path) -> set[str]:
    import csv

    with path.open(encoding="utf-8-sig", newline="") as file:
        return {
            row["handle"]
            for row in csv.DictReader(file)
            if row.get("decision") == "excluir" and row.get("estado") == "aplicado"
        }


def validate(record: dict) -> dict:
    path = REPO_DIR / record["ruta_json"]
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(path)],
        cwd=REPO_DIR / "fase2",
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return {
        "handle": record["handle"],
        "ruta_json": record["ruta_json"],
        "ok": result.returncode == 0,
        "estado": "sin_observaciones" if result.returncode == 0 else "con_observaciones",
        "returncode": result.returncode,
        "salida": ((result.stdout or "") + (result.stderr or "")).strip(),
    }


def build_report(inventory_path: Path, exclusions_path: Path) -> dict:
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    exclusions = load_exclusions(exclusions_path)
    records = [record for record in inventory["documentos"] if record["handle"] not in exclusions]
    results = [validate(record) for record in records]
    return {
        "version": "validacion-esquema-activo-v1",
        "generado_en": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "fuentes": {
            "inventario": inventory_path.relative_to(REPO_DIR).as_posix(),
            "exclusiones": exclusions_path.relative_to(REPO_DIR).as_posix(),
            "validador": VALIDATOR.relative_to(REPO_DIR).as_posix(),
        },
        "denominador": {
            "historico": len(inventory["documentos"]),
            "exclusiones_aplicadas": len(exclusions),
            "activo": len(records),
        },
        "resultado": {
            "validados": len(results),
            "sin_observaciones": sum(result["ok"] for result in results),
            "con_observaciones": sum(not result["ok"] for result in results),
        },
        "documentos": results,
    }


def write_markdown(report: dict, path: Path) -> None:
    lines = [
        "# Validación exhaustiva de esquema v1",
        "",
        f"Generada: `{report['generado_en']}`",
        "",
        f"Corpus histórico: **{report['denominador']['historico']}**",
        f"Exclusiones aplicadas: **{report['denominador']['exclusiones_aplicadas']}**",
        f"Corpus activo validado: **{report['denominador']['activo']}**",
        "",
        f"Resultado: **{report['resultado']['sin_observaciones']} sin observaciones / {report['resultado']['con_observaciones']} con observaciones**",
        "",
        "## Observaciones",
        "",
    ]
    failures = [result for result in report["documentos"] if not result["ok"]]
    if not failures:
        lines.append("No se detectaron observaciones en el validador de esquema v1.")
    else:
        for result in failures:
            lines.extend([f"### `{result['handle']}`", "", "```text", result["salida"], "```", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--exclusions", type=Path, default=DEFAULT_EXCLUSIONS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = build_report(args.inventory, args.exclusions)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, args.output.with_suffix(".md"))
    print(json.dumps({"output": args.output.as_posix(), **report["denominador"], **report["resultado"]}, ensure_ascii=False))
    raise SystemExit(0 if report["resultado"]["con_observaciones"] == 0 else 1)


if __name__ == "__main__":
    main()