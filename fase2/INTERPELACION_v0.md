# Metodología de interpelación institucional v0.3

**Fecha**: 2026-07-07 (creación) — revisado 2026-07-07 (Ronda 2), 2026-07-07 (Ronda 3) y 2026-07-08 (Ronda 4)
**Estado**: v0.3, recalibrado con la revisión humana de los 3 JSON piloto (Ronda 3): definición operativa del gran impulso ambiental anclada a [big_push.md](big_push.md), regla de ámbito de aplicación para el criterio (ii) —que corrigió el veredicto de doc13—, y regla de autocontención (los veredictos no referencian otros documentos del corpus, ver [esquema_json_v1.md](esquema_json_v1.md) regla transversal 3). Ronda 4 cierra dos preguntas que quedaban abiertas (ver [§1.6](#16-documentos-de-naturaleza-distinta-a-una-propuesta-de-política-climática-ronda-4) y el cierre de sección 4).
Sigue pendiente de validación por el equipo del curso antes de escalar a los 12 documentos restantes de la muestra.

**Unidad de análisis**: documento completo.

## 0. De dónde sale esto y por qué hace falta operacionalizarlo

La nota conceptual plantea (sección 2.2) que la CEPAL propone un "gran impulso ambiental" que implica "reorientación de inversiones, cambio estructural productivo, incorporación de innovación y desarrollode nuevos sectores sostenibles", y (sección 4) que esto exige "articulación de múltiples actores y sectores" y reemplazar la narrativa de costos por la de oportunidad de "innovación, productividad, creación de empleo y reducción de desigualdades". Es un párrafo de posicionamiento, no una rúbrica. Los
4 criterios de interpelación son una traducción de ese párrafo a preguntas evaluables — la traducción es interpretación del Lab y debe tratarse como tal (discutible, no un hecho dado) hasta que el equipo del curso la confirme o la corrija.

## 1. Guardrails (reusados de la tipología, sección 2 de [TIPOLOGIA_v0.md](TIPOLOGIA_v0.md))

Los mismos dos errores documentados en Desafío CEPAL aplican acá, con una manifestación específica:

- **Sesgo de palabra clave** → el riesgo es marcar "Sí, promueve el gran impulso ambiental" en cualquier documento que mencione "energía renovable" o "transición verde", sin distinguir apertura retórica de propuesta con instrumento concreto.
- **Justificación zombie** → el riesgo es que las 4 evidencias converjan en la misma frase genérica para todo el corpus ("el documento aborda la sostenibilidad de forma transversal").

**Regla anti-copia** (idéntica a la de tipología): la evidencia citada debe ser una cita textual literal del documento con página, nunca un parafraseo de la definición del criterio. Sin cita → el veredicto no puede ser "Sí".

**Veredicto en 3 valores, nunca binario**: Sí / Parcial / No, con default a Parcial o No ante ambigüedad. Forzar Sí/No es lo que produce sobre-interpretación optimista.

### 1.1 Por qué se sharpened (Ronda 2) — un tercer modo de falla que Ronda 1 no cubría

La Ronda 1 (ver [Bitácora en PLAN_ANALISIS_PROFUNDO.md](PLAN_ANALISIS_PROFUNDO.md#bitácora-de-calibración-metodológica)) resolvió la unidad de análisis y adoptó el protocolo anti-copia. Pero al revisar los veredictos concretos del
piloto sobre doc09/doc13 apareció un tercer modo de falla, más sutil que "palabra clave" o "justificación zombie": **evidencia real y con cita, pero elegida por ser la más fácil de citar, no la más fuerte disponible en el documento** — o una lista completa acreditada como "Sí" sin verificar si cada ítem individual pasa el
mismo estándar de concreción. Ejemplo concreto de este error, cometido en el primer intento sobre doc09 criterio (ii): se citó "promote a collaborative multiple-stakeholder approach... dialogue between traditional energy players... and other interested stakeholders" (p.9) — lenguaje de "deber ser" sin mecanismo nombrado
— cuando dos páginas antes el mismo documento describe el IRRP, un mecanismo ya adoptado por 5 países concretos con apoyo institucional de CCREEE (p.6-7). Ambas evidencias son literales y verificables, pero una es genérica y la otra es concreta; el primer intento citó la genérica. Las tres reglas de esta sección (1.2-1.4) existen para forzar la comparación explícita entre evidencia genérica y evidencia concreta antes
de fijar el veredicto, no solo para exigir que exista una cita.

### 1.2 Regla sharpened — criterio (ii): institución o mecanismo nombrado, no solo actores nombrados

No basta con que el documento nombre tipos de actores (gobiernos, sector privado, sociedad civil). El criterio busca un **mecanismo, plataforma, consejo, proceso o instrumento de coordinación con nombre propio** entre esos actores. "Se requiere la participación de todos los sectores" sigue siendo lenguaje de "deber ser" aunque enumere actores con detalle. Regla de decisión revisada:

- **Sí**: nombra un mecanismo/institución/plataforma específica de coordinación entre actores (p. ej. un consejo bilateral, un plan conjunto ya adoptado, una mesa de diálogo institucionalizada) — no basta con nombrar quiénes deberían participar.
- **Parcial**: nombra actores específicos (por tipo de entidad, no genérico) pero el mecanismo de coordinación entre ellos queda en "debería haber diálogo/colaboración", sin nombre propio ni evidencia de que ya existe o está siendo diseñado.
- **No**: no aborda coordinación entre actores, o lo hace en términos completamente genéricos ("todos los sectores de la sociedad").

**Ampliación Ronda 3 — el mecanismo debe pertenecer al ámbito de aplicación del documento.** Un cuarto modo de falla, detectado en la revisión humana del piloto: citar un mecanismo con nombre propio que el documento describe como **ejemplo extrarregional**, no como articulación propuesta o vigente para la región que el documento analiza. Caso concreto: en doc13 se acreditó "Sí" citando el "Consejo de Acero del CBAM" y el "Grupo Asesor de Comercio de Carbono" (p.70-71) — mecanismos creados por la **República de Corea** para su propio diálogo con la UE, presentados por el documento como referente de lo que otros países están haciendo. Para la subregión analizada, el mismo documento solo registra que México "expresó
interés" y lenguaje de "se podría considerar la posibilidad de colaborar". Regla resultante:

- El mecanismo nombrado cuenta para "Sí" solo si pertenece al **ámbito de aplicación** del documento (la región/países que analiza — misma distinción ámbito vs. referentes del [codebook §2](codebook_v0.md)) o si el documento lo **propone explícitamente** para ese ámbito.
- Mecanismos extrarregionales citados como referentes o buenas prácticas topean el veredicto en **"Parcial"**, por concretos que sean — describen la articulación de otros, no la del sujeto del documento.

### 1.3 Regla sharpened — criterio (iii): enumeración de oportunidades + chequeo explícito de empleo/desigualdad

No basta con una mención aislada de "co-beneficios económicos". El criterio pide dos cosas verificables por separado: (a) que el documento **enumere** sectores, industrias, mercados o actividades concretas donde ve la oportunidad (no una afirmación genérica de que "hay oportunidades"), y (b) que conecte esa enumeración
explícitamente con empleo, productividad o desigualdad — no basta con que ambos temas aparezcan en el mismo documento sin estar conectados entre sí.

- **Sí**: enumera sectores/actividades concretas **y** desarrolla el vínculo con empleo/productividad/desigualdad con cifra propia o mecanismo de política nombrado (no una sola frase de transición).
- **Parcial**: enumera sectores/actividades concretas pero el vínculo con empleo/desigualdad es una mención aislada sin desarrollo, **o** desarrolla el vínculo con empleo/desigualdad pero sin enumerar sectores concretos (queda en abstracto: "la transición genera oportunidades económicas").
- **No**: ninguno de los dos elementos aparece. **El veredicto "No" debe mostrar el chequeo negativo explícito** — es decir, la evidencia debe decir qué se buscó y no se encontró ("el documento no menciona empleo, productividad ni desigualdad en ningún pasaje; tampoco enumera sectores u oportunidades productivas"), no limitarse a `"pagina": null`.

### 1.4 Regla sharpened — criterio (iv): enumeración ítem por ítem, no la lista completa a la vez

Cuando el documento presenta una lista numerada de recomendaciones o pasos, **no se acredita la lista entera como "Sí" sin revisar cada ítem por separado**. Cada ítem se somete a un test de concreción: ¿tiene verbo de acción + objeto específico (+ opcionalmente actor, plazo o métrica)? o es una reformulación genérica del tipo "es fundamental fortalecer X"/"se recomienda avanzar hacia Y". El veredicto refleja qué
proporción de la lista pasa el test, no si existe una lista.

- **Sí**: la mayoría de los ítems enumerados (indicar M de N) pasan el test de concreción — verbo + objeto específico, identificable como acción ejecutable.
- **Parcial**: la lista existe pero es una mezcla — algunos ítems pasan el test de concreción y otros son genéricos/aspiracionales (indicar M de N igualmente, para que quede trazable cuál es cuál).
- **No**: la lista, si existe, es mayoritariamente genérica, o solo hay diagnóstico sin recomendación operativa.

### 1.5 Definición operativa del gran impulso ambiental — criterio (i) anclado a big_push.md (Ronda 3)

La revisión humana del piloto señaló que la definición del criterio (i) era demasiado vaga — "reorientación de inversiones, cambio estructural productivo..." tomada tal cual de la nota conceptual — y que esa vaguedad explica veredictos difíciles de fijar (el "Parcial" de doc09 costó justificarlo). Para resolverlo se creó [big_push.md](big_push.md), una nota con el significado elaborado del Big Push Ambiental (origen en *Horizontes 2030*, 2016). De ahí se derivan **tres tests operativos** para el criterio (i):

1. **Inversión masiva y coordinada, no reformas fragmentadas** — ¿el documento propone un paquete coordinado de inversiones/políticas simultáneas (la metáfora del despegue del avión), o medidas aisladas/graduales?
2. **Sectores estratégicos nombrados** — ¿aterriza en sectores concretos del tipo que enumera la nota (transición energética, electromovilidad, bioeconomía, economía circular, salud/cuidados), con instrumento identificable?
3. **Las tres eficiencias** — ¿conecta la propuesta con al menos dos de las tres dimensiones que definen el enfoque: eficiencia schumpeteriana (tecnología/conocimiento en procesos locales), keynesiana (empleo/demanda interna/desigualdad) y ambiental (desacople de emisiones)?

Lectura de los tests: **"Sí"** requiere el test 1 más al menos uno de los otros dos — eso es lo que significa "a escala de modelo de desarrollo". Instrumentos concretos pero sectoriales y sin lógica de paquete coordinado (test 1 ausente) → **"Parcial"**. Solo lenguaje aspiracional → **"No"**. Los tests no exigen que el documento use la etiqueta "gran impulso ambiental" — exigen que proponga su contenido.

### 1.6 Documentos de naturaleza distinta a una propuesta de política climática (Ronda 4)

Pregunta abierta desde Ronda 2 (caso doc11, estudio de modelización econométrica que no propone transformación productiva alguna): **se confirma que los 4 criterios se aplican sin excepción a todo documento del corpus, sin criterio de "no aplica".** Cuando el documento es de naturaleza distinta a una propuesta de política climática (diagnóstico, proyección cuantitativa, evaluación de impacto), se interpela igual contra los 4 criterios —los veredictos "No" que resulten son información válida, no un error del pipeline— y el campo `nota` de cada criterio debe indicar explícitamente esa naturaleza distinta y por qué (ver el `nota` de `gran_impulso_ambiental_concreto` en [pilot/doc11_pobreza_infantil.json](pilot/doc11_pobreza_infantil.json) como ejemplo ya aplicado: "El No es por diseño del documento, no por omisión descuidada..."). Esto cierra la pregunta que quedaba pendiente en la sección 4 de este documento y en `PLAN_ANALISIS_PROFUNDO.md §5`.

## 2. Los 4 criterios (definiciones vigentes, v0.2)

| #   | Pregunta (traducida de la nota)                                                                       | Definición operativa                                                                                                                                                                                                                                             | Regla de decisión                                                                                                                                                                                                                                                                                                                                                                                          | Ejemplo de "justificación zombie" a evitar                                                     |
| --- | ----------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| i   | ¿Promueve el gran impulso ambiental con elementos concretos?                                          | Los 3 tests operativos derivados de [big_push.md](big_push.md) — inversión masiva y coordinada, sectores estratégicos nombrados, las tres eficiencias — ver [§1.5](#15-definición-operativa-del-gran-impulso-ambiental--criterio-i-anclado-a-big_pushmd-ronda-3) | **Sí**: test 1 + al menos uno de los tests 2-3 (escala de modelo de desarrollo). **Parcial**: instrumento nombrado pero sectorial y sin lógica de paquete coordinado, o el documento es mayormente diagnóstico de un instrumento externo y no una propuesta autónoma de transformación. **No**: solo lenguaje aspiracional sin instrumento, o no aborda transformación productiva/de inversión en absoluto | "El documento se alinea con el espíritu de sostenibilidad y transición hacia energías limpias" |
| ii  | ¿Articula actores/sectores/niveles de gobierno mediante un mecanismo concreto?                        | Nombra un mecanismo, plataforma o institución de coordinación con nombre propio — ver regla sharpened [§1.2](#12-regla-sharpened--criterio-ii-institución-o-mecanismo-nombrado-no-solo-actores-nombrados)                                                        | Ver [§1.2](#12-regla-sharpened--criterio-ii-institución-o-mecanismo-nombrado-no-solo-actores-nombrados)                                                                                                                                                                                                                                                                                                    | "Se requiere la participación de todos los sectores de la sociedad"                            |
| iii | ¿Releva oportunidades productivas sostenibles enumeradas, con vínculo explícito a empleo/desigualdad? | Enumeración de sectores/actividades concretas + vínculo desarrollado con empleo, productividad o reducción de desigualdad — ver regla sharpened [§1.3](#13-regla-sharpened--criterio-iii-enumeración-de-oportunidades--chequeo-explícito-de-empleodesigualdad)   | Ver [§1.3](#13-regla-sharpened--criterio-iii-enumeración-de-oportunidades--chequeo-explícito-de-empleodesigualdad)                                                                                                                                                                                                                                                                                         | "La transición verde puede generar beneficios económicos y sociales"                           |
| iv  | ¿Propone el "cómo hacerlo" con ítems individualmente concretos?                                       | Lista de acciones donde cada ítem pasa un test de concreción (verbo + objeto específico) — ver regla sharpened [§1.4](#14-regla-sharpened--criterio-iv-enumeración-ítem-por-ítem-no-la-lista-completa-a-la-vez)                                                  | Ver [§1.4](#14-regla-sharpened--criterio-iv-enumeración-ítem-por-ítem-no-la-lista-completa-a-la-vez)                                                                                                                                                                                                                                                                                                       | "Es fundamental avanzar hacia una implementación efectiva de las políticas propuestas"         |

## 3. Relación con el campo `resumen_narrativo` (Etapa 2)

El mismo principio anti-genérico de esta sección aplica al campo `resumen_narrativo` agregado en Ronda 2 al esquema de enriquecimiento documental (ver
[PLAN_ANALISIS_PROFUNDO.md § Etapa 2](PLAN_ANALISIS_PROFUNDO.md#etapa-2--enriquecimiento-documental-punto-1-del-pedido)): un resumen narrativo de 3-5 oraciones que **no pase el test "¿esto podría describir cualquier otro documento del corpus con solo cambiar el título?"** no es un resumen narrativo, es relleno. La misma
disciplina de citar lo específico en vez de lo genérico que exige la interpelación aplica ahí.

## 4. Casos de calibración

Estado tras Ronda 2 — los tres documentos del piloto (doc09, doc13, doc11) fueron re-evaluados o evaluados desde el inicio bajo las reglas sharpened de esta sección. Los veredictos actuales en [pilot/doc09_caribbean_power.json](pilot/doc09_caribbean_power.json), [pilot/doc13_carbono_frontera.json](pilot/doc13_carbono_frontera.json) y
[pilot/doc11_pobreza_infantil.json](pilot/doc11_pobreza_infantil.json) siguen siendo un segundo intento a confirmar con el equipo del curso, no una verdad ya calibrada:

- **Doc. 9** — criterio (ii) se corrigió de "Sí" (evidencia genérica de p.9) a "Sí" con evidencia re-anclada al IRRP/CCREEE (p.6-7), que sí nombra un mecanismo concreto — el veredicto no cambió, pero la evidencia que lo sostiene ahora es la más fuerte disponible, no la más fácil de citar. Criterio (iv) se desglosó ítem por
  ítem: de las 8 recomendaciones, se identificaron cuáles pasan el test de concreción y cuáles son más aspiracionales (ver JSON). Criterio (iii) se mantiene en "No" pero ahora con el chequeo negativo explícito requerido por [§1.3](#13-regla-sharpened--criterio-iii-enumeración-de-oportunidades--chequeo-explícito-de-empleodesigualdad).
- **Doc. 13** — criterio (iii) se desglosó en las 4 oportunidades concretas que el documento sí enumera (empleo verde, servicios de medición/verificación de emisiones, coprocesamiento de residuos en CANACEM, educación STEM), confirmando el "Sí" pero ahora con trazabilidad ítem por ítem en vez de una sola cita agregada. Criterio (iv) se desglosó igual: de los 8 puntos de acción, cuántos pasan el test de concreción. El criterio (i) sigue en "Parcial" — sin cambios, ya reflejaba la distinción propuesta/respuesta-adaptativa antes de Ronda 2. **Criterio (ii), corregido en Ronda 3 de "Sí" a "Parcial"**: la revisión humana detectó
  que los mecanismos citados (Consejo de Acero del CBAM, Grupo Asesor de Comercio de Carbono, p.70-71) son instancias creadas por la República de Corea — ejemplos extrarregionales, no articulación propuesta o vigente para la subregión analizada. Verificado contra el PDF: para la subregión el documento solo
  registra interés expresado por México (Cuadro 8) y lenguaje de "se podría considerar colaborar". Aplica la ampliación del [§1.2](#12-regla-sharpened--criterio-ii-institución-o-mecanismo-nombrado-no-solo-actores-nombrados).
- **Doc. 11** (nuevo, tercer piloto) — documento de naturaleza distinta a los dos anteriores: es un estudio de modelización econométrica (impacto del cambio climático sobre la pobreza infantil vía PIB), no una propuesta de política climática en sí misma. Sirve como caso de estrés para los 4 criterios porque su "cómo hacerlo" está concentrado en 4 páginas de conclusiones (sección 4) después de 38 páginas de metodología/resultados cuantitativos — ver veredictos y su justificación en el JSON.

**Resuelto en Ronda 4 (2026-07-08)**, sin esperar al equipo del curso (contraparte de dominio poco proactiva en el diseño de esta revisión; el Lab avanzó con decisión propia, a confirmar si el equipo se pronuncia luego): (a) el estándar de "mecanismo con nombre propio" para (ii) se confirma como correcto — no basta con mencionar actores por tipo; (b) los 4 criterios se aplican sin excepción, incluso a documentos de naturaleza distinta a una propuesta de política climática (como doc11) — ver [§1.6](#16-documentos-de-naturaleza-distinta-a-una-propuesta-de-política-climática-ronda-4).
