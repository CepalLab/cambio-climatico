# Evaluación multimodelo/multiharness — doc09 (5 corridas)

**Fecha**: 2026-07-13
**Estado**: registro de evaluación (bitácora de la prueba de portabilidad). **Este documento NO es parte de
la metodología del pipeline** — no se lee como insumo para correr el pipeline sobre ningún documento (los
insumos son los 5 documentos listados al inicio de [../GUIA_OPERATIVA_PIPELINE.md](../GUIA_OPERATIVA_PIPELINE.md)).
Es el equivalente, para la pregunta de portabilidad, de lo que la bitácora de
[../PLAN_ANALISIS_PROFUNDO.md](../PLAN_ANALISIS_PROFUNDO.md) es para la calibración metodológica: registra
qué se observó y qué se propone cambiar, con el razonamiento completo.
**Qué ejecuta**: el [protocolo de prueba de portabilidad de harness/modelo](../GUIA_OPERATIVA_PIPELINE.md#protocolo-de-prueba-de-portabilidad-de-harnessmodelo)
(Ronda 4), que estaba pendiente como próximo paso 3.5 de PLAN_ANALISIS_PROFUNDO.md §5 — extendido de 1
corrida nueva a 4, más la referencia calibrada.
**Evaluador**: Claude Code (Claude Fable 5), con verificación factual contra el texto fuente del PDF y
ejecución de `validar_esquema.py` sobre los 5 artefactos. Los veredictos de esta evaluación son juicio de
un modelo evaluador, no revisión humana — mismo estatus provisional que el resto del piloto.

## 0. Los 5 casos

Los 5 JSON (`doc09_caribbean_power_01.json` … `_05.json`) son corridas del pipeline completo (Etapas 1-5)
sobre el mismo insumo (doc09, *Building a climate resilient power sector...*, LC/CAR/2022/6, 12 páginas),
producidas con distintos modelos/harnesses.

| Caso | Archivo | Modelo | Harness | Observación |
| ---- | ------- | ------ | ------- | ----------- |
| 01 | `doc09_caribbean_power_01.json` | Claude Sonnet | Claude Code | **Referencia calibrada** — verificado byte-idéntico al `doc09_caribbean_power.json` calibrado en Rondas 1-4 y commiteado en `e042f7d`. No es una corrida ciega nueva: es la respuesta de referencia del protocolo. |
| 02 | `doc09_caribbean_power_02.json` | GPT-5.5 | Codex | Corrida nueva |
| 03 | `doc09_caribbean_power_03.json` | Gemini | gemini-cli | Corrida nueva |
| 04 | `doc09_caribbean_power_04.json` | DeepSeek | OpenCode | Corrida nueva |
| 05 | `doc09_caribbean_power_05.json` | MiMo | OpenCode | Corrida nueva |

**La evaluación se hizo a ciegas por diseño**: el operador retuvo deliberadamente el mapeo caso →
modelo/harness hasta después de cerrada la evaluación comparada (secciones 1-5), para evitar sesgo de marca
en el evaluador. El mapeo se agregó post-hoc el mismo 2026-07-13. Las secciones 1-5 se conservan tal como se
escribieron a ciegas; la lectura con el mapeo revelado va en la subsección siguiente.

### 0.1 Lectura post-hoc con el mapeo revelado

- **Los casos 04 y 05 comparten harness (OpenCode) y divergen fuerte en calidad de juicio** — DeepSeek
  quedó 2º del ranking (el mejor de los nuevos) y MiMo 4º, con el único fallo de checkpoint duro (criterio
  ii). Con el harness constante, esa divergencia es atribuible al modelo: confirma que la disciplina de
  juicio calibrada es la capacidad que separa modelos, tal como anticipaba el punto 2 del protocolo.
- **El caso 02 (GPT-5.5/Codex) perdió tildes y eñes**: la degradación de encoding ocurre en la capa
  modelo+harness de serialización, no en la metodología — refuerza que el chequeo de encoding propuesto
  para `validar_esquema.py` (propuesta 4) debe correr siempre, sea cual sea el proveedor.
- **El caso 03 (Gemini/gemini-cli) concentra los errores de la capa de extracción** (alcance temporal
  contaminado por el artefacto de maqueta "January 1, 2018"; test de concreción corrido sobre el recuadro
  de portada): consistente con una lectura de PDF del harness que mezcla elementos de maqueta con el cuerpo.
  Es exactamente lo que el Paso 3 del protocolo (chequeo de extracción, bloqueante) debía atrapar antes de
  evaluar juicio — en corridas futuras con gemini-cli, no saltárselo.
- **Caveat de alcance**: n=1 corrida por modelo. Esto rankea *corridas*, no modelos — para afirmar algo
  sobre un modelo/harness harían falta repeticiones (la variación intra-modelo entre corridas no está
  medida). Útil como señal direccional para elegir con qué escalar, no como benchmark.

**Validación estructural**: los 5 pasan `validar_esquema.py` (estructura base OK). Única observación del
validador: el caso 01 menciona la tabla de anclas — la excepción permitida por la regla transversal 3 del
esquema, correctamente flaggeada como heurística. Conclusión: **el esquema v1 se transfiere bien; la
divergencia entre casos no está en la forma sino en el juicio y en la capa de extracción.**

## 1. Convergencias — el núcleo robusto del pipeline

- **Tipología: convergencia perfecta (5/5).** Primaria #6 Sostenibilidad ambiental / secundaria #11
  Capacidades del Estado, certeza "Alta" en ambas, en los 5 casos. El sistema de anclas + protocolo de 5
  pasos es agnóstico al modelo.
- **Criterio (i) gran impulso: Parcial (5/5)**, todos con el argumento correcto (instrumento concreto pero
  sectorial, sin lógica de paquete coordinado).
- **Criterio (iii) oportunidades productivas: No (5/5), todos con chequeo negativo explícito** conforme a
  INTERPELACION_v0 §1.3.
- **Metadatos duros idénticos** (handle, símbolo, fecha, idioma, 10/12 páginas).
- **Evidencia central compartida**: los 5 identifican el IRRP/CARICOM/CCREEE (p.6) como el hecho
  institucional clave y citan las mismas cifras verificables (18,7% renovables, US$0,33/kWh, María/Dominica
  4 meses).

Patrón general: **donde la calibración convirtió una falla en regla escrita + ejemplo resuelto, los 5
modelos convergen. Donde quedó un umbral sin ejemplos, divergen.**

## 2. Divergencias

| Elemento | 01 (ref.) | 02 | 03 | 04 | 05 |
|---|---|---|---|---|---|
| (i) Gran impulso | Parcial | Parcial | Parcial | Parcial | Parcial |
| (ii) Articulación | **Sí** (IRRP) | Sí | Sí | Sí | **Parcial** ⚠ |
| (iii) Oportunidades | No | No | No | No | No |
| (iv) Cómo hacerlo | Sí, 6/8 | Sí, 6/8 | Sí, 7/8 | **Parcial, 4/8** ⚠ | Sí, 7/8 |
| Secciones nivel 1 capturadas | 5 (fusiona) | 7 | 7 | 7 | 7 |
| `brechas_implementacion` detectada | ✔ (retrospectiva) | ✔ (retrospectiva) | ✘ | ✘ | ✘ |
| `tiene_resumen_ejecutivo` | false ✔ | **true** ✘ | **true** ✘ | false ✔ | false ✔ |

### 2.1 Criterio (iv) — la métrica más inestable del pipeline

El tally va de **4/8 a 7/8 con las mismas reglas escritas**, y en el caso 04 eso cambia el veredicto a
"Parcial". Más fino: 01 y 02 llegan al mismo tally (6/8) **con ítems distintos** — 02 marca CONCRETO el
"mainstreaming" (que 01 marca GENERICO) y GENERICO el "scale up renovables" (que 01 marca CONCRETO). El
único consenso 5/5 es que *"Promote a collaborative multiple-stakeholder approach"* es GENERICO. Ítems
frontera (al menos un voto disidente cada uno): *mainstream resilience*, *strengthen capacities*, *scale up
renewables*, *review and update policies*. El test "verbo + objeto específico" tiene vaguedad residual real:
¿"strengthen human and institutional capacities to collect... energy statistics" tiene objeto específico
(las estadísticas) o es "fortalecer capacidades" con adorno? Ambas lecturas son defendibles con la regla
vigente.

Además, el **caso 03 corrió el test sobre la unidad equivocada**: su `desglose_items` lleva `"pagina": 1`
porque evaluó los bullets abreviados del recuadro "Key recommendations" de la portada, no el texto completo
de las recomendaciones en p.9-10. Los bullets abreviados pierden justo el objeto específico que hace pasar
o fallar el test. Modo de falla nuevo, no documentado en ninguna ronda previa.

### 2.2 Criterio (ii) — el caso 05 falla el checkpoint duro del protocolo

El caso 05 encuentra el IRRP pero razona que "es un mecanismo de planificación, no de articulación de
actores" y baja el veredicto a Parcial. No es el error de Ronda 2 (citar la evidencia genérica de p.9 por
ser la más fácil); es una **interpretación alternativa defendible que la regla §1.2 no cierra**: un plan de
planificación multiactor con nombre propio queda en zona gris para un modelo que no vio la calibración. Los
otros 4 casos resolvieron conforme a la referencia.

### 2.3 Capa de extracción y metadatos — errores de harness, no de juicio

- **Caso 02 perdió todas las tildes y eñes** en el cuerpo ("pequenos Estados", "planificacion") — encoding
  del harness al serializar. A escala de 244 contamina cualquier análisis textual agregado.
- **Caso 03 reporta alcance temporal "2018-2022"**: casi con certeza contaminado por el artefacto de maqueta
  "January 1, 2018" que la extracción del PDF intercala en la página 1 (verificado en el `.txt`, presente
  también en la extracción nativa). Es exactamente el riesgo de extracción que la guía documenta como no
  resuelto (PLAN §1.4).
- **Caso 05 alucina "Unión Europea" como referente** en `referentes_dependencias` — no aparece en ninguna
  parte del texto (verificado con búsqueda literal). También traduce *tariffs* como "aranceles" (son
  tarifas eléctricas, no aranceles comerciales).
- **`tiene_resumen_ejecutivo`**: 02 y 03 dicen `true`; el documento no tiene abstract ni resumen ejecutivo
  (verificado). Probablemente interpretaron el recuadro "Key recommendations" de portada como tal. La regla
  actual no define el caso.
- **% de combustibles fósiles**: 01 dice 79,5% (suma correcta de la torta de p.3: oil 47,8 + gas 20,7 +
  carbón/turba 5,7 + fósiles n.e.s. 5,3); 04 dice 81,3% (suma además "other non-renewable" 1,7%, que no es
  fósil en sentido estricto). Ninguna cifra está literal en el texto — ambos computaron; 01 computó mejor.
  El esquema no tiene política para cifras computadas vs. literales.

### 2.4 Profundidad de las Etapas 2-3

- **Secciones**: el documento tiene 7 encabezados de nivel 1 (verificado contra el texto: Introduction,
  Background, Multi-hazard risks, Incorporating resilience, Technologies, Policy recommendations,
  Conclusion). Los casos 02-05 capturan los 7; **el 01 (la referencia) fusiona en 5** ("Introduction /
  Background" y "Policy recommendations / Conclusion"). Hallazgo incómodo pero útil: la referencia calibrada
  viola la letra de su propia regla ("todas las secciones de nivel 1, sin excepciones") — los cuatro modelos
  nuevos fueron más fieles al esquema que el original. *Resuelto el mismo día*: el JSON canónico se corrigió
  a 7 secciones (ver tabla de decisiones de Ronda 5 en la bitácora); `_01` conserva la versión previa como
  artefacto de la prueba a ciegas.
- **Calidad de resúmenes**: 01 claramente superior (largo proporcional, función argumental, cifras y
  actores — cumple la regla de calidad de Ronda 3 al pie). 04 y 02 buenos. 05 intermedio. **03 muy por
  debajo del piso**: resúmenes de 1-2 líneas que enuncian temas sin función ni cifras; su
  `resumen_narrativo` también es el más genérico de los cinco, y el del 05 tiene 2 oraciones (bajo el piso
  de 3-5).
- **Cobertura de dimensiones**: solo 01 y 02 detectan la `brechas_implementacion` retrospectiva (metas
  renovables vencidas de Trinidad y Tabago / San Vicente, p.2 y p.10). 03, 04 y 05 la pierden. Es la
  dimensión más sutil del codebook y la única con subtipo; perderla sistemáticamente sesga el agregado.

## 3. Ranking

1. **Caso 01 (referencia)** — el más cercano al resultado esperado, como corresponde a su origen. Único que
   corre los tests nombrados de la metodología de forma trazable (tests 1-3 del §1.5 uno por uno,
   verificación de ámbito del §1.2, guardrail anti-genérico explícito). Única debilidad real: la fusión de
   secciones (2.4).
2. **Caso 04** — el mejor de los cuatro nuevos: justificación anti-copia rica, chequeos negativos
   impecables, tests de big_push citados explícitamente. Su desviación es de umbral, no de método: aplicó
   el test de concreción con más severidad que la calibración (4/8 → Parcial). Es el tipo de desacuerdo que
   un ejemplo resuelto elimina.
3. **Caso 02** — juicio correcto en los 4 criterios y único nuevo que captura la brecha retrospectiva, pero
   arrastra fallas de capa de harness (encoding sin tildes, `tiene_resumen_ejecutivo` erróneo, título
   recortado), y sus clasificaciones ítem a ítem del (iv) están cruzadas respecto de la referencia aunque
   el tally coincida.
4. **Caso 05** — débil en **juicio**: falla el checkpoint (ii) del protocolo, alucina un referente, resumen
   narrativo bajo el piso, páginas imprecisas en el desglose.
5. **Caso 03** — débil en **profundidad**: veredictos finales casi todos correctos, pero resúmenes de
   sección bajo el estándar, dimensiones ralas (una sección con `[]`), test de concreción corrido sobre la
   portada, campo temporal contaminado por artefacto de extracción.

03 y 05 empatan abajo por razones distintas: 03 falla en las Etapas 2-3 (daña el agregado del codebook), 05
falla en la Etapa 4 (daña la interpelación). Cuál pesa más depende del uso final; para la síntesis de
posición institucional, el error de juicio del 05 es más grave; para la estadística por dimensión, el del 03.

**Decisión según el Paso 6 del protocolo**: ninguno de los 4 nuevos falla 2+ de los 3 checkpoints de juicio
(solo 05 falla 1) — técnicamente todos serían "portables con confianza moderada". **Pero el protocolo actual
no captura** las degradaciones de Etapas 2-3 que hunden al 03 ni las alucinaciones del 05. Eso es en sí un
hallazgo sobre el protocolo (propuesta 6).

## 4. Qué es intrínseco al modelo/harness (contener, no eliminar)

- **Fidelidad de extracción del PDF** (artefacto "January 1, 2018" → temporal del 03; encoding del 02). Es
  la fuente de error más silenciosa. El extractor determinístico (`docling`, PLAN §1.4) deja de ser
  "candidato pendiente" — es prerequisito para cualquier claim de universalidad.
- **Temperamento de umbral en tests subjetivos**: dado el mismo test de concreción, cada modelo corta en un
  punto distinto (4/8 a 7/8). No se elimina; se acota con ejemplos resueltos.
- **Verbosidad/profundidad por defecto** (resúmenes ricos de 01/04 vs. telegráficos de 03): estilo del
  modelo. Se contiene con pisos verificables por el validador, no con exhortaciones.
- **Propensión a alucinar en campos de síntesis libre** (UE en 05): inherente; se contiene exigiendo
  verificabilidad textual.

## 5. Refuerzos propuestos al pipeline

**Estado (2026-07-13, mismo día)**: el usuario aprobó aplicar de inmediato las propuestas **1, 2, 4 y 5**
(aplicadas — ver la tabla de decisiones de Ronda 5 en la bitácora de
[../PLAN_ANALISIS_PROFUNDO.md](../PLAN_ANALISIS_PROFUNDO.md) para el dónde exacto de cada una) y **diferir
la 3 y la 6** hasta el feedback del equipo del curso. El texto siguiente se conserva tal como se propuso, a
ciegas, antes de esa decisión.

1. **Anclar el test de concreción con ítems resueltos** (fuente de varianza #1): agregar a
   INTERPELACION_v0 §1.4 una tabla de 6-8 ítems ejemplo ya clasificados CONCRETO/GENERICO con una línea de
   por qué — usando ítems de doc11/doc13, **no de doc09**, para no quemar el caso de prueba de portabilidad.
   Más una regla nueva salida del caso 03: *el desglose se corre sobre el texto completo de la sección de
   recomendaciones, nunca sobre versiones abreviadas en recuadros de portada o key messages*.
2. **Cerrar la zona gris del criterio (ii)**: una línea en §1.2 aclarando que un mecanismo de
   *planificación* multiactor con nombre propio, adoptado o avalado institucionalmente, cuenta como
   mecanismo de articulación (IRRP como ejemplo resuelto). El razonamiento del caso 05 era defendible; que
   lo sea es un defecto de la regla, no del modelo.
3. **Estructurar el juicio en vez de narrarlo**: campos cerrados convergen 5/5, prosa libre diverge.
   Convertir los 3 tests del criterio (i) en subcampos del esquema (`test_inversion_coordinada:
   pasa/no_pasa` + evidencia, etc.) y lo mismo para la verificación de ámbito del (ii). Los casos 01/04 lo
   hicieron espontáneamente en prosa; el esquema puede exigirlo a todos (cambio a esquema_json_v1 → v2).
4. **Extender `validar_esquema.py`** con chequeos baratos que habrían atrapado errores reales de esta
   tanda: encoding (JSON en español sin una sola tilde = bandera), largo mínimo proporcional de resúmenes
   de sección, `desglose_items` con páginas dentro del rango de la sección de recomendaciones,
   `resumen_narrativo` con mínimo de oraciones.
5. **Reglas puntuales faltantes**: (a) qué cuenta como resumen ejecutivo — recuadros de portada / key
   messages no lo son; (b) política para cifras computadas vs. literales (¿79,5% o 81,3%? — definir si se
   suman solo fósiles estrictos y exigir marcar la cifra como computada); (c) confirmar que los encabezados
   tipográficos de un policy brief sin índice cuentan como "índice" para la regla de secciones — y decidir
   si la fusión de secciones del caso 01/referencia se corrige (hoy la referencia contradice al esquema).
6. **Ampliar el Paso 5 del protocolo de portabilidad** de 3 a ~6 checkpoints, agregando los tres modos de
   falla nuevos que esta corrida reveló: detección de `brechas_implementacion` retrospectiva (3 de 5 la
   perdieron), ausencia de referentes alucinados (verificable con búsqueda literal), y profundidad mínima
   de resúmenes. Con los 3 checkpoints actuales, 03 y 05 pasan; con los 6, quedarían correctamente
   señalados.

**Conclusión de fondo (alentadora para la universalidad)**: todo lo que las Rondas 1-4 convirtieron en regla
escrita con ejemplo resuelto se transfirió a modelos que nunca vieron esas rondas (tipología 5/5, criterios
i y iii 5/5, chequeo negativo 5/5). Lo que diverge es exactamente lo que quedó como umbral sin ejemplos
(test de concreción) o lo que vive debajo de la metodología, en la capa de extracción/harness. El camino
hacia un pipeline agnóstico no es más prompt — es más ejemplos resueltos, más estructura en el esquema, y un
extractor determinístico compartido.

## 6. Nota de housekeeping — el archivo de referencia fue renombrado

Al preparar esta prueba, `pilot/doc09_caribbean_power.json` (la referencia calibrada) se renombró a
`doc09_caribbean_power_01.json` (verificado idéntico), lo que dejaba rotas las referencias a ese archivo en
GUIA_OPERATIVA_PIPELINE.md (Paso 1 del protocolo), INTERPELACION_v0.md §4, PLAN_ANALISIS_PROFUNDO.md y
esquema_json_v1.md. **Resuelto (2026-07-13)**: se restauró la copia canónica `doc09_caribbean_power.json`
(la metodología vuelve a apuntar a un archivo existente) y se conservó `_01` como parte del set de 5 casos
de esta evaluación. Tras la corrección de secciones de la propuesta 5 (aplicada el mismo día), el canónico
ya no es idéntico a `_01`: el canónico es el artefacto vigente del pipeline (7 secciones), los numerados
son los artefactos congelados de esta prueba a ciegas.
