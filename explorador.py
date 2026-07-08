"""
Explorador de metadatos — cambio climático (CEPAL).

Ejecutar la app completa (explorador + estadísticas):
    streamlit run app.py

Solo esta página:
    streamlit run explorador.py
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from datos import (
    ARCHIVO_CLUSTERS,
    ARCHIVO_DATOS,
    COLOR_SIN_CLUSTER,
    MapaClusters,
    _mtime_archivo,
    cargar_datos,
    cargar_documentos_definitivos,
    cargar_mapa_clusters,
    color_tema,
)
from topic_spa import contiene_tema, normalizar_a_lista, temas_a_texto

COLUMNA_URI = "dc.identifier.uri"
COLUMNA_VER_DETALLE = "🔍"

# Selección por lotes sobre el filtro actual.
# Oculto por ahora; cambiar a True para reactivar el expander de acciones masivas.
MOSTRAR_ACCIONES_MASIVAS = False

# Campos del popup de vista rápida (se leen del registro completo, no solo columnas visibles)
CAMPOS_VISTA_RAPIDA: list[tuple[str, str]] = [
    ("dc.title", "Título"),
    ("division", "División"),
    ("cepal.topicSpa", "Temas"),
    ("dc.description.abstract", "Resumen"),
    ("dc.date.issued", "Fecha de publicación"),
    ("dc.identifier.uri", "Enlace"),
]


def formatear_fecha_es(valor) -> str:
    """Convierte una fecha a formato español dd/mm/aaaa. Si solo viene el año
    o no se puede parsear, devuelve el texto original sin inventar día/mes."""
    import re

    if pd.isna(valor):
        return ""
    texto = str(valor).strip()
    if not texto:
        return ""
    if re.fullmatch(r"\d{4}", texto):
        return texto
    fecha = pd.to_datetime(texto, errors="coerce")
    if pd.isna(fecha):
        return texto
    return fecha.strftime("%d/%m/%Y")

COLUMNAS_ORDEN_PRIORITARIAS: tuple[str, ...] = (
    "dc.year",
    "dc.date.issued",
    "dc.title",
    "dc.date.accessioned",
    "dc.date.available",
)

PLANTILLA_DEFECTO = "Revisión"
OPCIONES_PLANTILLA = ["Personalizado", "Todas las columnas"]  # + claves PLANTILLAS abajo

PLANTILLAS: dict[str, list[str]] = {
    "Textos": ["dc.title", "dc.description.abstract"],
    "Revisión": [
        "dc.title",
        "dc.description.abstract",
        "dc.year",
        "tipo_gr",
        "cepal.topicSpa",
        "dc.identifier.uri",
        "division",
    ],
    "Autoría y fechas": [
        "dc.title",
        "dc.contributor.author",
        "dc.date.issued",
        "dc.year",
        "dc.identifier.uri",
    ],
}

OPCIONES_PLANTILLA.extend(PLANTILLAS.keys())


def truncar(valor, max_chars: int) -> str:
    if pd.isna(valor):
        return ""
    texto = str(valor)
    if len(texto) <= max_chars:
        return texto
    return texto[:max_chars] + "…"


def columnas_por_plantilla(nombre: str, todas: list[str]) -> list[str]:
    if nombre == "Personalizado":
        return [c for c in PLANTILLAS["Textos"] if c in todas]
    if nombre == "Todas las columnas":
        return list(todas)
    return [c for c in PLANTILLAS.get(nombre, []) if c in todas]


def opciones_multiselect(
    todas: list[str],
    filtro_texto: str,
    seleccion: list[str],
    plantilla: str,
) -> list[str]:
    """
    Opciones del multiselect: filtro de búsqueda + columnas ya elegidas + plantilla activa.
    Evita que Streamlit descarte columnas de la plantilla que no están en options.
    """
    if filtro_texto.strip():
        filtradas = [c for c in todas if filtro_texto.lower() in c.lower()]
    else:
        filtradas = list(todas)
    necesarias = set(seleccion) | set(columnas_por_plantilla(plantilla, todas))
    return sorted(set(filtradas) | necesarias)


def es_columna_enlace(nombre: str, serie: pd.Series) -> bool:
    nombre_bajo = nombre.lower()
    if any(p in nombre_bajo for p in ("uri", "url", "link")):
        return True
    muestra = serie.dropna().astype(str).head(30)
    if muestra.empty:
        return False
    return muestra.str.match(r"https?://", na=False).mean() > 0.5


def es_url_valida(valor) -> bool:
    if pd.isna(valor):
        return False
    texto = str(valor).strip()
    return texto.startswith("http://") or texto.startswith("https://")


def construir_column_config(df: pd.DataFrame, columnas: list[str]) -> dict:
    config: dict = {}
    for col in columnas:
        if col == "cepal.topicSpa":
            config[col] = st.column_config.ListColumn(
                col,
                width="large",
                help="Temas del registro (pills)",
            )
        elif es_columna_enlace(col, df[col]):
            config[col] = st.column_config.LinkColumn(
                col,
                display_text="Abrir enlace",
                help="Clic para abrir en otra pestaña",
            )
    return config


def opciones_orden(columnas_visibles: list[str]) -> list[str]:
    vistos: set[str] = set()
    opciones = ["— sin orden —"]
    for col in COLUMNAS_ORDEN_PRIORITARIAS:
        if col in columnas_visibles and col not in vistos:
            opciones.append(col)
            vistos.add(col)
    for col in columnas_visibles:
        if col not in vistos:
            opciones.append(col)
    return opciones


def _clave_orden_columna(serie: pd.Series, nombre_col: str) -> pd.Series:
    nombre_bajo = nombre_col.lower()
    if nombre_col == "cepal.topicSpa":
        return serie.map(temas_a_texto).astype(str).str.casefold()
    if "year" in nombre_bajo:
        return pd.to_numeric(serie, errors="coerce")
    if "date" in nombre_bajo:
        return pd.to_datetime(serie, errors="coerce")
    numerico = pd.to_numeric(serie, errors="coerce")
    if len(serie) > 0 and numerico.notna().mean() >= 0.85:
        return numerico
    if serie.dtype == object or serie.dtype.name == "string":
        return serie.astype(str).str.casefold()
    return serie


def ordenar_dataframe(
    df: pd.DataFrame, columna: str | None, ascendente: bool
) -> pd.DataFrame:
    if not columna or columna not in df.columns:
        return df
    clave = _clave_orden_columna(df[columna], columna)
    return (
        df.assign(__sort_key=clave)
        .sort_values("__sort_key", ascending=ascendente, na_position="last", kind="mergesort")
        .drop(columns="__sort_key")
    )


def altura_tabla(n_filas: int, max_chars: int, con_temas_pills: bool = False) -> int:
    """Altura ajustada al alto real de las filas de `st.data_editor` (~35 px),
    sin cap superior, para que las N filas entren sin scroll interno."""
    altura_encabezado = 35
    altura_fila = 35
    if max_chars > 180:
        altura_fila += 3
    return altura_encabezado + max(n_filas, 1) * altura_fila + 4


def preparar_vista_tabla(df: pd.DataFrame, max_chars: int) -> pd.DataFrame:
    vista = df.copy()
    for col in vista.columns:
        if col == "cepal.topicSpa":
            vista[col] = vista[col].map(normalizar_a_lista)
        elif es_columna_enlace(col, vista[col]):
            vista[col] = vista[col].apply(
                lambda v: str(v).strip() if es_url_valida(v) else None
            )
        elif vista[col].dtype == object or vista[col].dtype.name == "string":
            vista[col] = vista[col].map(lambda v, m=max_chars: truncar(v, m))
    return vista


def marcar_limpieza_tras_dialogo() -> None:
    """on_dismiss del dialog: resetea el guard, incrementa el rev del editor para
    forzar una instancia nueva (con 🔍 en False) y limpia keys viejas."""
    st.session_state.pop("_dialogo_fila_idx", None)
    st.session_state["_editor_rev"] = st.session_state.get("_editor_rev", 0) + 1
    for k in list(st.session_state.keys()):
        if isinstance(k, str) and (
            k.startswith("editor_marcado_") or k.startswith("editor_vista_")
        ):
            del st.session_state[k]


_COLOR_TEXTO_PILL = "#ffffff"
_ALPHA_FONDO_PILL = 0.75


def _hex_a_rgba(hex_color: str, alpha: float) -> str:
    """Convierte '#rrggbb' a 'rgba(r, g, b, alpha)' para fondo tenue."""
    h = hex_color.lstrip("#")
    if len(h) != 6:
        return f"rgba(156, 163, 175, {alpha})"
    try:
        r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return f"rgba(156, 163, 175, {alpha})"
    return f"rgba({r}, {g}, {b}, {alpha})"


def _html_pill(texto: str, color_fondo: str) -> str:
    fondo_rgba = _hex_a_rgba(color_fondo, _ALPHA_FONDO_PILL)
    return (
        f'<span style="display:inline-block;background-color:{fondo_rgba};'
        f"color:{_COLOR_TEXTO_PILL};padding:3px 10px;border-radius:999px;"
        f"font-size:0.82em;font-weight:500;line-height:1.4;"
        f'margin:2px 4px 2px 0;white-space:nowrap;">{texto}</span>'
    )


def mostrar_temas_pills(valor, mapa: MapaClusters | None = None) -> None:
    temas = normalizar_a_lista(valor)
    if not temas:
        st.caption("_vacío_")
        return
    pills_html: list[str] = []
    for tema in temas:
        color = color_tema(tema, mapa) if mapa is not None else COLOR_SIN_CLUSTER
        pills_html.append(_html_pill(tema, color))
    st.markdown(
        f'<div style="display:flex;flex-wrap:wrap;gap:2px;">{"".join(pills_html)}</div>',
        unsafe_allow_html=True,
    )


@st.dialog("Vista rápida del registro", width="large", on_dismiss=marcar_limpieza_tras_dialogo)
def dialogo_vista_rapida(fila: pd.Series, mapa: MapaClusters | None = None) -> None:
    """Popup de detalle del registro."""
    for campo, etiqueta in CAMPOS_VISTA_RAPIDA:
        if campo not in fila.index:
            continue
        valor = fila[campo]
        st.markdown(f"**{etiqueta}**")
        if campo == "cepal.topicSpa":
            mostrar_temas_pills(valor, mapa)
        elif campo == "dc.identifier.uri":
            mostrar_detalle_campo(campo, valor)
        elif campo == "dc.date.issued":
            fecha_es = formatear_fecha_es(valor)
            if fecha_es:
                st.write(fecha_es)
            else:
                st.caption("_vacío_")
        elif pd.isna(valor) or str(valor).strip() == "":
            st.caption("_vacío_")
        else:
            st.write(str(valor))
    if "dc.year" in fila.index and (
        "dc.date.issued" not in fila.index
        or pd.isna(fila.get("dc.date.issued"))
        or str(fila.get("dc.date.issued", "")).strip() == ""
    ):
        st.markdown("**Año**")
        v_anio = fila["dc.year"]
        st.write(str(v_anio) if pd.notna(v_anio) else "_vacío_")

    # Mostrar trazabilidad
    st.divider()
    st.markdown("### Trazabilidad")
    if "__origen" in fila.index:
        origen = fila["__origen"]
        justificacion = fila.get("__justificacion", "")
        st.caption(f"**Origen**: {origen}")
        if justificacion:
            st.caption(f"**Justificación**: {justificacion}")

    if st.button("Cerrar", type="primary", use_container_width=True):
        marcar_limpieza_tras_dialogo()
        st.rerun()


def mostrar_detalle_campo(nombre: str, valor) -> None:
    if pd.isna(valor) or str(valor).strip() == "":
        st.caption("_vacío_")
    elif es_url_valida(valor):
        url = str(valor).strip()
        st.markdown(f"[{url}]({url})")
    else:
        st.write(str(valor))


def main() -> None:
    st.title("Explorador de publicaciones")
    st.caption("Corpus definitivo de publicaciones sobre cambio climático para Fase 2.")

    if not ARCHIVO_DATOS.exists():
        st.error(f"No se encontró el archivo de datos: {ARCHIVO_DATOS}")
        st.stop()

    df_completo = cargar_documentos_definitivos(_mtime=_mtime_archivo(ARCHIVO_DATOS))
    mapa_clusters = cargar_mapa_clusters(_mtime=_mtime_archivo(ARCHIVO_CLUSTERS))
    todas_las_columnas = sorted(df_completo.columns.tolist())

    col_filtro = "— ninguno —"
    modo_vacio = "Todos"
    valores: list = []

    columnas_visibles = columnas_por_plantilla(PLANTILLA_DEFECTO, todas_las_columnas)
    max_tabla = 120
    filas_pagina = 30

    df_base = df_completo

    texto_busqueda = st.text_input(
        "Buscar texto",
        placeholder="Palabra en las columnas visibles…",
    )

    with st.sidebar:
        st.subheader("Filtro rápido por campo")
        col_filtro = st.selectbox(
            "Campo",
            ["— ninguno —", *columnas_visibles],
            help="Filtra por vacío/con valor o por valor concreto.",
        )
        if col_filtro != "— ninguno —":
            modo_vacio = st.radio(
                "Contenido",
                ["Todos", "Solo vacíos", "Solo con valor"],
                horizontal=True,
            )
            if col_filtro in df_base.columns:
                serie_ref = df_base[col_filtro]
                if serie_ref.nunique(dropna=True) <= 20:
                    valores = st.multiselect(
                        "Valores",
                        sorted(serie_ref.dropna().unique(), key=str),
                        placeholder="Cualquiera",
                    )
                else:
                    valores = []

        st.divider()
        st.subheader("Orden global")
        orden_col = st.selectbox(
            "Ordenar por",
            opciones_orden(columnas_visibles),
            help=(
                "Ordena todo el conjunto filtrado antes de paginar. "
                "Las flechas del encabezado en la tabla solo reordenan la página visible."
            ),
        )
        orden_desc = st.toggle(
            "Descendente (mayor → menor)",
            value=False,
            help="Útil para ver primero años o fechas recientes (p. ej. dc.year 2026).",
        )

        st.divider()
        st.caption(f"**{len(df_completo):,}** filas · **{len(todas_las_columnas)}** columnas")

    if not columnas_visibles:
        st.warning("Selecciona al menos una columna en la barra lateral.")
        st.stop()

    df = df_base

    if texto_busqueda.strip():
        patron = texto_busqueda.strip()
        cols_para_buscar = [c for c in columnas_visibles if c in df.columns]
        if cols_para_buscar:
            mask = (
                df[cols_para_buscar]
                .astype(str)
                .apply(lambda col: col.str.contains(patron, case=False, na=False))
                .any(axis=1)
            )
            df = df[mask]

    if col_filtro != "— ninguno —" and col_filtro in df.columns:
        serie = df[col_filtro]
        if modo_vacio == "Solo vacíos":
            df = df[serie.isna() | serie.astype(str).str.strip().eq("")]
        elif modo_vacio == "Solo con valor":
            df = df[serie.notna() & serie.astype(str).str.strip().ne("")]
        if col_filtro in df.columns and valores:
            df = df[df[col_filtro].isin(valores)]

    columna_orden = None if orden_col == "— sin orden —" else orden_col
    ascendente = not orden_desc
    clave_orden = (columna_orden, ascendente)
    if st.session_state.get("_clave_orden") != clave_orden:
        st.session_state["_clave_orden"] = clave_orden
        st.session_state["pagina_tabla"] = 1

    if columna_orden:
        df = ordenar_dataframe(df, columna_orden, ascendente)

    total = len(df)
    if total == 0:
        st.info("No hay registros con los filtros actuales.")
        st.stop()

    paginas = max(1, (total - 1) // filas_pagina + 1)
    if "pagina_tabla" not in st.session_state:
        st.session_state["pagina_tabla"] = 1
    st.session_state["pagina_tabla"] = max(
        1, min(int(st.session_state["pagina_tabla"]), paginas)
    )

    col_p1, col_info = st.columns([1, 4])
    with col_p1:
        pagina = st.number_input(
            "Página",
            min_value=1,
            max_value=paginas,
            step=1,
            key="pagina_tabla",
        )
    with col_info:
        orden_txt = ""
        if columna_orden:
            flecha = "↓" if orden_desc else "↑"
            orden_txt = f" · orden: **{columna_orden}** {flecha}"
        st.markdown(
            f"**{total:,}** registros · página **{pagina}** de **{paginas}**{orden_txt}"
        )

    uris_filtradas: list[str] = (
        df[COLUMNA_URI].astype(str).tolist() if COLUMNA_URI in df.columns else []
    )
    n_filtrado = len(uris_filtradas)
    if MOSTRAR_ACCIONES_MASIVAS and n_filtrado:
        marcadas_en_filtro = sum(
            1 for u in uris_filtradas if seleccion.marca_de(u).incluir
        )
        with st.expander(
            f"⚡ Acciones masivas sobre el filtro actual "
            f"({marcadas_en_filtro}/{n_filtrado} marcadas)",
            expanded=False,
        ):
            st.caption(
                "Aplica a TODOS los registros del filtro actual (no solo la página visible). "
                "Conserva las notas existentes. Un solo commit a GitHub."
            )
            col_bulk_a, col_bulk_b = st.columns(2)
            with col_bulk_a:
                with st.popover(
                    f"Incluir los {n_filtrado}",
                    use_container_width=True,
                ):
                    st.markdown(
                        f"Vas a marcar **{n_filtrado}** registros como Incluir "
                        f"(de los cuales {marcadas_en_filtro} ya están marcados)."
                    )
                    if st.button(
                        "Confirmar inclusión",
                        type="primary",
                        key="bulk_inc_confirm",
                        use_container_width=True,
                    ):
                        try:
                            with st.spinner("Aplicando…"):
                                n = _aplicar_bulk(uris_filtradas, incluir=True)
                            st.toast(
                                f"{n} marca(s) actualizada(s)" if n else "Sin cambios",
                                icon="✅",
                            )
                            st.session_state["_editor_rev"] = (
                                st.session_state.get("_editor_rev", 0) + 1
                            )
                            st.rerun()
                        except Exception as exc:  # noqa: BLE001
                            st.error(f"No se pudo aplicar: {exc}")
            with col_bulk_b:
                with st.popover(
                    f"Desmarcar los {n_filtrado}",
                    use_container_width=True,
                ):
                    st.markdown(
                        f"Vas a quitar la marca a **{n_filtrado}** registros "
                        f"(actualmente {marcadas_en_filtro} están marcados)."
                    )
                    if st.button(
                        "Confirmar desmarcado",
                        type="primary",
                        key="bulk_exc_confirm",
                        use_container_width=True,
                    ):
                        try:
                            with st.spinner("Aplicando…"):
                                n = _aplicar_bulk(uris_filtradas, incluir=False)
                            st.toast(
                                f"{n} marca(s) quitada(s)" if n else "Sin cambios",
                                icon="✅",
                            )
                            st.session_state["_editor_rev"] = (
                                st.session_state.get("_editor_rev", 0) + 1
                            )
                            st.rerun()
                        except Exception as exc:  # noqa: BLE001
                            st.error(f"No se pudo aplicar: {exc}")

    inicio = (pagina - 1) * filas_pagina
    fin = min(inicio + filas_pagina, total)
    df_pagina = df.iloc[inicio:fin].reset_index(drop=True)

    cols_para_mostrar = [c for c in columnas_visibles if c in df_pagina.columns]
    df_vista = preparar_vista_tabla(df_pagina[cols_para_mostrar], max_tabla)

    uris_pagina: list[str] = []
    if COLUMNA_URI in df_pagina.columns:
        uris_pagina = df_pagina[COLUMNA_URI].astype(str).tolist()
        df_vista.insert(0, COLUMNA_VER_DETALLE, [False] * len(df_vista))

    column_cfg = construir_column_config(df_pagina, cols_para_mostrar)
    altura = altura_tabla(
        len(df_pagina),
        max_tabla,
        con_temas_pills="cepal.topicSpa" in columnas_visibles,
    )

    if uris_pagina:
        column_cfg[COLUMNA_VER_DETALLE] = st.column_config.CheckboxColumn(
            "🔍 ver",
            width="small",
            help="Click para abrir el popup con detalle completo.",
        )
        rev_editor = st.session_state.get("_editor_rev", 0)
        clave_editor = f"editor_vista_p{pagina}_v{rev_editor}"
        edited = st.data_editor(
            df_vista,
            use_container_width=True,
            hide_index=True,
            height=altura,
            column_config=column_cfg,
            disabled=cols_para_mostrar,
            key=clave_editor,
        )

        # 🔍 → abrir dialog (procesa el primero detectado)
        indice_a_inspeccionar: int | None = None
        for i, ojo in enumerate(edited[COLUMNA_VER_DETALLE].tolist()):
            if bool(ojo):
                indice_a_inspeccionar = i
                break

        if indice_a_inspeccionar is not None:
            indice_global = inicio + indice_a_inspeccionar
            if st.session_state.get("_dialogo_fila_idx") != indice_global:
                st.session_state["_dialogo_fila_idx"] = indice_global
                dialogo_vista_rapida(df.iloc[indice_global], mapa_clusters)
    else:
        rev_editor = st.session_state.get("_editor_rev", 0)
        st.data_editor(
            df_vista,
            use_container_width=True,
            hide_index=True,
            height=altura,
            column_config=column_cfg,
            disabled=cols_para_mostrar,
            key=f"editor_vista_p{pagina}_v{rev_editor}",
        )

    st.caption(
        "Columna **🔍 ver**: tilda para abrir el popup completo con detalle y trazabilidad. "
        "Orden global: barra lateral → «Ordenar por» (las flechas de la tabla solo reordenan la página visible)."
    )

    col_dl_a, col_dl_b = st.columns(2)
    with col_dl_a:
        st.download_button(
            "Descargar CSV (filtro actual)",
            data=df[cols_para_mostrar].to_csv(index=False).encode("utf-8-sig"),
            file_name="export_filtrado.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with col_dl_b:
        cols_trazabilidad = [c for c in ["dc.title", "dc.year", "dc.identifier.uri",
                                          "__origen", "__justificacion", "__fecha_inclusion"]
                             if c in df.columns]
        st.download_button(
            f"Descargar definitivos con trazabilidad ({len(df)})",
            data=df[cols_trazabilidad].to_csv(index=False).encode("utf-8-sig"),
            file_name="documentos_definitivos_trazabilidad.csv",
            mime="text/csv",
            use_container_width=True,
            help="Documentos definitivos con metadatos de origen y justificación.",
        )


if __name__ == "__main__":
    st.set_page_config(
        page_title="Explorador · Cambio climático",
        page_icon="🌎",
        layout="wide",
    )
    main()
