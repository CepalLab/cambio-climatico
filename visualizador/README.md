# Visualizador — Explorador del corpus climático CEPAL

Explorador estático (Next.js, `output: export`) del corpus de 238 publicaciones
CEPAL sobre cambio climático (2015–2026). Reemplaza a la app Streamlit, que
queda como legacy.

Diseño inspirado en [1kpapers.com](https://www.1kpapers.com/) de
[Nutlope](https://github.com/Nutlope/1kpapers) (MIT): hero con conteo,
explorar por división (= labs), temas con conteo, destacados (= trending),
línea de tiempo, benchmark de costos y relato metodológico. Todo el texto en
español. Las citas externas se sustituyen por evidencia interna (dimensiones +
citas literales verificadas).

## Estructura

- `web/` — app Next.js estática. `web/data/*.json` se genera, no se edita a mano.
- `web/public/portadas/` — thumbnails de primeras páginas (generados).
- `scripts/export_data.py` — SQLite `fase3_analitica_v1` → `web/data/`.
- `scripts/make_covers.py` — primera página de cada PDF local → JPG.

## Regenerar datos

```bash
CEPAL_DB=/tmp/fase3.sqlite python3 scripts/export_data.py
python3 scripts/make_covers.py
```

## Correr / compilar

```bash
cd web && npm install && npm run build   # sale a web/out/
```

## Decisiones (2026-09-26)

- Stack: Next.js estático. Portadas mixtas (thumbnail real + card tipográfica).
- Ranking "destacados" por evidencia interna, etiquetado honesto (cobertura, no calidad).
- Costos: placeholder hasta tener usage de proveedores con fecha.
