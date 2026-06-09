#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Valida integridad de datos para la segunda fase:
1. Handles únicos y con formato correcto (https://hdl.handle.net/11362/......)
2. cepal.topicSpa en formato lista normalizado
"""

from __future__ import annotations

import re
from pathlib import Path
from collections import Counter

import pandas as pd

from topic_spa import (
    construir_vocabulario,
    ampliar_vocabulario_desde_csv,
    normalizar_a_lista,
    formatear_lista,
    parece_lista,
)

DIR = Path(__file__).resolve().parent
ARCHIVO = DIR / "datos_dashboard_final.xlsx"
COLUMNA_URI = "dc.identifier.uri"
COLUMNA_TOPICS = "cepal.topicSpa"

PATRON_HANDLE = r"^https://hdl\.handle\.net/11362/\d+$"


def validar_handles(df: pd.DataFrame) -> dict:
    """Valida que todos los handles sean únicos y tengan formato correcto"""
    print("\n" + "=" * 80)
    print("VALIDACIÓN 1: HANDLES")
    print("=" * 80)
    
    handles = df[COLUMNA_URI].dropna().astype(str)
    print(f"Total de registros: {len(df)}")
    print(f"Handles no nulos: {len(handles)}")
    
    # Chequear formato
    validos = handles[handles.str.match(PATRON_HANDLE)]
    invalidos = handles[~handles.str.match(PATRON_HANDLE)]
    
    print(f"\n✓ Handles con formato correcto: {len(validos)}")
    print(f"✗ Handles con formato incorrecto: {len(invalidos)}")
    
    if len(invalidos) > 0:
        print("\nEjemplos de handles inválidos:")
        for h in invalidos.head(5).values:
            print(f"  - {h}")
    
    # Chequear duplicados
    contador = Counter(handles)
    duplicados = {h: c for h, c in contador.items() if c > 1}
    
    print(f"\n✓ Handles únicos: {len(set(handles))}")
    print(f"✗ Handles duplicados: {len(duplicados)}")
    
    if duplicados:
        print("\nHandles duplicados:")
        for h, c in sorted(duplicados.items(), key=lambda x: -x[1]):
            print(f"  - {h}: {c} veces")
    
    return {
        "validos": len(validos),
        "invalidos": len(invalidos),
        "unicos": len(set(handles)),
        "duplicados": len(duplicados),
        "handles_invalidos": invalidos.tolist() if len(invalidos) > 0 else None,
        "handles_duplicados": duplicados if len(duplicados) > 0 else None,
    }


def validar_topics(df: pd.DataFrame) -> dict:
    """Valida que cepal.topicSpa esté en formato lista normalizado"""
    print("\n" + "=" * 80)
    print("VALIDACIÓN 2: CEPAL.TOPICSPA")
    print("=" * 80)
    
    topics_serie = df[COLUMNA_TOPICS]
    print(f"Total de registros: {len(df)}")
    print(f"Valores no nulos: {topics_serie.notna().sum()}")
    print(f"Valores nulos: {topics_serie.isna().sum()}")
    
    # Chequear formato
    topics_str = topics_serie.dropna().astype(str)
    
    # Construir vocabulario para normalización
    vocab = construir_vocabulario(topics_serie)
    vocab = ampliar_vocabulario_desde_csv(topics_serie, vocab)
    
    pareceListaCount = sum(1 for v in topics_str if parece_lista(v))
    print(f"\n✓ Ya en formato lista: {pareceListaCount}")
    print(f"✗ No en formato lista: {len(topics_str) - pareceListaCount}")
    
    # Muestrear valores
    print("\nEjemplos de valores actuales:")
    for i, v in enumerate(topics_str.head(3).values):
        print(f"  [{i+1}] {v[:100]}")
    
    # Chequear si necesita normalización
    normalizadas = []
    cambios_necesarios = 0
    
    for valor in topics_serie:
        if pd.isna(valor):
            normalizadas.append(pd.NA)
            continue
        
        texto_antes = str(valor).strip()
        temas = normalizar_a_lista(valor, vocab)
        texto_despues = formatear_lista(temas) if temas else ""
        
        if texto_antes != texto_despues:
            cambios_necesarios += 1
        
        normalizadas.append(temas)
    
    print(f"\n✓ Ya normalizados: {len(topics_str) - cambios_necesarios}")
    print(f"⚠️  Necesitan normalización: {cambios_necesarios}")
    
    if cambios_necesarios > 0:
        print("\n⚠️  RECOMENDACIÓN: Ejecutar normalizar_topic_spa.py")
        print("   python normalizar_topic_spa.py")
    else:
        print("\n✅ TODOS LOS TEMAS YA ESTÁN NORMALIZADOS")
    
    return {
        "no_nulos": topics_serie.notna().sum(),
        "en_formato_lista": pareceListaCount,
        "necesitan_normalizacion": cambios_necesarios,
        "temas_unicos": len(vocab),
    }


def validar_segunda_fase(df: pd.DataFrame) -> dict:
    """Valida los datos que se usarán en la segunda fase"""
    print("\n" + "=" * 80)
    print("VALIDACIÓN 3: DATOS PARA SEGUNDA FASE")
    print("=" * 80)
    
    from datos import (
        filtrar_cambio_climatico,
        filtrar_solo_sustantivas,
        filtrar_excluir_boletines,
    )
    from segunda_fase import excluir_documentos, agregar_documentos
    
    # Aplicar filtros de la app
    df_cambio = filtrar_cambio_climatico(df)
    df_sustantivos = filtrar_solo_sustantivas(df_cambio)
    df_base = filtrar_excluir_boletines(df_sustantivos)
    
    print(f"Base inicial (239 sustantivos): {len(df_base)}")
    
    # Chequear handles en base
    handles_base = df_base[COLUMNA_URI].dropna().astype(str)
    handles_validos_base = handles_base[handles_base.str.match(PATRON_HANDLE)]
    
    print(f"  - Handles válidos: {len(handles_validos_base)}/{len(handles_base)}")
    
    if len(handles_validos_base) < len(handles_base):
        print(f"  ⚠️  {len(handles_base) - len(handles_validos_base)} handles inválidos en base")
    
    # Chequear topics en base
    topics_base = df_base[COLUMNA_TOPICS].notna().sum()
    print(f"  - Registros con topics: {topics_base}/{len(df_base)}")
    
    # Aplicar exclusiones y agregaciones
    df_filtrado = excluir_documentos(df_base)
    df_final = agregar_documentos(df_filtrado)
    
    print(f"\nDespués de exclusiones (-9): {len(df_filtrado)}")
    print(f"Después de agregaciones (+14): {len(df_final)}")
    
    # Chequear handles en final
    handles_final = df_final[COLUMNA_URI].dropna().astype(str)
    handles_validos_final = handles_final[handles_final.str.match(PATRON_HANDLE)]
    
    print(f"\n  - Handles válidos: {len(handles_validos_final)}/{len(handles_final)}")
    
    # Chequear duplicados en final
    contador_final = Counter(handles_final)
    duplicados_final = {h: c for h, c in contador_final.items() if c > 1}
    
    if duplicados_final:
        print(f"  ⚠️  {len(duplicados_final)} handles duplicados en resultado final")
        for h, c in list(duplicados_final.items())[:3]:
            print(f"    - {h}: {c} veces")
    else:
        print(f"  ✓ Sin duplicados en resultado final")
    
    # Chequear topics en final
    topics_final = df_final[COLUMNA_TOPICS].notna().sum()
    print(f"\n  - Registros con topics: {topics_final}/{len(df_final)}")
    
    return {
        "base_inicial": len(df_base),
        "despues_exclusiones": len(df_filtrado),
        "resultado_final": len(df_final),
        "handles_validos": len(handles_validos_final),
        "handles_duplicados": len(duplicados_final),
        "registros_con_topics": topics_final,
    }


def main():
    print("\n" + "=" * 80)
    print("VALIDACIÓN DE DATOS PARA SEGUNDA FASE")
    print("=" * 80)
    
    if not ARCHIVO.exists():
        print(f"\n❌ ERROR: No se encontró {ARCHIVO}")
        return
    
    print(f"\nLeyendo {ARCHIVO.name}...")
    df = pd.read_excel(ARCHIVO)
    
    # Ejecutar validaciones
    handles_report = validar_handles(df)
    topics_report = validar_topics(df)
    segunda_fase_report = validar_segunda_fase(df)
    
    # Resumen final
    print("\n" + "=" * 80)
    print("RESUMEN FINAL")
    print("=" * 80)
    
    print("\n✓ HANDLES:")
    print(f"  - Válidos: {handles_report['validos']}")
    print(f"  - Únicos: {handles_report['unicos']}")
    
    if handles_report['invalidos'] > 0:
        print(f"  ⚠️  Inválidos: {handles_report['invalidos']}")
    
    if handles_report['duplicados'] > 0:
        print(f"  ⚠️  Duplicados: {handles_report['duplicados']}")
    
    print("\n✓ CEPAL.TOPICSPA:")
    print(f"  - En formato lista: {topics_report['en_formato_lista']}")
    print(f"  - No nulos: {topics_report['no_nulos']}")
    
    if topics_report['necesitan_normalizacion'] > 0:
        print(f"  ⚠️  Necesitan normalización: {topics_report['necesitan_normalizacion']}")
    else:
        print(f"  ✅ Todos normalizados")
    
    print("\n✓ SEGUNDA FASE:")
    print(f"  - Resultado final: {segunda_fase_report['resultado_final']} documentos")
    print(f"  - Handles válidos: {segunda_fase_report['handles_validos']}")
    
    if segunda_fase_report['handles_duplicados'] > 0:
        print(f"  ⚠️  Handles duplicados: {segunda_fase_report['handles_duplicados']}")
    
    # Recomendaciones
    print("\n" + "=" * 80)
    print("RECOMENDACIONES")
    print("=" * 80)
    
    problemas = []
    
    if handles_report['invalidos'] > 0:
        problemas.append(f"✗ Existen {handles_report['invalidos']} handles con formato incorrecto")
    
    if handles_report['duplicados'] > 0:
        problemas.append(f"✗ Existen {handles_report['duplicados']} handles duplicados")
    
    if topics_report['necesitan_normalizacion'] > 0:
        problemas.append(f"⚠️  {topics_report['necesitan_normalizacion']} registros necesitan normalización de topics")
    
    if not problemas:
        print("✅ No se detectaron problemas. Los datos están listos para la segunda fase.")
    else:
        print("\nProblemas detectados:")
        for p in problemas:
            print(f"  {p}")
        
        if topics_report['necesitan_normalizacion'] > 0:
            print("\nPara normalizar topics, ejecutar:")
            print("  python normalizar_topic_spa.py")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
