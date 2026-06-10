#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Investiga por qué solo 2 de 14 documentos se agregaron en lugar de todos 14
"""

from __future__ import annotations

import pandas as pd
from pathlib import Path

from datos import cargar_datos, filtrar_cambio_climatico, filtrar_solo_sustantivas, filtrar_excluir_boletines
from segunda_fase import DOCUMENTOS_A_AGREGAR, excluir_documentos

DIR = Path(__file__).resolve().parent
COLUMNA_URI = "dc.identifier.uri"

def main():
    print("=" * 100)
    print("INVESTIGACION: POR QUE SOLO 2 DE 14 DOCUMENTOS SE AGREGARON")
    print("=" * 100)
    
    # Cargar base de 239
    df = cargar_datos()
    df_cambio = filtrar_cambio_climatico(df)
    df_sustantivos = filtrar_solo_sustantivas(df_cambio)
    df_base = filtrar_excluir_boletines(df_sustantivos)
    df_filtrado = excluir_documentos(df_base)
    
    print(f"\nBase después de exclusiones: {len(df_filtrado)} documentos")
    
    handles_en_base = set(df_filtrado[COLUMNA_URI].dropna().astype(str))
    print(f"Handles en base: {len(handles_en_base)}")
    
    # Cargar dataset completo
    df_completo = cargar_datos()
    
    print(f"\n{'=' * 100}")
    print(f"ANALISIS DE {len(DOCUMENTOS_A_AGREGAR)} DOCUMENTOS A AGREGAR")
    print(f"{'=' * 100}\n")
    
    en_base = 0
    no_en_base = 0
    en_completo = 0
    
    for i, doc in enumerate(DOCUMENTOS_A_AGREGAR, 1):
        handle = doc.get("handle", "")
        titulo = doc.get("titulo", "?")[:60]
        
        # Caso 1: Handle exacto en base
        if handle in handles_en_base:
            print(f"[{i:2d}] HANDLE EXACTO EN BASE: {titulo}")
            print(f"      Handle: {handle[:50]}")
            en_base += 1
            continue
        
        # Caso 2: En dataset completo
        registro_completo = df_completo[df_completo[COLUMNA_URI] == handle]
        if len(registro_completo) > 0:
            print(f"[{i:2d}] EN DATASET COMPLETO (pero NO en base): {titulo}")
            print(f"      Handle: {handle[:50]}")
            en_completo += 1
            continue
        
        # Caso 3: No está en ningún lado
        print(f"[{i:2d}] NO ENCONTRADO: {titulo}")
        print(f"      Handle: {handle[:50]}")
        no_en_base += 1
    
    print(f"\n{'=' * 100}")
    print(f"RESUMEN")
    print(f"{'=' * 100}")
    print(f"\nDocumentos por tipo:")
    print(f"  1. Handle exacto en base (230): {en_base}")
    print(f"  2. En dataset completo pero NO en base: {en_completo}")
    print(f"  3. No encontrados (se crean nuevos): {no_en_base}")
    print(f"  Total: {en_base + en_completo + no_en_base}")
    
    print(f"\nCalculo final:")
    print(f"  Base después exclusiones: 230")
    print(f"  + Documentos a agregar: {en_base + en_completo + no_en_base}")
    print(f"  = Total esperado: {230 + (en_base + en_completo + no_en_base)}")
    
    print(f"\nPero el resultado real es:")
    print(f"  - Si solo se agregan los NO en base: 230 + {en_completo + no_en_base} = {230 + en_completo + no_en_base}")
    print(f"  - Esto explica por qué tenemos 232 en lugar de 244")
    
    print(f"\nPROBLEMA: Los {en_base} documentos que ya están en base no se vuelven a agregar")
    print(f"SOLUCION: Se deben agregar los 14 TODOS, ignorando si algunos ya están en base")

if __name__ == "__main__":
    main()
