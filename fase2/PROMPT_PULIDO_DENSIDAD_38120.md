# Pulido de densidad — 11362/38120

Inicia una sesión limpia de OpenCode desde `C:\Users\abustamante\Cepal-lab\experimentos\cambio_climatico\fase2` y pega el bloque siguiente.

---

## INICIO DEL PROMPT

Realiza únicamente un pulido editorial de densidad sobre `11362/38120`. No reproceses el PDF, no descargues nada, no ejecutes OCR, no renderices páginas y no releas los tramos completos. No ejecutes `ledger.py` ni escribas en `corpus/resultados/`.

Usa como único insumo analítico:

`corpus/intermedios/11362/38120/borrador_preprueba.json`

La fuente OCR ya fue seleccionada y validada automáticamente. Solo consulta, si necesitas comprobar una cita que conservarás, el manifest paginado:

`corpus/intermedios/11362/38120/tramos_force_ocr/manifest.json`

## Objetivo

Reducir las `63` dimensiones actuales en `74` páginas (`0,85/página`) a aproximadamente `28–38` hallazgos. Conserva los hallazgos realmente distintos sobre producción científica, colaboración, redes y brechas de adaptación; elimina la granularidad de inventario bibliométrico y metodológico.

## Reglas de edición

1. Conserva tipología, interpelación, metadatos, resúmenes y estructura de secciones salvo un ajuste mínimo imprescindible por una dimensión eliminada.
2. Elimina dimensiones de metodología, definición o descripción de datos que no aporten un hallazgo climático/ambiental sustantivo.
3. Fusiona o elimina variaciones del mismo patrón: países, subregiones, indicadores de red, listas temáticas o cifras que solo ejemplifican una misma tesis.
4. Conserva, por cada tesis, la cita existente más autónoma y representativa; nunca combines citas ni generes una frase nueva.
5. Mantén citas literales y su página declarada. Si eliminas una dimensión, elimina su cita; no inventes ni corrijas texto OCR.
6. No rehagas la extracción, la clasificación ni la interpretación del documento.

Guarda el resultado en:

`corpus/intermedios/11362/38120/borrador_pulido_densidad.json`

Ejecuta una sola vez al final:

```bash
python3 pipeline/validar_esquema.py \
  corpus/intermedios/11362/38120/borrador_pulido_densidad.json \
  > corpus/intermedios/11362/38120/validacion_esquema_pulido.txt

python3 pipeline/validar_citas.py \
  corpus/intermedios/11362/38120/borrador_pulido_densidad.json \
  corpus/intermedios/11362/38120/tramos_force_ocr/tramo_001_025.txt \
  --page-source corpus/intermedios/11362/38120/tramos_force_ocr/manifest.json \
  --strict-quality \
  > corpus/intermedios/11362/38120/validacion_citas_pulido.txt

python3 pipeline/auditar_densidad.py \
  corpus/intermedios/11362/38120/borrador_pulido_densidad.json \
  > corpus/intermedios/11362/38120/auditoria_densidad_pulido.txt
```

Corrige únicamente si esquema o citas terminan con error. Al finalizar responde solo con rutas, cantidad final de dimensiones, resultado de las tres validaciones y confirmación de que no tocaste OCR, PDF, ledger ni resultados canónicos.

## FIN DEL PROMPT
