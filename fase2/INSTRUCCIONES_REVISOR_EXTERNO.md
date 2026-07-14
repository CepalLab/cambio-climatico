# Instrucciones para el revisor ciego externo — verificación cruzada de veredictos

**Fecha**: 2026-07-14 (Ronda 6)
**Estado**: v1. Diseñado a partir de la prueba de portabilidad multimodelo de Ronda 5
([pilot/EVALUACION_MULTIMODELO_DOC09.md](pilot/EVALUACION_MULTIMODELO_DOC09.md)).
**Qué es**: instrucciones autocontenidas para correr una **segunda lectura ciega** de la parte subjetiva
del pipeline (interpelación + tipología) en un harness/modelo **externo** al que corrió el ejecutor.
Para el piloto de la muestra de 17: **DeepSeek en OpenCode** (el mejor de los 4 modelos nuevos en la prueba
de Ronda 5, con perfil de error complementario al ejecutor). Eventualmente, cualquier harness/modelo que
pase el [protocolo de portabilidad](GUIA_OPERATIVA_PIPELINE.md#protocolo-de-prueba-de-portabilidad-de-harnessmodelo).
**Qué NO es**: no es una etapa del pipeline del ejecutor ([GUIA_OPERATIVA_PIPELINE.md](GUIA_OPERATIVA_PIPELINE.md))
ni re-hace la extracción (resúmenes, secciones, dimensiones) — solo re-deriva los **veredictos**, que es
donde la prueba de Ronda 5 mostró varianza entre modelos.

## 1. Cuándo se corre

**Después de completado el lote del ejecutor** (no documento a documento): se corre la revisión en tanda
sobre todos los documentos del lote, se compara contra los JSON del ejecutor, y se adjudica. Correrla por
lotes es deliberado: el revisor vive en otro harness operado a mano, y una sola sesión de revisión por lote
cuesta menos operación que intercalar revisiones por documento.

## 2. Regla de ceguera (la que hace válido el ejercicio)

El revisor **no debe ver, en ningún momento**:

- los JSON producidos por el ejecutor (`pilot/docNN_*.json` del lote en revisión);
- los tres JSON piloto calibrados (doc09, doc11, doc13) — contienen veredictos resueltos;
- los anexos divulgativos de `para_equipo_curso/` (son versiones legibles de esos mismos veredictos);
- este mismo repositorio completo — darle **solo** los insumos de la sección 3.

Si el revisor vio cualquiera de esos artefactos, esa revisión queda contaminada y no sirve como segunda
lectura independiente: anclarse a la salida del ejecutor produce confirmación, no verificación (es el mismo
principio de la evaluación a ciegas de Ronda 5).

## 3. Insumos exactos por documento

1. El PDF del documento (o el artefacto de texto determinístico si el harness no lee PDF con calidad — ver
   chequeo de la sección 4).
2. [INTERPELACION_v0.md](INTERPELACION_v0.md) — los 4 criterios y todas sus reglas de decisión.
3. [big_push.md](big_push.md) — definición operativa del criterio (i).
4. [TIPOLOGIA_v0.md](TIPOLOGIA_v0.md) — protocolo de 5 pasos y tabla de anclas.
5. Estas instrucciones (formato de salida de la sección 5).

Nada más. En particular, el revisor no necesita el codebook ni el esquema completo.

## 4. Chequeo de extracción (bloqueante, antes de revisar nada)

Igual que el Paso 3 del protocolo de portabilidad: comparar 2-3 pasajes del texto que el harness dice haber
leído contra el PDF, priorizando zonas de dos columnas o tablas. Si aparece texto intercalado o elementos
de maqueta mezclados con el cuerpo (en Ronda 5 esto contaminó campos de un caso), usar el `.txt` del
repositorio o un extracto determinístico en lugar de la lectura nativa del harness — o registrar el
problema y no revisar ese documento con ese harness.

## 5. Salida por documento

Un JSON reducido por documento en `fase2/pilot/revision/docNN_revision.json` con esta estructura exacta
(claves en español, citas siempre como objeto — mismas convenciones del pipeline):

```json
{
  "num_muestra": 15,
  "handle": "https://hdl.handle.net/11362/37310",
  "revisor": {
    "modelo": "deepseek-...",
    "harness": "opencode",
    "fecha": "YYYY-MM-DD"
  },
  "interpelacion": {
    "gran_impulso_ambiental_concreto": {
      "veredicto": "Sí | Parcial | No",
      "evidencia": "razonamiento contra los 3 tests de big_push.md, test por test",
      "citas": [{ "cita": "…", "pagina": 0 }]
    },
    "articulacion_actores": { "veredicto": "…", "evidencia": "…", "citas": [] },
    "oportunidades_productivas_sostenibles": { "veredicto": "…", "evidencia": "…", "citas": [] },
    "como_hacerlo_concreto": {
      "veredicto": "…",
      "evidencia": "…",
      "citas": [],
      "desglose_items": [{ "item": "…", "clasificacion": "CONCRETO | GENERICO", "pagina": 0 }],
      "tally": "M de N ítems pasan el test de concreción"
    }
  },
  "tipologia": {
    "transformacion_primaria": { "numero": 6, "nombre": "…", "certeza": "Alta | Media | Baja" },
    "transformacion_secundaria": { "numero": 11, "nombre": "…", "certeza": "…" },
    "justificacion_breve": "2-4 oraciones con conceptos literales del documento (regla anti-copia)"
  }
}
```

Reglas que el revisor debe respetar (son las mismas del ejecutor — están en los documentos de metodología,
se repiten acá las que la Ronda 5 mostró frágiles entre modelos):

- Veredictos en 3 valores, default a Parcial/No ante ambigüedad; sin cita textual no hay "Sí".
- Criterio (iv): el desglose se corre sobre el **texto completo de la sección de recomendaciones** (nunca
  recuadros de portada/key messages); decide el objeto, no el verbo; ante empate, GENERICO.
- Criterio (ii): un mecanismo de planificación multiactor con nombre propio, adoptado institucionalmente
  dentro del ámbito de aplicación, cuenta como mecanismo de articulación; mecanismos extrarregionales
  citados como referentes topean en "Parcial".
- Criterio (iii): el veredicto "No" exige chequeo negativo explícito (qué se buscó y no se encontró).
- Registrar siempre `revisor.modelo` y `revisor.harness` — en Ronda 5 el mapeo caso→modelo no quedó en los
  artefactos y hubo que reconstruirlo de memoria.

### Bloque de prompt sugerido (copiar/pegar en el harness externo)

> Actuá como codificador independiente de un ejercicio de calibración. Vas a leer un documento de la CEPAL
> (PDF adjunto) y tres documentos de metodología (INTERPELACION_v0.md, big_push.md, TIPOLOGIA_v0.md).
> Producí únicamente el JSON de veredictos con el formato de la sección 5 de
> INSTRUCCIONES_REVISOR_EXTERNO.md. Aplicá las reglas de decisión de la metodología al pie de la letra,
> con citas textuales y página para todo veredicto. No tenés acceso a ninguna respuesta previa sobre este
> documento y no debés intentar adivinarla: tu valor es la lectura independiente.

## 6. Qué pasa con el resultado (comparación y adjudicación)

1. **Comparación mecánica**: cruzar veredicto por veredicto (4 criterios + primaria/secundaria) contra el
   JSON del ejecutor. Registrar la **tasa de acuerdo** del lote — es la métrica que se reporta al equipo
   del curso y el insumo para decidir si el revisor se mantiene para los 244 (¿en todos o en submuestra?).
2. **Coincidencia** → veredicto confirmado, no se toca nada.
3. **Discrepancia** → adjudicación con la metodología a la vista (árbitro agente o revisión humana). Dos
   salidas posibles, con destinos distintos:
   - **Corrección puntual**: el ejecutor (o el revisor) aplicó mal una regla existente en ese documento →
     se corrige el JSON del ejecutor, citando la regla, y se deja constancia en la bitácora.
   - **Falla sistemática**: la discrepancia revela una regla ambigua o faltante (el patrón se repite en
     2+ documentos, o ambas lecturas son defendibles con la regla vigente) → **no** se corrige silenciosamente:
     se escribe la regla nueva o el ejemplo resuelto en el documento de metodología correspondiente, se
     registra como ronda en la bitácora, y recién entonces se corrigen los JSON afectados. Es el mismo ciclo
     que produjo las Rondas 2-5.
4. Los JSON de revisión se conservan en `pilot/revision/` como artefactos (no se borran tras adjudicar) —
   son la evidencia de la doble lectura.
