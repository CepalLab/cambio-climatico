# Pulido analítico OCR — 11362/37911

Inicia una sesión limpia del harness desde la raíz del repositorio y pega el bloque entre **INICIO DEL PROMPT** y **FIN DEL PROMPT**.

---

## INICIO DEL PROMPT

Realiza únicamente el pulido analítico de `11362/37911`. No ejecutes `ledger.py`, no escribas en `fase2/corpus/resultados/` y no rehagas la extracción OCR.

Usa como borrador de partida:

`fase2/corpus/intermedios/11362/37911/borrador_preprueba_ocr.json`

Usa exclusivamente la fuente paginada validada:

`fase2/corpus/intermedios/11362/37911/tramos_force_ocr/manifest.json`

Escribe el resultado en una ruta nueva:

`fase2/corpus/intermedios/11362/37911/borrador_preprueba_ocr_pulido.json`

## Correcciones obligatorias

1. Conserva la estructura sustantiva de la memoria del seminario, pero elimina dimensiones redundantes, débiles o que solo describen la agenda de una intervención. Deja aproximadamente 35–42 dimensiones distintas y sustentadas; no rellenes por cuota.
2. Sustituye toda cita que sea encabezado, título, fragmento, nota editorial o tenga ruido OCR visible. Cada cita debe ser una oración o cláusula autónoma de texto corrido, literal del tramo y verificable en su página PDF. No uses citas como `antonio prado...`, `uso de modelos...`, `conclusiones...`, `discusión...` ni frases con errores como `agricutura`, `sectoriala grícola`, `e la importancia` o números de pie de página incrustados.
3. Puedes capitalizar la primera letra y normalizar espacios de una cita si el contenido literal no cambia. Si una tilde, sigla o palabra es dudosa, selecciona otra oración limpia en vez de corregirla por inferencia.
4. Verifica los metadatos: `paginas_totales` debe reflejar las 100 páginas del PDF; no confundas el “Resumen” editorial con resumen ejecutivo. Revisa también la presencia real de anexos.
5. Conserva la tipología primaria `6. Sostenibilidad ambiental` y secundaria `11. Capacidades del Estado`, con razonamiento claro y sin referencias narrativas al proceso.
6. Interpelación: fija `gran_impulso_ambiental_concreto` en `Parcial`, pues la memoria reúne casos y acciones dispersas, no un programa regional integrado; fija `articulacion_actores` en `Parcial`, pues hay cooperación y diálogo institucional, pero no una arquitectura regional única de ejecución. Reevalúa las demás dimensiones sin atribuir al documento una voz normativa unificada donde solo hay ponencias.
7. Mantén un desglose de `como_hacerlo_concreto` solo para acciones que pasen realmente el test de concreción; ajusta tally, citas y nota para que coincidan.

Ejecuta y **guarda** los tres reportes:

```bash
python3 fase2/pipeline/validar_esquema.py \
  fase2/corpus/intermedios/11362/37911/borrador_preprueba_ocr_pulido.json \
  > fase2/corpus/intermedios/11362/37911/validacion_esquema_ocr_pulido.txt

python3 fase2/pipeline/validar_citas.py \
  fase2/corpus/intermedios/11362/37911/borrador_preprueba_ocr_pulido.json \
  fase2/corpus/intermedios/11362/37911/tramos_force_ocr/tramo_001_025.txt \
  --page-source fase2/corpus/intermedios/11362/37911/tramos_force_ocr/manifest.json \
  --strict-quality \
  > fase2/corpus/intermedios/11362/37911/validacion_citas_ocr_pulido.txt

python3 fase2/pipeline/auditar_densidad.py \
  fase2/corpus/intermedios/11362/37911/borrador_preprueba_ocr_pulido.json \
  > fase2/corpus/intermedios/11362/37911/auditoria_densidad_ocr_pulido.txt
```

Corrige hasta que esquema y citas terminen con código 0. Al finalizar, responde solo con rutas, dimensiones, resultado de controles y confirmación de que no tocaste ledger ni resultados canónicos.

## FIN DEL PROMPT
