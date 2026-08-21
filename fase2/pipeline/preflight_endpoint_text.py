"""Evalúa texto plano del endpoint antes de usarlo como fuente analítica."""

import argparse
import json
import sys
import unicodedata
from pathlib import Path


MOJIBAKE = ("Ã¡", "Ã©", "Ã­", "Ã³", "Ãº", "Ã±", "â€™", "â€œ", "â€", "\ufffd")
MAX_CHARS_PER_PAGE_BOUNDARY = 50_000


def assess(text: str) -> dict[str, int | float | bool | list[str]]:
    useful_length = len(text.strip())
    controls = sum(
        unicodedata.category(character).startswith("C") and character not in "\n\r\t"
        for character in text
    )
    mojibake = sum(text.count(marker) for marker in MOJIBAKE)
    near_limit = 99_000 <= useful_length <= 100_100
    reasons = []
    if useful_length < 5_000:
        reasons.append("texto_demasiado_breve")
    if controls / max(1, len(text)) > 0.02:
        reasons.append("exceso_caracteres_de_control")
    if mojibake:
        reasons.append("mojibake_o_caracteres_de_reemplazo")
    if near_limit:
        reasons.append("posible_truncamiento_limite_endpoint")
    return {
        "characters": useful_length,
        "control_characters": controls,
        "control_ratio": round(controls / max(1, len(text)), 6),
        "mojibake": mojibake,
        "near_endpoint_limit": near_limit,
        "usable": not reasons,
        "reasons": reasons,
    }


def write_json(path: Path, payload: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def write_chunks(output_dir: Path, pages: list[str], pages_per_chunk: int, source: Path, quality: dict) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "source_text": str(source),
        "extractor": "endpoint_formfeed",
        "page_count": len(pages),
        "pages_per_chunk": pages_per_chunk,
        "quality": quality,
        "chunks": [],
    }
    for start in range(0, len(pages), pages_per_chunk):
        end = min(start + pages_per_chunk, len(pages))
        chunk = output_dir / f"tramo_{start + 1:03d}_{end:03d}.txt"
        content = "\n\n".join(
            f"=== PÁGINA PDF {page_number} ===\n{pages[page_number - 1]}"
            for page_number in range(start + 1, end + 1)
        ) + "\n"
        chunk.write_text(content, encoding="utf-8")
        manifest["chunks"].append({"pages": f"{start + 1}-{end}", "path": chunk.name})
    write_json(output_dir / "manifest.json", manifest)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", type=Path, help="TXT descargado del bundle TEXT de DSpace")
    parser.add_argument("--report", type=Path, help="Ruta opcional para guardar el diagnóstico JSON")
    parser.add_argument("--output-dir", type=Path, help="Genera tramos paginados cuando el TXT usa saltos de página")
    parser.add_argument("--pages-per-chunk", type=int, default=25)
    arguments = parser.parse_args()
    try:
        content = arguments.text.read_bytes().decode("utf-8")
    except UnicodeDecodeError as error:
        report = {
            "source_text": str(arguments.text),
            "usable": False,
            "reasons": ["utf8_invalido"],
            "error": str(error),
        }
    else:
        report = {"source_text": str(arguments.text), **assess(content)}
        pages = content.split("\f")
        report["form_feeds"] = len(pages) - 1
        report["page_count"] = len(pages)
        report["characters_per_page_boundary"] = round(len(content.strip()) / max(1, len(pages)))
        report["page_boundaries_usable"] = bool(
            report["usable"]
            and len(pages) > 1
            and report["characters_per_page_boundary"] <= MAX_CHARS_PER_PAGE_BOUNDARY
        )
        report["requires_pdf_for_citations"] = bool(
            report["usable"] and not report["page_boundaries_usable"]
        )
        if report["usable"] and len(pages) > 1 and not report["page_boundaries_usable"]:
            report["page_boundary_reason"] = "saltos_de_pagina_implausibles_para_el_volumen_de_texto"
    if arguments.report:
        arguments.report.parent.mkdir(parents=True, exist_ok=True)
        write_json(arguments.report, report)
    if arguments.output_dir and report["usable"]:
        if not report.get("page_boundaries_usable"):
            raise SystemExit("El TXT es apto para lectura pero no contiene saltos de página para validar citas.")
        if arguments.pages_per_chunk < 1:
            raise SystemExit("--pages-per-chunk debe ser positivo")
        page_quality = assess("\n".join(pages))
        page_quality["pages_with_text"] = sum(bool(page.strip()) for page in pages)
        write_chunks(arguments.output_dir, pages, arguments.pages_per_chunk, arguments.text, page_quality)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["usable"] and not report.get("requires_pdf_for_citations") else 2


if __name__ == "__main__":
    sys.exit(main())
