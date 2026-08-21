# Pulido preaprobación — 11362/37791

Pega el bloque entre **INICIO DEL PROMPT** y **FIN DEL PROMPT** en una sesión limpia del harness, iniciada desde la raíz del repositorio.

---

## INICIO DEL PROMPT

Ejecuta solo una pasada editorial de preaprobación para `https://hdl.handle.net/11362/37791`.

No proceses otro documento. No edites `fase2/corpus/resultados/` y no ejecutes ningún comando de `ledger.py`. El resultado actual sigue en revisión humana; esta tarea genera un borrador alternativo para comparar antes de reemplazarlo.

## Insumos

- Borrador validado base: `fase2/corpus/intermedios/11362/37791/borrador_tramos_preprueba_v2.json`
- Tramos y mapa de capítulos: `fase2/corpus/intermedios/11362/37791/tramos/`
- PDF: `fase2/corpus/pdfs/11362_37791.pdf`
- Texto DSpace: `fase2/corpus/intermedios/11362/37791/texto.txt`
- Esquema y metodología: `fase2/esquema_json_v1.md`, `fase2/codebook_v0.md`, `fase2/INTERPELACION_v0.md` y `fase2/TIPOLOGIA_v0.md`

## Objetivo editorial

El borrador base tiene 94 dimensiones: está sobrecodificado para un documento de 148 páginas. Reduce el total a aproximadamente **45–60 dimensiones** sin perder los hallazgos sustantivos.

Para cada capítulo, conserva solo evidencia de afirmaciones analíticamente distintas: diagnóstico, tendencia, desafío, oportunidad o propuesta con contenido propio. No conviertas cada dato, encabezado o variación del mismo argumento en una dimensión separada. Como orientación, usa 3–6 dimensiones por capítulo, con excepción justificada del capítulo I si contiene varios bloques realmente diferenciados.

## Regla de pulido de citas

Cada cita que permanezca debe:

1. Ser literal y estar en la página declarada.
2. Ser una oración completa o una cláusula autónoma con sujeto/idea reconocible.
3. Conservar puntuación y capitalización legibles.
4. Excluir encabezados, pies, títulos de capítulo, viñetas aisladas, números sueltos, texto de URL y frases cortadas.

Elimina, en particular, citas como `"actualmente en"`, `"la movilidad urbana y los pobres"`, encabezados con `"CEPAL"` y cualquier cita que empiece o termine a mitad de oración. Si una dimensión no tiene una cita limpia disponible en su página, elimina esa dimensión en vez de conservar una cita defectuosa.

No cambies el índice, rangos de páginas, metadata, tipología `#6/#11`, ni el veredicto `No` de `como_hacerlo_concreto`, salvo que una corrección editorial revele un error factual verificable.

## Salida y validación

Escribe únicamente:

`fase2/corpus/intermedios/11362/37791/borrador_pulido_preaprobacion.json`

Ejecuta y guarda:

```bash
python3 fase2/pipeline/validar_esquema.py \
  fase2/corpus/intermedios/11362/37791/borrador_pulido_preaprobacion.json \
  > fase2/corpus/intermedios/11362/37791/validacion_esquema_pulido.txt

python3 fase2/pipeline/validar_citas.py \
  fase2/corpus/intermedios/11362/37791/borrador_pulido_preaprobacion.json \
  fase2/corpus/intermedios/11362/37791/texto.txt \
  --pdf fase2/corpus/pdfs/11362_37791.pdf \
  > fase2/corpus/intermedios/11362/37791/validacion_citas_pulido.txt
```

Corrige hasta que ambos comandos terminen con código 0. Al finalizar, informa únicamente: número de dimensiones antes/después; rutas del borrador y reportes; resultado de ambos validadores; y confirmación de que no tocaste el ledger ni `corpus/resultados/`.

## FIN DEL PROMPT
