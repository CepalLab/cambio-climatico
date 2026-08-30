# Plan de expansión v2 del informe maestro

**Estado:** aprobado para ejecución antes de reescribir el informe maestro.  
**Base:** `fase3-analitica-v1`, 238 documentos activos y 6 exclusiones aplicadas.  
**Extensión objetivo:** 6.800–7.800 palabras de prosa, aproximadamente 20 páginas; cuadros, figuras y anexos pueden aumentar la extensión total.

## Correcciones obligatorias

1. P3 se presentará como **2023–2026, con seis publicaciones fechadas en 2026**, no como período que llega hasta 2025. Los documentos son 85930, 86527, 89774, 89932, 89934 y 90001.
2. Las tensiones dialécticas se derivarán de `tipologia.tension_dialectica` en los JSON canónicos de Fase 2. SQLite conserva la tipología primaria y secundaria, pero no ese campo.
3. La prosa final usará título, año y página para las referencias. Rutas, hashes, JSON, SQLite y `dimension_id` se moverán al anexo técnico de trazabilidad.
4. Pérdidas y daños tendrá un párrafo acotado dentro de protección financiera, implementación y evaluación de desastres. Distinguirá la evaluación de daños e impactos del marco político-financiero de pérdidas y daños. CBDR será una nota cualitativa separada sobre negociación climática en la sección temporal. Ninguno figurará como pilar del resumen o de las conclusiones.

## Mapa de expansión

| Capítulo | Preguntas | Palabras guía | Evidencia principal | Figura o cuadro | Riesgo a controlar |
| --- | --- | ---: | --- | --- | --- |
| Resumen ejecutivo | Síntesis | 500 | Cinco convergencias revisadas | Recuadro de alcance | Evitar agenda procedimental. |
| 1. Introducción | Marco | 350 | Composición institucional del corpus | Cuadro 1 | No presentar el corpus como literatura regional completa. |
| 2. Corpus, método y límites | Marco | 400 | Perfiles, metadatos y evidencia documental | Cuadro 1 | Traducir metodología sin jerga interna. |
| 3. Evolución del objeto | P1-P3, P6 | 800 | Objetos candidatos, conclusiones y recomendaciones directas | Figuras 1 y 2 | Cambio de énfasis no equivale a etapas cerradas. |
| 4. Impactos, diagnóstico y herramientas | P1-P4 | 750 | Impactos territoriales, modelos, valoración y datos | Cuadro 2 | Casos no representan automáticamente a toda la región. |
| 5. Implementación, brechas y desafíos | P5-P7 | 750 | Propuestas, avances y brechas | Cuadro de coherencia propuesta/avances | Presencia documental no mide resultados. |
| 6. Enfasis, persistencias y ventanas | P6-P7 | 550 | Contraejemplos P1/P3 y recuperación pospandemia | Recuadro temporal | Composición por división, tipo y período. |
| 7. Territorio, escalas y capacidades | P1, P5-P7 | 700 | Ámbitos regionales, subregionales, nacionales y subnacionales; tipología de capacidades | Figura 4 | Escalas multi-etiqueta: los conteos no suman 238. |
| 8. Transformaciones y tensiones | Interpretación transversal | 600 | Tipología SQLite y tensiones canónicas | Cuadro de tensiones | No presentar tensiones como desenlaces resueltos. |
| 9. Gran Impulso Ambiental | P8 | 650 | Matriz de lectura, interpelación y anclas documentales | Figura 3 y Cuadro 3 | La rúbrica describe documentos, no desempeño de políticas. |
| 10. Participación, derechos y distribución | P9 | 500 | Derechos de acceso, derechos humanos y género | Recuadro de acceso | Mantener P9 cualitativa. |
| 11. Convergencias transversales | Síntesis | 400 | Cinco patrones recurrentes | Matriz de convergencias | Cada patrón necesita anclas y un límite. |
| 12. Conclusiones y agenda | Cierre | 550 | Hallazgos aprobados | Matriz final | Agenda sustantiva, no procedimental. |

## Nuevos capítulos analíticos

### Territorio, escalas de análisis y capacidades

El capítulo se organiza por escalas de análisis, no por la etiqueta `multinivel`. La evidencia candidata por período registra alcance regional (53/45/41), subregional (57/55/45), subnacional (19/21/11), nacional (7/3/4) y multinivel (5/8/1). La etiqueta multinivel es un subconjunto pequeño de articulación explícita, no el eje que explica el corpus.

La tipología aporta una señal complementaria: Capacidades del Estado como transformación primaria registra 19 documentos en P1, 15 en P2 y 25 en P3. El argumento debe conectar esas capacidades con inversión pública, coordinación y escala territorial, sin afirmar una tendencia causal ni sumar categorías superpuestas.

### Transformaciones y tensiones dialécticas

La sección usa la transformación primaria de SQLite como descripción agregada y el texto canónico de la tensión dialéctica como evidencia interpretativa. Organizará las tensiones como problemas que el corpus procesa: ambiente y desarrollo; derechos formales y ejecución; inversión necesaria y restricción fiscal; transición justa y costos distributivos; ambición climática y capacidad estatal. No se afirmará que los documentos resuelven esas tensiones.

### Coherencia entre propuestas, avances y brechas

Esta sección desarrolla una convergencia del corpus: las propuestas de política cubren 92/99 documentos en P1, 74/75 en P2 y 63/64 en P3; avances de implementación, 61,6%, 66,7% y 71,9%; y brechas de implementación, 59,6%, 76,0% y 70,3%. La lectura defendible es que las respuestas formuladas coexisten con atención creciente a avances y brechas, no que las propuestas hayan sido implementadas con éxito.

## Matriz de lectura del Gran Impulso Ambiental

En prosa se denominará **matriz de lectura del Gran Impulso Ambiental**. Distingue cuatro elementos documentales: oportunidades productivas sostenibles; articulación identificable entre actores; concreción operativa mediante instrumentos, responsables o recursos; y una estrategia integrada de inversión coordinada a escala. La matriz describe cómo cada publicación formula esos elementos. No evalúa la efectividad de las políticas ni transforma automáticamente una oportunidad sectorial en un Gran Impulso.

La Figura 3 debe explicar la ventana de recuperación pospandemia en P2 y la composición más técnica y financiera de P3. La rúbrica completa y sus veredictos quedan en el anexo técnico.

## Reglas editoriales

- Reducir los dos puntos: reservarlos para listas, definiciones y citas; preferir oraciones separadas cuando introduzcan una elaboración.
- En la prosa, nombrar los períodos por sus años: 2015–2018, 2019–2022 y 2023–2026. La primera mención puede indicar entre paréntesis que corresponden a P1, P2 y P3; las siglas se reservan después para cuadros, gráficos, notas metodológicas o comparaciones compactas.
- Reemplazar jerga interna por lenguaje de informe. La trazabilidad detallada pasa a un anexo.
- Cada figura entra dentro del argumento con un párrafo que explique patrón, alcance y cautela; no se agrupan solo al final.
- Cada expansión debe anclarse en un dato verificado, una ficha o un documento. Si no aumenta claridad analítica, no se agrega texto.
- El resumen y las conclusiones priorizan implementación, financiamiento, coordinación, capacidades, territorio, igualdad y derechos.

## Compuertas antes de integrar v2

1. Validar la corrección temporal P3 y propagarla en los documentos que aún usan la formulación anterior.
2. Construir un derivado versionado de tensiones dialécticas desde los JSON canónicos y revisar una muestra por período.
3. Preparar fichas narrativas para territorio/escalas, tipología/tensiones y coherencia propuesta/avances, cada una con anclas, límite y figura.
4. Realizar revisión humana y auditoría independiente de esos tres capítulos antes de promover el informe maestro v2.
5. Decidir si la compuerta específica de pérdidas y daños y CBDR habilita su inclusión acotada o si permanecen solo en el anexo de agenda.
