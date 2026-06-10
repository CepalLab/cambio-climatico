#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Debug: verificar por qué los documentos sin handle exacto no se crean
"""

from __future__ import annotations

import pandas as pd
from pathlib import Path

from datos import cargar_datos, filtrar_cambio_climatico, filtrar_solo_sustantivas, filtrar_excluir_boletines
from segunda_fase import DOCUMENTOS_A_AGREGAR, excluir_documentos, buscar_documento_inteligente

DIR = Path(__file__).resolve().parent
COLUMNA_URI = "dc.identifier.uri"

def main():
    print("=" * 100)
    print("DEBUG: DOCUMENTOS NO ENCONTRADOS - POR QUE NO SE CREAN")
    print("=" * 100)
    
    # Base
    df = cargar_datos()
    df_cambio = filtrar_cambio_climatico(df)
    df_sustantivos = filtrar_solo_sustantivas(df_cambio)
    df_base = filtrar_excluir_boletines(df_sustantivos)
    df_filtrado = excluir_documentos(df_base)
    
    handles_en_base = set(df_filtrado[COLUMNA_URI].dropna().astype(str))
    df_completo = cargar_datos()
    
    # Revisar documentos NO ENCONTRADOS
    documentos_no_encontrados = [
        DOCUMENTOS_A_AGREGAR[0],  # Doc 1
        DOCUMENTOS_A_AGREGAR[1],  # Doc 2
        DOCUMENTOS_A_AGREGAR[4],  # Doc 5
    ]
    
    print(f"\nRevisando documentos NO ENCONTRADOS:\n")
    
    for i, doc in enumerate(documentos_no_encontrados, 1):
        handle = doc.get("handle", "")
        titulo = doc.get("titulo", "?")[:50]
        anio = doc.get("anio", "?")
        
        print(f"Doc {i}: {titulo}")
        print(f"  Handle: {handle[:70]}")
        
        # Paso 1: ¿En base?
        en_base = handle in handles_en_base
        print(f"  1. ¿En base? {en_base}")
        
        # Paso 2: ¿En dataset completo?
        en_completo = len(df_completo[df_completo[COLUMNA_URI] == handle]) > 0
        print(f"  2. ¿En dataset completo? {en_completo}")
        
        # Paso 3: ¿Búsqueda inteligente encuentra algo?
        resultado = buscar_documento_inteligente(df_filtrado, doc)
        si_busqueda = resultado is not None
        print(f"  3. ¿Búsqueda inteligente encuentra algo? {si_busqueda}")
        
        if si_busqueda:
            uri_resultado = resultado.get(COLUMNA_URI, "")
            print(f"     -> Encontró: {resultado.get('dc.title', '?')[:40]}")
            print(f"     -> Handle: {uri_resultado[:50]}")
        
        # Conclusión
        print(f"  => Debería CREARSE COMO ENTRADA BASICA")
        print()

if __name__ == "__main__":
    main()
