# Prompt de sesión — revisor ciego (un documento por sesión)

**Archivo canónico**: copiar el contenido desde la sección [Prompt de sesión](#prompt-de-sesión) como primer mensaje de una conversación nueva.
**Diseño**: agnóstico de modelo y de harness (Cursor, OpenCode, Claude Code, u otro). Registrar en el JSON de salida el `modelo` y el `harness` realmente usados.
**Operativa**: **una sesión = un documento**. Evita agotar la ventana de contexto y reduce contaminación entre casos. La comparación entre ejecutor y revisor (`comparar_revision.py`) y la adjudicación son **otras sesiones**, cuando haya un conjunto de `pilot/revision/docNN_revision.json`.
**Metodología de referencia**: [INSTRUCCIONES_REVISOR_EXTERNO.md](INSTRUCCIONES_REVISOR_EXTERNO.md).

---

## Cómo usarlo (operador humano)

1. Abrir una conversación **nueva** en el harness elegido (sin historial del ejecutor ni de otras revisiones).
2. Completar el bloque **DOCUMENTO ACTIVO** al final del prompt (num, rutas de PDF/txt, handle).
3. Pegar **todo** el texto de [Prompt de sesión](#prompt-de-sesión) como primer mensaje.
4. Cuando exista `fase2/pilot/revision/docNN_revision.json` y el chequeo de extracción haya pasado, **cerrar la sesión**.
5. Repetir con otro documento en una sesión nueva.

Orden sugerido de la muestra de 17 (opcional):  
`9 → 13 → 11 → 2 → 3 → 15 → 18 → 1 → 6 → 8 → 12 → 14 → 16 → 10 → 4 → 17 → 19`

---

## Prompt de sesión

```
# Revisor ciego — Fase 2 (análisis de publicaciones CEPAL sobre cambio climático)

## Rol
Actúe como codificador independiente en un ejercicio de calibración. Su trabajo es una **segunda lectura ciega** limitada a:
- interpelación institucional (4 criterios), y
- tipología de transformaciones (primaria / secundaria).

No es el ejecutor del pipeline: no rehaga resúmenes enriquecidos, no construya `resumen_secciones`, no etiquete dimensiones del codebook.

Este prompt es **agnóstico de modelo y de harness**. Al final, registre en el JSON los campos `revisor.modelo` y `revisor.harness` con los valores reales de esta sesión (por ejemplo: modelo `grok-…`, harness `cursor`; u otros).

## Alcance de esta sesión
- Procesar **un solo documento**: el indicado en DOCUMENTO ACTIVO al final.
- Al terminar (JSON de revisión escrito en disco), deténgase. No pida el siguiente documento ni continúe con otro.
- No compare con la salida del ejecutor. No adjudique discrepancias. Eso corresponde a sesiones posteriores.

## Contexto mínimo (no explorar de más)
- Carpeta de trabajo del proyecto: `fase2/` dentro del repositorio de cambio climático.
- El ejecutor ya generó JSON canónicos en `fase2/pilot/docNN_*.json` para la muestra de calibración (17 documentos). Esos archivos existen, pero **están prohibidos** para usted (regla de ceguera).
- Instrucciones completas del rol: `fase2/INSTRUCCIONES_REVISOR_EXTERNO.md`.

## Regla de ceguera (bloqueante)
No abra, no cite y no use en ningún momento:
1. `fase2/pilot/docNN_*.json` (salida del ejecutor), incluidas variantes multimodelo (`doc09_caribbean_power_0[1-5].json`);
2. `fase2/para_equipo_curso/` (versiones legibles de veredictos ya resueltos);
3. cualquier veredicto o tipología previos sobre el documento activo.

Si en esta conversación ya se expuso alguno de esos artefactos, detenga el trabajo y declare la revisión contaminada. El valor del ejercicio es la lectura independiente, no la confirmación de una respuesta previa.

## Insumos permitidos (solo estos)
1. El PDF del documento activo (y, si hace falta, el `.txt` o chunks determinísticos bajo `fase2/pilot/pdfs/`).
2. `fase2/INTERPELACION_v0.md`
3. `fase2/big_push.md`
4. `fase2/TIPOLOGIA_v0.md`
5. `fase2/INSTRUCCIONES_REVISOR_EXTERNO.md` (formato de salida, sección 5)
6. La fila correspondiente en `fase2/muestra_calibracion.csv` (solo para `num`, título y `handle`)

No necesita el codebook ni el esquema JSON completo del ejecutor.

## Procedimiento (en este orden)
1. **Identificar** el documento activo (bloque al final) y localizar PDF / texto.
2. **Chequeo de extracción** (bloqueante, antes de codificar): comparar 2–3 pasajes del texto que el harness dice haber leído contra el PDF, priorizando zonas de dos columnas o tablas. Si hay texto intercalado o maqueta mezclada con el cuerpo, usar el `.txt` determinístico del repositorio (o chunks) en lugar de la lectura nativa del harness. Si tampoco es fiable, registrar el problema en un archivo corto `fase2/pilot/revision/docNN_REVISION_BLOQUEADA.md` y no producir veredictos.
3. **Aplicar** las reglas de `INTERPELACION_v0.md` (con `big_push.md` para el criterio i) y el protocolo de 5 pasos de `TIPOLOGIA_v0.md`.
4. **Escribir** exactamente un archivo:
   `fase2/pilot/revision/docNN_revision.json`
   (crear el directorio `fase2/pilot/revision/` si no existe; `NN` = número de muestra con dos dígitos, p. ej. `09`).
5. **Confirmar** en la respuesta: ruta del archivo, los 4 veredictos, primaria/secundaria con certeza, y si el chequeo de extracción usó PDF nativo o `.txt`/chunks. No es necesario pegar el JSON completo en el chat si ya está en disco.
6. **Terminar** la sesión.

## Formato de salida (obligatorio)
Estructura exacta de `INSTRUCCIONES_REVISOR_EXTERNO.md` §5:

{
  "num_muestra": <int>,
  "handle": "https://hdl.handle.net/11362/…",
  "revisor": {
    "modelo": "<id real del modelo en esta sesión>",
    "harness": "<cursor | opencode | claude-code | otro>",
    "fecha": "YYYY-MM-DD"
  },
  "interpelacion": {
    "gran_impulso_ambiental_concreto": {
      "veredicto": "Sí | Parcial | No",
      "evidencia": "…",
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
    "transformacion_primaria": { "numero": 0, "nombre": "…", "certeza": "Alta | Media | Baja" },
    "transformacion_secundaria": { "numero": 0, "nombre": "…", "certeza": "…" },
    "justificacion_breve": "2–4 oraciones con conceptos literales del documento (regla anti-copia)"
  }
}

Convenciones: claves en español; cada cita es objeto `{cita, pagina}`; `pagina` usa la numeración **interna** del documento (impresa), no la del archivo PDF.

## Reglas que no deben relajarse
- Veredictos en tres valores. Ante ambigüedad, preferir Parcial o No. Sin cita textual no hay "Sí".
- Criterio (iv) `como_hacerlo_concreto`: el desglose se corre sobre el **texto completo** de la sección de recomendaciones/conclusiones; nunca sobre recuadros de portada ni "key messages". Decide el objeto, no el verbo. Ante empate → GENERICO. **Ejemplos geográficos/ecosistémicos van como alcance dentro del ítem, no como filas separadas del tally** (ancla negativa: doc06 Cap. XII).
- Criterio (ii) `articulacion_actores`: mecanismo de planificación multiactor con nombre propio, adoptado institucionalmente dentro del ámbito de aplicación. Mecanismos extrarregionales citados como referentes topean en "Parcial".
- Criterio (iii): el veredicto "No" exige chequeo negativo explícito (qué se buscó y no se encontró).
- Tipología: protocolo de 5 pasos; justificación con conceptos del documento (anti-copia de las definiciones del documento metodológico).

## Prohibiciones
- Editar `fase2/pilot/docNN_*.json` del ejecutor.
- Ejecutar `comparar_revision.py` o abrir reportes de comparación en esta sesión.
- Mencionar otros documentos del corpus como evidencia comparativa.
- Inventar dimensiones de codebook o resúmenes por sección.

## DOCUMENTO ACTIVO
(Completar antes de pegar este prompt. Un solo documento.)

- num_muestra: <N>
- título (opcional, desde muestra_calibracion.csv): <…>
- handle: https://hdl.handle.net/11362/<…>
- PDF: fase2/pilot/pdfs/<archivo>.pdf
- texto alternativo (si existe): fase2/pilot/pdfs/<archivo>.txt  |  chunks: <ruta o "ninguno">
- archivo de salida esperado: fase2/pilot/revision/doc<NN>_revision.json
- revisor.modelo (si se conoce de antemano; si no, inferirlo al cerrar): <…>
- revisor.harness: <cursor | opencode | claude-code | otro>

Inicie por el chequeo de extracción del documento indicado. No procese ningún otro.
```

---

## Después de varias sesiones de revisión

Cuando existan varios `fase2/pilot/revision/docNN_revision.json`:

```bash
python fase2/pipeline/comparar_revision.py
```

Eso genera `fase2/pilot/revision/REPORTE_COMPARACION.md`. La **adjudicación** se pide en una sesión aparte del harness principal (ver circuito en [GUIA_OPERATIVA_PIPELINE.md](GUIA_OPERATIVA_PIPELINE.md) e [INSTRUCCIONES_REVISOR_EXTERNO.md](INSTRUCCIONES_REVISOR_EXTERNO.md) §6).
