#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from pathlib import Path

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
    print("VERIFICACIÓN: DOCUMENTOS SUSTANTIVOS CON TEMA 'CAMBIO CLIMÁTICO'")
    print("=" * 80)
    
    # Leer los datos
    df = pd.read_excel(ARCHIVO_DATOS)
    print(f"\nTotal de registros en dataset: {len(df)}")
    
    # Paso 1: Documentos con tema "CAMBIO CLIMÁTICO"
    df_cambio = df[df["cepal.topicSpa"].apply(lambda v: contiene_tema(v, "CAMBIO CLIMÁTICO"))]
    print(f"Documentos con tema 'CAMBIO CLIMÁTICO': {len(df_cambio)}")
    
    # Paso 2: Documentos sustantivos (Sustantivo == 1)
    if "Sustantivo" in df.columns:
        df_sustantivos = df_cambio[pd.to_numeric(df_cambio["Sustantivo"], errors="coerce") == 1]
        print(f"Documentos sustantivos (Sustantivo == 1): {len(df_sustantivos)}")
    else:
        print("Columna 'Sustantivo' no encontrada")
        df_sustantivos = df_cambio
    
    # Paso 3: Excluir boletines (pero mantener revistas)
    if "tipo_gr" in df_sustantivos.columns and "tipo_doc" in df_sustantivos.columns:
        es_grupo_byr = df_sustantivos["tipo_gr"].astype(str).eq("Boletines y Revistas")
        es_boletin = df_sustantivos["tipo_doc"].astype(str).eq("Boletines")
        df_sin_boletines = df_sustantivos[~(es_grupo_byr & es_boletin)]
        boletines_excluidos = len(df_sustantivos) - len(df_sin_boletines)
        print(f"Boletines excluidos: {boletines_excluidos}")
        print(f"Después de excluir boletines: {len(df_sin_boletines)}")
    else:
        df_sin_boletines = df_sustantivos
        print("Columnas 'tipo_gr' o 'tipo_doc' no encontradas")
    
    print("\n" + "=" * 80)
    print("RESUMEN PARA LA APP ACTUAL:")
    print("=" * 80)
    print(f"Documentos en la app (sustantivos, sin boletines): {len(df_sin_boletines)}")
    print(f"Diferencia con 239: {len(df_sin_boletines) - 239}")
    print("=" * 80)
    
    # Ahora aplicar los cambios para segunda fase
    print("\n" + "=" * 80)
    print("CAMBIOS PARA SEGUNDA FASE:")
    print("=" * 80)
    
    df_segunda_fase = df_sin_boletines.copy()
    
    # Excluir documentos específicos
    excluir_list = [
        "Acuerdo Regional",
        "Reglas de procedimiento del Acuerdo de Escazú",
        "Catálogo de publicaciones de la División de Desarrollo Sostenible y Asentamientos Humanos",
        "The Hummingbird",
    ]
    
    for titulo in excluir_list:
        antes = len(df_segunda_fase)
        df_segunda_fase = df_segunda_fase[~df_segunda_fase["dc.title"].str.contains(titulo, case=False, na=False)]
        despues = len(df_segunda_fase)
        if antes != despues:
            print(f"Excluido '{titulo}': -{antes - despues} documentos")
    
    # Excluir versiones accesibles
    antes = len(df_segunda_fase)
    df_segunda_fase = df_segunda_fase[~df_segunda_fase["dc.title"].str.contains("accesible", case=False, na=False)]
    despues = len(df_segunda_fase)
    if antes != despues:
        print(f"Excluido 'accesible': -{antes - despues} documentos")
    
    # Excluir por división
    antes = len(df_segunda_fase)
    df_segunda_fase = df_segunda_fase[~df_segunda_fase["division"].str.contains("Desarrollo Sostenible y Asentamientos Humanos", case=False, na=False)]
    despues = len(df_segunda_fase)
    if antes != despues:
        print(f"Excluido división 'Desarrollo Sostenible': -{antes - despues} documentos")
    
    # Excluir TODAS las revistas (no solo boletines)
    antes = len(df_segunda_fase)
    if "tipo_gr" in df_segunda_fase.columns:
        es_revista = df_segunda_fase["tipo_gr"].astype(str).eq("Boletines y Revistas")
        df_segunda_fase = df_segunda_fase[~es_revista]
    despues = len(df_segunda_fase)
    if antes != despues:
        print(f"Excluido todas las revistas: -{antes - despues} documentos")
    
    # Agregar 14 documentos
    documentos_a_agregar = 14
    total_final = len(df_segunda_fase) + documentos_a_agregar
    
    print(f"\nDocumentos sustantivos después de exclusiones: {len(df_segunda_fase)}")
    print(f"Documentos a agregar: +{documentos_a_agregar}")
    print(f"Total para segunda fase: {total_final}")
    
    print("\n" + "=" * 80)
    print(f"Base en app actual:    239 documentos")
    print(f"Documentos depurados:  {len(df_segunda_fase)} documentos")
    print(f"Cambio:                {len(df_segunda_fase) - 239:+d} documentos")
    print("=" * 80)

if __name__ == "__main__":
    main()