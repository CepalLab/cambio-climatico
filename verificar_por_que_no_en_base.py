#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verifica por qué los documentos no están en la base de 239 sustantivos
"""

from __future__ import annotations

import pandas as pd
from pathlib import Path

DIR = Path(__file__).resolve().parent
ARCHIVO = DIR / "datos_dashboard_final.xlsx"
COLUMNA_URI = "dc.identifier.uri"

HANDLES_A_VERIFICAR = [
    "https://hdl.handle.net/11362/46227",  # Construir un nuevo futuro...
    "https://hdl.handle.net/11362/43442",  # La ineficiencia de la desigualdad
]

def main():
    print("=" * 100)
    print("VERIFICACION: POR QUE NO ESTAN EN BASE DE 239 SUSTANTIVOS")
    print("=" * 100)
    
    df = pd.read_excel(ARCHIVO)
    
    for handle in HANDLES_A_VERIFICAR:
        print(f"\nHandle: {handle}")
        print("-" * 100)
        
        registro = df[df[COLUMNA_URI] == handle]
        
        if len(registro) == 0:
            print("  NO ENCONTRADO en dataset completo")
            continue
        
        fila = registro.iloc[0]
        titulo = fila.get('dc.title', '?')
        anio = fila.get('dc.year', '?')
        
        print(f"  Titulo: {titulo}")
        print(f"  Anio: {anio}")
        
        # Chequear atributos sustantivos
        es_sustantivo = pd.to_numeric(fila.get('Sustantivo', 0), errors='coerce')
        print(f"  Sustantivo: {es_sustantivo}")
        
        if 'cepal.topicSpa' in df.columns:
            topics = fila.get('cepal.topicSpa', '?')
            contiene_cambio_climatico = 'CAMBIO CLIMÁTICO' in str(topics).upper()
            print(f"  Contiene 'CAMBIO CLIMATICO': {contiene_cambio_climatico}")
            print(f"  Topics: {str(topics)[:100]}")
        
        # Chequear tipo_gr y tipo_doc
        tipo_gr = fila.get('tipo_gr', '?')
        tipo_doc = fila.get('tipo_doc', '?')
        print(f"  tipo_gr: {tipo_gr}")
        print(f"  tipo_doc: {tipo_doc}")
        
        # Resumen
        print("\n  RAZONES POR LAS QUE NO ESTA EN BASE DE 239:")
        razones = []
        
        if pd.to_numeric(es_sustantivo, errors='coerce') != 1:
            razones.append(f"- Sustantivo={es_sustantivo} (debe ser 1)")
        
        if 'CAMBIO CLIMÁTICO' not in str(topics).upper():
            razones.append("- No contiene tema 'CAMBIO CLIMATICO'")
        
        if tipo_gr == "Boletines y Revistas" and tipo_doc == "Boletines":
            razones.append("- Es boletin (tipo_gr='Boletines y Revistas' AND tipo_doc='Boletines')")
        
        if not razones:
            razones.append("DESCONOCIDA - revisar manualmente")
        
        for r in razones:
            print(f"    {r}")

if __name__ == "__main__":
    main()
