# Corrección puntual de citas — 11362/47534

Inicia una sesión limpia de MiMo/OpenCode desde
`C:\Users\abustamante\Cepal-lab\experimentos\cambio_climatico\fase2` y pega el bloque siguiente.

---

## INICIO DEL PROMPT

Corrige exclusivamente el borrador de `11362/47534` (*Salud y cambio climático: metodologías y políticas públicas*).
No reproceses el documento, no descargues archivos, no ejecutes OCR, no regeneres los tramos, no ejecutes
`ledger.py` y no escribas en `corpus/resultados/`.

Lee primero:

- `corpus/intermedios/11362/47534/PREPARACION_FUENTE.md`
- `corpus/intermedios/11362/47534/borrador_preprueba.json`
- `corpus/intermedios/11362/47534/reporte_validacion_citas.txt`
- `corpus/intermedios/11362/47534/reporte_validacion_esquema.txt`
- `corpus/intermedios/11362/47534/indice_fuente.json`
- `corpus/intermedios/11362/47534/tramos/manifest.json`

Usa como evidencia únicamente los tramos paginados de
`corpus/intermedios/11362/47534/tramos/`. Consulta solo las páginas y secciones involucradas por los reportes;
no releas el documento completo.

## Objetivo y alcance

El borrador actual conserva estructura, índice y orden válidos. Corrige únicamente los defectos registrados:

1. Las **10 de 58 citas** que no aparecen literalmente en la fuente.
2. Las **11 de 58 citas** que no coinciden con su página declarada.
3. Las dos citas que el validador de esquema marca fuera del rango de su sección:
   - `Capítulo II ... / Migrantes`: cita en página 42 para una sección declarada en página 41.
   - `Capítulo V ... / A. Pasos para la formulación de propuestas`: cita en página 85 para una sección declarada en páginas 86–89.

El listado completo y canónico de rutas afectadas está en `reporte_validacion_citas.txt`; úsalo como lista de
trabajo. Una misma cita puede alimentar más de una dimensión: corrige cada ubicación afectada, no supongas que
una modificación se propaga a otra.

## Reglas de corrección

1. Parte del JSON actual y escribe un candidato nuevo en
   `corpus/intermedios/11362/47534/borrador_corregido.json`. No sobrescribas `borrador_preprueba.json`.
2. Conserva sin cambios metadatos, pregunta de investigación, resumen enriquecido, tipología, interpelación,
   jerarquía, títulos, niveles, orden, rangos de las secciones y todas las citas que ya pasaron.
3. Para cada cita defectuosa, reemplázala por una cita **literal, autónoma y completa** que aparezca en la misma
   sección sustantiva y en la página PDF declarada. Registra la página física indicada por el marcador
   `=== PÁGINA PDF N ===`.
4. Si el problema es solo de página, cambia únicamente `pagina` cuando la cita literal aparezca completa y
   pertenezca al rango de la sección. No fuerces el rango de la sección para acomodar una cita ajena.
5. Si no existe una cita literal y pertinente dentro del rango de la sección, elimina solo esa dimensión y su
   cita; no inventes, parafrasees, acortes frases ni traslades evidencia de otra sección. No elimines una
   sección ni una subsección del índice.
6. No uses encabezados, pies de página, tablas aisladas, URLs, texto con artefactos OCR ni citas que terminen
   cortadas. No introduzcas una cita con menos de 40 caracteres normalizados.
7. Escribe el JSON de manera atómica: guarda primero una ruta temporal, comprueba que puede parsearse y luego
   renómbralo a `borrador_corregido.json`.

## Validación obligatoria

Ejecuta al final, sobre el candidato, las cinco compuertas siguientes y guarda las salidas UTF-8 en las rutas
indicadas. Si cualquier compuerta falla, corrige el candidato y repite la ronda completa. No declares éxito
hasta que esquema, índice, orden y citas terminen sin observaciones ni errores.

```bash
python3 pipeline/validar_esquema.py \
  corpus/intermedios/11362/47534/borrador_corregido.json \
  > corpus/intermedios/11362/47534/reporte_correccion_esquema.txt

python3 pipeline/validar_indice.py \
  corpus/intermedios/11362/47534/borrador_corregido.json \
  --indice corpus/intermedios/11362/47534/indice_fuente.json \
  > corpus/intermedios/11362/47534/reporte_correccion_indice.txt

python3 pipeline/validar_orden_json.py \
  corpus/intermedios/11362/47534/borrador_corregido.json \
  > corpus/intermedios/11362/47534/reporte_correccion_orden.txt

python3 pipeline/validar_citas.py \
  corpus/intermedios/11362/47534/borrador_corregido.json \
  --page-source corpus/intermedios/11362/47534/tramos \
  --strict-quality \
  > corpus/intermedios/11362/47534/reporte_correccion_citas.txt

python3 pipeline/auditar_densidad.py \
  corpus/intermedios/11362/47534/borrador_corregido.json \
  > corpus/intermedios/11362/47534/reporte_correccion_densidad.txt
```

Actualiza `corpus/intermedios/11362/47534/EJECUCION_ENRIQUECIMIENTO.md` con el harness/modelo real,
la fuente usada, las rutas de corrección, el número de citas corregidas/eliminadas y los resultados de las cinco
compuertas. No promociones el documento ni alteres el ledger.

Al finalizar responde solo con: rutas creadas, número de citas corregidas y eliminadas, resultado de cada
compuerta y una confirmación de que no tocaste PDF, OCR, ledger ni resultados canónicos.

## FIN DEL PROMPT
