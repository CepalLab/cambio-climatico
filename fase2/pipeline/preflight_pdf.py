"""Compara extractores locales y prepara tramos paginados solo si la mejor salida es usable."""

import argparse
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path

from layout_extraction import extract_document_layout_aware


MOJIBAKE = ("Ã¡", "Ã©", "Ã­", "Ã³", "Ãº", "Ã±", "â€™", "â€œ", "â€", "\ufffd")
OCR_ARTIFACT = re.compile(r"\b(?:[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]{3,}[0-9?]+[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]*|\d+oo)\b")


def assess(pages: list[str]) -> dict[str, int | float | bool]:
    text = "\n".join(pages)
    characters = len(text.strip())
    controls = sum(
        unicodedata.category(character).startswith("C") and character not in "\n\r\t"
        for character in text
    )
    mojibake = sum(text.count(marker) for marker in MOJIBAKE)
    ocr_artifacts = len(OCR_ARTIFACT.findall(text))
    cid_markers = text.count("(cid:")
    cipher_symbols = sum(character in "&$%`" for character in text)
    cipher_ratio = cipher_symbols / max(1, characters)
    pages_with_text = sum(bool(page.strip()) for page in pages)
    letters = sum(character.isalpha() for character in text)
    usable = (
        characters >= 5_000
        and pages_with_text >= max(1, int(len(pages) * 0.8))
        and controls / max(1, len(text)) <= 0.02
        and mojibake == 0
        and cid_markers == 0
        and cipher_ratio <= 0.005
    )
    score = (
        min(40, characters / max(1, len(pages)) / 100)
        + 25 * pages_with_text / max(1, len(pages))
        + 20 * letters / max(1, characters)
        - min(20, controls / max(1, len(text)) * 1_000)
        - min(10, mojibake * 2)
        - min(10, ocr_artifacts / max(1, len(pages)))
        - min(25, cid_markers / max(1, len(pages)))
        - min(25, cipher_ratio * 1_000)
    )
    return {
        "characters": characters,
        "pages_with_text": pages_with_text,
        "control_characters": controls,
        "control_ratio": round(controls / max(1, len(text)), 6),
        "mojibake": mojibake,
        "ocr_artifacts": ocr_artifacts,
        "cid_markers": cid_markers,
        "cipher_ratio": round(cipher_ratio, 6),
        "score": round(score, 2),
        "usable": usable,
    }


def extract_pypdf(pdf: Path) -> list[str]:
    from pypdf import PdfReader

    return [page.extract_text() or "" for page in PdfReader(pdf).pages]


def extract_pymupdf(pdf: Path) -> list[str]:
    import fitz

    document = fitz.open(pdf)
    try:
        pages, _ = extract_document_layout_aware(document)
        return pages
    finally:
        document.close()


def extract_pymupdf_with_layout(pdf: Path) -> tuple[list[str], dict]:
    import fitz

    document = fitz.open(pdf)
    try:
        return extract_document_layout_aware(document)
    finally:
        document.close()


def extract_pdfplumber(pdf: Path) -> list[str]:
    import pdfplumber

    with pdfplumber.open(pdf) as document:
        return [page.extract_text() or "" for page in document.pages]


EXTRACTORS = {
    "pypdf": extract_pypdf,
    "pymupdf": extract_pymupdf,
    "pdfplumber": extract_pdfplumber,
}


UNKNOWN_LAYOUT = {"layout": "unknown", "method": "not_available"}


def pymupdf_layout_diagnostic(candidates: list[dict]) -> dict:
    """Return the spatial layout diagnosis independently of the selected extractor."""
    candidate = next((item for item in candidates if item.get("extractor") == "pymupdf"), None)
    return candidate.get("layout", UNKNOWN_LAYOUT) if candidate else UNKNOWN_LAYOUT


def write_json(path: Path, payload: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def write_chunks(output_dir: Path, pages: list[str], pages_per_chunk: int, manifest: dict) -> None:
    for start in range(0, len(pages), pages_per_chunk):
        end = min(start + pages_per_chunk, len(pages))
        path = output_dir / f"tramo_{start + 1:03d}_{end:03d}.txt"
        content = "\n\n".join(
            f"=== PÁGINA PDF {page_number} ===\n{pages[page_number - 1]}"
            for page_number in range(start + 1, end + 1)
        ) + "\n"
        path.write_text(content, encoding="utf-8")
        manifest["chunks"].append(
            {"pages": f"{start + 1}-{end}", "path": path.name, "quality": assess(pages[start:end])}
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--pages-per-chunk", type=int, default=25)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Informa la selección sin escribir artefactos")
    arguments = parser.parse_args()
    if arguments.pages_per_chunk < 1:
        raise SystemExit("--pages-per-chunk debe ser positivo")
    if not arguments.pdf.is_file():
        raise SystemExit(f"PDF inexistente: {arguments.pdf}")
    if not arguments.dry_run and arguments.output_dir.exists() and any(arguments.output_dir.iterdir()):
        if not arguments.overwrite:
            raise SystemExit(f"Directorio no vacío: {arguments.output_dir}; use --overwrite para reemplazarlo")
        shutil.rmtree(arguments.output_dir)
    if not arguments.dry_run:
        arguments.output_dir.mkdir(parents=True, exist_ok=True)

    candidates = []
    extracted = {}
    extraction_metadata = {}
    for name, extractor in EXTRACTORS.items():
        try:
            if name == "pymupdf":
                pages, layout = extract_pymupdf_with_layout(arguments.pdf)
                extraction_metadata[name] = layout
            else:
                pages = extractor(arguments.pdf)
            extracted[name] = pages
            candidate = {"extractor": name, "page_count": len(pages), "quality": assess(pages)}
            if name in extraction_metadata:
                candidate["layout"] = extraction_metadata[name]
            candidates.append(candidate)
        except Exception as error:
            candidates.append({"extractor": name, "error": f"{type(error).__name__}: {error}"})
    usable = [candidate for candidate in candidates if candidate.get("quality", {}).get("usable")]
    layout_candidate = next(
        (
            candidate
            for candidate in usable
            if candidate["extractor"] == "pymupdf"
            and candidate.get("layout", {}).get("two_column_pages", 0) > 0
        ),
        None,
    )
    # Basta una página con columnas para que un tramo lineal pueda entrelazar
    # encabezados, evidencias y listas. PyMuPDF conserva el orden espacial por
    # página también en documentos ``mixed``; la fidelidad prevalece al score.
    best = layout_candidate or max(
        usable or [candidate for candidate in candidates if "quality" in candidate],
        key=lambda item: item["quality"]["score"],
        default=None,
    )
    report = {
        "source_pdf": str(arguments.pdf),
        "candidates": candidates,
        "selected_extractor": best["extractor"] if best else None,
        "requires_visual_or_ocr": not bool(best and best["quality"]["usable"]),
        "selection_rule": "pymupdf_layout_priority_for_any_two_column_page" if layout_candidate else "highest_usable_score",
        "layout_diagnostic": pymupdf_layout_diagnostic(candidates),
        "layout_extraction_applied": bool(best and best["extractor"] == "pymupdf"),
    }
    if best and best["extractor"] in extraction_metadata:
        report["selected_layout"] = extraction_metadata[best["extractor"]]
    if not arguments.dry_run:
        write_json(arguments.output_dir / "preflight.json", report)
    if not best or not best["quality"]["usable"]:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        print("Ninguna extracción local es utilizable; escale a lectura visual u OCR.", file=sys.stderr)
        return 2

    manifest = {
        "source_pdf": str(arguments.pdf),
        "extractor": best["extractor"],
        "page_count": len(extracted[best["extractor"]]),
        "pages_per_chunk": arguments.pages_per_chunk,
        "quality": best["quality"],
        # The diagnosis is always spatial (PyMuPDF), while this explicit flag
        # prevents confusing a pypdf/pdfplumber source with layout-aware chunks.
        "layout": report["layout_diagnostic"],
        "layout_extraction_applied": report["layout_extraction_applied"],
        "layout_diagnostic_extractor": "pymupdf",
        "chunks": [],
    }
    if not arguments.dry_run:
        write_chunks(arguments.output_dir, extracted[best["extractor"]], arguments.pages_per_chunk, manifest)
        write_json(arguments.output_dir / "manifest.json", manifest)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
