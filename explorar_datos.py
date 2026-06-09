#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from pathlib import Path

# Ruta al archivo de datos
DIR = Path(__file__).resolve().parent
ARCHIVO_DATOS = DIR / "datos_dashboard_final.xlsx"

def explorar_estructura_excel():
    """Explora la estructura del archivo Excel"""
    print("Explorando estructura del archivo Excel...")
    
    # Leer el archivo Excel
    df = pd.read_excel(ARCHIVO_DATOS)
    
    # Mostrar información básica
    print(f"Dimensiones del DataFrame: {df.shape}")
    print(f"Columnas: {list(df.columns)}")
    print("\nPrimeras filas:")
    print(df.head())
    
    # Mostrar información detallada
    print("\nInformación detallada:")
    print(df.info())
    
    # Verificar si existe la columna cepal.topicSpa
    if 'cepal.topicSpa' in df.columns:
        print("\nValores únicos en cepal.topicSpa:")
        print(df['cepal.topicSpa'].unique()[:20])  # Mostrar solo los primeros 20 valores únicos
    
    return df

if __name__ == "__main__":
    explorar_estructura_excel()