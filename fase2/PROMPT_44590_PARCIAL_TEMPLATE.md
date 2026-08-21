# 44590 — parcial `<BLOQUE_ID>`

Trabaja en una sesión limpia desde `fase2`. Procesa únicamente `11362/44590` y el bloque `<BLOQUE_ID>` definido en `corpus/intermedios/11362/44590/mapa_cortes_44590.md`.

Lee `PREPARACION_FUENTE.md`, `indice_fuente.json`, `mapa_cortes_44590.md`, `codebook_v0.md`, `esquema_json_v1.md`, `GUIA_OPERATIVA_PIPELINE.md` y `DIRECTRIZ_CALIDAD_EXPLICATIVA_v1.md`.

Fuente única: `corpus/intermedios/11362/44590/tramos/`. Lee únicamente los tramos y páginas asignados al bloque, secuencialmente.

Crea atómicamente `corpus/intermedios/11362/44590/parcial_<BLOQUE_ID>.json` con:

```json
{
  "documento_parcial": {
    "id": "44590",
    "bloque": "<BLOQUE_ID>",
    "fuente": "tramos",
    "rango_pdf": "<rango real>"
  },
  "resumen_secciones": [],
  "hallazgos_candidatos": [],
  "recomendaciones_normativas": []
}
```

Conserva literalmente la jerarquía del manifiesto. Cada nodo usa `seccion`, `nivel`, `paginas`, `resumen`, `dimensiones` y `subsecciones`. Cada dimensión exige una cita literal autónoma, página PDF física y evidencia perteneciente al bloque. No inventes tipología, interpelación ni conclusiones globales.

No incluyas material editorial, listas de cuadros/figuras, bibliografía, anexos, encabezados repetidos ni recuadros como secciones. No modifiques otros parciales, índice, borrador, ledger ni resultados.

Termina con conteo de secciones, hojas, dimensiones y citas, y confirma cobertura exclusiva del rango asignado.
