# Operación batch de fase 2

Al cerrar una sesión, aplicar el protocolo de relevo de `ESTADO_OPERATIVO_ACTUAL.md`: consultar y exportar el
ledger, confirmar los artefactos y validaciones por documento, registrar el cierre del lote, documentar issues
estructurales y dejar el comando exacto para la siguiente misión.

El ledger operativo mantiene el estado de ejecución de las 244 publicaciones sin sustituir los productos analíticos. SQLite registra estados, lotes, intentos, checkpoints, errores y costos; los JSON de `corpus/resultados/json/` siguen siendo la fuente canónica del análisis.

## Estrategia de ejecucion por extension

Gemini-3-Flash-Preview se reserva para documentos cortos o medianos (hasta aproximadamente 70-80 paginas de cuerpo). En documentos mayores no se ejecuta una corrida unica: se genera primero el manifiesto de indice, se divide por bloques contiguos y se consolidan los parciales despues. Los bloques independientes pueden correr en paralelo.

Para documentos tecnicos o de mas de aproximadamente 130 paginas, la consolidacion y cualquier correccion final deben ejecutarse con un modelo mas robusto. La revision debe verificar en particular titulos de nivel 2 o superiores, orden de secciones y paginas de citas: son los errores mas frecuentes en documentos extensos.

## Estructura

| Ruta | Función | Git |
| --- | --- | --- |
| `pipeline/ledger.py` | CLI y transiciones operativas | Versionado |
| `pipeline/ledger_schema.sql` | Esquema reproducible de SQLite | Versionado |
| `estado/pipeline.sqlite` | Estado vivo local | Ignorado |
| `estado/snapshots/` | Exportaciones CSV/JSON legibles | Versionable si se decide conservarlas |
| `corpus/lotes/L####.json` | Manifiesto inmutable de cada lote | Versionado |
| `corpus/intermedios/` | Artefactos recuperables por etapa | Ignorado |
| `corpus/resultados/json/` | JSON analíticos canónicos | Versionado |
| `corpus/resultados/certificados/` | Certificados de promoción disponibles | Versionado |
| `corpus/resultados/archivo/` | Borradores y artefactos no canónicos | Versionado si corresponde |

## Estados

```text
pending → queued → in_progress → processed → approved
                         ├──────→ review → approved
                         └──────→ error_retryable → queued/in_progress
                                           └──────→ error
```

Las etapas recuperables son `acquisition`, `extraction`, `enrichment`, `validation` y `review`. Un checkpoint conserva la etapa y la ruta del artefacto; no almacena el contenido analítico dentro de SQLite.

## Inicio

La inicialización es idempotente: reconcilia el CSV definitivo, detecta los 17 pilotos y los resultados de producción ya aceptados, y no duplica documentos.

```bash
python3 fase2/pipeline/ledger.py init
python3 fase2/pipeline/ledger.py status
```

Con el corte actual debe informar 244 documentos, 18 aprobados y 226 pendientes.

## Cola viva y prevención de reprocesamiento

`corpus/lotes/L####.json` es un manifiesto histórico e inmutable del lote: no refleja las aprobaciones posteriores y nunca debe usarse como cola actual. El estado vivo se consulta exclusivamente en el ledger.

Antes de asignar un documento, ejecutar:

```bash
python fase2/pipeline/ledger.py resume --batch L0003
python fase2/pipeline/ledger.py status --json
```

Solo se asignan documentos en estado `queued` o `error_retryable`. `start` bloquea los documentos aprobados y los handles que ya tienen un resultado canónico. Si hay una discrepancia entre el ledger y los resultados canónicos, ejecutar `ledger.py init` para reconciliarlos antes de continuar.

## Crear y ejecutar un lote

Se recomienda reservar 15–20 publicaciones, pero procesarlas con concurrencia acotada. El manifiesto fija orden, handles y versión metodológica.

```bash
python3 fase2/pipeline/ledger.py next-batch --size 20 --name lote-01
python3 fase2/pipeline/ledger.py start 11362/XXXXX \
  --model MODELO --prompt-version pre-batch-v1
python3 fase2/pipeline/ledger.py checkpoint 11362/XXXXX acquisition \
  --artifact fase2/corpus/pdfs/XXXXX.pdf
python3 fase2/pipeline/ledger.py checkpoint 11362/XXXXX extraction \
  --artifact fase2/corpus/intermedios/XXXXX/texto.txt \
  --metadata '{"source":"endpoint"}'
python3 fase2/pipeline/ledger.py checkpoint 11362/XXXXX enrichment \
  --artifact fase2/corpus/intermedios/XXXXX/borrador.json
python3 fase2/pipeline/crear_manifiesto_indice.py \
  fase2/corpus/intermedios/11362/XXXXX/tramos \
  --output fase2/corpus/intermedios/11362/XXXXX/indice_fuente.json
python3 fase2/pipeline/validar_esquema.py \
  fase2/corpus/intermedios/XXXXX/borrador.json \
  > fase2/corpus/intermedios/XXXXX/validacion.txt
python3 fase2/pipeline/validar_orden_json.py \
  fase2/corpus/intermedios/XXXXX/borrador.json \
  > fase2/corpus/intermedios/XXXXX/reporte_validacion_orden.txt
python3 fase2/pipeline/validar_indice.py \
  fase2/corpus/intermedios/XXXXX/borrador.json \
  --indice fase2/corpus/intermedios/11362/XXXXX/indice_fuente.json \
  > fase2/corpus/intermedios/11362/XXXXX/reporte_validacion_indice.txt
python3 fase2/pipeline/validar_citas.py \
  fase2/corpus/intermedios/XXXXX/borrador.json \
  fase2/corpus/intermedios/XXXXX/texto.txt \
  --pdf fase2/corpus/pdfs/XXXXX.pdf \
  --strict-quality
python3 fase2/pipeline/auditar_densidad.py \
  fase2/corpus/intermedios/XXXXX/borrador.json
python3 fase2/pipeline/ledger.py checkpoint 11362/XXXXX validation \
  --artifact fase2/corpus/intermedios/XXXXX/validacion.txt
python3 fase2/pipeline/ledger.py complete 11362/XXXXX \
  --result fase2/corpus/resultados/json/doc_XXXXX.json --review-required
python3 fase2/pipeline/ledger.py approve 11362/XXXXX
```

`complete` exige que exista el JSON, que se llame exactamente `doc_<handle_id>.json`, que su `documento.handle` coincida con el registro y que el documento haya alcanzado el checkpoint `validation`. Los checkpoints deben registrarse en orden y todos, salvo `review`, requieren un artefacto existente. Luego el resultado queda en `processed`, o en `review` con `--review-required`; la aprobación humana se registra por separado con `approve`.

### Compuerta de ?ndice

Antes de validar o completar un documento, se genera atómicamente `indice_fuente.json` desde la fuente paginada seleccionada con `crear_manifiesto_indice.py`. `validar_indice.py documento.json --indice indice_fuente.json` es bloqueante: exige que `tiene_resumen_ejecutivo` coincida con el manifiesto, rechaza front/back matter (incluidos Resumen Ejecutivo, Executive Summary y abreviaturas/acrónimos) y compara literalmente títulos, niveles, orden y cobertura de toda la jerarquía de secciones. Solo se normalizan Unicode, espacios y saltos de línea. El validador de esquema también bloquea secciones hermanas cuyo rango de páginas retroceda. El reporte `reporte_validacion_indice.txt` es un artefacto obligatorio del checkpoint de validación.

Antes del enriquecimiento, `extraction` exige UTF-8 estricto sin caracteres de reemplazo ni mojibake, al menos 5.000 caracteres, no más de 2% de caracteres de control y, cuando `source` es `endpoint`, rechazo de respuestas cercanas al límite conocido de 100.000 caracteres. En ese último caso se lee el PDF completo; ante texto ilegible o demasiado breve se usa lectura nativa u OCR. Nunca se pide al modelo completar lo que no puede leer.

El endpoint es la primera opción por costo, pero solo después de su preflight explícito. El comando deja un reporte reproducible y devuelve `0` si el TXT es apto o `2` si se debe pasar al PDF:

```bash
python3 fase2/pipeline/preflight_endpoint_text.py \
  fase2/corpus/intermedios/11362/XXXXX/texto.txt \
  --report fase2/corpus/intermedios/11362/XXXXX/preflight_endpoint.json
```

Si es apto, el TXT es la fuente paginada solo cuando contiene marcadores de página verificables; si no los contiene, se usa para lectura económica y las citas se comprueban contra el PDF. Si no es apto, se conserva el reporte y se continúa con el preflight del PDF, sin usar el TXT en el enriquecimiento.

### Modo segmentado para documentos largos

Usar este modo si el documento tiene **100 páginas o más**, o si la extracción válida supera **250.000 caracteres**. El umbral combina extensión física y carga real de contexto: el objetivo es evitar que una lectura única pierda la pertenencia de una cita a su página o capítulo.

```bash
python3 fase2/pipeline/preparar_tramos_pdf.py \
  fase2/corpus/pdfs/XXXXX.pdf \
  fase2/corpus/intermedios/11362/XXXXX/tramos
```

El comando genera bloques de 25 páginas, con el marcador `=== PÁGINA PDF N ===`, y un `manifest.json`. La extracción usa `pipeline/layout_extraction.py`: antes de enriquecer, comprobar en el manifiesto `extractor: pymupdf` y el diagnóstico `layout`. Si el documento es `two_column`, el orden acreditado es encabezados, columna izquierda, columna derecha y pies; los bloques de ancho completo se mantienen en su franja vertical. Si falla su compuerta de calidad, usar OCR o la lectura nativa del harness antes de continuar. Para cada tramo, el agente extrae únicamente secciones y evidencia pertenecientes a esas páginas; la consolidación final conserva la página declarada y valida cada cita contra el PDF. El checkpoint `extraction` apunta a `tramos/manifest.json` y registra `{"source":"pdf_chunks","pages_per_chunk":25}`.

Cuando `pypdf` no puede leer el PDF —fuentes codificadas, escaneo o extracción vacía— el harness debe crear tramos nativos/OCR con los mismos marcadores y un `manifest.json`. La validación usa entonces `--page-source ruta/a/tramos`, en vez de `--pdf`; esa fuente paginada se convierte en la evidencia verificable. El modo `--strict-quality` bloquea citas demasiado cortas, encabezados editoriales, URLs, artefactos OCR dentro de palabras y finales que dejan la cita como una frase cortada. La coincidencia literal contra OCR no sustituye la lectura visual cuando la fuente paginada contiene esos defectos.

Antes de recurrir a OCR, ejecutar el preflight local, que compara `pypdf`, PyMuPDF y `pdfplumber`, detecta layouts de dos columnas, selecciona la extracción espacialmente correcta y genera los tramos. Si termina con código `2`, no hay fuente local fiable: se escala a lectura visual u OCR en vez de enriquecer desde texto defectuoso. Un score numérico superior de otra extracción no puede desplazar a PyMuPDF cuando la compuerta `two_column` está activa.

```bash
python3 fase2/pipeline/preflight_pdf.py \
  fase2/corpus/pdfs/XXXXX.pdf \
  fase2/corpus/intermedios/11362/XXXXX/tramos \
  --pages-per-chunk 25
```

### Separación eficiente de trabajo determinista y modelo

Para evitar sesiones largas y costosas, la descarga, el preflight, la generación de tramos, OCR y las tres validaciones se ejecutan localmente como pasos deterministas. El modelo recibe solo la fuente ya seleccionada y realiza el enriquecimiento. Las correcciones de densidad o forma se hacen sobre el JSON borrador y sus citas existentes, sin releer PDF, OCR ni todos los tramos; solo se consulta la fuente cuando se conserva o cuestiona una cita concreta. Cada documento se procesa en una sesión independiente.

Todo enriquecimiento intermedio debe dejar `EJECUCION_ENRIQUECIMIENTO.md` con harness, proveedor/modelo y versión si se conoce, prompt, fuente y correcciones posteriores. Si la versión no fue informada, se registra explícitamente como `no registrada`; nunca se infiere.

La riqueza de resúmenes, razonamiento y justificaciones se rige por `DIRECTRIZ_CALIDAD_EXPLICATIVA_v1.md`; todo prompt de enriquecimiento debe pedir su lectura explícitamente. Esa exigencia no autoriza inflar dimensiones ni citas.

El entorno opcional de Poppler, QPDF y OCRmyPDF/Tesseract en español se instala y opera conforme a `ENTORNO_PDF.md`.

Ante OCR defectuoso, se realiza primero una muestra visual de páginas representativas antes de reintentar el enriquecimiento completo. `pipeline/validar_muestra_visual.py` controla que las transcripciones requeridas estén completas, sin artefactos detectables y en las páginas impresas pedidas; la revisión humana confirma que cada una coincide visualmente con el PDF.

`auditar_densidad.py` alerta —sin bloquear por defecto— si un documento de 80+ páginas supera 0,55 dimensiones por página o queda bajo 0,12. La alerta obliga a revisión humana de cobertura: una dimensión debe representar un hallazgo analíticamente distinto, no cada dato o variación de un mismo argumento, pero tampoco omitir el contenido sustantivo de capítulos completos.

## Fallos y reanudación

Cada `start` abre un lease de 60 minutos por defecto. Los checkpoints renuevan ese lease. Si la conexión o el proceso se cae, `resume` detecta leases vencidos, cierra el intento como interrumpido y conserva el último checkpoint.

```bash
python3 fase2/pipeline/ledger.py fail 11362/XXXXX \
  --error "rate limit"
python3 fase2/pipeline/ledger.py resume --batch L0001
python3 fase2/pipeline/ledger.py retry 11362/XXXXX
python3 fase2/pipeline/ledger.py start 11362/XXXXX
```

El nuevo intento retoma el artefacto asociado a `current_stage`; no vuelve a descargar ni extraer el documento si esos checkpoints ya existen. Tras superar `max_retries` —tres por defecto— el documento queda en `error` hasta una decisión manual.

## Seguimiento y respaldo

```bash
python3 fase2/pipeline/ledger.py status --json
python3 fase2/pipeline/ledger.py export
```

`export` genera un CSV completo de documentos y un JSON agregado de estados, tokens y costos. SQLite usa WAL y transacciones `BEGIN IMMEDIATE` para impedir que dos ejecutores reserven el mismo documento.

## Reglas operativas

1. Un documento pertenece a un solo lote activo, aunque pueda reaparecer en otro lote por reintento explícito.
2. No se edita `pipeline.sqlite` a mano; toda transición pasa por la CLI para conservar el historial de eventos.
3. Cada checkpoint apunta a un artefacto escrito de forma atómica.
   Los prompts de enriquecimiento deben escribir el JSON a una ruta temporal, validar su parseo y renombrarlo solo al terminar; un corte de conexión nunca debe dejar un JSON parcial en la ruta de borrador o resultado.
4. El JSON final solo pasa a `approved` después de validación y, cuando corresponda, revisión humana. Antes de
   `complete`, ejecutar `auditar_pre_promocion.py` y `certificar_promocion.py`; copiar el certificado junto al
   resultado como `doc_<id>.validation.json`. `ledger.py complete` comprueba que el certificado sea válido y que
   su SHA-256 corresponda exactamente al JSON que se promueve.
5. Cambiar prompts, modelo o metodología no sobrescribe el intento anterior: abre uno nuevo y registra sus versiones y costos.
6. `num_muestra` usa el `corpus_order` estable del manifiesto, no la posición dentro del lote.
7. `--model` identifica proveedor, modelo y harness de forma inequívoca. Tokens y costo se informan solo cuando existen datos reales; nunca se registra `0` como marcador provisional.
8. Antes de emitir un prompt o asignar un agente, verificar el handle contra `resume --batch` y `corpus/resultados/json/`.
