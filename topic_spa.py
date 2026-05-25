"""
Utilidades para el campo cepal.topicSpa (temas en español como listas).
"""

from __future__ import annotations

import ast
import re
from typing import Iterable

import pandas as pd

# Temas cuyo nombre incluye coma pero son un solo elemento
TEMAS_CON_COMA = (
    "INNOVACIÓN, CIENCIA Y TECNOLOGÍA",
    "MICRO, PEQUEÑAS Y MEDIANAS EMPRESAS (MIPYME)",
)


def parece_lista(texto: str) -> bool:
    texto = texto.strip()
    return texto.startswith("[") and texto.endswith("]")


def construir_vocabulario(series: pd.Series) -> set[str]:
    """Vocabulario canónico a partir de valores ya en formato lista y temas sueltos."""
    vocab: set[str] = set(TEMAS_CON_COMA)
    for valor in series.dropna().astype(str):
        texto = valor.strip()
        if not texto:
            continue
        if parece_lista(texto):
            for tema in parsear_lista_literal(texto):
                vocab.add(tema)
        elif "," not in texto:
            vocab.add(texto)
    return vocab


def parsear_lista_literal(texto: str) -> list[str]:
    try:
        items = ast.literal_eval(texto.strip())
    except (SyntaxError, ValueError):
        return []
    if not isinstance(items, list):
        return []
    return [str(item).strip() for item in items if str(item).strip()]


def dividir_csv_respetando_protegidos(texto: str, protegidos: Iterable[str]) -> list[str]:
    """Separa por comas sin romper temas que llevan coma en el nombre."""
    s = texto.strip()
    placeholders: dict[str, str] = {}
    for i, frase in enumerate(protegidos):
        if frase not in s:
            continue
        clave = f"__PROT_{i}__"
        s = s.replace(frase, clave)
        placeholders[clave] = frase

    partes = []
    for trozo in s.split(","):
        trozo = trozo.strip()
        if not trozo:
            continue
        partes.append(placeholders.get(trozo, trozo))
    return partes


def normalizar_a_lista(valor, vocab: set[str] | None = None) -> list[str]:
    """
    Convierte un valor de cepal.topicSpa a lista de strings.
    Acepta: lista serializada, CSV plano o tema único.
    """
    if pd.isna(valor):
        return []

    texto = str(valor).strip()
    if not texto:
        return []

    if parece_lista(texto):
        temas = parsear_lista_literal(texto)
        if temas:
            return temas

    protegidos = sorted(
        {t for t in (vocab or set()) if "," in t} | set(TEMAS_CON_COMA),
        key=len,
        reverse=True,
    )

    if "," not in texto:
        return [texto]

    return dividir_csv_respetando_protegidos(texto, protegidos)


def formatear_lista(temas: list[str]) -> str:
    """Representación uniforme para guardar en Excel (estilo Python)."""
    return str(temas)


def temas_a_texto(valor, max_chars: int | None = None) -> str:
    """Texto legible para tablas: 'A, B, C' sin corchetes ni comillas."""
    temas = normalizar_a_lista(valor)
    if not temas:
        return ""
    texto = ", ".join(temas)
    if max_chars and len(texto) > max_chars:
        return texto[:max_chars] + "…"
    return texto


def contiene_tema(valor, tema_buscado: str) -> bool:
    buscado = tema_buscado.strip().upper()
    return any(t.upper() == buscado for t in normalizar_a_lista(valor))


def ampliar_vocabulario_desde_csv(series: pd.Series, vocab: set[str]) -> set[str]:
    """Incorpora temas que aparecen solo en cadenas CSV planas."""
    protegidos = sorted(
        {t for t in vocab if "," in t} | set(TEMAS_CON_COMA),
        key=len,
        reverse=True,
    )
    for valor in series.dropna().astype(str):
        texto = valor.strip()
        if parece_lista(texto) or "," not in texto:
            continue
        for tema in dividir_csv_respetando_protegidos(texto, protegidos):
            vocab.add(tema)
    return vocab
