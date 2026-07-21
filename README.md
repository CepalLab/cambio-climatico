# Explorador de publicaciones · Cambio climático CEPAL

App Streamlit para explorar y revisar el corpus de publicaciones CEPAL sobre
cambio climático. Cuatro páginas: **Explorador** de metadatos (tabla con
filtros, pills coloreados por cluster, popup de detalle), **Estadísticas**
(Sankey división↔temas, coocurrencias, barras por periodo), **Documentos para
2da fase** (ficha técnica del corpus definitivo) y **Revisión del piloto**
(fichas de los 17 casos con resumen, secciones, interpelación, tipología y
comentarios del equipo revisor).

> Proyecto del [CEPAL Lab](https://www.cepal.org/es) — laboratorio de innovación
> de la CEPAL/ILPES.

## Ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

Requiere Python ≥ 3.10.

Datos esperados en la misma carpeta que `app.py`:

- `datos_dashboard_final.xlsx` — corpus
- `clusters.xlsx` — mapeo tema → cluster (para pills coloreados; ver [CLUSTERS.md](CLUSTERS.md))

## Estructura

```text
app.py                  # entrypoint Streamlit (st.navigation)
explorador.py           # página: tabla + filtros + popup + autosave
visualizaciones.py      # página: gráficos ECharts (barras, sankey, coocurrencias)
segunda_fase.py         # página: ficha técnica del corpus definitivo (244 docs)
revision_piloto.py      # página: fichas de revisión del piloto (17 casos)
comentarios_piloto.py   # persistencia de comentarios de revisión (GitHub/local)
datos.py                # carga cacheada + colores por cluster
topic_spa.py            # parsing del campo cepal.topicSpa
seleccion.py            # persistencia (GitHub o JSON local)
graficos_echarts.py     # opciones ECharts
clusters.xlsx           # mapeo tema → cluster (opcional)
datos_dashboard_final.xlsx  # corpus
requirements.txt
.streamlit/secrets.toml.example
```

## Selección para análisis (Incluir + Nota)

La tabla muestra dos columnas accionables al inicio de cada fila:

- **`🔍 ver`** — checkbox "fantasma": al tildarse abre el popup completo del
  registro con resumen, autor/a, división, temas con pills coloreados por
  cluster, toggle Incluir y textarea **Nota del revisor**. Al cerrar el
  popup la columna se auto-resetea.
- **`Incluir`** — checkbox editable con **autosave** (cada click commitea
  inmediatamente al backend; pausa ~1-3 s según latencia de GitHub).

Ambas acciones están disponibles en la misma vista — el revisor decide
entre marcar rápido inline (✓) o abrir el detalle para revisar el resumen
y/o agregar una nota (🔍).

En el sidebar:

- **Publicaciones marcadas** — contador del backend
- **Mostrar** — Todas / Solo marcadas / Solo no marcadas
- **Descargar selección final** — CSV con los registros marcados + nota + fecha

### Persistencia

El estado se guarda en un JSON con esquema:

```json
{
  "https://hdl.handle.net/...": {
    "incluir": true,
    "nota": "...",
    "marcado_en": "2026-05-22T14:32:00"
  }
}
```

Dos backends posibles (autodetectados):

1. **GitHub** (producción / Streamlit Cloud) — si `st.secrets["github"]`
   tiene `token` y `repo`, la app lee/escribe el JSON en ese repo vía API.
   Cada guardado = 1 commit.
2. **JSON local** (fallback de desarrollo) — `seleccion_revision.json` en
   esta carpeta. No requiere configuración.

## Despliegue en Streamlit Community Cloud

1. Subir este repo a GitHub (público o privado).
2. Conectar la app en [share.streamlit.io](https://share.streamlit.io) apuntando
   al `app.py` de la raíz del repo.
3. Generar un **Personal Access Token (fine-grained)** en
   [GitHub → Settings → Developer settings → Tokens (fine-grained)](https://github.com/settings/tokens?type=beta)
   con permisos `Contents: read & write` sobre el repo destino del JSON de
   selección (puede ser el mismo repo).
4. En **App settings → Secrets** pegar:

```toml
[github]
token = "github_pat_..."
repo = "CepalLab/cambio-climatico"
path = "seleccion_revision.json"
branch = "main"
```

Ver plantilla en [`.streamlit/secrets.toml.example`](.streamlit/secrets.toml.example).

> **Nota:** el filesystem de Streamlit Cloud es efímero — sin el bloque
> `[github]` las marcas se pierden al reiniciar el container.

## Licencia y créditos

Desarrollado por el CEPAL Lab. El corpus pertenece a la
[Comisión Económica para América Latina y el Caribe (CEPAL)](https://www.cepal.org).
