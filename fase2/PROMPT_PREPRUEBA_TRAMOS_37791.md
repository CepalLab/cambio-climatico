# Preprueba segmentada — 11362/37791

Pega el bloque entre **INICIO DEL PROMPT** y **FIN DEL PROMPT** en una sesión limpia del harness, iniciada desde la raíz del repositorio.

---

## INICIO DEL PROMPT

Ejecuta una **preprueba sin tocar el ledger** para el documento `https://hdl.handle.net/11362/37791`. No proceses ni edites otro documento. No crees archivos bajo `fase2/corpus/resultados/` y no ejecutes `ledger.py start`, `retry`, `complete`, `approve` ni `reject`.

El objetivo es verificar que puedes mantener unida la evidencia con su página y capítulo antes de gastar el último reintento operativo.

Lee primero:

- `fase2/CONGELAMIENTO_PRE_BATCH_v1.md`
- `fase2/esquema_json_v1.md`
- `fase2/codebook_v0.md`
- `fase2/INTERPELACION_v0.md`
- `fase2/TIPOLOGIA_v0.md`
- `fase2/CASOS_ANCLA_INTERPELACION_v1.md`
- `fase2/corpus/lotes/L0001_REVISION_37791_INTENTO2.md`

## Fuentes y mapa obligatorio

- PDF: `fase2/corpus/pdfs/11362_37791.pdf`
- Tramos paginados: `fase2/corpus/intermedios/11362/37791/tramos/manifest.json`
- Mapa verificado de capítulos: `fase2/corpus/intermedios/11362/37791/tramos/mapa_capitulos.json`

Los archivos `tramo_XXX_YYY.txt` contienen marcadores `=== PÁGINA PDF N ===`. El mapa de capítulos es vinculante: no uses los rangos ni las citas de los borradores rechazados.

## Método obligatorio

1. Lee un tramo por vez. Para cada capítulo que toque el tramo, toma notas solo de las páginas que el mapa le asigna.
2. Para cada cita, conserva texto literal y su marcador de página. Nunca reasignes una cita a otra página o capítulo.
3. Cuando completes los seis tramos, produce un único borrador UTF-8 en `fase2/corpus/intermedios/11362/37791/borrador_tramos_preprueba.json`.
4. El borrador debe cumplir el esquema canónico, con `num_muestra: 2`, `paginas_cuerpo: 148` y los once capítulos exactos del mapa.
5. En `como_hacerlo_concreto`, aplica la selección de unidad de Ronda 9: no armes un tally con recomendaciones dispersas de capítulos distintos. Si no hay una sección final de recomendaciones propias con ítems operativos, corresponde `No` y se explica esa ausencia.
6. Conserva UTF-8 real: acentos, `ñ`, `¿` e `¡`; no uses caracteres de reemplazo ni mojibake.

## Validación obligatoria

Ejecuta ambas validaciones:

```bash
python3 fase2/pipeline/validar_esquema.py \
  fase2/corpus/intermedios/11362/37791/borrador_tramos_preprueba.json \
  > fase2/corpus/intermedios/11362/37791/validacion_esquema_preprueba.txt

python3 fase2/pipeline/validar_citas.py \
  fase2/corpus/intermedios/11362/37791/borrador_tramos_preprueba.json \
  fase2/corpus/intermedios/11362/37791/texto.txt \
  --pdf fase2/corpus/pdfs/11362_37791.pdf \
  > fase2/corpus/intermedios/11362/37791/validacion_citas_preprueba.txt
```

Si una validación falla, corrige el borrador y repite. No declares éxito hasta que ambas terminen con código 0.

Al terminar, responde solo con: rutas del borrador y ambos reportes; resultado de las dos validaciones; los cuatro veredictos; tipología primaria/secundaria; y confirmación explícita de que no tocaste el ledger ni `corpus/resultados/`.

## FIN DEL PROMPT
