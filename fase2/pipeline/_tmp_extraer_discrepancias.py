# Uso interno de la adjudicación (temporal, borrar al terminar):
# vuelca evidencia completa de ejecutor y revisor para cada discrepancia.
import glob
import io
import json
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

DOCS = ["01", "02", "03", "04", "06", "08", "10", "11", "12", "13", "14", "15", "16", "18", "19"]
CRITS = [
    "gran_impulso_ambiental_concreto",
    "articulacion_actores",
    "oportunidades_productivas_sostenibles",
    "como_hacerlo_concreto",
]
MULTI = tuple(f"_{k:02d}.json" for k in range(1, 6))

for n in DOCS:
    ej = [p for p in glob.glob(f"fase2/pilot/doc{n}_*.json") if not p.endswith(MULTI)]
    with open(ej[0], encoding="utf-8") as f:
        E = json.load(f)
    with open(f"fase2/pilot/revision/doc{n}_revision.json", encoding="utf-8") as f:
        R = json.load(f)
    print("=" * 100)
    print(f"DOC{n}  ejecutor={ej[0]}")
    ei, ri = E.get("interpelacion", {}), R.get("interpelacion", {})
    for crit in CRITS:
        e, r = ei.get(crit, {}), ri.get(crit, {})
        if e.get("veredicto") == r.get("veredicto"):
            continue
        print(f"--- {crit}: EJEC={e.get('veredicto')} | REV={r.get('veredicto')}")
        print(f"  [EJEC] {e.get('evidencia', '')[:1200]}")
        if e.get("tally"):
            print(f"  [EJEC tally] {e['tally']}")
        for it in e.get("desglose_items", []):
            print(f"    EJEC item ({it.get('clasificacion')}, p.{it.get('pagina')}): {it.get('item', '')[:160]}")
        print(f"  [REV ] {r.get('evidencia', '')[:1200]}")
        if r.get("tally"):
            print(f"  [REV tally] {r['tally']}")
        for it in r.get("desglose_items", []):
            print(f"    REV  item ({it.get('clasificacion')}, p.{it.get('pagina')}): {it.get('item', '')[:160]}")
    et, rt = E.get("tipologia", {}), R.get("tipologia", {})
    ep, rp = et.get("transformacion_primaria", {}), rt.get("transformacion_primaria", {})
    es, rs = et.get("transformacion_secundaria", {}), rt.get("transformacion_secundaria", {})
    if ep.get("numero") != rp.get("numero") or es.get("numero") != rs.get("numero"):
        print(f"--- tipologia: EJEC prim=#{ep.get('numero')} {ep.get('nombre')} ({ep.get('certeza')}), "
              f"sec=#{es.get('numero')} {es.get('nombre')} ({es.get('certeza')})")
        print(f"               REV  prim=#{rp.get('numero')} {rp.get('nombre')} ({rp.get('certeza')}), "
              f"sec=#{rs.get('numero')} {rs.get('nombre')} ({rs.get('certeza')})")
        ju_e = et.get("justificacion_breve") or et.get("justificacion") or ""
        ju_r = rt.get("justificacion_breve") or rt.get("justificacion") or ""
        print(f"  [EJEC just] {ju_e[:800]}")
        print(f"  [REV  just] {ju_r[:800]}")
