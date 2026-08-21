"""Extrae un PDF en tramos paginados para análisis de documentos largos."""

import argparse
import json
import shutil
import sys
import unicodedata
from pathlib import Path

from layout_extraction import extract_document_layout_aware


def quality(text: str) -> dict[str, int | float | bool]:
    controls = sum(
        unicodedata.category(character).startswith("C") and character not in "\n\r\t"
        for character in text
    )
    return {
        "characters": len(text.strip()),
        "control_characters": controls,
        "control_ratio": round(controls / max(1, len(text)), 6),
        "usable": len(text.strip()) >= 5_000 and controls / max(1, len(text)) <= 0.02,
    }


def write_json(path: Path, content: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--pages-per-chunk", type=int, default=25)
    parser.add_argument("--overwrite", action="store_true")
    arguments = parser.parse_args()

    if arguments.pages_per_chunk < 1:
        raise SystemExit("--pages-per-chunk debe ser positivo")
    if not arguments.pdf.is_file():
        raise SystemExit(f"PDF inexistente: {arguments.pdf}")
    if arguments.output_dir.exists() and any(arguments.output_dir.iterdir()):
        if not arguments.overwrite:
            raise SystemExit(f"Directorio no vacío: {arguments.output_dir}; use --overwrite si desea reemplazarlo")
        shutil.rmtree(arguments.output_dir)
    arguments.output_dir.mkdir(parents=True, exist_ok=True)

    try:
        import fitz
    except ImportError as error:
        raise SystemExit("Este preparador requiere PyMuPDF") from error

    document = fitz.open(arguments.pdf)
    try:
        pages, layout = extract_document_layout_aware(document)
    finally:
        document.close()
    full_text = "\n".join(pages)
    manifest = {
        "source_pdf": str(arguments.pdf),
        "page_count": len(pages),
        "pages_per_chunk": arguments.pages_per_chunk,
        "quality": quality(full_text),
        "extractor": "pymupdf",
        "layout": layout,
        "chunks": [],
    }
    for start in range(0, len(pages), arguments.pages_per_chunk):
        end = min(start + arguments.pages_per_chunk, len(pages))
        chunk_path = arguments.output_dir / f"tramo_{start + 1:03d}_{end:03d}.txt"
        content = "\n\n".join(
            f"=== PÁGINA PDF {page_number} ===\n{pages[page_number - 1]}"
            for page_number in range(start + 1, end + 1)
        ) + "\n"
        temporary = chunk_path.with_suffix(".txt.tmp")
        temporary.write_text(content, encoding="utf-8")
        temporary.replace(chunk_path)
        manifest["chunks"].append(
            {
                "pages": f"{start + 1}-{end}",
                "path": chunk_path.name,
                "quality": quality(content),
            }
        )
    write_json(arguments.output_dir / "manifest.json", manifest)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    if not manifest["quality"]["usable"]:
        print("La extracción del PDF no es utilizable; use OCR o lectura nativa del harness.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
