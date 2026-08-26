# Guia de revision humana del piloto v1

## Objetivo

La revision humana no debe confirmar lo que dice la seleccion automatica. Debe
decidir si cada cita sirve para construir un hallazgo, si requiere reemplazo o
si revela una excepcion. El selector solo prioriza cobertura y senales textuales
simples; no evalua significado. El resultado es evidencia curada para M4, no
una calificacion de los documentos.

La unidad principal de revision humana sera la ficha de hallazgo `draft`, no
esta planilla. La planilla se usa como respaldo cuando se necesite comprobar,
reemplazar o ampliar una referencia concreta.

## Insumos

Para cada piloto se generan tres archivos en `salidas/`:

- `muestra_lectura_<piloto>_v1.json`: muestra y reglas de seleccion.
- `muestra_lectura_<piloto>_v1.md`: resumen de cobertura.
- `revision_humana_<piloto>_v1.csv`: planilla editable de decisiones.

Las citas llevan `source_path`, `source_sha256`, `document_id`,
`dimension_id` y pagina. El JSON canonico indicado por `source_path` es la
fuente de contexto; la pagina y cita permiten volver al texto original cuando
sea necesario.

## Procedimiento por fila

1. Leer la cita y su seccion; abrir el JSON canonico cuando falte contexto.
   En filas `interpellation_contrast`, leer tambien `interpellation_evidence`:
   es el razonamiento metodologico del veredicto, no una cita literal.
2. Confirmar que la cita es literal y que la pagina es coherente.
3. Evaluar su relevancia para la pregunta y el estrato indicado.
4. Registrar una accion en la planilla:
   - `keep`: evidencia util para un posible hallazgo;
   - `replace`: la celda necesita otra cita; explicar que falta;
   - `exception`: la cita matiza o contradice un patron posible;
   - `exclude`: no es pertinente para este piloto;
   - `needs_context`: no alcanza con la cita; indicar que seccion o pasaje se debe leer.
5. Escribir una nota concreta: que demuestra la evidencia, que no demuestra y
   que cita alternativa o contexto se necesita.

## Como completar la planilla CSV

- `literal_verified`: `yes`, `no` o `not_checked`.
- `relevance`: `high`, `medium`, `low` o `none`.
- `recommended_action`: uno de los cinco valores del procedimiento.
- `reviewer_note`: razonamiento breve y verificable.
- `reviewer` y `reviewed_at`: identidad de quien revisa y fecha ISO.

No modificar `document_id`, `dimension_id`, pagina, cita, ruta ni hash. Si
una referencia es incorrecta, marcarla y documentar el problema en vez de
editarla en la planilla.

## Criterio de salida de M4

Un piloto esta listo para revision humana cuando existan entre 5 y 8 fichas de
hallazgo `draft` con metricas, evidencia y excepciones. La revision decide si
cada ficha se mantiene, ajusta, divide, fusiona o descarta. La planilla se
consulta solo cuando una ficha requiere verificar, reemplazar o ampliar una
referencia.