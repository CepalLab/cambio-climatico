# Pulido final visual — 11362/37910

Inicia una sesión limpia del harness desde la raíz del repositorio y pega el bloque entre **INICIO DEL PROMPT** y **FIN DEL PROMPT**.

---

## INICIO DEL PROMPT

Realiza únicamente el pulido final de `11362/37910`. No ejecutes `ledger.py`, no escribas en `fase2/corpus/resultados/` y no cambies la estructura, capítulos, alcance ni las 31 dimensiones del borrador actual:

`fase2/corpus/intermedios/11362/37910/borrador_preprueba_visual.json`

Escribe el resultado en una ruta nueva:

`fase2/corpus/intermedios/11362/37910/borrador_preprueba_visual_pulido.json`

La fuente para cada cita es únicamente la lectura visual del PDF:

`fase2/corpus/pdfs/11362_37910.pdf`

## Correcciones obligatorias

1. Relee visualmente **cada una de las 34 citas** y reemplázala por una transcripción literal, completa y con la página impresa correcta. No parafrasees: conserva las palabras del PDF, tildes, cifras y términos técnicos. En particular, verifica las citas sobre el BIRF, los BPD, los fondos climáticos y los fondos de pensiones.
2. Corrige toda la prosa analítica sin cambiar sus afirmaciones ni agregar contenido. Deben desaparecer, entre otros, `banca iniciada`, `medición de y de inventario`, `las compromisos`, `flujos de alquiler`, `coordinación de bogos`, `opacidad de los magnitudes`, `casos de la del canal` y `autor financiero`.
3. Reescribe con español claro los cinco campos de `razonamiento_5_pasos`, manteniendo la clasificación primaria `10. Macroeconomía y fiscalidad` y secundaria `6. Sostenibilidad ambiental`.
4. Conserva los veredictos de interpelación (`No`, `Parcial`, `Parcial`, `No`), pero limpia su evidencia y notas. No conviertas el documento de inventario en una propuesta normativa.
5. No modifiques `evidencia_visual_muestra.json`, tramos OCR, mapas, resultados canónicos ni el ledger.

Ejecuta y guarda:

```bash
python3 fase2/pipeline/validar_esquema.py \
  fase2/corpus/intermedios/11362/37910/borrador_preprueba_visual_pulido.json \
  > fase2/corpus/intermedios/11362/37910/validacion_esquema_visual_pulido.txt

python3 fase2/pipeline/validar_citas.py \
  fase2/corpus/intermedios/11362/37910/borrador_preprueba_visual_pulido.json \
  --quality-only --strict-quality \
  > fase2/corpus/intermedios/11362/37910/validacion_calidad_citas_visual_pulido.txt

python3 fase2/pipeline/auditar_densidad.py \
  fase2/corpus/intermedios/11362/37910/borrador_preprueba_visual_pulido.json \
  > fase2/corpus/intermedios/11362/37910/auditoria_densidad_visual_pulido.txt
```

Corrige hasta que los tres comandos terminen con código 0. Al finalizar, responde solo con rutas, conteo de dimensiones, resultado de controles y confirmación de que no tocaste ledger ni resultados canónicos.

## FIN DEL PROMPT
