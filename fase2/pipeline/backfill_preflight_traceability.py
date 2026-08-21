"""Completa trazabilidad de preflight sin regenerar PDFs ni tramos existentes."""

import argparse
import json
import subprocess
import sys
from pathlib import Path


UNKNOWN_LAYOUT = {"layout": "unknown", "method": "not_available"}


def write_json(path: Path, payload: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def pymupdf_layout(candidates: list[dict]) -> dict:
    candidate = next((item for item in candidates if item.get("extractor") == "pymupdf"), None)
    return candidate.get("layout", UNKNOWN_LAYOUT) if candidate else UNKNOWN_LAYOUT


def backfill_document(root: Path, handle_id: str, endpoint_script: Path) -> dict:
    document_dir = root / "corpus" / "intermedios" / "11362" / handle_id
    text = document_dir / "texto.txt"
    endpoint_report = document_dir / "preflight_endpoint.json"
    if not text.is_file():
        raise FileNotFoundError(f"TXT inexistente: {text}")
    completed = subprocess.run(
        [sys.executable, str(endpoint_script), str(text), "--report", str(endpoint_report)],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode not in (0, 2):
        raise RuntimeError(f"preflight endpoint falló para {handle_id}: {completed.stderr.strip()}")

    tramos = document_dir / "tramos"
    preflight_path, manifest_path = tramos / "preflight.json", tramos / "manifest.json"
    preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    layout = pymupdf_layout(preflight.get("candidates", []))
    selected = manifest.get("extractor")
    if layout.get("layout") == "two_column" and selected != "pymupdf":
        raise RuntimeError(f"{handle_id}: two_column exige extractor pymupdf, no {selected}")

    preflight["layout_diagnostic"] = layout
    preflight["layout_extraction_applied"] = selected == "pymupdf"
    manifest["layout"] = layout
    manifest["layout_extraction_applied"] = selected == "pymupdf"
    manifest["layout_diagnostic_extractor"] = "pymupdf"
    write_json(preflight_path, preflight)
    write_json(manifest_path, manifest)
    return {"id": handle_id, "endpoint_exit": completed.returncode, "layout": layout.get("layout"), "extractor": selected}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="Manifiesto reservado del lote")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    arguments = parser.parse_args()
    batch = json.loads(arguments.manifest.read_text(encoding="utf-8"))
    endpoint_script = arguments.root / "pipeline" / "preflight_endpoint_text.py"
    results = [
        backfill_document(arguments.root, item["handle"].rsplit("/", 1)[-1], endpoint_script)
        for item in batch["documents"]
    ]
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
