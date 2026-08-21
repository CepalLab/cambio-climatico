#!/usr/bin/env python3
"""Read-only monitor and gate checker for isolated enrichment runs."""
from __future__ import annotations

import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDS = ["90001", "48304", "89934", "86527", "41173", "89932", "89774", "40159", "81405", "43415", "46682", "69132", "48823", "44551", "46227", "43442"]
REPORTS = ["indice_fuente.json", "borrador_preprueba.json", "reporte_validacion_esquema.txt", "reporte_validacion_indice.txt", "reporte_validacion_citas.txt", "reporte_auditoria_densidad.txt", "reporte_validacion_orden.txt", "EJECUCION_ENRIQUECIMIENTO.md"]

def text_ok(path: Path, needles: tuple[str, ...]) -> bool:
    if not path.exists(): return False
    s = path.read_text(encoding="utf-8", errors="replace").upper()
    return all(n.upper() in s for n in needles)

def check(doc_id: str) -> tuple[str, dict[str, str]]:
    d = ROOT / "corpus/intermedios/11362" / doc_id
    if not (d / "EJECUCION_ENRIQUECIMIENTO.md").exists(): return "GENERANDO BORRADOR", {"missing": "EJECUCION_ENRIQUECIMIENTO.md"}
    missing = [x for x in REPORTS if not (d / x).exists()]
    if missing: return "VALIDANDO", {"missing": ",".join(missing)}
    gates = {
        "esquema": text_ok(d/"reporte_validacion_esquema.txt", ("OK",)) and not text_ok(d/"reporte_validacion_esquema.txt", ("OBSERVACIÓN", "ERROR")),
        "indice": text_ok(d/"reporte_validacion_indice.txt", ("VALIDACIÓN DE ÍNDICE", "OK")),
        "citas": text_ok(d/"reporte_validacion_citas.txt", ("VERIFICADAS",)) and not text_ok(d/"reporte_validacion_citas.txt", ("ERROR", "OBSERVACIÓN")),
        "densidad": not text_ok(d/"reporte_auditoria_densidad.txt", ("ALERTA", "ERROR")),
        "orden": text_ok(d/"reporte_validacion_orden.txt", ("VALIDACIÓN DE ORDEN JSON", "OK")),
    }
    return ("COMPLETO" if all(gates.values()) else "REVISIÓN REQUERIDA"), {k: ("OK" if v else "FALLA") for k,v in gates.items()}

def main() -> None:
    seen = set()
    while True:
        all_done = True
        for doc_id in IDS:
            status, detail = check(doc_id)
            key = (doc_id, status, json.dumps(detail, sort_keys=True))
            if key not in seen:
                print(f"{doc_id}: {status} | {detail}", flush=True); seen.add(key)
            if status != "COMPLETO": all_done = False
        if all_done: return
        time.sleep(20)

if __name__ == "__main__": main()
