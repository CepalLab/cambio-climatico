# Plan de normalización de metadatos v1

## Alcance

La normalización parte de los 238 documentos activos definidos por
`inventario_corpus_v1.json` y `exclusiones_corpus_v1.csv`. Los JSON de Fase 2
son la fuente canónica y permanecen sin modificaciones.

El primer perfil reproducible está en `01_normalizacion/salidas/perfil_metadatos_v1.json`, generado por
`perfilar_metadatos.py`. Ese perfil conserva los valores originales y permite
diseñar los vocabularios a partir de las variantes observadas.

## Estado operativo

La normalización v1 se ejecutó sobre los **238 documentos activos** y produjo
`01_normalizacion/salidas/normalizacion_corpus_activo_v1.json`,
`01_normalizacion/salidas/corpus_activo_normalizado_v1.json` y
`01_normalizacion/revision/cola_revision_metadatos_v1.csv`. Es una base apta para comenzar los análisis
agregados: cada pendiente conserva su fuente y puede ajustarse en una versión
posterior del diccionario sin rehacer el corpus canónico.

La corrida v1 generó 238 documentos y 2.292 relaciones. Se validaron unicidad
de documentos, integridad referencial, hashes de los JSON fuente e idempotencia.
Las adjudicaciones automáticas no sustituyen la revisión futura de relaciones
semánticas; los valores no resueltos están reportados explícitamente.

## Principio de doble representación

Cada dato debe conservar:

1. El valor original, tal como aparece en el JSON.
2. Una o más representaciones normalizadas, con identificador canónico.
3. La relación con el documento y, cuando corresponda, el rol, la página,
   el método de extracción y la certeza.

La normalización no debe sustituir ni corregir silenciosamente el texto
original. Una inferencia dudosa queda como candidata para revisión.

## Derivados mínimos

### `documentos`

Una fila por documento: `documento_id`, `handle`, título, fecha, idioma,
tipo documental original y normalizado, páginas, división, transformación
primaria/secundaria y hashes del JSON fuente.

### `personas` y `organizaciones`

Entidades con `entidad_id`, nombre original, nombre canónico, tipo de entidad
y variantes conocidas. `documento_entidades` relaciona cada entidad con el
documento y conserva el rol: autor, editor, compilador, institución autora,
financiador, colaborador o referente.

La autoría compuesta no se separa por coma de forma ciega: expresiones como
"autores de los textos originales compilados" deben conservar su alcance y
rol específico.

### `paises` y `documento_ambitos`

Los países se normalizan a nombre canónico, código ISO y subregión CEPAL.
`documento_ambitos` distingue sujeto analizado, caso de estudio, ámbito de
aplicación y referente comparativo. Un país mencionado no se convierte
automáticamente en país analizado.

El ámbito de aplicación se clasifica, cuando la evidencia lo permite, en
`regional`, `subregional`, `nacional`, `subnacional` o `multinivel`. Para el nivel
subnacional se conserva el detalle: ciudad, municipio, provincia, departamento,
región, cuenca, urbano, rural o sectorial. `multinivel` se usa cuando el texto
combina explícitamente dos o más niveles de gobierno o escala territorial.

### `sectores` y `documento_sectores`

Se conserva el texto `sectorial` y se lo vincula a un vocabulario controlado.
La relación debe indicar si el sector es objeto principal, sector afectado,
sector de intervención, sector instrumental o mención contextual.

### `tipos_documentales`

Se conserva `tipo_documento` y `tipo_documento_climatico` por separado. El
primero describe el género editorial; el segundo, la función analítica del
documento dentro del corpus. Un valor original puede mapear a más de una
categoría normalizada solo con justificación explícita.

### `secciones`, `dimensiones` y `citas`

Mantienen la jerarquía, páginas, dimensiones y citas ya auditadas. Las nuevas
entidades pueden relacionarse con una sección o cita cuando la evidencia
permita atribuirles ese nivel de detalle; si no, quedan a nivel de documento.

## Vocabularios iniciales a construir

- Países y subregiones: nombres canónicos, ISO y variantes lingüísticas.
- Sectores: agricultura, agua, energía, transporte, salud, vivienda/ciudades,
  industria, comercio, finanzas, ecosistemas, empleo y protección social.
- Géneros editoriales: estudio técnico, documento de proyecto, informe,
  informe insignia/Panorama, policy brief, nota técnica, compilación,
  memoria de seminario, documento de trabajo, informe estratégico, catálogo
  y otro.
- Entidades: personas, instituciones públicas, organismos internacionales,
  universidades, empresas, bancos y redes.
- Roles y relaciones geográficas: vocabularios cerrados y versionados.

Estos vocabularios son propuestas iniciales. Las variantes ambiguas deben
quedar en una cola de revisión, no forzarse a una categoría.

## Secuencia de implementación

1. Perfilar y revisar las variantes de mayor frecuencia y mayor ambigüedad.
2. Versionar los diccionarios de países, sectores, tipos y entidades.
3. Generar derivados de prueba para una muestra contrastiva de 15–20 casos.
4. Validar unicidad, integridad referencial, cobertura, trazabilidad e
   idempotencia.
5. Escalar al corpus activo y generar un reporte de valores no emparejados.

## Criterios de aceptación

- Ningún documento activo desaparece del derivado `documentos`.
- Cada relación apunta a un `documento_id` y, cuando exista, a una entidad
  canónica válida.
- Todo valor normalizado conserva su valor fuente y método de resolución.
- Repetir la corrida produce los mismos derivados con la misma versión de
  diccionarios.
- Los no emparejados se reportan explícitamente y no se confunden con faltantes.