# CLAUDE.md

Guía para Claude Code (claude.ai/code) cuando trabaja en este repositorio.

## Qué es esto

App Streamlit del **CEPAL Lab** para explorar el corpus de publicaciones de la
CEPAL marcadas con el tema "CAMBIO CLIMÁTICO" en `cepal.topicSpa`. Pensada para
revisión humana asistida: el usuario filtra, lee el resumen, decide si la
publicación entra al análisis y opcionalmente deja una nota.

Desplegada en Streamlit Community Cloud apuntando a `app.py` en la raíz del
repo.

## Arquitectura

Cuatro páginas conectadas por `st.navigation` en [app.py](app.py):

- **Explorador** ([explorador.py](explorador.py)) — tabla paginada con filtros,
  pills coloreados por cluster, popup de detalle por registro, autosave del
  checkbox `Incluir` y campo de nota.
- **Estadísticas** ([visualizaciones.py](visualizaciones.py)) — visualizaciones
  ECharts (barras por periodo, Sankey división↔temas, red de coocurrencias).
  Los gráficos sankey/graph se renderizan vía CDN porque la versión empaquetada
  con `streamlit-echarts` no implementa `emphasis.focus: "trajectory"`.
- **Documentos para 2da fase** ([segunda_fase.py](segunda_fase.py)) — ficha
  técnica con metodología de construcción del corpus definitivo (244 documentos).
- **Revisión del piloto** ([revision_piloto.py](revision_piloto.py)) — fichas de
  17 documentos piloto con encabezado de metadatos, pestañas de resumen,
  secciones, interpelación, tipología y comentarios.

Módulos de soporte:

- [datos.py](datos.py) — carga cacheada de `datos_dashboard_final.xlsx` y
  `clusters.xlsx`, asignación de colores por cluster, helpers de filtrado.
- [topic_spa.py](topic_spa.py) — parsing del campo `cepal.topicSpa` (puede venir
  como lista Python en texto, string separado, etc.).
- [seleccion.py](seleccion.py) — persistencia de marcas Incluir/Nota.
  **Dos backends autodetectados**: GitHub (si `st.secrets["github"]` está
  configurado) o JSON local de fallback. Cada `actualizar_marca` o
  `aplicar_cambios_lote` = 1 commit al repo.
- [comentarios_piloto.py](comentarios_piloto.py) — persistencia de comentarios
  del equipo revisor para la página de piloto (backend GitHub o JSON local).
- [graficos_echarts.py](graficos_echarts.py) — construcción de opciones ECharts.

## Documentación de proceso

Además de este archivo, hay documentación de proceso que registra decisiones y metodología (no
código):

- [CLUSTERS.md](CLUSTERS.md) — mapeo tema → cluster usado por `clusters.xlsx`.
- [SEGUNDA_FASE.md](SEGUNDA_FASE.md) y [DOCUMENTOS_EXCLUIDOS_DEFINITIVO.md](DOCUMENTOS_EXCLUIDOS_DEFINITIVO.md)
  — metodología de depuración del corpus de 244 documentos (Fase 1→2). **Desactualizados**:
  referencian funciones (`excluir_documentos`, `agregar_documentos`) que ya no existen tras el
  refactor de `datos.py`/`segunda_fase.py`; usar `segunda_fase.py` como fuente de verdad del
  proceso actual.
- [fase2/](fase2/) — carpeta con el trabajo de Fase 2 (análisis estructurado a nivel de fragmento):
  [fase2/README.md](fase2/README.md) (revisión crítica de la nota conceptual e intercambio con el
  equipo del curso), [fase2/codebook_v0.md](fase2/codebook_v0.md) (propuesta de codificación) y
  [fase2/muestra_calibracion.csv](fase2/muestra_calibracion.csv) (14 documentos para calibrar el
  codebook antes de escalar a los 244).

## Datos esperados

En la raíz del repo (mismo nivel que `app.py`):

- `datos_dashboard_final.xlsx` — corpus principal (columnas estilo Dublin Core:
  `dc.title`, `dc.description.abstract`, `cepal.topicSpa`, `dc.identifier.uri`,
  `dc.year`, `division`, etc.). **~3.6 MB**, OK para GitHub.
- `clusters.xlsx` — mapeo tema → cluster (1ª col tema, 3ª col cluster). Si
  falta, los pills se muestran en gris. Ver [CLUSTERS.md](CLUSTERS.md).

El campo clave para identificar registros es `dc.identifier.uri` (handle único
por publicación, sirve de PK para la selección).

## Cómo correr

```bash
pip install -r requirements.txt
streamlit run app.py
```

Sin configurar secrets, la selección se guarda en `seleccion_revision.json`
local (ignorado por git para no contaminar el repo con marcas de prueba).

## Despliegue en Streamlit Community Cloud

1. Repo en GitHub con `app.py` en la raíz.
2. Conectar en [share.streamlit.io](https://share.streamlit.io) apuntando a `app.py`.
3. **App settings → Secrets**, pegar el bloque `[github]` (ver
   [.streamlit/secrets.toml.example](.streamlit/secrets.toml.example)) con un
   PAT fine-grained con permiso `Contents: read & write` sobre el repo donde
   se versiona el JSON de selección.

> Sin secrets, el filesystem de Streamlit Cloud es **efímero** — las marcas
> se pierden al reiniciar el container.

## Convenciones y decisiones

- **Cache**: `cargar_datos` y `cargar_mapa_clusters` usan `@st.cache_data` con
  `_mtime` como parámetro para invalidar cuando cambia el Excel.
- **`seleccion.py` no debe importar fuera del paquete**: usa solo stdlib +
  `streamlit` + `PyGithub` (importado perezosamente para no romper si falta).
- **Filtros del sidebar**: el orden global se aplica antes de paginar.
- **Autosave**: cambios en el checkbox `Incluir` se persisten en cada rerun
  (1 commit por click si el backend es GitHub).
- **Notas**: solo editables desde el popup 🔍, nunca se sobreescriben en
  operaciones bulk (`aplicar_cambios_lote` conserva la nota previa).
- **Pills**: HTML inyectado con `unsafe_allow_html=True`; el `ListColumn` de
  Streamlit no permite colorear por valor.

## Cosas que NO hacer

- No mover `app.py` a subcarpetas — Streamlit Cloud espera ese path.
- No commitear `seleccion_revision.json` con marcas reales — el archivo está
  ignorado; el estado vive en el repo configurado vía secrets, no aquí.
- No agregar dependencias pesadas al [requirements.txt](requirements.txt) —
  Streamlit Cloud tiene cuotas; mantener mínimo.
- No usar `st.experimental_*` — usar las APIs estables (`st.dialog`,
  `st.data_editor`, `st.navigation`).

## Dependencias

Mínimas (ver [requirements.txt](requirements.txt)):

- `streamlit>=1.36` — `st.navigation` y `st.Page` requieren ≥1.36.
- `pandas`, `openpyxl` — lectura del Excel.
- `streamlit-echarts` — gráficos de la página de estadísticas.
- `PyGithub` — backend de persistencia (importado perezosamente en
  [seleccion.py](seleccion.py)).
- `networkx` — layout Fruchterman-Reingold para el grafo de coocurrencias.
  **Importado perezosamente** dentro de `_layout_vos` en
  [graficos_echarts.py](graficos_echarts.py) — un grep de imports top-level lo
  pierde. Si añadís más imports lazy, actualizá ambos.
