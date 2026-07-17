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
    store_etiqueta,
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

    if re.get("pregunta_investigacion"):
        with st.expander("Pregunta de investigación"):
            st.write(re["pregunta_investigacion"])

    alc = re.get("alcance")
    if alc:
        with st.expander("Alcance"):
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

    if re.get("hallazgos_principales"):
        with st.expander(f"Hallazgos principales ({len(re['hallazgos_principales'])})"):
            for i, h in enumerate(re["hallazgos_principales"], 1):
                st.markdown(f"{i}. {h}")

    cr = re.get("conclusiones_recomendaciones")
    if cr:
        label_cr = "Conclusiones y recomendaciones"
        if isinstance(cr, dict):
            n = len(cr.get("conclusiones", [])) + len(cr.get("recomendaciones", []))
            label_cr = f"Conclusiones y recomendaciones ({n})"
        with st.expander(label_cr):
            if isinstance(cr, list):
                for i, item in enumerate(cr):
                    st.markdown(f"{i+1}. {item}")
            else:
                if cr.get("conclusiones"):
                    for c in cr["conclusiones"]:
                        st.markdown(f"- {c}")
                if cr.get("recomendaciones"):
                    st.markdown("**Recomendaciones:**")
                    for r in cr["recomendaciones"]:
                        st.markdown(f"- {r}")
                if cr.get("nota"):
                    st.caption(f"_{cr['nota']}_")

    if re.get("resumen_narrativo"):
        with st.expander("Resumen narrativo"):
            st.write(re["resumen_narrativo"])


def tab_secciones(doc: dict) -> None:
    secciones = doc.get("resumen_secciones", [])
    if not secciones:
        st.caption("Sin datos"); return

    for sec in secciones:
        _seccion_compacta(sec, 0)


def _seccion_compacta(sec: dict, nivel: int) -> None:
    titulo = sec.get("seccion", "")
    paginas = sec.get("paginas", "")
    resumen = sec.get("resumen")
    dims = sec.get("dimensiones", [])
    subs = sec.get("subsecciones", [])

    indent = "&nbsp;&nbsp;&nbsp;&nbsp;" * nivel

    pills = _pills_dimensiones(dims)
    html_pills = " " + " ".join(pills) if pills else ""
    cabecera = f"{indent}{titulo}{' · ' + paginas if paginas else ''}{html_pills}"

    if subs:
        with st.expander(cabecera, expanded=nivel < 1):
            if resumen:
                st.write(resumen)
            for d in dims:
                st.markdown(f"> {d.get('cita', '')} *(p. {d.get('pagina', '?')})*")
            for sub in subs:
                _seccion_compacta(sub, nivel + 1)
    else:
        st.markdown(f"{cabecera}", unsafe_allow_html=True)
        if resumen:
            st.write(resumen)
        for d in dims:
            st.markdown(f"> {d.get('cita', '')} *(p. {d.get('pagina', '?')})*")


def tab_interpelacion(doc: dict) -> None:
    interp = doc.get("interpelacion", {})
    if not interp:
        st.caption("Sin datos"); return

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
                st.markdown(
                    f"**{etiqueta}:** #{t.get('numero', '?')} {t.get('nombre', '')} "
                    f"{_badge(certeza, color_c)}",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(f"**{etiqueta}:** —")
    st.divider()

    razon = tip.get("razonamiento_5_pasos")
    if razon:
        with st.expander("Razonamiento (5 pasos)"):
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
                    st.divider()

    st.markdown(f"**Tipo de documento climático:** {tip.get('tipo_documento_climatico', '—')}")
    st.markdown(f"**Nivel de aplicación:** {tip.get('nivel_aplicacion', '—')}")

    amb = tip.get("ambiguedad_pendiente_validacion")
    if amb:
        with st.expander("Ambigüedad pendiente de validación"):
            st.write(amb)


def tab_comentarios(doc_id: str) -> None:
    c = comentario_de(doc_id)
    texto = c.comentario

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
        st.caption(f"Persistencia: {store_etiqueta()}")


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
        "seleccioná una y revisá su ficha estructurada por pestañas."
    )

    pilotos = _cargar_pilotos()
    if not pilotos:
        st.error(f"No se encontraron archivos JSON en `{DIR_PILOT}`")
        st.stop()

    # Selector
    opciones = {
        f"{p['id']} — {p['titulo'][:80]}": p
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
    doc_info = datos.get("documento", {})

    # Barra de info compacta
    tip = datos.get("tipologia", {})
    prim = tip.get("transformacion_primaria", {})
    c1, c2, c3, c4 = st.columns(4)
    c1.caption(f"**{doc_id}** · Muestra #{doc_info.get('num_muestra', '?')}")
    c2.caption(f"📅 {doc_info.get('fecha', '—')} · 🌐 {doc_info.get('idioma', '—')}")
    c3.caption(f"📄 {doc_info.get('tipo_documento', '—')[:40]}")
    c4.caption(f"🏷️ #{prim.get('numero', '?')} {prim.get('nombre', '')[:25]}")

    st.divider()

    # Tabs
    tabs = st.tabs(["📄 Documento", "📝 Resumen", "📑 Secciones", "🎯 Interpelación", "🏷️ Tipología", "💬 Comentarios"])

    with tabs[0]:
        tab_documento(datos)
    with tabs[1]:
        tab_resumen(datos)
    with tabs[2]:
        tab_secciones(datos)
    with tabs[3]:
        tab_interpelacion(datos)
    with tabs[4]:
        tab_tipologia(datos)
    with tabs[5]:
        tab_comentarios(doc_id)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Revisión del Piloto · Cambio climático",
        page_icon="📋",
        layout="wide",
    )
    main()
