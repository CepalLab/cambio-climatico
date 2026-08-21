# Enriquecimiento — 11362/39009

Inicia una sesión limpia de OpenCode desde `C:\Users\abustamante\Cepal-lab\experimentos\cambio_climatico\fase2` y pega el bloque siguiente.

---

## INICIO DEL PROMPT

Procesa exclusivamente `https://hdl.handle.net/11362/39009`, *Evaluación de los impactos del cambio climático sobre la salud: economía del cambio climático en la Argentina* (`num_muestra: 10`). Es una preprueba analítica: no ejecutes `ledger.py`, no escribas en `corpus/resultados/` y no declares aprobación.

Lee `esquema_json_v1.md`, `codebook_v0.md`, `INTERPELACION_v0.md`, `TIPOLOGIA_v0.md`, `CASOS_ANCLA_INTERPELACION_v1.md`, `DIRECTRIZ_CALIDAD_EXPLICATIVA_v1.md` y `OPERACION_BATCH.md`.

## Fuente obligatoria

Usa únicamente la fuente endpoint ya validada y paginada:

`corpus/intermedios/11362/39009/tramos_endpoint/manifest.json`

Sus dos tramos cubren 48 páginas lógicas y 70.412 caracteres. No descargues PDF, no ejecutes OCR, no regeneres tramos y no uses otra fuente.

## Producto

Construye:

`corpus/intermedios/11362/39009/borrador_preprueba.json`

Reconstruye metadatos y secciones desde el documento. Excluye portada, índice, bibliografía, anexos, créditos y listas editoriales.

Cada dimensión debe representar un hallazgo climático/ambiental distinto y no cada patología, indicador, territorio, período o detalle metodológico. Distingue entre evidencia de impacto climático sobre salud, vulnerabilidad, medidas de adaptación y capacidades institucionales. Aplica la regla objeto/instrumento para tipología: no clasifiques por palabra clave ni conviertas automáticamente al Estado en objeto solo porque el informe informa decisiones públicas.

Para citas, usa únicamente una oración o cláusula autónoma, literal y completa que aparezca en el tramo y en la página declarada. Evita encabezados, URLs, fragmentos de tablas, referencias bibliográficas y finales truncados.

Incluye interpelación y tipología justificadas contra el documento completo. Para propuestas concretas, aplica el test de `INTERPELACION_v0.md`; si no hay evidencia suficiente, deja el desglose vacío y explica el veredicto.

Ejecuta al final y guarda los reportes:

```bash
python3 pipeline/validar_esquema.py \
  corpus/intermedios/11362/39009/borrador_preprueba.json \
  > corpus/intermedios/11362/39009/validacion_esquema.txt

python3 pipeline/validar_citas.py \
  corpus/intermedios/11362/39009/borrador_preprueba.json \
  corpus/intermedios/11362/39009/tramos_endpoint/tramo_001_025.txt \
  --page-source corpus/intermedios/11362/39009/tramos_endpoint/manifest.json \
  --strict-quality \
  > corpus/intermedios/11362/39009/validacion_citas.txt

python3 pipeline/auditar_densidad.py \
  corpus/intermedios/11362/39009/borrador_preprueba.json \
  > corpus/intermedios/11362/39009/auditoria_densidad.txt
```

Corrige solo hasta que esquema y citas terminen con código `0`; la densidad es una alerta revisable, no una cuota. Al finalizar responde solo con rutas, cantidad de dimensiones, resultados de validación y confirmación de que no tocaste PDF, OCR, ledger ni resultados canónicos.

## FIN DEL PROMPT
