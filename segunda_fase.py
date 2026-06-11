"""
Segunda fase de documentos - cambio climático (CEPAL).

Ejecutar la app completa (explorador + estadísticas + segunda fase):
    streamlit run app.py

Solo esta página:
    streamlit run segunda_fase.py
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from datos import (
    ARCHIVO_DATOS,
    ARCHIVO_CLUSTERS,
    _mtime_archivo,
    cargar_datos,
    cargar_mapa_clusters,
    filtrar_cambio_climatico,
    filtrar_solo_sustantivas,
    filtrar_excluir_boletines,
)
from explorador import (
    CAMPOS_VISTA_RAPIDA,
    formatear_fecha_es,
    mostrar_detalle_campo,
    mostrar_temas_pills,
    preparar_vista_tabla,
)

COLUMNA_URI = "dc.identifier.uri"
COLUMNA_VER_DETALLE = "🔍"

# Documentos que deben excluirse según las instrucciones
DOCUMENTOS_A_EXCLUIR = [
    "Acuerdo Regional",  # Versiones duplicadas en varios idiomas
    "Reglas de procedimiento del Acuerdo de Escazú",
    "Catálogo de publicaciones de la División de Desarrollo Sostenible y Asentamientos Humanos",
    "The Hummingbird",  # Revistas que deben excluirse
    # Versiones accesibles de documentos de CEPAL (se identificarán por patrón)
]

# Documentos adicionales que deben agregarse
DOCUMENTOS_A_AGREGAR = [
    {
        "titulo": "América Latina y el Caribe ante las trampas del desarrollo: Transformaciones indispensables y cómo gestionarlas",
        "anio": 2024,
        "handle": "https://hdl.handle.net/11362/80727"
    },
    {
        "titulo": "Hacia la transformación del modelo de desarrollo en América Latina y el Caribe: producción, inclusión y sostenibilidad",
        "anio": 2022,
        "handle": "https://hdl.handle.net/11362/48304"
    },
    {
        "titulo": "Construir un nuevo futuro: una recuperación transformadora con igualdad y sostenibilidad",
        "anio": 2020,
        "handle": "https://hdl.handle.net/11362/46227"
    },
    {
        "titulo": "La ineficiencia de la desigualdad",
        "anio": 2018,
        "handle": "https://hdl.handle.net/11362/43442"
    },
    {
        "titulo": "Horizontes 2030: la igualdad en el centro del desarrollo Sostenible",
        "anio": 2016,
        "handle": "https://hdl.handle.net/11362/40159"
    },
    {
        "titulo": "Agenda 2030 en América Latina y el Caribe: ¿cómo acelerar el paso hacia su cumplimiento en la nueva era de incertidumbre y fragmentación geopolítica?",
        "anio": 2026,
        "handle": "https://hdl.handle.net/11362/89774"
    },
    {
        "titulo": "América Latina y el Caribe y la Agenda 2030 a cinco años de la meta: ¿cómo gestionar las transformaciones para acelerar el progreso?",
        "anio": 2025,
        "handle": "https://hdl.handle.net/11362/81405"
    },
    {
        "titulo": "América Latina y el Caribe ante el desafío de acelerar el paso hacia el cumplimiento de la Agenda 2030: transiciones hacia la sostenibilidad",
        "anio": 2024,
        "handle": "https://hdl.handle.net/11362/69132"
    },
    {
        "titulo": "América Latina y el Caribe en la mitad del camino hacia 2030: avances y propuestas de aceleración",
        "anio": 2023,
        "handle": "https://hdl.handle.net/11362/48823"
    },
    {
        "titulo": "Una década de acción para un cambio de época",
        "anio": 2022,
        "handle": "https://hdl.handle.net/11362/47745"
    },
    {
        "titulo": "INFORME ANUAL DE PROGRESO: Construir un futuro mejor: acciones para fortalecer la Agenda 2030 para el Desarrollo Sostenible",
        "anio": 2021,
        "handle": "https://hdl.handle.net/11362/46682"
    },
    {
        "titulo": "Informe de avance cuatrienal sobre el progreso y los desafíos regionales de la Agenda 2030 para el Desarrollo Sostenible en América Latina y el Caribe",
        "anio": 2019,
        "handle": "https://hdl.handle.net/11362/44551"
    },
    {
        "titulo": "Segundo informe anual sobre el progreso y los desafíos regionales de la Agenda 2030 para el Desarrollo Sostenible en América Latina y el Caribe",
        "anio": 2018,
        "handle": "https://hdl.handle.net/11362/43415"
    },
    {
        "titulo": "Informe anual sobre el progreso y los desafíos regionales de la Agenda 2030 para el Desarrollo Sostenible en América Latina y el Caribe",
        "anio": 2017,
        "handle": "https://hdl.handle.net/11362/41173"
    }
]


def excluir_documentos(df: pd.DataFrame) -> pd.DataFrame:
    """Excluye documentos según las instrucciones"""
    # Excluir documentos con títulos específicos
    for titulo in DOCUMENTOS_A_EXCLUIR:
        df = df[~df["dc.title"].str.contains(titulo, case=False, na=False)]
    
    # Excluir versiones accesibles de documentos de CEPAL (patrón)
    df = df[~df["dc.title"].str.contains("accesible", case=False, na=False)]
    
    # Excluir catálogo de publicaciones (específicamente el de la División de Desarrollo Sostenible y Asentamientos Humanos)
    # No excluimos toda la división, solo el catálogo específico
    df = df[~df["dc.title"].str.contains("Catálogo de publicaciones", case=False, na=False)]
    
    # Excluir revistas de CEPAL (excepto artículos sustantivos de CEPAL)
    # Las revistas generalmente están marcadas en tipo_gr == "Boletines y Revistas"
    if "tipo_gr" in df.columns:
        es_revista = df["tipo_gr"].astype(str).eq("Boletines y Revistas")
        # Excluir las revistas que no sean documentos sustantivos
        df = df[~es_revista]
    
    return df


def buscar_documento_inteligente(df: pd.DataFrame, doc: dict) -> dict | None:
    """Busca un documento usando múltiples estrategias"""
    # Estrategia 1: Buscar por handle/URI
    if "handle" in doc and pd.notna(doc["handle"]):
        mask = df['dc.identifier.uri'].astype(str).str.contains(doc["handle"], case=False, na=False)
        resultados = df[mask]
        if not resultados.empty:
            return resultados.iloc[0].to_dict()
    
    # Estrategia 2: Buscar por título completo (primeras palabras significativas)
    titulo_palabras = doc["titulo"].split()[:5]
    for palabra in titulo_palabras:
        if len(palabra) > 5:  # Solo palabras significativas
            mask = df['dc.title'].str.contains(palabra, case=False, na=False)
            resultados = df[mask]
            if not resultados.empty:
                # Filtrar por año si es disponible
                if "anio" in doc:
                    resultados_anio = resultados[resultados['dc.year'].astype(str).str.contains(str(doc["anio"]), na=False)]
                    if not resultados_anio.empty:
                        return resultados_anio.iloc[0].to_dict()
                # Si no hay coincidencia de año, devolver el primero
                return resultados.iloc[0].to_dict()
    
    # Estrategia 3: Buscar solo por año (último recurso)
    if "anio" in doc:
        mask = df['dc.year'].astype(str).str.contains(str(doc["anio"]), na=False)
        resultados = df[mask]
        # Buscar documento que contenga palabras clave del título
        for palabra in doc["titulo"].split():
            if len(palabra) > 5:
                resultados_filtrados = resultados[resultados['dc.title'].str.contains(palabra, case=False, na=False)]
                if not resultados_filtrados.empty:
                    return resultados_filtrados.iloc[0].to_dict()
    
    return None


def agregar_documentos(df_base: pd.DataFrame) -> pd.DataFrame:
    """Agrega documentos adicionales al DataFrame (los 14 documentos recomendados)"""
    # Crear un nuevo DataFrame con los documentos adicionales
    nuevos_documentos = []
    handles_en_base = set(df_base[COLUMNA_URI].dropna().astype(str))
    
    # Cargar dataset completo una sola vez para eficiencia
    df_completo = cargar_datos()
    
    for doc in DOCUMENTOS_A_AGREGAR:
        # Chequear si el handle ya está en la base
        handle = doc.get("handle", "")
        if handle in handles_en_base:
            # Ya existe en la base, no duplicar
            continue
        
        # Prioridad 1: Buscar el handle EXACTO en el dataset completo
        registro_completo = df_completo[df_completo[COLUMNA_URI] == handle]
        
        if len(registro_completo) > 0:
            # Encontrado con handle exacto en dataset completo - usar siempre
            nuevo_doc = registro_completo.iloc[0].to_dict()
            nuevos_documentos.append(nuevo_doc)
        else:
            # Si no está con handle exacto en dataset, crear entrada básica
            # No usar búsqueda inteligente porque puede encontrar documentos incorrectos
            nuevo_doc = {
                "dc.title": doc["titulo"],
                "dc.year": doc["anio"],
                "dc.identifier.uri": doc["handle"],
                "cepal.topicSpa": [],  # Sin topics asignados
                "division": "Documentos adicionales",
                "tipo_gr": "Documentos adicionales",
                "dc.description.abstract": f"Documento adicional para segunda fase. Año: {doc['anio']}"
            }
            nuevos_documentos.append(nuevo_doc)
    
    # Convertir a DataFrame
    df_nuevos = pd.DataFrame(nuevos_documentos) if nuevos_documentos else pd.DataFrame()
    
    # Combinar con el dataset base (solo agregar los que no estaban)
    if len(df_nuevos) > 0:
        df_combinado = pd.concat([df_base, df_nuevos], ignore_index=True)
    else:
        df_combinado = df_base.copy()
    return df_combinado


def _limpiar_tras_dialogo() -> None:
    st.session_state.pop("_dialogo_fila_idx", None)
    st.session_state["_editor_rev_segfase"] = st.session_state.get("_editor_rev_segfase", 0) + 1


@st.dialog("Vista rápida del registro", width="large", on_dismiss=_limpiar_tras_dialogo)
def _dialogo_vista_rapida(fila: pd.Series, mapa=None) -> None:
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

    if st.button("Cerrar", type="primary", use_container_width=True):
        _limpiar_tras_dialogo()
        st.rerun()


def main() -> None:
    """Página principal de la segunda fase de documentos"""
    st.title("Documentos para 2da fase")
    
    df = cargar_datos()
    mapa_clusters = cargar_mapa_clusters(_mtime=_mtime_archivo(ARCHIVO_CLUSTERS))
    
    df_cambio_climatico = filtrar_cambio_climatico(df)
    df_sustantivos = filtrar_solo_sustantivas(df_cambio_climatico)
    df_sin_boletines = filtrar_excluir_boletines(df_sustantivos)
    df_filtrado = excluir_documentos(df_sin_boletines)
    df_final = agregar_documentos(df_filtrado)
    
    with st.expander(f"Cómo se construyó este listado ({len(df_final)} documentos)"):
        st.markdown(f"""
        - **Base**: {len(df_sin_boletines)} documentos sustantivos con tema "CAMBIO CLIMÁTICO"
        - **Excluidos**: {len(df_sin_boletines) - len(df_filtrado)} (Acuerdo Regional duplicado, versiones accesibles, revistas)
        - **Agregados**: {len(df_final) - len(df_filtrado)} (documentos del Período de Sesiones y Foro Regional sobre DSS)
        """)
    
    # Mostrar tabla con resultados
    columnas_mostrar = [
        "dc.title",
        "dc.year",
        "division",
        "cepal.topicSpa",
        "dc.identifier.uri"
    ]
    columnas_existentes = [col for col in columnas_mostrar if col in df_final.columns]
    
    df_vista = preparar_vista_tabla(df_final[columnas_existentes], max_chars=120)
    df_vista.insert(0, COLUMNA_VER_DETALLE, [False] * len(df_vista))
    
    column_cfg: dict = {}
    for col in columnas_existentes:
        if col == "cepal.topicSpa":
            column_cfg[col] = st.column_config.ListColumn(
                col, width="large", help="Temas del registro",
            )
        elif col == "dc.identifier.uri":
            column_cfg[col] = st.column_config.LinkColumn(
                col, display_text="Abrir enlace",
                help="Clic para abrir en otra pestaña",
            )
    column_cfg[COLUMNA_VER_DETALLE] = st.column_config.CheckboxColumn(
        "🔍 ver", width="small",
        help="Click para abrir el popup con detalle completo.",
    )
    
    rev_editor = st.session_state.get("_editor_rev_segfase", 0)
    edited = st.data_editor(
        df_vista,
        use_container_width=True,
        hide_index=True,
        height=740,
        column_config=column_cfg,
        disabled=columnas_existentes,
        key=f"editor_segfase_v{rev_editor}",
    )
    
    for i, ojo in enumerate(edited[COLUMNA_VER_DETALLE].tolist()):
        if bool(ojo) and st.session_state.get("_dialogo_fila_idx") != i:
            st.session_state["_dialogo_fila_idx"] = i
            _dialogo_vista_rapida(df_final.iloc[i], mapa_clusters)
            break
    
    # Descargar listado
    csv = df_final.to_csv(index=False, encoding='utf-8')
    st.download_button(
        label="Descargar listado (CSV)",
        data=csv,
        file_name="documentos_segunda_fase.csv",
        mime="text/csv"
    )


if __name__ == "__main__":
    main()