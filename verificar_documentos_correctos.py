#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verifica los documentos con los handles correctos
"""

from __future__ import annotations

import pandas as pd
from pathlib import Path

DIR = Path(__file__).resolve().parent
ARCHIVO = DIR / "datos_dashboard_final.xlsx"
COLUMNA_URI = "dc.identifier.uri"

# Handles correctos proporcionados por el usuario
HANDLES_CORRECTOS = [
    "https://hdl.handle.net/11362/46227",
    "https://hdl.handle.net/11362/43442",
]

def main():
    print("=" * 100)
    print("VERIFICACION: DOCUMENTOS CON HANDLES CORRECTOS")
    print("=" * 100)
    
    df = pd.read_excel(ARCHIVO)
    print(f"\nDataset cargado: {len(df)} registros\n")
    
    for i, handle in enumerate(HANDLES_CORRECTOS, 1):
        print(f"\n{i}. Buscando handle: {handle}")
        print("-" * 100)
        
        registro = df[df[COLUMNA_URI] == handle]
        
        if len(registro) > 0:
            fila = registro.iloc[0]
            print(f"   ENCONTRADO")
            print(f"   Titulo: {fila.get('dc.title', '?')}")
            print(f"   Anio: {fila.get('dc.year', '?')}")
            print(f"   Division: {fila.get('division', '?')}")
            print(f"   Topics: {str(fila.get('cepal.topicSpa', '?'))[:100]}")
            print(f"   Handle: {fila.get(COLUMNA_URI, '?')}")
        else:
            print(f"   NO ENCONTRADO")
    
    print("\n" + "=" * 100)
    print("Documentos a usar en DOCUMENTOS_A_AGREGAR:")
    print("=" * 100)
    
    for i, handle in enumerate(HANDLES_CORRECTOS, 1):
        registro = df[df[COLUMNA_URI] == handle]
        if len(registro) > 0:
            fila = registro.iloc[0]
            titulo = fila.get('dc.title', '?')
            anio = fila.get('dc.year', '?')
            
            print(f"\n[{i}]")
            print(f'    "titulo": "{titulo}",')
            print(f'    "anio": {anio},')
            print(f'    "handle": "{handle}"')

if __name__ == "__main__":
    main()
