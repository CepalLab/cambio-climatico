# Prompt de reejecución controlada — 11362/37791

Pega desde **INICIO DEL PROMPT** hasta **FIN DEL PROMPT** en el harness económico, iniciado desde la raíz del repositorio.

---

## INICIO DEL PROMPT

Procesa exclusivamente el documento `https://hdl.handle.net/11362/37791`. No proceses ni alteres ningún otro documento del lote.

El intento anterior fue rechazado. Debes reconstruir el análisis desde la extracción válida existente, no limitarte a maquillar el JSON rechazado. Lee y obedece como fuentes metodológicas canónicas:

- `fase2/CONGELAMIENTO_PRE_BATCH_v1.md`
- `fase2/esquema_json_v1.md`
- `fase2/codebook_v0.md`
- `fase2/INTERPELACION_v0.md`
- `fase2/TIPOLOGIA_v0.md`
- `fase2/CASOS_ANCLA_INTERPELACION_v1.md`
- `fase2/OPERACION_BATCH.md`
- `fase2/corpus/lotes/L0001_REVISION_PRIMEROS_3.md`

### Fuentes del documento

- Texto fuente válido: `fase2/corpus/intermedios/11362/37791/texto.txt`
- PDF de respaldo: `fase2/corpus/pdfs/11362_37791.pdf`
- Registro estable en `fase2/corpus/lotes/L0001.json`: `corpus_order = 2`
- Resultado rechazado, solo para entender los fallos y nunca como fuente: `fase2/corpus/intermedios/11362/37791/rechazado_revision1.json`

### Reglas bloqueantes

1. `documento.num_muestra` debe ser `2`; el handle debe ser exacto.
2. Conserva UTF-8 real y los acentos, `ñ`, signos `¿` y `¡`. No produzcas mojibake ni caracteres de reemplazo.
3. Índice, títulos, niveles y rangos de páginas deben provenir del documento; no inventes secciones.
4. Toda cita debe ser textual y aparecer literalmente en `texto.txt`. Si no puedes encontrarla allí, no la uses.
5. Cumple el piso proporcional y los requisitos sustantivos de cada resumen de hoja. No resumas capítulos extensos en dos o tres frases genéricas.
6. Aplica interpelación y tipología desde cero con las reglas y anclas. No heredes automáticamente los veredictos del resultado rechazado.
7. No marques el documento `approved`; debe terminar en `review`.
8. Ante cualquier fallo de extracción, validación o escritura, registra el fallo en el ledger y detente. No completes vacíos por inferencia.

### Flujo obligatorio

1. Inicia el intento en el ledger. En `--model` registra un identificador inequívoco con proveedor, modelo y harness reales; sustituye el marcador del comando, no lo copies literalmente. Usa `--prompt-version reejecucion-37791-v1`:

   `python3 fase2/pipeline/ledger.py start 11362/37791 --model "PROVEEDOR/MODELO@HARNESS" --prompt-version reejecucion-37791-v1`

2. Vuelve a comprobar y registrar la extracción existente:

   `python3 fase2/pipeline/ledger.py checkpoint 11362/37791 extraction --artifact fase2/corpus/intermedios/11362/37791/texto.txt --metadata '{"source":"endpoint","reused":true}'`

3. Produce primero el borrador UTF-8 en:

   `fase2/corpus/intermedios/11362/37791/borrador_revision2.json`

4. Registra `enrichment` apuntando al borrador:

   `python3 fase2/pipeline/ledger.py checkpoint 11362/37791 enrichment --artifact fase2/corpus/intermedios/11362/37791/borrador_revision2.json`

5. Ejecuta ambas validaciones y guarda sus salidas:

   `python3 fase2/pipeline/validar_esquema.py fase2/corpus/intermedios/11362/37791/borrador_revision2.json > fase2/corpus/intermedios/11362/37791/validacion_esquema_revision2.txt`

   `python3 fase2/pipeline/validar_citas.py fase2/corpus/intermedios/11362/37791/borrador_revision2.json fase2/corpus/intermedios/11362/37791/texto.txt --pdf fase2/corpus/pdfs/11362_37791.pdf > fase2/corpus/intermedios/11362/37791/validacion_citas_revision2.txt`

   Si cualquiera termina con código distinto de cero, corrige el borrador y repite. No continúes mientras exista una observación.

6. Une ambos reportes exitosos en `fase2/corpus/intermedios/11362/37791/validacion_revision2.txt` y registra el checkpoint:

   `python3 fase2/pipeline/ledger.py checkpoint 11362/37791 validation --artifact fase2/corpus/intermedios/11362/37791/validacion_revision2.txt`

7. Solo después de ambas validaciones, copia el borrador validado a la ruta canónica exacta:

   `fase2/corpus/resultados/doc_37791.json`

8. Completa con `--review-required`:

   `python3 fase2/pipeline/ledger.py complete 11362/37791 --result fase2/corpus/resultados/doc_37791.json --review-required`

   Registra tokens y costo únicamente si el harness entrega valores reales; si no están disponibles, omite esos argumentos, nunca uses cero como marcador.

9. Responde únicamente con: ruta final, resultado de ambas validaciones, cuatro veredictos de interpelación, tipología primaria/secundaria con certeza, modelo/harness registrado y estado final del ledger.

## FIN DEL PROMPT
