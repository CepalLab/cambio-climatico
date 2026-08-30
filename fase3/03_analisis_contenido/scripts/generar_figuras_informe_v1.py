"""Genera figuras y cuadros del informe desde los derivados analíticos v1."""

import json
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter


ANALISIS_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ANALISIS_DIR / "salidas" / "figuras_informe_v1"
MATRIX_PATH = ANALISIS_DIR / "salidas" / "matriz_documental_candidata_v1.json"
PANELS_PATH = ANALISIS_DIR / "salidas" / "paneles_analiticos_v1.json"
PERIODS = ("P1", "P2", "P3")
COLORS = {"P1": "#4c78a8", "P2": "#59a14f", "P3": "#e15759"}
PERIOD_LABELS = {"P1": "2015–2018", "P2": "2019–2022", "P3": "2023–2026"}
OBJECT_LABELS = {
    "adaptacion": "Adaptación",
    "financiamiento_inversion": "Financiamiento e inversión",
    "gobernanza_institucionalidad": "Gobernanza e institucionalidad",
    "impactos_vulnerabilidad": "Impactos y vulnerabilidad",
    "mitigacion_transicion": "Mitigación y transición",
    "sin_asignacion": "Sin asignación",
}
MODE_LABELS = {
    "diagnostica": "Diagnóstico",
    "analiza": "Análisis",
    "prospecta": "Prospectiva",
    "evalua_implementacion": "Evalúa implementación",
    "propone_intervenir": "Propone intervención",
    "conclusiones_explicitas": "Conclusiones explícitas",
    "recomendaciones_explicitas": "Recomendaciones explícitas",
    "politica_concreta": "Política concreta",
}
CRITERION_LABELS = {
    "gran_impulso_ambiental_concreto": "Estrategia integral",
    "oportunidades_productivas_sostenibles": "Oportunidades sostenibles",
    "articulacion_actores": "Articulación de actores",
    "como_hacerlo_concreto": "Propuesta operativa",
}


def save(figure: plt.Figure, name: str) -> None:
    figure.tight_layout(pad=1.1)
    figure.savefig(OUTPUT_DIR / name, dpi=220, bbox_inches="tight")
    plt.close(figure)


def grouped_bars(axis, labels, values, ylabel="Porcentaje de documentos", ymax=1.06):
    positions = np.arange(len(labels))
    width = 0.24
    for index, period in enumerate(PERIODS):
        bars = axis.bar(positions + (index - 1) * width, values[period], width, label=PERIOD_LABELS[period], color=COLORS[period])
        axis.bar_label(bars, labels=[f"{value:.0%}" if value >= 0.06 else "" for value in values[period]], padding=2, fontsize=7)
    axis.set_xticks(positions, labels, rotation=22, ha="right")
    axis.set_ylim(0, ymax)
    axis.set_ylabel(ylabel)
    axis.yaxis.set_major_formatter(PercentFormatter(1))
    axis.grid(axis="y", alpha=0.22)
    axis.legend(frameon=False, ncols=3)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))["matrix"]
    panels = json.loads(PANELS_PATH.read_text(encoding="utf-8"))["panels"]
    denominators = Counter(row["period_id"] for row in matrix)

    objects = Counter((row["period_id"], row["candidate_assignments"]["primary_object"] or "sin_asignacion") for row in matrix)
    object_ids = sorted({object_id for _, object_id in objects})
    object_labels = [OBJECT_LABELS.get(object_id, object_id.replace("_", " ").capitalize()) for object_id in object_ids]
    object_values = {period: [objects[(period, object_id)] / denominators[period] for object_id in object_ids] for period in PERIODS}
    figure, axis = plt.subplots(figsize=(11.5, 5.6))
    grouped_bars(axis, object_labels, object_values, ymax=0.30)
    axis.text(0, -0.36, "Clasificaciones revisadas para este informe; organizan la lectura y no son una codificación definitiva.", transform=axis.transAxes, fontsize=8)
    save(figure, "figura_01_objetos_por_periodo.png")

    mode_rows = panels["analytical_modes"]
    mode_ids = ("diagnostica", "analiza", "prospecta", "evalua_implementacion", "propone_intervenir", "conclusiones_explicitas", "recomendaciones_explicitas", "politica_concreta")
    mode_values = {period: [next(row["proportion"] for row in mode_rows if row["period_id"] == period and row["mode"] == mode_id) for mode_id in mode_ids] for period in PERIODS}
    figure, axis = plt.subplots(figsize=(11.5, 5.8))
    grouped_bars(axis, [MODE_LABELS[mode_id] for mode_id in mode_ids], mode_values)
    axis.text(0, -0.32, "Los cinco primeros modos son candidatos; conclusiones, recomendaciones y política concreta proceden de campos directos.", transform=axis.transAxes, fontsize=8)
    save(figure, "figura_02_modos_analiticos.png")

    interpellation = panels["interpellation_big_push"]
    criteria = ("gran_impulso_ambiental_concreto", "oportunidades_productivas_sostenibles", "articulacion_actores", "como_hacerlo_concreto")
    verdicts = ("Sí", "Parcial", "No")
    verdict_colors = {"Sí": "#59a14f", "Parcial": "#edc948", "No": "#e15759"}
    figure, axes = plt.subplots(4, 1, figsize=(10.5, 8.2), sharex=True)
    for axis, criterion in zip(axes, criteria):
        left = np.zeros(3)
        for verdict in verdicts:
            values = np.array([next(row["proportion"] for row in interpellation if row["period_id"] == period and row["criterion"] == criterion and row["verdict"] == verdict) for period in PERIODS])
            axis.barh([PERIOD_LABELS[period] for period in PERIODS], values, left=left, color=verdict_colors[verdict], label=verdict)
            left += values
        axis.set_title(CRITERION_LABELS[criterion], loc="left", fontsize=10, fontweight="bold")
        axis.set_xlim(0, 1)
        axis.xaxis.set_major_formatter(PercentFormatter(1))
        axis.grid(axis="x", alpha=0.2)
    axes[0].legend(
        frameon=True,
        facecolor="white",
        edgecolor="#d0d0d0",
        ncols=3,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.28),
    )
    save(figure, "figura_05_panel_big_push.png")

    territory = Counter((row["period_id"], candidate["nombre"]) for row in matrix for candidate in row["document_profile_summary"]["territorial_scope"]["normalized_candidates"])
    figure, axis = plt.subplots(figsize=(8, 5.6))
    labels = sorted({label for _, label in territory}, key=lambda label: -sum(territory[(period, label)] for period in PERIODS))
    bottom = np.zeros(len(PERIODS))
    palette = plt.cm.Set2(np.linspace(0, 1, len(labels)))
    for label, color in zip(labels, palette):
        values = np.array([territory[(period, label)] / denominators[period] for period in PERIODS])
        axis.bar([PERIOD_LABELS[period] for period in PERIODS], values, bottom=bottom, label=label, color=color)
        bottom += values
    axis.set_title("Escalas territoriales", loc="left", fontweight="bold")
    axis.set_ylim(0, max(bottom) * 1.18)
    axis.yaxis.set_major_formatter(PercentFormatter(1))
    axis.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.13), ncols=2)
    axis.grid(axis="y", alpha=0.2)
    save(figure, "figura_03_territorio.png")

    sustainability_secondaries = Counter(
        row["document_profile_summary"]["existing_typology"]["transformacion_secundaria"]["nombre"]
        for row in matrix
        if row["document_profile_summary"]["existing_typology"]["transformacion_primaria"]["nombre"] == "Sostenibilidad ambiental"
        and row["document_profile_summary"]["existing_typology"].get("transformacion_secundaria")
    )
    secondary_labels = sorted(sustainability_secondaries, key=sustainability_secondaries.get, reverse=True)
    figure, axis = plt.subplots(figsize=(9, 6.2))
    angles = np.linspace(np.pi / 2, np.pi / 2 + 2 * np.pi, len(secondary_labels), endpoint=False)
    radius = 3.0
    positions = {label: (radius * np.cos(angle), radius * np.sin(angle)) for label, angle in zip(secondary_labels, angles)}
    secondary_colors = ("#d1495b", "#e9a93b", "#3f8f8b", "#6b8e23", "#7a6f9b", "#5a7d9a", "#b07d62")
    for index, (label, (x_coord, y_coord)) in enumerate(positions.items()):
        count = sustainability_secondaries[label]
        axis.plot([0, x_coord], [0, y_coord], color="#bcc8ca", linewidth=0.9 + count * 0.11, alpha=0.85, zorder=1)
        axis.scatter(
            x_coord,
            y_coord,
            s=450 + count * 115,
            color=secondary_colors[index % len(secondary_colors)],
            edgecolor="#718185",
            linewidth=1.1,
            zorder=2,
        )
        direction = 1 if x_coord >= 0 else -1
        label_x = x_coord + direction * (0.35 + np.sqrt(450 + count * 115) / 85)
        label_y = y_coord + (0.12 if y_coord >= 0 else -0.12)
        axis.text(
            label_x,
            label_y,
            label,
            ha="left" if direction > 0 else "right",
            va="center",
            fontsize=7.5,
            fontweight="bold",
            color="#263238",
            zorder=3,
        )
        axis.text(
            label_x,
            label_y - 0.23,
            f"{count} documento{'s' if count != 1 else ''}",
            ha="left" if direction > 0 else "right",
            va="center",
            fontsize=6.8,
            color="#52666a",
            zorder=3,
        )
    axis.scatter(0, 0, s=7200, color="#1f6f78", edgecolor="#718185", linewidth=1.3, zorder=2)
    axis.text(0, 0, "Sostenibilidad\nambiental", ha="center", va="center", color="white", fontsize=9, fontweight="bold", zorder=3)
    axis.set_title("Transformaciones secundarias asociadas a sostenibilidad ambiental", loc="left", fontweight="bold")
    axis.set_xlim(-5.2, 5.2)
    axis.set_ylim(-4.5, 4.5)
    axis.set_aspect("equal")
    axis.axis("off")
    save(figure, "figura_04_sostenibilidad_secundarias.png")

    coverage = panels["research_question_coverage"]
    lines = ["# Cuadros del informe v1", "", "## Cuadro 1. Cobertura y corpus", "", "| Período | Documentos |", "| --- | ---: |"]
    lines.extend(f"| {period} | {denominators[period]} |" for period in PERIODS)
    lines.extend(["", "## Cuadro 2. Cobertura de preguntas de investigación", "", "| Pregunta | P1 | P2 | P3 |", "| --- | ---: | ---: | ---: |"])
    for question in sorted({row["question_id"] for row in coverage}):
        values = [next(row["documents"] for row in coverage if row["question_id"] == question and row["period_id"] == period) for period in PERIODS]
        lines.append(f"| {question} | " + " | ".join(str(value) for value in values) + " |")
    lines.extend([
        "",
        "Nota: cobertura de dimensiones directas; no es respuesta final ni medida de consenso.",
        "",
        "## Cuadro 3. Conclusiones y recomendaciones transversales",
        "",
        "| Patrón | Períodos | Documento ancla | Límite |",
        "| --- | --- | --- | --- |",
        "| Impactos y vulnerabilidad conectados con capacidad adaptativa y territorio | P1-P3 | 39140 | Un caso subnacional no representa todos los territorios regionales. |",
        "| Instrumentos y financiamiento como condiciones de transformación | P1-P3 | 47720, 41832 | Las recomendaciones no prueban adopción ni eficacia. |",
        "| Ejecución condicionada por inversión, capacidades, datos y coordinación | P2-P3 | 80561, 81405 | Los documentos no miden desempeño comparable entre países. |",
        "| Participación vinculada con derechos, igualdad y justicia ambiental | P1-P3 | 43301, 44970, 41101 | P9 es cualitativa; no hay medición validada de incidencia efectiva. |",
        "| Gran Impulso como estrategia más exigente que una oportunidad sectorial | P1-P3 | 40159, 43825 | La rúbrica describe contenido documental, no resultados de política. |",
        "",
        "## Cuadro 4. Propuestas, avances y brechas de implementación",
        "",
        "| Cobertura documental | 2015–2018 (n=99) | 2019–2022 (n=75) | 2023–2026 (n=64) |",
        "| --- | ---: | ---: | ---: |",
        "| Propuestas de política | 92/99 (92,9%) | 74/75 (98,7%) | 63/64 (98,4%) |",
        "| Avances de implementación | 61,6% | 66,7% | 71,9% |",
        "| Brechas de implementación | 59,6% | 76,0% | 70,3% |",
        "",
        "Nota: la cobertura registra presencia documental de propuestas, avances o brechas. No mide intensidad, adopción, ejecución efectiva ni resultados comparables entre países; las variaciones también pueden reflejar la composición de publicaciones por período.",
        "",
    ])
    (OUTPUT_DIR / "cuadros_01_02_cobertura.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"output_dir": OUTPUT_DIR.as_posix(), "figures": 5, "tables": 4}, ensure_ascii=False))


if __name__ == "__main__":
    main()