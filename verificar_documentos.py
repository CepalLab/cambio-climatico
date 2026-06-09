#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from pathlib import Path

# Ruta al archivo de datos
DIR = Path(__file__).resolve().parent
ARCHIVO_DATOS = DIR / "datos_dashboard_final.xlsx"

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

def verificar_documentos():
    """Verifica si todos los documentos adicionales están en el dataset"""
    print("Verificando documentos adicionales...")
    
    # Leer el archivo Excel
    df = pd.read_excel(ARCHIVO_DATOS)
    print(f"Total de registros en el dataset: {len(df)}")
    
    # Verificar cada documento adicional
    documentos_encontrados = 0
    documentos_faltantes = []
    
    for doc in DOCUMENTOS_ADICIONALES:
        # Buscar por título (parcial)
        titulo_normalizado = doc["titulo"].lower()
        mask = df['dc.title'].str.contains(titulo_normalizado[:30], case=False, na=False)
        resultados = df[mask]
        
        if not resultados.empty:
            documentos_encontrados += 1
            print(f"✓ ENCONTRADO: {doc['titulo']} ({doc['anio']})")
        else:
            documentos_faltantes.append(doc)
            print(f"✗ NO ENCONTRADO: {doc['titulo']} ({doc['anio']})")
    
    print(f"\nResumen:")
    print(f"- Documentos encontrados: {documentos_encontrados}")
    print(f"- Documentos faltantes: {len(documentos_faltantes)}")
    
    if documentos_faltantes:
        print(f"\nDocumentos faltantes:")
        for doc in documentos_faltantes:
            print(f"- {doc['titulo']} ({doc['anio']})")
    
    return documentos_encontrados, documentos_faltantes

if __name__ == "__main__":
    verificar_documentos()