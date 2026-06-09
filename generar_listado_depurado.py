#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from pathlib import Path
import json

# Ruta al archivo de datos
DIR = Path(__file__).resolve().parent
ARCHIVO_DATOS = DIR / "datos_dashboard_final.xlsx"
ARCHIVO_SELECCION = DIR / "seleccion_revision.json"

# Lista de documentos adicionales que deben incluirse según las instrucciones
DOCUMENTOS_ADICIONALES = [
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

def cargar_seleccion():
    """Carga las selecciones de la revisión de expertos"""
    if ARCHIVO_SELECCION.exists():
        with open(ARCHIVO_SELECCION, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def filtrar_cambio_climatico(df):
    """Filtra documentos que contienen 'CAMBIO CLIMÁTICO' en cepal.topicSpa"""
    if "cepal.topicSpa" not in df.columns:
        return df.iloc[0:0]
    
    # Función para verificar si contiene el tema
    def contiene_cambio_climatico(temas_str):
        if pd.isna(temas_str):
            return False
        # Convertir a string si no lo es
        if not isinstance(temas_str, str):
            temas_str = str(temas_str)
        # Buscar el tema en la cadena
        return "CAMBIO CLIMÁTICO" in temas_str.upper()
    
    return df[df["cepal.topicSpa"].apply(contiene_cambio_climatico)]

def buscar_documento_por_titulo(df, titulo):
    """Busca un documento por su título"""
    # Buscar por título (parcial)
    titulo_normalizado = titulo.lower()
    mask = df['dc.title'].str.contains(titulo_normalizado[:30], case=False, na=False)
    resultados = df[mask]
    return resultados

def generar_listado_depurado():
    """Genera el listado depurado de publicaciones"""
    print("Generando listado depurado de publicaciones...")
    
    # Leer el archivo Excel
    df = pd.read_excel(ARCHIVO_DATOS)
    print(f"Total de registros en el dataset: {len(df)}")
    
    # Cargar selecciones de expertos
    seleccion = cargar_seleccion()
    print(f"Registros seleccionados por expertos: {len([k for k, v in seleccion.items() if v.get('incluir', False)])}")
    
    # Filtrar documentos con tema "CAMBIO CLIMÁTICO"
    df_cambio_climatico = filtrar_cambio_climatico(df)
    print(f"Documentos con tema 'CAMBIO CLIMÁTICO': {len(df_cambio_climatico)}")
    
    # Crear DataFrame con documentos seleccionados por expertos
    handles_seleccionados = [k for k, v in seleccion.items() if v.get('incluir', False)]
    df_seleccionados = df[df['dc.identifier.uri'].isin(handles_seleccionados)]
    print(f"Documentos seleccionados por expertos (filtrados): {len(df_seleccionados)}")
    
    # Buscar documentos adicionales que deben incluirse
    documentos_adicionales_encontrados = []
    for doc in DOCUMENTOS_ADICIONALES:
        resultados = buscar_documento_por_titulo(df, doc["titulo"])
        if not resultados.empty:
            documentos_adicionales_encontrados.append({
                "documento": doc,
                "encontrado": True,
                "registros": resultados.iloc[0].to_dict()  # Primer registro encontrado
            })
        else:
            documentos_adicionales_encontrados.append({
                "documento": doc,
                "encontrado": False,
                "registros": None
            })
    
    print(f"\nDocumentos adicionales encontrados en el dataset:")
    for doc in documentos_adicionales_encontrados:
        estado = "ENCONTRADO" if doc["encontrado"] else "NO ENCONTRADO"
        print(f"- {doc['documento']['titulo']} ({doc['documento']['anio']}): {estado}")
    
    # Crear listado final combinando seleccionados y adicionales
    handles_adicionales = []
    for doc in documentos_adicionales_encontrados:
        if doc["encontrado"]:
            handle = doc["registros"]["dc.identifier.uri"]
            if handle and handle not in handles_adicionales:
                handles_adicionales.append(handle)
    
    # Combinar documentos seleccionados por expertos y documentos adicionales
    handles_finales = list(set(handles_seleccionados + handles_adicionales))
    df_final = df[df['dc.identifier.uri'].isin(handles_finales)]
    
    print(f"\nListado depurado final:")
    print(f"- Documentos seleccionados por expertos: {len(handles_seleccionados)}")
    print(f"- Documentos adicionales encontrados: {len(handles_adicionales)}")
    print(f"- Total de documentos en listado final: {len(df_final)}")
    
    # Guardar el listado depurado
    archivo_salida = DIR / "listado_depurado.csv"
    df_final.to_csv(archivo_salida, index=False, encoding='utf-8')
    print(f"\nListado depurado guardado en: {archivo_salida}")
    
    # Mostrar algunos títulos del listado final
    print("\nAlgunos títulos del listado depurado:")
    for idx, row in df_final.head(10).iterrows():
        print(f"- {row['dc.title']}")
    
    return df_final

if __name__ == "__main__":
    df_final = generar_listado_depurado()