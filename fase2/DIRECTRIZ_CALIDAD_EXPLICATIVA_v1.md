# Directriz de calidad explicativa para modelos

Esta directriz controla la riqueza de la explicación, no la cantidad de dimensiones. Aplica a cualquier modelo u harness desde el lote L0001.

1. Cada resumen de sección hoja debe explicar su función argumental, incluir al menos un dato, mecanismo, instrumento o caso específico cuando exista, y cerrar con su implicación climática o de política. No basta enumerar temas.
2. `resumen_enriquecido` debe incluir los principales hallazgos diferenciados del documento y no limitarse a tres frases genéricas si la evidencia disponible permite mayor precisión.
   - `pregunta_investigacion` es obligatoria: debe formular en una oración interrogativa el problema explícito o implícito que el documento busca resolver; no se omite aunque el título o la introducción ya lo sugieran.
3. El razonamiento tipológico de cinco pasos debe anclarse en el método, los hallazgos de cierre y al menos dos rasgos propios del documento; no admite frases intercambiables entre publicaciones.
   - `tension_dialectica`: mínimo dos oraciones que expresen la contradicción estructural y cómo el documento la procesa.
   - `filtro_categoria_primaria`: debe contrastar explícitamente objeto versus instrumento y justificar por qué se descarta la alternativa más cercana.
   - `secundaria_obligatoria`: debe explicar qué función habilitadora, sectorial o de finalidad cumple la secundaria, no solo nombrarla.
   - `justificacion_anti_copia`: debe incorporar al menos tres elementos verificables propios del documento (método, mecanismo, caso, sector, resultado o instrumento).
   - `validacion_anclas`: debe nombrar el ancla comparada y explicar semejanza y diferencia relevantes.
4. La interpelación debe aplicar literalmente los tests de `INTERPELACION_v0.md`; evidencia genérica no acredita un mecanismo de articulación ni un ítem concreto.
5. Mayor explicación no significa más dimensiones: las dimensiones siguen representando solo hallazgos analíticamente distintos y se controlan con `auditar_densidad.py`.
6. Si el modelo genera texto breve, debe ampliar la justificación y los resúmenes con evidencia ya presente en la fuente, no inventar datos ni crear citas nuevas.
7. La directriz exige densidad argumentativa, no relleno: cada oración debe agregar una relación causal, una evidencia o una decisión de clasificación.
