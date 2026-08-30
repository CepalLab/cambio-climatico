# Aportes del revisor tematico al plan de expansion v2 del informe maestro

**Fecha:** 2026-08-27 (actualizado con aclaraciones del usuario: 30 paginas es
referencial, objetivo real ~20 paginas; el capítulo de territorio se organiza por
"escalas de analisis", no por la etiqueta multinivel)
**Autor:** revisor tematico independiente (desarrollo sostenible)
**Referencia:** intercambio usuario-agente sobre
`INFORME_MAESTRO_30P_BORRADOR_v1.md` (3.697 palabras, ~9 paginas; 43 dos puntos;
24 menciones de terminos internos sqlite/hash/json/canonica)
**Uso:** insumos para el plan de expansion v2 antes de reescribir el informe maestro.

---

## 0. Veredicto del intercambio

Coincido con el diagnostico del usuario y con el rumbo que propone el agente
(expansion analitica real hacia un cuerpo de ~7.000-7.500 palabras (objetivo
referencial de 30 paginas; el usuario lo ajusto a ~20 paginas de prosa, con
cuadros, graficos y anexos que pueden sumar algunas paginas mas y la regla de no
generar texto poco util), capitulos nuevos de territorio/escalas y
tipologia/tensiones, reorganizacion de P1-P9, agenda en terminos de politica,
retiro de terminos internos, citas por titulo/ano/pagina, perdidas y danos como
hallazgo acotado, y la "matriz de lectura del Gran Impulso Ambiental"). Este
documento agrega: una correccion factual, tres datos verificados que sustentan
los capitulos nuevos, la localizacion de la fuente de la tension dialectica, un
guardrail anti-inflado para la expansion, y el presupuesto de palabras por
capitulo ajustado a ~20 paginas.

## 1. Correccion factual obligatoria antes de expandir

El informe repite en resumen, arquitectura, especificacion y bloques: "P3
(2023-2026; el corpus disponible llega hasta 2025)". **Eso es inexacto: hay 6
documentos fechados en 2026 en la base SQLite** (85930, 86527, 89774, 89932,
89934, 90001), incluido un documento de transicion justa (90001) y la economia
del cambio climatico 2025 (86527). Correccion sugerida en todos los puntos: "P3
(2023-2026; con 6 publicaciones fechadas en 2026)". Afecta el Cuadro 1 y la nota
temporal de P3.

## 2. Fuente de la tension dialectica: el canon, no SQLite

La tabla `typology` de SQLite NO contiene `tension_dialectica` (solo
primary/secondary y application_level_original). La tension dialectica vive en el
campo `tipologia.tension_dialectica` de los JSON canonicos de Fase 2. El capitulo
nuevo de tipologia/tensiones debe construirse leyendo ese campo del canon (o
exportarlo como derivado), no consultando SQLite. Es la unica capa de tipologia
que no esta aplanada en la base.

## 3. Datos verificados para los dos capitulos nuevos

### 3.1 Territorio, escalas de analisis y capacidades de implementacion

- **Organizar el capitulo por "escalas de analisis", no por la etiqueta
  `multinivel`.** El espiritu (segun el usuario) es que el corpus trabaja en
  multiples escalas: regional y subregional como partes del continente; nacional;
  federal; subnacional y de territorios; y hasta ciudades. La etiqueta
  `multinivel` (articulacion explicita entre escalas) es un subconjunto pequeno y
  debil (14 docs candidatos; cae a 1 en P3: P1=5, P2=8, P3=1) y no debe ser la
  columna del capitulo.
- **Escalas como eje narrativo** con datos candidatos verificados por periodo:
  regional 53/45/41; subregional 57/55/45; subnacional 19/21/11; nacional 7/3/4;
  multinivel 5/8/1. Anclas sugeridas: regional (Adaptacion al CC en ALC),
  subregional (SICA, Caribe, Eta e Iota), nacional (impuesto al carbono,
  Guatemala, Brasil), subnacional/federal (rios de Mendoza y San Juan), ciudad
  (Belmopan, vivienda en el Caribe).
- **Cautela:** los ambitos son multi-etiqueta candidatos (los conteos no suman
  238) y el desplome de subnacional/multinivel en P3 puede ser
  composicion/codificacion; no narrarlo como tendencia.
- **Capacidades estatales como complemento verificable:** Capacidades del Estado
  como transformacion primaria P1=19, P2=15, P3=25 (senal ascendente en P3) y la
  escala subnacional como condicion de implementacion (Belmopan, municipios SICA,
  gobiernos subnacionales).

### 3.2 Tipologia de transformaciones y tensiones dialecticas

- **Distribucion verificada por periodo (SQLite):** Sostenibilidad ambiental
  60/45/27; Capacidades del Estado 19/15/25; Macroeconomia y fiscalidad 9/4/7;
  Igualdad de genero 1/6/1; Reduccion de la desigualdad 6/0/1; Integracion
  economica 1/3/2; Desarrollo productivo 3/2/1.
- **Tensiones sugeridas por periodo** (a verificar contra el campo canonico):
  - P1: ambiente y desarrollo; consagracion normativa (derechos de acceso) vs
    implementacion efectiva; inversion ambiental vs restriccion fiscal.
  - P2: derechos formales vs ejecucion; recuperacion pospandemia (inversion
    necesaria) vs espacio fiscal; desarrollo vs sostenibilidad en la salida de
    crisis.
  - P3: transicion justa vs costos distributivos; ambicion climatica vs
    capacidad estatal; inversion resiliente vs restriccion de deuda.
- **Regla de redaccion:** las tensiones se presentan como "tensiones que el
  corpus procesa", nunca como desenlace resuelto ni como clasificacion
  automatica concluyente (misma regla que la taxonomia candidata).

### 3.3 Coherencia propuesta vs avances (nueva seccion de convergencias)

- **Datos verificados (paquetes de evidencia):** cobertura de `propuestas_politica`
  casi universal en los tres periodos (92/99, 74/75, 63/64); `avances_implementacion`
  61.6% -> 66.7% -> 71.9%; `brechas_implementacion` 59.6% -> 76.0% -> 70.3%.
- **Lectura defendible:** propuestas casi universales + atencion creciente a
  avances y brechas + reclamos sobre la brecha de ejecucion = la tesis central
  del corpus ("respuestas aisladas no bastan"; "la brecha esta en la
  implementacion").
- **Cautela obligatoria:** las proporciones cambian con denominadores de distinto
  tamano y la presencia de codificacion no mide intensidad ni resultado. No usar
  conteos de citas como proxy unico.

## 4. Cinco convergencias transversales (proponer como apartado)

La expansion deberia convertir los cinco hallazgos del resumen en convergencias
desarrolladas, cada una con 2-3 documentos ancla y un contraejemplo:

1. Respuestas aisladas no bastan (pauta mas recurrente del corpus).
2. Financiamiento y capacidades como condiciones habilitantes.
3. Datos, medicion y MRV como precondicion de gestion.
4. Participacion, derechos y acceso como condicion de legitimidad y continuidad.
5. Territorialidad de la vulnerabilidad (la escala es parte del problema).

## 5. Perdidas y danos y CBDR: posicion acordada y ubicacion

- **Perdidas y danos como hallazgo acotado** (acuerdo): evidencia verificada en
  la auditoria de bloques 02/03 (26 documentos; 9 con marco de politica/fondo;
  14 de P3). Ubicacion sugerida: un parrafo en el capitulo de implementacion/
  financiamiento (proteccion financiera, acceso a fondos, SIDS) + una nota en la
  agenda. No entra al resumen como pilar ni como conclusion sustantiva.
- **CBDR como nota cualitativa** (7 documentos, concentrados en P1/P2): solo como
  observacion interpretativa de que el marco de negociacion de los primeros anos
  cedio a un foco de implementacion. Sin cifras, sin afirmacion de "desaparicion".

## 6. Figuras: que trabajen dentro del argumento

Las figuras estan enlazadas al final, no integradas. En la expansion cada figura
debe tener un parrafo interpretativo en prosa (patron visible, lectura, cautela)
y una nota metodologica visible. Especificas:

- **Figura 3 (panel Big Push):** debe explicar la ventana pospandemia (P2 sube)
  y el giro tecnico-financiero (P3 baja en estrategia integral). La "matriz de
  lectura del Gran Impulso Ambiental" se describe en prosa con las cuatro
  etiquetas narrativas; la rubrica completa va al anexo tecnico.
- **Figura 4 (escalas y tipologia):** mostrar solapamientos multi-etiqueta entre
  escalas (regional, subregional, nacional, subnacional, ciudad) y tipologia; no
  sumar a 238.
- **Figura 1:** nota "clasificacion candidata calibrada" siempre visible.
- **Figura 2:** separar taxonomia candidata, campos canonicos e interpelacion.

## 7. Guardrail anti-inflado de la expansion

Ir de 3.700 a ~7.000-7.500 palabras sin evidencia nueva seria inflar. El
objetivo no es llenar 30 paginas, sino expandir donde el corpus lo sustente:
la regla del usuario es "no generar texto poco util de mas". Reglas:

1. Cada parrafo nuevo se ancla en al menos una ficha/hallazgo, un documento
   ancla o un dato verificado (nunca solo en una afirmacion general).
2. Producir un **mapa de expansion** previo: capitulo -> preguntas que responde ->
   evidencia (capa directa/candidata/dato) -> figura o cuadro asociado -> riesgo
   de sobreafirmacion. Ese mapa es la columna vertebral del plan v2.
3. Compuerta v2: agregar filas de revision humana + auditoria independiente para
   los dos capitulos nuevos (territorio/escalas y tipologia/tensiones) y para la
   seccion de coherencia propuesta/avances, con los mismos criterios de salida
   que las filas existentes.

## 8. Presupuesto de palabras ajustado a ~20 paginas de prosa

Objetivo referencial del usuario: ~20 paginas de prosa (las 30 paginas de la
arquitectura son referenciales; cuadros, graficos y anexos pueden sumar paginas
mas). A ~350-400 palabras por pagina, ~20 paginas equivalen a ~7.000-7.500
palabras de cuerpo.

| Capitulo | Paginas | Palabras |
| --- | ---: | ---: |
| Resumen ejecutivo | 1.5 | 500 |
| 1. Introduccion | 1 | 350 |
| 2. Corpus, metodo y limites | 1 | 400 |
| 3. Evolucion del objeto (P1-P3, Fig 1-2) | 2.5 | 800 |
| 4. Impactos, diagnostico, herramientas (P1-P4; incl. agua) | 2 | 750 |
| 5. Implementacion, brechas, desafios (P5-P7; propuesta/avances) | 2 | 750 |
| 6. Enfasis, persistencias y ventanas (P6-P7; recuadro contraejemplos) | 1.5 | 550 |
| 7. Territorio, escalas de analisis y capacidades (Fig 4) | 2 | 700 |
| 8. Tipologia de transformaciones y tensiones dialecticas | 1.5 | 600 |
| 9. Gran Impulso Ambiental (P8; Fig 3, Cuadro 3) | 1.5 | 650 |
| 10. Participacion, derechos y distribucion (P9) | 1.5 | 500 |
| 11. Convergencias transversales | 1 | 400 |
| 12. Conclusiones y agenda | 1.5 | 550 |
| **Total** | **20.5** | **7.500** |

Nota: la extension es flexible dentro de 6.800-7.800 palabras. Si una seccion
termina con 600 palabras en lugar de 750 porque el corpus no da mas, eso es
correcto. El presupuesto se usa para decidir que se expande y que se comprime,
no como meta de llenado. La arquitectura de 30 paginas queda como referencial;
el plan v2 debe declarar la extension objetivo final.

## 9. Editorial (refuerzos al intercambio)

- **Dos puntos:** 43 en 3.697 palabras (~1 cada 86). Regla: maximo uno cada
  ~120 palabras; reservarlos para introducir citas o enumeraciones. Donde hoy
  separan afirmacion/elaboracion, usar punto y oracion nueva o punto y coma.
- **Terminos internos:** 24 menciones, concentradas en las secciones 2, el
  resumen y el parrafo de agenda. Pasar la trazabilidad completa al anexo
  tecnico (titulo, ano, pagina, dimension_id, ruta, hash, exclusiones). En prosa
  citar solo "titulo (ano, p. X)".
- **Agenda del resumen y de las conclusiones:** reescribir a problemas de
  politica y capacidades (implementacion, financiamiento, coordinacion,
  capacidades, territorio, igualdad, derechos); eliminar prioridades
  metodologicas del cierre (trazabilidad, cuadros, revisiones pendientes).
- **Igualdad de genero:** mantener como ejemplo sectorial es defendible. Si el
  equipo quiere un tratamiento minimo, un parrafo de "igualdad y genero" en el
  capitulo transversal con 2 anclas y la nota de que Igualdad de genero como
  transformacion primaria salta de 1 a 6 en P2 (dato verificado). Requiere
  confirmacion humana (fila en compuerta).

## 10. Fuentes y trazabilidad

- Datos de transformaciones y niveles: tablas `typology`, `documents` de
  `fase3/02_eda/salidas/fase3_analitica_v1.sqlite`.
- Proporciones de dimensiones: `salidas/paquete_evolucion_enfoques_v1.md` y
  `salidas/paquete_gobernanza_multinivel_v1.md`.
- Tension dialectica: campo `tipologia.tension_dialectica` en los JSON canonicos.
- Verificacion de citas de bloques 02/03: `revisiones/AUDITORIA_INDEPENDIENTE_BLOQUES_02_03_v1.md`.
- Documentos de 2026: tabla `documents` (anio=2026): 85930, 86527, 89774, 89932,
  89934, 90001.
