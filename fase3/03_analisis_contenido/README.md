# Fase 3.3 - Analisis de contenido

Esta carpeta contiene los productos analiticos derivados del corpus activo de
238 documentos. No modifica los JSON canonicos de Fase 2 ni reemplaza la base
SQLite `fase3-analitica-v1`.

## Estado al 2026-08-27

La integración editorial está completada en el informe maestro v2: 238
publicaciones activas (2015–2026), cinco figuras reproducibles, cuatro cuadros
y un anexo técnico independiente. La revisión temática independiente fue
incorporada y las validaciones de scripts, Markdown y `git diff --check` fueron
limpias. La siguiente fase no es analítica: corresponde a revisión humana final
y preparación de la versión de circulación en el formato que defina el equipo.

## Punto de entrada

- [ESPECIFICACION_ANALITICA_v2.md](ESPECIFICACION_ANALITICA_v2.md): contrato de
  trabajo, modelo de evidencia y plan de ejecucion.
- [CHECKPOINT_FASE3_3_2026-08-26.md](CHECKPOINT_FASE3_3_2026-08-26.md): estado
  consolidado y punto de reanudacion.

## Estructura prevista

- `scripts/`: consultas reproducibles, construccion de paquetes de evidencia y
  exportaciones del grafo derivado.
- `salidas/`: metricas, paquetes de evidencia, fichas de hallazgo, grafo y
  borradores de informe versionados.
- `contratos/`: definiciones de formatos y ciclo de vida del conocimiento.
- `preguntas/`, `conceptos/`, `hallazgos/` y `decisiones/`: registros
  versionados del activo analitico vivo.
- `grafo/`: exportaciones navegables; no constituye una base alternativa.

## Capa viva minima (M2)

- [contratos/MODELO_CONOCIMIENTO_VIVO_v1.md](contratos/MODELO_CONOCIMIENTO_VIVO_v1.md): contrato de formatos y procedencia.
- [preguntas/catalogo_preguntas_v1.json](preguntas/catalogo_preguntas_v1.json): preguntas de investigacion activas.
- [conceptos/catalogo_conceptos_v1.json](conceptos/catalogo_conceptos_v1.json): concepto de ejemplo en estado `draft`.
- [hallazgos/F3-M2-EJEMPLO-001.json](hallazgos/F3-M2-EJEMPLO-001.json): ficha demostrativa, no promocionable al informe.
- [decisiones/registro_decisiones_v1.json](decisiones/registro_decisiones_v1.json): decision de adopcion del formato.
- [grafo/grafo_m2_ejemplo_v1.json](grafo/grafo_m2_ejemplo_v1.json): recorrido de evidencia de ejemplo.

## Paquetes de evidencia (M3)

- `scripts/generar_paquetes_evidencia_v1.py`: genera los paquetes reproducibles
  de los dos pilotos desde SQLite.
- `salidas/paquete_evolucion_enfoques_v1.json` y `.md`: evidencia para la
  evolucion de enfoques CEPAL, 2015–2026.
- `salidas/paquete_gobernanza_multinivel_v1.json` y `.md`: evidencia para
  gobernanza multinivel, capacidades e implementacion.

Los paquetes exportan el universo de citas candidatas. No constituyen aun una
seleccion cualitativa ni hallazgos aprobados.

## Piloto y revision humana (M4)

- `scripts/seleccionar_muestra_piloto_v1.py`: selecciona una muestra de
  cobertura y genera planillas de revision para ambos pilotos.
- [GUIA_REVISION_HUMANA_PILOTO_v1.md](GUIA_REVISION_HUMANA_PILOTO_v1.md): procedimiento y criterios para la revision humana.
- `salidas/muestra_lectura_<piloto>_v1.*`: muestra reproducible por piloto.
- `salidas/revision_humana_<piloto>_v1.csv`: registro editable de decisiones.

La muestra distribuye lectura por estratos; no es estadistica ni equivale a
hallazgos aprobados.

## Hallazgos draft para revision

- [hallazgos/REVISION_HALLAZGOS_EVOLUCION_v1.md](hallazgos/REVISION_HALLAZGOS_EVOLUCION_v1.md): lectura humana de las cinco primeras hipotesis comparativas.
- `hallazgos/F3-EVO-001_*.json` a `F3-EVO-005_*.json`: fichas con metricas,
  citas, limites y preguntas de revision.

## Perfil global del corpus (reorientacion 2026-08-26)

- [PLAN_REORIENTACION_DOCUMENTAL_v1.md](PLAN_REORIENTACION_DOCUMENTAL_v1.md): secuencia aprobada para iniciar desde documentos completos.
- [TAXONOMIA_DOCUMENTAL_ANALITICA_v1.md](TAXONOMIA_DOCUMENTAL_ANALITICA_v1.md): objetos, dominios, funciones y relaciones a calibrar.
- `scripts/construir_perfiles_documentales_v1.py`: construye perfiles directos desde los JSON canonicos.
- `salidas/perfiles_documentales_v1.json` y `salidas/panorama_perfiles_documentales_v1.md`: derivados de entrada para el analisis global.
- `scripts/clasificar_perfiles_documentales_v1.py`: aplica reglas ponderadas y transparentes para generar asignaciones candidatas.
- `salidas/matriz_documental_candidata_v1.json` y `salidas/panorama_documental_candidato_v1.md`: mapa candidato de objetos, dominios y funciones por documento.
- `salidas/calibracion_documental_taxonomia_v1.md`: diez perfiles completos para calibrar la taxonomia antes de interpretar agregados.
- [LECTURA_GLOBAL_DOCUMENTAL_BORRADOR_v1.md](LECTURA_GLOBAL_DOCUMENTAL_BORRADOR_v1.md): primera sintesis global revisable desde perfiles documentales.
- [SINTESIS_GLOBAL_COMPLETA_BORRADOR_v1.md](SINTESIS_GLOBAL_COMPLETA_BORRADOR_v1.md): sintesis revisable sobre los 238 perfiles documentales completos.
- [RESPUESTAS_PREGUNTAS_FASE3_3_BORRADOR_v1.md](RESPUESTAS_PREGUNTAS_FASE3_3_BORRADOR_v1.md): respuestas revisables a las nueve preguntas de investigacion.
- [SINTESIS_GLOBAL_COMPLETA_BORRADOR_v2.md](SINTESIS_GLOBAL_COMPLETA_BORRADOR_v2.md): mapa corregido activo, pendiente de la compuerta de revision.
- [RESPUESTAS_PREGUNTAS_FASE3_3_BORRADOR_v2.md](RESPUESTAS_PREGUNTAS_FASE3_3_BORRADOR_v2.md): respuestas v2 con las cautelas de composicion, evolucion y Big Push.
- `scripts/verificar_ejes_canonicos_v1.py` y `salidas/verificacion_ejes_canonicos_v1.*`: verificacion reproducible de perdidas y danos, transicion justa y responsabilidades diferenciadas.
- [revisiones/COMPUERTA_REVISION_V2.md](revisiones/COMPUERTA_REVISION_V2.md): revision humana y auditoria de segundo modelo requeridas antes de la prosa narrativa.
- [revisiones/AUDITORIA_INDEPENDIENTE_BLOQUES_02_03_v1.md](revisiones/AUDITORIA_INDEPENDIENTE_BLOQUES_02_03_v1.md): auditoria de citas, alcance y consistencia de los bloques 02 y 03.
- [revisiones/VERIFICACION_REPRODUCIBILIDAD_PAQUETES_v1.md](revisiones/VERIFICACION_REPRODUCIBILIDAD_PAQUETES_v1.md): cierre de hashes y cobertura temporal de los paquetes de evidencia.
- [ARQUITECTURA_INFORME_30P_v1.md](ARQUITECTURA_INFORME_30P_v1.md): estructura de 30 paginas con preguntas, anclas y figuras previstas.
- [PLAN_EXPANSION_INFORME_V2.md](PLAN_EXPANSION_INFORME_V2.md): mapa aprobado de expansion hacia un informe de aproximadamente 20 paginas de prosa.
- [FICHAS_EXPANSION_INFORME_V2.md](FICHAS_EXPANSION_INFORME_V2.md): fichas de territorio, tensiones y coherencia de implementacion pendientes de revision.
- `scripts/construir_tensiones_dialecticas_v1.py` y `salidas/tensiones_dialecticas_v1.*`: derivado canonico de tensiones dialecticas para la expansion.
- [INFORME_MAESTRO_30P_BORRADOR_v1.md](INFORME_MAESTRO_30P_BORRADOR_v1.md): integracion editorial del resumen, los tres bloques narrativos y los materiales graficos.
- [INFORME_MAESTRO_V2_BORRADOR.md](INFORME_MAESTRO_V2_BORRADOR.md): informe integrado de 12 secciones, con 7.134 palabras, figuras embebidas y cuadro de coherencia.
- [ANEXO_TECNICO_INFORME_V2.md](ANEXO_TECNICO_INFORME_V2.md): metodología ampliada, rúbrica del Gran Impulso Ambiental, exclusiones y trazabilidad de citas ancla.
- [RESUMEN_EJECUTIVO_INFORME_v1.md](RESUMEN_EJECUTIVO_INFORME_v1.md): borrador de las dos paginas iniciales, basado en los bloques narrativos revisados.
- [BLOQUE_NARRATIVO_01_METODO_EVOLUCION_BIG_PUSH_v1.md](BLOQUE_NARRATIVO_01_METODO_EVOLUCION_BIG_PUSH_v1.md): borrador de trabajo del primer bloque, pendiente de la compuerta v2.
- [BLOQUE_NARRATIVO_02_P1_P7_v1.md](BLOQUE_NARRATIVO_02_P1_P7_v1.md): borrador de trabajo sobre impactos, instrumentos, implementacion y desafios de P1-P7.
- [BLOQUE_NARRATIVO_03_P9_CONCLUSIONES_AGENDA_v1.md](BLOQUE_NARRATIVO_03_P9_CONCLUSIONES_AGENDA_v1.md): borrador de trabajo sobre participacion, derechos, conclusiones y agenda.
- [BLOQUE_NARRATIVO_04_EXPANSION_V2.md](BLOQUE_NARRATIVO_04_EXPANSION_V2.md): borrador sobre escalas, capacidades, transformaciones, tensiones y coherencia de implementacion.
- [cuadros_01_02_cobertura.md](salidas/figuras_informe_v1/cuadros_01_02_cobertura.md): cuadros 1 a 4 del informe.
- [figura_01_objetos_por_periodo.png](salidas/figuras_informe_v1/figura_01_objetos_por_periodo.png), [figura_02_modos_analiticos.png](salidas/figuras_informe_v1/figura_02_modos_analiticos.png), [figura_03_panel_big_push.png](salidas/figuras_informe_v1/figura_03_panel_big_push.png) y [figura_04_territorio_tipologia.png](salidas/figuras_informe_v1/figura_04_territorio_tipologia.png): figuras reproducibles del informe.
- `salidas/paneles_analiticos_v1.json` y `.md`: modos analiticos, Big Push e interpelacion, y cobertura de preguntas.
- [PLAN_CUADROS_GRAFICOS_v1.md](PLAN_CUADROS_GRAFICOS_v1.md): cuadros y graficos propuestos para el informe.
- [GUIA_REDACCION_NARRATIVA_Y_EVIDENCIA_v1.md](GUIA_REDACCION_NARRATIVA_Y_EVIDENCIA_v1.md): patron de prosa, uso de documentos ancla y traduccion de la nomenclatura metodologica.
- [PILOTO_PROSA_NARRATIVA_P8_BIG_PUSH_v1.md](PILOTO_PROSA_NARRATIVA_P8_BIG_PUSH_v1.md): modelo narrativo para oportunidades y Big Push.

Los hallazgos `F3-EVO` estan pausados como ejercicios microanaliticos. El mapa
activo es v2; las proximas conclusiones partiran de perfiles documentales y
usaran citas como respaldo despues de superar su compuerta de revision.

## Reanudación

El [CHECKPOINT_FASE3_3_2026-08-27.md](CHECKPOINT_FASE3_3_2026-08-27.md) es el
punto de entrada de una sesión nueva. Contiene el estado de cierre, las órdenes
de reproducción, las validaciones realizadas y los pendientes de circulación.

## Regla de procedencia

Cada producto debe declarar `fase3-analitica-v1`, denominador, filtros, las 6
exclusiones aplicadas y sus referencias de evidencia. Una referencia valida
conserva `document_id`, `dimension_id`, pagina, `source_sha256` y ruta al JSON
canonico cuando corresponda.

Las anotaciones, conceptos, hallazgos y aristas del grafo son derivados
revisables. Nunca se confunden con evidencia literal ni se escriben de vuelta
en los JSON canonicos.
