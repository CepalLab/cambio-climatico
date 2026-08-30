# Fichas de expansión del informe v2

**Estado:** borradores para revisión humana y auditoría independiente.  
**Base:** `fase3-analitica-v1`, 238 documentos activos y 6 exclusiones.  
**Regla:** las nuevas secciones amplían solo donde existe evidencia documental o dato agregado verificable.

## FE-01. De la subregión a la ciudad: escalas y capacidades de implementación

**Preguntas:** P1, P5, P6 y P7.  
**Argumento:** la escala no es una etiqueta auxiliar. El corpus permite seguir un hilo desde prioridades subregionales, pasando por una cuenca binacional donde se articulan autoridades y actores locales, hasta una ciudad que enfrenta brechas operativas de información. La articulación entre escalas es un subconjunto, no el eje único de la lectura.

**Datos agregados:** los ámbitos candidatos registran alcance regional de 53/45/41 documentos, subregional de 57/55/45, subnacional de 19/21/11, nacional de 7/3/4 y multinivel de 5/8/1 en 2015–2018, 2019–2022 y 2023–2026, respectivamente. Las categorías son multi-etiqueta y no suman 238. Capacidades del Estado como transformación primaria registra 19/15/25 documentos.

**Documentos ancla y recorrido narrativo:**

- **Subregional:** *La economía del cambio climático en América Latina y el Caribe: paradojas y desafíos del desarrollo sostenible* (2015, p. 55): “En el seno del Sistema de la Integración Centroamericana (SICA), los presidentes de los países miembros han establecido el cambio climático como uno de sus cinco ejes prioritarios…” (registro SQLite `dimension_id` 531).
- **Cuenca binacional:** *Agenda 2030 en América Latina y el Caribe: ¿cómo acelerar el paso hacia su cumplimiento en la nueva era de incertidumbre y fragmentación geopolítica?* (2026, p. 76): “En la cuenca del río Sixaola (compartida por Costa Rica y Panamá), las dos naciones articulan comisiones, planes de trabajo, alertas tempranas y acciones concertadas…” (registro SQLite `dimension_id` 8215).
- **Ciudad:** *Climate action guidelines 2022–2030: City of Belmopan, Belize* (2022, p. 27): “Greenhouse gas emissions data for the city of Belmopan is not available” (registro SQLite `dimension_id` 5662).

**Límite:** los ámbitos proceden de una normalización candidata y los casos no prueban calidad ni efectividad homogénea de las capacidades estatales. SICA registra arreglos y mandatos, Sixaola ilustra un caso y Belmopan evidencia una brecha de datos; ninguno permite generalizar por sí solo.  
**Figura asociada:** Figura 4, con nota visible de solapamientos entre escalas.

## FE-02. Grandes transformaciones y tensiones dialécticas

**Preguntas:** interpretación transversal de P1-P8.  
**Argumento:** la tipología muestra qué problema de desarrollo organiza cada documento; las tensiones dialécticas permiten leer los conflictos que el corpus procesa, sin tratarlos como soluciones ya logradas.

**Datos agregados:** la transformación primaria Sostenibilidad ambiental registra 60/45/27 documentos y Capacidades del Estado 19/15/25. Macroeconomía y fiscalidad registra 9/4/7; Desarrollo productivo, 3/2/1. El derivado canónico de tensiones conserva texto para los 238 documentos.

**Documentos ancla:**

- *Ocho tesis sobre el cambio climático y el desarrollo sostenible en América Latina* (2015, p. 27): “esta transformación al modelo de desarrollo pasa por la configuración de una nueva matriz de bienes y servicios públicos y privados y en una sociedad más igualitaria…” (registro SQLite `dimension_id` 72).
- *América Latina y el Caribe ante las trampas del desarrollo: transformaciones indispensables y cómo gestionarlas* (2024, p. 209): “Aunque en la región existe un enorme potencial de generación de energías renovables, apenas se aprovecha el 30% del potencial hidroeléctrico, el 10% del eólico y el 1% del solar” (registro SQLite `dimension_id` 474).

**Límite:** la tipología es una capa complementaria; la tensión se toma del texto canónico y formula un problema analítico, no un desenlace resuelto.  
**Figura asociada:** Cuadro de transformaciones por período y matriz cualitativa de tensiones.

## FE-03. Coherencia entre propuestas, avances y brechas

**Preguntas:** P3, P5 y P7.  
**Argumento:** el corpus formula propuestas en casi todos los documentos y, al mismo tiempo, registra avances y brechas. Esa coexistencia sustenta una lectura de implementación condicionada, no una narrativa de éxito o fracaso uniforme.

**Datos agregados:** propuestas de política cubren 92/99, 74/75 y 63/64 documentos; avances de implementación, 61,6%, 66,7% y 71,9%; y brechas de implementación, 59,6%, 76,0% y 70,3%, respectivamente. La presencia de codificación no mide intensidad, adopción ni resultado.

**Documentos ancla:**

- *Acción climática en la agricultura* (2023, p. 79): “la reducción de emisiones a partir de incentivos basados en el mercado, como el Plan Brasileño de Agricultura Baja en Carbono, no se puede verificar fácilmente con los enfoques actuales de monitoreo por teledetección” (registro SQLite `dimension_id` 417).
- *Panorama de la Gestión Pública en América Latina y el Caribe, 2023* (2024, p. 88): “en muchos países de ALC no existe una conexión clara entre los planes nacionales de desarrollo y su asignación en el presupuesto gubernamental, y con frecuencia su financiación resulta insuficiente” (registro SQLite `dimension_id` 689).

**Límite:** los documentos describen instrumentos, avances y brechas; no permiten estimar resultados comparables de política entre países.  
**Figura asociada:** nuevo cuadro de coherencia propuesta/avances/brechas, con denominadores por período.

## Tratamiento acotado de pérdidas y daños y CBDR

Pérdidas y daños entrará como un párrafo breve en el capítulo de implementación y protección financiera. Diferenciará la evaluación de daños e impactos por desastres del marco político-financiero de pérdidas y daños, sin elevarlo a conclusión central. CBDR, responsabilidades comunes pero diferenciadas, aparecerá como una nota cualitativa de negociación climática en la comparación temporal. No son sinónimos ni se usarán como pilares del resumen ejecutivo.

## Compuerta de revisión

Cada ficha requiere una revisión humana y una auditoría independiente de sus citas, datos, límites y figura antes de alimentar `INFORME_MAESTRO_30P_BORRADOR_v2.md`.
