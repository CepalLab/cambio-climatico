#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Investiga los handles duplicados que aparecen en el resultado final
"""

from __future__ import annotations

import pandas as pd
from pathlib import Path
from collections import Counter

from datos import (
    cargar_datos,
    filtrar_cambio_climatico,
    filtrar_solo_sustantivas,
    filtrar_excluir_boletines,
)
from segunda_fase import excluir_documentos, agregar_documentos

DIR = Path(__file__).resolve().parent
COLUMNA_URI = "dc.identifier.uri"

def main():
    print("=" * 80)
    print("INVESTIGACIÓN: DUPLICADOS EN SEGUNDA FASE")
    print("=" * 80)
    
    # Cargar y filtrar a base de 239
    df = cargar_datos()
    df_cambio = filtrar_cambio_climatico(df)
    df_sustantivos = filtrar_solo_sustantivas(df_cambio)
    df_base = filtrar_excluir_boletines(df_sustantivos)
    
    print(f"\nBase inicial: {len(df_base)} documentos")
    
    # Obtener handles de base
    handles_base = set(df_base[COLUMNA_URI].dropna().astype(str))
    print(f"Handles únicos en base: {len(handles_base)}")
    
    # Aplicar exclusiones
    df_filtrado = excluir_documentos(df_base)
    print(f"Después exclusiones: {len(df_filtrado)} documentos")
    
    # Obtener handles después de exclusiones
    handles_filtrados = set(df_filtrado[COLUMNA_URI].dropna().astype(str))
    print(f"Handles únicos después exclusiones: {len(handles_filtrados)}")
    
    # Agregar documentos
    df_final = agregar_documentos(df_filtrado)
    print(f"Después agregaciones: {len(df_final)} documentos")
    
    # Buscar duplicados
    handles_final = df_final[COLUMNA_URI].dropna().astype(str)
    contador = Counter(handles_final)
    duplicados = {h: c for h, c in contador.items() if c > 1}
    
    print(f"\nHandles únicos en final: {len(set(handles_final))}")
    print(f"Duplicados encontrados: {len(duplicados)}")
    
    if duplicados:
        print("\n" + "=" * 80)
        print("DETALLES DE DUPLICADOS")
        print("=" * 80)
        
        for handle, count in sorted(duplicados.items(), key=lambda x: -x[1]):
            print(f"\nHandle: {handle}")
            print(f"Apariciones: {count}")
            
            # Buscar en datos originales
            registros = df_final[df_final[COLUMNA_URI] == handle]
            
            for i, (idx, row) in enumerate(registros.iterrows(), 1):
                print(f"\n  [{i}] {row['dc.title'][:70]}")
                print(f"      Año: {row['dc.year']}")
                print(f"      División: {row['division']}")
                print(f"      Topics: {str(row['cepal.topicSpa'])[:80]}")
                
                # Chequear si estaba en base original
                estaba_en_base = handle in handles_base
                print(f"      ¿Estaba en base? {'SÍ' if estaba_en_base else 'NO (agregado)'}")
    
    print("\n" + "=" * 80)
    print("ANÁLISIS")
    print("=" * 80)
    
    # Analizar qué está pasando
    print("\nCriterios para agregar (de segunda_fase.py):")
    from segunda_fase import DOCUMENTOS_A_AGREGAR
    
    print(f"\nDocumentos a agregar (definición): {len(DOCUMENTOS_A_AGREGAR)}")
    for i, doc in enumerate(DOCUMENTOS_A_AGREGAR, 1):
        titulo = doc.get('titulo', '?')
        handle = doc.get('handle', '?')
        print(f"  [{i:2d}] {titulo[:50]} -> {handle}")
        
        # Chequear si este handle ya está en la base
        if handle in handles_base:
            matching_rows = df_base[df_base[COLUMNA_URI] == handle]
            if len(matching_rows) > 0:
                print(f"        ⚠️  YA ESTÁ EN BASE: {matching_rows.iloc[0]['dc.title'][:50]}")

if __name__ == "__main__":
    main()
