# Archivo `clusters.xlsx`

Coloca este archivo en la misma carpeta que `explorador.py` / `app.py`:

`experimentos/cambio_climatico/clusters.xlsx`

## Columnas esperadas

El cargador detecta nombres flexibles (sin distinguir mayúsculas):

| Rol | Nombres aceptados | Posición por defecto |
|-----|-------------------|----------------------|
| Tema | `temas`, `tema`, `topic`, `topico`, `cepal.topicSpa` | 1ª columna |
| Cluster | `cluster`, `cluster_id`, `grupo`, `cluster_nombre` | 3ª columna |
| Color | `color`, `hex`, `colour` | opcional |

## Formato actual (`clusters.xlsx`)

| temas | Item | Cluster |
|-------|------|---------|
| BIODIVERSIDAD | … | 3. Sustentabilidad ambiental y gestión de recursos naturales |
| ASUNTOS FISCALES | … | 1. Desarrollo económico |

No hace falta columna de color: se asigna automáticamente según el **Cluster** (id 1–5 o palabras clave).

- **tema:** debe coincidir (mayúsculas/minúsculas ignoradas) con los valores de `cepal.topicSpa` tras normalización.
- **color:** opcional; si no hay columna color, se asigna por nombre de **CLUSTER**:

| Cluster (palabras clave) | Color |
|--------------------------|-------|
| Desarrollo económico / macroeconomía / comercio | Rojo `#c0392b` |
| Desarrollo social / grupos poblacionales | Azul `#2980b9` |
| Sostenibilidad / ambiental / recursos naturales | Verde `#27ae60` |
| Desarrollo productivo / innovación / tecnológico | Púrpura `#8e44ad` |
| Institucionalidad / gobernanza / transversal | Mostaza `#d4ac0d` |

## Si falta el archivo

Los gráficos de redes siguen funcionando; los nodos de temas se muestran en gris (`#9ca3af`) y el cluster aparece como «Sin cluster».
