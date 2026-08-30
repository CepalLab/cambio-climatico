# Auditoria independiente de bloques narrativos 02 y 03 - v1

**Fecha:** 2026-08-27
**Auditor:** revisor tematico independiente (desarrollo sostenible)
**Base:** `fase3-analitica-v1`, 238 documentos activos, 6 exclusiones
**Alcance:** `BLOQUE_NARRATIVO_02_P1_P7_v1.md` y `BLOQUE_NARRATIVO_03_P9_CONCLUSIONES_AGENDA_v1.md`
**Metodo:** verificacion de las 10 citas contra SQLite y los JSON canonicos (texto,
pagina, `dimension_id`, SHA-256 real del archivo) + evaluacion de las cinco
comprobaciones solicitadas + revision de consistencia con arquitectura, resumen
ejecutivo y compuerta v2.

---

## 1. Las citas respaldan cada afirmacion y conservan documento, pagina, hash y dimension_id

**VERIFICADO: 10/10 citas correctas.**

| dimension_id | Doc | Pagina | Texto verbatim | SHA-256 real vs declarado | Dimensión |
| --- | --- | --- | --- | --- | --- |
| 1129 | 39140 | 16 | OK | OK | tendencias |
| 3289 | 44640 | 18 | OK | OK | brechas_implementacion |
| 1935 | 41832 | 85 | OK | OK | propuestas_politica |
| 5351 | 47720 | 22 | OK | OK | propuestas_politica |
| 7019 | 80561 | 35 | OK | OK | desafios |
| 7500 | 81405 | 137 | OK | OK | propuestas_politica |
| 549 | 43301 | 16 | OK | OK | propuestas_politica |
| 3309 | 44970 | 14 | OK | OK | propuestas_politica |
| 1843 | 41101 | 78 | OK | OK | propuestas_politica |
| 332 | 47745 | 119 | OK (elipsis original) | OK | propuestas_politica |

- Cada `dimension_id` existe en SQLite y apunta al documento correcto.
- Cada cita es un fragmento verbatim del registro SQLite.
- Los SHA-256 declarados coinciden con el hash calculado sobre el archivo fuente.
- La nota de los bloques es correcta: `dimension_id` es un registro derivado de
  SQLite, no un campo del JSON canonico.

**Observaciones de higiene (no alteran la integridad):**
- 4 citas (39140, 80561, 81405, 41101) son fragmentos que omiten inicio y/o final
  de la cita completa sin marcarlo con "…". Son verbatim; conviene marcar la
  elision con elipsis en la version final.
- La cita 47745 conserva la elipsis original del registro SQLite ("..."), correcta.

## 2. P1-P7 no convierten recomendaciones o estudios de caso en evidencia de implementacion regional

**VERIFICADO.** Los pasajes clave del bloque 02 lo hacen explicito:

- FN-05 limite: "las metodologias y propuestas de politica muestran herramientas
  disponibles, no su adopcion ni eficacia demostrada".
- FN-06 limite: "ambos textos presentan marcos, experiencias y recomendaciones;
  no miden una ejecucion homogenea ni resultados comparables entre paises".
- Narrativa seccion 5 (80561): "La cita no prueba que tal incorporacion este
  ocurriendo con igual intensidad en todos los paises; muestra, en cambio, que el
  corpus identifica la inversion como un sitio decisivo...".
- Narrativa seccion 5 (81405): "debe leerse como una orientacion de politica y no
  como evidencia de ejecucion efectiva".

Ninguna cita se usa para afirmar resultados de politica. La distincion
recomendacion/resultado se mantiene tambien en la conclusion 4 del bloque 03.

**Nota menor:** FN-04 usa 44640 (restriccion de financiamiento a la innovacion)
para sostener "los impactos son estructurales". La cita respalda mejor la tesis
de "medios de implementacion" que la de "impactos". El texto puente lo conecta,
pero conviene explicitar esa funcion en la ficha o reubicar el ancla.

## 3. P9 conserva su condicion cualitativa

**VERIFICADO.** Bloque 03:
- Limite explicito en FN-08: "P9 es cualitativa; el corpus no cuenta con una
  anotacion semantica validada que mida calidad, incidencia vinculante ni
  resultados de participacion climatica".
- Narrativa: "La formulacion no permite inferir que esos derechos se apliquen de
  manera uniforme en toda la region ni que toda participacion sea vinculante".
- FN-09 usa 47745 a nivel de agenda, con limite explicito (documento multitematico;
  "orienta una agenda institucional, pero no mide participacion climatica efectiva").
- El resumen ejecutivo declara lo mismo y el recuadro Escazu / limite cualitativo
  esta planificado en la arquitectura (seccion 8).

No se presenta presencia documental como medicion de participacion efectiva.

## 4. Conclusiones con limites, contraejemplos y distincion enfasis vs agenda

**PARCIAL — dos ajustes antes del final:**

1. **Contraejemplos nombrados pero no redactados.** El bloque 02 cita el
   recuadro de contraejemplos ("debe recordar que P1 ya incluye instrumentos
   fiscales y financieros, y que P3 conserva impactos y vulnerabilidad") pero el
   contenido no esta redactado en el bloque. Los datos lo respaldan
   (P1 `financiamiento_inversion`: 8 docs; P3 `impactos_vulnerabilidad`: 9 docs),
   asi que es un artefacto pendiente, no un error. Redactar el recuadro antes de
   declarar el bloque final.
2. **Falta la pata "composicion del corpus" del criterio P6 de la compuerta.**
   La compuerta exige para P6 "Distingue cambio de agenda, **composicion del
   corpus** y persistencias por periodo". El bloque 02 distingue bien enfasis vs
   persistencias y la cautela de taxonomia candidata, pero **no explicita** que
   parte del cambio P1->P3 puede estar conducida por la composicion de la
   produccion CEPAL (divisiones, tipos documentales, ventana de recuperacion
   pospandemia), tal como sugiere el REVIEW_BRIEF (A1/A3). Esa oracion debe
   incorporarse a la seccion 6 antes de cerrar la compuerta.

La distincion "cambio de enfasis, no secuencia lineal" esta bien formulada
(FN-07 y seccion 6: "La comparacion temporal no justifica una historia de
reemplazos") y la conclusion del bloque 03 la conserva.

## 5. Las figuras no hacen afirmaciones mas fuertes que sus datos

**VERIFICADO a nivel de diseno.** No hay figuras producidas en los bloques; solo
se "asocian" con las notas metodologicas correspondientes. Nada sobreafirma
porque aun no existe. Datos disponibles en `paneles_analiticos_v1.md` para cada
figura planificada. Al producirlas, exigir:

- Grafico 1: nota visible "clasificacion candidata calibrada".
- Grafico 2: separar taxonomia candidata / campos canonicos / interpelacion.
- Grafico 3: no presentar los porcentajes como trayectoria uniforme; explicar la
  ventana pospandemia (P2) y el giro tecnico-financiero (P3).
- Grafico 4: solapamientos territoriales, no cadena causal.
- Cuadro 2: cobertura de evidencia, no respuesta final ni consenso.

## Hallazgos adicionales (no bloqueantes, resolver antes del cierre)

1. **Arquitectura desalineada con los bloques.** Las secciones 4-6 de
   ARQUITECTURA_INFORME_30P_v1.md listan anclas (3955, 45692, 44974, 44472,
   46681, 67989, SICA) que no coinciden con los anclas verificados del bloque 02
   (39140, 44640, 41832, 47720, 80561, 81405). El bloque esta correcto; la
   arquitectura debe actualizarse. Ademas, 44472 figura duplicada en las
   secciones 4 y 5.
2. **Panorama v1 desactualizado.** `salidas/panorama_perfiles_documentales_v1.md`
   y `eda_descriptivo_v1.md` reportan tipos "Estudio tecnico 101 / Sin clasificar
   84 / Informe 19 / Policy brief 12". La base SQLite actual tiene 148 / 27 / 25
   (+ reclasificacion de los 84 "Sin clasificar"). El resumen ejecutivo usa los
   valores correctos (SQLite). Regenerar el panorama o marcarlo desactualizado;
   el Cuadro 1 del informe debe tomar los tipos de la base SQLite.
3. **Elision sin marcar** en 39140, 80561, 81405, 41101 (ver seccion 1).
4. **Conclusion 5 del bloque 03 (Big Push)** remite al panel sin numeros. En el
   informe final debe anclarse a los datos del bloque 01 / Grafico 3.

## Veredicto

- **Bloque 02: aprobar con ajustes.** Incorporar la pata "composicion del corpus"
  en la seccion 6 (criterio P6 de la compuerta), redactar el recuadro de
  contraejemplos con los documentos concretos, y marcar las elisiones.
- **Bloque 03: aprobar.** P9 cualitativa correcta; cinco conclusiones acotadas;
  limites y distincion recomendacion/resultado mantenidos.
- Registrar esta auditoria como la revision independiente pendiente de los
  bloques 02 y 03 en la compuerta v2. Las afirmaciones de perdidas y danos y
  CBDR siguen sin entrar a capitulo narrativo hasta su compuerta especifica.

## Trazabilidad

- Verificacion tecnica reproducible desde `fase3/02_eda/salidas/fase3_analitica_v1.sqlite`
  (tablas `dimensions`, `documents`) y los JSON canonicos listados en cada tabla
  de trazabilidad de los bloques.
- Contraste de tipos documentales: tabla `documents.type_normalized_name` en SQLite.
