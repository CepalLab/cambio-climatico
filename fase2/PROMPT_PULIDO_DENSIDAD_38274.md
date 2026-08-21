# Pulido de densidad — 11362/38274

Inicia una sesión limpia de OpenCode desde `C:\Users\abustamante\Cepal-lab\experimentos\cambio_climatico\fase2` y pega el bloque siguiente.

---

## INICIO DEL PROMPT

Realiza únicamente un pulido editorial de densidad sobre `11362/38274`. No reproceses el PDF, no descargues nada, no ejecutes OCR, no renderices páginas y no releas los tramos completos. No ejecutes `ledger.py` ni escribas en `corpus/resultados/`.

Usa como único insumo analítico:

`corpus/intermedios/11362/38274/borrador_preprueba_p1.json`

La fuente ya fue recuperada y validada. Solo consulta, si necesitas comprobar una cita que conservarás, el manifest paginado:

`corpus/intermedios/11362/38274/tramos_texto/manifest_validador.json`

## Objetivo

Reducir las `52` dimensiones actuales en `54` páginas (`0,96/página`) a aproximadamente `25–35` hallazgos. Conserva cobertura de los cuatro trabajos del volumen, pero elimina la granularidad de inventario.

## Reglas de edición

1. Conserva tipología, interpelación, metadatos, resúmenes y estructura de secciones salvo que una dimensión eliminada obligue a un ajuste mínimo de redacción.
2. Para cada sección, conserva solo hallazgos climáticos/ambientales analíticamente distintos: mecanismo, impacto, brecha, instrumento, resultado o propuesta sustantiva.
3. Fusiona o elimina dimensiones que repitan la misma tesis con cifras, localidades, ejemplos o variables distintas. Prioriza una cita completa y representativa; nunca combines citas para crear una nueva frase.
4. Elimina contexto genérico, antecedentes repetidos, detalles metodológicos aislados, definiciones, cifras sin implicación analítica y descripciones de casos que no cambien el hallazgo.
5. Mantén citas existentes de forma literal y su página declarada. Si eliminas una dimensión, elimina también su cita; no inventes, corrijas ni reemplaces texto con OCR.
6. No hagas una nueva extracción ni una nueva clasificación del documento.

Guarda el resultado en:

`corpus/intermedios/11362/38274/borrador_pulido_densidad.json`

Ejecuta una sola vez al final:

```bash
python3 pipeline/validar_esquema.py \
  corpus/intermedios/11362/38274/borrador_pulido_densidad.json \
  > corpus/intermedios/11362/38274/validacion_esquema_pulido.txt

python3 pipeline/validar_citas.py \
  corpus/intermedios/11362/38274/borrador_pulido_densidad.json \
  corpus/intermedios/11362/38274/tramos_texto/texto_pdf_chunk_1_25.md \
  --page-source corpus/intermedios/11362/38274/tramos_texto/manifest_validador.json \
  --strict-quality \
  > corpus/intermedios/11362/38274/validacion_citas_pulido.txt

python3 pipeline/auditar_densidad.py \
  corpus/intermedios/11362/38274/borrador_pulido_densidad.json \
  > corpus/intermedios/11362/38274/auditoria_densidad_pulido.txt
```

Corrige únicamente si esquema o citas terminan con error. Al finalizar responde solo con rutas, cantidad final de dimensiones, resultados de los tres controles y confirmación de que no tocaste OCR, PDF, ledger ni resultados canónicos.

## FIN DEL PROMPT
