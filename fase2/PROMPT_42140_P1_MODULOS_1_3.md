# 42140 ? extraccion parcial A: modulos 1 a 3

Trabaja en una sesion limpia, desde fase2. Procesa solamente 11362/42140.

Prerequisito: deben existir indice_fuente.json y mapa_modulos_42140.md creados por la fase de indice. Leelos junto a codebook_v0.md, esquema_json_v1.md, GUIA_OPERATIVA_PIPELINE.md, DIRECTRIZ_CALIDAD_EXPLICATIVA_v1.md y PREPARACION_FUENTE.md.

Fuente unica: corpus/intermedios/11362/42140/tramos/. Lee secuencialmente desde tramo_001_025.txt hasta tramo_251_275.txt. El ultimo tramo es de solape: detente antes del encabezado literal de Modulo IV. El objetivo es cubrir solo Modulo 1, Modulo 2 y Modulo 3, incluyendo todos sus articulos.

Crea atomica y exclusivamente:
corpus/intermedios/11362/42140/parcial_modulos_1_3.json

Formato minimo del parcial:
{
  "documento_parcial": {"id": "42140", "modulos": ["<titulos literales>"], "fuente": "tramos", "rango_pdf": "<rango real>"},
  "resumen_secciones": [<arbol de secciones de los modulos 1-3>],
  "hallazgos_candidatos": [<hallazgos para consolidacion>],
  "recomendaciones_normativas": [<voz normativa propia encontrada, con cita/pagina>]
}

Reglas:
- Conserva literalidad, jerarquia y orden: Modulo es nivel 1; Articulo es nivel 2.
- Cada dimension debe tener cita literal completa y pagina PDF fisica tomada de === PAGINA PDF N ===.
- No incluyas resumen/abstract de articulos como seccion; usalos solo como contexto si es sustantivo.
- No inventes metadatos, tipologia, resumen_enriquecido ni interpelacion final.
- No edites indice_fuente.json, borrador_preprueba.json, ledger ni resultados.
- Ejecuta validar_citas.py sobre el parcial si el formato lo permite; de no ser compatible, deja todas las citas listas para que la consolidacion las valide contra tramos.

Termina con conteo de modulos, articulos, dimensiones y citas.
