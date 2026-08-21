# 45023 — parcial `<BLOQUE_ID>`

Trabaja en una sesión limpia desde `fase2`. Procesa únicamente `11362/45023` y el bloque `<BLOQUE_ID>` definido en `corpus/intermedios/11362/45023/mapa_cortes_45023.md`.

Lee `PREPARACION_FUENTE.md`, `indice_fuente.json`, `mapa_cortes_45023.md`, `codebook_v0.md`, `esquema_json_v1.md`, `GUIA_OPERATIVA_PIPELINE.md` y `DIRECTRIZ_CALIDAD_EXPLICATIVA_v1.md`.

Fuente única: `corpus/intermedios/11362/45023/tramos/`. Lee únicamente los tramos y páginas asignados a `<BLOQUE_ID>`, secuencialmente.

Crea atómicamente `corpus/intermedios/11362/45023/parcial_<BLOQUE_ID>.json` con esta estructura mínima:

```json
{
  "documento_parcial": {
    "id": "45023",
    "bloque": "<BLOQUE_ID>",
    "fuente": "tramos",
    "rango_pdf": "<rango real>"
  },
  "resumen_secciones": [],
  "hallazgos_candidatos": [],
  "recomendaciones_normativas": []
}
```

Conserva literalmente los títulos, numeración, niveles y orden del manifiesto. Cada nodo de `resumen_secciones` debe tener `seccion`, `nivel`, `paginas`, `resumen`, `dimensiones` y `subsecciones`. Cada dimensión necesita una cita literal autónoma y su página PDF física. No uses citas ni evidencia fuera del rango del bloque; no inventes tipología, interpelación ni resumen global.

No incluyas material editorial, listas de cuadros/figuras, bibliografía, anexos, encabezados repetidos ni recuadros como secciones. No modifiques otros parciales, el índice, el borrador, el ledger ni resultados.

Termina con conteo de secciones, hojas, dimensiones y citas, y confirma que todas pertenecen al rango asignado.
