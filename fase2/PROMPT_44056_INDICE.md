# 44056 ? ?ndice jer?rquico

Trabaja solo en `fase2/corpus/intermedios/11362/44056/`.

1. Lee `PREPARACION_FUENTE.md` y usa `tramos/` como fuente paginada.
2. Genera at?micamente el ?ndice definitivo:

```powershell
python fase2/pipeline/crear_manifiesto_indice.py fase2/corpus/intermedios/11362/44056/tramos --output fase2/corpus/intermedios/11362/44056/indice_fuente.json
```

3. Confirma que el manifiesto contiene, en este orden, las cuatro secciones de nivel 1: `Introducci?n`, cap?tulo I, cap?tulo II y `III. CONCLUSIONES Y RECOMENDACIONES`.
4. El manifiesto no debe incluir el encabezado repetido del t?tulo del documento, cuadros, gr?ficos, bibliograf?a ni anexos.
5. No edites el borrador ni promociones en esta fase.
