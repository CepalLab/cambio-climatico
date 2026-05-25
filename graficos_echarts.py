"""
Construcción de opciones ECharts para visualizaciones estadísticas.
"""

from __future__ import annotations

import math
import unicodedata
from collections import Counter
from itertools import combinations

import pandas as pd

from datos import (
    COLOR_CAMBIO_CLIMATICO,
    COLOR_DIVISION,
    TEMA_CAMBIO_CLIMATICO,
    MapaClusters,
    PERIODOS_BINS,
    asignar_periodo,
    color_tema,
    frecuencia_temas,
    normalizar_nombre_tema,
    temas_sin_cambio_climatico,
)
from topic_spa import normalizar_a_lista

CLIMA_KEY = normalizar_nombre_tema(TEMA_CAMBIO_CLIMATICO)


def _escala_tamano(
    freq: int, min_f: int, max_f: int, min_s: float = 14, max_s: float = 52
) -> float:
    if max_f <= min_f:
        return (min_s + max_s) / 2
    return min_s + (freq - min_f) / (max_f - min_f) * (max_s - min_s)


def resumen_periodos(df: pd.DataFrame) -> tuple[dict[str, int], int, int]:
    """Conteos por bin, omitidos sin año y fuera de rango."""
    conteos = {etiqueta: 0 for etiqueta, _, _ in PERIODOS_BINS}
    sin_anio = 0
    fuera_rango = 0
    if "dc.year" not in df.columns:
        return conteos, len(df), 0

    for year in df["dc.year"]:
        periodo = asignar_periodo(year)
        if periodo:
            conteos[periodo] += 1
        elif pd.isna(pd.to_numeric(year, errors="coerce")):
            sin_anio += 1
        else:
            fuera_rango += 1
    return conteos, sin_anio, fuera_rango


def opciones_barras_periodo(df: pd.DataFrame) -> dict:
    conteos, sin_anio, fuera_rango = resumen_periodos(df)
    categorias = [p[0] for p in PERIODOS_BINS]
    valores = [conteos[c] for c in categorias]

    return {
        "title": {
            "text": "Publicaciones por periodo",
            "left": "center",
        },
        "tooltip": {"trigger": "axis"},
        "grid": {"left": "3%", "right": "4%", "bottom": "8%", "containLabel": True},
        "xAxis": {
            "type": "category",
            "data": categorias,
            "axisLabel": {"interval": 0},
        },
        "yAxis": {"type": "value", "name": "Nº publicaciones"},
        "series": [
            {
                "type": "bar",
                "data": valores,
                "itemStyle": {"borderRadius": [4, 4, 0, 0]},
                "label": {"show": True, "position": "top"},
            }
        ],
        "_meta": {"sin_anio": sin_anio, "fuera_rango": fuera_rango},
    }


# Sufijos invisibles para evitar colisiones de nombres entre divisiones, CC y
# temas (p.ej. "RECURSOS NATURALES" existe como división y como tema).
SUFIJO_DIV = "\u200b"
SUFIJO_TEMA = "\u200b\u200b"
DIV_LABEL_CHARS = 20
DIV_TRUNCAR_DESDE = "DESARROLLO ECONOMICO"
DIV_TRUNCAR_MAX = 20


def _cc_pivot_id(division: str) -> str:
    """ID único del nodo CC-pivot por división (label sigue siendo Cambio Climático)."""
    return f"{TEMA_CAMBIO_CLIMATICO}\u200b\u200b\u200b{division}"


def _wrap_label(text: str, max_chars: int = 22) -> str:
    """Inserta saltos de línea para evitar labels largos que se solapen."""
    if len(text) <= max_chars:
        return text
    palabras = text.split()
    lineas: list[str] = []
    actual = ""
    for palabra in palabras:
        candidato = f"{actual} {palabra}".strip()
        if len(candidato) > max_chars and actual:
            lineas.append(actual)
            actual = palabra
        else:
            actual = candidato
    if actual:
        lineas.append(actual)
    return "\n".join(lineas)


def _truncar_label(text: str, max_chars: int = 28) -> str:
    """Trunca el label visible. El name del nodo conserva el texto completo
    para que el tooltip al hacer hover muestre el nombre real sin recortar."""
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip() + "…"


def _normalizar_div_key(texto: str) -> str:
    sin_tildes = unicodedata.normalize("NFD", texto)
    sin_tildes = "".join(c for c in sin_tildes if unicodedata.category(c) != "Mn")
    return sin_tildes.upper().strip()


def _indice_division_ancla(divisiones: list[str]) -> int | None:
    """Índice de la división ancla; debajo de ella los labels se truncan."""
    objetivo = _normalizar_div_key(DIV_TRUNCAR_DESDE)
    for i, div in enumerate(divisiones):
        if _normalizar_div_key(div) == objetivo:
            return i
    for i, div in enumerate(divisiones):
        clave = _normalizar_div_key(div)
        if "DESARROLLO" in clave and "ECONOMIC" in clave:
            return i
    return None


def _label_division_visible(div: str, indice: int, divisiones: list[str]) -> str:
    ancla = _indice_division_ancla(divisiones)
    if ancla is not None and indice > ancla:
        return _truncar_label(div, DIV_TRUNCAR_MAX)
    return _wrap_label(div, DIV_LABEL_CHARS)


def _distribuir_y(
    items: list[tuple[str, float]],
    gap_pct: float = 1.5,
    min_slot_pct: float = 0.0,
    min_slot_por_item: dict[str, float] | None = None,
) -> dict[str, float]:
    """
    Distribuye `items` verticalmente en proporción al peso y devuelve {id: y}.
    `y` está en el rango [0, 1] (formato esperado por sankey de ECharts cuando
    `layoutIterations: 0`). Se reserva `gap_pct` (en porcentaje) de aire entre
    cada par de nodos.

    `min_slot_pct` aplica un piso global. `min_slot_por_item` permite un mínimo
    distinto por id (p. ej. según líneas del label de cada división).
    """
    if not items:
        return {}
    n = len(items)
    aire_total = gap_pct * max(n - 1, 0)
    altura_util = max(100.0 - aire_total, 1.0)

    pesos = [max(w, 1) for _, w in items]
    mins = [
        max(
            min_slot_pct,
            (min_slot_por_item or {}).get(item_id, 0.0),
        )
        for item_id, _ in items
    ]
    h = [0.0] * n
    libres = list(range(n))
    h_disponible = altura_util

    if any(m > 0 for m in mins):
        while libres:
            total_libre_w = sum(pesos[i] for i in libres)
            if total_libre_w <= 0:
                break
            nuevos_libres = []
            for i in libres:
                asignado = (pesos[i] / total_libre_w) * h_disponible
                if asignado < mins[i]:
                    h[i] = mins[i]
                else:
                    nuevos_libres.append(i)
            if nuevos_libres == libres:
                total_libre_w = sum(pesos[i] for i in nuevos_libres)
                if total_libre_w > 0:
                    for i in nuevos_libres:
                        h[i] = (pesos[i] / total_libre_w) * h_disponible
                break
            h_disponible = altura_util - sum(
                h[j] for j in range(n) if j not in nuevos_libres
            )
            libres = nuevos_libres
    else:
        total_pesos = sum(pesos)
        for i in range(n):
            h[i] = (pesos[i] / total_pesos) * altura_util

    cursor = 0.0
    resultado: dict[str, float] = {}
    for (item_id, _), hi in zip(items, h):
        resultado[item_id] = (cursor + hi / 2) / 100.0
        cursor += hi + gap_pct
    return resultado


def _agregar_flujos_sankey(
    df: pd.DataFrame, top_temas_otros: int, peso_min: int
) -> tuple[Counter, Counter, dict[str, int]]:
    """
    Flujos para diagrama Sankey División → Cambio Climático → Otros temas.

    Devuelve:
      - div_tema: Counter[(división, tema) -> nº publicaciones con CC + tema]
      - div_pub_cc: Counter[división -> nº publicaciones únicas con CC]
        (cada publicación cuenta una sola vez, no por cada tema que toca)
      - freq: frecuencia general de temas
    """
    freq = frecuencia_temas(df)
    otros_ordenados = [
        t
        for t, _ in sorted(freq.items(), key=lambda x: -x[1])
        if t != CLIMA_KEY
    ][:top_temas_otros]
    temas_otros = set(otros_ordenados)
    div_tema: Counter = Counter()
    div_pub_cc: Counter = Counter()

    if "division" not in df.columns or "cepal.topicSpa" not in df.columns:
        return div_tema, div_pub_cc, freq

    for _, fila in df.iterrows():
        division = fila.get("division")
        if pd.isna(division) or not str(division).strip():
            continue
        div_name = str(division).strip()
        temas = {
            normalizar_nombre_tema(t)
            for t in normalizar_a_lista(fila.get("cepal.topicSpa"))
        }
        if CLIMA_KEY not in temas:
            continue
        div_pub_cc[div_name] += 1
        for clave in temas:
            if clave == CLIMA_KEY or clave not in temas_otros:
                continue
            div_tema[(div_name, clave)] += 1

    div_tema = Counter({k: v for k, v in div_tema.items() if v >= peso_min})
    divs_validas = {d for (d, _) in div_tema}
    div_pub_cc = Counter({d: c for d, c in div_pub_cc.items() if d in divs_validas})
    return div_tema, div_pub_cc, freq


def opciones_grafo_division_temas(
    df: pd.DataFrame,
    mapa: MapaClusters,
    top_temas: int = 40,
    peso_min: int = 1,
) -> dict:
    """
    Sankey de tres niveles: divisiones → CAMBIO CLIMÁTICO (puente) → otros temas.

    Para que el hover sobre una división resalte SÓLO sus temas (no todos), se
    crea un nodo CC-pivot por división en la columna central. Todos los pivots
    son color verde y juntos visualmente forman un único bloque de "Cambio
    Climático", pero el grafo trackea las rutas individualmente.

    `emphasis.focus: "trajectory"` propaga el hover por toda la cadena de la
    división específica hasta sus temas particulares.

    Pesos:
      - División → CC[div] = nº publicaciones únicas de la división con CC
      - CC[div] → Tema    = nº publicaciones de la división con CC + ese tema
    Como una publicación puede tocar varios temas, la suma de salidas del nodo
    CC[div] puede superar la entrada; ECharts ajusta la altura del nodo al
    máximo. Es la representación honesta del cruce (división, tema | clima).
    """
    div_tema, div_pub_cc, freq = _agregar_flujos_sankey(df, top_temas, peso_min)
    if not div_tema:
        return _grafo_vacio(
            "Sankey división ↔ cambio climático ↔ temas (sin datos con los filtros actuales)"
        )

    # Peso entrante por tema = suma de aristas CC[div] → tema
    tema_peso: Counter = Counter()
    for (_, tema), w in div_tema.items():
        tema_peso[tema] += w

    # Divisiones ordenadas por nº publicaciones con CC (desc), para que arriba
    # queden las más prolíficas y abajo las que aportan menos.
    divisiones = sorted(
        {d for (d, _) in div_tema.keys()},
        key=lambda d: -div_pub_cc.get(d, 0),
    )
    # Temas ordenados por peso entrante total (desc): arriba los más conectados.
    temas_unicos = sorted(tema_peso.keys(), key=lambda t: -tema_peso[t])

    # Balanceo de columnas: cada publicación con CC cuenta 1 vez en el lado
    # izquierdo pero N veces en el derecho (una por tema). Sin balancear,
    # ECharts comprime la columna izquierda dentro de un rango vertical mucho
    # menor que el canvas. Escalamos las aristas División→CC para que la suma
    # del lado izquierdo iguale a la del derecho y la columna de divisiones
    # aproveche toda la altura del gráfico.
    total_div_w = sum(div_pub_cc.values())
    total_tema_w = sum(tema_peso.values())
    escala_div = (total_tema_w / total_div_w) if total_div_w > 0 else 1.0

    y_div = _distribuir_y(
        [(d, div_pub_cc[d]) for d in divisiones],
        gap_pct=0.0,
        min_slot_pct=5.0,
    )
    y_tema = _distribuir_y(
        [(t, tema_peso[t]) for t in temas_unicos], gap_pct=1.0
    )

    nodos: list[dict] = []
    for i, div in enumerate(divisiones):
        nodos.append(
            {
                "name": f"{div}{SUFIJO_DIV}",
                "depth": 0,
                "y": y_div[div],
                "real_value": div_pub_cc[div],
                "itemStyle": {"color": COLOR_DIVISION, "borderColor": "#fff"},
                "label": {
                    "position": "left",
                    "fontSize": 9,
                    "formatter": _label_division_visible(div, i, divisiones),
                    "lineHeight": 11,
                    "distance": 10,
                    "align": "right",
                },
            }
        )

    # Un nodo CC-pivot por división. Todos del mismo color y sin label salvo en
    # el primero (que muestra "CAMBIO CLIMÁTICO" encima del bloque). Visualmente
    # se ven como un único bloque vertical verde compacto.
    for i, div in enumerate(divisiones):
        es_etiqueta = i == 0
        nodos.append(
            {
                "name": _cc_pivot_id(div),
                "depth": 1,
                "y": y_div[div],
                "itemStyle": {
                    "color": COLOR_CAMBIO_CLIMATICO,
                    "borderColor": COLOR_CAMBIO_CLIMATICO,
                    "borderWidth": 0,
                },
                "label": {
                    "show": es_etiqueta,
                    "position": "top",
                    "formatter": TEMA_CAMBIO_CLIMATICO if es_etiqueta else "",
                    "fontSize": 13,
                    "fontWeight": "bold",
                    "color": "#000000",
                    "distance": 18,
                },
            }
        )

    for tema in temas_unicos:
        nodos.append(
            {
                "name": f"{tema}{SUFIJO_TEMA}",
                "depth": 2,
                "y": y_tema[tema],
                "itemStyle": {
                    "color": color_tema(tema, mapa),
                    "borderColor": "#fff",
                },
                "label": {
                    "position": "right",
                    "fontSize": 9,
                    # Truncado visual con "…". El name del nodo sigue siendo el
                    # texto completo, así que el tooltip al hacer hover muestra
                    # el nombre íntegro del tema.
                    "formatter": _truncar_label(tema, 28),
                },
            }
        )

    links: list[dict] = []
    for div, w in div_pub_cc.items():
        links.append(
            {
                "source": f"{div}{SUFIJO_DIV}",
                "target": _cc_pivot_id(div),
                # `value` está escalado para que el lado izquierdo ocupe toda
                # la altura. `real_value` es el peso real (nº publicaciones con
                # CC) que muestra el tooltip.
                "value": w * escala_div,
                "real_value": w,
                "lineStyle": {"color": "source", "opacity": 0.45},
            }
        )
    for (div, tema), w in div_tema.items():
        links.append(
            {
                "source": _cc_pivot_id(div),
                "target": f"{tema}{SUFIJO_TEMA}",
                "value": w,
                "real_value": w,
                "lineStyle": {"color": "target", "opacity": 0.45},
            }
        )

    return {
        "title": {
            "text": "Red división ↔ cambio climático ↔ otros temas",
            "subtext": (
                "Sankey: cada división tiene su propio puente por CAMBIO CLIMÁTICO · "
                "hover: ruta específica de la división"
            ),
            "left": "center",
        },
        "tooltip": {
            "trigger": "item",
            "triggerOn": "mousemove",
        },
        "series": [
            {
                "type": "sankey",
                "left": "24%",
                "right": "16%",
                "top": "14%",
                "bottom": "4%",
                "nodeAlign": "justify",
                "nodeGap": 8,
                "nodeWidth": 14,
                "layoutIterations": 0,
                "data": nodos,
                "links": links,
                "label": {"show": True, "color": "#2c3e50"},
                "lineStyle": {"curveness": 0.5, "opacity": 0.4},
                "emphasis": {
                    "focus": "trajectory",
                    "label": {"fontWeight": "bold"},
                    "lineStyle": {"opacity": 0.85},
                },
                "blur": {
                    "itemStyle": {"opacity": 0.2},
                    "label": {"opacity": 0.2},
                    "lineStyle": {"opacity": 0.07},
                },
            }
        ],
    }


def _agregar_coocurrencias(
    df: pd.DataFrame, top_temas: int, peso_min: int
) -> tuple[Counter, Counter]:
    freq = Counter()
    aristas: Counter = Counter()

    if "cepal.topicSpa" not in df.columns:
        return aristas, freq

    for valor in df["cepal.topicSpa"]:
        temas = [
            normalizar_nombre_tema(t) for t in temas_sin_cambio_climatico(valor)
        ]
        for t in temas:
            freq[t] += 1
        if len(temas) < 2:
            continue
        for a, b in combinations(sorted(set(temas)), 2):
            aristas[(a, b)] += 1

    temas_top = {t for t, _ in freq.most_common(top_temas)}
    aristas_filtradas = Counter(
        {
            (a, b): w
            for (a, b), w in aristas.items()
            if w >= peso_min and a in temas_top and b in temas_top
        }
    )
    nodos = {a for a, _ in aristas_filtradas} | {b for _, b in aristas_filtradas}
    freq_filtrada = Counter({t: freq[t] for t in nodos})
    return aristas_filtradas, freq_filtrada


def _grado_coocurrencia(aristas: Counter) -> dict[str, int]:
    """Nº de temas distintos con los que co-ocurre cada nodo en el subgrafo."""
    grado: dict[str, int] = {}
    for (a, b), _ in aristas.items():
        grado[a] = grado.get(a, 0) + 1
        grado[b] = grado.get(b, 0) + 1
    return grado


def _strength_nodos(aristas: Counter) -> dict[str, float]:
    """Fuerza ponderada = suma de todos los pesos de aristas del nodo."""
    s: dict[str, float] = {}
    for (a, b), w in aristas.items():
        s[a] = s.get(a, 0.0) + w
        s[b] = s.get(b, 0.0) + w
    return s


def _escala_sqrt(val: float, max_v: float, min_s: float = 7, max_s: float = 68) -> float:
    """Escala con √ para amplificar diferencias en el extremo inferior (estilo NPM)."""
    if max_v <= 0:
        return min_s
    return min_s + (math.sqrt(max(val, 0)) / math.sqrt(max_v)) * (max_s - min_s)


def _layout_vos(
    aristas: Counter,
    nodos_grafo: list[str],
    nodos_aislados: list[str] | None = None,
    ancho: float = 760,
    alto: float = 680,
    margen: float = 55,
) -> dict[str, tuple[float, float]]:
    """
    Posiciones via Fruchterman-Reingold con pesos (solo nodos conectados).
    Nodos aislados se colocan en las esquinas como pequenos puntos.
    """
    import networkx as nx

    G = nx.Graph()
    G.add_nodes_from(nodos_grafo)
    for (a, b), w in aristas.items():
        if a in G and b in G:
            G.add_edge(a, b, weight=w)

    n = len(G)
    k = 3.0 / max(n ** 0.5, 1)
    pos = nx.spring_layout(G, weight="weight", k=k, iterations=350, seed=42)

    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    rng_x = max(max_x - min_x, 1e-9)
    rng_y = max(max_y - min_y, 1e-9)
    area_w = ancho - 2 * margen
    area_h = alto - 2 * margen

    result = {
        t: (
            margen + (pos[t][0] - min_x) / rng_x * area_w,
            margen + (pos[t][1] - min_y) / rng_y * area_h,
        )
        for t in nodos_grafo
    }

    # Aislados: esquinas (son puntos muy pequenos)
    esquinas = [
        (margen * 0.6, margen * 0.6),
        (ancho - margen * 0.6, margen * 0.6),
        (margen * 0.6, alto - margen * 0.6),
        (ancho - margen * 0.6, alto - margen * 0.6),
    ]
    for i, t in enumerate(sorted(nodos_aislados or [])):
        result[t] = esquinas[i % len(esquinas)]

    return result


def _temas_aislados_corpus(df: pd.DataFrame) -> set[str]:
    """Temas que aparecen en el corpus pero NUNCA co-ocurren con otro tema."""
    con_vecinos: set[str] = set()
    for valor in df["cepal.topicSpa"] if "cepal.topicSpa" in df.columns else []:
        temas = [normalizar_nombre_tema(t) for t in temas_sin_cambio_climatico(valor)]
        if len(temas) >= 2:
            for t in temas:
                con_vecinos.add(t)
    freq_todos = {
        normalizar_nombre_tema(t)
        for t in frecuencia_temas(df)
        if normalizar_nombre_tema(t) != CLIMA_KEY
    }
    return freq_todos - con_vecinos


def opciones_grafo_coocurrencias(
    df: pd.DataFrame,
    mapa: MapaClusters,
    top_temas: int = 60,
    peso_min: int = 2,
) -> dict:
    aristas, freq = _agregar_coocurrencias(df, top_temas, peso_min)

    # Nodos verdaderamente aislados (nunca co-ocurren con nadie)
    aislados = sorted(_temas_aislados_corpus(df))
    freq_todos = {
        normalizar_nombre_tema(t): c
        for t, c in frecuencia_temas(df).items()
        if normalizar_nombre_tema(t) != CLIMA_KEY
    }

    if not aristas and not aislados:
        return _grafo_vacio(
            "Coocurrencias entre temas (excl. CAMBIO CLIMÁTICO) — sin datos"
        )

    # Para que los aislados no dupliquen nodos que ya están en el grafo
    aislados = [t for t in aislados if t not in freq]

    nodos_grafo = sorted(freq.keys(), key=lambda t: -freq[t])
    todos_nodos = nodos_grafo + aislados

    pos = _layout_vos(aristas, nodos_grafo, aislados if aislados else None)

    strength = _strength_nodos(aristas)
    max_str = max(strength.values()) if strength else 1.0
    grado = _grado_coocurrencia(aristas)

    # Solo los 15 nodos más fuertes muestran etiqueta (como NPM graph)
    top15 = {
        t for t, _ in sorted(strength.items(), key=lambda x: -x[1])[:15]
    }

    data = []
    for tema in todos_nodos:
        f = freq_todos.get(tema, freq.get(tema, 0))
        s = strength.get(tema, 0.0)
        g = grado.get(tema, 0)
        size = _escala_sqrt(s, max_str, 6, 68)
        x, y = pos.get(tema, (380, 340))
        es_aislado = tema in aislados

        data.append(
            {
                "id": tema,
                "name": tema,
                "value": s,
                "pubCount": f,
                "coocCount": g,
                "symbol": "circle",
                "symbolSize": [round(size, 1)] * 2,
                "x": x,
                "y": y,
                "itemStyle": {
                    "color": color_tema(tema, mapa),
                    "opacity": 0.45 if es_aislado else 0.85,
                    "borderColor": "#ffffff",
                    "borderWidth": 1.5,
                    "shadowBlur": 0 if es_aislado else 4,
                    "shadowColor": "rgba(0,0,0,0.12)",
                },
                "label": {
                    "show": tema in top15,
                    "position": "right",
                    "distance": 3,
                    "fontSize": 9,
                    "color": "#222",
                    "textBorderColor": "#fff",
                    "textBorderWidth": 2,
                },
            }
        )

    max_w = max(aristas.values()) if aristas else 1
    links = [
        {
            "source": a,
            "target": b,
            "value": w,
            "lineStyle": {
                "width": 0.5 + (w / max_w) * 4.5,
                "curveness": 0,
                "color": "#b0b8c8",
                "opacity": 0.12 + (w / max_w) * 0.55,
            },
        }
        for (a, b), w in aristas.items()
    ]

    clusters_unicos = sorted(
        {mapa.tema_a_cluster.get(t, "Sin cluster") for t in todos_nodos}
    )
    leyenda_colores = [
        {"name": c, "itemStyle": {"color": mapa.cluster_a_color.get(c, "#9ca3af")}}
        for c in clusters_unicos
    ]

    opciones = {
        "title": {
            "text": "Coocurrencias entre temas",
            "subtext": (
                "Sin CAMBIO CLIMÁTICO · tamaño ∝ fuerza de co-ocurrencia · "
                "clic para enfocar vecinos"
            ),
            "left": "center",
        },
        "tooltip": {"trigger": "item", "triggerOn": "mousemove|click"},
        "series": [
            {
                "type": "graph",
                "layout": "none",
                "left": "1%",
                "right": "1%",
                "top": "11%",
                "bottom": "5%",
                "data": data,
                "links": links,
                "roam": True,
                "draggable": True,
                "emphasis": {
                    "focus": "adjacency",
                    "scale": 1.1,
                    "lineStyle": {"width": 2.5, "opacity": 0.85, "color": "#445"},
                    "itemStyle": {"opacity": 1, "borderWidth": 2.5},
                    "label": {
                        "show": True,
                        "fontWeight": "bold",
                        "fontSize": 10,
                        "color": "#111",
                    },
                },
                "blur": {
                    "itemStyle": {"opacity": 0.05},
                    "label": {"opacity": 0.05},
                    "lineStyle": {"opacity": 0.03},
                },
                "label": {
                    "position": "right",
                    "distance": 3,
                    "fontSize": 9,
                    "color": "#222",
                    "textBorderColor": "#fff",
                    "textBorderWidth": 2,
                },
            }
        ],
    }
    if leyenda_colores:
        opciones["legend"] = {
            "data": [x["name"] for x in leyenda_colores],
            "bottom": 0,
            "itemGap": 12,
        }
    return opciones


def _grafo_vacio(titulo: str) -> dict:
    return {
        "title": {"text": titulo, "left": "center"},
        "series": [{"type": "graph", "data": [], "links": []}],
    }


def quitar_meta(opciones: dict) -> dict:
    """Elimina claves internas antes de pasar a st_echarts."""
    return {k: v for k, v in opciones.items() if not k.startswith("_")}
