# Enriquecimiento con OCR validado — 11362/37911

Inicia una sesión limpia del harness desde la raíz del repositorio y pega el bloque entre **INICIO DEL PROMPT** y **FIN DEL PROMPT**.

---

## INICIO DEL PROMPT

Procesa exclusivamente `https://hdl.handle.net/11362/37911`, **Agricultura y cambio climático: economía y modelación**. Es una preprueba analítica: no ejecutes `ledger.py` ni escribas en `fase2/corpus/resultados/`.

Lee `fase2/esquema_json_v1.md`, `fase2/codebook_v0.md`, `fase2/INTERPELACION_v0.md`, `fase2/TIPOLOGIA_v0.md`, `fase2/CASOS_ANCLA_INTERPELACION_v1.md` y `fase2/OPERACION_BATCH.md`.

## Fuente obligatoria

Usa solo los tramos OCR forzados y su manifest, ya revisados como aptos:

`fase2/corpus/intermedios/11362/37911/tramos_force_ocr/manifest.json`

No uses el TXT de DSpace (`texto.txt`) ni los tramos anteriores. La revisión de fuente está en `fase2/corpus/intermedios/11362/37911/REVISION_PREPRUEBA_37911.md`.

El OCR es legible, pero puede añadir ruido menor en encabezados, líneas de puntos, tablas, notas y algunas siglas. Para cada cita, usa solo texto corrido y una oración o cláusula autónoma completa que aparezca literalmente en el tramo y en la página declarada. Evita la página 67 si no es imprescindible.

## Producto

Construye:

`fase2/corpus/intermedios/11362/37911/borrador_preprueba_ocr.json`

Usa `num_muestra: 5`. Reconstruye los metadatos y la estructura desde el índice y las páginas fuente; no heredes el borrador rechazado. Excluye portada, índice, bibliografía, anexos, listas editoriales y notas de crédito.

El documento es memoria de un seminario: distingue con fidelidad las secciones y exposiciones sustantivas. No atribuyas al documento una posición normativa unificada si corresponde a intervenciones de distintos participantes. Clasifica dimensiones solo cuando la evidencia desarrolla un hallazgo climático/ambiental sustantivo; no llenes por cuota ni repitas la misma idea entre ponencias.

Incluye interpelación y tipología debidamente justificadas contra el contenido completo, no solo una intervención aislada. Si el documento contiene propuestas concretas, aplícales el test de concreción de `INTERPELACION_v0.md`; si no, deja el desglose vacío y justifica el veredicto.

Ejecuta y guarda:

```bash
python3 fase2/pipeline/validar_esquema.py \
  fase2/corpus/intermedios/11362/37911/borrador_preprueba_ocr.json \
  > fase2/corpus/intermedios/11362/37911/validacion_esquema_ocr.txt

python3 fase2/pipeline/validar_citas.py \
  fase2/corpus/intermedios/11362/37911/borrador_preprueba_ocr.json \
  fase2/corpus/intermedios/11362/37911/tramos_force_ocr/tramo_001_025.txt \
  --page-source fase2/corpus/intermedios/11362/37911/tramos_force_ocr/manifest.json \
  --strict-quality \
  > fase2/corpus/intermedios/11362/37911/validacion_citas_ocr.txt

python3 fase2/pipeline/auditar_densidad.py \
  fase2/corpus/intermedios/11362/37911/borrador_preprueba_ocr.json \
  > fase2/corpus/intermedios/11362/37911/auditoria_densidad_ocr.txt
```

Corrige hasta que esquema y citas terminen con código 0. La auditoría de densidad es una alerta revisable.

Al finalizar, responde solo con rutas, conteo de dimensiones, resultado de validaciones y confirmación de que no tocaste ledger ni resultados canónicos.

## FIN DEL PROMPT
