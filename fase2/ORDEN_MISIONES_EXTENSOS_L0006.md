# Orden de misiones para los documentos extensos restantes de L0006

## 1. Documento 45023

1. Ejecutar `PROMPT_45023_INDICE_MAPA.md`.
2. Revisar `indice_fuente.json` y `mapa_cortes_45023.md`.
3. Crear una copia del `PROMPT_45023_PARCIAL_TEMPLATE.md` por cada bloque del mapa, sustituyendo `<BLOQUE_ID>` y el nombre de salida.
4. Ejecutar los parciales en sesiones independientes. Pueden correr en paralelo si el límite de TPM lo permite; si no, secuencialmente.
5. Ejecutar `PROMPT_45023_CONSOLIDACION.md` solo cuando todos los parciales existan.
6. Revisar humanamente y promover solo después de las cuatro validaciones limpias.

## 2. Documento 44590

1. Ejecutar `PROMPT_44590_INDICE_MAPA.md` y verificar el índice existente o regenerado.
2. Revisar `mapa_cortes_44590.md`.
3. Crear una copia del `PROMPT_44590_PARCIAL_TEMPLATE.md` por cada bloque, sustituyendo `<BLOQUE_ID>` y el nombre de salida.
4. Ejecutar los parciales en sesiones independientes.
5. Ejecutar la consolidación en dos niveles con `PROMPT_44590_CONSOLIDACION.md`.
6. Revisar humanamente y promover solo después de las cuatro validaciones limpias.

## Reglas comunes

- El índice y el mapa son secuenciales y preceden a todos los parciales.
- Cada parcial lee únicamente sus páginas asignadas.
- La consolidación puede consultar tramos para resolver dudas puntuales, pero no rehace la lectura completa sin justificación.
- No editar `pipeline.sqlite` desde estos prompts.
- No escribir en `corpus/resultados/` hasta la aprobación humana.
- Cualquier modificación posterior al JSON obliga a regenerar esquema, índice, citas y densidad.
