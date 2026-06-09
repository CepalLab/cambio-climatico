#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from pathlib import Path

# Ruta al archivo de datos
DIR = Path(__file__).resolve().parent
ARCHIVO_DATOS = DIR / "datos_dashboard_final.xlsx"

def filtrar_cambio_climatico(df):
    """Filtra documentos que contienen 'CAMBIO CLIMÁTICO' en cepal.topicSpa"""
    if "cepal.topicSpa" not in df.columns:
        return df.iloc[0:0]
    
    def contiene_cambio_climatico(temas_str):
        if pd.isna(temas_str):
            return False
        if not isinstance(temas_str, str):
            temas_str = str(temas_str)
        return "CAMBIO CLIMÁTICO" in temas_str.upper()
    
    return df[df["cepal.topicSpa"].apply(contiene_cambio_climatico)]

def excluir_documentos(df):
    """Excluye documentos según las instrucciones"""
    documentos_a_excluir = [
        "Acuerdo Regional",
        "Reglas de procedimiento del Acuerdo de Escazú",
        "Catálogo de publicaciones de la División de Desarrollo Sostenible y Asentamientos Humanos",
        "The Hummingbird",
    ]
    
    # Excluir documentos con títulos específicos
    for titulo in documentos_a_excluir:
        df = df[~df["dc.title"].str.contains(titulo, case=False, na=False)]
    
    # Excluir versiones accesibles
    df = df[~df["dc.title"].str.contains("accesible", case=False, na=False)]
    
    # Excluir por división
    df = df[~df["division"].str.contains("Desarrollo Sostenible y Asentamientos Humanos", case=False, na=False)]
    
    # Excluir revistas
    if "tipo_gr" in df.columns:
        es_revista = df["tipo_gr"].astype(str).eq("Boletines y Revistas")
        df = df[~es_revista]
    
    return df

def main():
    print("=" * 80)
    print("RECAP: DOCUMENTOS PARA SEGUNDA FASE")
    print("=" * 80)
    
    # Leer los datos
    df = pd.read_excel(ARCHIVO_DATOS)
    
    # Paso 1: Base inicial - Documentos con tema "CAMBIO CLIMÁTICO"
    df_inicial = filtrar_cambio_climatico(df)
    print(f"\n1. BASE INICIAL (documentos con tema 'CAMBIO CLIMÁTICO'): {len(df_inicial)} documentos")
    
    # Paso 2: Después de aplicar exclusiones
    df_filtrado = excluir_documentos(df_inicial)
    documentos_excluidos = len(df_inicial) - len(df_filtrado)
    print(f"\n2. DESPUÉS DE EXCLUSIONES: {len(df_filtrado)} documentos")
    print(f"   Documentos excluidos: {documentos_excluidos}")
    
    # Detalles de exclusiones
    print(f"\n   Detalles de lo que se excluyó:")
    
    # Excluir Acuerdo Regional
    df_temp = df_inicial.copy()
    df_sin_acuerdo = df_temp[~df_temp["dc.title"].str.contains("Acuerdo Regional", case=False, na=False)]
    print(f"   - Acuerdo Regional (versiones duplicadas): {len(df_temp) - len(df_sin_acuerdo)} documentos")
    
    # Excluir Escazú
    df_temp = df_sin_acuerdo.copy()
    df_sin_escazu = df_temp[~df_temp["dc.title"].str.contains("Reglas de procedimiento del Acuerdo de Escazú", case=False, na=False)]
    print(f"   - Escazú (reglas de procedimiento): {len(df_temp) - len(df_sin_escazu)} documentos")
    
    # Excluir catálogo
    df_temp = df_sin_escazu.copy()
    df_sin_catalogo = df_temp[~df_temp["dc.title"].str.contains("Catálogo de publicaciones de la División de Desarrollo Sostenible", case=False, na=False)]
    print(f"   - Catálogo de publicaciones: {len(df_temp) - len(df_sin_catalogo)} documentos")
    
    # Excluir versiones accesibles
    df_temp = df_sin_catalogo.copy()
    df_sin_accesible = df_temp[~df_temp["dc.title"].str.contains("accesible", case=False, na=False)]
    print(f"   - Versiones accesibles: {len(df_temp) - len(df_sin_accesible)} documentos")
    
    # Excluir revistas
    df_temp = df_sin_accesible.copy()
    if "tipo_gr" in df_temp.columns:
        es_revista = df_temp["tipo_gr"].astype(str).eq("Boletines y Revistas")
        df_sin_revistas = df_temp[~es_revista]
        print(f"   - Revistas de CEPAL: {len(df_temp) - len(df_sin_revistas)} documentos")
    
    # Paso 3: Agregar los 14 documentos
    documentos_a_agregar = 14
    print(f"\n3. DOCUMENTOS A AGREGAR: {documentos_a_agregar} publicaciones")
    print(f"   - Período de Sesiones de CEPAL: 5 documentos")
    print(f"   - Foro Regional sobre Desarrollo Sostenible: 9 documentos")
    
    # Paso 4: Total final
    total_final = len(df_filtrado) + documentos_a_agregar
    print(f"\n4. TOTAL FINAL PARA SEGUNDA FASE: {total_final} documentos")
    print(f"   ({len(df_filtrado)} documentos depurados + {documentos_a_agregar} documentos agregados)")
    
    print("\n" + "=" * 80)
    print("RESUMEN DE CAMBIOS:")
    print("=" * 80)
    print(f"Base inicial:          {len(df_inicial):3d} documentos")
    print(f"Menos exclusiones:     -{documentos_excluidos:2d} documentos")
    print(f"Más documentos nuevos: +{documentos_a_agregar:2d} documentos")
    print(f"{'─' * 40}")
    print(f"TOTAL SEGUNDA FASE:     {total_final:3d} documentos")
    print("=" * 80)

if __name__ == "__main__":
    main()