"""Ensambla el informe maestro v2 desde los bloques narrativos revisados."""

import re
from pathlib import Path


ANALISIS_DIR = Path(__file__).resolve().parents[1]
SOURCES = {
    "summary": ANALISIS_DIR / "RESUMEN_EJECUTIVO_INFORME_v1.md",
    "block_01": ANALISIS_DIR / "BLOQUE_NARRATIVO_01_METODO_EVOLUCION_BIG_PUSH_v1.md",
    "block_02": ANALISIS_DIR / "BLOQUE_NARRATIVO_02_P1_P7_v1.md",
    "block_03": ANALISIS_DIR / "BLOQUE_NARRATIVO_03_P9_CONCLUSIONES_AGENDA_v1.md",
    "block_04": ANALISIS_DIR / "BLOQUE_NARRATIVO_04_EXPANSION_V2.md",
    "annex": ANALISIS_DIR / "ANEXO_TECNICO_INFORME_V2.md",
}
OUTPUT = ANALISIS_DIR / "INFORME_MAESTRO_V2_BORRADOR.md"
CITATIONS = {
    "46227": ("Construir un nuevo futuro: una recuperación transformadora con igualdad y sostenibilidad", 2020),
    "39140": ("Impactos y vulnerabilidad al cambio climático de los principales ríos de Mendoza y San Juan", 2015),
    "44640": ("Hacia una bioeconomía sostenible en América Latina y el Caribe", 2019),
    "41832": ("Metodologías para apoyar la estimación de costos en Guatemala", 2017),
    "47720": ("Cómo financiar el desarrollo sostenible", 2022),
    "80561": ("Desafíos y oportunidades para la ejecución de proyectos de inversión pública con criterios de sostenibilidad", 2024),
    "81405": ("América Latina y el Caribe y la Agenda 2030 a cinco años de la meta", 2025),
    "40159": ("Horizontes 2030: la igualdad en el centro del desarrollo sostenible", 2016),
    "43825": ("Contribuciones a un gran impulso ambiental en América Latina y el Caribe: bioeconomía", 2018),
    "43301": ("Acceso a la información, la participación y la justicia en asuntos ambientales", 2018),
    "44970": ("Cambio climático y derechos humanos", 2019),
    "41101": ("La transversalización del enfoque de género en las políticas públicas frente al cambio climático en América Latina", 2017),
}


def between(text: str, start: str, end: str | None) -> str:
    result = text.split(start, 1)[1]
    return result.split(end, 1)[0].strip() if end else result.strip()


def clean(text: str) -> str:
    text = re.sub(r"; registro SQLite `dimension_id` \d+", "", text)
    text = text.replace("P1 (2015–2018)", "2015–2018")
    text = text.replace("P2 (2019–2022)", "2019–2022")
    text = text.replace("P3 (2023–2026, con seis publicaciones fechadas en 2026)", "2023–2026 (período abierto, con seis publicaciones fechadas en 2026)")
    text = text.replace("P3 (2023–2026; el corpus disponible llega hasta 2025)", "2023–2026")
    text = re.sub(r"\bP1\b", "2015–2018", text)
    text = re.sub(r"\bP2\b", "2019–2022", text)
    text = re.sub(r"\bP3\b", "2023–2026", text)
    for handle, (title, year) in CITATIONS.items():
        text = text.replace(f"({handle}, p.", f"(*{title}*, {year}, p.")
    return text.replace("#### Recuadro.", "### Recuadro.")


def promote(text: str) -> str:
    if text.startswith("### "):
        text = "## " + text[4:]
    return text.replace("\n### ", "\n## ").replace("\n#### ", "\n### ")


def main() -> None:
    summary = SOURCES["summary"].read_text(encoding="utf-8")
    summary = summary[summary.index("Este informe analiza"):].strip()
    block_01 = between(SOURCES["block_01"].read_text(encoding="utf-8"), "## Borrador narrativo", "## Referencias de evidencia")
    intro = between(block_01, "### 1. Un corpus para leer una agenda institucional", "### 2. De los impactos a las condiciones de transformación")
    evolution = between(block_01, "### 2. De los impactos a las condiciones de transformación", "### 3. Del sector a la estrategia: el Gran Impulso Ambiental")
    big_push = between(block_01, "### 3. Del sector a la estrategia: el Gran Impulso Ambiental", None)
    block_02 = promote(between(SOURCES["block_02"].read_text(encoding="utf-8"), "## Borrador narrativo", "## Trazabilidad de evidencia"))
    block_03 = promote(between(SOURCES["block_03"].read_text(encoding="utf-8"), "## Borrador narrativo", "## Trazabilidad de evidencia"))
    participation = between(block_03, "## 8. Participación, derechos y distribución", "## 9. Conclusiones y agenda de análisis")
    conclusions = between(block_03, "## 9. Conclusiones y agenda de análisis", None)
    conclusions = conclusions.split("La agenda derivada", 1)[0].strip() + "\n\n" + "La agenda sustantiva que plantea el corpus se concentra en conectar los objetivos climáticos con financiamiento asequible, inversión pública, coordinación institucional, capacidades territoriales, datos para el seguimiento, igualdad y derechos de acceso. El desafío no consiste únicamente en ampliar instrumentos, sino en asegurar que puedan operar de manera sostenida en los territorios y distribuir de forma justa costos, riesgos y beneficios."
    block_04 = SOURCES["block_04"].read_text(encoding="utf-8")
    scales = between(block_04, "## 7. De la subregión a la ciudad: escalas y capacidades de implementación", "## 8. Grandes transformaciones y tensiones que el corpus procesa")
    tensions = between(block_04, "## 8. Grandes transformaciones y tensiones que el corpus procesa", "## 9. Propuestas, avances y brechas: una coherencia condicionada")
    coherence = between(block_04, "## 9. Propuestas, avances y brechas: una coherencia condicionada", "## Nota sobre pérdidas y daños y CBDR")
    tables = (ANALISIS_DIR / "salidas" / "figuras_informe_v1" / "cuadros_01_02_cobertura.md").read_text(encoding="utf-8")
    coherence_table = between(tables, "## Cuadro 4. Propuestas, avances y brechas de implementación", None)
    coherence_table = "### Cuadro 4. Propuestas, avances y brechas de implementación\n\n" + coherence_table
    figures_01_02 = """![Figura 1. Objetos principales candidatos por período](salidas/figuras_informe_v1/figura_01_objetos_por_periodo.png)

*Figura 1. La comparación presenta proporciones de objetos principales candidatos por período; no equivale a una codificación experta exhaustiva.*

![Figura 2. Modos analíticos por período](salidas/figuras_informe_v1/figura_02_modos_analiticos.png)

*Figura 2. Los cinco primeros modos son candidatos; conclusiones, recomendaciones y política concreta proceden de campos directos de los documentos.*"""
    figure_03 = """![Figura 3. Escalas territoriales por período](salidas/figuras_informe_v1/figura_03_territorio.png)

*Figura 3. Las escalas territoriales son multietiqueta y no suman el total del corpus.*"""
    figure_04 = """![Figura 4. Transformaciones secundarias asociadas a sostenibilidad ambiental](salidas/figuras_informe_v1/figura_04_sostenibilidad_secundarias.png)

*Figura 4. Cada conexión representa documentos con sostenibilidad ambiental como transformación primaria y la categoría indicada como secundaria; el tamaño de los nodos secundarios corresponde al número de documentos.*"""
    figure_05 = """![Figura 5. Panel Big Push Ambiental por período](salidas/figuras_informe_v1/figura_05_panel_big_push.png)

*Figura 5. La matriz describe el contenido documental mediante cuatro criterios; no mide ejecución ni resultados de política.*"""
    document = f"""# Evolución del abordaje CEPAL sobre cambio climático

**Borrador v2 para revisión editorial.** El informe examina 238 publicaciones activas de la CEPAL entre 2015 y 2026. Para ordenar la comparación, distingue un primer período (2015–2018), un período intermedio (2019–2022) y un período reciente (2023–2026), que incluye seis publicaciones fechadas en 2026.

## Resumen ejecutivo

{clean(summary)}

## 1. Introducción: un corpus para leer una agenda institucional

{clean(intro)}

## 2. Corpus, método y límites

El análisis parte de publicaciones completas, considerando sus preguntas, ámbitos, hallazgos, conclusiones y recomendaciones. Las clasificaciones de objeto, territorio y tipología organizan la lectura, pero no reemplazan la interpretación de cada documento. Las citas se usan de manera selectiva para sostener definiciones y mecanismos decisivos. El informe identifica patrones en la agenda institucional de la CEPAL y no estima consenso regional, adopción, eficacia ni causalidad de políticas.

La comparación usa tres ventanas de calendario: 2015–2018, 2019–2022 y 2023–2026. El corpus comienza en 2015, año del Acuerdo de París, y los intervalos de aproximadamente cuatro años permiten comparar bloques de tamaño razonable y seguir una evolución legible. No son etapas derivadas automáticamente del contenido ni de un único evento. Sus denominadores son desiguales (99, 75 y 64 documentos) y el período más reciente sigue abierto, con seis publicaciones de 2026. Por eso, las diferencias se interpretan como cambios de énfasis que también pueden reflejar composición documental, tipos de publicación y divisiones institucionales.

## 3. Evolución del objeto de estudio

{clean(evolution)}

{figures_01_02}

{clean(block_02)}

## 7. De la subregión a la ciudad: escalas y capacidades de implementación

{clean(scales)}

{figure_03}

## 8. Grandes transformaciones y tensiones que el corpus procesa

{clean(tensions)}

{figure_04}

## 9. Del sector a la estrategia: el Gran Impulso Ambiental

{clean(big_push)}

{figure_05}

## 10. Participación, derechos y distribución

{clean(participation)}

## 11. Propuestas, avances y brechas: una coherencia condicionada

{clean(coherence)}

{coherence_table}

## 12. Conclusiones y agenda

{clean(conclusions)}

## Figuras y cuadros

- [Cuadros 1 a 3](salidas/figuras_informe_v1/cuadros_01_02_cobertura.md)
- [Figuras 1 a 5](salidas/figuras_informe_v1/)

## Anexo técnico

La metodología ampliada, la rúbrica del Gran Impulso Ambiental, las exclusiones, la trazabilidad de las citas ancla y la verificación de ejes se encuentran en el [Anexo técnico del informe v2](ANEXO_TECNICO_INFORME_V2.md).
"""
    OUTPUT.write_text(document, encoding="utf-8")
    print(OUTPUT.as_posix())


if __name__ == "__main__":
    main()