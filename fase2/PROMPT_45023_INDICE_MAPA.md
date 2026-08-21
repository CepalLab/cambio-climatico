# 45023 — índice jerárquico y mapa de cortes

Trabaja en una sesión limpia desde `fase2`. Procesa únicamente `11362/45023`.

Fuente única: `corpus/intermedios/11362/45023/tramos/`. No uses `texto.txt` como fuente de citas, no descargues fuentes, no uses OCR, no edites el ledger ni escribas en `corpus/resultados/`.

Lee `PREPARACION_FUENTE.md`, `tramos/manifest.json` y los tramos necesarios para verificar el índice y el inicio real de cada capítulo.

Ejecuta y revisa:

```bash
python3 fase2/pipeline/crear_manifiesto_indice.py \
  fase2/corpus/intermedios/11362/45023/tramos \
  --output fase2/corpus/intermedios/11362/45023/indice_fuente.json
```

El manifiesto debe conservar literalmente títulos, numeración, niveles y orden de toda la jerarquía sustantiva. Excluye resumen ejecutivo, abstracts, prólogos, abreviaturas, bibliografía, anexos, índices de cuadros/figuras, cuadros, gráficos, mapas, recuadros y encabezados repetidos.

Después crea `corpus/intermedios/11362/45023/mapa_cortes_45023.md`. Divide el documento en bloques contiguos de aproximadamente 40–75 páginas, respetando límites de capítulos y sin partir una sección padre de forma arbitraria. El mapa debe incluir por bloque: identificador, rango PDF físico, primer y último título literal, capítulos incluidos y tramos que debe leer.

Usa entre 4 y 7 bloques según la jerarquía real. Si una sección extensa supera un bloque, córtala únicamente en un límite de subsección y decláralo explícitamente.

No construyas `borrador_preprueba.json`, parciales, tipología ni interpelación en esta sesión. Termina informando las rutas creadas y la tabla de cortes confirmados.
