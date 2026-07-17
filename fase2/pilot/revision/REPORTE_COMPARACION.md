# Reporte de comparación ejecutor ↔ revisor ciego externo

Generado por `pipeline/comparar_revision.py` sobre 17 documento(s) con revisión. Ver INSTRUCCIONES_REVISOR_EXTERNO.md §6 para el uso de este reporte (adjudicación).

## Tasa de acuerdo

**87 de 102** ítems comparados coinciden (85%).

| Documento | Revisor | Acuerdo |
| --- | --- | --- |
| doc01 | cursor-grok-4.5/cursor | 6/6 |
| doc02 | cursor-grok-4.5/cursor | 5/6 |
| doc03 | cursor-grok-4.5/cursor | 6/6 |
| doc04 | cursor-grok-4.5/cursor | 4/6 |
| doc06 | cursor-grok-4.5/cursor | 4/6 |
| doc08 | cursor-grok-4.5/cursor | 4/6 |
| doc09 | cursor-grok-4.5/cursor | 6/6 |
| doc10 | cursor-grok-4.5/cursor | 5/6 |
| doc11 | cursor-grok-4.5/cursor | 6/6 |
| doc12 | cursor-grok-4.5/cursor | 3/6 |
| doc13 | cursor-grok-4.5/cursor | 5/6 |
| doc14 | cursor-grok-4.5/cursor | 6/6 |
| doc15 | cursor-grok-4.5/cursor | 4/6 |
| doc16 | cursor-grok-4.5/cursor | 6/6 |
| doc17 | claude-sonnet-4.5/cursor | 6/6 |
| doc18 | cursor-grok-4.5/cursor | 6/6 |
| doc19 | cursor-grok-4.5/cursor | 5/6 |

## Adjudicación Ronda 9 (2026-07-16)

De las **35** discrepancias originales: **20** a favor del revisor (JSON del ejecutor corregido), **15** a favor del ejecutor (veredicto canónico = ejecutor).

- Acuerdo bruto inicial ejecutor↔revisor: **67/102 (66%)**.
- Acuerdo tras corregir el ejecutor según Ronda 9: **87/102 (85%)** (coincide con la tasa que reporta `comparar_revision.py` sobre los JSON ya corregidos).

Las discrepancias listadas abajo son las **15** que permanecen (Lab confirmó al ejecutor). Detalle completo: [ADJUDICACION_RONDA9.md](ADJUDICACION_RONDA9.md). Reglas: [INTERPELACION_v0.md](../../INTERPELACION_v0.md) v0.5, [TIPOLOGIA_v0.md](../../TIPOLOGIA_v0.md) v0.1.

## Discrepancias residuales (ejecutor confirmado)

### 1. doc02 — tipología (transformacion_secundaria)

- **Ejecutor**: `2` — #2 Reducción de la desigualdad
- **Revisor (cursor-grok-4.5/cursor)**: `1` — #1 Desarrollo productivo
- **Adjudicación**: **ejecutor** — R9 tipología: secundaria #2 desigualdad ancla mejor el hilo distributivo de las tesis que #1

### 2. doc04 — interpelación (gran_impulso_ambiental_concreto)

- **Ejecutor**: `No` — El documento no pasa los tres tests operativos de big_push.md. Test 1 (paquete coordinado de inversión): el término "gran impulso ambiental" se menciona citando literalmente la resolución de la CEPAL de 2016 (p.17) y se retoma en el bloque de adaptación sostenible e incluyente (p…
- **Revisor (cursor-grok-4.5/cursor)**: `Parcial` — Documento técnico de escenarios de impactos/costos del cambio climático en Honduras (ECC CA), no una hoja de ruta de inversión de modelo de desarrollo. Test 1 (paquete masivo coordinado): ausente — no hay salto de inversión con montos/instrumentos de despegue simultáneos para Hon…
- **Adjudicación**: **ejecutor** — R9 §1.5/1.6: estudio de impactos/costos; mención de gran impulso sin paquete propio → No

### 3. doc04 — tipología (transformacion_secundaria)

- **Ejecutor**: `11` — #11 Capacidades del Estado
- **Revisor (cursor-grok-4.5/cursor)**: `2` — #2 Reducción de la desigualdad
- **Adjudicación**: **ejecutor** — R9 tipología: secundaria #11 (capacidades) encaja con ECC CA como estudio técnico de política; #2 no es el hilo

### 4. doc06 — interpelación (gran_impulso_ambiental_concreto)

- **Ejecutor**: `No` — El documento no propone un paquete coordinado de inversión masiva ni aterriza en sectores estratégicos con instrumento identificable siguiendo la lógica del Big Push; de hecho, advierte explícitamente contra la lógica de promoción de inversiones (p.38). Chequeo negativo explícito…
- **Revisor (cursor-grok-4.5/cursor)**: `Parcial` — Test 1 (paquete de inversión masiva y coordinada): no se cumple como Big Push de inversiones — el libro exige el fin del modelo de desarrollo vigente y un cambio estructural/cultural hacia otro desarrollo o “buen vivir”, pero reconoce que esa utopía está lejos y prioriza cruces d…
- **Adjudicación**: **ejecutor** — R9 §1.5: advierte contra lógica de promoción de inversiones; sin paquete Big Push → No

### 5. doc06 — tipología (transformacion_secundaria)

- **Ejecutor**: `11` — #11 Capacidades del Estado
- **Revisor (cursor-grok-4.5/cursor)**: `1` — #1 Desarrollo productivo
- **Adjudicación**: **ejecutor** — R9 tipología: secundaria #11 (Estado/gobernanza) frente a #1; el libro no prioriza desarrollo productivo

### 6. doc08 — tipología (transformacion_primaria)

- **Ejecutor**: `11` — #11 Capacidades del Estado
- **Revisor (cursor-grok-4.5/cursor)**: `6` — #6 Sostenibilidad ambiental
- **Adjudicación**: **ejecutor** — R9 tipología objeto/instrumento: gobernanza hídrica → #11 primaria / #6 secundaria

### 7. doc08 — tipología (transformacion_secundaria)

- **Ejecutor**: `6` — #6 Sostenibilidad ambiental
- **Revisor (cursor-grok-4.5/cursor)**: `11` — #11 Capacidades del Estado
- **Adjudicación**: **ejecutor** — R9 tipología: #6 secundaria (clima/ambiente como restricción del recurso)

### 8. doc10 — tipología (transformacion_secundaria)

- **Ejecutor**: `11` — #11 Capacidades del Estado
- **Revisor (cursor-grok-4.5/cursor)**: `1` — #1 Desarrollo productivo
- **Adjudicación**: **ejecutor** — R9 tipología: secundaria #11 (capacidades/implementación Agenda 2030) mejor que #1

### 9. doc12 — interpelación (oportunidades_productivas_sostenibles)

- **Ejecutor**: `Sí` — El documento enumera sectores/actividades concretas de manera reiterada a lo largo de los 12 países y 4 casos (café, ganadería, arroz, maíz, cacao, banano, entre otros) y desarrolla el vínculo con empleo y productividad con cifra propia en el caso de la NAMA Café (150.000 empleos…
- **Revisor (cursor-grok-4.5/cursor)**: `Parcial` — Enumera actividades/tecnologías productivas bajas en carbono (recuperación de pasturas, ILPF, siembra directa, fijación biológica de nitrógeno, NAMA café/ganadería, ganadería climáticamente inteligente). Hay vínculo con productividad (mejoras de ingreso neto e índices productivos…
- **Adjudicación**: **ejecutor** — R9 §1.3: enumeración + NAMA Café con cifra de empleo → Sí

### 10. doc12 — tipología (transformacion_primaria)

- **Ejecutor**: `11` — #11 Capacidades del Estado
- **Revisor (cursor-grok-4.5/cursor)**: `6` — #6 Sostenibilidad ambiental
- **Adjudicación**: **ejecutor** — R9 tipología: inventario institucional PLACA → #11/#6

### 11. doc12 — tipología (transformacion_secundaria)

- **Ejecutor**: `6` — #6 Sostenibilidad ambiental
- **Revisor (cursor-grok-4.5/cursor)**: `11` — #11 Capacidades del Estado
- **Adjudicación**: **ejecutor** — R9 tipología: #6 secundaria (acción climática agropecuaria como contenido de los instrumentos)

### 12. doc13 — interpelación (como_hacerlo_concreto)

- **Ejecutor**: `Parcial` — El documento enumera 8 puntos de acción en el capítulo IV (p.73-78). Aplicando el test de concreción ítem por ítem del §1.4 de INTERPELACION_v0.md (verbo de acción + objeto específico, opcionalmente actor, plazo o métrica): 4 de los 8 nombran un instrumento, tecnología o programa…
- **Revisor (cursor-grok-4.5/cursor)**: `Sí` — Desglose sobre el texto completo de los 8 puntos de acción del capítulo IV (Implicaciones y recomendaciones, pp. 73–77 internas), no sobre el resumen inicial. 5 de 8 pasan el test: datos (informes de sostenibilidad, blockchain, estándares); políticas laborales activas/pasivas con…
- **Adjudicación**: **ejecutor** — R9 §1.4 / ancla Ronda 2: 4/8 no es mayoría → Parcial (no subir a Sí por re-conteo)

### 13. doc15 — interpelación (articulacion_actores)

- **Ejecutor**: `Sí` — El documento nombra un mecanismo institucionalizado de coordinación multiactor dentro de su propio ámbito de aplicación (Centroamérica, subregión analizada en el capítulo III): el Sistema de la Integración Centroamericana (SICA), con mandato presidencial explícito sobre cambio cl…
- **Revisor (cursor-grok-4.5/cursor)**: `No` — Chequeo negativo explícito: se buscó un mecanismo/plataforma/consejo/proceso de planificación multiactor con nombre propio adoptado o propuesto para ALC. No aparece. La articulación se formula en lenguaje genérico (“matriz público-privada”, “acuerdo global” con responsabilidades …
- **Adjudicación**: **ejecutor** — R9 §1.2: SICA + ECC Centroamérica en ámbito del cap. III → Sí (mecanismo vigente, no solo propuesta)

### 14. doc15 — tipología (transformacion_secundaria)

- **Ejecutor**: `10` — #10 Macroeconomía y fiscalidad
- **Revisor (cursor-grok-4.5/cursor)**: `2` — #2 Reducción de la desigualdad
- **Adjudicación**: **ejecutor** — R9 tipología: secundaria #10 (macro/fiscal, matriz público-privada/precios) mejor que #2 genérica

### 15. doc19 — interpelación (como_hacerlo_concreto)

- **Ejecutor**: `No` — Se aplicó el test de concreción ítem por ítem a la lista de desafíos pendientes del capítulo III (p.156-157), la más operativa del documento en cuanto a "cómo hacerlo". De los cinco ítems, solo uno nombra un objeto concreto (una metodología específica, el precio social del carbon…
- **Revisor (cursor-grok-4.5/cursor)**: `Parcial` — No hay una sección única titulada 'recomendaciones'; el 'cómo hacerlo' se concentra en la sección B de la Introducción ('El Estado, la gestión pública y la acción climática', p.24-29), que enumera de forma sistemática, para cada fase del ciclo de gestión, tres argumentos normativ…
- **Adjudicación**: **ejecutor** — R9 §1.4: unidad no puede ser Intro B; lista de desafíos III mayoritariamente genérica → No

