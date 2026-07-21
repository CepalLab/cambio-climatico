"""
Ficha técnica — Construcción del corpus definitivo de cambio climático (CEPAL).

Muestra la metodología aplicada para depurar el listado de publicaciones
y llegar a los 244 documentos definitivos de la Fase 2.
"""

from __future__ import annotations

import streamlit as st

from datos import (
    ARCHIVO_DATOS,
    ARCHIVO_CLUSTERS,
    _mtime_archivo,
    cargar_datos,
    cargar_documentos_definitivos,
    filtrar_cambio_climatico,
    filtrar_excluir_boletines,
    filtrar_solo_sustantivas,
    _excluir_documentos,
    DOCUMENTOS_A_AGREGAR,
)


def mostrar_ficha_tecnica(df_completo: pd.DataFrame, df_final: pd.DataFrame) -> None:
    """Renderiza el contenido de la ficha técnica (reutilizable desde página o dialog)."""

    st.markdown(
        "Para la selección inicial se tomaron todos aquellos documentos sustantivos "
        "producidos por CEPAL entre 2015 y 2025 que tenían en su lista de temas "
        '"CAMBIO CLIMÁTICO" — 248 en total — luego se excluyeron algunos y se '
        "agregaron 14 adicionales que el equipo consideró _core_ en la producción "
        'editorial de la CEPAL pero que no tenían el tema "CAMBIO CLIMÁTICO" '
        "(ver detalles abajo)."
    )

    # ── Resumen ejecutivo ──────────────────────────────────────────────
    st.header("Resumen ejecutivo")

    df_cc = filtrar_cambio_climatico(df_completo)
    df_sust = filtrar_solo_sustantivas(df_cc)
    df_sin_bol = filtrar_excluir_boletines(df_sust)
    df_exc = _excluir_documentos(df_sin_bol)

    n_base = len(df_sin_bol)
    n_excluidos = n_base - len(df_exc)
    n_agregados = len(df_final) - len(df_exc)

    col1, col2, col3 = st.columns(3)
    col1.metric("Corpus base (sustantivas + CC)", f"{n_base:,}")
    col2.metric("Excluidos", f"{n_excluidos}")
    col3.metric("Agregados", f"+{n_agregados}")

    st.metric("Total definitivo", f"{len(df_final):,}")

    # ── Criterios de exclusión ─────────────────────────────────────────
    st.header("Criterios de exclusión")

    st.markdown("""
    Se excluyeron documentos por las siguientes razones:

    | Criterio | Motivo |
    |----------|--------|
    | **Acuerdo Regional** | Versiones duplicadas en varios idiomas |
    | **Reglas de procedimiento del Acuerdo de Escazú** | Documento administrativo, no sustantivo |
    | **Catálogo de publicaciones** | Catálogo de la División de Desarrollo Sostenible |
    | **The Hummingbird y revistas** | No todos los artículos son de autoría de CEPAL |
    | **Versiones "accesibles"** | Versiones adaptadas, no la versión oficial |
    | **Boletines** | Excluidos por tipo_doc == "Boletines" |
    """)

    # ── Documentos agregados ───────────────────────────────────────────
    st.header("Documentos agregados (Período de Sesiones y Foro Regional)")

    st.markdown("""
    Se agregaron 14 documentos clave que no estaban en el corpus original
    pero son fundamentales para el análisis de cambio climático:
    """)

    # Período de Sesiones
    st.subheader("Período de Sesiones de CEPAL")
    docs_ps = [d for d in DOCUMENTOS_A_AGREGAR if d["anio"] in [2024, 2022, 2020, 2018, 2016]]
    for i, doc in enumerate(docs_ps, 1):
        st.markdown(f"{i}. **{doc['titulo']}** ({doc['anio']})")

    # Foro Regional
    st.subheader("Foro Regional sobre Desarrollo Sostenible")
    docs_foro = [d for d in DOCUMENTOS_A_AGREGAR if d["anio"] not in [2024, 2022, 2020, 2018, 2016]]
    for i, doc in enumerate(docs_foro, 1):
        st.markdown(f"{i}. **{doc['titulo']}** ({doc['anio']})")

    # ── Flujo del proceso ──────────────────────────────────────────────
    st.header("Flujo del proceso")

    st.markdown("""
    ```
    ┌─────────────────────────────────────┐
    │  datos_dashboard_final.xlsx         │
    │  (corpus completo)                  │
    └─────────────┬───────────────────────┘
                  │
                  ▼
    ┌─────────────────────────────────────┐
    │  Filtrar: tema "CAMBIO CLIMÁTICO"   │
    └─────────────┬───────────────────────┘
                  │
                  ▼
    ┌─────────────────────────────────────┐
    │  Filtrar: solo sustantivas           │
    └─────────────┬───────────────────────┘
                  │
                  ▼
    ┌─────────────────────────────────────┐
    │  Excluir boletines                   │
    └─────────────┬───────────────────────┘
                  │
                  ▼
    ┌─────────────────────────────────────┐
    │  Excluir documentos específicos      │
    │  (duplicados, revistas, etc.)        │
    └─────────────┬───────────────────────┘
                  │
                  ▼
    ┌─────────────────────────────────────┐
    │  Agregar 14 documentos adicionales   │
    │  (Período de Sesiones + Foro)        │
    └─────────────┬───────────────────────┘
                  │
                  ▼
    ┌─────────────────────────────────────┐
    │  244 documentos definitivos          │
    │  + columnas de trazabilidad          │
    └─────────────────────────────────────┘
    ```

    """)

    # ── Trazabilidad ───────────────────────────────────────────────────
    st.header("Trazabilidad")

    n_original = len(df_final[df_final["__origen"] == "corpus_original"])
    n_agregados_real = len(df_final[df_final["__origen"] == "agregado_fase2"])

    col_a, col_b = st.columns(2)
    col_a.metric("Del corpus original", f"{n_original}")
    col_b.metric("Agregados en Fase 2", f"{n_agregados_real}")

    st.markdown("""
    Cada documento incluye metadatos de trazabilidad:
    - `__origen`: `corpus_original` o `agregado_fase2`
    - `__justificacion`: Razón de inclusión/exclusión
    - `__fecha_inclusion`: Timestamp de procesamiento
    - `__fase`: `fase2_depuracion`
    """)

    # ── Archivos de salida ─────────────────────────────────────────────
    st.header("Archivos de salida")

    st.markdown("""
    - **`documentos_definitivos_trazabilidad.csv`** — Listado completo con metadatos
    - **`coocurrencias_periodos.pptx`** — 3 láminas de coocurrencias (2015-2018, 2019-2022, 2023-2026)
    - **Explorador** — Vista interactiva con filtros y búsqueda
    - **Estadísticas** — Gráficos ECharts del corpus definitivo
    """)

    # ── Botón de descarga ──────────────────────────────────────────────
    csv = df_final.to_csv(index=False, encoding="utf-8-sig")
    st.download_button(
        label="Descargar listado completo (CSV)",
        data=csv,
        file_name="documentos_definitivos_trazabilidad.csv",
        mime="text/csv",
        use_container_width=True,
    )


def main() -> None:
    st.title("Ficha técnica del corpus")
    st.caption("Metodología de construcción de los 244 documentos definitivos para Fase 2.")

    df_completo = cargar_datos()
    df_final = cargar_documentos_definitivos(_mtime=_mtime_archivo(ARCHIVO_DATOS))

    mostrar_ficha_tecnica(df_completo, df_final)

    st.divider()
    st.markdown(
        "<div style='text-align:center;font-size:0.8em;color:#888;'>"
        "<em>Elaborado por CEPAL Lab · 2026</em></div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
