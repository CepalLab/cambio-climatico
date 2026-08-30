# Manifiesto de congelación - Informe maestro v2

**Fecha de congelación:** 2026-08-28  
**Estado:** aprobado para circulación tras revisión humana final

## Artefacto congelado

- Archivo: `INFORME_MAESTRO_V2_CONGELADO_2026-08-28.md`
- SHA-256: `500114FBB00DF94F61D5FDA6716CC8FCC696DD39774AF5F7174C30046F4779DA`
- Corpus: 238 publicaciones activas de la CEPAL, 2015–2026, con 6 exclusiones documentadas.
- Figuras: 5 reproducibles.
- Cuadros: 4.
- Conteo editorial reproducible: 7.600 palabras, excluyendo sintaxis Markdown, enlaces y rutas de imagen.

## Alcance de la aprobación

La revisión humana final aprobó tono, prioridades, claridad y adecuación de las figuras. La versión de circulación podrá modificar únicamente portada, índice, estilo y formato de salida. No debe alterar evidencia, citas ancla, denominadores, exclusiones ni límites metodológicos.

## Reproducción

```powershell
& .venv/Scripts/python.exe fase3/03_analisis_contenido/scripts/generar_figuras_informe_v1.py
& .venv/Scripts/python.exe fase3/03_analisis_contenido/scripts/construir_informe_maestro_v2.py
```

La regeneración corresponde al informe de trabajo. La versión congelada se preserva como referencia de contenido aprobada para la circulación.