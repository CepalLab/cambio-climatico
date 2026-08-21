"""Ejecuta compuertas finales y sella sus insumos mediante hashes SHA-256."""
import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(name, command, report):
    result = subprocess.run(command, text=True, capture_output=True)
    report.write_text(result.stdout + result.stderr, encoding="utf-8")
    return {"name": name, "exit_code": result.returncode, "report": str(report)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("documento", type=Path)
    parser.add_argument("--indice", type=Path, required=True)
    parser.add_argument("--page-source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--strict-coverage", action="store_true")
    parser.add_argument("--review-matrix", type=Path, help="Matriz de revisión semántica dimensión–cita")
    arguments = parser.parse_args()
    workdir = arguments.output.parent
    workdir.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    jobs = [
        ("esquema", [py, str(HERE / "validar_esquema.py"), str(arguments.documento)]),
        ("indice", [py, str(HERE / "validar_indice.py"), str(arguments.documento), "--indice", str(arguments.indice)]),
        ("orden", [py, str(HERE / "validar_orden_json.py"), str(arguments.documento)]),
        ("citas", [py, str(HERE / "validar_citas.py"), str(arguments.documento), "--page-source", str(arguments.page_source), "--strict-quality"]),
        ("titulos_cobertura", [py, str(HERE / "auditar_pre_promocion.py"), str(arguments.documento)] + (["--strict-coverage"] if arguments.strict_coverage else [])),
    ]
    if arguments.review_matrix:
        jobs.append(("revision_dimensiones_citas", [py, str(HERE / "validar_revision_dimensiones_citas.py"), str(arguments.review_matrix)]))
    checks = [run(name, command, workdir / f"reporte_validacion_{name}.txt") for name, command in jobs]
    manifest = arguments.page_source / "manifest.json" if arguments.page_source.is_dir() else arguments.page_source
    payload = {
        "version": "promocion-v1",
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "result_path": str(arguments.documento),
        "result_sha256": digest(arguments.documento),
        "indice_sha256": digest(arguments.indice),
        "page_source_sha256": digest(manifest),
        "review_matrix_sha256": digest(arguments.review_matrix) if arguments.review_matrix else None,
        "checks": checks,
        "ok": all(check["exit_code"] == 0 for check in checks),
    }
    temporary = arguments.output.with_suffix(arguments.output.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(arguments.output)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
