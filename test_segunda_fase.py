#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from pathlib import Path
from segunda_fase import excluir_documentos, agregar_documentos

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
    print("TEST: VISTA 'DOCUMENTOS PARA 2DA FASE'")
    print("=" * 80)
    
    # Leer los datos
    df = pd.read_excel(ARCHIVO_DATOS)
    print(f"\nDataset total: {len(df)} registros")
    
    # Paso 1: Base de 239 sustantivos
    df_cambio = df[df["cepal.topicSpa"].apply(lambda v: contiene_tema(v, "CAMBIO CLIMÁTICO"))]
    df_sustantivos = df_cambio[pd.to_numeric(df_cambio["Sustantivo"], errors="coerce") == 1]
    
    if "tipo_gr" in df_sustantivos.columns and "tipo_doc" in df_sustantivos.columns:
        es_grupo_byr = df_sustantivos["tipo_gr"].astype(str).eq("Boletines y Revistas")
        es_boletin = df_sustantivos["tipo_doc"].astype(str).eq("Boletines")
        df_base = df_sustantivos[~(es_grupo_byr & es_boletin)]
    
    print(f"\n1. BASE INICIAL (239 sustantivos):")
    print(f"   - Cambio climático: {len(df_cambio)}")
    print(f"   - Sustantivos: {len(df_sustantivos)}")
    print(f"   - Sin boletines: {len(df_base)}")
    
    # Paso 2: Aplicar exclusiones
    df_filtrado = excluir_documentos(df_base)
    excluidos = len(df_base) - len(df_filtrado)
    
    print(f"\n2. DESPUÉS DE EXCLUSIONES:")
    print(f"   - Documentos excluidos: {excluidos}")
    print(f"   - Documentos restantes: {len(df_filtrado)}")
    
    # Paso 3: Agregar documentos
    df_final = agregar_documentos(df_filtrado)
    agregados = len(df_final) - len(df_filtrado)
    
    print(f"\n3. DESPUÉS DE AGREGACIONES:")
    print(f"   - Documentos agregados: {agregados}")
    print(f"   - TOTAL FINAL: {len(df_final)}")
    
    print("\n" + "=" * 80)
    print("RESUMEN FINAL:")
    print("=" * 80)
    print(f"Base inicial:        239 documentos")
    print(f"Menos exclusiones:   -{excluidos:2d} documentos")
    print(f"Más agregaciones:    +{agregados:2d} documentos")
    print(f"{'─' * 40}")
    print(f"TOTAL SEGUNDA FASE:   {len(df_final):3d} documentos ✓")
    
    if len(df_final) == 244:
        print("\n✅ CORRECTO: La vista genera exactamente 244 documentos")
    else:
        print(f"\n⚠️  ADVERTENCIA: Se esperaban 244 documentos, se generaron {len(df_final)}")
    
    print("=" * 80)

if __name__ == "__main__":
    main()