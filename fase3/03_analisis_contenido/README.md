# Fase 3.3 - Analisis de contenido

Esta carpeta contiene los productos analiticos derivados del corpus activo de
238 documentos. No modifica los JSON canonicos de Fase 2 ni reemplaza la base
SQLite `fase3-analitica-v1`.

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
  evolucion de enfoques CEPAL, 2015-2025.
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
- `salidas/paneles_analiticos_v1.json` y `.md`: modos analiticos, Big Push e interpelacion, y cobertura de preguntas.
- [PLAN_CUADROS_GRAFICOS_v1.md](PLAN_CUADROS_GRAFICOS_v1.md): cuadros y graficos propuestos para el informe.
- [GUIA_REDACCION_NARRATIVA_Y_EVIDENCIA_v1.md](GUIA_REDACCION_NARRATIVA_Y_EVIDENCIA_v1.md): patron de prosa, uso de documentos ancla y traduccion de la nomenclatura metodologica.
- [PILOTO_PROSA_NARRATIVA_P8_BIG_PUSH_v1.md](PILOTO_PROSA_NARRATIVA_P8_BIG_PUSH_v1.md): modelo narrativo para oportunidades y Big Push.

Los hallazgos `F3-EVO` estan pausados como ejercicios microanaliticos. Las
proximas conclusiones partiran de perfiles documentales y usaran citas como
respaldo.

## Regla de procedencia

Cada producto debe declarar `fase3-analitica-v1`, denominador, filtros, las 6
exclusiones aplicadas y sus referencias de evidencia. Una referencia valida
conserva `document_id`, `dimension_id`, pagina, `source_sha256` y ruta al JSON
canonico cuando corresponda.

Las anotaciones, conceptos, hallazgos y aristas del grafo son derivados
revisables. Nunca se confunden con evidencia literal ni se escriben de vuelta
en los JSON canonicos.