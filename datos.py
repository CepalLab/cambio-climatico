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


def filtrar_solo_sustantivas(df: pd.DataFrame) -> pd.DataFrame:
    """Mantiene solo publicaciones marcadas como sustantivas (Sustantivo == 1)."""
    if "Sustantivo" not in df.columns:
        return df
    return df[pd.to_numeric(df["Sustantivo"], errors="coerce") == 1]


def filtrar_excluir_boletines(df: pd.DataFrame) -> pd.DataFrame:
    """Dentro de tipo_gr == 'Boletines y Revistas' deja solo las revistas
    (excluye tipo_doc == 'Boletines'). El resto del corpus queda intacto."""
    if "tipo_gr" not in df.columns or "tipo_doc" not in df.columns:
        return df
    es_grupo_byr = df["tipo_gr"].astype(str).eq("Boletines y Revistas")
    es_boletin = df["tipo_doc"].astype(str).eq("Boletines")
    return df[~(es_grupo_byr & es_boletin)]


def filtrar_periodos(df: pd.DataFrame, periodos: list[str]) -> pd.DataFrame:
    """Filtra a publicaciones cuyo `dc.year` cae en los bins indicados
    (etiquetas de `PERIODOS_BINS`). Si la selección está vacía o incluye los
    tres bins devuelve el df sin tocar (no se considera filtro activo)."""
    if "dc.year" not in df.columns:
        return df
    todos = {etiqueta for etiqueta, _, _ in PERIODOS_BINS}
    sel = set(periodos)
    if not sel or sel >= todos:
        return df
    serie_anio = pd.to_numeric(df["dc.year"], errors="coerce")
    mask = pd.Series(False, index=df.index)
    for etiqueta, ini, fin in PERIODOS_BINS:
        if etiqueta in sel:
            mask = mask | ((serie_anio >= ini) & (serie_anio <= fin))
    return df[mask]


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


# ---------------------------------------------------------------------------
# Documentos definitivos para Fase 2
# ---------------------------------------------------------------------------

# Documentos que deben excluirse según las instrucciones de los expertos
DOCUMENTOS_A_EXCLUIR: list[str] = [
    "Acuerdo Regional",  # Versiones duplicadas en varios idiomas
    "Reglas de procedimiento del Acuerdo de Escazú",
    "Catálogo de publicaciones de la División de Desarrollo Sostenible y Asentamientos Humanos",
    "The Hummingbird",  # Revistas que deben excluirse
]

# Documentos adicionales que deben agregarse (Período de Sesiones + Foro Regional)
DOCUMENTOS_A_AGREGAR: list[dict] = [
    {"titulo": "América Latina y el Caribe ante las trampas del desarrollo", "anio": 2024,
     "handle": "https://hdl.handle.net/11362/80727"},
    {"titulo": "Hacia la transformación del modelo de desarrollo", "anio": 2022,
     "handle": "https://hdl.handle.net/11362/48304"},
    {"titulo": "Construir un nuevo futuro", "anio": 2020,
     "handle": "https://hdl.handle.net/11362/46227"},
    {"titulo": "La ineficiencia de la desigualdad", "anio": 2018,
     "handle": "https://hdl.handle.net/11362/43442"},
    {"titulo": "Horizontes 2030", "anio": 2016,
     "handle": "https://hdl.handle.net/11362/40159"},
    {"titulo": "Agenda 2030 en América Latina y el Caribe", "anio": 2026,
     "handle": "https://hdl.handle.net/11362/89774"},
    {"titulo": "América Latina y el Caribe y la Agenda 2030 a cinco años", "anio": 2025,
     "handle": "https://hdl.handle.net/11362/81405"},
    {"titulo": "América Latina y el Caribe ante el desafío de acelerar el paso", "anio": 2024,
     "handle": "https://hdl.handle.net/11362/69132"},
    {"titulo": "América Latina y el Caribe en la mitad del camino hacia 2030", "anio": 2023,
     "handle": "https://hdl.handle.net/11362/48823"},
    {"titulo": "Una década de acción para un cambio de época", "anio": 2022,
     "handle": "https://hdl.handle.net/11362/47745"},
    {"titulo": "INFORME ANUAL DE PROGRESO", "anio": 2021,
     "handle": "https://hdl.handle.net/11362/46682"},
    {"titulo": "Informe de avance cuatrienal sobre el progreso", "anio": 2019,
     "handle": "https://hdl.handle.net/11362/44551"},
    {"titulo": "Segundo informe anual sobre el progreso", "anio": 2018,
     "handle": "https://hdl.handle.net/11362/43415"},
    {"titulo": "Informe anual sobre el progreso y los desafíos regionales", "anio": 2017,
     "handle": "https://hdl.handle.net/11362/41173"},
]

COLUMNA_URI = "dc.identifier.uri"


def _excluir_documentos(df: pd.DataFrame) -> pd.DataFrame:
    """Excluye documentos según las instrucciones de los expertos."""
    for titulo in DOCUMENTOS_A_EXCLUIR:
        df = df[~df["dc.title"].str.contains(titulo, case=False, na=False)]
    df = df[~df["dc.title"].str.contains("accesible", case=False, na=False)]
    df = df[~df["dc.title"].str.contains("Catálogo de publicaciones", case=False, na=False)]
    if "tipo_gr" in df.columns:
        es_revista = df["tipo_gr"].astype(str).eq("Boletines y Revistas")
        df = df[~es_revista]
    return df


def _agregar_documentos(df_base: pd.DataFrame, df_completo: pd.DataFrame) -> pd.DataFrame:
    """Agrega los 14 documentos adicionales al DataFrame."""
    nuevos_documentos: list[dict] = []
    handles_en_base = set(df_base[COLUMNA_URI].dropna().astype(str))

    for doc in DOCUMENTOS_A_AGREGAR:
        handle = doc.get("handle", "")
        if handle in handles_en_base:
            continue
        registro = df_completo[df_completo[COLUMNA_URI] == handle]
        if len(registro) > 0:
            nuevos_documentos.append(registro.iloc[0].to_dict())
        else:
            nuevos_documentos.append({
                "dc.title": doc["titulo"],
                "dc.year": doc["anio"],
                "dc.identifier.uri": doc["handle"],
                "cepal.topicSpa": [],
                "division": "Documentos adicionales",
                "tipo_gr": "Documentos adicionales",
                "dc.description.abstract": f"Documento adicional para segunda fase. Año: {doc['anio']}",
            })

    if nuevos_documentos:
        return pd.concat([df_base, pd.DataFrame(nuevos_documentos)], ignore_index=True)
    return df_base.copy()


def _marcar_trazabilidad(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega columnas de trazabilidad al DataFrame de definitivos."""
    import datetime

    df = df.copy()
    handles_agregados = {d["handle"] for d in DOCUMENTOS_A_AGREGAR}
    ahora = datetime.datetime.now().isoformat(timespec="seconds")

    def _origen(fila):
        uri = str(fila.get(COLUMNA_URI, ""))
        if uri in handles_agregados:
            return "agregado_fase2"
        return "corpus_original"

    def _justificacion(fila):
        uri = str(fila.get(COLUMNA_URI, ""))
        titulo = str(fila.get("dc.title", ""))
        if uri in handles_agregados:
            doc = next((d for d in DOCUMENTOS_A_AGREGAR if d["handle"] == uri), None)
            if doc:
                if "foro" in titulo.lower() or "agenda 2030" in titulo.lower():
                    return "agregado_foro_regional"
                return "agregado_periodo_sesiones"
        for excl in DOCUMENTOS_A_EXCLUIR:
            if excl.lower() in titulo.lower():
                return "excluido_" + excl[:30].replace(" ", "_")
        if "accesible" in titulo.lower():
            return "excluido_version_accesible"
        return "corpus_original"

    df["__origen"] = df.apply(_origen, axis=1)
    df["__justificacion"] = df.apply(_justificacion, axis=1)
    df["__fecha_inclusion"] = ahora
    df["__fase"] = "fase2_depuracion"
    return df


def cargar_documentos_definitivos(_mtime: int = 0) -> pd.DataFrame:
    """Carga el corpus definitivo para Fase 2 con columnas de trazabilidad.

    Aplica: cambio climático → sustantivas → excluir boletines →
    excluir documentos específicos → agregar documentos adicionales →
    marcar trazabilidad.
    """
    df_completo = cargar_datos(_mtime=_mtime)
    df = filtrar_cambio_climatico(df_completo)
    df = filtrar_solo_sustantivas(df)
    df = filtrar_excluir_boletines(df)
    df = _excluir_documentos(df)
    df = _agregar_documentos(df, df_completo)
    df = _marcar_trazabilidad(df)
    return df
