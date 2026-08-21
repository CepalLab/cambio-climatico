# Preflight batch — L0003

Inicia una sesión limpia de Mimo/OpenCode desde `C:\Users\abustamante\Cepal-lab\experimentos\cambio_climatico\fase2` y pega el bloque siguiente.

---

## INICIO DEL PROMPT

Realiza exclusivamente el preflight determinista de todos los documentos del manifiesto `corpus/lotes/L0003.json`. No hagas enriquecimiento, no leas analíticamente los textos, no construyas JSON analíticos, no ejecutes `ledger.py` y no escribas en `corpus/resultados/`.

Para evitar límites TPM, procesa los documentos **secuencialmente**, sin abrir tareas paralelas, sin copiar el contenido de los TXT a la conversación y sin producir explicaciones extensas por documento.

Para cada entrada del manifiesto:

1. Resuelve el handle con `pipeline/cepal_repositorio.py`.
2. Descarga primero el bundle `TEXT` como `corpus/intermedios/11362/<id>/texto.txt`.
3. Ejecuta `pipeline/preflight_endpoint_text.py` con `--report` y `--output-dir .../tramos_endpoint --pages-per-chunk 25`.
4. Si el endpoint es apto y tiene saltos de página utilizables, registra `endpoint_apto`; no descargues PDF ni uses OCR.
5. Si falla o marca que las páginas no son utilizables para citas, descarga el PDF, ejecuta `preflight_pdf.py` hacia `tramos/`; solo si devuelve `2`, aplica `ocrmypdf --force-ocr --deskew --language spa` y repite hacia `tramos_force_ocr/`.
6. Escribe `PREPARACION_FUENTE.md` dentro de `corpus/intermedios/11362/<id>/` con fuente seleccionada, métricas, rutas, necesidad de muestra visual y bloqueos.

Si hay un error puntual, registra `bloqueado` para ese documento y continúa con el siguiente; no repitas descargas ni reintentos automáticos. Al finalizar responde solo con una tabla compacta: id, fuente (`endpoint_apto`/`pdf_tramos`/`ocr_forzada`/`bloqueado`), manifest/ruta y revisión visual requerida.

## FIN DEL PROMPT
