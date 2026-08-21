# Tipología de documentos v1.0 — transformación primaria/secundaria

**Fecha**: 2026-07-07 — revisado 2026-08-05 (congelamiento pre-batch)
**Estado**: v1.0 (**vigente y congelada para el primer lote de producción**). Anclas ampliadas tras la revisión ciega de la muestra de 17 y el cierre humano de doc10. Cambios posteriores requieren una nueva versión y no se aplican silenciosamente a lotes ya procesados.
**Unidad de análisis**: documento completo — a diferencia de las dimensiones del codebook (que operan a nivel de apartado), la tipología clasifica el documento como una sola pieza de pensamiento institucional.

## 0. Por qué se reutiliza el canon de las 11 Grandes Transformaciones

El Lab ya clasificó 495 publicaciones de la CEPAL bajo este canon en un proyecto anterior (`Desafío CEPAL`, basado en la Revista CEPAL N° 141). Reusarlo acá — en vez de inventar una taxonomía paralela solo para el corpus climático — mantiene un nexo con ese trabajo: los 244 documentos de este corpus son un subconjunto del universo que ya tiene (o debería tener) una transformación primaria/secundaria asignada, y es deseable que ambas clasificaciones sean comparables entre sí en vez de vivir en lenguajes distintos.

Ese proyecto también dejó documentados sus propios errores de forma explícita
(`05_Critica_y_Lecciones_Aprendidas.md`, `15_Metodologia_Detallada_Clasificacion.md`): sesgo de palabra clave (clasificar por mención superficial, no por función real del texto) y "justificación zombie" (justificaciones genéricas que sirven para cualquier documento). El protocolo de la sección 2 reusa literalmente las mitigaciones que ese proyecto ya validó, en vez de rederivarlas.

## 1. Las 11 Grandes Transformaciones (canon, sin cambios)

1. Desarrollo productivo — 2. Reducción de la desigualdad — 3. Protección social — 4. Educación y formación profesional — 5. Igualdad de género — **6. Sostenibilidad ambiental** — 7. Transformación digital — 8. Migración — 9. Integración económica — 10. Macroeconomía y fiscalidad — **11. Capacidades del Estado** (habilitadora/transversal).

Para el corpus climático, la mayoría de los documentos mapeará a **#6** como primaria — el valor analítico real está en identificar cuándo NO es así (el documento es en verdad sobre financiamiento → #10, sobre comercio → #9, sobre gobernanza/planificación → #11) y en la secundaria, que es obligatoria (ver protocolo).

## 2. Protocolo de razonamiento obligatorio

Adaptado del `Protocolo de Cirugía Mayor` de Desafío CEPAL. Es de cumplimiento obligatorio, no opcional — saltarse un paso es exactamente lo que produjo los errores documentados en ese proyecto.

**Paso 1 — Tensión dialéctica.** ¿De qué trata realmente el documento? ¿Qué contradicción estructural intenta procesar? Si menciona un tema técnico (comercio, tecnología, información), ¿es el *sujeto* del documento o el *canal* a través del cual se aborda otra cosa?

**Paso 2 — Filtro de categoría primaria.** ¿Cuál es el objetivo principal de cambio que persigue el documento? (No: ¿de qué habla?, sino: ¿qué pretende transformar?)

**Regla objeto vs instrumento (Ronda 9)** — cierra el swap recurrente #6 Sostenibilidad ambiental ↔ #11 Capacidades del Estado observado en la revisión ciega (doc08, doc12):

1. Si el hilo estructural es **arquitectura institucional** (leyes, gabinetes, entidades de cuenca, MRV, separación regulador/prestador) y clima/ambiente es el **sector o restricción** sobre el que se gobierna → **#11 primaria / #6 secundaria**.
2. Si el hilo es **transformación ambiental-climática** (mitigación, adaptación, resiliencia sectorial, descarbonización) y la institucionalidad es el **medio** → **#6 primaria / #11 secundaria**.
3. Si el clima es solo **canal causal** de otro objeto (pobreza, desigualdad) → patrón doc11 (#2/#6); no forzar #6 como primaria.
4. Ante empate título vs método → priorizar **método y hallazgo de cierre** (qué concluye que hay que cambiar).

**Paso 3 — Secundaria obligatoria.** Todo documento institucional de la CEPAL tiene una segunda intención transformadora. **No se permite "N/A"** salvo caso extremadamente técnico y excepcional (y ese caso debe justificarse explícitamente, no omitirse en silencio).

**Paso 4 — Justificación específica (regla anti-copia).** La justificación debe citar conceptos específicos y literales del documento (no de la definición de la categoría). **Prohibido usar más de 5 palabras seguidas de la definición de la transformación** al redactar la justificación — si la justificación podría pegarse sin cambios en otro documento del corpus, está mal.

**Paso 5 — Validación contra anclas.** Contrastar la clasificación contra las anclas de calibración de la sección 3. Si el documento es de una serie institucional conocida (Panorama, Balance, informe insignia), esas series ya tienen categorías ancla y el modelo no debería desviarse de ellas sin justificación explícita de por qué este caso es distinto.

## 3. Anclas de calibración (corpus climático)

A diferencia de Desafío CEPAL, que ya tenía cientos de casos clasificados como ancla, este corpus arrancó de cero. La muestra revisada aporta los siguientes casos contrastivos. Una alternativa considerada durante el razonamiento no convierte por sí sola al caso en ambiguo: `ambiguedad_pendiente_validacion` se reserva para decisiones realmente abiertas.

| #   | Documento                                                                                           | Primaria                                | Secundaria                           | Nota                                                                                                                                                                                                                                                        |
| --- | --------------------------------------------------------------------------------------------------- | --------------------------------------- | ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 9   | *Building a climate resilient power sector...* (Caribe)                                             | #6 Sostenibilidad ambiental             | #11 Capacidades del Estado           | Caso relativamente claro: tecnología/resiliencia energética como sujeto, pero las recomendaciones concretas son de capacidad institucional (datos, coordinación)                                                                                            |
| 11  | *El impacto del cambio climático en la pobreza infantil y juvenil de América Latina* (UNICEF-CEPAL) | #2 Reducción de la desigualdad          | #6 Sostenibilidad ambiental          | Tercer patrón, distinto a los dos anteriores: #6 entra como secundaria por ser el **canal causal** del análisis (clima → PIB → pobreza), no por afinidad temática directa con el objeto del documento, que es enteramente distributivo/de protección social |
| 8   | *Reflexiones sobre la gestión del agua...*                                                          | #11 Capacidades del Estado              | #6 Sostenibilidad ambiental          | **Ancla Ronda 9 (objeto/instrumento)**: libro de gobernanza hídrica; clima como estrés disperso. Primaria = arquitectura institucional, no el recurso en sí.                                                                                                |
| 12  | *Acción climática en la agricultura (PLACA)*                                                        | #11 Capacidades del Estado              | #6 Sostenibilidad ambiental          | **Ancla Ronda 9**: inventario comparado de leyes/gabinetes/MRV; hallazgo de cierre sobre brecha institucional vs. acción territorial. El título nombra clima; el método es institucional.                                                                   |
| 14  | *Trampas de desarrollo...* (fragmento climático)                                                    | #1 Desarrollo productivo                | #11 Capacidades del Estado           | **Ancla Ronda 9**: objeto = transformación productiva / salida de trampas; el eje climático articula trampas, no redefine el objeto como #6. Secundaria = capacidades TOPP/gobernanza.                                                                     |
| 3   | *The rise of green bonds...*                                                                        | #10 Macroeconomía y fiscalidad          | #6 Sostenibilidad ambiental          | **Ancla financiamiento-como-objeto**: el instrumento y el mercado financiero son el objeto analizado; el destino verde define la secundaria.                                                                                                               |
| 18  | *La economía del cambio climático, 2023: necesidades de financiamiento...*                          | #6 Sostenibilidad ambiental             | #10 Macroeconomía y fiscalidad       | **Ancla financiamiento-como-medio**: el objetivo declarado es la transición baja en carbono y resiliente; la cuantificación fiscal-financiera es la herramienta para alcanzarla.                                                                           |
| 10  | *Una década de acción para un cambio de época*                                                      | #11 Capacidades del Estado              | #6 Sostenibilidad ambiental          | **Ancla humana de serie, 2026-08-05**: en este informe multitemático de seguimiento, planificación, coordinación, territorialización y financiamiento de la implementación son el centro; la sostenibilidad ambiental es el sujeto agregador.                  |
| 16  | *Acceso a la información, participación y justicia ambiental...*                                    | #11 Capacidades del Estado              | #6 Sostenibilidad ambiental          | **Ancla gobernanza ambiental**: tribunales, fiscalías, órganos garantes, registros y derechos de acceso constituyen el objeto institucional; lo ambiental define el ámbito de aplicación.                                                                    |
| 19  | *Panorama de la Gestión Pública 2023: un Estado preparado para la acción climática*                  | #11 Capacidades del Estado              | #6 Sostenibilidad ambiental          | **Ancla de Panorama institucional**: el documento mide y propone capacidades públicas; la acción climática orienta esas capacidades sin invertir objeto e instrumento.                                                                                       |
| 20  | *Impactos económicos del cambio climático en Colombia. Síntesis*                                    | #6 Sostenibilidad ambiental             | #11 Capacidades del Estado           | **Ancla de impacto/adaptación nacional**: vulnerabilidad y adaptación climática de sectores productivos como objeto; información, planificación y regulación estatal como medio. Resultado aceptado como procesado antes del primer batch.                    |
| 13  | *Comercio, cambio climático y el impuesto fronterizo al carbono*                                    | #9 Integración económica                | #6 Sostenibilidad ambiental          | **Ancla comercio-clima**: el CBAM organiza la pregunta, el diagnóstico de exposición y las recomendaciones de acceso y coordinación comercial; descarbonización y medición de emisiones son la respuesta sustantiva.                                         |
| 17  | *Estudio Económico 2023: financiamiento de una transición sostenible*                               | #10 Macroeconomía y fiscalidad          | #6 Sostenibilidad ambiental          | **Ancla de informe económico híbrido**: la unidad completa y la parte climática se estructuran mediante crecimiento, deuda, recaudación, financiamiento y banca central; el clima define la finalidad. Contraste deliberado con doc18 (#6/#10).              |

### Casos límite resueltos

- **Doc13** se resuelve #9/#6 porque una regulación comercial externa estructura la pregunta, la exposición medida y la agenda de respuesta.
- **Doc17** se resuelve #10/#6 porque la unidad es el informe completo y el aparato macrofinanciero domina también la parte climática.

La tensión conceptual se conserva en el razonamiento de cinco pasos, pero ambos llevan certeza `Alta` y `ambiguedad_pendiente_validacion: null`. Funcionan como anclas fronterizas, no como excepciones abiertas.

Esta tabla es la memoria institucional congelada para el primer batch. Los casos nuevos solo se incorporan mediante control de versión; no se reescribe esta referencia durante una corrida.

## 4. Tipo de documento (formato/género — metadato, no parte de la tipología transformacional)

Se registra junto a la tipología porque el Paso 5 del protocolo depende de reconocer la serie: Policy Brief / Documento de proyecto o estudio técnico / Informe insignia o Panorama / Nota técnica. Doc10 fija el ancla #11/#6 para informes multitemáticos de seguimiento de la Agenda 2030 cuyo centro sea la capacidad de implementación; doc19 fija el mismo par para Panoramas institucionales de gestión pública con lente climática. Una serie no hereda mecánicamente el ancla si cambia su objeto: toda desviación debe justificarse de forma explícita.

## 5. Qué NO incluye este documento

La clasificación de "tipo de brecha climática" (retrospectiva/prospectiva) que se manejó como propuesta de eje aparte durante la discusión de calibración **no quedó acá** — se resolvió que es una subdivisión de la dimensión `brechas_implementacion` del codebook (ver [codebook_v0.md §1](codebook_v0.md)), no un eje de tipología nuevo. Ver la bitácora en
[PLAN_ANALISIS_PROFUNDO.md](PLAN_ANALISIS_PROFUNDO.md#bitácora-de-calibración-metodológica) para el razonamiento de por qué se descartó como eje independiente.
