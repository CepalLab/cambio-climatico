"""Aplica decisiones aprobadas de la matriz semántica, con coincidencia exacta de citas."""
import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
MATRIX = BASE / "fase3" / "revision_semantica_117_v1.csv"
INVENTORY = BASE / "fase3" / "inventario_corpus_v1.json"
LOG = BASE / "fase3" / "aplicacion_revision_semantica_v1.json"
AUDIT = BASE / "fase3" / "auditoria_dimensiones_v1.json"


def walk(sections):
    for section in sections:
        yield section
        yield from walk(section.get("subsecciones") or [])


def main():
    rows = list(csv.DictReader(MATRIX.open(encoding="utf-8-sig", newline="")))
    candidates = json.loads(AUDIT.read_text(encoding="utf-8"))["candidatos"]
    for row in rows:
        if not row.get("cita"):
            candidate = candidates[int(row["caso"]) - 1]
            row["cita"] = candidate["cita"]
    records = {r["handle"]: r for r in json.loads(INVENTORY.read_text(encoding="utf-8"))["documentos"]}
    by_handle = defaultdict(list)
    for row in rows:
        if row.get("decision") in {"reclasificar", "excluir"}:
            by_handle[row["handle"]].append(row)

    log = {"version": "aplicacion-revision-semantica-v1", "generado_en": datetime.now(timezone.utc).isoformat(timespec="seconds"), "cambios": [], "errores": []}
    for handle, decisions in by_handle.items():
        record = records[handle]
        path = BASE / record["ruta_json"]
        data = json.loads(path.read_text(encoding="utf-8"))
        changed = False
        for decision in decisions:
            citation = decision["cita"]
            original = decision["dimension_original"]
            target = decision.get("dimension_nueva") or ""
            matches = [d for s in walk(data.get("resumen_secciones") or []) for d in (s.get("dimensiones") or []) if d.get("cita") == citation]
            original_matches = [d for d in matches if d.get("dimension") == original]
            if not original_matches:
                already = [d for d in matches if d.get("dimension") == target] if target else []
                if already:
                    log["cambios"].append({"caso": decision["caso"], "handle": handle, "accion": "ya_aplicado", "dimension": target})
                    continue
                log["errores"].append({"caso": decision["caso"], "handle": handle, "error": "cita_o_dimension_original_no_encontrada"})
                continue
            if len(original_matches) != 1:
                log["errores"].append({"caso": decision["caso"], "handle": handle, "error": f"coincidencias_ambiguas:{len(original_matches)}"})
                continue
            item = original_matches[0]
            if decision["decision"] == "reclasificar":
                item["dimension"] = target
                action = "reclasificar"
            else:
                for section in walk(data.get("resumen_secciones") or []):
                    section["dimensiones"] = [d for d in (section.get("dimensiones") or []) if d is not item]
                action = "excluir_dimension"
            changed = True
            log["cambios"].append({"caso": decision["caso"], "handle": handle, "accion": action, "antes": original, "despues": target or None})
        if changed:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    log["resultado"] = {"decisiones_procesadas": len(rows), "cambios_o_ya_aplicados": len(log["cambios"]), "errores": len(log["errores"]), "archivos_modificados": len({c["handle"] for c in log["cambios"] if c["accion"] != "ya_aplicado"})}
    LOG.write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(log["resultado"], ensure_ascii=False))
    if log["errores"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
