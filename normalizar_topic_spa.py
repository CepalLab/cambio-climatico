"""
Normaliza cepal.topicSpa a formato lista en datos_dashboard_final.xlsx.

Uso:
    python normalizar_topic_spa.py

Crea respaldo en datos_dashboard_final.backup.xlsx antes de sobrescribir.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pandas as pd

from topic_spa import (
    ampliar_vocabulario_desde_csv,
    construir_vocabulario,
    formatear_lista,
    normalizar_a_lista,
    parece_lista,
)

DIR = Path(__file__).resolve().parent
ARCHIVO = DIR / "datos_dashboard_final.xlsx"
RESPALDO = DIR / "datos_dashboard_final.backup.xlsx"
COLUMNA = "cepal.topicSpa"


def main() -> None:
    if not ARCHIVO.exists():
        raise FileNotFoundError(f"No se encontró {ARCHIVO}")

    print(f"Leyendo {ARCHIVO.name}…")
    df = pd.read_excel(ARCHIVO)

    if COLUMNA not in df.columns:
        raise KeyError(f"Falta la columna {COLUMNA}")

    serie = df[COLUMNA]
    ya_lista = serie.dropna().astype(str).apply(parece_lista).sum()
    print(f"Filas totales: {len(df)}")
    print(f"Valores no nulos: {serie.notna().sum()}")
    print(f"Ya en formato lista: {ya_lista}")

    vocab = construir_vocabulario(serie)
    vocab = ampliar_vocabulario_desde_csv(serie, vocab)
    print(f"Temas en vocabulario: {len(vocab)}")

    temas_por_fila: list[list[str]] = []
    cambiadas = 0
    unicas_antes = set()
    unicas_despues = set()

    for valor in serie:
        if pd.isna(valor):
            temas_por_fila.append([])
            continue
        texto_antes = str(valor).strip()
        unicas_antes.add(texto_antes)
        temas = normalizar_a_lista(valor, vocab)
        texto_despues = formatear_lista(temas) if temas else ""
        temas_por_fila.append(temas)
        unicas_despues.add(texto_despues)
        if texto_antes != texto_despues:
            cambiadas += 1

    df[COLUMNA] = [formatear_lista(t) if t else pd.NA for t in temas_por_fila]

    print(f"Filas modificadas: {cambiadas}")
    print(f"Valores unicos antes: {len(unicas_antes)} -> despues: {len(unicas_despues)}")

    if not RESPALDO.exists():
        shutil.copy2(ARCHIVO, RESPALDO)
        print(f"Respaldo creado: {RESPALDO.name}")
    else:
        print(f"Respaldo ya existía: {RESPALDO.name} (no se sobrescribe)")

    df.to_excel(ARCHIVO, index=False)
    print(f"Guardado: {ARCHIVO.name}")

    # Muestras de verificación
    print("\n--- Ejemplos ---")
    ejemplos = [
        "INNOVACIÓN, CIENCIA Y TECNOLOGÍA",
        "MICRO, PEQUEÑAS Y MEDIANAS EMPRESAS (MIPYME)",
        "DESARROLLO SOSTENIBLE, CAMBIO CLIMÁTICO, PRODUCTIVIDAD",
    ]
    for ej in ejemplos:
        print(f"  CSV: {ej!r}")
        print(f"    -> {formatear_lista(normalizar_a_lista(ej, vocab))}")


if __name__ == "__main__":
    main()
