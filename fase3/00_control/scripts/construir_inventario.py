"""Construye el inventario unificado de pilotos y resultados de producción."""

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parents[3]
FASE2_DIR = REPO_DIR / "fase2"
DEFAULT_OUTPUT = REPO_DIR / "fase3" / "00_control" / "inventario" / "inventario_corpus_v1.json"


def normalize_handle(value: str) -> str:
    value = value.strip().rstrip("/")
    if value.startswith("http://hdl.handle.net/"):
        return "https://" + value.removeprefix("http://")
    if value.startswith("11362/"):
        return f"https://hdl.handle.net/{value}"
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_csv_handles(path: Path) -> set[str]:
    with path.open(encoding="utf-8-sig", newline="") as file:
        return {
            normalize_handle(row["dc.identifier.uri"])
            for row in csv.DictReader(file)
            if row.get("dc.identifier.uri")
        }


def read_document(path: Path, source: str, certificate_path: Path | None) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    document = data["documento"]
    return {
        "handle": normalize_handle(document["handle"]),
        "titulo": document.get("titulo"),
        "fecha": document.get("fecha"),
        "num_muestra": document.get("num_muestra"),
        "origen": source,
        "ruta_json": path.relative_to(REPO_DIR).as_posix(),
        "sha256_json": sha256(path),
        "certificado_disponible": certificate_path is not None and certificate_path.is_file(),
        "ruta_certificado": (
            certificate_path.relative_to(REPO_DIR).as_posix()
            if certificate_path is not None and certificate_path.is_file()
            else None
        ),
        "sha256_certificado": (
            sha256(certificate_path)
            if certificate_path is not None and certificate_path.is_file()
            else None
        ),
        "claves_superiores": sorted(data),
    }


def build_inventory() -> dict:
    pilot_paths = sorted((FASE2_DIR / "pilot").glob("doc*.json"))
    production_paths = sorted((FASE2_DIR / "corpus" / "resultados" / "json").glob("doc_*.json"))
    records = [read_document(path, "piloto", None) for path in pilot_paths]
    records += [
        read_document(
            path,
            "produccion",
            FASE2_DIR / "corpus" / "resultados" / "certificados" / f"{path.stem}.validation.json",
        )
        for path in production_paths
    ]
    handles = [record["handle"] for record in records]
    csv_handles = load_csv_handles(REPO_DIR / "documentos_definitivos_trazabilidad.csv")
    duplicate_handles = sorted({handle for handle in handles if handles.count(handle) > 1})
    inventory_handles = set(handles)
    return {
        "version": "inventario-corpus-v1",
        "generado_en": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "fuentes": {
            "pilotos": "fase2/pilot/",
            "produccion": "fase2/corpus/resultados/json/",
            "certificados": "fase2/corpus/resultados/certificados/",
            "trazabilidad": "documentos_definitivos_trazabilidad.csv",
        },
        "conteos": {
            "total": len(records),
            "pilotos": len(pilot_paths),
            "produccion": len(production_paths),
            "certificados_disponibles": sum(record["certificado_disponible"] for record in records),
        },
        "validacion": {
            "handles_unicos": len(duplicate_handles) == 0,
            "handles_duplicados": duplicate_handles,
            "filas_csv": len(csv_handles),
            "handles_fuera_del_csv": sorted(inventory_handles - csv_handles),
            "handles_faltantes_del_inventario": sorted(csv_handles - inventory_handles),
        },
        "documentos": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    inventory = build_inventory()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": args.output.as_posix(), **inventory["conteos"], **inventory["validacion"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()