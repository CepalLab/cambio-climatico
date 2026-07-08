"""Chequeo de conformidad de los JSON del pipeline contra esquema_json_v1.md.

Uso: python validar_esquema.py <ruta1.json> [<ruta2.json> ...]
Sin argumentos, valida los 3 JSON del piloto (rutas relativas a la raíz del repo).
Solo stdlib, igual que el resto del pipeline. Creado en Ronda 3.

El chequeo de referencias cruzadas es heurístico (regex sobre menciones a otros documentos del
corpus y narrativa de proceso): una coincidencia es una observación a revisar a mano, no
necesariamente un error — la única excepción legítima es tipologia.validacion_anclas contra la
tabla de TIPOLOGIA_v0.md §3.
"""
import json, re, sys

SLUGS = {"contexto_antecedentes","estado_de_situacion","diagnostico_estructural","tendencias",
         "desafios","oportunidades","propuestas_politica","avances_implementacion","brechas_implementacion"}
CRITERIOS = {"gran_impulso_ambiental_concreto","articulacion_actores",
             "oportunidades_productivas_sostenibles","como_hacerlo_concreto"}
DOC_KEYS = {"num_muestra","titulo","autoria","handle","simbolo","isbn","fecha","tipo_documento",
            "paginas_cuerpo","paginas_totales","idioma","tiene_resumen_ejecutivo"}
XREF = re.compile(r"doc\s*\.?\s*0?9|doc\s*\.?\s*11|doc\s*\.?\s*13|documento[s]?\s+(9|11|13)\b|versi[oó]n previa|Ronda [12]", re.I)

errores = []
def err(doc, msg): errores.append(f"[{doc}] {msg}")

def check_secciones(doc, secs, nivel_esperado=1, path=""):
    for s in secs:
        p = f"{path}/{s.get('seccion','?')[:40]}"
        for k in ("seccion","nivel","paginas","resumen","dimensiones","subsecciones"):
            if k not in s: err(doc, f"seccion {p}: falta clave '{k}'")
        if s.get("nivel") != nivel_esperado: err(doc, f"seccion {p}: nivel {s.get('nivel')} != esperado {nivel_esperado}")
        for d in s.get("dimensiones", []):
            if not isinstance(d, dict): err(doc, f"seccion {p}: dimension no es objeto"); continue
            if d.get("dimension") not in SLUGS: err(doc, f"seccion {p}: slug no canonico '{d.get('dimension')}'")
            if "cita" not in d or "pagina" not in d: err(doc, f"seccion {p}: dimension sin cita/pagina propia")
            if "subtipo_brecha" in d and d["dimension"] != "brechas_implementacion":
                err(doc, f"seccion {p}: subtipo_brecha en dimension no-brecha")
        if s.get("subsecciones"): check_secciones(doc, s["subsecciones"], nivel_esperado+1, p)

PILOTO = [f"fase2/pilot/{n}.json" for n in
          ("doc09_caribbean_power", "doc11_pobreza_infantil", "doc13_carbono_frontera")]

for ruta in (sys.argv[1:] or PILOTO):
    name = ruta.rsplit("/", 1)[-1].rsplit("\\", 1)[-1].removesuffix(".json")
    raw = open(ruta, encoding="utf-8").read()
    j = json.loads(raw)
    if '"verdict"' in raw: err(name, "usa clave 'verdict' (debe ser 'veredicto')")
    for m in set(XREF.findall(raw)) if XREF.search(raw) else []:
        pass
    for match in XREF.finditer(raw):
        err(name, f"posible referencia cruzada/narrativa de proceso: ...{raw[max(0,match.start()-60):match.end()+60].strip()}...")
    if set(j) != {"documento","resumen_enriquecido","resumen_secciones","interpelacion","tipologia"}:
        err(name, f"bloques raiz: {sorted(j)}")
    d = j["documento"]
    if set(d) != DOC_KEYS: err(name, f"claves documento difieren: faltan {DOC_KEYS-set(d)}, sobran {set(d)-DOC_KEYS}")
    if not isinstance(d.get("paginas_cuerpo"), int): err(name, "paginas_cuerpo no es entero")
    if not isinstance(d.get("paginas_totales"), int): err(name, "paginas_totales no es entero")
    elif d["paginas_totales"] < d.get("paginas_cuerpo", 0): err(name, "paginas_totales menor que paginas_cuerpo")
    if not str(d.get("handle","")).startswith("https://hdl.handle.net/11362/"): err(name, f"handle sospechoso: {d.get('handle')}")
    a = j["resumen_enriquecido"].get("alcance", {})
    if set(a) != {"ambito_aplicacion","referentes_dependencias","sectorial","temporal"}:
        err(name, f"claves alcance: {sorted(a)}")
    check_secciones(name, j["resumen_secciones"])
    itp = j["interpelacion"]
    if set(itp) != CRITERIOS: err(name, f"criterios interpelacion: {sorted(itp)}")
    for c, v in itp.items():
        if v.get("veredicto") not in {"Sí","Parcial","No"}: err(name, f"{c}: veredicto invalido '{v.get('veredicto')}'")
        for k in ("evidencia","citas","nota"):
            if k not in v: err(name, f"{c}: falta '{k}'")
        for cit in v.get("citas", []):
            if not isinstance(cit, dict) or "cita" not in cit or "pagina" not in cit:
                err(name, f"{c}: cita no es objeto {{cita,pagina}}")
    if "desglose_items" not in itp["como_hacerlo_concreto"] or "tally" not in itp["como_hacerlo_concreto"]:
        err(name, "como_hacerlo_concreto sin desglose_items/tally")
    t = j["tipologia"]
    for k in ("transformacion_primaria","transformacion_secundaria","razonamiento_5_pasos",
              "tipo_documento_climatico","nivel_aplicacion","ambiguedad_pendiente_validacion"):
        if k not in t: err(name, f"tipologia: falta '{k}'")
    if "tipo_brecha" in t: err(name, "tipologia conserva 'tipo_brecha' (debe desaparecer)")
    for k in ("transformacion_primaria","transformacion_secundaria"):
        if set(t.get(k, {})) != {"numero","nombre","certeza"}: err(name, f"tipologia.{k} no es {{numero,nombre,certeza}}")
    if set(t.get("razonamiento_5_pasos", {})) != {"tension_dialectica","filtro_categoria_primaria",
            "secundaria_obligatoria","justificacion_anti_copia","validacion_anclas"}:
        err(name, f"razonamiento_5_pasos incompleto: {sorted(t.get('razonamiento_5_pasos', {}))}")
    print(f"{name}: OK estructura base" if not any(e.startswith(f'[{name}]') for e in errores) else f"{name}: con observaciones")

print()
if errores:
    print(f"{len(errores)} observaciones:")
    for e in errores: print(" -", e)
    sys.exit(1)
print("Los 3 JSON conformes al esquema v1, sin referencias cruzadas.")
