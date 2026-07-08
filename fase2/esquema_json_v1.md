# Esquema JSON canónico v1 — salida por documento del pipeline de Fase 2b

**Fecha**: 2026-07-07 (Ronda 3)
**Estado**: v1, creado a raíz del feedback de la Ronda 3 sobre los 3 JSON piloto: los tres artefactos usaban estructuras distintas entre sí (claves en inglés y español mezcladas, citas como string plano en un documento y como objeto en otro, dos formatos diferentes de tipología). Para análisis agregado sobre 244 documentos esa consistencia no es cosmética — es la condición para poder computar cualquier cosa.
**Regla general**: todo JSON producido por el pipeline (piloto, muestra de 14, corpus de 244) valida contra este esquema. Si un caso real no cabe en el esquema, se discute y se versiona el esquema — no se improvisa una variante en el artefacto.
**Validador automático**: [pipeline/validar_esquema.py](pipeline/validar_esquema.py) (solo stdlib) chequea
la conformidad estructural — claves, slugs, formato de citas, veredictos, tipología — y hace un chequeo heurístico de referencias cruzadas. `python fase2/pipeline/validar_esquema.py [rutas...]` (sin argumentos valida los 3 piloto).

## 0. Reglas transversales

1. **Claves siempre en español** y en `snake_case`. El campo de veredicto se llama `veredicto` (nunca `verdict`).
2. **Toda cita textual es un objeto** `{"cita": "...", "pagina": N}` — nunca un string plano con la página embebida. `pagina` es entero cuando la cita cae en una página, string `"N-M"` cuando abarca un rango. La numeración es la **interna del documento** (la impresa en el pie/encabezado), no la del archivo PDF.
3. **Autocontención**: el JSON de un documento no menciona ningún otro documento del corpus — ni en `resumen_narrativo`, ni en `conclusiones_recomendaciones`, ni en las notas de interpelación. Cada documento se evalúa solo contra la metodología ([INTERPELACION_v0.md](INTERPELACION_v0.md), [TIPOLOGIA_v0.md](TIPOLOGIA_v0.md), [codebook_v0.md](codebook_v0.md)). **Única excepción**: `tipologia.validacion_anclas` puede referirse a la tabla de anclas de
   [TIPOLOGIA_v0.md §3](TIPOLOGIA_v0.md) — que es parte de la metodología — sin narrar comparaciones con otros JSON. Las observaciones comparativas entre casos van a la bitácora de [PLAN_ANALISIS_PROFUNDO.md](PLAN_ANALISIS_PROFUNDO.md), no al artefacto por documento.
   *Razón*: a escala de 244 las referencias cruzadas dependen del orden de procesamiento (no son reproducibles) y contaminan cualquier agregado.
4. **`handle` viene de [muestra_calibracion.csv](muestra_calibracion.csv)** (o del corpus definitivo a
   escala) — es la PK del corpus y ya está resuelto ahí. Nunca `"pendiente de confirmar"`.
5. **Dimensiones del codebook**: solo los 9 slugs canónicos (tabla §2). Nada de variantes (`propuestas` ≠ `propuestas_politica`; `contexto/antecedentes` ≠ `contexto_antecedentes`).

## 1. Esqueleto completo

```json
{
  "documento": {
    "num_muestra": 9,
    "titulo": "…",
    "autoria": "… | null",
    "handle": "https://hdl.handle.net/11362/NNNNN",
    "simbolo": "LC/… | null",
    "isbn": "… | null",
    "fecha": "YYYY-MM-DD | YYYY-MM",
    "tipo_documento": "…",
    "paginas_cuerpo": 12,
    "paginas_totales": 12,
    "idioma": "es | en",
    "tiene_resumen_ejecutivo": true
  },
  "resumen_enriquecido": {
    "pregunta_investigacion": "…",
    "alcance": {
      "ambito_aplicacion": "…",
      "referentes_dependencias": "… | null",
      "sectorial": "…",
      "temporal": "…"
    },
    "hallazgos_principales": ["… (p.N)"],
    "conclusiones_recomendaciones": ["…"],
    "resumen_narrativo": "…"
  },
  "resumen_secciones": [
    {
      "seccion": "título tal como aparece en el índice",
      "nivel": 1,
      "paginas": "1-2",
      "resumen": "… | null solo si se delega íntegramente en subsecciones",
      "dimensiones": [
        {
          "dimension": "estado_de_situacion",
          "cita": "…",
          "pagina": 2,
          "subtipo_brecha": "retrospectiva | prospectiva  (solo si dimension = brechas_implementacion)"
        }
      ],
      "subsecciones": []
    }
  ],
  "interpelacion": {
    "gran_impulso_ambiental_concreto": {
      "veredicto": "Sí | Parcial | No",
      "evidencia": "razonamiento; si el veredicto es No, chequeo negativo explícito (§1.3 de INTERPELACION_v0.md)",
      "citas": [{ "cita": "…", "pagina": 10 }],
      "nota": "… | null"
    },
    "articulacion_actores": { "veredicto": "…", "evidencia": "…", "citas": [], "nota": null },
    "oportunidades_productivas_sostenibles": { "veredicto": "…", "evidencia": "…", "citas": [], "nota": null },
    "como_hacerlo_concreto": {
      "veredicto": "…",
      "evidencia": "…",
      "citas": [],
      "desglose_items": [
        { "item": "…", "clasificacion": "CONCRETO | GENERICO", "pagina": 75 }
      ],
      "tally": "M de N ítems pasan el test de concreción",
      "nota": null
    }
  },
  "tipologia": {
    "transformacion_primaria": { "numero": 6, "nombre": "Sostenibilidad ambiental", "certeza": "Alta | Media | Baja" },
    "transformacion_secundaria": { "numero": 11, "nombre": "Capacidades del Estado", "certeza": "…" },
    "razonamiento_5_pasos": {
      "tension_dialectica": "…",
      "filtro_categoria_primaria": "…",
      "secundaria_obligatoria": "…",
      "justificacion_anti_copia": "…",
      "validacion_anclas": "…"
    },
    "tipo_documento_climatico": "…",
    "nivel_aplicacion": "…",
    "ambiguedad_pendiente_validacion": "… | null"
  }
}
```

## 2. Reglas por bloque

### `documento`

| Campo                     | Regla                                                                                                                                                                                  |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `handle`                  | Copiado de `muestra_calibracion.csv` (columna final). Fuente de verdad del corpus, no se re-deriva del PDF.                                                                            |
| `paginas_cuerpo`          | Entero: **hasta el final de conclusiones/recomendaciones** según la numeración interna (Resumen/Introducción → Conclusiones), excluyendo bibliografía y anexos (Ronda 4, decisión que separa este campo de `paginas_totales`). Es la medida comparable de "cuánto argumento sustantivo" tiene el documento, sin que anexos técnicos infrecuentes distorsionen el agregado. |
| `paginas_totales`         | Entero: numeración interna completa del documento (incluye bibliografía y anexos, sin contar tapas/colofón). Dato calculado/imputado, no extraído de un metadato único — se mantiene junto a `paginas_cuerpo` en vez de elegir uno solo, porque ambos son útiles y no son intercambiables (Ronda 4). |
| `autoria`                 | `null` si el documento es institucional sin autoría personal.                                                                                                                          |
| `tiene_resumen_ejecutivo` | Ver regla de `resumen_secciones` abajo.                                                                                                                                                |

### `resumen_enriquecido`

- `alcance` separa `ambito_aplicacion` (sobre qué región/países el documento analiza o propone) de
  `referentes_dependencias` (bloques/países citados como comparación u origen de un instrumento
  externo) — variables del [codebook §2](codebook_v0.md), decisión de Ronda 1 punto 7.
- `resumen_narrativo`: 3-5 oraciones, guardrail anti-genérico de
  [INTERPELACION_v0.md §3](INTERPELACION_v0.md). Sin referencias a otros documentos del corpus (regla
  transversal 3).

### `resumen_secciones` — estructura anidada por niveles (Ronda 3)

1. **Se capturan siempre todas las secciones de nivel 1 del índice**, en orden, sin excepciones. Nunca se salta del nivel 1 al nivel 3 sin registrar el padre intermedio.
2. **Se desciende a subsecciones solo cuando la sección de nivel 1 supera ~8-10 páginas**, y las subsecciones van **anidadas dentro de su padre** (campo `subsecciones`, mismo shape, `nivel` 2 o 3) — no aplanadas como filas hermanas del nivel 1. El padre conserva su fila con `paginas` del rango completo; su `resumen` puede ser una síntesis breve de 1-2 líneas del arco de la sección o `null` si
   las subsecciones lo cubren todo.
3. **El resumen ejecutivo / resumen / abstract del propio documento NO se procesa como sección.** Su contenido ya alimenta `resumen_enriquecido`; procesarlo como sección duplica el conteo de dimensiones en el agregado (repite lo que las demás secciones ya dicen). Se deja constancia con `documento.tiene_resumen_ejecutivo: true`.
4. **Calidad del resumen** (endurece la regla proporcional de Ronda 2): además del largo proporcional (~1 línea por página, piso 3-4 líneas), cada resumen debe incluir (a) el argumento o función de la sección dentro del documento — qué trabajo hace, no solo qué temas toca; (b) las cifras o datos clave si los hay; (c) los instrumentos, actores o casos nombrados si los hay. Un resumen que solo enuncia
   temas ("aborda la vulnerabilidad y las políticas del sector") no cumple, aunque tenga el largo correcto.
5. `dimensiones` es una **lista de objetos** (no un dict), cada uno con su cita+página propia — una dimensión no hereda la cita de otra (regla de Ronda 2).
6. **Dimensiones solo en las hojas (Ronda 4)**: cuando una sección de nivel 1 se descompone en `subsecciones`, el padre lleva `"dimensiones": []` — las etiquetas viven únicamente en las subsecciones. Excepción: si el padre tiene contenido propio antes de su primera subsección (una frase de encuadre del capítulo que ninguna subsección cubre), ese fragmento sí lleva su propia dimensión con cita+página específica. Razón: la misma lógica anti-doble-conteo de la regla 3 (resumen ejecutivo) — una cita no puede sostener una dimensión en dos filas distintas del mismo agregado.
7. **Anexos: no se procesan como sección (Ronda 4)**: los anexos técnicos (metodología detallada, pruebas de robustez, fuentes de datos) no se incluyen en `resumen_secciones`. Se registra su existencia como metadato (`documento.tiene_anexos: true | false`, campo nuevo) pero no se etiquetan dimensiones sobre su contenido. **Excepción histórica**: `pilot/doc11_pobreza_infantil.json` procesó su sección 5 (Anexos) completa porque se generó antes de esta decisión (Ronda 4, 2026-07-08) — se conserva así en el piloto, no se retroactúa; los documentos siguientes (12 restantes de la muestra, luego 244) siguen esta regla nueva.

### `interpelacion`

- Las 4 claves fijas del ejemplo, siempre las 4, siempre con `veredicto`/`evidencia`/`citas`/`nota`.
- `desglose_items` + `tally` son obligatorios en `como_hacerlo_concreto` cuando el documento tiene lista de recomendaciones; opcionales (mismo formato) en `oportunidades_productivas_sostenibles` si hay enumeración desglosable.
- Los criterios y reglas de decisión viven en [INTERPELACION_v0.md](INTERPELACION_v0.md) (v0.2+): en
  particular la definición operativa del gran impulso ambiental anclada a [big_push.md](big_push.md) y el requisito de que el mecanismo de articulación pertenezca al ámbito de aplicación del documento.

### `tipologia`

- Formato único: primaria/secundaria como objetos `{numero, nombre, certeza}` +
  `razonamiento_5_pasos` completo (protocolo de [TIPOLOGIA_v0.md §2](TIPOLOGIA_v0.md)). El caso ambiguo no cambia el formato: se asigna la mejor hipótesis con `certeza: "Baja"` y se explica en `ambiguedad_pendiente_validacion`.
- **No lleva `tipo_brecha`**: eso se replegó al codebook como `subtipo_brecha` de la dimensión `brechas_implementacion` (Ronda 1, punto 6).

## 3. Slugs canónicos de dimensiones (codebook v0.1)

`contexto_antecedentes` · `estado_de_situacion` · `diagnostico_estructural` · `tendencias` · `desafios` · `oportunidades` · `propuestas_politica` · `avances_implementacion` · `brechas_implementacion`
