# 43725 - extraccion parcial A: introduccion y capitulos I-III

Trabaja en una sesion limpia, desde `fase2`. Procesa solamente 11362/43725.

Prerequisito: deben existir `indice_fuente.json` y `mapa_cortes_43725.md`. Leelos junto a `codebook_v0.md`, `esquema_json_v1.md`, `GUIA_OPERATIVA_PIPELINE.md`, `DIRECTRIZ_CALIDAD_EXPLICATIVA_v1.md` y `PREPARACION_FUENTE.md`.

Fuente unica: `corpus/intermedios/11362/43725/tramos/`. Lee secuencialmente solo el rango A registrado en el mapa: Introduccion, I. Escenarios de referencia, II. Escenarios climaticos y III. Impactos potenciales en recursos hidricos e hidroelectricidad, con todas sus subsecciones.

Crea atomica y exclusivamente `corpus/intermedios/11362/43725/parcial_capitulos_i_iii.json`.

Formato minimo:
```json
{
  "documento_parcial": {"id": "43725", "bloque": "Introduccion y capitulos I-III", "fuente": "tramos", "rango_pdf": "<rango real>"},
  "resumen_secciones": [],
  "hallazgos_candidatos": [],
  "recomendaciones_normativas": []
}
```

Conserva literalidad, jerarquia y orden. Cada dimension necesita cita literal completa y pagina PDF fisica. No uses resumen, mensajes clave, cuadros o recuadros como seccion. No inventes documento, resumen_enriquecido, tipologia ni interpelacion final. No edites manifiesto, borrador_preprueba, ledger ni resultados.

Termina con conteo de capitulos, subsecciones, dimensiones y citas.
