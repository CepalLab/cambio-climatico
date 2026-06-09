#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Analiza cuáles documentos están en la base y cuáles se agregarán realmente
"""

from __future__ import annotations

import pandas as pd
from pathlib import Path

from datos import cargar_datos, filtrar_cambio_climatico, filtrar_solo_sustantivas, filtrar_excluir_boletines
from segunda_fase import DOCUMENTOS_A_AGREGAR, buscar_documento_inteligente

DIR = Path(__file__).resolve().parent
COLUMNA_URI = "dc.identifier.uri"

def main():
    print("=" * 100)
    print("ANÁLISIS: DOCUMENTOS A AGREGAR vs BASE")
    print("=" * 100)
    
    # Cargar base
    df = cargar_datos()
    df_cambio = filtrar_cambio_climatico(df)
    df_sustantivos = filtrar_solo_sustantivas(df_cambio)
    df_base = filtrar_excluir_boletines(df_sustantivos)
    
    print(f"\nBase de 239 sustantivos cargada: {len(df_base)} registros")
    
    handles_en_base = set(df_base[COLUMNA_URI].dropna().astype(str))
    print(f"Handles únicos en base: {len(handles_en_base)}\n")
    
    print("=" * 100)
    print(f"ANÁLISIS DE {len(DOCUMENTOS_A_AGREGAR)} DOCUMENTOS A AGREGAR")
    print("=" * 100)
    
    en_base = []
    no_en_base = []
    
    for i, doc in enumerate(DOCUMENTOS_A_AGREGAR, 1):
        titulo = doc.get("titulo", "?")
        anio = doc.get("anio", "?")
        handle = doc.get("handle", "")
        
        # Chequear si el handle está en la base
        if handle in handles_en_base:
            print(f"\n[{i:2d}] [EN BASE]")
            print(f"      Titulo: {titulo[:70]}")
            print(f"      Anio: {anio}")
            print(f"      Handle: {handle[:50]}")
            en_base.append((titulo, anio, handle))
            continue
        
        # Intentar buscar con búsqueda inteligente
        resultado = buscar_documento_inteligente(df_base, doc)
        
        if resultado is not None:
            print(f"\n[{i:2d}] [ENCONTRADO POR BUSQUEDA]")
            print(f"      Titulo original: {titulo[:70]}")
            print(f"      Titulo encontrado: {resultado.get('dc.title', '?')[:70]}")
            print(f"      Anio: {anio}")
            print(f"      Handle original: {handle[:50]}")
            print(f"      Handle encontrado: {resultado.get(COLUMNA_URI, '?')[:50]}")
            en_base.append((titulo, anio, handle))
        else:
            print(f"\n[{i:2d}] [NO ENCONTRADO - SE AGREGARA]")
            print(f"      Titulo: {titulo[:70]}")
            print(f"      Anio: {anio}")
            print(f"      Handle: {handle[:50]}")
            no_en_base.append((titulo, anio, handle))
    
    print("\n" + "=" * 100)
    print("RESUMEN")
    print("=" * 100)
    print(f"\nDocumentos YA EN BASE: {len(en_base)}")
    print(f"Documentos a AGREGAR: {len(no_en_base)}")
    print(f"{'_' * 50}")
    print(f"Total esperado: 239 - 9 + {len(no_en_base)} = {239 - 9 + len(no_en_base)}")
    
    if len(no_en_base) > 0:
        print(f"\nDocumentos que se AGREGARÁN:")
        for i, (titulo, anio, handle) in enumerate(no_en_base, 1):
            print(f"  {i}. {titulo[:60]}")
            print(f"     Anio: {anio}")
            print(f"     Handle: {handle[:50]}")

if __name__ == "__main__":
    main()
