# Revisión independiente de dimensiones y citas

Usa este prompt como misión separada de revisión, después del enriquecimiento y antes de promover.
No descargues fuentes, no regeneres tramos, no ejecutes `ledger.py` y no escribas en `corpus/resultados/`.

Para el documento asignado, usa exclusivamente `tramos/`, `indice_fuente.json` y
`borrador_preprueba.json`. Revisa cada dimensión con esta regla: la cita debe ser una afirmación de cuerpo
completa, aparecer en su página declarada y demostrar directamente el slug asignado; no basta con que sea
temáticamente cercana.

Marca cada entrada como `directa`, `parcial` o `no_sustenta` y registra sección, dimensión, página, cita,
veredicto y justificación breve en `matriz_revision_dimensiones_citas.json`. Rechaza rótulos de tablas,
figuras, listas, notas de fuente, URLs, encabezados, frases truncadas y evidencia reutilizada sin una razón
explícita. Si una cita no sustenta la dimensión, sustitúyela por evidencia directa, reclasifica o elimina la
dimensión; nunca inventes evidencia.

La matriz debe ser un objeto con `entradas`; cada entrada requiere `ruta_seccion`, `dimension`, `pagina`,
`veredicto` y `justificacion`. Una entrada `parcial` requiere además `decision_humana`; una entrada
`no_sustenta` bloquea promoción.

Haz revisión completa en documentos con columnas, títulos multilínea, más de 80 páginas, idioma distinto del
español, densidad extrema de citas/dimensiones o una alerta previa. Para los demás, revisa una muestra
estratificada que cubra todos los slugs y secciones de nivel 1; si aparece un fallo, escala a revisión completa.

Al terminar, ejecuta de nuevo esquema, índice, orden JSON, citas con `--strict-quality`, densidad y
`auditar_pre_promocion.py`. La promoción solo procede si no quedan entradas `no_sustenta` y cualquier entrada
`parcial` tiene decisión humana documentada. Al certificar, añade
`--review-matrix matriz_revision_dimensiones_citas.json` a `certificar_promocion.py`.
