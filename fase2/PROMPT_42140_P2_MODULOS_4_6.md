# 42140 ? extraccion parcial B: modulos IV a VI

Trabaja en una sesion limpia, desde fase2. Procesa solamente 11362/42140.

Prerequisito: deben existir indice_fuente.json y mapa_modulos_42140.md. Leelos junto a codebook_v0.md, esquema_json_v1.md, GUIA_OPERATIVA_PIPELINE.md, DIRECTRIZ_CALIDAD_EXPLICATIVA_v1.md y PREPARACION_FUENTE.md.

Fuente unica: corpus/intermedios/11362/42140/tramos/. Empieza en tramo_251_275.txt para capturar el encabezado de transicion y continua secuencialmente hasta tramo_526_534.txt. Extrae exclusivamente Modulo IV, Modulo V y Modulo VI. No reextraigas ni dupliques los modulos 1-3.

Crea atomica y exclusivamente:
corpus/intermedios/11362/42140/parcial_modulos_4_6.json

Usa exactamente el mismo formato de parcial que la fase A:
{
  "documento_parcial": {"id": "42140", "modulos": ["<titulos literales>"], "fuente": "tramos", "rango_pdf": "<rango real>"},
  "resumen_secciones": [<arbol de secciones de los modulos IV-VI>],
  "hallazgos_candidatos": [<hallazgos para consolidacion>],
  "recomendaciones_normativas": [<voz normativa propia encontrada, con cita/pagina>]
}

Reglas:
- Modulo es nivel 1 y Articulo es nivel 2; conserva los titulos literales y el orden.
- Toda cita debe ser literal, autosuficiente y usar la pagina PDF fisica del marcador === PAGINA PDF N ===.
- Excluye resumen/abstract de cada articulo, bibliografias, anexos, cuadros, graficos y catalogos como secciones.
- No redactes tipologia, interpelacion ni borrador final.
- No edites indice_fuente.json, el parcial A, ledger ni resultados.

Termina con conteo de modulos, articulos, dimensiones y citas.
