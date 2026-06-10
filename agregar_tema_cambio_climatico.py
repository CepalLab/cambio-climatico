#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Agrega el tema CAMBIO CLIMÁTICO a los dos documentos que el usuario indicó
"""

from __future__ import annotations

import pandas as pd
from pathlib import Path

DIR = Path(__file__).resolve().parent
ARCHIVO = DIR / "datos_dashboard_final.xlsx"
COLUMNA_URI = "dc.identifier.uri"
COLUMNA_TOPICS = "cepal.topicSpa"

HANDLES_A_ACTUALIZAR = {
    "https://hdl.handle.net/11362/46227": "Construir un nuevo futuro...",
    "https://hdl.handle.net/11362/43442": "La ineficiencia de la desigualdad",
}

def main():
    print("=" * 100)
    print("ACTUALIZACION: AGREGAR TEMA 'CAMBIO CLIMATICO'")
    print("=" * 100)
    
    df = pd.read_excel(ARCHIVO)
    print(f"\nDataset cargado: {len(df)} registros\n")
    
    for handle, titulo_referencia in HANDLES_A_ACTUALIZAR.items():
        print(f"\nProcesando: {titulo_referencia}")
        print(f"Handle: {handle}")
        print("-" * 100)
        
        # Buscar el registro
        mask = df[COLUMNA_URI] == handle
        if not mask.any():
            print(f"  ERROR: No encontrado")
            continue
        
        idx = df[mask].index[0]
        fila = df.loc[idx]
        
        titulo = fila.get('dc.title', '?')
        topics_actual = fila.get(COLUMNA_TOPICS, [])
        
        print(f"  Titulo: {titulo}")
        print(f"  Topics actuales: {topics_actual}")
        
        # Convertir a lista si es string
        if isinstance(topics_actual, str):
            # Parsear formato lista [...]
            import ast
            try:
                topics_list = ast.literal_eval(topics_actual)
            except:
                topics_list = [topics_actual]
        elif isinstance(topics_actual, list):
            topics_list = topics_actual
        else:
            topics_list = []
        
        # Agregar CAMBIO CLIMATICO si no está
        if "CAMBIO CLIMÁTICO" not in topics_list:
            topics_list.append("CAMBIO CLIMÁTICO")
            # Ordenar alfabéticamente
            topics_list = sorted(topics_list)
            
            # Actualizar el DataFrame
            df.loc[idx, COLUMNA_TOPICS] = topics_list
            
            print(f"  Topics nuevos: {topics_list}")
            print(f"  ACTUALIZADO ✓")
        else:
            print(f"  Ya contiene CAMBIO CLIMATICO")
    
    # Guardar
    print("\n" + "=" * 100)
    print("GUARDANDO CAMBIOS")
    print("=" * 100)
    
    df.to_excel(ARCHIVO, index=False)
    print(f"\nArchivo guardado: {ARCHIVO.name}")
    print(f"Total registros: {len(df)}")

if __name__ == "__main__":
    main()
