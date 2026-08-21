# Corrección de preprueba segmentada — 11362/37791

Pega el bloque entre **INICIO DEL PROMPT** y **FIN DEL PROMPT** en una sesión limpia del harness, iniciada desde la raíz del repositorio.

---

## INICIO DEL PROMPT

Corrige exclusivamente la preprueba del documento `https://hdl.handle.net/11362/37791`.

No proceses ni edites otro documento. No toques `fase2/corpus/resultados/` y no ejecutes `ledger.py start`, `retry`, `complete`, `approve`, `reject` ni ningún otro comando del ledger. Esta es una preprueba de corrección; aún no es el reintento formal.

## Insumos obligatorios

- Borrador a corregir: `fase2/corpus/intermedios/11362/37791/borrador_tramos_preprueba.json`
- Tramos con páginas explícitas: `fase2/corpus/intermedios/11362/37791/tramos/manifest.json`
- Mapa verificado de capítulos: `fase2/corpus/intermedios/11362/37791/tramos/mapa_capitulos.json`
- PDF: `fase2/corpus/pdfs/11362_37791.pdf`
- Texto DSpace: `fase2/corpus/intermedios/11362/37791/texto.txt`
- Revisión anterior: `fase2/corpus/lotes/L0001_REVISION_37791_INTENTO2.md`
- Metodología: `fase2/esquema_json_v1.md`, `fase2/INTERPELACION_v0.md`, `fase2/TIPOLOGIA_v0.md` y `fase2/CASOS_ANCLA_INTERPELACION_v1.md`

## Correcciones obligatorias

1. Conserva los once capítulos y sus rangos del mapa. No vuelvas a usar los rangos desplazados de borradores anteriores.
2. Amplía cada resumen de capítulo que no cumpla el piso proporcional del esquema. Debe explicar argumento, hallazgos/cifras y actores o instrumentos cuando existan; no rellenes con frases genéricas.
3. Conserva una cita solo si aparece en la página que declara. Si cambias una cita o su página, compruébala contra el tramo y el PDF.
4. Corrige el bloque `documento` a estos valores:

   ```json
   {
     "num_muestra": 2,
     "autoria": "Carlos de Miguel • Marcia Tavares (compiladores)",
     "simbolo": "LC/M.23",
     "isbn": "978-92-1-057087-9",
     "fecha": "2015-01-01",
     "tipo_documento": "Compilación de textos seleccionados",
     "paginas_cuerpo": 148,
     "paginas_totales": 148
   }
   ```

5. Fija la tipología en primaria `#6 Sostenibilidad ambiental` y secundaria `#11 Capacidades del Estado`, ambas con certeza alta. Justifica la secundaria con la regla objeto–instrumento: la sostenibilidad ambiental es el objeto; regulación, planificación, fiscalidad, derechos de acceso e institucionalidad son medios de implementación. No uses `#2` como secundaria solo porque el documento menciona igualdad.
6. Mantén `como_hacerlo_concreto` en `No` si, aplicando la regla de Ronda 9, no existe una única sección de cierre con recomendaciones propias y operativas. No armes el tally mezclando medidas dispersas del cuerpo.
7. Reevalúa los otros tres criterios de interpelación con sus citas ya bien localizadas; no fuerces un cambio de veredicto si la evidencia no lo exige.
8. Conserva UTF-8 real: acentos, `ñ`, `¿` e `¡`; no uses mojibake ni caracteres de reemplazo.

## Salida y validación

Escribe el resultado únicamente en:

`fase2/corpus/intermedios/11362/37791/borrador_tramos_preprueba_v2.json`

Luego ejecuta y guarda ambos reportes:

```bash
python3 fase2/pipeline/validar_esquema.py \
  fase2/corpus/intermedios/11362/37791/borrador_tramos_preprueba_v2.json \
  > fase2/corpus/intermedios/11362/37791/validacion_esquema_preprueba_v2.txt

python3 fase2/pipeline/validar_citas.py \
  fase2/corpus/intermedios/11362/37791/borrador_tramos_preprueba_v2.json \
  fase2/corpus/intermedios/11362/37791/texto.txt \
  --pdf fase2/corpus/pdfs/11362_37791.pdf \
  > fase2/corpus/intermedios/11362/37791/validacion_citas_preprueba_v2.txt
```

Si cualquiera falla, corrige y repite. No declares éxito hasta que ambas terminen con código 0.

Al finalizar, responde solo con: rutas del borrador y reportes; resultado de ambas validaciones; cuatro veredictos; tipología primaria/secundaria; y confirmación explícita de que no tocaste el ledger ni `corpus/resultados/`.

## FIN DEL PROMPT
