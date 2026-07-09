# Cómo estamos leyendo el corpus climático de la CEPAL

**Nota metodológica para el equipo del curso** — CEPAL Lab, julio de 2026

> **Qué es este documento.** Una explicación de la metodología que proponemos para analizar los 244 documentos del corpus climático, con la lista de las 14 publicaciones que elegimos para calibrarla y 3 ejemplos completos del resultado que produce. No es un documento técnico del pipeline: es la versión para discutir, validar y poder replicar a manualmente. El detalle (reglas de decisión completas, historial de calibración) vive en el repositorio del proyecto y está disponible cuando se requiera.
> 
> **Acompañan a esta nota tres anexos**, uno por cada documento piloto, con la ficha completa que produjo la metodología sobre cada uno: todos los apartados, todas las citas con su página, y los razonamientos íntegros.

---

## 1. El punto de partida

En la Etapa 1, hicimos la selección inicial de los documentos sobre cambio climático (2015-2026) que totalizaban 239 publicaciones. En la Etapa 2 construimos un corpus depurado de **244 publicaciones de la CEPAL**, a partir de la exclusión de publicaciones que no eran pertinentes (9) y la inclusión de otras (14) que el equipo del curso consideró relevantes incorporar. La Etapa 3, consiste en pasar del corpus a mirar su contenido: qué dice cada uno, dónde lo dice y con qué nivel de concreción, de forma estructurada, trazable y comparable entre documentos, para poder responder las preguntas de investigación de la nota conceptual del curso.

Para eso, cada documento se procesa una sola vez y produce una **ficha estructurada** — un conjunto estandarizado de campos, siempre los mismos para todos los documentos — con cuatro grandes bloques:

1. **Metadatos y resumen enriquecido** — qué documento es y de qué trata.
2. **Resumen por secciones + dimensiones analíticas** — qué dice cada apartado y qué tipo de contenido aporta (diagnóstico, propuesta, brecha…), con cita textual y página.
3. **Interpelación institucional** — cuán concreto es el documento frente a 4 criterios derivados de la nota conceptual.
4. **Tipología** — qué transformación estructural persigue el documento como pieza de pensamiento institucional.

Antes de correr esto sobre los 244 documentos, lo calibramos: escribimos las reglas, las aplicamos a 3 documentos piloto, revisamos los resultados en 4 rondas de crítica interna (corrigiendo veredictos, endureciendo reglas y unificando formatos), y ahora les compartimos el paquete para su validación.

---

## 2. Una idea clave: dos niveles de análisis distintos

No todo se analiza con la misma lupa. Algunos elementos se extraen **apartado por apartado** (la unidad mínima de análisis) y otros se evalúan sobre el **documento completo**. Esta distinción es importante para replicar o validar:

| Elemento                                                              | ¿Sobre qué se aplica? |
| --------------------------------------------------------------------- | --------------------- |
| Metadatos (título, fecha, páginas, idioma…)                           | Documento completo    |
| Resumen enriquecido (pregunta, alcance, hallazgos, resumen narrativo) | Documento completo    |
| Resumen por secciones                                                 | Cada apartado         |
| Las 9 dimensiones analíticas (con cita y página)                      | Cada apartado         |
| Interpelación institucional (4 criterios)                             | Documento completo    |
| Tipología (transformación primaria/secundaria)                        | Documento completo    |

**¿Qué es un "apartado"?** Es la unidad de encabezado más profunda que exista en la estructura real de cada documento: en un policy brief corto, sus secciones sin numerar; en un documento estándar, las secciones y subsecciones del índice (2.1, 3.2…); en los más extensos, hasta el tercer nivel (III.B.2). Elegimos el apartado —y no el párrafo— porque es la unidad que el propio documento declara en su índice: es reproducible entre lectores distintos (dos personas siempre van a coincidir en dónde empieza y termina la sección 2.1, no necesariamente en dónde "corta" un párrafo temático).

Dos reglas prácticas que decidimos en la calibración:

- El **resumen ejecutivo** del documento no se procesa como apartado (su contenido ya alimenta el resumen enriquecido; procesarlo duplicaría el conteo).
- Los **anexos técnicos** tampoco: se registra que existen, pero no se etiquetan.

---

## 3. Los campos que extraemos de cada documento

El identificador unívoco del documento. La mayoría se explican solos; señalamos aquí los que tienen ciertas particularidades:

| Campo                          | Qué es                                                                                                                                                                           |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Título, autoría, fecha, idioma | Lo esperable. La autoría queda vacía si el documento es institucional sin autores personales.                                                                                    |
| **Handle**                     | El enlace permanente del repositorio de la CEPAL (`hdl.handle.net/…`). Es el identificador único de cada documento en todo el análisis.                                          |
| Símbolo / ISBN                 | El símbolo ONU (LC/…) y el ISBN si existe.                                                                                                                                       |
| Tipo de documento              | Policy brief, documento de proyecto/estudio técnico, informe insignia, etc.                                                                                                      |
| **Páginas de cuerpo**          | Cuántas páginas hay desde la introducción hasta el final de las conclusiones — la medida de "cuánto argumento sustantivo" tiene el documento.                                    |
| **Páginas totales**            | La numeración completa, incluyendo bibliografía y anexos. Mantenemos ambas cifras porque miden cosas distintas (un documento de 105 páginas con 25 de anexos "argumenta" en 80). |
| ¿Tiene resumen ejecutivo?      | Sí/No — registra por qué esa parte no aparece en el resumen por secciones.                                                                                                       |

Además, el **resumen enriquecido** captura, a nivel de documento completo:

- **Pregunta de investigación**, qué interrogante pretende responder el documento, formulada como pregunta.
- **Alcance**, en cuatro planos: *ámbito de aplicación* (sobre qué países/región el documento analiza o propone algo), *referentes o dependencias* (países o bloques que solo se mencionan como comparación u origen de un instrumento externo — p. ej. la Unión Europea en un documento sobre Centroamérica), *sectorial* y *temporal*. Separamos ámbito de referentes porque un campo geográfico único obliga a elegir mal: un documento puede analizar Centroamérica hablando todo el tiempo de la experiencia de la UE.
- **Hallazgos principales**, los 5-7 resultados con cifra y página de referencia.
- **Resumen narrativo**, 3 a 5 oraciones que cuentan el documento. Con una regla anti-relleno: si el resumen podría describir cualquier otro documento del corpus con solo cambiar el título, no sirve. Debe incluir datos y nombres propios verificables.

---

## 4. Las 9 dimensiones analíticas (nivel: apartado)

Es el corazón de la codificación en línea a lo que propone la nota. Cada apartado del documento recibe una o más etiquetas según **qué tipo de contenido aporta**. Las etiquetas no son excluyentes (un mismo apartado suele describir un problema Y explicar su causa), pero cada etiqueta debe sostenerse con una **cita textual literal y su número de página** — esa es la garantía de que se puede auditar.

| #   | Dimensión                     | En una frase                                                                                                                                                                                                                                                                         | Pista para reconocerla                                                                            |
| --- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| 1   | **Estado de situación**       | Describe QUÉ está pasando (impactos, riesgos, vulnerabilidad), sin explicar por qué                                                                                                                                                                                                  | Datos y estadísticas: "los impactos observados son…", "la vulnerabilidad es mayor en…"            |
| 2   | **Diagnóstico estructural**   | Explica POR QUÉ ocurre, atribuyéndolo a factores de fondo (modelo productivo, matriz energética, institucionalidad, desigualdad)                                                                                                                                                     | Conectores causales: "debido a", "esto se explica por", "producto de"                             |
| 3   | **Propuestas de política**    | Recomienda instrumentos o acciones concretas                                                                                                                                                                                                                                         | Verbo prescriptivo + instrumento: "se recomienda crear un fondo…", "es necesario un impuesto al…" |
| 4   | **Avances de implementación** | Algo YA se hizo y tuvo un resultado observable                                                                                                                                                                                                                                       | Pasado + país + resultado: "Chile implementó…", "cinco países ya desarrollan…"                    |
| 5   | **Brechas de implementación** | Falta o falla algo que debería estar. Dos subtipos: **retrospectiva** (se incumplió un compromiso ya asumido: "pese a las NDC, persiste…") y **prospectiva** (no hay preparación para algo que viene: "los países no están listos para el instrumento X que entra en vigor en 2026") | Referencia a un compromiso incumplido, o a un requisito futuro sin preparación                    |
| 6   | **Tendencias**                | Cómo evolucionó algo en el tiempo (2015–2025)                                                                                                                                                                                                                                        | Comparación entre períodos: "ha aumentado", "se consolida…"                                       |
| 7   | **Desafíos**                  | Obstáculo estructural o futuro, sin estar atado a una política puntual ya intentada (eso sería brecha)                                                                                                                                                                               | Dificultad en clave prospectiva/genérica: "coordinar niveles de gobierno sigue siendo complejo"   |
| 8   | **Oportunidades**             | Condición favorable o ventana no explotada, en clave positiva (sin ser todavía una recomendación — eso sería propuesta)                                                                                                                                                              | Verbos de potencial: "permite", "abre la posibilidad de", "podría catalizar"                      |
| 9   | **Contexto / antecedentes**   | Describe un marco o instrumento externo a la región (cómo funciona el sistema europeo de comercio de emisiones, la historia de una institución ajena) que hace falta para entender el resto, sin ser diagnóstico ni propuesta sobre América Latina                                   | Fechas e instituciones extrarregionales, sin mención a países de ALC                              |

Dos aclaraciones útiles para quien codifique a mano:

- Los pares que más se confunden son **estado de situación vs. diagnóstico** (¿describe o explica?) y **avances vs. brechas** (¿se hizo o falta?). En caso de duda, se permite la doble etiqueta — con una cita propia para cada una.
- La dimensión 9 (contexto) nació de la calibración: en el documento sobre el impuesto fronterizo al carbono, 18 páginas aproximadamente sobre el funcionamiento del sistema europeo no calzaban en ninguna categoría. Sin esta etiqueta, ese contenido quedaba invisible.

---

## 5. La interpelación institucional (nivel: documento completo)

La nota conceptual plantea que la CEPAL propone un "gran impulso ambiental" que exige articulación de actores y una narrativa de oportunidad. Nosotros tradujimos ese posicionamiento a **4 preguntas evaluables**, que se le hacen a cada documento completo.

Para el primer criterio no inventamos la definición: la anclamos en el documento donde la propia CEPAL elabora el concepto de gran impulso ambiental — ***Horizontes 2030: la igualdad en el centro del desarrollo sostenible*** (CEPAL, 2016). De ahí derivamos tres pruebas verificables: (a) ¿propone inversión masiva y **coordinada**, no reformas fragmentadas?; (b) ¿aterriza en sectores estratégicos nombrados (transición energética, electromovilidad, bioeconomía, economía circular…) con instrumento identificable?; y (c) ¿conecta la propuesta con al menos dos de las "tres eficiencias" de ese enfoque (la tecnológica/de conocimiento, la de empleo y demanda interna, y la ambiental)?

| #   | Pregunta                                                         | Qué exige un "Sí"                                                                                                                                                                                                                                                                                                                                                   |
| --- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| i   | ¿Promueve el **gran impulso ambiental** con elementos concretos? | Las tres pruebas derivadas de *Horizontes 2030*: paquete coordinado de inversiones/políticas simultáneas (no medidas sueltas), aterrizado en sectores estratégicos nombrados y/o conectado con al menos dos de las tres eficiencias                                                                                                                                 |
| ii  | ¿**Articula actores** mediante un mecanismo concreto?            | Que nombre un mecanismo, plataforma, consejo o proceso de coordinación **con nombre propio** — no basta decir "se requiere la participación de todos los sectores". Y el mecanismo debe pertenecer a la región que el documento analiza (un consejo creado por Corea para dialogar con la UE es un referente interesante, pero no es articulación de Centroamérica) |
| iii | ¿Releva **oportunidades productivas sostenibles**?               | Dos cosas a la vez: que enumere sectores/actividades concretas donde ve la oportunidad, Y que conecte esa enumeración con empleo, productividad o desigualdad con cifras o mecanismos — no una frase de transición                                                                                                                                                  |
| iv  | ¿Propone el **"cómo hacerlo"** de forma concreta?                | Que sus recomendaciones, revisadas **una por una**, sean acciones ejecutables (verbo + objeto específico). No se acredita una lista entera por sus mejores ítems: el veredicto refleja cuántos de los N ítems pasan la prueba ("4 de 8")                                                                                                                            |

Los veredictos son siempre **Sí / Parcial / No** (nunca binarios) y cada uno debe venir acompañado de **citas textuales con página**. Tres reglas de honestidad que nos autoimpusimos tras las rondas de calibración, porque son los errores que efectivamente cometimos y corregimos:

1. **Prohibida la "justificación zombie"**. La llamamos así porque es una justificación que *parece* viva —suena razonable, está bien escrita— pero no dice nada específico. Un ejemplo: *"el documento aborda la sostenibilidad de forma transversal y se alinea con la agenda climática regional"*. Esa frase podría pegarse, sin cambiar una sola palabra, en cualquiera de los 244 documentos del corpus — y una justificación que sirve para todos no justifica a ninguno. El antídoto es simple: sin cita textual literal con número de página, no puede haber "Sí".
2. **La evidencia debe ser la más fuerte del documento, no la más fácil de citar**: en un piloto citamos una frase genérica de "diálogo multiactor" cuando dos páginas antes el documento describía un mecanismo concreto ya adoptado por 5 países.
3. **Los "No" también se demuestran**: un veredicto negativo debe decir qué se buscó y no se encontró ("el documento no menciona empleo, productividad ni desigualdad en ningún pasaje"), no simplemente quedar vacío.

Los 4 criterios se aplican a **todo** documento, incluso a los que no son propuestas de política (estudios econométricos, diagnósticos): un "No" en esos casos es información válida sobre el corpus —describe la naturaleza del documento—, no un error, y así se deja anotado.

---

## 6. La tipología (nivel: documento completo)

Cada documento se clasifica según qué **transformación estructural** persigue, usando el canon de las **11 Grandes Transformaciones** que el Lab ya usó para clasificar 495 publicaciones de la CEPAL en un proyecto anterior (Desafío CEPAL). Reusar ese canon —en vez de inventar una taxonomía nueva solo para este corpus— hace que ambas clasificaciones sean comparables.

Las 11 son:  (1) Desarrollo productivo, (2) Reducción de la desigualdad, (3) Protección social, (4) Educación, (5) Igualdad de género, (6) **Sostenibilidad ambiental**, (7) Transformación digital, (8) Migración, (9) Integración económica, (10) Macroeconomía y fiscalidad, (11) Capacidades del Estado.

Cada documento recibe una transformación **primaria** y una **secundaria** (obligatoria: asumimos que todo documento institucional de la CEPAL tiene una segunda intención transformadora), cada una con un nivel de **certeza** (Alta/Media/Baja). La pregunta clave no es "¿de qué habla el documento?" sino "¿**qué pretende transformar**?" — un documento puede hablar todo el tiempo de comercio y ser, en el fondo, un documento sobre preparación climática (o viceversa; ese caso existe en la muestra y lo dejamos marcado como ambiguo para ustedes, ver ejemplo 3).

Obviamente casi todo el corpus climático mapeará a #6 como primaria. El valor analítico de la tipología es doble:

- **Detectar cuándo no** es así (¿es en realidad un documento de financiamiento → #10? ¿de comercio → #9? ¿de desigualdad → #2?), lo que revela desde qué agenda está pensando la institución cada aspecto del problema climático.
- **Mapear la interdependencia entre agendas**. El par primaria y secundaria de cada documento, agregado sobre los 244, permitirá dibujar cómo se entrelazan las transformaciones:  clima ↔ desigualdad, clima ↔ comercio, clima ↔ capacidades del Estado, etc. Consideramos que esto es central cuando se habla de problemas complejos donde se asume que las brechas no viven aisladas, y saber qué combinaciones aparecen (y cuáles nunca aparecen) en el pensamiento institucional es en sí mismo un hallazgo sobre cómo la CEPAL entiende (o tal vez todavía no entiende) esas interdependencias.

---

## 7. Las 14 publicaciones de calibración

| #   | Publicación                                                                                                                | Año  | Enlace                               |
| --- | -------------------------------------------------------------------------------------------------------------------------- | ---- | ------------------------------------ |
| 1   | Efectos del cambio climático en la costa de América Latina y el Caribe: dinámicas, tendencias y variabilidad climática     | 2015 | <https://hdl.handle.net/11362/3955>  |
| 2   | Ocho tesis sobre el cambio climático y el desarrollo sostenible en América Latina                                          | 2015 | <https://hdl.handle.net/11362/39840> |
| 3   | The rise of green bonds: Financing for development in Latin America and the Caribbean                                      | 2017 | <https://hdl.handle.net/11362/42230> |
| 4   | Economía del Cambio Climático en Honduras: documento técnico 2017                                                          | 2017 | <https://hdl.handle.net/11362/42355> |
| 5   | Informe anual sobre el progreso y los desafíos regionales de la Agenda 2030 en América Latina y el Caribe                  | 2017 | <https://hdl.handle.net/11362/41173> |
| 6   | La tragedia ambiental de América Latina y el Caribe                                                                        | 2020 | <https://hdl.handle.net/11362/46101> |
| 7   | Cuarto informe sobre financiamiento para el cambio climático en América Latina y el Caribe, 2013-2016                      | 2019 | <https://hdl.handle.net/11362/44487> |
| 8   | Reflexiones sobre la gestión del agua en América Latina y el Caribe. Textos seleccionados 2002-2020                        | 2021 | <https://hdl.handle.net/11362/46792> |
| 9   | Building a climate resilient power sector in the context of the Caribbean SIDS' energy transition. Policy Brief            | 2022 | <https://hdl.handle.net/11362/48603> |
| 10  | Una década de acción para un cambio de época. Quinto informe sobre el progreso y los desafíos regionales de la Agenda 2030 | 2022 | <https://hdl.handle.net/11362/47745> |
| 11  | El impacto del cambio climático en la pobreza infantil y juvenil de América Latina                                         | 2025 | <https://hdl.handle.net/11362/82426> |
| 12  | Acción climática en la agricultura: la experiencia de países miembros de la PLACA                                          | 2023 | <https://hdl.handle.net/11362/48724> |
| 13  | Comercio, cambio climático y el impuesto fronterizo al carbono                                                             | 2023 | <https://hdl.handle.net/11362/68639> |
| 14  | América Latina y el Caribe ante las trampas del desarrollo: transformaciones indispensables y cómo gestionarlas            | 2024 | <https://hdl.handle.net/11362/80727> |

**¿Por qué estas 14?** No son una muestra aleatoria: están elegidas para **estresar la metodología** en todas las direcciones en que el corpus completo varía.

- **Cubren los tres períodos** del análisis: 2015–2018 (5 documentos), 2019–2022 (5) y 2023–2026 (4) — para verificar que las dimensiones funcionan igual sobre la literatura pre-Acuerdo de París que sobre la más reciente.
- **Cubren las divisiones y sedes** que más publican en el tema: Desarrollo Sostenible, Desarrollo Económico, Recursos Naturales, la sede subregional de México, la de Puerto España (Caribe) y la Secretaría Ejecutiva.
- **Cubren los géneros documentales**: policy briefs cortos, estudios técnicos largos con anexos, informes de financiamiento, compilaciones, e informes insignia institucionales. Si la metodología funciona en un brief de 12 páginas y en un documento de proyecto de 105, funcionará en el medio.
- **Cubren los ejes temáticos** con los que la tipología y la interpelación deben lidiar: energía, comercio, financiamiento, agua, agricultura, costas, pobreza y desigualdad.
- Once vienen del corpus original filtrado por tema; **tres (5, 10 y 14) son documentos institucionales estratégicos** incorporados al corpus en la Etapa 2 porque, aunque el cambio climático no es su tema exclusivo, expresan la posición oficial de la CEPAL — exactamente el tipo de documento donde la interpelación institucional más importa.

De estas 14, tres ya fueron procesadas de punta a punta como piloto (las número 9, 11 y 13 — elegidas por ser deliberadamente opuestas entre sí: un brief corto de energía, un estudio econométrico de pobreza de extensión media, y un documento largo de comercio). Son los ejemplos de la sección siguiente. Las 11 restantes se procesarán una vez que ustedes validen el enfoque.

---

## 8. Tres ejemplos: así se ve el resultado

Para cada piloto mostramos aquí lo esencial: la ficha, la tipología, los 4 veredictos de interpelación y **una muestra** de la extracción por apartado (algunos apartados y algunas de sus etiquetas, elegidos por ser ilustrativos, no constituyen la extracción completa). La ficha completa de cada documento con todos sus apartados, todas las citas y los razonamientos íntegros está en su anexo correspondiente:

- **Anexo 1**,  Policy brief del Caribe (doc. 9)
- **Anexo 2**,  Estudio de pobreza infantil UNICEF-CEPAL (doc. 11)
- **Anexo 3**,  Documento sobre el impuesto fronterizo al carbono (doc. 13)

**Los invitamos a auditar cualquier cita contra el PDF: cada una lleva su página.**



### Ejemplo 1 — Policy brief corto (doc. 9 de la muestra)

*Building a climate resilient power sector in the context of the Caribbean SIDS' energy transition* (2022, 12 páginas) — <https://hdl.handle.net/11362/48603>

| Ficha                      |                                                                                                                                                                                                                                              |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tipo de documento          | Policy Brief (sede subregional del Caribe)                                                                                                                                                                                                   |
| Páginas (cuerpo / totales) | 10 / 12                                                                                                                                                                                                                                      |
| Ámbito de aplicación       | SIDS del Caribe, con CARICOM como marco institucional                                                                                                                                                                                        |
| Referentes/dependencias    | EE.UU. (comparación de tarifas), Puerto Rico (caso ilustrativo), IEA/IRENA/Banco Mundial (fuentes)                                                                                                                                           |
| Pregunta que responde      | ¿Cómo incorporar resiliencia climática en la planificación eléctrica de los SIDS del Caribe durante su transición renovable?                                                                                                                 |
| Tipología                  | Primaria: **#6 Sostenibilidad ambiental** (certeza alta) · Secundaria: **#11 Capacidades del Estado** (alta) — el sujeto es la energía, pero las recomendaciones concretas son de capacidad institucional (datos, planificación, regulación) |

**Interpelación** (documento completo):

| Criterio                  | Veredicto   | Por qué (resumido)                                                                                                                                                                                                                 |
| ------------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Gran impulso ambiental    | **Parcial** | Nombra instrumentos concretos (IRRP, actualización de metas renovables, reforma, regulatoria) pero todo dentro de un solo sector,  no hay paquete coordinado de inversiones a escala de modelo de desarrollo                       |
| Articulación de actores   | **Sí**      | Mecanismo con nombre propio y del propio ámbito: el Integrated Resource and Resilience Plan (IRRP), avalado por CARICOM y ya en desarrollo en 5 países con apoyo del CCREEE (p.6)                                                  |
| Oportunidades productivas | **No**      | Chequeo negativo explícito: en las 12 páginas no aparece ninguna enumeración de sectores como oportunidad económica; las palabras empleo, productividad y desigualdad no figuran en el texto                                       |
| "Cómo hacerlo" concreto   | **Sí**      | 8 recomendaciones revisadas una por una: **6 de 8** pasan la prueba de concreción (p. ej. "mapear las necesidades eléctricas de la infraestructura crítica: hospitales, telecomunicaciones, agua…"); 2 quedan en principio general |

**Muestra de la extracción por apartado** (2 de los 5 apartados del documento; la extracción completa está en el Anexo 1):

| Apartado (páginas)                                                     | Dimensión                                | Cita que la sostiene (página)                                                                                                                                                             |
| ---------------------------------------------------------------------- | ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Introduction / Background (1-3)                                        | Estado de situación                      | "plants fuelled by oil and natural gas represented the highest share of electricity installed capacity in the subregion in 2021, with renewables accounting for just 18.7 per cent" (p.2) |
| Introduction / Background (1-3)                                        | Brecha de implementación — retrospectiva | "Targets set by Trinidad and Tobago and Saint Vincent and the Grenadines have expired in 2021 and 2020 respectively and have not yet been updated" (p.2)                                  |
| Incorporating resilience requirements into power sector planning (6-7) | Propuesta de política                    | "CARICOM member States endorsed the IRRP as a preferred mechanism to guide planning in the electricity sector" (p.6)                                                                      |
| Incorporating resilience requirements… (6-7)                           | Avance de implementación                 | "Belize, Guyana, Jamaica, Saint Kitts and Nevis, and Trinidad and Tobago have already engaged with the CCREEE Climate Resilience Programme to develop IRRPs" (p.6)                        |

### Ejemplo 2 — Estudio econométrico de extensión media (doc. 11 de la muestra)

*El impacto del cambio climático en la pobreza infantil y juvenil de América Latina* (UNICEF-CEPAL, 2025, 62 páginas) — <https://hdl.handle.net/11362/82426>

Este caso muestra algo importante: **la metodología también funciona con documentos que no son propuestas de política**. Es un estudio de modelización (clima → PIB → pobreza) y sus veredictos "No" describen fielmente esa naturaleza — no son un error.

| Ficha                      |                                                                                                                                                                                                                                                                            |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tipo de documento          | Estudio técnico (modelización econométrica interinstitucional)                                                                                                                                                                                                             |
| Páginas (cuerpo / totales) | 43 / 62                                                                                                                                                                                                                                                                    |
| Ámbito de aplicación       | 18 países de América Latina (~95% de la población regional)                                                                                                                                                                                                                |
| Referentes/dependencias    | Escenarios NGFS, modelo NiGEM/CLIMADA, líneas de pobreza del Banco Mundial — insumos metodológicos, no sujetos de análisis                                                                                                                                                 |
| Pregunta que responde      | ¿Cuánta pobreza infantil y juvenil adicional generará el cambio climático hacia 2030, según el escenario global de emisiones y la trayectoria de desigualdad?                                                                                                              |
| Hallazgo central           | Incluso con mitigación ambiciosa (Net Zero 2050): 5,9 millones de niños/as y jóvenes adicionales en pobreza a 2030; hasta 27,5 millones con inacción climática y Gini en deterioro                                                                                         |
| Tipología                  | Primaria: **#2 Reducción de la desigualdad** (alta) · Secundaria: **#6 Sostenibilidad ambiental** (alta) — el clima entra como *canal causal* del problema distributivo, no como objeto de política. Es el ejemplo de que "hablar de clima" no ancla automáticamente en #6 |

**Interpelación**:

| Criterio                  | Veredicto   | Por qué (resumido)                                                                                                                                                                                                                               |
| ------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Gran impulso ambiental    | **No**      | El documento no propone transformación productiva alguna: delega explícitamente la mitigación en los grandes emisores globales (ALC emite <10% de los GEI, p.34). El "No" es por diseño del documento, y así queda anotado                       |
| Articulación de actores   | **Parcial** | Nombra con detalle *quiénes* deberían coordinarse (ministerios, fondos multilaterales, sector privado, p.42) pero ningún mecanismo de coordinación con nombre propio                                                                             |
| Oportunidades productivas | **No**      | Todo el contenido económico cuantifica pérdidas y costos; el empleo aparece como canal de daño, nunca como oportunidad. Chequeo negativo documentado sección por sección                                                                         |
| "Cómo hacerlo" concreto   | **Parcial** | Sus 4 áreas de política se desglosan en 11 ítems: **7 de 11** pasan la prueba de concreción, pero varios son limítrofes (sin actor, plazo ni métrica) — se fijó "Parcial" como decisión conservadora y se dejó marcado para discutir con ustedes |

**Muestra de la extracción por apartado** (una selección; la ficha completa del Anexo 2 cubre los 10 apartados del documento):

| Apartado (páginas)                                                            | Dimensión               | Cita que la sostiene (página)                                                                                                                                                                                          |
| ----------------------------------------------------------------------------- | ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Introducción (5-17)                                                        | Estado de situación     | "en la región unos 94 millones de niños, niñas, adolescentes y jóvenes son pobres (es decir, el 52 por ciento del total de pobres)" (p.9)                                                                              |
| 1. Introducción (5-17)                                                        | Diagnóstico estructural | "la efectividad de las políticas redistributivas se ve limitada por la estructura fiscal, enfocada principalmente en impuestos indirectos" (p.14)                                                                      |
| 3.2. El impacto del cambio climático en la pobreza infantil y juvenil (34-38) | Estado de situación     | "En el escenario Net Zero 2050, se estima que, en 2030, 5.9 millones adicionales de niños, niñas, adolescentes y jóvenes, aproximadamente, podrían encontrarse en situación de pobreza por el cambio climático" (p.34) |
| 4. Conclusiones y recomendaciones (39-43)                                     | Propuesta de política   | "se pueden identificar cuatro grandes áreas de políticas para mitigar los efectos del cambio climático en la pobreza infantil y juvenil" (p.41)                                                                        |

### Ejemplo 3 — Documento largo de comercio (doc. 13 de la muestra)

*Comercio, cambio climático y el impuesto fronterizo al carbono* (2023, 105 páginas) — <https://hdl.handle.net/11362/68639>

El caso de estrés: largo, con anexos, con cambio constante de universo geográfico (la UE regula, la subregión se analiza, Corea y Chile aparecen como referentes). Aquí nacieron varias reglas de la metodología — incluida la dimensión "contexto/antecedentes" (sus capítulos I y II, ~18 páginas sobre el sistema europeo, no calzaban en ninguna otra) y la regla de que un mecanismo extrarregional no acredita articulación regional.

| Ficha                      |                                                                                                                                                                                                                                                                                                                    |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Tipo de documento          | Documento de proyecto / estudio técnico (sede subregional de México)                                                                                                                                                                                                                                               |
| Páginas (cuerpo / totales) | 80 / 105                                                                                                                                                                                                                                                                                                           |
| Ámbito de aplicación       | 10 países: Centroamérica, México, Cuba, Haití y República Dominicana                                                                                                                                                                                                                                               |
| Referentes/dependencias    | Unión Europea (sujeto regulador del CBAM), Corea/Canadá/Japón (diálogos con la UE), EE.UU. y China (socios dominantes), Chile (pionero en impuesto al carbono)                                                                                                                                                     |
| Pregunta que responde      | ¿Qué impacto tiene el mecanismo de ajuste en frontera por carbono (CBAM) de la UE sobre la subregión, y qué tan preparada está para este tipo de instrumentos?                                                                                                                                                     |
| Hallazgo central           | Impacto inmediato mínimo (los sectores CBAM son el 0,09% de las exportaciones subregionales a la UE), pero el riesgo real es prospectivo: la expansión del instrumento y su posible adopción por EE.UU. (destino del 74% de las exportaciones)                                                                     |
| Tipología                  | Primaria: **#6 Sostenibilidad ambiental** · Secundaria: **#9 Integración económica** — **ambas con certeza BAJA**. Es un caso genuinamente ambiguo que dejamos sin resolver a propósito: podría defenderse #9 como primaria con igual fuerza. **Es la pregunta abierta que más nos interesa discutir con ustedes** |

**Interpelación**:

| Criterio                  | Veredicto   | Por qué (resumido)                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Gran impulso ambiental    | **Parcial** | Nombra instrumentos fiscales concretos (impuestos al carbono, eliminación de subsidios, bonos verdes) pero como medidas sueltas de preparación ante un instrumento ajeno — no un paquete coordinado propio                                                                                                                                                                                             |
| Articulación de actores   | **Parcial** | Los únicos mecanismos con nombre propio (Consejo de Acero del CBAM, Grupo Asesor de Comercio de Carbono) son instancias **de Corea** para su diálogo con la UE — referentes, no articulación de la subregión, que solo registra "interés expresado" por México. *Este veredicto fue corregido de "Sí" a "Parcial" en la revisión humana: es el mejor ejemplo de por qué las reglas estrictas importan* |
| Oportunidades productivas | **Sí**      | Enumera 4 oportunidades concretas (empleo verde con cifras OIT: +100.000 en renovables, +540.000 en construcción; servicios de medición de emisiones; blockchain; coprocesamiento cementero CANACEM) y desarrolla el vínculo con empleo y brecha de género en varias páginas con datos propios                                                                                                         |
| "Cómo hacerlo" concreto   | **Parcial** | De sus 8 puntos de acción, exactamente **4 de 8** pasan la prueba de concreción. No se acredita la lista por sus mejores ítems (blockchain, CANACEM): eso es precisamente el error que la regla evita                                                                                                                                                                                                  |

**Muestra de la extracción por apartado** (una selección de los 12 apartados; nótese la dimensión "contexto" y la brecha prospectiva, ambas nacidas de este documento — la extracción completa está en el Anexo 3):

| Apartado (páginas)                                      | Dimensión                                  | Cita que la sostiene (página)                                                                                                                                                                       |
| ------------------------------------------------------- | ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Introducción (13-14)                                    | Brecha de implementación — **prospectiva** | "los países de la subregión no están bien preparados para este cambio, ni otros relacionados con el cambio climático" (p.13)                                                                        |
| I. El sistema de comercio de emisiones de la UE (15-18) | **Contexto/antecedentes**                  | "el sistema de comercio de derechos de emisión de la UE es el primer y hasta ahora el mayor sistema de tope y comercio (cap-and-trade) a nivel de instalación del mundo" (p.15)                     |
| III.B.2 Comercio de bienes con la UE (38-51)            | Estado de situación                        | "la exportación de los sectores del mecanismo de ajuste en frontera por carbono a la UE representó un promedio de 0,011% en relación con las exportaciones totales de la subregión al mundo" (p.38) |
| III.B.3 Estado de preparación subregional (52-66)       | Brecha de implementación — prospectiva     | "en 2021, los países de la subregión invirtieron alrededor de 55.400 millones de dólares en subsidios energéticos (…), lo que equivale en promedio al 3% del PIB de la subregión" (p.60)            |
| IV. Implicaciones y recomendaciones (73-78)             | Avance de implementación                   | "En 2023, CANACEM anunció un Plan de Acción actualizado hacia una Economía Baja en Carbono… reducir las emisiones de GEI provenientes de la industria del cemento 17% en 2030" (p.76)               |

---

## 9. Qué les pedimos (y cómo pueden validar)

La división de trabajo que propusimos desde el inicio: el **Lab** aporta el pipeline técnico de extracción, su calibración y propuesta de elementos a extraer del texto; el **equipo del curso** aporta la precisión conceptual de las categorías y la validación de contenido. Concretamente, tres formas de participar, de menor a mayor esfuerzo:

1. **Revisar las definiciones** de este documento: ¿las 9 dimensiones capturan lo que ustedes necesitan para responder las preguntas de la nota conceptual? ¿Los 4 criterios de interpelación traducen bien el posicionamiento institucional? ¿Falta o sobra alguna categoría? En particular, la taxonomía de "tipo de instrumento" (planificación / regulación / financiamiento / gobernanza / información-monitoreo) es la que más necesita su criterio experto.
2. **Auditar los 3 ejemplos**: tomar cualquiera de los veredictos o citas de la sección 8 (o de los anexos completos), abrir el PDF en la página indicada y verificar si están de acuerdo. Cada discrepancia que encuentren es exactamente el insumo que la calibración necesita.
3. **Codificar a mano 1 o 2 de los 14 documentos** (idealmente alguno que no sea de los 3 piloto), usando las definiciones de este documento: leer, etiquetar sus apartados, emitir los 4 veredictos y clasificar la tipología. Comparar su lectura con la nuestra en una reunión es la mejor prueba posible de que las reglas son operativas — si dos lectores razonables llegan a resultados distintos, la regla se afina, no el lector.

Y una pregunta específica que dejamos abierta a propósito porque requiere juicio de dominio, no técnica: **la tipología del documento 13** (¿es primariamente un documento de sostenibilidad ambiental o de integración económica?).

---

## 10. Próximos pasos

| Paso | Qué                                                                                                                                         | Quién            |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| 1    | Revisión de esta nota, las definiciones y los 3 ejemplos                                                                                    | Equipo del curso |
| 2    | (Opcional pero muy valioso) Codificación manual independiente de 1-2 documentos de la muestra                                               | Equipo del curso |
| 3    | Reunión de calibración: comparar lecturas, afinar definiciones y cerrar las preguntas abiertas                                              | Ambos            |
| 4    | Procesar los 11 documentos restantes de la muestra con la metodología ajustada, con verificación cruzada de los veredictos de interpelación | Lab              |
| 5    | Segunda revisión rápida sobre la muestra completa de 14                                                                                     | Ambos            |
| 6    | Escalar al corpus completo de 244 documentos y construir los agregados por dimensión, período, división y pregunta de investigación         | Lab              |

**¿Y para qué sirve todo esto al final?** Cuando la metodología calibrada esté aplicada a los 244 documentos, el resultado ya no será una colección de PDFs sino un **corpus estructurado y consultable**: cada afirmación etiquetada, con su cita, su página, su documento y sus variables. Sobre esa base se construyen directamente las etapas finales previstas en la nota conceptual: **responder las preguntas de investigación** (cada pregunta se traduce en combinaciones de dimensiones, variables y filtros sobre el corpus), elaborar la **síntesis** solicitada (los resúmenes narrativos y hallazgos por documento son su insumo directo), y analizar las **tendencias temáticas por bloques de años** (2015–2018, 2019–2022, 2023–2026), por división, por país y por tipo de instrumento — es decir, cómo ha evolucionado el pensamiento de la CEPAL sobre el cambio climático a lo largo de la década.



---

*CEPAL Lab · Laboratorio de Innovación de la CEPAL/ILPES — julio de 2026. Los anexos 1 a 3 (fichas completas de los tres documentos piloto) acompañan a esta nota. Los documentos técnicos de la metodología están versionados en el repositorio del proyecto y disponibles a pedido.*
