"""Ronda 8: limpia front/back-matter de resumen_secciones en los JSON del piloto.

Quita filas cuyo título matchea bibliografía, acrónimos/glosario, prólogo,
prefacio o mensajes institucionales/clave. Opera in-place, recursive sobre
subsecciones. No toca anexos (excepción histórica doc11) ni resumen_enriquecido /
interpelacion / tipología.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

PILOT = Path(__file__).resolve().parent.parent / "pilot"

# Título completo (anclado al inicio). Cubre es/en y variantes frecuentes del corpus CEPAL.
SECCION_EXCLUIDA = re.compile(
    r"^(?:"
    r"bibliograf[ií]a|bibliography|referencias?(?:\s+bibliogr[aá]ficas?)?|references?|"
    r"acr[oó]nimos?|acronyms?|list\s+of\s+acronyms|glosario|glossary|"
    r"pr[oó]logo|prologue|prefacio|preface|"
    r"mensajes?(?:\s+(?:del|de\s+la|clave|institucional|principal(?:es)?))?|"
    r"(?:key\s+)?messages?(?:\s+from)?|"
    r"message\s+from"
    r")\b",
    re.I,
)


def clasificar(title: str) -> str:
    t = title.lower()
    if re.search(r"bibliograf|bibliograph|referencia|reference", t):
        return "bibliografia"
    if re.search(r"acr[oó]nim|acronym|glosario|glossary", t):
        return "acronimos"
    if re.search(r"pr[oó]logo|prologue", t):
        return "prologo"
    if re.search(r"prefacio|preface", t):
        return "prefacio"
    if re.search(r"mensaje|message", t):
        return "mensajes"
    return "otro"


def filtrar(secs: list, removidas: list, doc: str, path: str = "") -> list:
    kept = []
    for s in secs:
        title = (s.get("seccion") or "").strip()
        p = f"{path}/{title}" if path else title
        if SECCION_EXCLUIDA.search(title):
            n_dims = len(s.get("dimensiones") or [])
            n_sub = len(s.get("subsecciones") or [])
            removidas.append(
                {
                    "doc": doc,
                    "titulo": title,
                    "tipo": clasificar(title),
                    "nivel": s.get("nivel"),
                    "paginas": s.get("paginas"),
                    "n_dims": n_dims,
                    "n_sub": n_sub,
                    "path": p,
                }
            )
            continue
        if s.get("subsecciones"):
            s = dict(s)
            s["subsecciones"] = filtrar(s["subsecciones"], removidas, doc, p)
        kept.append(s)
    return kept


def main() -> None:
    files = sorted(
        f for f in PILOT.glob("doc*.json") if not re.search(r"_0[1-5]\.json$", f.name)
    )
    removidas: list[dict] = []
    tocados = 0
    for f in files:
        j = json.loads(f.read_text(encoding="utf-8"))
        antes = len(removidas)
        j["resumen_secciones"] = filtrar(j["resumen_secciones"], removidas, f.name)
        if len(removidas) > antes:
            f.write_text(
                json.dumps(j, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            tocados += 1

    print(f"Archivos modificados: {tocados}")
    print(f"Secciones removidas: {len(removidas)}")
    by_tipo: dict[str, int] = {}
    for r in removidas:
        by_tipo[r["tipo"]] = by_tipo.get(r["tipo"], 0) + 1
        print(
            f"  - {r['doc']}: [{r['tipo']}] nivel={r['nivel']} "
            f"pp={r['paginas']} dims={r['n_dims']} :: {r['titulo']}"
        )
    print("Por tipo:", by_tipo)


if __name__ == "__main__":
    main()
