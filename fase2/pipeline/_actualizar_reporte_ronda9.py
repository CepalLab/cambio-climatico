"""Rellena adjudicaciones en REPORTE_COMPARACION.md (post comparar_revision)."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "pilot" / "revision" / "REPORTE_COMPARACION.md"

spec = importlib.util.spec_from_file_location(
    "adj", Path(__file__).parent / "_adjudicar_ronda9.py"
)
adj = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adj)

text = REPORT.read_text(encoding="utf-8")
lines = text.splitlines(keepends=True)
out: list[str] = []
i = 0
header_re = re.compile(
    r"^### \d+\. doc(\d+) — (?:interpelación|tipología) \(([^)]+)\)\s*$"
)
current_key: tuple[int, str] | None = None
patched = 0

while i < len(lines):
    line = lines[i]
    m = header_re.match(line.rstrip("\n"))
    if m:
        current_key = (int(m.group(1)), m.group(2).strip())
        out.append(line)
        i += 1
        continue
    if line.startswith("- **Adjudicación**:") and current_key is not None:
        if current_key in adj.ADJ:
            ganador, nota = adj.ADJ[current_key]
            out.append(f"- **Adjudicación**: **{ganador}** — {nota}\n")
            patched += 1
        else:
            out.append(line)
        current_key = None
        i += 1
        continue
    out.append(line)
    i += 1

new_text = "".join(out)

rev_wins = sum(1 for v in adj.ADJ.values() if v[0] == "revisor")
ej_wins = sum(1 for v in adj.ADJ.values() if v[0] == "ejecutor")
summary = f"""## Adjudicación Ronda 9 (2026-07-16)

De las **35** discrepancias originales: **{rev_wins}** a favor del revisor (JSON del ejecutor corregido), **{ej_wins}** a favor del ejecutor (veredicto canónico = ejecutor).

- Acuerdo bruto inicial ejecutor↔revisor: **67/102 (66%)**.
- Acuerdo tras corregir el ejecutor según Ronda 9: **{67 + rev_wins}/102 ({round(100 * (67 + rev_wins) / 102)}%)** (coincide con la tasa que reporta `comparar_revision.py` sobre los JSON ya corregidos).

Las discrepancias listadas abajo son las **{ej_wins}** que permanecen (Lab confirmó al ejecutor). Detalle completo: [ADJUDICACION_RONDA9.md](ADJUDICACION_RONDA9.md). Reglas: [INTERPELACION_v0.md](../../INTERPELACION_v0.md) v0.5, [TIPOLOGIA_v0.md](../../TIPOLOGIA_v0.md) v0.1.

"""

if "## Adjudicación Ronda 9" not in new_text:
    new_text = new_text.replace(
        "## Discrepancias para adjudicar\n",
        summary + "## Discrepancias residuales (ejecutor confirmado)\n",
    )
else:
    new_text = new_text.replace(
        "## Discrepancias para adjudicar\n",
        "## Discrepancias residuales (ejecutor confirmado)\n",
    )

REPORT.write_text(new_text, encoding="utf-8")
pending = new_text.count("_(pendiente:")
print(f"Parches: {patched}; pendientes: {pending}")
