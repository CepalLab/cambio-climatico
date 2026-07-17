"""Adjudicación Ronda 9: aplica reglas definitivas y corrige JSON del ejecutor."""
from __future__ import annotations

import json
import shutil
from copy import deepcopy
from pathlib import Path

PILOT = Path(__file__).resolve().parents[1] / "pilot"
REV = PILOT / "revision"

# adjudicacion: "ejecutor" | "revisor" | "regla" (falla sistemática → regla nueva, ganador indicado)
# ganador: quién tiene el veredicto correcto tras Ronda 9
ADJ = {
    # (doc, campo) -> (ganador, nota corta)
    (1, "articulacion_actores"): (
        "revisor",
        "R9 §1.2: ERECC/C3A son producción del estudio, no gobernanza de acción climática → No",
    ),
    (2, "gran_impulso_ambiental_concreto"): (
        "revisor",
        "R9 umbral: tesis sin paquete de inversión coordinado → No (no Parcial por lenguaje de transformación)",
    ),
    (2, "como_hacerlo_concreto"): (
        "revisor",
        "R9 §1.4: cierre sin lista operativa; sentencias en tesis no son sección de recomendaciones → No",
    ),
    (2, "transformacion_secundaria"): (
        "ejecutor",
        "R9 tipología: secundaria #2 desigualdad ancla mejor el hilo distributivo de las tesis que #1",
    ),
    (3, "oportunidades_productivas_sostenibles"): (
        "revisor",
        "R9 §1.3: enumera sectores (a) sin vínculo empleo desarrollado (b) → Parcial, no No",
    ),
    (3, "como_hacerlo_concreto"): (
        "revisor",
        "R9 §1.4: Conclusion pp.41-42 es la unidad; mayoría de ítems concretos → Sí",
    ),
    (4, "gran_impulso_ambiental_concreto"): (
        "ejecutor",
        "R9 §1.5/1.6: estudio de impactos/costos; mención de gran impulso sin paquete propio → No",
    ),
    (4, "oportunidades_productivas_sostenibles"): (
        "revisor",
        "R9 §1.3: sectores aparecen como vulnerabilidad/adaptación, no como oportunidad productiva de transición → No",
    ),
    (4, "como_hacerlo_concreto"): (
        "revisor",
        "R9 §1.4: unidad = Conclusiones 208-212 (no recuadros intercalados); 9/13 → Sí",
    ),
    (4, "transformacion_secundaria"): (
        "ejecutor",
        "R9 tipología: secundaria #11 (capacidades) encaja con ECC CA como estudio técnico de política; #2 no es el hilo",
    ),
    (6, "gran_impulso_ambiental_concreto"): (
        "ejecutor",
        "R9 §1.5: advierte contra lógica de promoción de inversiones; sin paquete Big Push → No",
    ),
    (6, "transformacion_secundaria"): (
        "ejecutor",
        "R9 tipología: secundaria #11 (Estado/gobernanza) frente a #1; el libro no prioriza desarrollo productivo",
    ),
    (8, "articulacion_actores"): (
        "revisor",
        "R9 §1.2: COIRCO/Pilcomayo/Titicaca/CNRH en ámbito = Sí (gobernanza, no autoría)",
    ),
    (8, "oportunidades_productivas_sostenibles"): (
        "revisor",
        "R9 §1.3: enumera sectores del agua + vínculo productividad débil → Parcial",
    ),
    (8, "como_hacerlo_concreto"): (
        "revisor",
        "R9 §1.4: unidad = C1 Conclusiones y recomendaciones (286-294) completa; 15/21 → Sí",
    ),
    (8, "transformacion_primaria"): (
        "ejecutor",
        "R9 tipología objeto/instrumento: gobernanza hídrica → #11 primaria / #6 secundaria",
    ),
    (8, "transformacion_secundaria"): (
        "ejecutor",
        "R9 tipología: #6 secundaria (clima/ambiente como restricción del recurso)",
    ),
    (10, "transformacion_secundaria"): (
        "ejecutor",
        "R9 tipología: secundaria #11 (capacidades/implementación Agenda 2030) mejor que #1",
    ),
    (11, "como_hacerlo_concreto"): (
        "revisor",
        "R9 §1.4: cap.4 recomendaciones; mayoría pasa test (regla Sí = mayoría) → Sí",
    ),
    (12, "oportunidades_productivas_sostenibles"): (
        "ejecutor",
        "R9 §1.3: enumeración + NAMA Café con cifra de empleo → Sí",
    ),
    (12, "como_hacerlo_concreto"): (
        "revisor",
        "R9 §1.4: Plan ABC/lecciones de casos ≠ recomendaciones del documento → No",
    ),
    (12, "transformacion_primaria"): (
        "ejecutor",
        "R9 tipología: inventario institucional PLACA → #11/#6",
    ),
    (12, "transformacion_secundaria"): (
        "ejecutor",
        "R9 tipología: #6 secundaria (acción climática agropecuaria como contenido de los instrumentos)",
    ),
    (13, "como_hacerlo_concreto"): (
        "ejecutor",
        "R9 §1.4 / ancla Ronda 2: 4/8 no es mayoría → Parcial (no subir a Sí por re-conteo)",
    ),
    (14, "oportunidades_productivas_sostenibles"): (
        "revisor",
        "R9 §1.3: portafolio + cifras de empleo (economía circular 8,8 M) → Sí",
    ),
    (14, "transformacion_primaria"): (
        "revisor",
        "R9 tipología: trampas de desarrollo; objeto = transformación productiva (#1), clima como eje de trampas → #1 primaria",
    ),
    (15, "articulacion_actores"): (
        "ejecutor",
        "R9 §1.2: SICA + ECC Centroamérica en ámbito del cap. III → Sí (mecanismo vigente, no solo propuesta)",
    ),
    (15, "como_hacerlo_concreto"): (
        "revisor",
        "R9 §1.4: Cap.VII sin lista; Recuadro II.2 no es unidad de cierre → No",
    ),
    (15, "transformacion_secundaria"): (
        "ejecutor",
        "R9 tipología: secundaria #10 (macro/fiscal, matriz público-privada/precios) mejor que #2 genérica",
    ),
    (16, "como_hacerlo_concreto"): (
        "revisor",
        "R9 §1.4: Reflexiones finales sin lista operativa; desafíos de capítulos ≠ unidad de cierre → No",
    ),
    (18, "oportunidades_productivas_sostenibles"): (
        "revisor",
        "R9 §1.3: sectores transformadores + vínculo inversión/empleo desarrollado → Sí",
    ),
    (18, "como_hacerlo_concreto"): (
        "revisor",
        "R9 §1.4: Cap.III Recomendaciones A–D es la unidad; 4/4 concretos → Sí",
    ),
    (19, "gran_impulso_ambiental_concreto"): (
        "revisor",
        "R9 §1.5: paquetes de inversión + sectores estratégicos nombrados a escala de modelo → Sí",
    ),
    (19, "oportunidades_productivas_sostenibles"): (
        "revisor",
        "R9 §1.3: sectores dinamizadores + vínculo infraestructura/empleo → Sí",
    ),
    (19, "como_hacerlo_concreto"): (
        "ejecutor",
        "R9 §1.4: unidad no puede ser Intro B; lista de desafíos III mayoritariamente genérica → No",
    ),
}


def find_ejecutor(num: int) -> Path:
    matches = [
        p
        for p in PILOT.glob(f"doc{num:02d}_*.json")
        if "_0" not in p.name and p.parent == PILOT
    ]
    if len(matches) != 1:
        raise FileNotFoundError(f"doc{num:02d}: {matches}")
    return matches[0]


def apply_interpelacion(ej: dict, rev: dict, campo: str) -> None:
    ej["interpelacion"][campo] = deepcopy(rev["interpelacion"][campo])
    # conservar nota si el revisor no trae y el ejecutor sí (opcional)
    if "nota" not in ej["interpelacion"][campo]:
        ej["interpelacion"][campo]["nota"] = (
            f"Corregido en adjudicación Ronda 9 (2026-07-16) según revisor ciego."
        )
    else:
        prev = ej["interpelacion"][campo].get("nota")
        suffix = " [Ronda 9: veredicto alineado al revisor ciego / regla de unidad o mecanismo.]"
        if prev:
            if "Ronda 9" not in str(prev):
                ej["interpelacion"][campo]["nota"] = str(prev) + suffix
        else:
            ej["interpelacion"][campo]["nota"] = suffix.strip()


def apply_tipologia(ej: dict, rev: dict, campo: str) -> None:
    key = campo  # transformacion_primaria | transformacion_secundaria
    ej["tipologia"][key] = deepcopy(rev["tipologia"][key])
    # si cambia primaria en doc14, actualizar justificación breve si existe en revisor
    if campo == "transformacion_primaria" and "justificacion_breve" in rev.get("tipologia", {}):
        # mantener razonamiento_5_pasos pero marcar ambigüedad
        tip = ej["tipologia"]
        tip["ambiguedad_pendiente_validacion"] = (
            "Ronda 9 adjudicación: primaria alineada al revisor (#1 Desarrollo productivo). "
            "Justificación revisor: "
            + rev["tipologia"].get("justificacion_breve", "")[:500]
        )


def _group_by_doc() -> dict[int, list[tuple[str, str, str]]]:
    by_doc: dict[int, list[tuple[str, str, str]]] = {}
    for (num, campo), (ganador, nota) in ADJ.items():
        by_doc.setdefault(num, []).append((campo, ganador, nota))
    return by_doc


def _apply_doc(num: int, items: list[tuple[str, str, str]]) -> tuple[list[str], bool]:
    """Devuelve filas de tabla markdown y si el JSON del ejecutor cambió."""
    path = find_ejecutor(num)
    rev_path = REV / f"doc{num:02d}_revision.json"
    ej = json.loads(path.read_text(encoding="utf-8"))
    rev = json.loads(rev_path.read_text(encoding="utf-8"))
    rows: list[str] = []
    file_changed = False

    for campo, ganador, nota in items:
        accion = "sin cambio"
        if ganador == "revisor":
            if campo.startswith("transformacion_"):
                apply_tipologia(ej, rev, campo)
            else:
                apply_interpelacion(ej, rev, campo)
            accion = "corregido ← revisor"
            file_changed = True
        rows.append(f"| | doc{num:02d} | `{campo}` | {ganador} | {nota} | {accion} |")

    if file_changed:
        bak = path.with_suffix(path.suffix + ".pre_ronda9.bak")
        if not bak.exists():
            shutil.copy2(path, bak)
        path.write_text(
            json.dumps(ej, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return rows, file_changed


def main() -> None:
    changed_files: list[str] = []
    report_lines = [
        "# Adjudicación Ronda 9 (2026-07-16)",
        "",
        "Juez: calibración Lab (dominio + casos del piloto), sin esperar al equipo del curso.",
        "Reglas nuevas en INTERPELACION_v0.md §1.2/§1.4 y TIPOLOGIA_v0.md §2/§3.",
        "",
        "| # | Documento | Campo | Ganador | Nota | Acción JSON |",
        "|---|-----------|-------|---------|------|-------------|",
    ]

    for num, items in sorted(_group_by_doc().items()):
        rows, changed = _apply_doc(num, items)
        report_lines.extend(rows)
        if changed:
            path = find_ejecutor(num)
            changed_files.append(str(path.relative_to(PILOT.parent)))

    report_lines.extend(["", "## Archivos del ejecutor modificados", ""])
    report_lines.extend(f"- `{f}`" for f in changed_files)
    out = REV / "ADJUDICACION_RONDA9.md"
    out.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print(f"OK: {len(changed_files)} archivos corregidos. Reporte: {out}")


if __name__ == "__main__":
    main()
