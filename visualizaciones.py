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
    _mtime_archivo,
    cargar_datos,
    cargar_mapa_clusters,
    frecuencia_temas,
    filtrar_cambio_climatico,
)
from graficos_echarts import (
    opciones_barras_periodo,
    opciones_grafo_coocurrencias,
    opciones_grafo_division_temas,
    quitar_meta,
)

ECHARTS_CDN = "https://cdn.jsdelivr.net/npm/echarts@5.6.0/dist/echarts.min.js"


def render_echarts(options: dict, height: int = 720, key: str = "chart") -> None:
    """
    Renderiza un gráfico ECharts cargando la librería directamente desde CDN.
    Se usa para gráficos que dependen de funcionalidades nuevas
    (p. ej. `emphasis.focus: "trajectory"` en sankey, que la versión empaquetada
    con `streamlit-echarts` no implementa por completo).

    Para sankey inyecta automáticamente un formatter de tooltip que:
      - muestra `real_value` en lugar del `value` (que puede estar escalado
        para balancear la altura del canvas)
      - limpia los sufijos invisibles (\\u200b) que usamos para
        desambiguar nombres de nodos
    """
    options_json = json.dumps(options, ensure_ascii=False, default=str)
    html_template = f"""
<div id="echarts-{key}" style="width: 100%; height: {height}px;"></div>
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

    with st.sidebar:
        st.header("Filtros")
        solo_clima = st.checkbox(
            'Tema "CAMBIO CLIMÁTICO" (`cepal.topicSpa`)',
            value=True,
        )
        st.divider()
        st.header("Redes")
        top_temas_div = st.slider(
            "Máx. otros temas (eje derecho)",
            min_value=15,
            max_value=80,
            value=40,
            step=5,
        )
        peso_min_div = st.slider(
            "Peso mínimo arista (división ↔ temas)",
            min_value=1,
            max_value=10,
            value=1,
        )
        top_temas_cooc = st.slider(
            "Máx. temas (coocurrencias)",
            min_value=15,
            max_value=136,
            value=60,
            step=5,
        )
        peso_min_cooc = st.slider(
            "Peso mínimo coocurrencia",
            min_value=1,
            max_value=15,
            value=2,
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

    if mapa.archivo_encontrado:
        freq = frecuencia_temas(df)
        temas_sin = sum(1 for t in freq if t not in mapa.tema_a_color)
        if temas_sin:
            st.sidebar.caption(f"{temas_sin} tema(s) sin entrada en clusters.xlsx")

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
    st.caption(
        "Diagrama Sankey: **divisiones** → **CAMBIO CLIMÁTICO** (puente central) → **otros temas**. "
        "Pasa el cursor sobre una división, sobre el nodo central o sobre un tema "
        "para resaltar toda la ruta del flujo."
    )
    opt_div = opciones_grafo_division_temas(
        df,
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
        "**excluyendo** CAMBIO CLIMÁTICO."
    )
    opt_cooc = opciones_grafo_coocurrencias(
        df, mapa, top_temas=top_temas_cooc, peso_min=peso_min_cooc
    )
    render_echarts(
        options=quitar_meta(opt_cooc),
        height=760,
        key="chart_coocurrencias",
    )

    _mostrar_leyenda_clusters(mapa, df)


def _mostrar_leyenda_clusters(mapa, df: pd.DataFrame) -> None:
    if not mapa.archivo_encontrado:
        return
    with st.expander("Leyenda de clusters (temas en el subconjunto actual)"):
        freq = frecuencia_temas(df)
        filas = [
            {
                "Tema": tema,
                "Cluster": mapa.tema_a_cluster.get(tema, "Sin cluster"),
                "Color": mapa.tema_a_color.get(tema, "#9ca3af"),
                "Frecuencia": freq[tema],
            }
            for tema, _ in sorted(freq.items(), key=lambda x: -x[1])
        ]
        if filas:
            st.dataframe(pd.DataFrame(filas), use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
