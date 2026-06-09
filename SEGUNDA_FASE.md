# Documentos para Segunda Fase - Guía de Referencia

## Descripción General

La vista "Documentos para 2da fase" es una nueva página en la aplicación Streamlit que proporciona un listado depurado de publicaciones sobre cambio climático para la segunda fase del análisis.

## Ubicación en la Aplicación

- **Módulo**: `segunda_fase.py`
- **Integrado en**: `app.py` como tercera pestaña en la navegación principal
- **Ícono**: `:material/checklist:`
- **URL**: `/segunda-fase`

## Criterios de Filtrado

### Documentos Excluidos

La vista excluye los siguientes tipos de documentos:

1. **Versiones duplicadas**
   - Acuerdo Regional (disponible en varios idiomas)

2. **Documentos administrativos**
   - Reglas de procedimiento del Acuerdo de Escazú
   - Catálogo de publicaciones de la División de Desarrollo Sostenible y Asentamientos Humanos

3. **Documentos inaccesibles**
   - Versiones accesibles de documentos de CEPAL (patrón: contiene "accesible")

4. **Revistas de CEPAL**
   - Se excluyen todos los documentos clasificados como "Boletines y Revistas"
   - Incluye publicaciones como "The Hummingbird" y otras revistas CEPAL
   - **Nota**: Según las instrucciones de los expertos, no se incluyen revistas ya que no todos los artículos son de autoría de CEPAL

### Documentos Agregados

Se agregan 14 documentos clave del Período de Sesiones de CEPAL y del Foro Regional sobre Desarrollo Sostenible:

#### Período de Sesiones de CEPAL
1. **América Latina y el Caribe ante las trampas del desarrollo: Transformaciones indispensables y cómo gestionarlas** (2024)
   - URL: https://repositorio.cepal.org/server/api/core/bitstreams/ddaf4444-dcbc-48a9-afd2-06306ac3e5c3/content

2. **Hacia la transformación del modelo de desarrollo en América Latina y el Caribe: producción, inclusión y sostenibilidad** (2022)
   - URL: https://repositorio.cepal.org/server/api/core/bitstreams/cfdfbffc-660a-4b8c-86e8-532bcf884af5/content

3. **Construir un nuevo futuro: una recuperación transformadora con igualdad y sostenibilidad** (2020)
   - Handle: https://hdl.handle.net/11362/46682

4. **La ineficiencia de la desigualdad** (2018)
   - URL: https://repositorio.cepal.org/server/api/core/bitstreams/cd373168-ed4d-4bb7-b70a-4d9fd80c68a9/content

5. **Horizontes 2030: la igualdad en el centro del desarrollo Sostenible** (2016)
   - URL: https://periododesesiones.cepal.org/36/es/horizontes-2030-la-igualdad-centro-desarrollo-sostenible

#### Foro Regional sobre Desarrollo Sostenible
6. **Agenda 2030 en América Latina y el Caribe: ¿cómo acelerar el paso hacia su cumplimiento en la nueva era de incertidumbre y fragmentación geopolítica?** (2026)
   - URL: https://foroalc2030.cepal.org/2026/es/documentos/agenda-2030-america-latina-caribe-como-acelerar-paso-su-cumplimiento-la-nueva-era

7. **América Latina y el Caribe y la Agenda 2030 a cinco años de la meta: ¿cómo gestionar las transformaciones para acelerar el progreso?** (2025)
   - URL: https://foroalc2030.cepal.org/2025/es/documentos/america-latina-caribe-la-agenda-2030-cinco-anos-la-meta-como-gestionar-transformaciones

8. **América Latina y el Caribe ante el desafío de acelerar el paso hacia el cumplimiento de la Agenda 2030: transiciones hacia la sostenibilidad** (2024)
   - URL: https://foroalc2030.cepal.org/2024/es/documentos/america-latina-caribe-desafio-acelerar-paso-cumplimiento-la-agenda-2030-transiciones-la

9. **América Latina y el Caribe en la mitad del camino hacia 2030: avances y propuestas de aceleración** (2023)
   - URL: https://foroalc2030.cepal.org/2023/es/documentos/america-latina-caribe-la-mitad-camino-2030-avances-propuestas-aceleracion

10. **Una década de acción para un cambio de época** (2022)
    - Handle: https://hdl.handle.net/11362/47745
    - **Estado**: No encontrado en el dataset original (será creado como documento adicional)

11. **INFORME ANUAL DE PROGRESO: Construir un futuro mejor: acciones para fortalecer la Agenda 2030 para el Desarrollo Sostenible** (2021)
    - URL: https://foroalc2030.cepal.org/2021/es/documentos/informe-anual-progreso-construir-un-futuro-mejor-acciones-fortalecer-la-agenda-2030
    - **Estado**: No encontrado en el dataset original (será creado como documento adicional)

12. **Informe de avance cuatrienal sobre el progreso y los desafíos regionales de la Agenda 2030 para el Desarrollo Sostenible en América Latina y el Caribe** (2019)
    - URL: https://foroalc2030.cepal.org/2019/es/documentos/informe-avance-cuatrienal-progreso-desafios-regionales-la-agenda-2030-desarrollo

13. **Segundo informe anual sobre el progreso y los desafíos regionales de la Agenda 2030 para el Desarrollo Sostenible en América Latina y el Caribe** (2018)
    - URL: https://foroalc2030.cepal.org/2018/es/documentos/segundo-informe-anual-progreso-desafios-regionales-la-agenda-2030-desarrollo-sostenible

14. **Informe anual sobre el progreso y los desafíos regionales de la Agenda 2030 para el Desarrollo Sostenible en América Latina y el Caribe** (2017)
    - URL: https://foroalc2030.cepal.org/2017/es/documentos/informe-anual-progreso-desafios-regionales-la-agenda-2030-desarrollo-sostenible-america

## Proceso de Generación del Listado

1. **Carga de datos**: Se cargan todos los registros del dataset principal
2. **Filtro inicial**: Se filtran solo documentos que contienen el tema "CAMBIO CLIMÁTICO"
3. **Aplicación de exclusiones**: Se aplican los criterios de exclusión descritos arriba
4. **Agregación de documentos**: Se agregan los 14 documentos especificados (12 encontrados en el dataset + 2 nuevos)
5. **Salida**: Se genera una tabla interactiva y un archivo CSV descargable

## Columnas Mostradas

- **dc.title**: Título del documento
- **dc.year**: Año de publicación
- **division**: División de CEPAL responsable
- **cepal.topicSpa**: Temas asignados
- **dc.identifier.uri**: Enlace al documento

## Funcionalidad Técnica

### Funciones Principales

- `excluir_documentos(df)`: Aplica los criterios de exclusión al DataFrame
- `agregar_documentos(df_base)`: Agrega los 14 documentos especificados
- `main()`: Renderiza la página en Streamlit

### Interactividad

- Tabla interactiva con scroll horizontal/vertical
- Botón de descarga en formato CSV
- Indicadores de cantidad de documentos en cada etapa

## Archivos Relacionados

- `segunda_fase.py`: Módulo principal de esta funcionalidad
- `app.py`: Integración en la aplicación principal
- `datos.py`: Módulo de carga de datos
- `topic_spa.py`: Parsing de temas
- `verificar_documentos.py`: Script de verificación (solo documentación)

## Notas Importantes

1. Los documentos faltantes ("Una década de acción para un cambio de época" y el "INFORME ANUAL DE PROGRESO") se crean como nuevas entradas en el listado final para asegurar su inclusión.

2. La exclusión de revistas sigue la recomendación de los expertos: "Respecto de las revistas de CEPAL, sugeririamos no incluirlas, ya que no todos los artículos son de autoría de CEPAL."

3. El filtro de "accesible" excluye versiones adaptadas de documentos que no son la versión oficial de CEPAL.

4. La columna `division` se usa para excluir publicaciones de la División de Desarrollo Sostenible y Asentamientos Humanos, pero solo aquellas catalogadas como tales en el dataset.

## Cambios Futuros Sugeridos

- Agregar un campo para indicar si un documento fue agregado (no encontrado en el dataset original)
- Implementar sistema de etiquetado para marcar documentos como revisados
- Agregar filtros interactivos en la interfaz
- Crear reportes de análisis con estadísticas de cobertura
