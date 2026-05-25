"""
Aplicación Streamlit — explorador y estadísticas (cambio climático CEPAL).

Ejecutar desde esta carpeta:
    streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from explorador import main as pagina_explorador
from visualizaciones import main as pagina_visualizaciones

st.set_page_config(
    page_title="Cambio climático · CEPAL Lab",
    page_icon="🌎",
    layout="wide",
)

pg = st.navigation(
    [
        st.Page(
            pagina_explorador,
            title="Explorador",
            icon=":material/table:",
            url_path="explorador",
        ),
        st.Page(
            pagina_visualizaciones,
            title="Estadísticas",
            icon=":material/analytics:",
            url_path="estadisticas",
        ),
    ]
)
pg.run()
