# 44163 ? consolidaci?n final

Trabaja ?nicamente en `fase2/corpus/intermedios/11362/44163/`.

Lee `borrador_preprueba.json`, `indice_fuente.json`, `parcial_44163_p1.json`, `parcial_44163_p2.json`, `parcial_44163_p3.json`, `texto.txt` y `tramos/`.

1. Conserva sin cambios `documento`, `resumen_enriquecido`, `interpelacion` y `tipologia` del borrador actual.
2. Reemplaza solo `resumen_secciones` por la concatenaci?n ordenada P1, P2 y P3.
3. La jerarqu?a resultante debe coincidir exactamente con `secciones_jerarquicas_incluidas` en t?tulos, puntuaci?n, niveles, orden y cobertura. No incluyas anexos, abreviaturas, bibliograf?a ni encabezados repetidos.
4. Escribe `borrador_preprueba.json` at?micamente y actualiza `EJECUCION_ENRIQUECIMIENTO.md` con este re-enriquecimiento estructural.
5. Ejecuta y guarda en UTF-8 los cuatro reportes:

```powershell
python fase2/pipeline/validar_esquema.py fase2/corpus/intermedios/11362/44163/borrador_preprueba.json
python fase2/pipeline/validar_indice.py fase2/corpus/intermedios/11362/44163/borrador_preprueba.json --indice fase2/corpus/intermedios/11362/44163/indice_fuente.json
python fase2/pipeline/validar_citas.py fase2/corpus/intermedios/11362/44163/borrador_preprueba.json fase2/corpus/intermedios/11362/44163/texto.txt --page-source fase2/corpus/intermedios/11362/44163/tramos --strict-quality
python fase2/pipeline/auditar_densidad.py fase2/corpus/intermedios/11362/44163/borrador_preprueba.json
```

Corrige hasta que las cuatro compuertas est?n limpias. No promociones el documento.
