"""
Genera el CSV de trazabilidad con los documentos definitivos de Fase 2.

Ejecutar:
    python3 generar_trazabilidad.py
"""

from datos import cargar_documentos_definitivos, _mtime_archivo, ARCHIVO_DATOS

def main():
    print("Cargando documentos definitivos...")
    df = cargar_documentos_definitivos(_mtime=_mtime_archivo(ARCHIVO_DATOS))
    
    print(f"Total de documentos definitivos: {len(df)}")
    
    # Estadísticas por origen
    if "__origen" in df.columns:
        print("\nDistribución por origen:")
        print(df["__origen"].value_counts().to_string())
    
    # Guardar CSV
    archivo_salida = "documentos_definitivos_trazabilidad.csv"
    df.to_csv(archivo_salida, index=False, encoding="utf-8-sig")
    print(f"\nCSV guardado en: {archivo_salida}")
    
    # Mostrar primeras filas
    print("\nPrimeras 5 filas:")
    print(df[["dc.title", "dc.year", "__origen", "__justificacion"]].head())

if __name__ == "__main__":
    main()
