# Revisión de 11362/37791 — intento 2

**Decisión:** rechazado; no aprobar ni liberar los otros documentos.

El intento mejoró la cobertura de los resúmenes, el nombre del archivo, UTF-8 y la literalidad global de las citas. Sin embargo, la comprobación inicial solo verificaba que la cita apareciera en algún lugar del TXT: no comprobaba la página ni que perteneciera a la sección asignada.

La revisión contra el PDF encontró:

- 31 de 36 citas literales con página declarada incorrecta.
- 1 cita adicional no localizable literalmente en el PDF.
- Citas de las páginas iniciales reutilizadas como evidencia de capítulos posteriores; por ejemplo, una acción sobre residuos de la página 24 fue declarada como página 89.
- Rangos de los once capítulos desplazados dos páginas: los inicios reales son 11, 35, 41, 63, 71, 87, 101, 109, 121, 129 y 141, no 13, 37, 43, 65, 73, 89, 103, 111, 123, 131 y 142/143.
- `paginas_cuerpo = 141` es incompatible con el capítulo XI sustantivo, que ocupa las páginas 141-148.
- `como_hacerlo_concreto` declara `5 de 5` ítems concretos pero mantiene `Parcial`; la regla vigente asigna `Sí` cuando la mayoría pasa, salvo que primero se justifique que no existe una unidad válida de recomendaciones propias para construir el tally.

La causa principal ya no es UTF-8 ni truncamiento: el modelo localizó frases en el documento completo, pero no mantuvo su pertenencia a página y capítulo. El validador de citas ahora admite `--pdf` y bloquea este modo de falla.
