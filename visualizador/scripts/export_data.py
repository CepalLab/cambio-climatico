"""Exporta fase3_analitica_v1.sqlite a JSON para el visualizador.

Uso: python3 scripts/export_data.py  (desde visualizador/)
Genera data/*.json + data/covers.json (mapa id -> tiene PDF local).
"""
import json
import os
import re
import sqlite3
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # visualizador/
REPO = ROOT.parent                                      # repo raiz
DB = Path(os.environ.get("CEPAL_DB") or
           (REPO / "fase3/02_eda/salidas/fase3_analitica_v1.sqlite"))
PDFDIR = REPO / "fase2/corpus/pdfs"
OUT = ROOT / "web/data"
OUT.mkdir(parents=True, exist_ok=True)

CRITERIOS = {
    "gran_impulso_ambiental_concreto": "Gran impulso ambiental",
    "articulacion_actores": "Articulación de actores",
    "oportunidades_productivas_sostenibles": "Oportunidades productivas",
    "como_hacerlo_concreto": "Cómo hacerlo concreto",
}
DIM_NOMBRES = {
    "propuestas_politica": "Propuestas de política",
    "estado_de_situacion": "Estado de situación",
    "diagnostico_estructural": "Diagnóstico estructural",
    "desafios": "Desafíos",
    "avances_implementacion": "Avances de implementación",
    "oportunidades": "Oportunidades",
    "brechas_implementacion": "Brechas de implementación",
    "tendencias": "Tendencias",
    "contexto_antecedentes": "Contexto y antecedentes",
}


def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.lower()).strip("-")
    return s or "s-n"


def doc_num(handle: str) -> str:
    m = re.search(r"11362/(\d+)", handle or "")
    return m.group(1) if m else ""


con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

pdfs = {p.stem for p in PDFDIR.glob("*.pdf")} if PDFDIR.exists() else set()

counts = {}
for doc_id, nsec, ndim, nq in con.execute(
        "SELECT d.document_id, "
        "(SELECT COUNT(*) FROM sections s WHERE s.document_id=d.document_id), "
        "(SELECT COUNT(*) FROM dimensions m WHERE m.document_id=d.document_id), "
        "(SELECT COUNT(*) FROM dimensions m WHERE m.document_id=d.document_id "
        " AND m.quote IS NOT NULL AND m.quote<>'') "
        "FROM documents d"):
    counts[doc_id] = (nsec, ndim, nq)
typos = {r["document_id"]: dict(r) for r in con.execute("SELECT * FROM typology")}
interps = {}
for r in con.execute("SELECT * FROM interpellation"):
    interps.setdefault(r["document_id"], {})[r["criterion"]] = {
        "veredicto": r["verdict"], "evidencia": r["evidence"]}

docs = []
for r in con.execute("SELECT * FROM documents ORDER BY anio DESC, title"):
    d = dict(r)
    num = doc_num(d["handle"])
    topics = [t for t in json.loads(d["topic_spa_json"] or "[]")
              if "CAMBIO CLIM" not in t.upper()]
    nsec, ndim, nquotes = counts.get(d["document_id"], (0, 0, 0))
    typo = typos.get(d["document_id"])
    interp = interps.get(d["document_id"], {})
    has_pdf = f"11362_{num}" in pdfs
    docs.append({
        "id": num, "handle": d["handle"], "titulo": d["title"],
        "anio": d["anio"], "division": d["division"], "temas": topics,
        "resumen": d["abstract"], "tipo": d["type_normalized_name"],
        "slug": slug(d["title"] or num)[:80],
        "secciones": nsec, "dimensiones": ndim, "citas": nquotes,
        "evidencia": ndim + nquotes,
        "tipologia": {"primaria": typo["primary_name"] if typo else None,
                      "secundaria": typo["secondary_name"] if typo else None} if typo else None,
        "interpelacion": interp,
        "portada": has_pdf,
    })

div_counter = Counter(d["division"] for d in docs)
topic_counter = Counter(t for d in docs for t in d["temas"])
divisiones = [{"nombre": n, "slug": slug(n), "total": c}
              for n, c in div_counter.most_common()]
temas = [{"nombre": n, "slug": slug(n), "total": c}
         for n, c in topic_counter.most_common()]

tipo_counter = Counter((d["tipologia"] or {}).get("primaria") for d in docs)
tipologia = [{"nombre": n or "Sin clasificar", "total": c}
             for n, c in tipo_counter.most_common()]

interp_rows = []
for crit, nombre in CRITERIOS.items():
    v = Counter(d["interpelacion"].get(crit, {}).get("veredicto") for d in docs)
    interp_rows.append({"criterio": crit, "nombre": nombre,
                        "si": v.get("Sí", 0), "parcial": v.get("Parcial", 0),
                        "no": v.get("No", 0)})

dim_rows = [{"dimension": k, "nombre": DIM_NOMBRES.get(k, k), "total": v}
            for k, v in con.execute(
                "SELECT dimension, COUNT(*) FROM dimensions GROUP BY 1 ORDER BY 2 DESC")]

timeline = [{"anio": a, "total": c} for a, c in
            con.execute("SELECT anio, COUNT(*) FROM documents GROUP BY 1 ORDER BY 1")]

tipos = [{"nombre": n or "Sin clasificar", "total": c} for n, c in
         Counter(d["tipo"] for d in docs).most_common()]

destacados = sorted(docs, key=lambda d: -d["evidencia"])[:12]

(OUT / "documentos.json").write_text(json.dumps(docs, ensure_ascii=False), encoding="utf-8")
(OUT / "agregados.json").write_text(json.dumps({
    "totales": {"documentos": len(docs), "dimensiones": sum(d["dimensiones"] for d in docs),
                "citas": sum(d["citas"] for d in docs),
                "periodo": [min(d["anio"] for d in docs), max(d["anio"] for d in docs)]},
    "divisiones": divisiones, "temas": temas, "tipologia": tipologia,
    "interpelacion": interp_rows, "dimensiones": dim_rows,
    "timeline": timeline, "tipos": tipos,
    "destacados": [d["id"] for d in destacados],
}, ensure_ascii=False), encoding="utf-8")

print(f"{len(docs)} documentos, {len(divisiones)} divisiones, {len(temas)} temas -> {OUT}")
