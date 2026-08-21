# Reanudación segura — 11362/38985

Inicia una sesión limpia de OpenCode desde `C:\Users\abustamante\Cepal-lab\experimentos\cambio_climatico\fase2` y pega el bloque siguiente.

---

## INICIO DEL PROMPT

Reanuda exclusivamente el enriquecimiento de `11362/38985`, *Sostenibilidad ambiental y competitividad internacional: la huella de carbono de las exportaciones de alimentos* (`num_muestra: 9`). El archivo actual `corpus/intermedios/11362/38985/borrador_preprueba.json` está truncado y no es JSON válido: no intentes repararlo ni usarlo como producto final.

No descargues PDF, no ejecutes OCR, no regeneres tramos, no ejecutes `ledger.py` y no escribas en `corpus/resultados/`.

Lee `esquema_json_v1.md`, `codebook_v0.md`, `INTERPELACION_v0.md`, `TIPOLOGIA_v0.md`, `CASOS_ANCLA_INTERPELACION_v1.md`, `DIRECTRIZ_CALIDAD_EXPLICATIVA_v1.md` y `OPERACION_BATCH.md`.

Usa exclusivamente:

`corpus/intermedios/11362/38985/tramos_endpoint/manifest.json`

Reconstruye el análisis completo desde esos cuatro tramos. El resultado debe cubrir las secciones sustantivas, usar dimensiones distintas sin convertir cada país/producto/indicador en una dimensión y aplicar la ancla comercio-clima para la tipología. Cada cita debe ser literal, autónoma y con página verificable.

Escribe el JSON completo en:

`corpus/intermedios/11362/38985/borrador_preprueba.json.tmp`

Antes de publicarlo, verifica que el temporal sea JSON válido:

```bash
python3 -m json.tool \
  corpus/intermedios/11362/38985/borrador_preprueba.json.tmp \
  > /dev/null
```

Solo si ese comando termina con código `0`, reemplaza atómicamente el archivo final:

```bash
mv corpus/intermedios/11362/38985/borrador_preprueba.json.tmp \
  corpus/intermedios/11362/38985/borrador_preprueba.json
```

Luego ejecuta `validar_esquema.py`, `validar_citas.py --strict-quality` con `tramos_endpoint/manifest.json` y `auditar_densidad.py`; guarda los tres reportes en el directorio del documento. Corrige solo hasta que esquema y citas terminen con código `0`.

Al finalizar responde solo con rutas, dimensiones, resultados de validación y confirmación de que no tocaste PDF, OCR, ledger ni resultados canónicos.

## FIN DEL PROMPT
