"""Escaneo rápido de longitudes de resumen_secciones en el piloto."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from statistics import median

PILOT = Path(__file__).resolve().parents[1] / "pilot"
rows: list[dict] = []


def walk(secs, doc: str, path: str = "") -> None:
    for s in secs or []:
        titulo = s.get("seccion") or s.get("titulo") or "?"
        p = f"{path}/{titulo}" if path else titulo
        res = s.get("resumen")
        n_sub = len(s.get("subsecciones") or [])
        if res is None:
            nchar = None
            kind = "null"
            preview = ""
        else:
            text = res.strip()
            nchar = len(text)
            kind = "ok"
            preview = text[:140].replace("\n", " ")
        rows.append(
            {
                "doc": doc,
                "sec": p[:90],
                "nivel": s.get("nivel"),
                "paginas": s.get("paginas"),
                "nchar": nchar,
                "n_sub": n_sub,
                "kind": kind,
                "preview": preview,
            }
        )
        walk(s.get("subsecciones") or [], doc, p)


def main() -> None:
    for path in sorted(PILOT.glob("doc*.json")):
        if "_0" in path.name:
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        walk(data.get("resumen_secciones") or [], path.stem)

    with_text = [r for r in rows if r["nchar"] is not None]
    nulls = [r for r in rows if r["kind"] == "null"]
    print(
        f"Total filas: {len(rows)} | con resumen: {len(with_text)} | resumen null: {len(nulls)}"
    )
    lens = [r["nchar"] for r in with_text]
    print(f"nchar: min={min(lens)} med={int(median(lens))} max={max(lens)}")
    for thr in (80, 150, 250, 400):
        n = sum(1 for x in lens if x < thr)
        print(f"  <{thr} chars: {n} ({100 * n / len(lens):.0f}%)")

    print("\n--- 20 mas cortos ---")
    for r in sorted(with_text, key=lambda x: x["nchar"])[:20]:
        print(
            f"{r['nchar']:4d}c  {r['doc']:28s} n{r['nivel']} p={r['paginas']} "
            f"subs={r['n_sub']} | {r['sec']}"
        )
        print(f"       {r['preview']}")

    print("\n--- docs con mas resúmenes <150 chars ---")
    short = [r for r in with_text if r["nchar"] < 150]
    tot_by = Counter(r["doc"] for r in with_text)
    for doc, n in Counter(r["doc"] for r in short).most_common(12):
        print(f"  {doc}: {n}/{tot_by[doc]} cortos")

    # null with content expected vs not
    null_leaf = [r for r in nulls if r["n_sub"] == 0]
    null_parent = [r for r in nulls if r["n_sub"] > 0]
    print(f"\nnull con subsecciones (padre OK?): {len(null_parent)}")
    print(f"null sin subsecciones (posible hueco): {len(null_leaf)}")
    for r in null_leaf[:12]:
        print(f"  HUECO {r['doc']} n{r['nivel']} p={r['paginas']} | {r['sec']}")


if __name__ == "__main__":
    main()
