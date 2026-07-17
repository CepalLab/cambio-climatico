# Archivo — respaldos de calibración (Ronda 9)

Esta carpeta guarda versiones previas que ya no están en uso activo pero
se preservan por trazabilidad del proceso de calibración.

## `*.pre_ronda9.bak` (12 archivos)

Respaldos automáticos de los JSON del piloto inmediatamente antes de aplicar
la limpieza de front/back-matter de la Ronda 8 y la retropropagación del
objeto canónico `{conclusiones, recomendaciones}` de la Ronda 9. Corresponden
a los documentos de la muestra de 14+3 que tenían conclusiones extraídas.

Si en el futuro cambia el esquema canónico de nuevo, estos respaldos permiten
reconstruir el estado "pre-Ronda 9" de cada documento sin tener que re-extraer
desde cero.

## `doc09_multiversion/` (5 variantes)

Cinco versiones del doc09 ("Building a climate resilient power sector…")
generadas por distintos agentes o configuraciones durante la calibración
de la Ronda 5 (portabilidad). Se preservan porque:

- **doc09_01** — primera extracción (agente por defecto)
- **doc09_02** — segunda extracción con prompt ajustado
- **doc09_03** — versión con interpelación aplicada
- **doc09_04** — cuarta variante, revisor ciego
- **doc09_05** — quinta variante, ajuste final

La versión canónica vigente es `fase2/pilot/doc09_caribbean_power.json`.
