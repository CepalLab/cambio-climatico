#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from pathlib import Path

# Ruta al archivo de datos
DIR = Path(__file__).resolve().parent
ARCHIVO_DATOS = DIR / "datos_dashboard_final.xlsx"

def contiene_tema(temas_str, tema_buscado):
    """Verifica si un tema está en la cadena de temas"""
    if pd.isna(temas_str):
        return False
    if not isinstance(temas_str, str):
        temas_str = str(temas_str)
    return tema_buscado.upper() in temas_str.upper()

def main():
    print("=" * 80)
    print("DOCUMENTOS EXCLUIDOS PARA SEGUNDA FASE")
    print("=" * 80)
    
    # Leer los datos
    df = pd.read_excel(ARCHIVO_DATOS)
    
    # Base: Documentos sustantivos con tema "CAMBIO CLIMÁTICO", sin boletines
    df_cambio = df[df["cepal.topicSpa"].apply(lambda v: contiene_tema(v, "CAMBIO CLIMÁTICO"))]
    df_sustantivos = df_cambio[pd.to_numeric(df_cambio["Sustantivo"], errors="coerce") == 1]
    
    if "tipo_gr" in df_sustantivos.columns and "tipo_doc" in df_sustantivos.columns:
        es_grupo_byr = df_sustantivos["tipo_gr"].astype(str).eq("Boletines y Revistas")
        es_boletin = df_sustantivos["tipo_doc"].astype(str).eq("Boletines")
        df_base = df_sustantivos[~(es_grupo_byr & es_boletin)]
    
    print(f"\nBase (sustantivos sin boletines): {len(df_base)} documentos\n")
    
    # Excluir Acuerdo Regional
    print("1. ACUERDO REGIONAL (versiones duplicadas):")
    df_temp = df_base.copy()
    acuerdo_regional = df_base[df_base["dc.title"].str.contains("Acuerdo Regional", case=False, na=False)]
    print(f"   Encontrados: {len(acuerdo_regional)}")
    for idx, row in acuerdo_regional.iterrows():
        print(f"   - {row['dc.title']}")
    df_base = df_base[~df_base["dc.title"].str.contains("Acuerdo Regional", case=False, na=False)]
    print()
    
    # Excluir versiones accesibles
    print("2. VERSIONES ACCESIBLES:")
    accesibles = df_base[df_base["dc.title"].str.contains("accesible", case=False, na=False)]
    print(f"   Encontrados: {len(accesibles)}")
    for idx, row in accesibles.iterrows():
        print(f"   - {row['dc.title']}")
    df_base = df_base[~df_base["dc.title"].str.contains("accesible", case=False, na=False)]
    print()
    
    # Excluir revistas de CEPAL
    print("3. REVISTAS DE CEPAL (Boletines y Revistas):")
    if "tipo_gr" in df_base.columns:
        revistas = df_base[df_base["tipo_gr"].astype(str).eq("Boletines y Revistas")]
        print(f"   Encontrados: {len(revistas)}")
        for idx, row in revistas.iterrows():
            print(f"   - {row['dc.title']}")
        df_base = df_base[~df_base["tipo_gr"].astype(str).eq("Boletines y Revistas")]
    print()
    
    # Excluir catálogo de publicaciones
    print("4. CATÁLOGO DE PUBLICACIONES:")
    catalogo = df_base[df_base["dc.title"].str.contains("Catálogo de publicaciones", case=False, na=False)]
    print(f"   Encontrados: {len(catalogo)}")
    for idx, row in catalogo.iterrows():
        print(f"   - {row['dc.title']}")
    df_base = df_base[~df_base["dc.title"].str.contains("Catálogo de publicaciones", case=False, na=False)]
    print()
    
    # Excluir Escazú
    print("5. REGLAS DE PROCEDIMIENTO DEL ACUERDO DE ESCAZÚ:")
    escazu = df_base[df_base["dc.title"].str.contains("Reglas de procedimiento del Acuerdo de Escazú", case=False, na=False)]
    print(f"   Encontrados: {len(escazu)}")
    for idx, row in escazu.iterrows():
        print(f"   - {row['dc.title']}")
    df_base = df_base[~df_base["dc.title"].str.contains("Reglas de procedimiento del Acuerdo de Escazú", case=False, na=False)]
    print()
    
    # Excluir The Hummingbird
    print("6. THE HUMMINGBIRD:")
    hummingbird = df_base[df_base["dc.title"].str.contains("The Hummingbird", case=False, na=False)]
    print(f"   Encontrados: {len(hummingbird)}")
    for idx, row in hummingbird.iterrows():
        print(f"   - {row['dc.title']}")
    df_base = df_base[~df_base["dc.title"].str.contains("The Hummingbird", case=False, na=False)]
    print()
    
    print("=" * 80)
    print("RESUMEN TOTAL DE EXCLUIDOS:")
    print("=" * 80)
    total_excluidos = len(acuerdo_regional) + len(accesibles) + len(revistas) + len(catalogo) + len(escazu) + len(hummingbird)
    print(f"Acuerdo Regional: {len(acuerdo_regional)}")
    print(f"Versiones accesibles: {len(accesibles)}")
    print(f"Revistas de CEPAL: {len(revistas)}")
    print(f"Catálogo de publicaciones: {len(catalogo)}")
    print(f"Escazú (reglas): {len(escazu)}")
    print(f"The Hummingbird: {len(hummingbird)}")
    print("-" * 80)
    print(f"TOTAL EXCLUIDOS: {total_excluidos}")
    print("=" * 80)

if __name__ == "__main__":
    main()