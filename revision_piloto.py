"""
Revisión del Piloto — fichas de las 17 publicaciones del piloto de Fase 2.
"""

from __future__ import annotations

import json
from glob import glob
from pathlib import Path

import streamlit as st

from comentarios_piloto import (
    comentario_de,
    guardar_comentario,
)

DIR_PILOT = Path(__file__).resolve().parent / "fase2" / "pilot"

VEREDICTO_COLOR = {"Sí": "#10B981", "Parcial": "#F59E0B", "No": "#EF4444"}

DIMENSION_COLOR: dict[str, str] = {
    "contexto_antecedentes": "#3B82F6",
    "estado_de_situacion": "#8B5CF6",
    "diagnostico_estructural": "#EF4444",
    "tendencias": "#F59E0B",
    "desafios": "#F97316",
    "oportunidades": "#10B981",
    "propuestas_politica": "#06B6D4",
    "avances_implementacion": "#6366F1",
    "brechas_implementacion": "#EC4899",
}

DIMENSION_LABEL: dict[str, str] = {
    "contexto_antecedentes": "Contexto y antecedentes",
    "estado_de_situacion": "Estado de situación",
    "diagnostico_estructural": "Diagnóstico estructural",
    "tendencias": "Tendencias",
    "desafios": "Desafíos",
    "oportunidades": "Oportunidades",
    "propuestas_politica": "Propuestas de política",
    "avances_implementacion": "Avances en implementación",
    "brechas_implementacion": "Brechas de implementación",
}

DIMENSION_RESUMEN: dict[str, str] = {
    "estado_de_situacion": "Qué está pasando (impactos, vulnerabilidad, riesgos observados).",
    "diagnostico_estructural": "Por qué pasa (causas estructurales del problema).",
    "propuestas_politica": "Qué instrumentos o acciones concretas propone.",
    "avances_implementacion": "Qué ya se implementó y con qué resultado.",
    "brechas_implementacion": "Qué falta o falla respecto de compromisos/exigencias.",
    "tendencias": "Qué evolución temporal muestra el documento.",
    "desafios": "Qué obstáculos estructurales/futuros identifica.",
    "oportunidades": "Qué ventanas favorables detecta.",
    "contexto_antecedentes": "Qué marco de contexto aporta para interpretar el análisis.",
}

DIMENSION_BADGE_COLOR: dict[str, str] = {
    "contexto_antecedentes": "blue",
    "estado_de_situacion": "violet",
    "diagnostico_estructural": "red",
    "tendencias": "orange",
    "desafios": "orange",
    "oportunidades": "green",
    "propuestas_politica": "blue",
    "avances_implementacion": "violet",
    "brechas_implementacion": "red",
}


def _pill(texto: str, color: str) -> str:
    return (
        f'<span style="display:inline-block;background:{color}22;'
        f"color:{color};padding:1px 9px;border-radius:999px;"
        f"font-size:0.78em;font-weight:500;line-height:1.5;"
        f'border:1px solid {color}55;">{texto}</span>'
    )


def _badge(texto: str, color: str) -> str:
    return (
        f'<span style="display:inline-block;background:{color};'
        f"color:#fff;padding:0 10px;border-radius:999px;"
        f"font-size:0.78em;font-weight:600;line-height:1.6;"
        f'margin:0 3px 0 0;">{texto}</span>'
    )


def _pills_dimensiones(dims: list) -> list[str]:
    partes = []
    for d in dims:
        slug = d.get("dimension", "")
        label = DIMENSION_LABEL.get(slug, slug)
        color = DIMENSION_COLOR.get(slug, "#6B7280")
        pill = _pill(label, color)
        if d.get("subtipo_brecha"):
            pill += " " + _pill(f"brecha: {d['subtipo_brecha']}", "#BE185D")
        partes.append(pill)
    return partes


def _badge_md_dimensiones(dims: list[dict]) -> str:
    partes: list[str] = []
    for d in dims:
        slug = d.get("dimension", "")
        label = DIMENSION_LABEL.get(slug, slug)
        color = DIMENSION_BADGE_COLOR.get(slug, "gray")
        partes.append(f":{color}-badge[{label}]")
        if d.get("subtipo_brecha"):
            partes.append(f":red-badge[brecha: {d['subtipo_brecha']}]")
    return " ".join(partes)


def _dims_descendencia(sec: dict) -> list[dict]:
    vistos: set[str] = set()
    acumulado: list[dict] = []

    def _push(dim: dict) -> None:
        slug = str(dim.get("dimension", ""))
        if not slug:
            return
        if slug in vistos:
            return
        vistos.add(slug)
        acumulado.append({"dimension": slug})

    def _walk(nodo: dict) -> None:
        for dim in nodo.get("dimensiones", []):
            if isinstance(dim, dict):
                _push(dim)
        for subnodo in nodo.get("subsecciones", []):
            if isinstance(subnodo, dict):
                _walk(subnodo)

    _walk(sec)
    return acumulado


def _guia_dimensiones() -> None:
    st.markdown("##### Cómo leer esta sección")
    st.caption(
        "Cada sección resume una parte del documento y puede tener una o más dimensiones analíticas. "
        "Las etiquetas son acumulativas: en secciones con subsecciones se muestran también las etiquetas de su descendencia."
    )
    slugs = [
        "contexto_antecedentes",
        "estado_de_situacion",
        "diagnostico_estructural",
        "tendencias",
        "desafios",
        "oportunidades",
        "propuestas_politica",
        "avances_implementacion",
        "brechas_implementacion",
    ]

    mitad = (len(slugs) + 1) // 2
    col_izq, col_der = st.columns(2)

    for idx, slug in enumerate(slugs):
        label = DIMENSION_LABEL.get(slug, slug)
        definicion = DIMENSION_RESUMEN.get(slug, "")
        color_hex = DIMENSION_COLOR.get(slug, "#6B7280")
        linea = f"{_pill(label, color_hex)} {definicion}"
        if idx < mitad:
            with col_izq:
                st.markdown(linea, unsafe_allow_html=True)
        else:
            with col_der:
                st.markdown(linea, unsafe_allow_html=True)
    st.divider()


def _meta_chip(etiqueta: str, valor: str) -> str:
    return (
        "<span style=\"display:inline-block;margin:0 8px 8px 0;padding:3px 10px;"
        "border-radius:999px;background:#F3F4F6;color:#374151;font-size:0.8rem;"
        "border:1px solid #E5E7EB;\">"
        f"<strong>{etiqueta}:</strong> {valor}</span>"
    )


def encabezado_publicacion(doc: dict, muestra_idx: int) -> None:
    d = doc.get("documento", {})
    tip = doc.get("tipologia", {})
    prim = tip.get("transformacion_primaria", {})

    titulo = d.get("titulo", "(sin título)")
    autoria = d.get("autoria") or "—"
    fecha = d.get("fecha") or "—"
    idioma = d.get("idioma") or "—"
    tipo = d.get("tipo_documento") or "—"
    prim_txt = f"#{prim.get('numero', '?')} {prim.get('nombre', '—')}"

    st.markdown(f"### {titulo}")
    st.caption(f"Muestra #{muestra_idx}")

    chips_html = "".join(
        [
            _meta_chip("Fecha", str(fecha)),
            _meta_chip("Idioma", str(idioma)),
            _meta_chip("Tipo", str(tipo)),
            _meta_chip("Tipología", prim_txt),
        ]
    )
    st.markdown(chips_html, unsafe_allow_html=True)

    col_autoria, col_extra = st.columns([3, 2])
    with col_autoria:
        st.markdown(f"**Autoría:** {autoria}")
    with col_extra:
        handle = d.get("handle")
        simbolo = d.get("simbolo")
        if simbolo:
            st.markdown(f"**Símbolo:** {simbolo}")
        if handle:
            st.markdown(f"**Handle:** [{handle}]({handle})")

    c1, c2, c3 = st.columns(3)
    c1.caption(f"Páginas cuerpo: {d.get('paginas_cuerpo', '—')}")
    c2.caption(f"Resumen ejecutivo: {'Sí' if d.get('tiene_resumen_ejecutivo') else 'No'}")
    c3.caption(f"Anexos: {'Sí' if d.get('tiene_anexos') else 'No'}")


# ── Tabs ────────────────────────────────────────────────────────────────


def tab_documento(doc: dict) -> None:
    d = doc.get("documento", {})
    if not d:
        st.caption("Sin datos"); return

    izq, der = st.columns(2)
    with izq:
        st.markdown(f"**Título:** {d.get('titulo', '—')}")
        st.markdown(f"**Autoría:** {d.get('autoria', '—')}")
        h = d.get("handle")
        if h:
            st.markdown(f"**Handle:** [{h}]({h})")
        else:
            st.markdown("**Handle:** —")
        st.markdown(f"**ISBN:** {d.get('isbn') or '—'}")
    with der:
        st.markdown(f"**Tipo:** {d.get('tipo_documento', '—')}")
        st.markdown(f"**Fecha:** {d.get('fecha', '—')}")
        st.markdown(f"**Idioma:** {d.get('idioma', '—')}")
        st.markdown(f"**Símbolo:** {d.get('simbolo') or '—'}")

    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Páginas (cuerpo)", d.get("paginas_cuerpo", "—"))
    c2.metric("Páginas (total)", d.get("paginas_totales", "—"))
    c3.metric("Resumen ejecutivo", "Sí" if d.get("tiene_resumen_ejecutivo") else "No")
    c4.metric("Anexos", "Sí" if d.get("tiene_anexos") else "No")


def tab_resumen(doc: dict) -> None:
    re = doc.get("resumen_enriquecido", {})
    if not re:
        st.caption("Sin datos"); return

    if re.get("resumen_narrativo"):
        st.markdown("#### Resumen narrativo")
        st.write(re["resumen_narrativo"])
        st.divider()

    if re.get("pregunta_investigacion"):
        st.markdown("#### Pregunta de investigación")
        st.write(re["pregunta_investigacion"])
        st.divider()

    alc = re.get("alcance")
    if alc:
        st.markdown("#### Alcance")
        for campo, etiqueta in [
            ("ambito_aplicacion", "Ámbito de aplicación"),
            ("referentes_dependencias", "Referentes / dependencias"),
            ("sectorial", "Sectorial"),
            ("temporal", "Temporal"),
        ]:
            v = alc.get(campo)
            if v:
                st.markdown(f"**{etiqueta}:** {v}")
            else:
                st.markdown(f"**{etiqueta}:** —")
        st.divider()

    if re.get("hallazgos_principales"):
        st.markdown(f"#### Hallazgos principales ({len(re['hallazgos_principales'])})")
        for i, h in enumerate(re["hallazgos_principales"], 1):
            st.markdown(f"{i}. {h}")
        st.divider()

    cr = re.get("conclusiones_recomendaciones")
    if cr:
        label_cr = "#### Conclusiones y recomendaciones"
        if isinstance(cr, dict):
            n = len(cr.get("conclusiones", [])) + len(cr.get("recomendaciones", []))
            label_cr = f"#### Conclusiones y recomendaciones ({n})"
        st.markdown(label_cr)
        if isinstance(cr, list):
            for i, item in enumerate(cr):
                st.markdown(f"{i+1}. {item}")
        else:
            if cr.get("conclusiones"):
                st.markdown("**Conclusiones:**")
                for c in cr["conclusiones"]:
                    st.markdown(f"- {c}")
            if cr.get("recomendaciones"):
                st.markdown("**Recomendaciones:**")
                for r in cr["recomendaciones"]:
                    st.markdown(f"- {r}")
            if cr.get("nota"):
                st.caption(f"_{cr['nota']}_")


def tab_secciones(doc: dict) -> None:
    secciones = doc.get("resumen_secciones", [])
    if not secciones:
        st.caption("Sin datos"); return

    _guia_dimensiones()

    for sec in secciones:
        _seccion_compacta(sec, 0)


def _seccion_compacta(sec: dict, nivel: int) -> None:
    titulo = sec.get("seccion", "")
    paginas = sec.get("paginas", "")
    resumen = sec.get("resumen")
    dims = sec.get("dimensiones", [])
    subs = sec.get("subsecciones", [])

    indent = "&nbsp;&nbsp;&nbsp;&nbsp;" * nivel

    dims_header = _dims_descendencia(sec)
    pills = _pills_dimensiones(dims)
    html_pills = " " + " ".join(pills) if pills else ""

    if paginas:
        cabecera_base = f"{indent}{titulo} · págs. {paginas}"
    else:
        cabecera_base = f"{indent}{titulo}"

    badges_md = _badge_md_dimensiones(dims_header)
    cabecera = f"{cabecera_base}  {badges_md}" if badges_md else cabecera_base

    # Mostramos bloques contraídos hasta el segundo nivel visual para mantener
    # consistencia entre secciones hermanas, aunque alguna no tenga subsecciones.
    mostrar_expander = bool(subs) or nivel <= 1

    if mostrar_expander:
        with st.expander(cabecera, expanded=False):
            if resumen:
                st.write(resumen)
            for d in dims:
                if subs:
                    st.markdown(f"> {d.get('cita', '')} *(p. {d.get('pagina', '?')})*")
                else:
                    slug = d.get("dimension", "")
                    label = DIMENSION_LABEL.get(slug, slug)
                    color = DIMENSION_COLOR.get(slug, "#6B7280")
                    pill = _pill(label, color)
                    if d.get("subtipo_brecha"):
                        pill += " " + _pill(f"brecha: {d['subtipo_brecha']}", "#BE185D")
                    st.markdown(
                        f"> {pill}<br>{d.get('cita', '')} *(p. {d.get('pagina', '?')})*",
                        unsafe_allow_html=True,
                    )
            for sub in subs:
                _seccion_compacta(sub, nivel + 1)
    else:
        st.markdown(f"{cabecera_base}{html_pills}", unsafe_allow_html=True)
        if resumen:
            st.write(resumen)
        for d in dims:
            slug = d.get("dimension", "")
            label = DIMENSION_LABEL.get(slug, slug)
            color = DIMENSION_COLOR.get(slug, "#6B7280")
            pill = _pill(label, color)
            if d.get("subtipo_brecha"):
                pill += " " + _pill(f"brecha: {d['subtipo_brecha']}", "#BE185D")
            st.markdown(
                f"> {pill}<br>{d.get('cita', '')} *(p. {d.get('pagina', '?')})*",
                unsafe_allow_html=True,
            )


def tab_interpelacion(doc: dict) -> None:
    interp = doc.get("interpelacion", {})
    if not interp:
        st.caption("Sin datos"); return

    st.markdown("##### Qué es la interpelación")
    st.caption(
        "La interpelación es una lectura crítica del documento contra 4 preguntas comunes. "
        "No resume el texto: evalúa si el documento propone, con evidencia, una agenda accionable "
        "para la transición climática en su ámbito de aplicación."
    )
    st.markdown("###### Componentes evaluados")
    st.markdown(
        ":green-badge[Sí] :orange-badge[Parcial] :red-badge[No]  "
        "Cada componente se califica según la solidez de la evidencia presentada en el documento."
    )
    st.markdown(
        "- **Gran impulso ambiental concreto**: si plantea un paquete coordinado de transformación, "
        "no solo medidas aisladas."
    )
    st.markdown(
        "- **Articulación de actores**: si nombra mecanismos concretos de coordinación multiactor "
        "(instituciones, plataformas o procesos)."
    )
    st.markdown(
        "- **Oportunidades productivas sostenibles**: si identifica oportunidades concretas y las "
        "vincula con empleo, productividad o desigualdad."
    )
    st.markdown(
        "- **Cómo hacerlo concreto**: si baja recomendaciones a acciones ejecutables, con desglose "
        "ítem por ítem cuando corresponde."
    )
    st.divider()

    for nombre, key in [
        ("Gran impulso ambiental concreto", "gran_impulso_ambiental_concreto"),
        ("Articulación de actores", "articulacion_actores"),
        ("Oportunidades productivas sostenibles", "oportunidades_productivas_sostenibles"),
        ("Cómo hacerlo concreto", "como_hacerlo_concreto"),
    ]:
        c = interp.get(key)
        if not c:
            continue
        v = c.get("veredicto", "")
        color = VEREDICTO_COLOR.get(v, "#6B7280")
        st.markdown(
            f"**{nombre}** {_badge(v, color)}",
            unsafe_allow_html=True,
        )
        if c.get("evidencia"):
            st.write(c["evidencia"])
        if c.get("citas"):
            for ct in c["citas"]:
                pag = ct.get("pagina", "")
                st.markdown(f"> {ct.get('cita', '')} *{'p. ' + str(pag) if pag else ''}*")
        if c.get("desglose_items"):
            for item in c["desglose_items"]:
                cls = item.get("clasificacion", "")
                color_cls = "#10B981" if cls == "CONCRETO" else "#F59E0B"
                st.markdown(
                    f"- {item.get('item', '')} {_badge(cls, color_cls)} *p. {item.get('pagina', '?')}*",
                    unsafe_allow_html=True,
                )
            if c.get("tally"):
                st.caption(c["tally"])
        if c.get("nota"):
            st.caption(f"_{c['nota']}_")
        st.divider()


def tab_tipologia(doc: dict) -> None:
    tip = doc.get("tipologia", {})
    if not tip:
        st.caption("Sin datos"); return

    st.markdown("##### Qué es la tipología")
    st.caption(
        "La tipología ubica cada documento dentro del marco de las 11 grandes transformaciones: "
        "define una transformación primaria (el objeto principal de cambio que organiza el texto) "
        "y una secundaria (el eje complementario que también estructura su argumento)."
    )
    st.caption(
        "La asignación no se hace por título o palabras sueltas: sigue un razonamiento de 5 pasos "
        "(tensión central, filtro de primaria, secundaria obligatoria, justificación anti-copia y "
        "validación con anclas de calibración). Por eso se muestra la certeza y, cuando aplica, "
        "la ambigüedad pendiente de validación."
    )

    st.markdown("#### Etiquetas tipológicas")

    certeza_color = {"Alta": "#10B981", "Media": "#F59E0B", "Baja": "#EF4444"}

    c1, c2 = st.columns(2)
    for col, key, etiqueta in [
        (c1, "transformacion_primaria", "Transformación primaria"),
        (c2, "transformacion_secundaria", "Transformación secundaria"),
    ]:
        t = tip.get(key)
        with col:
            if t:
                certeza = t.get("certeza", "")
                color_c = certeza_color.get(certeza, "#6B7280")
                st.markdown(f"**{etiqueta}**")
                st.markdown(
                    f"### #{t.get('numero', '?')} {t.get('nombre', '')} {_badge(certeza, color_c)}",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(f"**{etiqueta}:** —")

    st.divider()

    razon = tip.get("razonamiento_5_pasos")
    st.markdown("#### Razonamiento")
    if razon:
        for paso, etiqueta_paso in [
            ("tension_dialectica", "1. Tensión dialéctica"),
            ("filtro_categoria_primaria", "2. Filtro categoría primaria"),
            ("secundaria_obligatoria", "3. Secundaria obligatoria"),
            ("justificacion_anti_copia", "4. Justificación anti-copia"),
            ("validacion_anclas", "5. Validación con anclas"),
        ]:
            texto = razon.get(paso)
            if texto:
                st.markdown(f"**{etiqueta_paso}:**")
                st.write(texto)
    else:
        st.caption("Sin datos de razonamiento.")

    st.divider()

    st.markdown("#### Ambigüedad pendiente de validación")
    amb = tip.get("ambiguedad_pendiente_validacion")
    if amb:
        st.write(amb)
    else:
        st.caption("No registra ambigüedad pendiente.")

    st.divider()

    st.markdown("#### Metadatos complementarios")

    st.markdown(f"**Tipo de documento climático:** {tip.get('tipo_documento_climatico', '—')}")
    st.markdown(f"**Nivel de aplicación:** {tip.get('nivel_aplicacion', '—')}")


def tab_comentarios(doc_id: str) -> None:
    c = comentario_de(doc_id)
    texto = c.comentario

    st.markdown("##### Comentarios del equipo revisor")
    st.caption(
        "Este espacio es para validación metodológica y observaciones críticas del análisis. "
        "Puedes usarlo para confirmar criterios aplicados, señalar desacuerdos con alguna "
        "clasificación (dimensiones, interpelación o tipología), o dejar notas sobre evidencia "
        "que creas que falta o debería interpretarse de otra manera."
    )
    st.caption(
        "Los comentarios son libres: no requieren formato fijo y pueden combinar acuerdos, "
        "objeciones y sugerencias de mejora."
    )
    st.divider()

    st.text_area(
        "Tus observaciones sobre esta publicación",
        value=texto,
        height=150,
        key=f"com_{doc_id}",
        placeholder="Escribe aquí tus notas, dudas o sugerencias para el equipo del curso...",
    )

    gcol, icol = st.columns([1, 3])
    with gcol:
        if st.button("Guardar comentario", type="primary", use_container_width=True, key=f"btn_{doc_id}"):
            nuevo = st.session_state.get(f"com_{doc_id}", "")
            guardar_comentario(doc_id, nuevo.strip())
            st.success("Comentario guardado", icon="✅")
    with icol:
        if texto.strip() and c.ultima_modificacion:
            st.caption(f"Última modificación: {c.ultima_modificacion}")


# ── Carga ───────────────────────────────────────────────────────────────


@st.cache_data(show_spinner=False)
def _cargar_pilotos() -> list[dict]:
    rutas = sorted(glob(str(DIR_PILOT / "doc*.json")))
    pilotos = []
    for r in rutas:
        try:
            datos = json.loads(Path(r).read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        doc_info = datos.get("documento", {})
        pilotos.append({
            "ruta": r,
            "id": Path(r).stem,
            "num_muestra": doc_info.get("num_muestra", 0),
            "titulo": doc_info.get("titulo", "(sin título)"),
            "datos": datos,
        })
    pilotos.sort(key=lambda p: p["num_muestra"])
    return pilotos


# ── Página principal ───────────────────────────────────────────────────


def main() -> None:
    st.title("Revisión del Piloto")
    st.caption(
        "17 publicaciones del piloto de Fase 2 — "
        "seleccione una y revise su ficha estructurada por pestañas."
    )

    pilotos = _cargar_pilotos()
    if not pilotos:
        st.error(f"No se encontraron archivos JSON en `{DIR_PILOT}`")
        st.stop()

    # Selector
    opciones = {
        f"{p['id'].split('_', 1)[0]} - "
        f"{(p['titulo'] if len(p['titulo']) <= 110 else p['titulo'][:107] + '...')}": p
        for p in pilotos
    }
    seleccion = st.selectbox(
        "Publicación",
        options=list(opciones.keys()),
        index=0,
        label_visibility="collapsed",
    )
    piloto = opciones[seleccion]
    doc_id = piloto["id"]
    datos = piloto["datos"]
    muestra_idx = pilotos.index(piloto) + 1
    encabezado_publicacion(datos, muestra_idx)

    st.divider()

    # Tabs
    tabs = st.tabs(["📝 Resumen", "📑 Secciones", "🎯 Interpelación", "🏷️ Tipología", "💬 Comentarios"])

    with tabs[0]:
        tab_resumen(datos)
    with tabs[1]:
        tab_secciones(datos)
    with tabs[2]:
        tab_interpelacion(datos)
    with tabs[3]:
        tab_tipologia(datos)
    with tabs[4]:
        tab_comentarios(doc_id)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Revisión del Piloto · Cambio climático",
        page_icon="📋",
        layout="wide",
    )
    main()
