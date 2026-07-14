"""Compara los JSON del ejecutor contra las revisiones ciegas externas y genera el reporte de discrepancias.

Paso 3 del circuito de revisión (ver INSTRUCCIONES_REVISOR_EXTERNO.md §6): el revisor externo deja sus
JSON en fase2/pilot/revision/docNN_revision.json; este script los cruza contra los JSON del ejecutor en
fase2/pilot/docNN_*.json y escribe fase2/pilot/revision/REPORTE_COMPARACION.md con la tasa de acuerdo y el
detalle de cada discrepancia (ambos veredictos + ambas evidencias), listo para la sesión de adjudicación.

La comparación es deliberadamente mecánica (los veredictos son valores cerrados) — el juicio vive en la
adjudicación, no acá. Solo stdlib, igual que el resto del pipeline.

Uso: python fase2/pipeline/comparar_revision.py   (rutas relativas a la raíz del repo)
"""
import glob
import json
import os
import re
import sys

PILOT = "fase2/pilot"
REVISION = f"{PILOT}/revision"
REPORTE = f"{REVISION}/REPORTE_COMPARACION.md"
CRITERIOS = ["gran_impulso_ambiental_concreto", "articulacion_actores",
             "oportunidades_productivas_sostenibles", "como_hacerlo_concreto"]


def cargar(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def buscar_ejecutor(prefijo):
    """docNN -> el JSON del ejecutor docNN_*.json (excluye _revision y los casos numerados _01.._05)."""
    candidatos = [r for r in glob.glob(f"{PILOT}/{prefijo}_*.json")
                  if not re.search(r"_(revision|\d\d)\.json$", r)]
    return candidatos[0] if len(candidatos) == 1 else None


def evid(bloque, limite=280):
    e = str(bloque.get("evidencia", ""))
    return e[:limite] + ("…" if len(e) > limite else "")


def main():
    revisiones = sorted(glob.glob(f"{REVISION}/doc*_revision.json"))
    if not revisiones:
        print(f"No hay revisiones en {REVISION}/ (esperado: docNN_revision.json). Nada que comparar.")
        return 0

    filas, discrepancias, problemas = [], [], []
    total_items = acuerdos = 0

    for ruta_rev in revisiones:
        prefijo = os.path.basename(ruta_rev).split("_revision")[0]
        ruta_eje = buscar_ejecutor(prefijo)
        if not ruta_eje:
            problemas.append(f"{prefijo}: sin JSON de ejecutor inequívoco en {PILOT}/ — se omite")
            continue
        rev, eje = cargar(ruta_rev), cargar(ruta_eje)
        if rev.get("handle") and rev["handle"] != eje["documento"]["handle"]:
            problemas.append(f"{prefijo}: handle no coincide (revisión {rev['handle']} vs ejecutor "
                             f"{eje['documento']['handle']}) — verificar antes de confiar en la comparación")
        quien = rev.get("revisor", {})
        etiqueta_rev = f"{quien.get('modelo', '?')}/{quien.get('harness', '?')}"

        comparaciones = []
        for c in CRITERIOS:
            v_e = eje["interpelacion"][c].get("veredicto")
            v_r = rev.get("interpelacion", {}).get(c, {}).get("veredicto")
            comparaciones.append((f"interpelación ({c})", v_e, v_r,
                                  evid(eje["interpelacion"][c]),
                                  evid(rev.get("interpelacion", {}).get(c, {}))))
        for t in ("transformacion_primaria", "transformacion_secundaria"):
            n_e = eje["tipologia"][t].get("numero")
            n_r = rev.get("tipologia", {}).get(t, {}).get("numero")
            comparaciones.append((f"tipología ({t})", n_e, n_r,
                                  f"#{n_e} {eje['tipologia'][t].get('nombre', '')}",
                                  f"#{n_r} {rev.get('tipologia', {}).get(t, {}).get('nombre', '')}"))

        ok_doc = 0
        for nombre, v_e, v_r, ev_e, ev_r in comparaciones:
            total_items += 1
            if v_e == v_r and v_r is not None:
                acuerdos += 1
                ok_doc += 1
            else:
                discrepancias.append((prefijo, etiqueta_rev, nombre, v_e, v_r, ev_e, ev_r))
        filas.append((prefijo, etiqueta_rev, ok_doc, len(comparaciones)))

    lineas = ["# Reporte de comparación ejecutor ↔ revisor ciego externo", "",
              f"Generado por `pipeline/comparar_revision.py` sobre {len(filas)} documento(s) con revisión. "
              "Ver INSTRUCCIONES_REVISOR_EXTERNO.md §6 para el uso de este reporte (adjudicación).", ""]
    if problemas:
        lineas += ["## Problemas de apareamiento", ""] + [f"- {p}" for p in problemas] + [""]
    lineas += ["## Tasa de acuerdo", "",
               f"**{acuerdos} de {total_items}** ítems comparados coinciden "
               f"({(100 * acuerdos / total_items):.0f}%)." if total_items else "Sin ítems comparables.", "",
               "| Documento | Revisor | Acuerdo |", "| --- | --- | --- |"]
    lineas += [f"| {p} | {r} | {ok}/{n} |" for p, r, ok, n in filas]
    lineas += ["", "## Discrepancias para adjudicar", ""]
    if not discrepancias:
        lineas.append("Ninguna — acuerdo total. No hay adjudicación pendiente.")
    for i, (p, r, nombre, v_e, v_r, ev_e, ev_r) in enumerate(discrepancias, 1):
        lineas += [f"### {i}. {p} — {nombre}", "",
                   f"- **Ejecutor**: `{v_e}` — {ev_e}",
                   f"- **Revisor ({r})**: `{v_r}` — {ev_r}",
                   "- **Adjudicación**: _(pendiente: ejecutor | revisor | regla ambigua → falla sistemática)_", ""]

    os.makedirs(REVISION, exist_ok=True)
    with open(REPORTE, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")
    print(f"{len(filas)} documento(s) comparado(s), {len(discrepancias)} discrepancia(s). Reporte: {REPORTE}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
