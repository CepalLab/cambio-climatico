# Congelamiento pre-batch v1

**Fecha de corte:** 2026-08-05  
**Alcance:** metodología y casos ancla para iniciar el procesamiento incremental del corpus climático.

## Decisiones congeladas

- Corpus definitivo: 244 publicaciones con `dc.identifier.uri` único en `documentos_definitivos_trazabilidad.csv`.
- Procesadas y aceptadas: 18 publicaciones — muestra de calibración de 17 más doc20 (`11362/37879`).
- Pendientes para producción: 226 publicaciones.
- Tipología: [TIPOLOGIA_v0.md](TIPOLOGIA_v0.md) v1.0 congelada.
- Interpelación: [INTERPELACION_v0.md](INTERPELACION_v0.md) v0.5, confirmada en Ronda 9.
- Esquema de salida: [esquema_json_v1.md](esquema_json_v1.md), incluidas las aclaraciones posteriores a Ronda 9 y la regla 6bis reforzada en Ronda 10.
- Unidad de ejecución: un documento por conversación/agente, etapas 1–5 encadenadas.

## Resultados aceptados

- Los 17 JSON canónicos de `fase2/pilot/doc*.json` constituyen la muestra cerrada.
- `fase2/corpus/resultados/doc20_colombia.json` es el resultado canónico aceptado de `https://hdl.handle.net/11362/37879` y se excluye de la cola pendiente.
- Doc10 queda resuelto como primaria #11 Capacidades del Estado y secundaria #6 Sostenibilidad ambiental.

## Ambigüedad tipológica

`ambiguedad_pendiente_validacion` solo se usa cuando existe una decisión humana pendiente y las categorías afectadas llevan certeza `Baja`. En este corte no quedan casos tipológicos pendientes.

- Doc13 queda resuelto como #9 Integración económica / #6 Sostenibilidad ambiental.
- Doc17 queda resuelto como #10 Macroeconomía y fiscalidad / #6 Sostenibilidad ambiental.

Ambos se incorporan como anclas fronterizas. Las alternativas descartadas permanecen dentro del razonamiento de cinco pasos para preservar la lógica de desambiguación, sin presentarse como pendientes.

## Control de cambios

Cada lote debe registrar esta versión de congelamiento. Una regla nueva motivada por dos o más casos detiene la admisión del lote, se adjudica, genera una versión nueva y luego se aplica de manera explícita. Las correcciones puntuales no alteran la metodología congelada.

## Control previo al lote 1

- Auditoría manual de dimensiones de doc08, doc14 y doc17: completada, con correcciones solo cuando existía cita verificable y descarte documentado de falsos positivos.
- Ledger operativo implementado en `pipeline/ledger.py`, con lotes, leases, checkpoints, reintentos, revisión, costos y exportaciones legibles; ver `OPERACION_BATCH.md`.
