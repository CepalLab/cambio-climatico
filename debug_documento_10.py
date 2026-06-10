#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Debug del documento 10 que está en dataset completo pero no se agrega
"""

from __future__ import annotations

import pandas as pd
from pathlib import Path

from datos import cargar_datos, filtrar_cambio_climatico, filtrar_solo_sustantivas, filtrar_excluir_boletines
from segunda_fase import excluir_documentos, buscar_documento_inteligente

DIR = Path(__file__).resolve().parent
COLUMNA_URI = "dc.identifier.uri"

def main():
    print("=" * 100)
    print("DEBUG: DOCUMENTO 10 - 'Una década de acción para un cambio de época'")
    print("=" * 100)
    
    # Datos del documento
    handle = "https://hdl.handle.net/11362/47745"
    titulo = "Una década de acción para un cambio de época"
    anio = 2022
    
    doc = {
        "titulo": titulo,
        "anio": anio,
        "handle": handle
    }
    
    print(f"\nBuscando documento:")
    print(f"  Handle: {handle}")
    print(f"  Titulo: {titulo}")
    print(f"  Anio: {anio}")
    
    # Cargar datos
    df = cargar_datos()
    df_cambio = filtrar_cambio_climatico(df)
    df_sustantivos = filtrar_solo_sustantivas(df_cambio)
    df_base = filtrar_excluir_boletines(df_sustantivos)
    df_filtrado = excluir_documentos(df_base)
    
    print(f"\n--- En base de 230 ---")
    en_base = df_filtrado[df_filtrado[COLUMNA_URI] == handle]
    print(f"  ¿En base? {len(en_base) > 0}")
    
    print(f"\n--- Buscando en dataset completo ---")
    df_completo = cargar_datos()
    en_completo = df_completo[df_completo[COLUMNA_URI] == handle]
    
    if len(en_completo) > 0:
        fila = en_completo.iloc[0]
        print(f"  Encontrado en dataset completo: SI")
        print(f"  Titulo real: {fila.get('dc.title', '?')}")
        print(f"  Año: {fila.get('dc.year', '?')}")
    else:
        print(f"  Encontrado en dataset completo: NO")
    
    print(f"\n--- Buscando con búsqueda inteligente en base ---")
    resultado = buscar_documento_inteligente(df_filtrado, doc)
    
    if resultado is not None:
        print(f"  Encontrado por búsqueda inteligente: SI")
        print(f"  Handle encontrado: {resultado.get(COLUMNA_URI, '?')}")
        print(f"  Titulo encontrado: {resultado.get('dc.title', '?')[:60]}")
        
        # Este es el problema: si buscar_documento_inteligente lo encuentra,
        # no se va a agregar como nuevo porque ya "existe"
    else:
        print(f"  Encontrado por búsqueda inteligente: NO")

if __name__ == "__main__":
    main()
