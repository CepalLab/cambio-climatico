# Revision independiente del informe maestro v2

**Fecha:** 2026-08-27
**Revisor:** revisor tematico independiente (desarrollo sostenible)
**Alcance:** `INFORME_MAESTRO_V2_BORRADOR.md` (7.220 palabras) y
`ANEXO_TECNICO_INFORME_V2.md`
**Verificacion tecnica:** citas nuevas de la v2 contra JSON canonicos y SQLite
(paginas, anos, literalidad); conteos de secciones 8 y 11; numeros de perdidas y
danos contra `salidas/verificacion_ejes_canonicos_v1.md`.

---

## A. Confirmacion de las dos observaciones del usuario

### A1. El binning de tres periodos no se justifica — CONFIRMADO

La v2 declara los periodos (introduccion) pero nunca explica por que tres ventanas
ni por que esos cortes. Falta en la seccion 2 (Corpus, metodo y limites), que ni
siquiera menciona la comparacion temporal. Proponer un parrafo explicito, por
ejemplo:

- **Origen:** el corpus empieza en 2015, el ano del Acuerdo de Paris, cuando se
  consolida la produccion CEPAL relevante.
- **Ventanas de ~4 anos:** permiten comparar bloques de tamano razonable y trazar
  una evolucion legible (2015-2018 diagnostico e impactos; 2019-2022 recuperacion
  transformadora; 2023-2026 financiamiento, ejecucion y transicion justa).
- **Limitaciones declaradas:** los cortes son de calendario, no derivados de un
  evento de contenido; los denominadores son desiguales (99/75/64); el tercer
  periodo esta abierto y tiene 6 publicaciones de 2026.
- **Coherencia con la tesis:** justamente porque son ventanas de comparacion y no
  etapas cerradas, la interpretacion de diferencias debe controlar composicion,
  tipos y divisiones (que la seccion 6 ya hace).

### A2. Frases redaccionales residuales — CONFIRMADO

Siguen presentes y deben eliminarse en la version final (las figuras 1-4 ya estan
embebidas; esas frases deben convertirse en prosa interpretativa en presente):

| Linea | Frasis actual | Accion |
| --- | --- | --- |
| 45 | "El Grafico 1 debe mostrar esta comparacion..." | Convertir en lectura en presente de la Figura 1. |
| 99 | "El Grafico 1 y el Grafico 2 deben trabajar juntos..." | Idem (y unificar Grafico/Figura). |
| 121 | "La Figura 4 debe leerse con esa cautela." | Convertir en lectura en presente. |
| 159 | "El Grafico 3 debe hacer visible ese contraste... El Cuadro 3 lo complementara..." | Convertir; y la descripcion del Cuadro 3 no coincide con el real (ver B3). |
| 193 | "La seccion incluira un cuadro de coherencia..." | Producir el cuadro o quitar la frase (el cuadro no existe). |

## B. Hallazgos nuevos de esta revision

### B1. El resumen ejecutivo NO recibio las directrices editoriales (prioridad alta)

- Linea 23 conserva la antigua agenda metodologica ("La primera es conservar
  trazabilidad entre argumentos, documentos, paginas, hashes y registros de
  SQLite... La cuarta es producir los cuadros y graficos previstos...") que
  **contradice** la agenda sustantiva ya reescrita en las conclusiones (linea
  203: "financiamiento asequible, inversion publica, coordinacion institucional,
  capacidades territoriales, datos, igualdad y derechos"). El resumen debe
  replicar la agenda sustantiva, no la metodologica.
- Lineas 9 y 23 conservan terminos internos que la directriz pedia retirar de la
  prosa: "citas canonicas", "hashes", "registros de SQLite".
- Linea 9: "clasificaciones candidatas calibradas" debe traducirse para el lector
  ("clasificaciones revisadas para este informe, que organizan la lectura y no
  son una codificacion definitiva").

### B2. Formato de cita inconsistente en prosa (prioridad media)

La directriz era citar con titulo, ano y pagina. La v2 mezcla:
- Con ano: "(2015, p. 55)", "(2026, p. 76)", "(2022, p. 39, traduccion propia)", "(2024, p. 209)".
- Sin ano: (*Mendoza y San Juan*, p. 16), (*bioeconomia*, p. 18), (*Metodologias... Guatemala*, p. 85), (*Como financiar el desarrollo sostenible*, p. 22), (*80561*, p. 35), (*Agenda 2030*, p. 137), (*Horizontes 2030*, p. 32), etc.

Uniformizar: (Titulo, ano, p. X) en todos los casos.

### B3. Descripcion de Cuadro 3 en prosa vs. cuadro real (prioridad media)

La linea 159 describe un Cuadro 3 de "oportunidades sectoriales, condiciones
habilitantes, riesgos distributivos y documentos ancla", pero el Cuadro 3 que ya
existe en `salidas/figuras_informe_v1/cuadros_01_02_cobertura.md` es "patrones,
periodos, documento ancla y limite". Alinear la prosa al cuadro existente (o
producir el cuadro descrito).

### B4. Cuadro de coherencia de la seccion 11 no existe (prioridad media)

"La seccion incluira un cuadro de coherencia" es un placeholder. El cuadro debe
producirse con las tres coberturas y sus denominadores (propuestas 92/99, 74/75,
63/64; avances 61.6/66.7/71.9; brechas 59.6/76.0/70.3) y la nota de composicion,
o la frase se elimina.

### B5. Anexo tecnico duplicado e incompleto (prioridad media)

- El bloque "Anexo tecnico" del informe (lineas 210-224) y el archivo
  `ANEXO_TECNICO_INFORME_V2.md` son **identicos** (13 lineas de apuntadores).
- Ninguno es un anexo real: solo deriva a bloques y salidas. Si la trazabilidad
  debe vivir en el anexo (directriz editorial), este debe contener: la matriz de
  lectura del Gran Impulso (rubrica completa), la definicion de la taxonomia
  candidata, la lista de 6 exclusiones, la justificacion del binning, la tabla de
  trazabilidad de las citas usadas (titulo, ano, pagina, handle, hash) y el
  resumen de verificacion de ejes (perdidas y danos, transicion justa, CBDR).
  Alternativa: declarar el anexo como apuntador explicito a los bloques. En
  cualquier caso, eliminar la duplicacion.

### B6. Error de edicion (prioridad baja, facil)

Linea 43: "En **2023-2026 (2023-2026, con seis publicaciones fechadas en 2026)**"
— "2023-2026" duplicado. Corregir a "En **2023-2026** (periodo abierto, con seis
publicaciones fechadas en 2026), ...".

### B7. Unificar Grafico/Figura (prioridad baja)

Mezcla "Grafico 1/2/3" (lineas 45, 99, 159) y "Figura 1-4". Usar "Figura" en
todo el documento.

### B8. Identificadores internos en el recuadro de contraejemplos (prioridad baja)

Linea 103 cita "(42230)" y "(41867)" como handles en prosa. Bajo la directriz
"los codigos internos solo permanecen en el anexo", eliminar los handles y dejar
titulo + ano.

### B9. Termino de codebook en seccion 6 (prioridad baja)

Linea 97: "la cobertura de la dimension `tendencias` es desigual" — traducir a
"la cobertura de las menciones a tendencias es desigual".

## C. Verificacion tecnica de las citas nuevas de la v2 (OK)

| Cita (v2) | Doc | Pagina | Ano | Resultado |
| --- | --- | --- | --- | --- |
| SICA cinco ejes prioritarios | 37310 | 55 | 2015 | OK (dimension auditada) |
| Cuenca Sixaola | 89774 | 76 | 2026 | OK (dimension auditada) |
| Ocho tesis (matriz de bienes) | 39840 | 27 | 2015 | OK (dimension auditada) |
| Accion climatica agricultura (teledeteccion) | 48724 | 79 | 2023 | OK (dimension auditada) |
| Gestion Publica (conexion presupuesto) | 69075 | 88 | 2024 | OK (dimension auditada) |
| Belmopan ("formar y dotar de recursos...") | 48097 | 39 | 2022 | OK; original en ingles "Train and equip city officials..." verificado; traduccion propia correcta |
| Trampas (30/10/1%) | 80727 | 209 | 2024 | OK (dimension auditada: "apenas se aprovecha el 30% del potencial hidroelectrico, el 10% del eolico y el 1% del solar") |
| Construir un nuevo futuro ("cambio de epoca") | 46227 | 20 | — | OK |

- **Perdidas y danos (seccion 5):** los numeros 27 docs / 13 evaluacion de danos /
  12 politica-financiamiento / 31 requiere revision coinciden con
  `salidas/verificacion_ejes_canonicos_v1.md`. La redaccion es ejemplar: no
  agrega sentidos, distingue marcos y no infiere disponibilidad de recursos.
- **Seccion 8 (tipologia):** 60/45/27 y 19/15/25 coinciden con SQLite.
- **Seccion 11 (coherencia):** 92/99, 74/75, 63/64; avances 61.6/66.7/71.9;
  brechas 59.6/76.0/70.3 coinciden con los paquetes de evidencia.

## D. Lo que quedo bien (no tocar)

- Seccion 5 (perdidas y danos): precision conceptual correcta.
- Seccion 7 (escalas SICA -> cuenca -> ciudad): organizacion narrativa solida y
  anclada; usa la etiqueta `multinivel` solo para la coordinacion entre niveles,
  no como eje cuantitativo.
- Seccion 9: la matriz de lectura del Gran Impulso se explica antes del panel;
  no mide ejecucion.
- Seccion 11: coherencia condicionada con denominadores y cautela de composicion.
- Figuras embebidas con notas metodologicas visibles.
- Extension: 7.220 palabras, dentro del objetivo de ~20 paginas.

## E. Checklist de cierre para la version final

1. Justificar el binning de tres periodos en la seccion 2 (A1).
2. Eliminar todas las frases redaccionales en futuro/imperativo (A2).
3. Reescribir la agenda del resumen ejecutivo en terminos de politica (B1).
4. Uniformar citas en prosa: titulo, ano y pagina (B2).
5. Alinear prosa y contenido del Cuadro 3 (B3).
6. Producir o eliminar el cuadro de coherencia de la seccion 11 (B4).
7. Resolver la duplicacion del anexo tecnico y definir su alcance (B5).
8. Corregir la duplicacion de "2023-2026" (B6), unificar Figura/Grafico (B7),
   quitar handles del recuadro (B8) y traducir "dimension tendencias" (B9).

## F. Fuentes

- JSON canonicos: `fase2/corpus/resultados/json/` y `fase2/pilot/`.
- SQLite: `fase3/02_eda/salidas/fase3_analitica_v1.sqlite` (tablas `documents`,
  `dimensions`, `typology`).
- Verificacion de ejes: `salidas/verificacion_ejes_canonicos_v1.md`.
- Cuadros: `salidas/figuras_informe_v1/cuadros_01_02_cobertura.md`.
