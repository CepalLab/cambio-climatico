# Prueba visual acotada — 11362/37910

Inicia una sesión limpia del harness desde la raíz del repositorio y pega el bloque entre **INICIO DEL PROMPT** y **FIN DEL PROMPT**. Esta prueba decide si el modelo puede leer visualmente el PDF; no es un nuevo enriquecimiento del documento.

---

## INICIO DEL PROMPT

Realiza exclusivamente una prueba de lectura visual del PDF de `https://hdl.handle.net/11362/37910`:

`fase2/corpus/pdfs/11362_37910.pdf`

No uses el TXT de DSpace ni los tramos OCR como fuente para transcribir. No modifiques `corpus/resultados/`, `ledger.py`, `tramos_nativo/`, mapas de capítulos ni borradores analíticos.

Abre y lee visualmente las páginas **impresas** 7, 15, 25, 30, 40, 48, 62, 80, 106 y 121. La página impresa puede diferir del índice físico del PDF: confírmala por el número visible en la página, no por la posición del visor.

Para cada una, copia una oración completa de 80 a 280 caracteres de texto corrido que tenga contenido sustantivo y climático o financiero. No copies encabezados, pies, títulos, tablas, viñetas ni frases que terminen a mitad de oración. Conserva tildes, eñes, puntuación, cifras y nombres exactamente como se ven en el PDF.

Escribe este archivo:

`fase2/corpus/intermedios/11362/37910/evidencia_visual_muestra.json`

Con este formato exacto:

```json
{
  "documento": "11362/37910",
  "metodo": "lectura visual directa del PDF",
  "muestras": [
    {"pagina_impresa": 7, "cita": "..."}
  ]
}
```

Debe haber exactamente diez objetos, uno por cada página solicitada, sin páginas duplicadas. No expliques ni resumas; las citas deben ser transcripciones directas, limpias y terminar con puntuación de oración.

Ejecuta este control y guarda su salida:

```bash
python3 fase2/pipeline/validar_muestra_visual.py \
  fase2/corpus/intermedios/11362/37910/evidencia_visual_muestra.json \
  --document 11362/37910 \
  --pages 7,15,25,30,40,48,62,80,106,121 \
  > fase2/corpus/intermedios/11362/37910/validacion_evidencia_visual.txt
```

Corrige el archivo hasta que el comando termine con código 0.

Al finalizar, responde solo con las rutas de la muestra y de la validación, y las diez páginas verificadas.

## FIN DEL PROMPT
