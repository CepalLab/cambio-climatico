# Taxonomia documental analitica v1

**Estado:** propuesta para calibrar sobre perfiles documentales  
**Unidad de analisis:** documento completo, con respaldo en su pregunta,
resumen, hallazgos, conclusiones y recomendaciones canonicas.

## Proposito

La taxonomia organiza el panorama global de lo que estudia la CEPAL. No
reemplaza las nueve dimensiones de Fase 2 ni convierte relaciones sugeridas en
causalidad. Toda asignacion posterior debe conservar su texto fuente y estado
de revision.

## 1. Objeto principal de estudio

Un documento puede tener uno o mas objetos, con uno marcado como principal:

| ID | Objeto | Definicion breve |
| --- | --- | --- |
| `impactos_vulnerabilidad` | Impactos y vulnerabilidad | Efectos climaticos, riesgos y poblaciones o territorios expuestos. |
| `adaptacion_resiliencia` | Adaptacion y resiliencia | Medidas, capacidades o sistemas para enfrentar impactos. |
| `mitigacion_descarbonizacion` | Mitigacion y descarbonizacion | Reduccion de emisiones, energia limpia y transicion tecnologica. |
| `transicion_productiva` | Transformacion productiva | Cambio estructural, empleo, innovacion y sectores sostenibles. |
| `gobernanza_capacidades` | Gobernanza y capacidades estatales | Institucionalidad, coordinacion, regulacion, informacion y participacion. |
| `financiamiento_inversion` | Financiamiento e inversion | Fiscalidad, presupuesto, instrumentos financieros y movilizacion de recursos. |
| `igualdad_proteccion_social` | Igualdad y proteccion social | Pobreza, genero, cuidados, empleo y distribucion de impactos. |
| `territorio_ciudad` | Territorio, ciudades y multinivel | Escala subnacional, vivienda, infraestructura y coordinacion territorial. |
| `ecosistemas_recursos` | Ecosistemas y recursos naturales | Agua, agricultura, biodiversidad, costas y sistemas alimentarios. |
| `informacion_prospectiva` | Informacion, medicion y prospectiva | Modelos, escenarios, indicadores, datos y evaluacion. |

## 2. Dominios o variables analizadas

Cada perfil puede combinar los siguientes dominios: `ambiental`, `social`,
`productivo`, `macroeconomico`, `financiero`, `institucional`, `territorial`,
`sectorial` e `informacion_prospectiva`.

La asignacion debe responder que variable o sistema se estudia, no solo que
palabra aparece. Por ejemplo, un impuesto al carbono puede ser financiero,
macroeconomico e institucional a la vez.

## 3. Ambito territorial

El lugar o escala de aplicacion se registra como eje independiente del objeto
de estudio. Se reutilizan los candidatos normalizados v1 y su estado de
revision: `regional`, `subregional`, `nacional`, `subnacional` y `multinivel`.

Un documento puede ocupar varias escalas. `multinivel` no significa solo que
menciona varios lugares: se reserva para articulacion explicita entre lo
subnacional y un nivel nacional o superior. Los referentes externos no entran
en este eje; permanecen separados en `referentes_dependencias`.

## 4. Tipologia existente y tension dialectica

La tipologia de Fase 2 se incorpora como una capa complementaria ya adjudicada:
transformacion primaria, secundaria, tipo documental climatico y tension
dialectica. No sustituye objetos, dominios ni funciones: permite preguntar que
problema de desarrollo organiza el documento y que tension intenta procesar.

La `tension_dialectica` se conserva como texto canonico y puede alimentar el
grafo como nodo de interpretacion documental. No se reduce automaticamente a
una relacion causal ni se reescribe durante la clasificacion de variables.

## 5. Funcion analitica del documento

Las funciones no son causales y pueden coexistir:

- `diagnostica`: caracteriza causas, condiciones o brechas.
- `analiza`: estudia mecanismos, impactos o asociaciones.
- `prospecta`: proyecta escenarios o trayectorias.
- `evalua_implementacion`: revisa avances, instrumentos o resultados.
- `propone_intervenir`: formula recomendaciones o instrumentos.

## 6. Relaciones explicitadas

Solo se registra una relacion si el texto canonico la formula de forma clara.
Los verbos permitidos son `afecta`, `condiciona`, `habilita`, `restringe`,
`requiere`, `contribuye_a` y `propone_intervenir_sobre`.

Una coocurrencia de variables no crea una arista. Si la relacion es una
interpretacion del analista, se marca `draft` y no se presenta como afirmacion
de CEPAL.

## 7. Fuente y revision

La primera asignacion se generara como candidata a partir de campos directos
del perfil documental. Las conclusiones y recomendaciones se analizaran por
separado: describen lo que CEPAL concluye y propone, no necesariamente el
objeto principal del documento.