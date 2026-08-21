"""Chequeo de conformidad de los JSON del pipeline contra esquema_json_v1.md.

Uso: python validar_esquema.py <ruta1.json> [<ruta2.json> ...]
Sin argumentos, valida todos los JSON canónicos de fase2/pilot/ y fase2/corpus/resultados/
(excluye variantes multimodelo doc09_01..05). Solo stdlib, igual que el resto del pipeline. Creado en Ronda 3;
chequeo de secciones excluidas (reglas 7–9) agregado en Ronda 8; chequeo heurístico de
dimensiones vacías en hojas con señal climática agregado en Ronda 10.

El chequeo de referencias cruzadas es heurístico (regex sobre menciones a otros documentos del
corpus y narrativa de proceso): una coincidencia es una observación a revisar a mano, no
necesariamente un error — la única excepción legítima es tipologia.validacion_anclas contra la
tabla de TIPOLOGIA_v0.md §3.
"""
import json, re, sys
from pathlib import Path

SLUGS = {"contexto_antecedentes","estado_de_situacion","diagnostico_estructural","tendencias",
         "desafios","oportunidades","propuestas_politica","avances_implementacion","brechas_implementacion"}
CRITERIOS = {"gran_impulso_ambiental_concreto","articulacion_actores",
             "oportunidades_productivas_sostenibles","como_hacerlo_concreto"}
DOC_KEYS = {"num_muestra","titulo","autoria","handle","simbolo","isbn","fecha","tipo_documento",
            "paginas_cuerpo","paginas_totales","idioma","tiene_resumen_ejecutivo"}
# tiene_anexos es opcional: campo nuevo desde Ronda 4 (esquema_json_v1.md regla 7), ausente por
# diseño en los 3 pilotos originales (doc09/11/13, generados antes de esa regla).
DOC_KEYS_OPCIONALES = {"tiene_anexos"}
RESUMEN_ENRIQUECIDO_KEYS = {"pregunta_investigacion", "alcance", "hallazgos_principales",
                            "conclusiones_recomendaciones", "resumen_narrativo"}
TRANSFORMACIONES = {
    1: "Desarrollo productivo", 2: "Reducción de la desigualdad", 3: "Protección social",
    4: "Educación y formación profesional", 5: "Igualdad de género",
    6: "Sostenibilidad ambiental", 7: "Transformación digital", 8: "Migración",
    9: "Integración económica", 10: "Macroeconomía y fiscalidad", 11: "Capacidades del Estado",
}
TRANSFORMACIONES_ALIASES = {10: {"Macroeconomía y finanzas públicas"}}
XREF = re.compile(r"doc\s*\.?\s*0?9|doc\s*\.?\s*11|doc\s*\.?\s*13|documento[s]?\s+(9|11|13)\b|versi[oó]n previa|Ronda [12]", re.I)
# Títulos de sección excluidos (esquema §2 reglas 7–9). Anclados al inicio del título.
# Anexos: se alerta salvo excepción histórica doc11 (regla 7).
SECCION_EXCLUIDA = re.compile(
    r"^(?:"
    r"(?:(?:\d+(?:\.\d+)*|[IVXLCDM]+)\.?\s*)?(?:resumen(?!\s+(?:de\s+recomendaciones|y\s+conclusiones)\b)(?!\s*,\s*\w)|resumen\s+ejecutivo|abstract|executive\s+summary)|"
    r"bibliograf[ií]a|bibliography|referencias?(?:\s+bibliogr[aá]ficas?)?|references?|"
    r"(?:lista\s+de\s+)?(?:siglas?|abrevi(?:aturas?|aciones?))(?:\s+y\s+acr[o\u00f3]nimos?)?|acr[o\u00f3]nimos?|acronyms?|list\s+of\s+acronyms|glosario|glossary|"
    r"pr[oó]logo|prologue|foreword|prefacio|preface|"
    r"mensajes?(?:\s+(?:del|de\s+la|clave|institucional|principal(?:es)?))?|"
    r"(?:key\s+)?messages?(?:\s+from)?|"
    r"message\s+from|"
    r"(?:\d+\.\s*)?anexos?"
    r")\b",
    re.I,
)
ANEXO_HISTORICO = re.compile(r"(?:\d+\.\s*)?anexos?\b", re.I)

errores = []
def err(doc, msg): errores.append(f"[{doc}] {msg}")

def rango_pagina(p):
    """Normaliza `pagina`/`paginas` (int, "9", "9-10") a una tupla (desde, hasta) o None."""
    if isinstance(p, int): return (p, p)
    if isinstance(p, str):
        m = re.fullmatch(r"\s*(\d+)\s*(?:-\s*(\d+))?\s*", p)
        if m: return (int(m.group(1)), int(m.group(2) or m.group(1)))
    return None

def contar_oraciones(texto):
    return len([s for s in re.split(r"[.!?]+(?:\s|$)", texto or "") if s.strip()])

KEYWORDS_CLIMA = re.compile(
    r"cambio clim[áa]tico|clim[áa]tic[oa]s?|calentamiento|carbono|efecto invernadero|"
    r"precipitaci[oó]n|temperatura|mitigaci[oó]n|adaptaci[oó]n|sostenibilidad ambiental|"
    r"ambiental|ambientales|ecol[oó]gico|sequ[ií]a|inundaci[oó]n|biodiversidad|bioma|ecosistema",
    re.I,
)
SIN_SENAL_CLIMATICA = re.compile(
    r"(?:no (?:hay|contiene|menciona)|no se detect[oó]|sin (?:ninguna )?(?:menci[oó]n|desarrollo|vinculaci[oó]n|contenido|calificar))"
    r".{0,100}(?:cambio clim[áa]tico|variabilidad clim[áa]tica|señal clim[áa]tica|clim[áa]tic[oa])|"
    r"menci[oó]n.{0,120}(?:solo|gen[eé]rica|sin desarrollo)|"
    r"remit\w*.{0,100}(?:tema )?clim[áa]tic",
    re.I | re.S,
)


def check_secciones(doc, secs, nivel_esperado=1, path=""):
    pagina_anterior = None
    for s in secs:
        titulo = (s.get("seccion") or "").strip()
        p = f"{path}/{titulo[:40] or '?'}"
        for k in ("seccion","nivel","paginas","resumen","dimensiones","subsecciones"):
            if k not in s: err(doc, f"seccion {p}: falta clave '{k}'")
        if s.get("nivel") != nivel_esperado: err(doc, f"seccion {p}: nivel {s.get('nivel')} != esperado {nivel_esperado}")
        rango_actual = rango_pagina(s.get("paginas"))
        if pagina_anterior and rango_actual and rango_actual[0] < pagina_anterior[0]:
            err(doc, f"seccion {p}: orden de p?ginas retrocede ({s.get('paginas')} despu?s de {pagina_anterior[0]}-{pagina_anterior[1]})")
        if rango_actual:
            pagina_anterior = rango_actual
        # Reglas 7–9: front/back-matter no debe aparecer como fila.
        if SECCION_EXCLUIDA.search(titulo):
            if doc.startswith("doc11") and ANEXO_HISTORICO.search(titulo):
                pass  # excepción histórica regla 7
            else:
                err(doc, f"seccion excluida por reglas 7-9 del esquema: '{titulo}' (nivel {s.get('nivel')})")
        for d in s.get("dimensiones", []):
            if not isinstance(d, dict): err(doc, f"seccion {p}: dimension no es objeto"); continue
            if d.get("dimension") not in SLUGS: err(doc, f"seccion {p}: slug no canonico '{d.get('dimension')}'")
            if "cita" not in d or "pagina" not in d: err(doc, f"seccion {p}: dimension sin cita/pagina propia")
            rango_seccion, pagina_cita = rango_pagina(s.get("paginas")), rango_pagina(d.get("pagina"))
            if rango_seccion and pagina_cita and not (
                rango_seccion[0] <= pagina_cita[0] <= pagina_cita[1] <= rango_seccion[1]
            ):
                err(doc, f"seccion {p}: cita en pagina {d.get('pagina')} fuera del rango {s.get('paginas')}")
            if "subtipo_brecha" in d and d["dimension"] != "brechas_implementacion":
                err(doc, f"seccion {p}: subtipo_brecha en dimension no-brecha")
        if s.get("subsecciones"):
            # Padres-puente: sin piso proporcional (post-Ronda 9). El contenido vive en las hojas.
            check_secciones(doc, s["subsecciones"], nivel_esperado + 1, p)
        else:
            # Piso proporcional solo en hojas (Ronda 5 + aclaración post-Ronda 9).
            # Heurística: max(200, 55*páginas) caracteres.
            r, rng = s.get("resumen"), rango_pagina(s.get("paginas"))
            if r and rng:
                piso = max(200, 55 * (rng[1] - rng[0] + 1))
                if len(r) < piso:
                    err(
                        doc,
                        f"seccion {p}: resumen de {len(r)} caracteres, por debajo del piso "
                        f"proporcional (~{piso}) para {rng[1] - rng[0] + 1} pagina(s)",
                    )
            # Heurística: hojas sin dimensiones pero con señal climática en el resumen.
            if (not s.get("dimensiones") and r and KEYWORDS_CLIMA.search(r)
                    and not SIN_SENAL_CLIMATICA.search(r)):
                err(
                    doc,
                    f"seccion {p}: dimensiones vacías en hoja con contenido climático/ambiental "
                    f"detectado en el resumen — verificar si debe llevar al menos una dimensión",
                )

# Sin argumentos: todos los canónicos del piloto y resultados del corpus.
_PILOT_DIR = Path(__file__).resolve().parent.parent / "pilot"
_RESULTADOS_DIR = Path(__file__).resolve().parent.parent / "corpus" / "resultados"
PILOTO = sorted(
    str(p) for p in _PILOT_DIR.glob("doc*.json")
    if not re.search(r"_0[1-5]\.json$", p.name)
) + sorted(str(p) for p in _RESULTADOS_DIR.glob("*.json"))

for ruta in (sys.argv[1:] or PILOTO):
    name = ruta.rsplit("/", 1)[-1].rsplit("\\", 1)[-1].removesuffix(".json")
    raw = open(ruta, encoding="utf-8").read()
    j = json.loads(raw)
    if '"verdict"' in raw: err(name, "usa clave 'verdict' (debe ser 'veredicto')")
    # Las comparaciones explícitas con anclas son legítimas solo en validacion_anclas.
    xref_doc = json.loads(raw)
    try:
        xref_doc["tipologia"]["razonamiento_5_pasos"]["validacion_anclas"] = ""
    except (KeyError, TypeError):
        pass
    xref_raw = json.dumps(xref_doc, ensure_ascii=False)
    for match in XREF.finditer(xref_raw):
        err(name, f"posible referencia cruzada/narrativa de proceso: ...{xref_raw[max(0,match.start()-60):match.end()+60].strip()}...")
    if set(j) != {"documento","resumen_enriquecido","resumen_secciones","interpelacion","tipologia"}:
        err(name, f"bloques raiz: {sorted(j)}")
    d = j["documento"]
    faltan, sobran = DOC_KEYS - set(d), set(d) - DOC_KEYS - DOC_KEYS_OPCIONALES
    if faltan or sobran: err(name, f"claves documento difieren: faltan {faltan}, sobran {sobran}")
    if not isinstance(d.get("paginas_cuerpo"), int): err(name, "paginas_cuerpo no es entero")
    if not isinstance(d.get("paginas_totales"), int): err(name, "paginas_totales no es entero")
    if not isinstance(d.get("tiene_resumen_ejecutivo"), bool): err(name, "tiene_resumen_ejecutivo debe ser booleano")
    elif d["paginas_totales"] < d.get("paginas_cuerpo", 0): err(name, "paginas_totales menor que paginas_cuerpo")
    if not str(d.get("handle","")).startswith("https://hdl.handle.net/11362/"): err(name, f"handle sospechoso: {d.get('handle')}")
    resumen_enriquecido = j["resumen_enriquecido"]
    faltan, sobran = RESUMEN_ENRIQUECIDO_KEYS - set(resumen_enriquecido), set(resumen_enriquecido) - RESUMEN_ENRIQUECIDO_KEYS
    if faltan or sobran:
        err(name, f"claves resumen_enriquecido difieren: faltan {faltan}, sobran {sobran}")
    pregunta = resumen_enriquecido.get("pregunta_investigacion")
    if not isinstance(pregunta, str) or not pregunta.strip():
        err(name, "pregunta_investigacion ausente o vacía")
    a = resumen_enriquecido.get("alcance", {})
    if set(a) != {"ambito_aplicacion","referentes_dependencias","sectorial","temporal"}:
        err(name, f"claves alcance: {sorted(a)}")
    # conclusiones_recomendaciones: objeto canónico {conclusiones, recomendaciones}; lista = legado piloto.
    cr = j["resumen_enriquecido"].get("conclusiones_recomendaciones")
    if isinstance(cr, dict):
        if "conclusiones" not in cr or "recomendaciones" not in cr:
            err(name, "conclusiones_recomendaciones (objeto) debe tener 'conclusiones' y 'recomendaciones'")
        elif not isinstance(cr.get("conclusiones"), list) or not isinstance(cr.get("recomendaciones"), list):
            err(name, "conclusiones y recomendaciones deben ser listas")
        extras = set(cr) - {"conclusiones", "recomendaciones", "nota"}
        if extras:
            err(name, f"conclusiones_recomendaciones: claves de mas {sorted(extras)}")
    elif isinstance(cr, list):
        pass  # legado muestra de 17
    else:
        err(name, "conclusiones_recomendaciones ausente o tipo invalido (objeto o lista legacy)")
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
    # --- Chequeos Ronda 5 (heurísticos, derivados de la prueba de portabilidad multimodelo) ---
    chc = itp["como_hacerlo_concreto"]
    items = chc.get("desglose_items") or []
    # 1. Consistencia tally ↔ desglose: "M de N" debe coincidir con los ítems y sus clasificaciones.
    m_tally = re.search(r"(\d+)\s+de\s+(\d+)", str(chc.get("tally", "")))
    if m_tally and items:
        m_dice, n_dice = int(m_tally.group(1)), int(m_tally.group(2))
        concretos = sum(1 for it in items if it.get("clasificacion") == "CONCRETO")
        if n_dice != len(items): err(name, f"tally dice N={n_dice} pero desglose_items tiene {len(items)} items")
        if m_dice != concretos: err(name, f"tally dice M={m_dice} pero hay {concretos} items CONCRETO en el desglose")
    # 2. Páginas del desglose dentro de la sección de recomendaciones (regla de unidad de INTERPELACION §1.4):
    #    el test se corre sobre el texto completo de las recomendaciones, no sobre recuadros de portada.
    def _todas_secciones(secs):
        for s in secs:
            yield s
            yield from _todas_secciones(s.get("subsecciones") or [])
    rec_rangos = [rango_pagina(s.get("paginas")) for s in _todas_secciones(j["resumen_secciones"])
                  if re.search(r"recomenda|recommendation|conclusi|conclusion|propuesta|proposal|pillar", str(s.get("seccion", "")), re.I)]
    rec_rangos = [r for r in rec_rangos if r]
    if rec_rangos:
        lo, hi = min(r[0] for r in rec_rangos), max(r[1] for r in rec_rangos)
        fuera = [it for it in items if (rp := rango_pagina(it.get("pagina"))) and (rp[1] < lo or rp[0] > hi)]
        if fuera:
            err(name, f"{len(fuera)} item(s) del desglose con pagina fuera del rango de la seccion de recomendaciones ({lo}-{hi}) — posible uso de recuadro de portada/key messages")
    # 3. Largo mínimo del resumen narrativo (3-5 oraciones según esquema §2).
    narr = j["resumen_enriquecido"].get("resumen_narrativo", "")
    if contar_oraciones(narr) < 3:
        err(name, f"resumen_narrativo con {contar_oraciones(narr)} oracion(es), por debajo del piso de 3-5")
    # 4. Encoding: un JSON en español sin un solo caracter acentuado/ñ delata pérdida de tildes en la
    #    serialización del harness (observado en la prueba de portabilidad).
    prosa = narr + " ".join(str(s.get("resumen") or "") for s in j["resumen_secciones"]) + \
            " ".join(str(v.get("evidencia", "")) for v in itp.values())
    if len(prosa) > 400 and not re.search(r"[áéíóúñÁÉÍÓÚÑ¿¡]", prosa):
        err(name, "prosa en español sin tildes/enies/signos de apertura: posible perdida de encoding del harness")
    t = j["tipologia"]
    for k in ("transformacion_primaria","transformacion_secundaria","razonamiento_5_pasos",
              "tipo_documento_climatico","nivel_aplicacion","ambiguedad_pendiente_validacion"):
        if k not in t: err(name, f"tipologia: falta '{k}'")
    if "tipo_brecha" in t: err(name, "tipologia conserva 'tipo_brecha' (debe desaparecer)")
    for k in ("transformacion_primaria","transformacion_secundaria"):
        if set(t.get(k, {})) != {"numero","nombre","certeza"}: err(name, f"tipologia.{k} no es {{numero,nombre,certeza}}")
        else:
            numero, nombre = t[k].get("numero"), t[k].get("nombre")
            nombres_validos = {TRANSFORMACIONES.get(numero)} | TRANSFORMACIONES_ALIASES.get(numero, set())
            if nombre not in nombres_validos:
                err(name, f"tipologia.{k} no corresponde al canon: {numero!r} / {nombre!r}")
    ambiguedad = t.get("ambiguedad_pendiente_validacion")
    if ambiguedad is not None and (not isinstance(ambiguedad, str) or not ambiguedad.strip()):
        err(name, "ambiguedad_pendiente_validacion debe ser texto no vacío o null")
    if ambiguedad:
        certezas = {
            t.get("transformacion_primaria", {}).get("certeza"),
            t.get("transformacion_secundaria", {}).get("certeza"),
        }
        if certezas != {"Baja"}:
            err(name, "ambigüedad activa exige certeza Baja en primaria y secundaria")
    if set(t.get("razonamiento_5_pasos", {})) != {"tension_dialectica","filtro_categoria_primaria",
            "secundaria_obligatoria","justificacion_anti_copia","validacion_anclas"}:
        err(name, f"razonamiento_5_pasos incompleto: {sorted(t.get('razonamiento_5_pasos', {}))}")
    print(f"{name}: OK estructura base" if not any(e.startswith(f'[{name}]') for e in errores) else f"{name}: con observaciones")

print()
if errores:
    print(f"{len(errores)} observaciones:")
    for e in errores: print(" -", e)
    sys.exit(1)
print("Todos los JSON conformes al esquema v1 (reglas 7-9 de exclusion incluidas).")
