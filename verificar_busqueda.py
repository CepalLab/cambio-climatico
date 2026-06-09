#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from pathlib import Path

# Ruta al archivo de datos
DIR = Path(__file__).resolve().parent
ARCHIVO_DATOS = DIR / "datos_dashboard_final.xlsx"

# Los dos documentos que faltaban
DOCUMENTOS_BUSCAR = [
    {
        "titulo": "Una década de acción para un cambio de época",
        "anio": 2022,
        "handle": "https://hdl.handle.net/11362/47745"
    },
    {
        "titulo": "INFORME ANUAL DE PROGRESO: Construir un futuro mejor: acciones para fortalecer la Agenda 2030 para el Desarrollo Sostenible",
        "anio": 2021,
        "handle": "https://foroalc2030.cepal.org/2021/es/documentos/informe-anual-progreso-construir-un-futuro-mejor-acciones-fortalecer-la-agenda-2030"
    }
]

def buscar_documento_inteligente(df, doc):
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

def main():
    print("Verificando búsqueda mejorada de documentos...")
    
    # Leer el archivo Excel
    df = pd.read_excel(ARCHIVO_DATOS)
    print(f"Total de registros en el dataset: {len(df)}\n")
    
    for doc in DOCUMENTOS_BUSCAR:
        print(f"Buscando: {doc['titulo']} ({doc['anio']})")
        print(f"Handle: {doc['handle']}\n")
        
        resultado = buscar_documento_inteligente(df, doc)
        
        if resultado is not None:
            print(f"✓ ENCONTRADO")
            print(f"  Título en dataset: {resultado.get('dc.title', 'N/A')}")
            print(f"  Año: {resultado.get('dc.year', 'N/A')}")
            print(f"  URI: {resultado.get('dc.identifier.uri', 'N/A')}")
        else:
            print(f"✗ NO ENCONTRADO (será creado como documento adicional)")
        
        print("-" * 80 + "\n")

if __name__ == "__main__":
    main()