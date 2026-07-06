# Codebook v0 — propuesta de codificación para Fase 2

Construido a partir de las 7 dimensiones nombradas en la nota conceptual (sección 7, Etapa 3), con
las reglas de decisión y ejemplos que el documento original no incluye. Es un punto de partida para
la calibración con [muestra_calibracion.csv](muestra_calibracion.csv), no una versión definitiva —
ver [README.md](README.md) para el contexto y el proceso de validación.

## 1. Dimensiones analíticas (multi-etiqueta a nivel de párrafo/fragmento)

| Dimensión | Definición operativa | Regla de decisión | Marcadores típicos |
|---|---|---|---|
| **Estado de situación** | Describe QUÉ está pasando (impactos, vulnerabilidad, riesgos observados), sin explicar causas | Si el fragmento describe un fenómeno/impacto sin atribuir causa estructural → esta etiqueta | Datos, estadísticas, "los impactos observados son...", "la vulnerabilidad es mayor en..." |
| **Diagnóstico estructural** | Explica POR QUÉ ocurre lo anterior, atribuyendo el fenómeno a factores estructurales (modelo productivo, matriz energética, institucionalidad, desigualdad) | Si hay conector causal ("debido a", "esto se explica por", "producto de") ligando el fenómeno a un factor sistémico → esta etiqueta. Puede coexistir con "estado de situación" en el mismo párrafo | Atribución causal, referencia a modelo de desarrollo/estructura productiva |
| **Propuestas e instrumentos de política** | Recomendaciones o instrumentos concretos (leyes, fondos, impuestos al carbono, taxonomías, planes) | Verbo prescriptivo ("se recomienda", "es necesario", "debería") + sustantivo de instrumento | Nombra un instrumento específico o una acción recomendada |
| **Avances de implementación** | Evidencia de una acción/política YA implementada con resultado observado | Verbo en pasado/presente perfecto + país/territorio + resultado | "Chile implementó...", "se ha logrado..." |
| **Brechas de implementación** | Ausencia, insuficiencia o falla respecto de algo que se esperaría dado un compromiso o política ya anunciada | Requiere referencia (explícita o implícita) a una política/compromiso previo que no se cumplió | "pese a los compromisos NDC, persiste...", "no se ha traducido en..." |
| **Tendencias** | Patrón de evolución temporal 2015–2025 | Comparación explícita o implícita entre períodos | "ha aumentado", "se observa una consolidación de..." |
| **Desafíos** | Obstáculo estructural o futuro para la acción climática, sin estar atado a una política específica ya intentada (a diferencia de "brecha") | Framing prospectivo/genérico de dificultad, no retrospectivo de una política puntual | "coordinar múltiples niveles de gobierno sigue siendo complejo" |
| **Oportunidades** | Condición favorable o ventana no explotada, framing positivo | Verbo de potencial ("permite", "abre la posibilidad de"), sin ser recomendación prescriptiva concreta (eso sería "propuesta") | "representa una oportunidad para...", "podría catalizar..." |

**Nota de diseño:** estado de situación/diagnóstico y avances/brechas son los pares más propensos a
confusión — por eso llevan regla de decisión explícita y permiten doble etiqueta en vez de forzar
exclusividad.

## 2. Variables adicionales

| Variable | Valores | Cómo se resuelve |
|---|---|---|
| **Nivel de aplicación** | Regional (ALC en conjunto) / Nacional / Subnacional (territorio, ciudad, sector) | Se toma el nivel más específico mencionado; multi-tag si el fragmento cubre varios |
| **Cobertura geográfica** | Lista cerrada: 33 países ALC + subregiones (Centroamérica, Caribe, Cono Sur, Andina) + "regional" | Se resuelve técnicamente vía extracción de entidades (NER); requiere solo que el equipo del curso confirme la lista de valores |
| **Tipo de instrumento** (solo si la dimensión es "propuestas") | Planificación / Regulación / Financiamiento / Gobernanza / Información-monitoreo | Es la taxonomía más débil hoy — requiere confirmación del equipo del curso |
