# Misión de consolidación — documento 11362/80595

Usa obligatoriamente el modelo `gpt-5.6-luna` con `-c model_reasoning_effort=xhigh`. Trabaja solo en `/mnt/c/Users/abustamante/Cepal-lab/experimentos/cambio_climatico/fase2` y procesa exclusivamente el documento `11362/80595`. No proceses otros IDs, no descargues ni regeneres fuentes, no uses `texto.txt`, no uses `corpus/resultados/`, no ejecutes ni modifiques `ledger.py` y no promociones.

## Objetivo

Consolidar los cuatro parciales contiguos en `corpus/intermedios/11362/80595/borrador_preprueba.json`, escrito atómicamente. El índice canónico ya está fijado en `corpus/intermedios/11362/80595/indice_fuente.json`; no lo edites. La fuente exclusiva es `corpus/intermedios/11362/80595/tramos/`, y toda verificación de citas debe volver a esa fuente.

Antes de actuar, lee completamente `codebook_v0.md`, `esquema_json_v1.md`, `GUIA_OPERATIVA_PIPELINE.md`, `OPERACION_BATCH.md`, `DIRECTRIZ_CALIDAD_EXPLICATIVA_v1.md`, `INTERPELACION_v0.md`, `big_push.md`, `CASOS_ANCLA_INTERPELACION_v1.md`, `TIPOLOGIA_v0.md`, `PROMPT_ENRIQUECIMIENTO_UNIDAD.md`, `corpus/intermedios/11362/80595/PREPARACION_FUENTE.md` y `PROMPT_REVISION_DIMENSIONES_CITAS.md`. Lee también el índice y los cuatro parciales:

- `corpus/intermedios/11362/80595/parcial_001_026.json`
- `corpus/intermedios/11362/80595/parcial_027_071.json`
- `corpus/intermedios/11362/80595/parcial_072_110.json`
- `corpus/intermedios/11362/80595/parcial_111_122.json`

Haz spot-check de citas dudosas y del cierre directamente en los tramos, siempre usando marcadores `=== PÁGINA PDF N ===`. La página de cada cita debe ser el número N del marcador de fuente, nunca el folio interno impreso.

## Estructura obligatoria

Respeta exactamente el orden de claves y la forma exigidos por `esquema_json_v1.md` y por los validadores. El borrador debe incluir, como mínimo, los bloques canónicos `documento`, `resumen_enriquecido`, `resumen_secciones`, `interpelacion` y `tipologia`, con todos los campos obligatorios. Incluye obligatoriamente:

- `resumen_enriquecido.pregunta_investigacion`, en forma interrogativa;
- alcance, hallazgos, conclusiones y recomendaciones diferenciadas;
- resumen narrativo específico de 3–5 oraciones;
- citas literales completas, sin elipsis, y páginas verificables;
- interpelación completa, con veredictos, justificaciones, evidencia y chequeo negativo explícito cuando corresponda;
- tipología completa usando únicamente el canon congelado #1–#11.

## Jerarquía y secciones

Reconstruye `resumen_secciones` a partir de `secciones_jerarquicas_incluidas` del índice, literalmente y en recorrido profundidad-primero. Deben aparecer los 123 títulos, conservando padres, niveles, orden, numeración y texto exacto; no reformules ni recortes títulos. Anida solo según los niveles literales del índice. Los rangos de páginas deben referir a marcadores PDF de los tramos, ser plausibles para el contenido, y las secciones hermanas nunca deben retroceder en página. Los padres pueden tener `dimensiones: []` cuando la evidencia se encuentra en sus hojas hijas, pero cada hoja pertinente debe conservar sus dimensiones y citas. Las hojas no climáticas pueden tener dimensiones vacías; no infles señales climáticas.

Excluye Resumen, Resumen Ejecutivo, Abstract, Executive Summary, abreviaturas/acrónimos, bibliografía, anexos, cuadros, gráficos, índices y otros front matter excluido por la guía. No inventes entradas fuera del índice. Registra `tiene_resumen_ejecutivo` exactamente como `has_executive_summary` del manifiesto (`true`).

## Dimensiones, interpelación y tipología

Aplica literalmente las reglas acumulativas de `INTERPELACION_v0.md`, `big_push.md`, `DIRECTRIZ_CALIDAD_EXPLICATIVA_v1.md` y el prompt de unidad. En particular:

- Para `gran_impulso_ambiental_concreto`, un Sí exige paquete coordinado de inversiones/políticas y además al menos un sector estratégico o dos eficiencias; medidas sectoriales sueltas son Parcial y aspiración/ausencia de propuesta es No.
- Para `oportunidades_productivas_sostenibles`, un Sí exige enumeración de sectores o actividades concretas y vínculo desarrollado con empleo, productividad o desigualdad; si falta una parte es Parcial.
- Para `articulacion_actores`, exige mecanismo nombrado dentro del ámbito de aplicación; mencionar actores o territorios sin mecanismo no basta.
- Para `como_hacerlo_concreto`, usa exclusivamente la voz normativa propia del cierre elegido, ítem por ítem. Cubre la sección de recomendaciones completa, nunca un sub-bullet aislado; usa `desglose_items` y `tally`. Casos o terceros no acreditan el criterio. Un marco global es `GENERICO` salvo instrumento, entregable, responsable, plazo o métrica identificable. Incluye chequeo negativo explícito si el veredicto es No.

En tipología usa exclusivamente `#1 Desarrollo productivo`, `#2 Reducción de la desigualdad`, `#3 Protección social`, `#4 Educación y formación profesional`, `#5 Igualdad de género`, `#6 Sostenibilidad ambiental`, `#7 Transformación digital`, `#8 Migración`, `#9 Integración económica`, `#10 Macroeconomía y fiscalidad` y `#11 Capacidades del Estado`. Justifica tensión, objeto frente al instrumento alternativo, función de la secundaria, al menos tres rasgos propios y comparación con un ancla identificada por ID y título. No inventes evidencia. Por el alcance dominante del estudio, evalúa con rigor #10 como primaria y #6 como posible secundaria, sin inflar dimensiones; si eliges otras, susténtalo textualmente. La comparación entre documentos solo puede aparecer en `validacion_anclas`.

## Metadatos y calidad

Usa el título de `PREPARACION_FUENTE.md`: `Estudio Económico de América Latina y el Caribe, 2024: trampa de bajo crecimiento, cambio climático y dinámica del empleo`; ID `11362/80595`; año 2024; 287 páginas verificadas; handle `https://hdl.handle.net/11362/80595`; y los demás metadatos que permita el esquema, sin inventar autores o identificadores. Diferencia claramente resultados descriptivos, conclusiones e instrumentos recomendados. El cierre del Capítulo IV es la base de las recomendaciones y del test de concreción; no atribuyas como recomendación propia una medida de un caso o de un tercero.

Verifica antes de escribir:

1. que el aplanado depth-first de `resumen_secciones` coincide exactamente con los 123 títulos y niveles del índice;
2. que cada cita es literal completa y que su `pagina` existe en la fuente seleccionada;
3. que no se mezclan folios internos con páginas PDF;
4. que no hay dimensiones con evidencia insuficiente;
5. que no se alteran `indice_fuente.json` ni los parciales.

Escribe solo `borrador_preprueba.json` de forma atómica. No escribas los reportes finales ni el registro global. Al terminar, informa únicamente el tamaño del JSON, el recuento de secciones y las comprobaciones realizadas.
