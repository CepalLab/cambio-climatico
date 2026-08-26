# Plan de reorientacion documental v1

**Fecha:** 2026-08-26  
**Estado:** aprobado para ejecucion

## Decision

El analisis de Fase 3.3 comienza desde perfiles documentales completos y no
desde citas individuales. Las citas conservan su funcion de trazabilidad,
verificacion y profundizacion de hallazgos agregados.

## Secuencia

1. Construir perfiles directos de los 238 documentos desde sus JSON canonicos.
2. Calibrar la taxonomia de objetos, dominios, funciones y relaciones.
3. Generar una matriz documental para responder que estudia CEPAL, que
   variables analiza y que conclusiones y recomendaciones formula.
4. Integrar como ejes complementarios el ambito territorial y la tipologia con
  su tension dialectica.
5. Comparar la matriz por periodo y ambito.
6. Construir el grafo `Documento -> Objeto/Variable -> Relacion -> Conclusion/Recomendacion`.
7. Usar dimensiones y citas para probar o matizar las sintesis globales.

## Estado de artefactos previos

- Los paquetes de evidencia y las citas siguen vigentes como respaldo.
- `F3-EVO-001` a `F3-EVO-005` se pausan como ejercicios microanaliticos; no
  guian la sintesis global ni pasan a revision humana por ahora.
- La revision humana inicial se desplazara a matrices y hallazgos documentales
  agregados, que son la unidad de decision sustantiva.

## Criterio de salida de la primera capa

El perfil directo debe conservar 238 documentos, identificadores unicos, hash
de origen y los campos canonicos de pregunta, ambito, resumen, hallazgos,
conclusiones y recomendaciones. Solo despues se incorporan asignaciones
analiticas candidatas.

## Avance al 2026-08-26

La primera capa se genero para los 238 documentos. La matriz candidata usa
reglas ponderadas por titulo, pregunta de investigacion y resumenes directos;
la muestra de 10 perfiles en `salidas/calibracion_documental_taxonomia_v1.md`
es el siguiente control antes de producir un panorama sustantivo.

El perfil y la matriz tambien integran el ambito territorial normalizado v1 y
la tipologia ya adjudicada, incluida su tension dialectica. Ambos ejes se usan
como agregados complementarios y no sustituyen la lectura de objeto, dominio,
funcion, conclusiones o recomendaciones.

La primera lectura global revisable esta en
`LECTURA_GLOBAL_DOCUMENTAL_BORRADOR_v1.md`; su revision sustantiva precede a
cualquier redaccion del informe de 30 paginas.

La lectura piloto fue escalada a los 238 perfiles en
`SINTESIS_GLOBAL_COMPLETA_BORRADOR_v1.md`. Este es el documento activo para
revision sustantiva; el piloto conserva valor como ensayo de forma y limites.

El segundo frente activo es `RESPUESTAS_PREGUNTAS_FASE3_3_BORRADOR_v1.md`, que
organiza la evidencia documental y los paneles directos para las nueve
preguntas de Fase 3.3, incluido el analisis del Big Push Ambiental.

La siguiente fase transforma ambos frentes en prosa narrativa basada en
documentos ancla y citas selectivas. La guia y el piloto de P8 fijan el patron
de redaccion antes de extenderlo a los capitulos del informe.

El estado completo de este ciclo queda congelado en
[CHECKPOINT_FASE3_3_2026-08-26.md](CHECKPOINT_FASE3_3_2026-08-26.md).