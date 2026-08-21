# 44590 — índice jerárquico y mapa de cortes

Trabaja en una sesión limpia desde `fase2`. Procesa únicamente `11362/44590`.

Fuente única: `corpus/intermedios/11362/44590/tramos/`. No uses `texto.txt` como fuente de citas, no descargues fuentes, no uses OCR, no edites el ledger ni escribas en `corpus/resultados/`.

Lee `PREPARACION_FUENTE.md`, `tramos/manifest.json` y el `indice_fuente.json` existente si está presente. El índice existente es preliminar: verifícalo contra la fuente y regénéralo atómicamente si no cubre literalmente toda la jerarquía sustantiva.

Ejecuta, si corresponde:

```bash
python3 fase2/pipeline/crear_manifiesto_indice.py \
  fase2/corpus/intermedios/11362/44590/tramos \
  --output fase2/corpus/intermedios/11362/44590/indice_fuente.json
```

Conserva títulos, numeración, niveles y orden literal. Excluye resumen ejecutivo, prólogos, abreviaturas, bibliografía, anexos, índices de cuadros/figuras, cuadros, gráficos, mapas, recuadros y encabezados repetidos. Revisa especialmente la frontera entre capítulos sustantivos y anexos técnicos.

Crea `corpus/intermedios/11362/44590/mapa_cortes_44590.md`. Divide el documento en aproximadamente 7–10 bloques contiguos de 40–75 páginas, respetando límites de capítulos y subsecciones. Para cada bloque registra identificador, rango PDF físico, títulos inicial y final, capítulos incluidos y tramos asignados. No partas una sección padre salvo en un límite explícito de subsección.

No construyas borrador, parciales, tipología ni interpelación en esta sesión. Termina con el índice y la tabla de cortes confirmados.
