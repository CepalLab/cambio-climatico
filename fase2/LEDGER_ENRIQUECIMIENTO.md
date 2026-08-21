# Ledger de enriquecimiento (fase2)

Estado por documento del lote de producción. Columnas: `archivo | estado | motor`.

- `archivo`: nombre en `corpus/resultados/`.
- `estado`: `PREPRUEBA` (borrador validado por los 4 chequeos), `APROBADO` (revisión humana), `OBSERVADO`.
- `motor`: qué harness/agente generó el borrador.

---
borrador_42527.json | PREPRUEBA | opencode-agent + pipeline fase2 (crear_manifiesto_indice, validar_indice, validar_citas --strict-quality --page-source, validar_esquema, auditar_densidad --strict); sin LLM de chat
