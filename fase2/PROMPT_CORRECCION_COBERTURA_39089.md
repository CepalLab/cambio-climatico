# Corrección de cobertura — 11362/39089

Inicia una sesión limpia de OpenCode desde `C:\Users\abustamante\Cepal-lab\experimentos\cambio_climatico\fase2` y pega el bloque siguiente.

---

## INICIO DEL PROMPT

Corrige únicamente la cobertura analítica de `11362/39089`, *The Economics of Climate Change in Central America: Summary 2012* (`num_muestra: 11`). No descargues PDF, no ejecutes OCR, no regeneres tramos, no ejecutes `ledger.py` y no escribas en `corpus/resultados/`.

El borrador actual es estructuralmente válido pero insuficiente: contiene solo 8 dimensiones en 107 páginas (`0,07/página`), una por capítulo. No hagas un pulido de reducción; realiza una ampliación selectiva de cobertura.

Lee `esquema_json_v1.md`, `codebook_v0.md`, `INTERPELACION_v0.md`, `TIPOLOGIA_v0.md`, `CASOS_ANCLA_INTERPELACION_v1.md` y `OPERACION_BATCH.md`.

Usa exclusivamente los cinco tramos endpoint ya validados:

`corpus/intermedios/11362/39089/tramos_endpoint/manifest.json`

Toma como punto de partida:

`corpus/intermedios/11362/39089/borrador_preprueba.json`

Construye un reemplazo en:

`corpus/intermedios/11362/39089/borrador_cobertura_corregida.json`

## Criterio de corrección

1. Lee los cinco tramos y cubre de modo proporcional el resumen ejecutivo, el contexto climático y cada capítulo sustantivo sobre aridez, generación hidroeléctrica, ecosistemas/valor económico y enfermedades sensibles al clima.
2. Recupera entre `25` y `38` dimensiones, pero solo cuando expresen hallazgos distintos: proyección, impacto, vulnerabilidad, costo económico, brecha, instrumento o propuesta. No uses una cuota mecánica.
3. No conviertas cada país, escenario, tabla o cifra en una dimensión. Consolida los ejemplos que expresen la misma tesis regional.
4. Reevalúa tipología e interpelación contra la cobertura completa; conserva el razonamiento existente solo si sigue siendo defendible. Aplica la regla objeto/instrumento, no el título ni una sola sección.
5. Cada cita debe ser literal, autónoma, completa y verificable en la página declarada. Evita encabezados, URLs, referencias, tablas de lectura ambigua y frases cortadas.

Ejecuta y guarda en UTF-8 los tres controles:

```bash
python3 pipeline/validar_esquema.py \
  corpus/intermedios/11362/39089/borrador_cobertura_corregida.json \
  > corpus/intermedios/11362/39089/validacion_esquema_cobertura.txt

python3 pipeline/validar_citas.py \
  corpus/intermedios/11362/39089/borrador_cobertura_corregida.json \
  corpus/intermedios/11362/39089/tramos_endpoint/tramo_001_025.txt \
  --page-source corpus/intermedios/11362/39089/tramos_endpoint/manifest.json \
  --strict-quality \
  > corpus/intermedios/11362/39089/validacion_citas_cobertura.txt

python3 pipeline/auditar_densidad.py \
  corpus/intermedios/11362/39089/borrador_cobertura_corregida.json \
  > corpus/intermedios/11362/39089/auditoria_densidad_cobertura.txt
```

Si la terminal es PowerShell, no uses su redirección predeterminada para estos reportes: usa `Out-File -Encoding utf8` o ejecútalos desde Bash/WSL. Corrige hasta que esquema y citas terminen con código `0`. Al finalizar responde solo con rutas, número de dimensiones, resultados de controles y confirmación de que no tocaste PDF, OCR, ledger ni resultados canónicos.

## FIN DEL PROMPT
