"""Extracción de texto PDF consciente de columnas para documentos CEPAL."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class TextBlock:
    x0: float
    y0: float
    x1: float
    y1: float
    text: str


def _blocks(page: Any) -> list[TextBlock]:
    """Devuelve únicamente bloques de texto no vacíos de una página PyMuPDF."""
    result = []
    for block in page.get_text("blocks"):
        if len(block) < 7 or block[6] != 0 or not block[4].strip():
            continue
        result.append(TextBlock(float(block[0]), float(block[1]), float(block[2]), float(block[3]), block[4].strip()))
    return result


def _ordered(blocks: Iterable[TextBlock]) -> list[TextBlock]:
    return sorted(blocks, key=lambda block: (block.y0, block.x0))


def _is_full_width(block: TextBlock, width: float) -> bool:
    return block.x0 <= width * 0.08 and block.x1 >= width * 0.92


def order_page_blocks(blocks: list[TextBlock], width: float, height: float) -> tuple[list[TextBlock], dict[str, Any]]:
    """Ordena bloques en lectura natural y devuelve diagnóstico de layout.

    Los bloques de ancho completo se mantienen en su posición vertical. En una página
    de dos columnas, primero se recorre la columna izquierda y luego la derecha dentro
    de cada franja separada por un bloque de ancho completo.
    """
    if not blocks:
        return [], {"layout": "empty", "has_left_column": False, "has_right_column": False}

    headers = _ordered([block for block in blocks if block.y1 <= 110])
    footers = _ordered([block for block in blocks if block.y0 >= height - 60])
    body = [block for block in blocks if block not in headers and block not in footers]
    full_width = _ordered([block for block in body if _is_full_width(block, width)])
    body_without_full = [block for block in body if block not in full_width]
    midpoint = width / 2.0
    left = [block for block in body_without_full if block.x1 <= midpoint]
    right = [block for block in body_without_full if block.x0 >= midpoint]
    has_two_columns = bool(left and right)

    if not has_two_columns:
        ordered_body = _ordered(body)
    elif not full_width:
        ordered_body = _ordered(left) + _ordered(right)
    else:
        ordered_body = []
        cursor = 110.0
        for separator in full_width:
            ordered_body.extend(_ordered(block for block in left if cursor <= block.y0 < separator.y0))
            ordered_body.extend(_ordered(block for block in right if cursor <= block.y0 < separator.y0))
            ordered_body.append(separator)
            cursor = separator.y1
        ordered_body.extend(_ordered(block for block in left if block.y0 >= cursor))
        ordered_body.extend(_ordered(block for block in right if block.y0 >= cursor))

    ordered = headers + ordered_body + footers
    return ordered, {
        "layout": "two_column" if has_two_columns else "single_column",
        "has_left_column": bool(left),
        "has_right_column": bool(right),
        "body_blocks": len(body),
        "full_width_blocks": len(full_width),
    }


def extract_page_layout_aware(page: Any) -> tuple[str, dict[str, Any]]:
    blocks = _blocks(page)
    ordered, metadata = order_page_blocks(blocks, float(page.rect.width), float(page.rect.height))
    return "\n\n".join(block.text for block in ordered), metadata


def extract_document_layout_aware(document: Any) -> tuple[list[str], dict[str, Any]]:
    pages: list[str] = []
    page_layouts: list[dict[str, Any]] = []
    for index in range(len(document)):
        text, metadata = extract_page_layout_aware(document.load_page(index))
        pages.append(text)
        page_layouts.append(metadata)
    two_column_pages = sum(item.get("layout") == "two_column" for item in page_layouts)
    page_count = len(page_layouts)
    ratio = two_column_pages / max(1, page_count)
    document_layout = "two_column" if ratio > 0.5 else ("mixed" if two_column_pages else "single_column")
    return pages, {
        "layout": document_layout,
        "pages_analyzed": page_count,
        "two_column_pages": two_column_pages,
        "two_column_ratio": round(ratio, 6),
        "detection_threshold": 0.5,
        "method": "pymupdf_text_blocks_spatial_order",
        "pages": page_layouts,
    }
