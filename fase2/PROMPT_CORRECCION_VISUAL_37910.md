# Corrección visual final — 11362/37910

Inicia una sesión limpia del harness desde la raíz del repositorio y pega el bloque entre **INICIO DEL PROMPT** y **FIN DEL PROMPT**.

---

## INICIO DEL PROMPT

Corrige exclusivamente el análisis de `https://hdl.handle.net/11362/37910`, **Financiamiento para el cambio climático en América Latina en 2013**. Esta es una preprueba final: no ejecutes `ledger.py` ni escribas en `fase2/corpus/resultados/`.

La prueba visual ya fue aprobada en `fase2/corpus/intermedios/11362/37910/evidencia_visual_muestra.json`. El preflight local confirma que las extracciones automáticas de este PDF no son fuente fiable. Lee visualmente el PDF, no el TXT de DSpace ni los tramos OCR, para interpretar y citar:

`fase2/corpus/pdfs/11362_37910.pdf`

Lee antes `fase2/esquema_json_v1.md`, `fase2/codebook_v0.md`, `fase2/INTERPELACION_v0.md`, `fase2/TIPOLOGIA_v0.md`, `fase2/CASOS_ANCLA_INTERPELACION_v1.md` y `fase2/OPERACION_BATCH.md`.

Usa como punto de partida el contenido analítico de `fase2/corpus/intermedios/11362/37910/borrador_prueba_nativo.json`, pero no reutilices sus citas ni errores OCR. Conserva el alcance de páginas y capítulos del mapa existente solo si coinciden con la lectura visual.

## Producto

Escribe únicamente:

`fase2/corpus/intermedios/11362/37910/borrador_preprueba_visual.json`

Condiciones obligatorias:

1. Cada cita debe ser una oración o cláusula autónoma, visualmente transcrita del PDF, con página **impresa** correcta, tildes y puntuación; no uses encabezados, tablas, URLs ni frases cortadas.
2. Corrige toda prosa analítica a español natural y preciso. No conserves errores OCR ni razonamientos defectuosos del borrador previo.
3. Mantén entre 25 y 35 dimensiones analíticamente distintas, solo en secciones hoja. No introduzcas dimensiones por cuota ni dupliques evidencias.
4. La tipología debe ser primaria **10. Macroeconomía y fiscalidad** y secundaria **6. Sostenibilidad ambiental**: el objeto central es la cuantificación y estructura del financiamiento; lo ambiental es finalidad sectorial. Reescribe los cinco campos de razonamiento de manera coherente.
5. Interpelación: justifica cada veredicto con evidencia limpia; deja vacío el desglose de `como_hacerlo_concreto` si no hay acciones normativas concretas.
6. No afirmes que una cita fue validada automáticamente contra los tramos OCR.

Ejecuta y guarda:

```bash
python3 fase2/pipeline/validar_esquema.py \
  fase2/corpus/intermedios/11362/37910/borrador_preprueba_visual.json \
  > fase2/corpus/intermedios/11362/37910/validacion_esquema_visual.txt

python3 fase2/pipeline/validar_citas.py \
  fase2/corpus/intermedios/11362/37910/borrador_preprueba_visual.json \
  --quality-only \
  --strict-quality \
  > fase2/corpus/intermedios/11362/37910/validacion_calidad_citas_visual.txt

python3 fase2/pipeline/auditar_densidad.py \
  fase2/corpus/intermedios/11362/37910/borrador_preprueba_visual.json \
  > fase2/corpus/intermedios/11362/37910/auditoria_densidad_visual.txt
```

El segundo comando es un control de formato de citas, no de literalidad integral, porque esa evidencia se verifica visualmente en el PDF. Corrige hasta que los tres comandos terminen con código 0.

Al finalizar, responde solo con rutas, conteo de dimensiones, resultado de los tres controles y confirmación de que no tocaste ledger ni resultados canónicos.

## FIN DEL PROMPT
