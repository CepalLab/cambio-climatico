# Checkpoint Fase 3.3 - 2026-08-26

## Estado

La Fase 3.3 queda pausada en un punto estable antes de la redaccion final. El
corpus activo es de 238 documentos: 244 historicos menos 6 exclusiones. Los
JSON de Fase 2 siguen siendo la fuente canonica y no fueron reescritos.

## Trabajo completado

- Se documento el contrato analitico v2 y el modelo de conocimiento vivo.
- Se construyeron paquetes de evidencia reproducibles para evolucion de
  enfoques y gobernanza multinivel.
- Se reoriento el analisis desde citas aisladas hacia perfiles documentales
  completos.
- Se construyeron 238 perfiles con pregunta, ambito, resumen narrativo,
  hallazgos, conclusiones, recomendaciones, territorio y tipologia.
- Se creo una matriz candidata de objetos, dominios y funciones con reglas
  ponderadas por titulo, pregunta y resumen.
- Se calibro la matriz sobre 10 perfiles completos; los objetos principales
  fueron coherentes como capa candidata y los secundarios permanecen abiertos.
- Se integro el ambito territorial normalizado v1: regional, subregional,
  nacional, subnacional y multinivel.
- Se integro la tipologia existente, incluida su tension dialectica, como eje
  complementario y no sustitutivo.
- Se genero una sintesis global completa sobre P1, P2 y P3.
- Se generaron paneles de modos analiticos, Big Push/interpelacion y cobertura
  de las nueve preguntas.
- Se genero un borrador de respuestas a las nueve preguntas de investigacion.
- Se fijo la guia de prosa narrativa y se produjo un piloto narrativo de P8.

## Artefactos principales

- `salidas/perfiles_documentales_v1.json`: 238 perfiles directos.
- `salidas/matriz_documental_candidata_v1.json`: objetos, dominios y funciones
  candidatas.
- `salidas/corpus_sintesis_documental_v1.json`: 238 perfiles mas 691
  conclusiones y 956 recomendaciones.
- `salidas/paquete_panoramico_documental_v1.json`: agregados y 30 documentos
  representativos.
- `salidas/paneles_analiticos_v1.json`: modos, Big Push y preguntas.
- `SINTESIS_GLOBAL_COMPLETA_BORRADOR_v1.md`: evolucion del objeto de estudio.
- `RESPUESTAS_PREGUNTAS_FASE3_3_BORRADOR_v1.md`: respuestas P1-P9.
- `PILOTO_PROSA_NARRATIVA_P8_BIG_PUSH_v1.md`: modelo de redaccion.
- `PLAN_CUADROS_GRAFICOS_v1.md`: figuras y cuadros previstos.

## Decisiones metodologicas vigentes

- El informe se construye desde documentos completos; las citas verifican
  hallazgos seleccionados.
- Los objetos, dominios y territorios candidatos no se presentan como
  codificacion experta exhaustiva.
- La tipologia y la tension dialectica complementan la lectura documental.
- El Big Push se explica conceptualmente y se distingue de oportunidad,
  articulacion o recomendacion concreta aisladas.
- La prosa final usa español UTF-8 completo y expande P1 como 2015–2018, P2
  como 2019–2022 y P3 como 2023–2026, aclarando que el corpus llega hasta 2025.

## Validaciones al checkpoint

- 238 perfiles con identificadores unicos y hash de fuente normalizada.
- 237 documentos con conclusiones explicitas y 225 con recomendaciones.
- 691 items de conclusion y 956 items de recomendacion integrados.
- Paneles generados: 24 filas de modos, 36 de interpelacion y 27 de cobertura
  de preguntas.
- 15 citas de las fichas micro verificadas exactamente contra SQLite antes de
  pausarlas.
- Cita literal del piloto Big Push verificada contra `dimension_id` 1525,
  pagina 114.
- JSON, enlaces internos y `git diff --check` validados en los ultimos ciclos.

## Reproduccion

Desde la raiz del repositorio:

```powershell
& .venv/Scripts/python.exe fase3/03_analisis_contenido/scripts/construir_perfiles_documentales_v1.py
& .venv/Scripts/python.exe fase3/03_analisis_contenido/scripts/clasificar_perfiles_documentales_v1.py
& .venv/Scripts/python.exe fase3/03_analisis_contenido/scripts/seleccionar_calibracion_documental_v1.py
& .venv/Scripts/python.exe fase3/03_analisis_contenido/scripts/construir_paquete_panoramico_documental_v1.py
& .venv/Scripts/python.exe fase3/03_analisis_contenido/scripts/construir_corpus_sintesis_documental_v1.py
& .venv/Scripts/python.exe fase3/03_analisis_contenido/scripts/generar_paneles_analiticos_v1.py
```

## Punto de reanudacion

La proxima mision es redactar el informe por secciones narrativas, comenzando
por metodo, evolucion del objeto de estudio y Gran Impulso Ambiental. Cada
seccion debe recuperar sus citas canonicas despues de que el argumento haya
sido seleccionado y debe proponer los cuadros o graficos que realmente
ayuden a leerlo.

## Registro

Las decisiones acumuladas hasta este checkpoint estan en
`decisiones/registro_decisiones_v1.json`; la ultima decision es
`DEC-F3-2026-08-26-013`.