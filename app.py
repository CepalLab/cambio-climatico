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
    initial_sidebar_state="collapsed",
)

# Tabs un poco más grandes + stepper del number_input con flechas en vez de +/-.
# Los selectores con data-testid son los que Streamlit expone públicamente; si
# cambian en una versión futura habría que reajustar.
st.markdown(
    """
    <style>
    [data-testid="stPageLink-NavLink"] {
        font-size: 1.05rem !important;
        padding: 0.5rem 0.95rem !important;
    }
    [data-testid="stNumberInputStepUp"],
    [data-testid="stNumberInputStepDown"] {
        position: relative;
    }
    [data-testid="stNumberInputStepUp"] > *,
    [data-testid="stNumberInputStepDown"] > * {
        visibility: hidden;
    }
    [data-testid="stNumberInputStepUp"]::after,
    [data-testid="stNumberInputStepDown"]::after {
        position: absolute;
        inset: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        pointer-events: none;
        color: var(--text-color, currentColor);
        visibility: visible;
    }
    [data-testid="stNumberInputStepUp"]::after { content: "▶"; }
    [data-testid="stNumberInputStepDown"]::after { content: "◀"; }
    </style>
    """,
    unsafe_allow_html=True,
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
    ],
    position="top",
)
pg.run()
