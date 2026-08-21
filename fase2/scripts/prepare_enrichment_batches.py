#!/usr/bin/env python3
"""Prepare isolated Codex prompts and PowerShell launchers for the requested batches."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "PROMPT_ENRIQUECIMIENTO_UNIDAD.md"
DOC_ROOT = ROOT / "corpus" / "intermedios" / "11362"
BATCHES = [
    ["90001", "48304", "89934", "86527"],
    ["41173", "89932", "89774", "40159"],
    ["81405", "43415", "46682", "69132"],
    ["48823", "44551", "46227", "43442"],
]


def manifest_for(doc: Path) -> Path:
    p = doc / "tramos" / "manifest.json"
    return p if p.exists() else doc / "tramos_endpoint" / "manifest.json"


def source_rule(prep: str) -> str:
    for line in prep.splitlines():
        if line.startswith("- **Tipo**:"):
            kind = line.split(":", 1)[1].strip().strip("`")
            if kind == "endpoint_apto":
                return "Usa exclusivamente `corpus/intermedios/11362/<ID>/tramos_endpoint/` (endpoint TEXT apto)."
            return "Usa exclusivamente `corpus/intermedios/11362/<ID>/tramos/` (tramos PDF/PyMuPDF preparados)."
    raise ValueError("No se encontró Tipo en PREPARACION_FUENTE.md")


def make_prompt(doc_id: str, pages: int, prep: str, base: str) -> str:
    effort = "medium" if pages <= 100 else "xhigh"
    extra = ""
    if pages > 100:
        extra = """
## Control reforzado por extensión

Este documento tiene más de 100 páginas. Fija primero el índice y trabaja en parciales
contiguos, sin solapamientos ni huecos, seguidos por una consolidación separada. Revisa
reforzadamente índice, jerarquía literal completa, rangos/páginas y citas literales. Ejecuta
la cobertura completa y genera `matriz_cobertura.json` cuando corresponda. La consolidación
y cualquier reparación deben usar el esfuerzo xhigh.
"""
    return f"""# Misión aislada de enriquecimiento — 11362/{doc_id}

ID exclusivo: `11362/{doc_id}`
Páginas del manifest/preparación: {pages}
Modelo obligatorio: `gpt-5.6-luna`
Esfuerzo obligatorio: `{effort}` (`-c model_reasoning_effort={effort}`)

{source_rule(prep)}

Prohibido procesar otros IDs, leer o usar fuentes de otros documentos, descargar archivos,
regenerar OCR o tramos, ejecutar o modificar `pipeline/ledger.py`, modificar el ledger,
escribir en `corpus/resultados/`, promocionar documentos o escribir el registro global.
No uses una fuente distinta de la declarada arriba y en PREPARACION_FUENTE.md.

Lee íntegramente y aplica acumulativamente el contenido de PROMPT_ENRIQUECIMIENTO_UNIDAD.md
que se reproduce a continuación. Debes respetar jerarquía literal completa, citas literales
completas verificadas en la página declarada y las validaciones finales. Si una compuerta falla,
corrige antes de declarar terminado y vuelve a ejecutar la ronda completa.

## PREPARACION_FUENTE.md (lectura obligatoria)

```text
{prep}
```

{extra}

## PROMPT_ENRIQUECIMIENTO_UNIDAD.md (instrucciones íntegras)

{base}

## Cierre obligatorio

Trabaja solamente en `corpus/intermedios/11362/{doc_id}/` y responde solo con el resumen final
y rutas generadas. Deja `EJECUCION_ENRIQUECIMIENTO.md` actualizado allí. No modifiques ledger
ni `corpus/resultados/` bajo ninguna circunstancia.
"""


def launcher(batch_no: int, ids: list[str], metadata: dict[str, tuple[int, str]]) -> str:
    lines = [
        "$repoWin = $PSScriptRoot",
        'if ([string]::IsNullOrWhiteSpace($repoWin)) { throw "No se pudo resolver la ruta Windows del repositorio." }',
        "$repoWinForWsl = $repoWin -replace '\\\\','/'",
        "$repoWsl = (wsl.exe -d Ubuntu -- wslpath -a $repoWinForWsl).Trim()",
        'if ([string]::IsNullOrWhiteSpace($repoWsl)) { throw "wslpath devolvió una ruta WSL vacía para: $repoWin" }',
    ]
    for doc_id in ids:
        pages, effort = metadata[doc_id]
        lines += [
            f"$id = '{doc_id}'",
            "$model = 'gpt-5.6-luna'",
            f"$reasoningEffort = '{effort}'",
            f'$promptWsl = "$repoWsl/temp_prompt_{doc_id}.md"',
            '$wslCommand = "export PATH=/home/abustamante/.nvm/versions/node/v24.14.0/bin:/usr/bin:/bin; cd \'$repoWsl\' && cat \'$promptWsl\' | /home/abustamante/.nvm/versions/node/v24.14.0/bin/codex exec --model $model -c model_reasoning_effort=$reasoningEffort --dangerously-bypass-approvals-and-sandbox -C \'$repoWsl\' -"',
            '$childCommand = "wsl.exe -d Ubuntu -- bash -lc `"$wslCommand`""',
            '$encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($childCommand))',
            "Start-Process powershell.exe -ArgumentList '-NoExit','-NoProfile','-EncodedCommand',$encoded",
            'Start-Sleep -Seconds 1',
        ]
    return "\n".join(lines) + "\n"


def main() -> None:
    base = BASE.read_text(encoding="utf-8")
    metadata: dict[str, tuple[int, str]] = {}
    for batch in BATCHES:
        for doc_id in batch:
            doc = DOC_ROOT / doc_id
            prep_path = doc / "PREPARACION_FUENTE.md"
            prep = prep_path.read_text(encoding="utf-8")
            manifest = json.loads(manifest_for(doc).read_text(encoding="utf-8"))
            pages = int(manifest["page_count"])
            effort = "medium" if pages <= 100 else "xhigh"
            metadata[doc_id] = (pages, effort)
            (ROOT / f"temp_prompt_{doc_id}.md").write_text(make_prompt(doc_id, pages, prep, base), encoding="utf-8")
    for n, batch in enumerate(BATCHES, 1):
        # Keep the launcher at repository root so $PSScriptRoot is the repository,
        # not the scripts subdirectory.
        (ROOT / f"launch_batch_{n}.ps1").write_text(launcher(n, batch, metadata), encoding="utf-8")
    print(json.dumps({k: {"pages": v[0], "effort": v[1]} for k, v in metadata.items()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
