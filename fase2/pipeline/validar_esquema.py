"""Chequeo de conformidad de los JSON del pipeline contra esquema_json_v1.md.

Uso: python validar_esquema.py <ruta1.json> [<ruta2.json> ...]
Sin argumentos, valida todos los JSON canónicos de fase2/pilot/ (excluye variantes
multimodelo doc09_01..05). Solo stdlib, igual que el resto del pipeline. Creado en Ronda 3;
chequeo de secciones excluidas (reglas 7–9) agregado en Ronda 8.

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
XREF = re.compile(r"doc\s*\.?\s*0?9|doc\s*\.?\s*11|doc\s*\.?\s*13|documento[s]?\s+(9|11|13)\b|versi[oó]n previa|Ronda [12]", re.I)
# Títulos de sección excluidos (esquema §2 reglas 7–9). Anclados al inicio del título.
# Anexos: se alerta salvo excepción histórica doc11 (regla 7).
SECCION_EXCLUIDA = re.compile(
    r"^(?:"
    r"bibliograf[ií]a|bibliography|referencias?(?:\s+bibliogr[aá]ficas?)?|references?|"
    r"acr[oó]nimos?|acronyms?|list\s+of\s+acronyms|glosario|glossary|"
    r"pr[oó]logo|prologue|prefacio|preface|"
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

def check_secciones(doc, secs, nivel_esperado=1, path=""):
    for s in secs:
        titulo = (s.get("seccion") or "").strip()
        p = f"{path}/{titulo[:40] or '?'}"
        for k in ("seccion","nivel","paginas","resumen","dimensiones","subsecciones"):
            if k not in s: err(doc, f"seccion {p}: falta clave '{k}'")
        if s.get("nivel") != nivel_esperado: err(doc, f"seccion {p}: nivel {s.get('nivel')} != esperado {nivel_esperado}")
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

# Sin argumentos: todos los canónicos del piloto (excluye variantes multimodelo doc09_01..05).
_PILOT_DIR = Path(__file__).resolve().parent.parent / "pilot"
PILOTO = sorted(
    str(p) for p in _PILOT_DIR.glob("doc*.json")
    if not re.search(r"_0[1-5]\.json$", p.name)
)

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
    faltan, sobran = DOC_KEYS - set(d), set(d) - DOC_KEYS - DOC_KEYS_OPCIONALES
    if faltan or sobran: err(name, f"claves documento difieren: faltan {faltan}, sobran {sobran}")
    if not isinstance(d.get("paginas_cuerpo"), int): err(name, "paginas_cuerpo no es entero")
    if not isinstance(d.get("paginas_totales"), int): err(name, "paginas_totales no es entero")
    elif d["paginas_totales"] < d.get("paginas_cuerpo", 0): err(name, "paginas_totales menor que paginas_cuerpo")
    if not str(d.get("handle","")).startswith("https://hdl.handle.net/11362/"): err(name, f"handle sospechoso: {d.get('handle')}")
    a = j["resumen_enriquecido"].get("alcance", {})
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
    rec_rangos = [rango_pagina(s.get("paginas")) for s in j["resumen_secciones"]
                  if re.search(r"recomenda|recommendation|conclusi|conclusion", str(s.get("seccion", "")), re.I)]
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
