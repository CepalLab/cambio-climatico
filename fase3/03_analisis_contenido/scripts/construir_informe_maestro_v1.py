"""Ensambla el borrador maestro del informe desde sus entregas narrativas revisadas."""

from pathlib import Path


ANALISIS_DIR = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ANALISIS_DIR / "RESUMEN_EJECUTIVO_INFORME_v1.md"
BLOCK_01_PATH = ANALISIS_DIR / "BLOQUE_NARRATIVO_01_METODO_EVOLUCION_BIG_PUSH_v1.md"
BLOCK_02_PATH = ANALISIS_DIR / "BLOQUE_NARRATIVO_02_P1_P7_v1.md"
BLOCK_03_PATH = ANALISIS_DIR / "BLOQUE_NARRATIVO_03_P9_CONCLUSIONES_AGENDA_v1.md"
OUTPUT_PATH = ANALISIS_DIR / "INFORME_MAESTRO_30P_BORRADOR_v1.md"


def section_between(path: Path, start: str, end: str | None) -> str:
    content = path.read_text(encoding="utf-8")
    section = content.split(start, 1)[1]
    if end:
        section = section.split(end, 1)[0]
    return section.strip()


def split_block_one(content: str) -> tuple[str, str]:
    big_push_heading = "### 3. Del sector a la estrategia: el Gran Impulso Ambiental"
    before, big_push = content.split(big_push_heading, 1)
    return before.strip(), ("### 7. Del sector a la estrategia: el Gran Impulso Ambiental" + big_push).strip()


def promote_sections(content: str) -> str:
    if content.startswith("### "):
        content = "## " + content[4:]
    return content.replace("\n### ", "\n## ")


def executive_content() -> str:
    content = SUMMARY_PATH.read_text(encoding="utf-8")
    marker = "Este informe analiza"
    return content[content.index(marker):].strip()


def main() -> None:
    block_one = section_between(BLOCK_01_PATH, "## Borrador narrativo", "## Referencias de evidencia")
    introduction, big_push = split_block_one(block_one)
    block_two = promote_sections(section_between(BLOCK_02_PATH, "## Borrador narrativo", "## Trazabilidad de evidencia"))
    block_three = promote_sections(section_between(BLOCK_03_PATH, "## Borrador narrativo", "## Trazabilidad de evidencia"))
    big_push = promote_sections(big_push)
    content = f"""# Informe maestro - Evolución del abordaje CEPAL sobre cambio climático

**Estado:** borrador integrado para revisión editorial final.  
**Base:** `fase3-analitica-v1`, 238 documentos activos y 6 exclusiones aplicadas.  
**Cobertura temporal:** 2015-2025; P1 (2015–2018), P2 (2019–2022) y P3 (2023–2026; el corpus disponible llega hasta 2025).

## Resumen ejecutivo

{executive_content()}

## 1. Introducción: un corpus para leer una agenda institucional

{introduction.split('### 1. Un corpus para leer una agenda institucional', 1)[1].split('### 2. De los impactos a las condiciones de transformación', 1)[0].strip()}

## 2. Corpus, método y límites

La unidad de análisis es el documento completo: pregunta de investigación, ámbito, resumen, hallazgos, conclusiones y recomendaciones. Los JSON de Fase 2 son la fuente canónica; SQLite permite consultas reproducibles; las clasificaciones de objeto, dominio y territorio son candidatas calibradas. Las citas literales se usan para definiciones, tensiones y mecanismos seleccionados, y conservan documento, página, hash y registro SQLite. El informe identifica patrones de formulación institucional; no estima consenso regional, adopción, eficacia ni causalidad de las políticas.

## 3. Evolución del objeto de estudio

{introduction.split('### 2. De los impactos a las condiciones de transformación', 1)[1].strip()}

{block_two}

{big_push}

{block_three}

## Cuadros y figuras

- [Cuadros 1 a 3](salidas/figuras_informe_v1/cuadros_01_02_cobertura.md)
- [Figura 1: objetos por período](salidas/figuras_informe_v1/figura_01_objetos_por_periodo.png)
- [Figura 2: modos analíticos](salidas/figuras_informe_v1/figura_02_modos_analiticos.png)
- [Figura 3: panel Big Push](salidas/figuras_informe_v1/figura_03_panel_big_push.png)
- [Figura 4: territorio y tipología](salidas/figuras_informe_v1/figura_04_territorio_tipologia.png)

## Estado de revisión

Los bloques narrativos 01, 02 y 03 cuentan con revisión humana y auditoría independiente. Las afirmaciones sobre pérdidas y daños y responsabilidades comunes pero diferenciadas no se presentan como conclusiones sustantivas en este borrador hasta completar su compuerta específica.

## Fuentes de integración

- `RESUMEN_EJECUTIVO_INFORME_v1.md`
- `BLOQUE_NARRATIVO_01_METODO_EVOLUCION_BIG_PUSH_v1.md`
- `BLOQUE_NARRATIVO_02_P1_P7_v1.md`
- `BLOQUE_NARRATIVO_03_P9_CONCLUSIONES_AGENDA_v1.md`
"""
    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(OUTPUT_PATH.as_posix())


if __name__ == "__main__":
    main()