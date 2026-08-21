# 44163 ? ?ndice jer?rquico

Trabaja ?nicamente en `fase2/corpus/intermedios/11362/44163/`.

1. Lee `PREPARACION_FUENTE.md` y usa `tramos/` como fuente paginada.
2. Genera at?micamente el manifiesto definitivo:

```powershell
python fase2/pipeline/crear_manifiesto_indice.py fase2/corpus/intermedios/11362/44163/tramos --output fase2/corpus/intermedios/11362/44163/indice_fuente.json
```

3. Inspecciona el manifiesto. Debe conservar literalmente toda la jerarqu?a sustantiva de Introducci?n a `VI. Propuesta`; `I. Pol?ticas regionales y nacionales` debe ser nivel 2 dentro de `II. La producci?n de caf? en la Rep?blica Dominicana`.
4. No edites `borrador_preprueba.json`, no promociones y no crees res?menes en esta fase.
