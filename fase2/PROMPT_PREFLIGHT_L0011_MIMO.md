# Preflight batch — L0011

Inicia una sesión limpia de MiMo/OpenCode desde
`C:\Users\abustamante\Cepal-lab\experimentos\cambio_climatico\fase2` y pega el bloque siguiente.

---

## INICIO DEL PROMPT

Realiza exclusivamente el preflight determinista de todos los documentos del manifiesto
`corpus/lotes/L0011.json`. No hagas enriquecimiento, no leas analíticamente los textos, no construyas
JSON analíticos, no ejecutes `ledger.py` y no escribas en `corpus/resultados/`.

El lote L0011 ya fue reservado en el ledger. Antes de procesar cada documento, verifica sus artefactos
locales. Si una etapa ya tiene un reporte y una fuente completa, consérvala y continúa desde la etapa
siguiente; no borres ni sobrescribas fuentes originales ni repitas descargas innecesariamente.

Para evitar límites TPM, procesa los documentos **secuencialmente**, sin abrir tareas paralelas, sin copiar
el contenido de los TXT a la conversación y sin producir explicaciones extensas por documento.

Para cada entrada del manifiesto:

1. Resuelve el handle con `pipeline/cepal_repositorio.py`.
2. Descarga primero el bundle `TEXT` como `corpus/intermedios/11362/<id>/texto.txt`.
3. Ejecuta `pipeline/preflight_endpoint_text.py` con `--report` y `--output-dir .../tramos_endpoint --pages-per-chunk 25`.
4. Si el endpoint es apto y tiene saltos de página utilizables, registra `endpoint_apto`; no descargues PDF ni uses OCR.
5. Si falla o marca que las páginas no son utilizables para citas, descarga el PDF oficial como
   `corpus/pdfs/11362_<id>.pdf` y ejecuta `pipeline/preflight_pdf.py` hacia
   `corpus/intermedios/11362/<id>/tramos/` con bloques de 25 páginas.
6. Comprueba en `preflight.json` y `manifest.json` el diagnóstico `layout`. Si se detecta `two_column`,
   conserva la extracción espacial de PyMuPDF seleccionada por el pipeline; no sustituyas sus tramos por
   una extracción lineal de mayor score. Si la compuerta de calidad falla, registra el bloqueo y no
   enriquezcas desde texto defectuoso.
7. Solo si `preflight_pdf.py` devuelve código `2`, crea una copia OCR con
   `ocrmypdf --force-ocr --deskew --language spa`, conserva el original y repite el preflight hacia
   `tramos_force_ocr/`. Nunca uses `--skip-text` para reemplazar una capa textual corrupta.
8. Escribe `PREPARACION_FUENTE.md` dentro de `corpus/intermedios/11362/<id>/` con fuente seleccionada,
   métricas, diagnóstico de layout, rutas, necesidad de muestra visual y bloqueos. No declares revisión
   visual realizada si no fue efectivamente hecha.
9. En la bitácora de cada documento registra el harness real (`MiMo/OpenCode`) y el modelo/versión que
   muestre la sesión. Si no está disponible, registra explícitamente `modelo: no registrado`; no lo infieras.

Si hay un error puntual, registra `bloqueado` para ese documento y continúa con el siguiente; no repitas
descargas ni hagas reintentos automáticos. Conserva todos los reportes reproducibles y no borres fuentes
originales ni artefactos previos.

Al finalizar responde solo con una tabla compacta que incluya: id, fuente
(`endpoint_apto`/`pdf_tramos`/`ocr_forzada`/`bloqueado`), manifest o ruta de tramos, diagnóstico de layout,
y si requiere revisión visual.

## FIN DEL PROMPT

---

El manifiesto reservado es `corpus/lotes/L0011.json` y contiene 15 documentos. La misión termina al completar
el preflight; el enriquecimiento se ejecutará después, en una misión separada.
