"""Verifica que todas las citas del JSON aparezcan literalmente en el texto fuente."""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

# Evita que un glifo v?lido de la fuente trunque un reporte de error en consolas
# Windows configuradas en cp1252.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).replace("\u00ad", "")
    text = re.sub(r"(?<=\w)-\s+(?=\w)", "", text)
    return re.sub(r"\s+", " ", text).strip().casefold()


def section_citations(sections: list[dict], path: str = ""):
    for section in sections:
        section_path = f"{path}/{section.get('seccion', '?')}"
        for index, dimension in enumerate(section.get("dimensiones", []), 1):
            yield f"resumen_secciones{section_path}/dimension[{index}]", dimension.get("cita")
        yield from section_citations(section.get("subsecciones", []), section_path)


def citations(document: dict):
    yield from section_citations(document.get("resumen_secciones", []))
    for criterion, value in document.get("interpelacion", {}).items():
        for index, citation in enumerate(value.get("citas", []), 1):
            yield f"interpelacion/{criterion}/cita[{index}]", citation.get("cita")


PAGE_MARKER = re.compile(r"^=== PÁGINA (?:PDF|IMPRESA) (\d+) ===\s*$", re.M)
OCR_TOKEN = re.compile(r"\b(?:[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]{3,}[0-9?]+[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]*|\d+oo)\b")
OCR_TOKEN_EXCEPTIONS = {"gtco2", "gtco2e", "tco2e", "cop20", "cop21", "cop20e", "cop21e"}
TRUNCATED_END = re.compile(
    r"(?:\b(?:a|al|de|del|el|en|la|las|lo|los|por|para|que|un|una|y)|[,;:])$",
    re.I,
)
EDITORIAL_LABEL = re.compile(
    r"^(?:(?:tabla|table|cuadro|figure|figura|chart|gr[áa]fico|diagram|diagrama|box|recuadro|mapa)"
    r"\s*(?:[a-z]?\d+[\w.:-]*|[ivxlcdm]+)?\b|(?:fuente|source)\s*:)",
    re.I,
)
META_TABLE_SENTENCE = re.compile(
    r"^(?:the )?(?:sources?|fuentes?)\s+(?:of |de )?(?:information|informaci[oó]n).*"
    r"(?:table|tabla|cuadro|figure|figura)\b",
    re.I,
)


def load_page_source(path: Path) -> dict[int, str]:
    manifest_path = path / "manifest.json" if path.is_dir() else path
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pages = {}
    for chunk in manifest.get("chunks", []):
        chunk_path = manifest_path.parent / chunk["path"]
        text = chunk_path.read_text(encoding="utf-8")
        markers = list(PAGE_MARKER.finditer(text))
        for index, marker in enumerate(markers):
            page = int(marker.group(1))
            end = markers[index + 1].start() if index + 1 < len(markers) else len(text)
            pages[page] = normalize(text[marker.end() : end])
    if not pages:
        raise ValueError("El manifiesto de tramos no contiene marcadores de página legibles")
    return pages


def citation_quality(quotation: str) -> str | None:
    cleaned = quotation.strip()
    if len(normalize(cleaned)) < 40:
        return "demasiado corta o fragmentaria"
    if re.match(r"(?i)^(cepal|cap[ií]tulo|parte\s+[ivx]+)\b", cleaned):
        return "incluye encabezado editorial"
    if EDITORIAL_LABEL.match(cleaned):
        return "es un rótulo editorial (tabla, figura, cuadro, fuente o gráfico), no evidencia de cuerpo"
    if META_TABLE_SENTENCE.match(cleaned):
        return "describe la procedencia de una tabla, no una afirmación analítica"
    if "•" in cleaned and not re.search(r"[.!?;:]$", cleaned):
        return "es una lista o etiqueta sin una proposición autónoma"
    if "http://" in cleaned.lower() or "https://" in cleaned.lower():
        return "incluye URL editorial"
    ocr_tokens = [match.group().casefold() for match in OCR_TOKEN.finditer(cleaned)]
    if "\ufffd" in cleaned or any(token not in OCR_TOKEN_EXCEPTIONS for token in ocr_tokens):
        return "contiene un artefacto OCR dentro de una palabra"
    if TRUNCATED_END.search(cleaned):
        return "termina como una frase cortada; use una oración o cláusula autónoma completa"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result", type=Path)
    parser.add_argument("source", type=Path, nargs="?", help="Texto fuente para literalidad")
    parser.add_argument("--pdf", type=Path, help="Comprueba también la página declarada contra el PDF")
    parser.add_argument(
        "--page-source",
        type=Path,
        help="Manifiesto o directorio de tramos nativos/OCR con marcadores === PÁGINA PDF N ===",
    )
    parser.add_argument("--strict-quality", action="store_true", help="Convierte citas fragmentarias/editoriales en error")
    parser.add_argument(
        "--quality-only",
        action="store_true",
        help="Revisa formato editorial sin afirmar literalidad; usar solo con evidencia visual revisada",
    )
    arguments = parser.parse_args()
    if arguments.pdf and arguments.page_source:
        raise SystemExit("Use solo uno de --pdf o --page-source")
    if not arguments.quality_only and not arguments.page_source and arguments.source is None:
        raise SystemExit("source es obligatorio salvo con --quality-only o --page-source")

    document = json.loads(arguments.result.read_text(encoding="utf-8"))
    source = ""
    if arguments.source and arguments.source.is_file():
        source = normalize(arguments.source.read_text(encoding="utf-8"))
    pdf_pages = None
    page_source = None
    if arguments.pdf:
        try:
            from pypdf import PdfReader
        except ImportError as error:
            raise SystemExit("La validación de páginas requiere pypdf") from error
        pdf_pages = [normalize(page.extract_text() or "") for page in PdfReader(arguments.pdf).pages]
    if arguments.page_source:
        page_source = load_page_source(arguments.page_source)
        source = normalize(" ".join(page_source.values()))
    checked = 0
    missing = []
    wrong_page = []
    quality_warnings = []
    dimension_citations = {}
    for location, quotation, page_value in citation_records(document):
        checked += 1
        if not isinstance(quotation, str) or not quotation.strip():
            missing.append((location, "<cita vacía>"))
        elif not arguments.quality_only and normalize(quotation) not in source:
            missing.append((location, quotation))
        else:
            issue = citation_quality(quotation)
            if issue:
                quality_warnings.append((location, issue, quotation))
            if location.startswith("resumen_secciones"):
                dimension_citations.setdefault(normalize(quotation), []).append(location)
        if (
            not arguments.quality_only
            and (pdf_pages is not None or page_source is not None)
            and isinstance(quotation, str)
            and quotation.strip()
        ):
            page_range = parse_page_range(page_value)
            if page_range is None:
                wrong_page.append((location, page_value, [], quotation))
                continue
            if pdf_pages is not None:
                claimed_text = " ".join(pdf_pages[page_range[0] - 1 : page_range[1]])
                actual = [index for index, page in enumerate(pdf_pages, 1) if normalize(quotation) in page]
            else:
                claimed_text = " ".join(page_source.get(page, "") for page in range(page_range[0], page_range[1] + 1))
                actual = [page for page, text in page_source.items() if normalize(quotation) in text]
            if normalize(quotation) not in claimed_text:
                wrong_page.append((location, page_value, actual, quotation))

    if missing:
        print(f"{len(missing)} de {checked} citas no aparecen literalmente en la fuente:")
        for location, quotation in missing:
            print(f" - {location}: {quotation[:160]}")
    if wrong_page:
        print(f"{len(wrong_page)} de {checked} citas no coinciden con la página declarada:")
        for location, claimed, actual, quotation in wrong_page:
            print(f" - {location}: declara {claimed}; aparece en {actual or 'página no localizada'}; {quotation[:120]}")
    if quality_warnings:
        print(f"{len(quality_warnings)} cita(s) requieren pulido editorial:")
        for location, issue, quotation in quality_warnings:
            print(f" - {location}: {issue}; {quotation[:120]}")
    duplicates = [locations for quote, locations in dimension_citations.items() if quote and len(locations) > 1]
    if duplicates:
        print(f"{len(duplicates)} cita(s) se reutilizan entre dimensiones:")
        for locations in duplicates:
            print(f" - {' | '.join(locations)}")
    if missing or wrong_page or (arguments.strict_quality and (quality_warnings or duplicates)):
        return 1
    if arguments.quality_only:
        print(f"Todas las citas superan el control editorial ({checked}/{checked}).")
    else:
        suffix = " y en la página declarada" if pdf_pages is not None or page_source is not None else ""
        print(f"Todas las citas verificadas literalmente en la fuente{suffix} ({checked}/{checked}).")
    return 0


def parse_page_range(value):
    if isinstance(value, int) and value > 0:
        return value, value
    if isinstance(value, str):
        match = re.fullmatch(r"\s*(\d+)\s*(?:-\s*(\d+))?\s*", value)
        if match:
            return int(match.group(1)), int(match.group(2) or match.group(1))
    return None


def citation_records(document: dict):
    def section_records(sections: list[dict], path: str = ""):
        for section in sections:
            section_path = f"{path}/{section.get('seccion', '?')}"
            for index, dimension in enumerate(section.get("dimensiones", []), 1):
                yield (
                    f"resumen_secciones{section_path}/dimension[{index}]",
                    dimension.get("cita"),
                    dimension.get("pagina"),
                )
            yield from section_records(section.get("subsecciones", []), section_path)

    yield from section_records(document.get("resumen_secciones", []))
    for criterion, value in document.get("interpelacion", {}).items():
        for index, citation in enumerate(value.get("citas", []), 1):
            yield (
                f"interpelacion/{criterion}/cita[{index}]",
                citation.get("cita"),
                citation.get("pagina"),
            )


if __name__ == "__main__":
    sys.exit(main())
