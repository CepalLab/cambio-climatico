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
    cargar_datos,
    filtrar_cambio_climatico,
)
import seleccion

COLUMNA_URI = "dc.identifier.uri"
COLUMNA_INCLUIR_VISUAL = "✓"
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
        "handle": "https://repositorio.cepal.org/server/api/core/bitstreams/ddaf4444-dcbc-48a9-afd2-06306ac3e5c3/content"
    },
    {
        "titulo": "Hacia la transformación del modelo de desarrollo en América Latina y el Caribe: producción, inclusión y sostenibilidad",
        "anio": 2022,
        "handle": "https://repositorio.cepal.org/server/api/core/bitstreams/cfdfbffc-660a-4b8c-86e8-532bcf884af5/content"
    },
    {
        "titulo": "Construir un nuevo futuro: una recuperación transformadora con igualdad y sostenibilidad",
        "anio": 2020,
        "handle": "https://hdl.handle.net/11362/46682"
    },
    {
        "titulo": "La ineficiencia de la desigualdad",
        "anio": 2018,
        "handle": "https://repositorio.cepal.org/server/api/core/bitstreams/cd373168-ed4d-4bb7-b70a-4d9fd80c68a9/content"
    },
    {
        "titulo": "Horizontes 2030: la igualdad en el centro del desarrollo Sostenible",
        "anio": 2016,
        "handle": "https://periododesesiones.cepal.org/36/es/horizontes-2030-la-igualdad-centro-desarrollo-sostenible"
    },
    {
        "titulo": "Agenda 2030 en América Latina y el Caribe: ¿cómo acelerar el paso hacia su cumplimiento en la nueva era de incertidumbre y fragmentación geopolítica?",
        "anio": 2026,
        "handle": "https://foroalc2030.cepal.org/2026/es/documentos/agenda-2030-america-latina-caribe-como-acelerar-paso-su-cumplimiento-la-nueva-era"
    },
    {
        "titulo": "América Latina y el Caribe y la Agenda 2030 a cinco años de la meta: ¿cómo gestionar las transformaciones para acelerar el progreso?",
        "anio": 2025,
        "handle": "https://foroalc2030.cepal.org/2025/es/documentos/america-latina-caribe-la-agenda-2030-cinco-anos-la-meta-como-gestionar-transformaciones"
    },
    {
        "titulo": "América Latina y el Caribe ante el desafío de acelerar el paso hacia el cumplimiento de la Agenda 2030: transiciones hacia la sostenibilidad",
        "anio": 2024,
        "handle": "https://foroalc2030.cepal.org/2024/es/documentos/america-latina-caribe-desafio-acelerar-paso-cumplimiento-la-agenda-2030-transiciones-la"
    },
    {
        "titulo": "América Latina y el Caribe en la mitad del camino hacia 2030: avances y propuestas de aceleración",
        "anio": 2023,
        "handle": "https://foroalc2030.cepal.org/2023/es/documentos/america-latina-caribe-la-mitad-camino-2030-avances-propuestas-aceleracion"
    },
    {
        "titulo": "Una década de acción para un cambio de época",
        "anio": 2022,
        "handle": "https://hdl.handle.net/11362/47745"
    },
    {
        "titulo": "INFORME ANUAL DE PROGRESO: Construir un futuro mejor: acciones para fortalecer la Agenda 2030 para el Desarrollo Sostenible",
        "anio": 2021,
        "handle": "https://foroalc2030.cepal.org/2021/es/documentos/informe-anual-progreso-construir-un-futuro-mejor-acciones-fortalecer-la-agenda-2030"
    },
    {
        "titulo": "Informe de avance cuatrienal sobre el progreso y los desafíos regionales de la Agenda 2030 para el Desarrollo Sostenible en América Latina y el Caribe",
        "anio": 2019,
        "handle": "https://foroalc2030.cepal.org/2019/es/documentos/informe-avance-cuatrienal-progreso-desafios-regionales-la-agenda-2030-desarrollo"
    },
    {
        "titulo": "Segundo informe anual sobre el progreso y los desafíos regionales de la Agenda 2030 para el Desarrollo Sostenible en América Latina y el Caribe",
        "anio": 2018,
        "handle": "https://foroalc2030.cepal.org/2018/es/documentos/segundo-informe-anual-progreso-desafios-regionales-la-agenda-2030-desarrollo-sostenible"
    },
    {
        "titulo": "Informe anual sobre el progreso y los desafíos regionales de la Agenda 2030 para el Desarrollo Sostenible en América Latina y el Caribe",
        "anio": 2017,
        "handle": "https://foroalc2030.cepal.org/2017/es/documentos/informe-anual-progreso-desafios-regionales-la-agenda-2030-desarrollo-sostenible-america"
    }
]


def excluir_documentos(df: pd.DataFrame) -> pd.DataFrame:
    """Excluye documentos según las instrucciones"""
    # Excluir documentos con títulos específicos
    for titulo in DOCUMENTOS_A_EXCLUIR:
        df = df[~df["dc.title"].str.contains(titulo, case=False, na=False)]
    
    # Excluir versiones accesibles de documentos de CEPAL (patrón)
    df = df[~df["dc.title"].str.contains("accesible", case=False, na=False)]
    
    # Excluir catálogo de publicaciones de la División de Desarrollo Sostenible y Asentamientos Humanos
    df = df[~df["division"].str.contains("Desarrollo Sostenible y Asentamientos Humanos", case=False, na=False)]
    
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
    """Agrega documentos adicionales al DataFrame"""
    # Crear un nuevo DataFrame con los documentos adicionales
    nuevos_documentos = []
    
    for doc in DOCUMENTOS_A_AGREGAR:
        # Intentar encontrar el documento usando búsqueda inteligente
        resultado = buscar_documento_inteligente(df_base, doc)
        
        if resultado is not None:
            # Si existe en el dataset, usar los datos originales
            nuevos_documentos.append(resultado)
        else:
            # Si no existe, crear una entrada básica con el título proporcionado
            nuevo_doc = {
                "dc.title": doc["titulo"],
                "dc.year": doc["anio"],
                "dc.identifier.uri": doc["handle"],
                "cepal.topicSpa": "CAMBIO CLIMÁTICO",  # Asignar tema por relevancia
                "division": "Documentos adicionales",  # Marcar como documento adicional
                "tipo_gr": "Documentos adicionales",
                "dc.description.abstract": f"Documento adicional para segunda fase. Año: {doc['anio']}"
            }
            nuevos_documentos.append(nuevo_doc)
    
    # Convertir a DataFrame
    df_nuevos = pd.DataFrame(nuevos_documentos)
    
    # Combinar con el dataset base
    df_combinado = pd.concat([df_base, df_nuevos], ignore_index=True)
    
    return df_combinado


def main() -> None:
    """Página principal de la segunda fase de documentos"""
    st.title("Documentos para 2da fase")
    st.markdown("""
    Esta vista muestra el listado depurado de documentos para la segunda fase del análisis.
    Se han aplicado los siguientes criterios:
    
    **Documentos excluidos:**
    - Versiones duplicadas (ej. Acuerdo Regional en varios idiomas)
    - Reglas de procedimiento del Acuerdo de Escazú
    - Versiones accesibles de documentos de CEPAL
    - Catálogo de publicaciones de la División de Desarrollo Sostenible y Asentamientos Humanos
    
    **Documentos agregados:**
    - Documentos del Período de Sesiones de CEPAL
    - Documentos del Foro Regional sobre Desarrollo Sostenible
    """)
    
    # Cargar datos
    df = cargar_datos()
    st.info(f"Total de registros en el dataset: {len(df)}")
    
    # Filtrar documentos con tema "CAMBIO CLIMÁTICO"
    df_cambio_climatico = filtrar_cambio_climatico(df)
    st.info(f"Documentos con tema 'CAMBIO CLIMÁTICO': {len(df_cambio_climatico)}")
    
    # Excluir documentos según instrucciones
    df_filtrado = excluir_documentos(df_cambio_climatico)
    st.info(f"Documentos después de aplicar exclusiones: {len(df_filtrado)}")
    
    # Agregar documentos adicionales
    df_final = agregar_documentos(df_filtrado)
    st.success(f"Listado final para segunda fase: {len(df_final)} documentos")
    
    # Mostrar tabla con resultados
    columnas_mostrar = [
        "dc.title",
        "dc.year",
        "division",
        "cepal.topicSpa",
        "dc.identifier.uri"
    ]
    
    # Filtrar columnas que existen en el DataFrame
    columnas_existentes = [col for col in columnas_mostrar if col in df_final.columns]
    
    st.dataframe(
        df_final[columnas_existentes],
        use_container_width=True,
        hide_index=True
    )
    
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