# Bloque narrativo 02 - Impactos, instrumentos, implementación y desafíos

**Estado:** borrador de trabajo para revisión.  
**Alcance previsto:** secciones 4 a 6 de la arquitectura; 11 páginas planificadas.  
**Base:** `fase3-analitica-v1`, 238 documentos activos y 6 exclusiones aplicadas.

## Fichas narrativas

### FN-04. Los impactos territoriales requieren condiciones de transformación

- **Argumento:** el corpus no trata los impactos como un fenómeno físico autónomo; los vincula con recursos, infraestructura, desigualdad y capacidad adaptativa.
- **Documentos ancla:** *Impactos y vulnerabilidad al cambio climático de los principales ríos de Mendoza y San Juan* (39140), para el impacto territorial, y *Hacia una bioeconomía sostenible en América Latina y el Caribe* (44640), para la restricción financiera de los medios de implementación.
- **Citas literales:** “En la actualidad la tendencia al aumento de la temperatura está alterando el hidrograma de los ríos andinos…” (39140, p. 16; registro SQLite `dimension_id` 1129). “La falta de recursos de financiamiento es una restricción a la innovación en América Latina, especialmente en nuevos ámbitos, como la bioeconomía” (44640, p. 18; registro SQLite `dimension_id` 3289).
- **Límite:** Mendoza y San Juan son un caso subnacional; la bioeconomía no representa todas las formas de innovación climática regional.
- **Figura asociada:** Cuadro 2, cobertura de P1-P4.

### FN-05. Las herramientas orientan, pero no sustituyen la decisión pública

- **Argumento:** los instrumentos de análisis permiten priorizar inversiones y políticas, pero requieren financiamiento, capacidades y articulación institucional para influir en la ejecución.
- **Documentos ancla:** *Metodologías para apoyar la estimación de costos... en Guatemala* (41832) y *Cómo financiar el desarrollo sostenible* (47720).
- **Citas literales:** “Se recomienda desarrollar la valoración económica de los planes estratégicos institucionales de reducción de vulnerabilidad, adaptación y mitigación al cambio climático” (41832, p. 85; registro SQLite `dimension_id` 1935). “Es necesario orientar los rendimientos de la inversión, palanca del cambio estructural, en la dirección correcta mediante los instrumentos de política pública” (47720, p. 22; registro SQLite `dimension_id` 5351).
- **Límite:** las metodologías y propuestas de política muestran herramientas disponibles, no su adopción ni eficacia demostrada.
- **Figura asociada:** Gráfico 2, modos analíticos por período.

### FN-06. La brecha decisiva aparece en la ejecución

- **Argumento:** el problema recurrente no es solo identificar medidas climáticas, sino integrarlas a la inversión, los presupuestos, las capacidades y la coordinación territorial.
- **Documentos ancla:** *Desafíos y oportunidades para la ejecución de proyectos de inversión pública con criterios de sostenibilidad* (80561) y *América Latina y el Caribe y la Agenda 2030 a cinco años de la meta* (81405).
- **Citas literales:** “… resulta urgente e impostergable la plena incorporación de los enfoques de resiliencia y reducción de riesgo de desastres en los procesos de inversión, tanto pública como privada” (80561, p. 35; registro SQLite `dimension_id` 7019). “… los países pueden transversalizar las decisiones en materia de cambio climático en diversos sectores y vincularlas con sus planes de desarrollo e inversión, así como con los presupuestos nacionales” (81405, p. 137; registro SQLite `dimension_id` 7500).
- **Límite:** ambos textos presentan marcos, experiencias y recomendaciones; no miden una ejecución homogénea ni resultados comparables entre países.
- **Figura asociada:** Gráfico 4, territorio, tipología y objeto.

### FN-07. Cambio de énfasis, no secuencia lineal

- **Argumento:** la evolución del corpus se expresa en el modo de conectar impactos, instrumentos, inversión y distribución; no en el reemplazo total de una agenda por otra.
- **Evidencia documental:** P1 conserva una base de impactos y vulnerabilidad; P2 aumenta la visibilidad de instrumentos e inversión en la recuperación sostenible; P3 enfatiza con mayor frecuencia ejecución, presupuestos, datos y transición justa. Esta comparación también puede reflejar la composición de la producción CEPAL por división, tipo documental y ventana de recuperación pospandemia.
- **Documentos ancla:** 39140, 47720, 80561 y 81405.
- **Límite:** la dimensión `tendencias` tiene cobertura desigual entre períodos y la taxonomía de objetos es candidata calibrada. La afirmación requiere revisión frente a contraejemplos de cada período.
- **Figura asociada:** Gráfico 1, objetos principales candidatos por período, junto con el recuadro de contraejemplos.

## Borrador narrativo

### 4. Impactos, diagnóstico y herramientas para decidir

El punto de partida del corpus es que el cambio climático modifica condiciones materiales de vida y de producción en territorios concretos. Los impactos no se presentan como un dato físico que pueda separarse de la estructura social, de los recursos disponibles o de la capacidad pública de respuesta. Agua, agricultura, costas, energía, infraestructura y ciudades aparecen como ámbitos donde una amenaza climática se vuelve riesgo cuando coincide con exposición, desigualdad y déficits de información o inversión.

El estudio sobre los ríos de Mendoza y San Juan ofrece una escena territorial precisa. “En la actualidad la tendencia al aumento de la temperatura está alterando el hidrograma de los ríos andinos…” (39140, p. 16; registro SQLite `dimension_id` 1129). La cita no permite extender mecánicamente un resultado hidrológico subnacional a toda la región, pero sí muestra el tipo de vínculo que el corpus documenta: los cambios climáticos alteran sistemas biofísicos de los que dependen actividades económicas, poblaciones y decisiones de infraestructura.

Este encadenamiento importa porque desplaza la pregunta desde la ocurrencia de una amenaza hacia la manera en que se distribuye el riesgo. Una variación en la disponibilidad de agua puede afectar al mismo tiempo abastecimiento, producción agrícola, generación eléctrica y mantenimiento de infraestructura. Sus consecuencias dependen de los márgenes de adaptación de hogares, empresas, gobiernos locales y organismos sectoriales. Así, el diagnóstico climático que recorre el corpus no se limita a registrar daños potenciales: busca reconocer qué relaciones entre ecosistemas, actividades y desigualdades deben entrar en la decisión pública.

El diagnóstico se prolonga en las condiciones de transformación. En el caso de la bioeconomía, la restricción no es únicamente tecnológica: “La falta de recursos de financiamiento es una restricción a la innovación en América Latina, especialmente en nuevos ámbitos, como la bioeconomía” (44640, p. 18; registro SQLite `dimension_id` 3289). El caso ilustra que la respuesta climática requiere conectar oportunidades productivas con financiamiento, instituciones y capacidades. No demuestra que todas las innovaciones enfrenten la misma restricción, pero ayuda a explicar por qué el corpus desplaza la discusión desde el problema ambiental aislado hacia los medios de implementación.

Las herramientas analíticas ocupan un lugar intermedio entre diagnóstico y acción. Escenarios, modelos, valoración económica, indicadores, información geoespacial y sistemas de monitoreo permiten identificar alternativas y ordenar prioridades. El documento metodológico aplicado a Guatemala propone “desarrollar la valoración económica de los planes estratégicos institucionales de reducción de vulnerabilidad, adaptación y mitigación al cambio climático” (41832, p. 85; registro SQLite `dimension_id` 1935). La recomendación pone de relieve que una herramienta no decide por sí misma: aporta una base para deliberar sobre inversión pública, costos, fuentes de financiamiento y secuencia de medidas.

La distinción es decisiva para interpretar la creciente presencia de datos y herramientas en el período reciente. Un modelo puede comparar escenarios; un indicador puede hacer visible una brecha; una valoración puede hacer explícitos costos antes omitidos. Ninguno resuelve por sí mismo el conflicto entre usos alternativos de recursos, ni determina quién asume el costo de una medida o quién recibe primero su protección. La utilidad de estos instrumentos depende de que sus supuestos sean discutibles, sus resultados sean inteligibles para quienes deciden y existan instituciones capaces de incorporarlos en presupuestos, proyectos y mecanismos de seguimiento.

Por eso, el corpus no opone conocimiento técnico y decisión política. Los vincula en una secuencia: producir información pertinente, priorizar inversiones, definir responsabilidades, ejecutar y aprender de lo ejecutado. La secuencia tampoco es automática. La ausencia de datos comparables, la incertidumbre sobre impactos y la capacidad desigual de producir información pueden reproducir sesgos territoriales si solo se financia aquello que ya puede medirse con facilidad. El valor del diagnóstico consiste, precisamente, en hacer visibles esas decisiones y no en prometer una neutralidad inexistente.

### 5. Instrumentos, ejecución y desafíos de implementación

El corpus describe instrumentos fiscales, financieros, regulatorios, tecnológicos y de planificación como partes de conjuntos de política. En lugar de tratar la inversión como consecuencia automática de un diagnóstico climático, los textos preguntan cómo orientar incentivos, recursos y capacidades hacia actividades compatibles con sostenibilidad e igualdad. En un documento de recuperación sostenible, la formulación es directa: “Es necesario orientar los rendimientos de la inversión, palanca del cambio estructural, en la dirección correcta mediante los instrumentos de política pública” (47720, p. 22; registro SQLite `dimension_id` 5351).

Esta perspectiva permite leer las brechas de implementación con más precisión. Los obstáculos recurrentes no se reducen a falta de normas: incluyen capacidades técnicas y subnacionales, datos, financiamiento, coordinación entre sectores y continuidad institucional. El reto es integrar la reducción del riesgo y la resiliencia en las decisiones que determinan qué proyectos se financian, cómo se diseñan y qué poblaciones reciben protección.

El documento sobre inversión pública con criterios de sostenibilidad formula la urgencia de esa integración: “… resulta urgente e impostergable la plena incorporación de los enfoques de resiliencia y reducción de riesgo de desastres en los procesos de inversión, tanto pública como privada” (80561, p. 35; registro SQLite `dimension_id` 7019). La cita no prueba que tal incorporación esté ocurriendo con igual intensidad en todos los países; muestra, en cambio, que el corpus identifica la inversión como un sitio decisivo donde el diagnóstico climático puede traducirse, o no, en acción pública.

Mirar la inversión de este modo permite distinguir volumen, orientación y secuencia. Aumentar recursos puede ser necesario, pero no basta cuando los proyectos se definen sin criterios de exposición, mantenimiento, igualdad o riesgo futuro. Del mismo modo, una regla ambiental o un incentivo financiero pierde alcance si no conversa con la planificación territorial, las capacidades de preparación de proyectos y los sistemas que permiten sostener una obra o un servicio. El problema de ejecución es, por tanto, también un problema de complementariedades: los instrumentos se refuerzan o se bloquean según cómo se conecten.

Esa conexión tiene una dimensión distributiva. La transición puede crear nuevas actividades, empleo e infraestructura, pero también modificar precios, condiciones laborales, acceso a servicios y exposición a riesgos. Incorporar protección social, participación y criterios de equidad no es una compensación externa al diseño climático. Es una condición para anticipar costos, sostener acuerdos y evitar que las medidas recaigan desproporcionadamente sobre quienes tienen menor capacidad de respuesta. Los documentos del corpus formulan estas relaciones como orientaciones y desafíos; no permiten concluir que los arreglos distributivos ya funcionen de forma homogénea.

La coordinación se completa cuando las decisiones climáticas se relacionan con presupuestos y planes de desarrollo. *América Latina y el Caribe y la Agenda 2030 a cinco años de la meta* sostiene que “… los países pueden transversalizar las decisiones en materia de cambio climático en diversos sectores y vincularlas con sus planes de desarrollo e inversión, así como con los presupuestos nacionales” (81405, p. 137; registro SQLite `dimension_id` 7500). Este marco integra clima, inversión y coherencia institucional, aunque debe leerse como una orientación de política y no como evidencia de ejecución efectiva.

El tratamiento de pérdidas y daños ilustra por qué la precisión conceptual importa en esta discusión. La búsqueda verificada identifica 27 documentos con menciones al término, pero las coincidencias no describen una sola materia: pueden referirse a la evaluación de daños e impactos de fenómenos extremos, a necesidades de protección y recuperación, o al marco político-financiero internacional. La clasificación automática conserva 13 coincidencias candidatas de evaluación de daños, 12 de política y financiamiento y 31 que requieren revisión. En consecuencia, el informe no agrega esas referencias como evidencia de un mismo instrumento ni infiere disponibilidad efectiva de recursos. La distinción permite relacionar la evaluación de impactos con la preparación e inversión, y discutir por separado los mecanismos de financiamiento y cooperación.

La ejecución también requiere continuidad. Una cartera climática madura no termina cuando se aprueba un plan o se asigna una partida: necesita responsables identificables, información para monitorear, capacidad de ajuste y recursos para operación y mantenimiento. Esta mirada explica la recurrencia de capacidades estatales, datos y coordinación en el corpus reciente. No constituye una medida de capacidad institucional regional, sino una señal de que la CEPAL formula la acción climática como una práctica sostenida de gestión pública, más allá de la formulación inicial de objetivos.

### 6. Una evolución de énfasis y articulaciones

La comparación temporal no justifica una historia de reemplazos. En P1, impactos, vulnerabilidad y adaptación ya se relacionan con instituciones, financiamiento y planificación. P2 pone en primer plano la recuperación sostenible y amplía la discusión de instrumentos, inversión y cambio estructural. P3 hace más visible la discusión sobre ejecución, presupuestos, datos, infraestructura resiliente y distribución de los costos de transición. Los tres períodos mantienen problemas físicos y territoriales, pero modifican el tipo de articulación que se vuelve central.

La ventana de 2019–2022 ayuda a explicar el segundo movimiento. La recuperación posterior a la pandemia ofreció un lenguaje para reunir problemas que a menudo se trataban en circuitos separados: reactivación, empleo, protección social, digitalización, infraestructura e inversión sostenible. Ese lenguaje no elimina diferencias entre sectores ni países, pero vuelve más explícita la necesidad de coordinar objetivos climáticos con transformaciones productivas y sociales. En 2023–2026, el foco en financiamiento, ejecución y seguimiento prolonga esa preocupación, ahora con mayor atención a la factibilidad de proyectos, presupuestos y capacidades territoriales.

Las responsabilidades comunes pero diferenciadas ocupan un lugar distinto dentro de esta evolución. La revisión sistemática de los documentos fuente encuentra menciones en siete publicaciones, distribuidas en los tres períodos. Esa presencia limitada no basta para medir su peso en la agenda institucional ni para reconstruir posiciones negociadoras. Permite, de manera más acotada, reconocer que algunos textos sitúan la acción climática en un marco de responsabilidades y capacidades heterogéneas entre países. El principio no equivale a una regla de implementación doméstica: orienta la discusión sobre cooperación, financiamiento y ambición en la negociación climática internacional.

Esta lectura combina tres fuentes de evidencia: perfiles completos con conclusiones y recomendaciones directas; paneles de modos e interpelación; y citas seleccionadas. La cobertura de las menciones a tendencias es desigual, por lo que no sostiene por sí sola la comparación. Tampoco los objetos principales revisados para este informe se presentan como una codificación experta exhaustiva. Además, parte de la diferencia temporal puede obedecer a qué publicó CEPAL, desde qué división y en qué contexto: la ventana de recuperación pospandemia favoreció documentos diseñados para articular inversión, coordinación y sostenibilidad. El argumento es más acotado: el corpus muestra una creciente preocupación por conectar acción climática con condiciones de inversión, coordinación y ejecución, sin abandonar impactos, vulnerabilidad y desigualdad.

Las Figuras 1 y 2 se leen juntas. La primera permite observar los objetos revisados por período; la segunda evita leerlos como sustituto de los campos directos, al distinguir diagnóstico, prospectiva, evaluación de implementación, conclusiones, recomendaciones y política concreta. El recuadro de contraejemplos recuerda que 2015–2018 ya incluye instrumentos fiscales y financieros, y que 2023–2026 conserva impactos y vulnerabilidad. Esa tensión hace más defendible la tesis de cambio de énfasis.

> **Recuadro 1. Contraejemplos de la comparación temporal**
>
> La comparación no convierte 2015–2018 en una etapa exclusivamente biofísica. Ocho documentos de ese período tienen financiamiento e inversión como objeto principal revisado, entre ellos *The rise of green bonds: Financing for development in Latin America and the Caribbean* (2017) y el estudio sobre efectos potenciales de un impuesto al carbono (2017). Tampoco 2023–2026 es una etapa exclusivamente financiera o institucional: nueve documentos tienen impactos y vulnerabilidad como objeto principal revisado, incluidos *Assessment of the effects and impacts of Hurricane Beryl on Barbados, 2024* (2024) y la evaluación de la tormenta tropical Sara en Honduras (2024). Son conteos revisados para este informe, no una codificación experta exhaustiva, pero muestran que los énfasis cambian sin borrar los problemas previos.

## Trazabilidad de evidencia

Las citas se verifican en los JSON canónicos indicados por ruta y SHA-256. El `dimension_id` identifica el registro correspondiente en SQLite y no es un campo del JSON canónico.

| Documento | Fuente canónica | Página | Registro SQLite |
| --- | --- | --- | --- |
| 39140 | `fase2/corpus/resultados/json/doc_39140.json`; SHA-256 `ebe7f003ea339a6a616044b515281c270cc7a560acc6010ed21a859d2dd30567` | 16 | `dimension_id` 1129 |
| 41832 | `fase2/corpus/resultados/json/doc_41832.json`; SHA-256 `9a6115719e4f5492ae537341f61193135ad1699be1a148445f39dec4ee719d9c` | 85 | `dimension_id` 1935 |
| 44640 | `fase2/corpus/resultados/json/doc_44640.json`; SHA-256 `4c4b4bbe0e206182fbb9a23b7059ae218f0ef4fe4b777c54a528b454c0a1f8b5` | 18 | `dimension_id` 3289 |
| 47720 | `fase2/corpus/resultados/json/doc_47720.json`; SHA-256 `bac14714f49713c81a94bda9b0e757d6142a0bddfbef55f1304790c06c3f7cb5` | 22 | `dimension_id` 5351 |
| 80561 | `fase2/corpus/resultados/json/doc_80561.json`; SHA-256 `1b2f7e460585b4247bbb2d3395594db2ba8ae2d3316a7a962e42a4040bb0a144` | 35 | `dimension_id` 7019 |
| 81405 | `fase2/corpus/resultados/json/doc_81405.json`; SHA-256 `4b8a1c9c9a56ad6c6192e6db9e2fbb927a22545f4343a2f071e29c666ee5b14c` | 137 | `dimension_id` 7500 |

## Revisión requerida

- Evaluar si cada cita cumple una función de ancla y no solo de ilustración.
- Confirmar que la síntesis de cambio de énfasis conserva los contraejemplos de P1 y P3.
- Mantener fuera de este bloque las afirmaciones sustantivas sobre pérdidas y daños y CBDR hasta completar su compuerta específica.
