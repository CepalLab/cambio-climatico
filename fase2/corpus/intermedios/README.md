# Artefactos intermedios

Directorio local para textos extraídos, borradores JSON y otros checkpoints recuperables. Su contenido no se versiona; cada artefacto debe quedar referenciado en el ledger operativo.

Para documentos de 100+ páginas o 250.000+ caracteres, `pipeline/preparar_tramos_pdf.py` crea un subdirectorio `tramos/` con bloques de 25 páginas y un manifiesto. Los tramos mantienen el número de página del PDF para evitar reasignar evidencia entre capítulos.
