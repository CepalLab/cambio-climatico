"""
Página de estadísticas — visualizaciones ECharts del corpus de cambio climático.
"""

from __future__ import annotations

import json

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from streamlit_echarts import st_echarts

from datos import (
    ARCHIVO_CLUSTERS,
    ARCHIVO_DATOS,
    PERIODOS_BINS,
    _mtime_archivo,
    cargar_datos,
    cargar_mapa_clusters,
    frecuencia_temas,
    filtrar_cambio_climatico,
    filtrar_excluir_boletines,
    filtrar_periodos,
    filtrar_solo_sustantivas,
)
from graficos_echarts import (
    opciones_barras_periodo,
    opciones_grafo_coocurrencias,
    opciones_grafo_division_temas,
    quitar_meta,
)

ECHARTS_CDN = "https://cdn.jsdelivr.net/npm/echarts@5.6.0/dist/echarts.min.js"


def render_echarts(
    options: dict,
    height: int = 720,
    key: str = "chart",
    max_width: int | None = None,
) -> None:
    """
    Renderiza un gráfico ECharts cargando la librería directamente desde CDN.
    Se usa para gráficos que dependen de funcionalidades nuevas
    (p. ej. `emphasis.focus: "trajectory"` en sankey, que la versión empaquetada
    con `streamlit-echarts` no implementa por completo).

    `max_width` (px) cap-ea el ancho del wrapper. Útil para `layout: "none"`
    con posiciones precomputadas: si el canvas se hace mucho más ancho que la
    grilla del layout (al colapsar el sidebar) las x se estiran y la red se
    ve dispersa. Capando el ancho preservamos el aspect ratio del layout.

    Para sankey inyecta automáticamente un formatter de tooltip que:
      - muestra `real_value` en lugar del `value` (que puede estar escalado
        para balancear la altura del canvas)
      - limpia los sufijos invisibles (\\u200b) que usamos para
        desambiguar nombres de nodos
    """
    options_json = json.dumps(options, ensure_ascii=False, default=str)
    wrapper_style = "width: 100%;"
    if max_width:
        wrapper_style += f" max-width: {max_width}px; margin: 0 auto;"
    html_template = f"""
<div style="{wrapper_style}">
<div id="echarts-{key}" style="width: 100%; height: {height}px;"></div>
</div>
<script src="{ECHARTS_CDN}"></script>
<script>
(function() {{
    var el = document.getElementById('echarts-{key}');
    var chart = echarts.init(el, null, {{ renderer: 'canvas' }});
    var options = {options_json};
    var clean = function(s) {{ return String(s == null ? '' : s).replace(/\\u200b/g, ''); }};
    var series0 = options.series && options.series[0];
    var chartType = series0 && series0.type;
    options.tooltip = options.tooltip || {{}};
    if (chartType === 'sankey') {{
        options.tooltip.formatter = function(params) {{
            var d = params.data || {{}};
            if (params.dataType === 'edge') {{
                var val = (typeof d.real_value !== 'undefined') ? d.real_value : params.value;
                return clean(d.source) + ' &rarr; ' + clean(d.target)
                    + '<br/><b>' + val + '</b> publicaciones';
            }}
            if (params.dataType === 'node' && typeof d.real_value !== 'undefined') {{
                return clean(params.name) + '<br/><b>' + d.real_value + '</b> publicaciones';
            }}
            return clean(params.name);
        }};
    }} else if (chartType === 'graph') {{
        options.tooltip.formatter = function(params) {{
            var d = params.data || {{}};
            if (params.dataType === 'node') {{
                var pubs = (typeof d.pubCount !== 'undefined') ? d.pubCount : params.value;
                var cooc = (typeof d.coocCount !== 'undefined') ? d.coocCount : 0;
                return '<b>' + clean(params.name) + '</b>'
                    + '<br/>Publicaciones con este tema: <b>' + pubs + '</b>'
                    + '<br/>Co-ocurre con: <b>' + cooc + '</b> temas';
            }}
            if (params.dataType === 'edge') {{
                return clean(d.source) + ' &harr; ' + clean(d.target)
                    + '<br/>Publicaciones en común: <b>' + params.value + '</b>';
            }}
            return clean(params.name);
        }};
    }}
    chart.setOption(options);
    if (chartType === 'graph') {{
        chart.on('click', function(params) {{
            if (params.dataType === 'node') {{
                chart.dispatchAction({{
                    type: 'focusNodeAdjacency',
                    seriesIndex: params.seriesIndex,
                    dataIndex: params.dataIndex
                }});
            }} else {{
                chart.dispatchAction({{ type: 'unfocusNodeAdjacency', seriesIndex: 0 }});
            }}
        }});
    }}
    var ro = new ResizeObserver(function() {{ chart.resize(); }});
    ro.observe(el);
    window.addEventListener('resize', function() {{ chart.resize(); }});
}})();
</script>
"""
    components.html(html_template, height=height + 20, scrolling=False)


def main() -> None:
    st.title("Estadísticas del corpus")
    st.caption(
        "Visualizaciones sobre el conjunto filtrado. "
        "Gráficos con [streamlit-echarts](https://github.com/andfanilo/streamlit-echarts) "
        "y redes estilo [ECharts graph](https://echarts.apache.org/examples/en/editor.html?c=graph)."
    )

    if not ARCHIVO_DATOS.exists():
        st.error(f"No se encontró el archivo de datos: {ARCHIVO_DATOS}")
        st.stop()

    df_completo = cargar_datos(_mtime=_mtime_archivo(ARCHIVO_DATOS))
    mapa = cargar_mapa_clusters(_mtime=_mtime_archivo(ARCHIVO_CLUSTERS))

    solo_clima = True
    solo_sustantivas = True
    excluir_boletines = True

    todos_periodos = [etiqueta for etiqueta, _, _ in PERIODOS_BINS]

    with st.sidebar:
        st.subheader("Periodo")
        periodos_sel = st.multiselect(
            "Bins de años",
            options=todos_periodos,
            default=todos_periodos,
            help=(
                "Filtra el Sankey y la red de coocurrencias por uno o varios "
                "bins de años. El gráfico de barras siempre muestra los tres "
                "periodos. Sin selección equivale a no filtrar."
            ),
        )

        st.divider()
        st.subheader("Sankey: división ↔ temas")
        top_temas_div = st.slider(
            "Máx. otros temas a mostrar",
            min_value=15,
            max_value=80,
            value=40,
            step=5,
            help="Cantidad máxima de temas (no CAMBIO CLIMÁTICO) en la columna derecha del Sankey.",
        )
        peso_min_div = st.slider(
            "Peso mínimo de arista",
            min_value=1,
            max_value=10,
            value=1,
            help="Mínimo de publicaciones que debe tener una conexión para aparecer en el Sankey.",
        )

        st.divider()
        st.subheader("Red de coocurrencias entre temas")
        top_temas_cooc = st.slider(
            "Máx. temas a mostrar",
            min_value=15,
            max_value=136,
            value=60,
            step=5,
            help="Cuántos temas (nodos) entran en el grafo de coocurrencias.",
        )
        peso_min_cooc = st.slider(
            "Peso mínimo de coocurrencia",
            min_value=1,
            max_value=15,
            value=2,
            help="Mínimo de publicaciones compartidas para que dos temas queden conectados.",
        )

        st.divider()
        if not mapa.archivo_encontrado:
            st.warning(
                f"No se encontró `{ARCHIVO_CLUSTERS.name}`. "
                "Los temas se mostrarán en gris. Ver `CLUSTERS.md`."
            )
        elif mapa.columnas_detectadas:
            st.caption(
                "Columnas clusters: "
                + ", ".join(c for c in mapa.columnas_detectadas if c)
            )

    df = filtrar_cambio_climatico(df_completo) if solo_clima else df_completo
    if solo_sustantivas:
        df = filtrar_solo_sustantivas(df)
    if excluir_boletines:
        df = filtrar_excluir_boletines(df)

    df_periodo = filtrar_periodos(df, periodos_sel)
    periodo_activo = len(df_periodo) != len(df)

    if mapa.archivo_encontrado:
        freq = frecuencia_temas(df_periodo)
        temas_sin = sum(1 for t in freq if t not in mapa.tema_a_color)
        if temas_sin:
            st.sidebar.caption(f"{temas_sin} tema(s) sin entrada en clusters.xlsx")

    if periodo_activo:
        etiqueta_periodo = ", ".join(periodos_sel) if periodos_sel else "—"
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Registros (corpus)", f"{len(df):,}")
        col_m2.metric(f"Registros en {etiqueta_periodo}", f"{len(df_periodo):,}")
    else:
        st.metric("Registros en análisis", f"{len(df):,}")

    st.subheader("Publicaciones por periodo")
    opt_barras = opciones_barras_periodo(df)
    meta = opt_barras.pop("_meta", {})
    st.caption(
        f"Bins fijos 2015-2018, 2019-2022, 2023-2026. "
        f"Sin año válido: **{meta.get('sin_anio', 0)}** · "
        f"Fuera de rango: **{meta.get('fuera_rango', 0)}**."
    )
    st_echarts(
        options=quitar_meta(opt_barras),
        height="380px",
        theme="streamlit",
        key="chart_periodos",
    )

    st.subheader("Red división ↔ cambio climático ↔ otros temas")
    cap_periodo = (
        f" · periodo: **{', '.join(periodos_sel)}**" if periodo_activo and periodos_sel else ""
    )
    st.caption(
        "Diagrama Sankey: **divisiones** → **CAMBIO CLIMÁTICO** (puente central) → **otros temas**. "
        "Pasa el cursor sobre una división, sobre el nodo central o sobre un tema "
        "para resaltar toda la ruta del flujo." + cap_periodo
    )
    opt_div = opciones_grafo_division_temas(
        df_periodo,
        mapa,
        top_temas=top_temas_div,
        peso_min=peso_min_div,
    )
    render_echarts(
        options=quitar_meta(opt_div),
        height=920,
        key="division_temas",
    )

    st.subheader("Coocurrencias entre temas")
    st.caption(
        "Temas que aparecen juntos en una publicación, "
        "**excluyendo** CAMBIO CLIMÁTICO." + cap_periodo
    )
    opt_cooc = opciones_grafo_coocurrencias(
        df_periodo, mapa, top_temas=top_temas_cooc, peso_min=peso_min_cooc
    )
    render_echarts(
        options=quitar_meta(opt_cooc),
        height=760,
        key="chart_coocurrencias",
        max_width=900,
    )

    _mostrar_leyenda_clusters(mapa, df_periodo)


def _mostrar_leyenda_clusters(mapa, df: pd.DataFrame) -> None:
    if not mapa.archivo_encontrado:
        return
    with st.expander("Frecuencia de temas"):
        freq = frecuencia_temas(df)
        filas = [
            {
                "Tema": tema,
                "Cluster": mapa.tema_a_cluster.get(tema, "Sin cluster"),
                "Frecuencia": freq[tema],
            }
            for tema, _ in sorted(freq.items(), key=lambda x: -x[1])
        ]
        if filas:
            st.dataframe(pd.DataFrame(filas), use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
