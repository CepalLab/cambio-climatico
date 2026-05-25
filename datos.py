"""
Carga de datos y utilidades compartidas — explorador y visualizaciones.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import streamlit as st

from topic_spa import contiene_tema, normalizar_a_lista

DIR = Path(__file__).resolve().parent
ARCHIVO_DATOS = DIR / "datos_dashboard_final.xlsx"
ARCHIVO_CLUSTERS = DIR / "clusters.xlsx"

TEMA_CAMBIO_CLIMATICO = "CAMBIO CLIMÁTICO"
COLOR_SIN_CLUSTER = "#9ca3af"
CLUSTER_SIN_ASIGNAR = "Sin cluster"
COLOR_DIVISION = "#4a6fa5"
COLOR_CAMBIO_CLIMATICO = "#16a085"

# Paleta institucional: 5 clusters de clusters.xlsx (columna Cluster, 3ª col.)
_COLOR_CLUSTER_ID: dict[str, str] = {
    "1": "#c0392b",  # Desarrollo económico
    "2": "#2980b9",  # Desarrollo social
    "3": "#27ae60",  # Sustentabilidad ambiental
    "4": "#8e44ad",  # Desarrollo productivo e innovación
    "5": "#d4ac0d",  # Institucionalidad y temas transversales
}
_PALETA_CLUSTER: tuple[tuple[tuple[str, ...], str], ...] = (
    (("desarrollo economico", "macroeconomia", "comercio", "finanzas", "fiscal"), "#c0392b"),
    (("desarrollo social", "grupos poblacionales", "poblacional"), "#2980b9"),
    (
        ("sostenibilidad", "sustentabilidad", "ambiental", "recursos naturales", "medio ambiente"),
        "#27ae60",
    ),
    (
        ("desarrollo productivo", "innovacion", "tecnolog", "productivo"),
        "#8e44ad",
    ),
    (
        ("institucionalidad", "gobernanza", "transversal", "institucional", "miscelaneo"),
        "#d4ac0d",
    ),
)
_CANDIDATOS_COL_TEMA = (
    "temas",
    "tema",
    "topic",
    "topico",
    "cepal.topicspa",
    "cepal.topicSpa",
)
_CANDIDATOS_COL_CLUSTER = (
    "cluster",
    "cluster_id",
    "grupo",
    "cluster_nombre",
)

PERIODOS_BINS: tuple[tuple[str, int, int], ...] = (
    ("2015-2018", 2015, 2018),
    ("2019-2022", 2019, 2022),
    ("2023-2026", 2023, 2026),
)


def normalizar_nombre_tema(tema: str) -> str:
    return tema.strip().upper()


def _normalizar_texto_cluster(texto: str) -> str:
    sin_acentos = "".join(
        c
        for c in unicodedata.normalize("NFD", texto.lower())
        if unicodedata.category(c) != "Mn"
    )
    return re.sub(r"[^a-z0-9]+", " ", sin_acentos).strip()


def _mtime_archivo(path: Path) -> int:
    """Marca de tiempo del archivo; cambia al guardar el Excel y invalida caché."""
    try:
        return int(path.stat().st_mtime_ns)
    except OSError:
        return 0


def color_por_nombre_cluster(cluster: str) -> str:
    """Color del cluster según id 1–5 o palabras clave del nombre en clusters.xlsx."""
    norm = _normalizar_texto_cluster(cluster)
    match_id = re.match(r"^(\d)\b", norm) or re.match(r"^(\d)", norm)
    if match_id and match_id.group(1) in _COLOR_CLUSTER_ID:
        return _COLOR_CLUSTER_ID[match_id.group(1)]
    for palabras, color in _PALETA_CLUSTER:
        if any(p in norm for p in palabras):
            return color
    return COLOR_SIN_CLUSTER


@st.cache_data(show_spinner="Cargando datos…")
def cargar_datos(_mtime: int = 0) -> pd.DataFrame:
    """_mtime invalida caché cuando cambia datos_dashboard_final.xlsx."""
    return pd.read_excel(ARCHIVO_DATOS)


def filtrar_cambio_climatico(df: pd.DataFrame) -> pd.DataFrame:
    if "cepal.topicSpa" not in df.columns:
        return df.iloc[0:0]
    return df[df["cepal.topicSpa"].apply(lambda v: contiene_tema(v, TEMA_CAMBIO_CLIMATICO))]


def asignar_periodo(year) -> str | None:
    valor = pd.to_numeric(year, errors="coerce")
    if pd.isna(valor):
        return None
    anio = int(valor)
    for etiqueta, inicio, fin in PERIODOS_BINS:
        if inicio <= anio <= fin:
            return etiqueta
    return None


def _detectar_columna(columnas: list[str], candidatos: tuple[str, ...]) -> str | None:
    mapa = {c.lower().strip(): c for c in columnas}
    for nombre in candidatos:
        if nombre in mapa:
            return mapa[nombre]
    return None


@dataclass(frozen=True)
class MapaClusters:
    tema_a_color: dict[str, str]
    tema_a_cluster: dict[str, str]
    cluster_a_color: dict[str, str]
    archivo_encontrado: bool
    columnas_detectadas: tuple[str, str, str] | None


@st.cache_data(show_spinner="Cargando clusters…")
def cargar_mapa_clusters(_mtime: int = 0) -> MapaClusters:
    vacio = MapaClusters({}, {}, {}, False, None)
    if not ARCHIVO_CLUSTERS.exists():
        return vacio

    df = pd.read_excel(ARCHIVO_CLUSTERS)
    cols = list(df.columns)
    col_tema = _detectar_columna(cols, _CANDIDATOS_COL_TEMA)
    col_cluster = _detectar_columna(cols, _CANDIDATOS_COL_CLUSTER)
    col_color = _detectar_columna(cols, ("color", "hex", "colour", "colores"))

    # clusters.xlsx: 1ª columna = temas, 3ª = Cluster (p. ej. temas | Item | Cluster)
    if not col_tema and len(cols) >= 1:
        col_tema = cols[0]
    if not col_cluster and len(cols) >= 3:
        col_cluster = cols[2]

    if not col_tema:
        return vacio

    tema_a_color: dict[str, str] = {}
    tema_a_cluster: dict[str, str] = {}
    cluster_a_color: dict[str, str] = {}

    for _, fila in df.iterrows():
        tema_raw = fila.get(col_tema)
        if pd.isna(tema_raw) or not str(tema_raw).strip():
            continue
        clave = normalizar_nombre_tema(str(tema_raw))
        cluster = (
            str(fila[col_cluster]).strip()
            if col_cluster and pd.notna(fila.get(col_cluster))
            else CLUSTER_SIN_ASIGNAR
        )
        color = color_por_nombre_cluster(cluster)
        if col_color and pd.notna(fila.get(col_color)):
            color_raw = str(fila[col_color]).strip()
            if color_raw.startswith("#"):
                color = color_raw
        tema_a_cluster[clave] = cluster
        tema_a_color[clave] = color
        if cluster not in cluster_a_color:
            cluster_a_color[cluster] = color

    detectadas = (
        col_tema,
        col_cluster or "",
        col_color or "",
    )
    return MapaClusters(
        tema_a_color=tema_a_color,
        tema_a_cluster=tema_a_cluster,
        cluster_a_color=cluster_a_color,
        archivo_encontrado=True,
        columnas_detectadas=detectadas,
    )


def color_tema(tema: str, mapa: MapaClusters) -> str:
    clave = normalizar_nombre_tema(tema)
    if clave in mapa.tema_a_color:
        return mapa.tema_a_color[clave]
    return color_por_nombre_cluster(cluster_tema(tema, mapa))


def cluster_tema(tema: str, mapa: MapaClusters) -> str:
    return mapa.tema_a_cluster.get(normalizar_nombre_tema(tema), CLUSTER_SIN_ASIGNAR)


def temas_sin_cambio_climatico(valor) -> list[str]:
    return [
        t
        for t in normalizar_a_lista(valor)
        if normalizar_nombre_tema(t) != normalizar_nombre_tema(TEMA_CAMBIO_CLIMATICO)
    ]


def frecuencia_temas(df: pd.DataFrame) -> dict[str, int]:
    conteo: dict[str, int] = {}
    if "cepal.topicSpa" not in df.columns:
        return conteo
    for valor in df["cepal.topicSpa"]:
        for tema in normalizar_a_lista(valor):
            clave = normalizar_nombre_tema(tema)
            conteo[clave] = conteo.get(clave, 0) + 1
    return conteo
