# Entorno local de PDF y OCR

El pipeline compara primero `pypdf`, PyMuPDF y `pdfplumber` mediante `pipeline/preflight_pdf.py`. PyMuPDF se extrae mediante bloques espaciales (`pipeline/layout_extraction.py`), no con texto lineal: esto evita entrelazar renglones de documentos de dos columnas. Solo cuando ninguna extracción es utilizable se activa el fallback de sistema: Poppler para texto y renderizado, y OCRmyPDF/Tesseract en español para PDF escaneado o con fuentes codificadas.

## Instalación (Ubuntu/WSL)

Ejecutar una vez desde la raíz del repositorio, en una terminal con permisos `sudo`:

```bash
bash fase2/pipeline/instalar_entorno_pdf.sh
```

El script instala `poppler-utils`, `qpdf`, `tesseract-ocr`, `tesseract-ocr-spa` y `ocrmypdf`, y confirma que el idioma `spa` esté disponible.

## Uso operativo

1. Ejecutar `preflight_pdf.py` para cada PDF antes del enriquecimiento.
2. Si retorna `0`, usar el `manifest.json` y los tramos generados.
3. Si retorna `2`, generar una versión OCR con el original como insumo, conservarla en `corpus/intermedios/<handle>/` y volver a correr el preflight sobre ese PDF.
4. Si OCR no alcanza calidad utilizable, hacer una muestra visual de diez páginas antes de pedir análisis al modelo.

## Detección de documentos en dos columnas

`preflight_pdf.py` inspecciona los bloques de texto de cada página PyMuPDF. Una página se marca como
`two_column` cuando contiene bloques de cuerpo a ambos lados del eje central; el documento se marca como
`two_column` cuando más del 50% de sus páginas cumplen esa condición. El diagnóstico queda en `preflight.json`
y en `manifest.json`, con `two_column_pages`, `two_column_ratio` y el método de detección.

Cuando se detecta al menos una página de dos columnas, la salida PyMuPDF layout-aware tiene prioridad aunque
`pypdf` obtenga un score numérico mayor. Esto incluye documentos `mixed`: una sola página crítica puede
entrelazar encabezados, evidencias y listas. El orden de lectura es encabezados, columna izquierda, columna derecha y pies; los bloques de
ancho completo se conservan en su posición vertical. `preparar_tramos_pdf.py` usa el mismo extractor compartido.

No se debe enriquecer desde un TXT o tramo que no tenga `layout` y `extractor` acreditados en su manifiesto.
La validación literal de una cita no compensa una fuente espacialmente entrelazada: si el diagnóstico muestra
`two_column` o `mixed`, revisar el orden de lectura antes de generar el índice y el borrador.

```bash
python3 fase2/pipeline/preflight_pdf.py \
  fase2/corpus/pdfs/11362_XXXXX.pdf \
  fase2/corpus/intermedios/11362/XXXXX/tramos

ocrmypdf --language spa --force-ocr --deskew \
  fase2/corpus/pdfs/11362_XXXXX.pdf \
  fase2/corpus/intermedios/11362/XXXXX/fuente_ocr.pdf
```

`--skip-text` solo corresponde a PDF escaneado sin capa textual. Si el preflight detecta texto codificado, cifrado o ilegible, usar `--force-ocr` para reemplazar esa capa. Nunca reemplazar el PDF original ni usar OCR como prueba de una cita sin una comprobación visual cuando el documento presente codificación o maquetación problemática.
