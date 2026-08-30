# Compuerta de revision del mapa analitico v2

**Estado:** cerrada para circulación  
**Base:** `fase3-analitica-v1`, 238 documentos activos, 6 exclusiones

La prosa narrativa y la arquitectura final del informe no comienzan hasta que esta compuerta registre una resolucion humana y una auditoria de segundo modelo. La revision evalua argumentos y evidencia, no reescribe los JSON canonicos.

## Insumos obligatorios

- `SINTESIS_GLOBAL_COMPLETA_BORRADOR_v2.md`
- `RESPUESTAS_PREGUNTAS_FASE3_3_BORRADOR_v2.md`
- `salidas/verificacion_ejes_canonicos_v1.json`
- `salidas/paneles_analiticos_v1.md`

## Revision humana

| Area | Decision requerida | Criterio de salida |
| --- | --- | --- |
| P6, cambios de enfasis | Mantener, ajustar, dividir o descartar la tesis | Distingue cambio de agenda, composicion del corpus y persistencias por periodo. |
| P8, Big Push | Mantener, ajustar o descartar la lectura de ventanas temporales | Explica P1-P2-P3 sin presentar porcentajes como trayectoria uniforme. |
| Transicion justa | Seleccionar documentos ancla y formulacion | No infiere adopcion de politica desde una mencion documental. |
| Perdidas y danos | Clasificar evidencia como evaluacion de danos, marco politico-financiero o no utilizable | Cada caso usado conserva cita completa, pagina, ruta y hash. |
| CBDR | Aprobar o descartar su uso como hilo cualitativo | No se presenta como tendencia cuantitativa ni se afirma desaparicion. |

## Auditoria de segundo modelo

El segundo revisor debe evaluar, sin recibir la conclusion esperada, una muestra de afirmaciones de P6, P8 y los tres ejes verificados. Para cada una debe indicar: evidencia suficiente, evidencia insuficiente, formulacion inflada, contraejemplo omitido o trazabilidad incompleta.

## Registro de salida

La compuerta se cierra cuando cada fila tenga responsable, fecha, decision y nota de resolucion. Las correcciones se incorporan en una version posterior del mapa; los desacuerdos se conservan como limites explicitos del informe.

## Registro parcial: bloque 01

| Alcance | Responsable | Fecha | Decisión | Resolución |
| --- | --- | --- | --- | --- |
| Método, P6 y P8 en `BLOQUE_NARRATIVO_01_METODO_EVOLUCION_BIG_PUSH_v1.md` | Equipo revisor | 2026-08-26 | aprobar | El equipo revisó el bloque y autorizó continuar con la siguiente entrega narrativa. |
| Trazabilidad y alcance del bloque 01 | Auditoría independiente | 2026-08-26 | ajustar y aprobar | Se corrigió la distinción entre citas canónicas e identificadores derivados de SQLite, se incorporaron ruta y SHA-256 de las fuentes y se corrigió el alcance de 8 a 12 páginas planificadas. |
| P1-P7 en `BLOQUE_NARRATIVO_02_P1_P7_v1.md` | Equipo revisor | 2026-08-26 | aprobar | El equipo revisó el bloque y autorizó avanzar a participación, conclusiones y agenda. La auditoría independiente queda pendiente antes de la versión final. |
| P9, conclusiones y agenda en `BLOQUE_NARRATIVO_03_P9_CONCLUSIONES_AGENDA_v1.md` | Equipo revisor | 2026-08-27 | aprobar | Se incorporó la referencia canónica del documento de género y el equipo autorizó continuar con el resumen ejecutivo y las figuras. La auditoría independiente queda pendiente antes de la versión final. |
| Bloques 02 y 03 | Auditor temático independiente | 2026-08-27 | aprobar con ajustes / aprobar | Verificó 10 de 10 citas. El bloque 02 incorporó composición del corpus, contraejemplos y elipsis; el bloque 03 solo requirió marcar la elipsis de la cita de género. |
| FE-01, territorio, escalas y capacidades | Equipo revisor | 2026-08-27 | aprobar | Se aprueba el recorrido SICA, cuenca binacional Sixaola y ciudad de Belmopan; mantener agregados multi-etiqueta y límite de no inferir capacidad homogénea. |
| FE-02, transformaciones y tensiones | Equipo revisor | 2026-08-27 | aprobar | Mantener las tensiones canónicas como problemas que el corpus procesa, no como desenlaces resueltos. |
| FE-03, propuestas, avances y brechas | Equipo revisor | 2026-08-27 | aprobar | Mantener denominadores explícitos y la coexistencia de codificación sin inferir resultados de política. |
| Paquetes de evidencia para expansión v2 | Auditoría independiente | 2026-08-27 | aprobar | Ambos paquetes fueron regenerados contra la SQLite actual, comparten el hash físico y declaran 2015–2026. |
| Bloque 04, expansión v2 | Equipo revisor | 2026-08-27 | aprobar | Se aprueban los capítulos de escalas, tensiones y coherencia para integrarlos al informe maestro v2. |
| Transición justa, pérdidas y daños y CBDR | Equipo revisor | 2026-08-28 | aprobar uso acotado | Se mantienen las distinciones conceptuales y los límites de inferencia en la versión de circulación. |
| Informe maestro v2 congelado | Equipo revisor | 2026-08-28 | aprobar para circulación | Revisión humana final completada: tono, prioridades, claridad y adecuación de las cinco figuras aprobados. |

Este registro cierra la compuerta v2. La versión congelada conserva los bloques 01, 02, 03 y 04, junto con el tratamiento acotado de transición justa, pérdidas y daños y CBDR. La siguiente tarea es producir la versión de circulación sin modificar evidencia, citas ancla ni límites metodológicos.
