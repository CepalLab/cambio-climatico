# Arquitectura del informe de 30 páginas v1

**Estado:** estructura de trabajo aprobable; la prosa queda sujeta a la compuerta v2.  
**Base:** `fase3-analitica-v1`, 238 documentos activos y 6 exclusiones aplicadas.  
**Propósito:** explicar la evolución del abordaje CEPAL sobre cambio climático entre 2015 y 2025 sin confundir composición del corpus, evidencia documental y resultados de política.

## Principio de organización

El informe no reproduce nueve respuestas aisladas. Ordena una pregunta de fondo: ¿cómo cambia el modo en que la CEPAL vincula clima, desarrollo, igualdad e implementación? Las preguntas P1-P9 operan como pruebas y desagregaciones de ese argumento. Cada sección parte de documentos completos; las citas literales aparecen solo para definiciones, tensiones o mecanismos cuya formulación debe verificarse.

## Estructura y extensión

| Sección | Páginas | Pregunta que responde | Evidencia y documentos ancla | Cuadro o gráfico |
| --- | ---: | --- | --- | --- |
| Resumen ejecutivo | 2 | ¿Cuál es el argumento, qué cubre y qué no permite concluir? | Síntesis v2; 238 perfiles; P1-P3. | Recuadro de hallazgos y límites. |
| 1. Introducción | 2 | ¿Por qué leer el corpus CEPAL como producción institucional y no como muestra neutral de la literatura regional? | Composición por división y tipo documental; *Horizontes 2030* (40159). | Cuadro 1, cobertura y corpus. |
| 2. Corpus, método y límites | 3 | ¿Qué se analiza, con qué unidad de evidencia y qué inferencias se excluyen? | JSON canónicos, SQLite, perfiles, taxonomía candidata, interpelación y verificación canónica. | Cuadro 1 y nota de procedencia. |
| 3. Evolución del objeto de estudio | 4 | ¿Qué cambia entre P1, P2 y P3 y qué persiste? | *Adaptación al cambio climático en ALC* (39842), *Horizontes 2030* (40159), *Construir un nuevo futuro* (46227), *Empleos verdes* (81886). | Gráfico 1, objetos por período; Gráfico 2, modos analíticos. |
| 4. Impactos, diagnóstico y herramientas (P1-P4) | 4 | ¿Cómo se describen impactos, restricciones estructurales e instrumentos de decisión? | Ríos de Mendoza y San Juan (39140), bioeconomía (44640), metodologías de costos (41832), financiamiento sostenible (47720). | Cuadro 2, cobertura P1-P4; inserto de herramientas. |
| 5. Implementación, brechas y desafíos (P5-P7) | 4 | ¿Por qué los planes e instrumentos no se traducen automáticamente en ejecución territorial? | Inversión pública sostenible (80561), Agenda 2030 (81405). | Gráfico 4, territorio, tipología y objeto. |
| 6. Cambios de énfasis y tensiones de agenda (P6-P7) | 3 | ¿Cómo leer la evolución sin convertirla en etapas cerradas? | Impactos (39140), instrumentos (47720), inversión pública (80561) y coordinación presupuestaria (81405). | Recuadro de contraejemplos por período. |
| 7. Oportunidades y Gran Impulso Ambiental (P8) | 3 | ¿Cuándo una oportunidad sectorial se convierte en estrategia de transformación? | *Horizontes 2030* (40159), bioeconomía (43825), recuperación transformadora (46227). | Gráfico 3, panel Big Push; Cuadro 3, oportunidades y condiciones habilitantes. |
| 8. Participación, derechos y distribución (P9) | 2 | ¿Qué papel tienen información, participación, justicia y grupos subrepresentados? | Acceso a la información y justicia ambiental (44590), derechos humanos (44970), género y clima (41101). | Recuadro Escazú y límite cualitativo. |
| 9. Conclusiones y agenda | 3 | ¿Qué tesis del corpus se sostiene y qué agenda de análisis queda abierta? | Hallazgos revisados; documentos ancla por capítulo. | Matriz final de hallazgo, alcance y límite. |
| **Total** | **30** | | | |

## Figuras y cuadros obligatorios

1. **Cuadro 1. Cobertura y corpus:** período, tipo documental normalizado, escala territorial y transformación primaria. Debe declarar que el corpus es producción CEPAL.
2. **Gráfico 1. Evolución del objeto de estudio:** objetos principales candidatos normalizados por período; nota visible de clasificación candidata calibrada.
3. **Gráfico 2. Modos analíticos por período:** separa taxonomía candidata, campos canónicos e interpelación directa.
4. **Cuadro 2. Cobertura de P1-P9:** cobertura de evidencia, no respuesta final ni consenso.
5. **Gráfico 3. Panel Big Push Ambiental:** Sí/Parcial/No por período para los cuatro criterios; explica la ventana de recuperación pospandemia.
6. **Gráfico 4. Territorio, tipología y objeto:** visualización de solapamientos, no cadena causal.
7. **Cuadro 3. Conclusiones y recomendaciones transversales:** patrón, período, ancla, límite y cita a recuperar.

## Reglas de redacción y cierre

- La primera mención expande P1 (2015–2018), P2 (2019–2022) y P3 (2023–2026; el corpus disponible llega hasta 2025).
- Las secciones 3, 6 y 7 no pasan a versión final hasta cerrar la revisión humana y la auditoría de segundo modelo de la compuerta v2.
- Cada bloque narrativo conserva una ficha con argumento, documentos ancla, citas, límite y figura; ninguna cita se reutiliza como prueba de una generalización no respaldada por el perfil documental.
- La arquitectura se revisará después de la primera entrega narrativa; no se generan los gráficos definitivos antes de aprobar la pregunta que cada uno debe responder.
