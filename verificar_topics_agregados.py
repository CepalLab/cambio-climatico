#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verifica que los documentos agregados tengan los topics correctos del dataset
"""

from __future__ import annotations

import pandas as pd
from pathlib import Path

from datos import cargar_datos, filtrar_cambio_climatico, filtrar_solo_sustantivas, filtrar_excluir_boletines
from segunda_fase import excluir_documentos, agregar_documentos

DIR = Path(__file__).resolve().parent
COLUMNA_URI = "dc.identifier.uri"
COLUMNA_TOPICS = "cepal.topicSpa"

HANDLES_AGREGADOS = [
    "https://hdl.handle.net/11362/46227",
    "https://hdl.handle.net/11362/43442",
]

def main():
    print("=" * 100)
    print("VERIFICACION: TOPICS DE DOCUMENTOS AGREGADOS")
    print("=" * 100)
    
    # Cargar datos completos para verificar
    df_completo = cargar_datos()
    
    # Construir segunda fase
    df = cargar_datos()
    df_cambio = filtrar_cambio_climatico(df)
    df_sustantivos = filtrar_solo_sustantivas(df_cambio)
    df_base = filtrar_excluir_boletines(df_sustantivos)
    df_filtrado = excluir_documentos(df_base)
    df_final = agregar_documentos(df_filtrado)
    
    print(f"\nDataset final: {len(df_final)} documentos\n")
    
    print("=" * 100)
    print("VERIFICACION DE TOPICS EN DOCUMENTOS AGREGADOS")
    print("=" * 100)
    
    for handle in HANDLES_AGREGADOS:
        print(f"\n\nHandle: {handle}")
        print("-" * 100)
        
        # Buscar en dataset final
        registro_final = df_final[df_final[COLUMNA_URI] == handle]
        
        if len(registro_final) == 0:
            print("  NO ENCONTRADO EN RESULTADO FINAL")
            continue
        
        fila_final = registro_final.iloc[0]
        titulo = fila_final.get('dc.title', '?')
        topics_final = fila_final.get(COLUMNA_TOPICS, [])
        
        print(f"\nTitulo: {titulo}")
        print(f"Topics en resultado final:")
        print(f"  {topics_final}")
        
        # Verificar contra dataset completo
        registro_completo = df_completo[df_completo[COLUMNA_URI] == handle]
        
        if len(registro_completo) > 0:
            fila_completo = registro_completo.iloc[0]
            topics_completo = fila_completo.get(COLUMNA_TOPICS, [])
            
            print(f"\nTopics en dataset completo (groundtruth):")
            print(f"  {topics_completo}")
            
            # Comparar
            if topics_final == topics_completo:
                print(f"\n  ✓ CORRECTO: Topics coinciden con groundtruth")
            else:
                print(f"\n  ⚠️  DIFERENCIA:")
                print(f"     Final:     {topics_final}")
                print(f"     Completo:  {topics_completo}")
        else:
            print(f"\n  ⚠️  No encontrado en dataset completo")
    
    print("\n" + "=" * 100)

if __name__ == "__main__":
    main()
