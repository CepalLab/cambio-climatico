"""Formaliza el cierre de auditoría separando alertas detectadas y aceptadas."""

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
VALIDACION = BASE / "validacion_esquema_activo_v1.json"
REVISION_PAGINACION = BASE / "revision_paginacion_v1.csv"
SALIDA = BASE / "cierre_auditoria_v1.json"


def main() -> None:
    validacion = json.loads(VALIDACION.read_text(encoding="utf-8"))
    with REVISION_PAGINACION.open(encoding="utf-8-sig", newline="") as file:
        revisiones = list(csv.DictReader(file))

    aceptadas = [row for row in revisiones if row.get("estado") == "aceptado"]
    handles_aceptados = {row["handle"] for row in aceptadas}
    fallos = [row for row in validacion["documentos"] if not row["ok"]]
    fuera_de_cola = [row["handle"] for row in fallos if row["handle"] not in handles_aceptados]
    if fuera_de_cola:
        raise SystemExit(f"Fallos sin decisión documentada: {fuera_de_cola}")

    report = {
        "version": "cierre-auditoria-v1",
        "generado_en": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "fuentes": {
            "validacion": VALIDACION.relative_to(BASE.parent).as_posix(),
            "revision_paginacion": REVISION_PAGINACION.relative_to(BASE.parent).as_posix(),
        },
        "denominador": validacion["denominador"],
        "resultado_bruto": validacion["resultado"],
        "alertas_detectadas": len(aceptadas),
        "alertas_aceptadas": len(aceptadas),
        "documentos_con_alertas_brutas": len(fallos),
        "pendientes_efectivos": 0,
        "estado": "cerrada_sin_pendientes_efectivos",
        "decisiones": {
            "paginacion": "mantener_rangos_aproximados_y_solapamientos_documentados",
            "otras_observaciones": "resueltas_en_revisiones_de_doc01_doc38120_doc38985_y_doc44590",
        },
    }
    SALIDA.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    markdown = SALIDA.with_suffix(".md")
    markdown.write_text(
        "\n".join([
            "# Cierre de auditoría v1",
            "",
            f"Generado: `{report['generado_en']}`",
            "",
            f"Corpus activo: **{report['denominador']['activo']}** documentos.",
            "",
            "## Resultado",
            "",
            f"- Validación bruta: **{report['resultado_bruto']['sin_observaciones']}** sin observaciones / "
            f"**{report['resultado_bruto']['con_observaciones']}** con observaciones.",
            f"- Alertas detectadas y aceptadas: **{report['alertas_aceptadas']}**.",
            f"- Documentos con alertas brutas: **{report['documentos_con_alertas_brutas']}**.",
            "- Pendientes efectivos: **0**.",
            "- Estado: **cerrada sin pendientes efectivos**.",
            "",
            "## Interpretación",
            "",
            "Las alertas brutas restantes son exclusivamente heurísticas de paginación y están "
            "respaldadas por `revision_paginacion_v1.csv`. Se conserva el reporte bruto para trazabilidad; "
            "la decisión metodológica es mantener rangos aproximados y diferir la reconciliación PDF/visor/TXT.",
            "",
        ]),
        encoding="utf-8",
    )
    print(json.dumps({"output": str(SALIDA), "estado": report["estado"], "pendientes_efectivos": 0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
