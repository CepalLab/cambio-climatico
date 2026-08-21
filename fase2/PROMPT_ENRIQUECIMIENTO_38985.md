# Enriquecimiento — 11362/38985

Inicia una sesión limpia de OpenCode desde `C:\Users\abustamante\Cepal-lab\experimentos\cambio_climatico\fase2` y pega el bloque siguiente.

---

## INICIO DEL PROMPT

Procesa exclusivamente `https://hdl.handle.net/11362/38985`, *Sostenibilidad ambiental y competitividad internacional: la huella de carbono de las exportaciones de alimentos* (`num_muestra: 9`). Es una preprueba analítica: no ejecutes `ledger.py`, no escribas en `corpus/resultados/` y no declares aprobación.

Lee `esquema_json_v1.md`, `codebook_v0.md`, `INTERPELACION_v0.md`, `TIPOLOGIA_v0.md`, `CASOS_ANCLA_INTERPELACION_v1.md`, `DIRECTRIZ_CALIDAD_EXPLICATIVA_v1.md` y `OPERACION_BATCH.md`.

## Fuente obligatoria

Usa únicamente la fuente endpoint ya validada y paginada:

`corpus/intermedios/11362/38985/tramos_endpoint/manifest.json`

Sus cuatro tramos cubren 97 páginas lógicas y 251.288 caracteres. No descargues PDF, no ejecutes OCR, no regeneres tramos y no uses otra fuente. Lee los tramos por bloques y consolida el resultado al final; no necesitas reproducir el texto fuente en tu respuesta.

## Producto

Construye:

`corpus/intermedios/11362/38985/borrador_preprueba.json`

Escribe primero el JSON completo en una ruta temporal del mismo directorio, comprueba que parsea como JSON y solo entonces muévelo atómicamente a la ruta final. Nunca dejes un JSON parcial en la ruta final si se interrumpe la sesión.

Reconstruye metadatos y secciones desde el documento. Excluye portada, índice, bibliografía, anexos, créditos y listas editoriales.

Cada dimensión debe representar un hallazgo climático/ambiental distinto. No llenes por cuota ni conviertas cada producto, país, mercado, metodología o indicador en una dimensión independiente. En especial, diferencia con precisión el objeto comercial del documento y el objetivo ambiental: aplica la regla objeto/instrumento y contrasta con el ancla de comercio-clima (`#9 Integración económica / #6 Sostenibilidad ambiental`) antes de fijar tipología.

Para citas, usa únicamente una oración o cláusula autónoma, literal y completa que aparezca en el tramo y en la página declarada. Evita encabezados, URLs, fragmentos de tablas, referencias bibliográficas y finales truncados.

Incluye interpelación y tipología justificadas contra el documento completo. Para propuestas concretas, aplica el test de `INTERPELACION_v0.md`; si no hay evidencia suficiente, deja el desglose vacío y explica el veredicto.

Ejecuta al final y guarda los reportes:

```bash
python3 pipeline/validar_esquema.py \
  corpus/intermedios/11362/38985/borrador_preprueba.json \
  > corpus/intermedios/11362/38985/validacion_esquema.txt

python3 pipeline/validar_citas.py \
  corpus/intermedios/11362/38985/borrador_preprueba.json \
  corpus/intermedios/11362/38985/tramos_endpoint/tramo_001_025.txt \
  --page-source corpus/intermedios/11362/38985/tramos_endpoint/manifest.json \
  --strict-quality \
  > corpus/intermedios/11362/38985/validacion_citas.txt

python3 pipeline/auditar_densidad.py \
  corpus/intermedios/11362/38985/borrador_preprueba.json \
  > corpus/intermedios/11362/38985/auditoria_densidad.txt
```

Corrige solo hasta que esquema y citas terminen con código `0`; la densidad es una alerta revisable, no una cuota. Al finalizar responde solo con rutas, cantidad de dimensiones, resultados de validación y confirmación de que no tocaste PDF, OCR, ledger ni resultados canónicos.

## FIN DEL PROMPT
