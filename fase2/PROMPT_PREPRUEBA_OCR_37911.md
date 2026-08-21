# Preprueba de extracción con fallback OCR — 11362/37911

Inicia una sesión limpia del harness desde la raíz del repositorio y pega el bloque entre **INICIO DEL PROMPT** y **FIN DEL PROMPT**.

---

## INICIO DEL PROMPT

Realiza exclusivamente la preprueba de extracción de `https://hdl.handle.net/11362/37911`. No ejecutes `ledger.py`, no escribas en `corpus/resultados/` y no generes todavía un JSON analítico.

PDF original:

`fase2/corpus/pdfs/11362_37911.pdf`

Primero ejecuta el preflight local:

```bash
python3 fase2/pipeline/preflight_pdf.py \
  fase2/corpus/pdfs/11362_37911.pdf \
  fase2/corpus/intermedios/11362/37911/tramos_preflight
```

Si termina con código `0`, conserva `tramos_preflight/manifest.json` como fuente propuesta. Si termina con código `2`, no analices sus tramos: ejecuta OCR, sin reemplazar el original, y vuelve a probar:

```bash
ocrmypdf --language spa --force-ocr --deskew \
  fase2/corpus/pdfs/11362_37911.pdf \
  fase2/corpus/intermedios/11362/37911/fuente_force_ocr.pdf

python3 fase2/pipeline/preflight_pdf.py \
  fase2/corpus/intermedios/11362/37911/fuente_force_ocr.pdf \
  fase2/corpus/intermedios/11362/37911/tramos_force_ocr
```

Si el segundo preflight también termina con código `2`, escribe `fase2/corpus/intermedios/11362/37911/PREPRUEBA_BLOQUEADA.md` con sus resultados y detente. Si termina con código `0`, lee visualmente las páginas impresas 7, 15, 25, 40 y 80, confirma que el texto de los tramos coincide con el PDF y escribe:

`fase2/corpus/intermedios/11362/37911/resultado_preprueba_extraccion.md`

El informe debe declarar: extractor elegido, fuente propuesta, páginas del PDF, calidad reportada por el preflight, resultado de la comprobación visual y recomendación (`apto para enriquecimiento`, `requiere muestra visual` o `bloqueado`).

Al finalizar, responde solo con las rutas creadas, el código de salida de cada preflight y la recomendación. 

## FIN DEL PROMPT
