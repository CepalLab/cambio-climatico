"""Cribado semántico de dimensiones: genera candidatos para revisión humana."""

import argparse
import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DEFAULT_INVENTORY = Path(__file__).resolve().parent / "inventario_corpus_v1.json"
DEFAULT_EXCLUSIONS = Path(__file__).resolve().parent / "exclusiones_corpus_v1.csv"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "auditoria_dimensiones_v1.json"

# Marcadores de incompatibilidad explícita: producen candidatos, no veredictos.
# No se marca la ausencia de un marcador, porque una cita válida puede ser nominal,
# elíptica o depender del contexto del apartado.
RULES = {
    "avances_implementacion": re.compile(
        r"\b(?:se recomienda|se propone|deber[ií]a|deben|podr[ií]a|"
        r"se espera|ser[aá]|ser[ií]a|deber[aá]n|es necesario)\b",
        re.I,
    ),
    "propuestas_politica": re.compile(
        r"\b(?:se observa|se observan|describe|presenta|analiza|reporta|"
        r"exist[ií]a|existe|ha aumentado|ha disminuido|se registr[oó])\b",
        re.I,
    ),
    "tendencias": re.compile(
        r"\b(?:se recomienda|se propone|deber[ií]a|deben|es necesario|"
        r"fondo|ley|impuesto|regulaci[oó]n)\b",
        re.I,
    ),
    "brechas_implementacion": re.compile(
        r"\b(?:logr[oó]|implement[oó]|aplic[oó]|ejecut[oó]|se ha logrado|"
        r"ya se (?:implement[oó]|aplic[oó])|resultado positivo|éxito)\b",
        re.I,
    ),
    "oportunidades": re.compile(
        r"\b(?:brecha|insuficien|carencia|ausencia|falta|d[eé]bil|limitaci[oó]n|"
        r"no cuenta|no existe|obst[aá]culo|incumpl|rezago)\b",
        re.I,
    ),
    "diagnostico_estructural": re.compile(
        r"\b(?:se recomienda|se propone|deber[ií]a|deben|podr[ií]a|"
        r"fondo|ley|impuesto|regulaci[oó]n)\b",
        re.I,
    ),
}

REASONS = {
    "avances_implementacion": "La cita contiene lenguaje prescriptivo, futuro o condicional, incompatible potencialmente con una acción ya implementada.",
    "propuestas_politica": "La cita contiene lenguaje descriptivo o reportativo, sin una propuesta o instrumento explícito.",
    "tendencias": "La cita contiene lenguaje normativo o de instrumento, sin describir necesariamente una evolución temporal.",
    "brechas_implementacion": "La cita contiene lenguaje de logro o implementación, potencialmente incompatible con una brecha.",
    "oportunidades": "La cita contiene lenguaje de carencia, limitación u obstáculo, potencialmente incompatible con una oportunidad.",
    "diagnostico_estructural": "La cita contiene lenguaje prescriptivo o de instrumento, sin causalidad estructural explícita.",
}


def load_exclusions(path: Path) -> set[str]:
    with path.open(encoding="utf-8-sig", newline="") as file:
        return {
            row["handle"] for row in csv.DictReader(file)
            if row.get("decision") == "excluir" and row.get("estado") == "aplicado"
        }


def walk_sections(sections: list[dict], path: str = ""):
    for section in sections:
        title = section.get("seccion") or "?"
        current = f"{path}/{title}"
        yield section, current
        yield from walk_sections(section.get("subsecciones") or [], current)


def audit(inventory_path: Path, exclusions_path: Path) -> dict:
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    exclusions = load_exclusions(exclusions_path)
    candidates = []
    total_dimensions = 0
    by_dimension = Counter()
    flagged_by_dimension = Counter()
    for record in inventory["documentos"]:
        if record["handle"] in exclusions:
            continue
        path = BASE / record["ruta_json"]
        data = json.loads(path.read_text(encoding="utf-8"))
        for section, section_path in walk_sections(data.get("resumen_secciones") or []):
            for dimension in section.get("dimensiones") or []:
                total_dimensions += 1
                slug = dimension.get("dimension")
                by_dimension[slug] += 1
                citation = dimension.get("cita") or ""
                rule = RULES.get(slug)
                match = rule.search(citation) if rule else None
                if match:
                    flagged_by_dimension[slug] += 1
                    candidates.append({
                        "handle": record["handle"],
                        "ruta_json": record["ruta_json"],
                        "seccion": section_path,
                        "paginas_seccion": section.get("paginas"),
                        "dimension": slug,
                        "cita": citation,
                        "pagina_cita": dimension.get("pagina"),
                        "motivo": REASONS[slug],
                        "marcador_detectado": match.group(0),
                        "decision": "pendiente",
                    })

    return {
        "version": "auditoria-dimensiones-v1",
        "generado_en": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "fuentes": {
            "inventario": inventory_path.relative_to(BASE).as_posix(),
            "exclusiones": exclusions_path.relative_to(BASE).as_posix(),
            "codebook": "fase2/codebook_v0.md",
        },
        "denominador": {
            "historico": len(inventory["documentos"]),
            "exclusiones_aplicadas": len(exclusions),
            "activo": len(inventory["documentos"]) - len(exclusions),
            "dimensiones_revisadas": total_dimensions,
        },
        "resultado_cribado": {
            "candidatos": len(candidates),
            "proporcion_candidatos": round(len(candidates) / total_dimensions, 4) if total_dimensions else 0,
            "advertencia": "Los candidatos requieren revisión humana; ausencia de marcador no demuestra error semántico.",
        },
        "por_dimension": {
            slug: {
                "total": by_dimension[slug],
                "candidatos": flagged_by_dimension[slug],
            }
            for slug in sorted(by_dimension)
        },
        "candidatos": candidates,
    }


def write_markdown(report: dict, path: Path) -> None:
    lines = [
        "# Auditoría semántica de dimensiones v1",
        "",
        f"Generada: `{report['generado_en']}`",
        "",
        "## Alcance",
        "",
        f"- Corpus activo: **{report['denominador']['activo']}** documentos.",
        f"- Dimensiones revisadas por cribado: **{report['denominador']['dimensiones_revisadas']}**.",
        f"- Candidatos para revisión humana: **{report['resultado_cribado']['candidatos']}**.",
        "",
        "> El cribado busca incompatibilidades explícitas derivadas del codebook. Un candidato no es un error: la decisión requiere leer la cita en contexto.",
        "",
        "## Candidatos por dimensión",
        "",
        "| Dimensión | Total | Candidatos |",
        "|---|---:|---:|",
    ]
    for slug, values in report["por_dimension"].items():
        lines.append(f"| `{slug}` | {values['total']} | {values['candidatos']} |")
    lines.extend(["", "## Candidatos", ""])
    for index, candidate in enumerate(report["candidatos"], 1):
        lines.extend([
            f"### {index}. `{candidate['handle']}` — `{candidate['dimension']}`",
            "",
            f"- Sección: `{candidate['seccion']}`",
            f"- Página: `{candidate['pagina_cita']}`",
            f"- Motivo: {candidate['motivo']}",
            f"- Marcador detectado: `{candidate['marcador_detectado']}`",
            f"- Cita: “{candidate['cita']}”",
            "- Decisión: `pendiente`",
            "",
        ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--exclusions", type=Path, default=DEFAULT_EXCLUSIONS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = audit(args.inventory, args.exclusions)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, args.output.with_suffix(".md"))
    print(json.dumps({"output": str(args.output), **report["denominador"], **report["resultado_cribado"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
