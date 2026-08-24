"""Audita completitud y cardinalidades del corpus activo de Fase 3."""

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parent.parent
DEFAULT_INVENTORY = Path(__file__).resolve().parent / "inventario_corpus_v1.json"
DEFAULT_EXCLUSIONS = Path(__file__).resolve().parent / "exclusiones_corpus_v1.csv"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "auditoria_transversal_v1.json"
REQUIRED_TOP_LEVEL = {"documento", "resumen_enriquecido", "resumen_secciones", "interpelacion", "tipologia"}
REQUIRED_INTERPELATION = {
    "gran_impulso_ambiental_concreto",
    "articulacion_actores",
    "oportunidades_productivas_sostenibles",
    "como_hacerlo_concreto",
}
CANONICAL_TRANSFORMATIONS = {
    "Desarrollo productivo",
    "Reducción de la desigualdad",
    "Protección social",
    "Educación y formación profesional",
    "Igualdad de género",
    "Sostenibilidad ambiental",
    "Transformación digital",
    "Migración",
    "Integración económica",
    "Macroeconomía y fiscalidad",
    "Capacidades del Estado",
}
CANONICAL_DIMENSIONS = {
    "contexto_antecedentes",
    "estado_de_situacion",
    "diagnostico_estructural",
    "tendencias",
    "desafios",
    "oportunidades",
    "propuestas_politica",
    "avances_implementacion",
    "brechas_implementacion",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_exclusions(path: Path) -> set[str]:
    with path.open(encoding="utf-8-sig", newline="") as file:
        return {
            row["handle"]
            for row in csv.DictReader(file)
            if row.get("decision") == "excluir" and row.get("estado") == "aplicado"
        }


def walk_sections(sections: list[dict]):
    for section in sections:
        yield section
        yield from walk_sections(section.get("subsecciones") or [])


def valid_page(value) -> bool:
    if isinstance(value, int):
        return value > 0
    if isinstance(value, str):
        return bool(re.fullmatch(r"\d+(?:-\d+)?", value.strip()))
    return False


def audit_document(record: dict, exclusions: set[str]) -> tuple[dict, list[str]]:
    path = REPO_DIR / record["ruta_json"]
    data = json.loads(path.read_text(encoding="utf-8"))
    document = data.get("documento") or {}
    tipologia = data.get("tipologia") or {}
    interpelacion = data.get("interpelacion") or {}
    sections = list(walk_sections(data.get("resumen_secciones") or []))
    dimensions = [dimension for section in sections for dimension in section.get("dimensiones") or []]
    citations = [dimension.get("cita") for dimension in dimensions]
    anomalies = []

    if record["handle"] in exclusions:
        anomalies.append("incluido_en_inventario_activo_pese_a_exclusion_aplicada")
    if set(data) != REQUIRED_TOP_LEVEL:
        missing = sorted(REQUIRED_TOP_LEVEL - set(data))
        extra = sorted(set(data) - REQUIRED_TOP_LEVEL)
        if missing:
            anomalies.append(f"claves_superiores_faltantes:{','.join(missing)}")
        if extra:
            anomalies.append(f"claves_superiores_adicionales:{','.join(extra)}")
    if not document.get("handle"):
        anomalies.append("handle_vacio")
    if document.get("handle") != record["handle"]:
        anomalies.append("handle_no_coincide_con_inventario")
    if document.get("num_muestra") is None:
        anomalies.append("num_muestra_nulo")
    for key in ("transformacion_primaria", "transformacion_secundaria"):
        value = tipologia.get(key) or {}
        if not value.get("nombre") or value.get("numero") is None:
            anomalies.append(f"tipologia_incompleta:{key}")
        elif value["nombre"] not in CANONICAL_TRANSFORMATIONS:
            anomalies.append(f"transformacion_no_canonica:{key}:{value['nombre']}")
    missing_interpelation = sorted(REQUIRED_INTERPELATION - set(interpelacion))
    if missing_interpelation:
        anomalies.append(f"interpelacion_incompleta:{','.join(missing_interpelation)}")
    verdicts = [item.get("veredicto") for item in interpelacion.values() if isinstance(item, dict)]
    invalid_verdicts = sorted({str(value) for value in verdicts if value not in {"Sí", "Parcial", "No"}})
    if invalid_verdicts:
        anomalies.append(f"veredictos_no_canonicos:{','.join(invalid_verdicts)}")
    if any(not isinstance(citation, str) or not citation.strip() for citation in citations):
        anomalies.append("dimension_sin_cita")
    unknown_dimensions = sorted({
        str(dimension.get("dimension"))
        for dimension in dimensions
        if dimension.get("dimension") not in CANONICAL_DIMENSIONS
    })
    if unknown_dimensions:
        anomalies.append(f"dimensiones_no_canonicas:{','.join(unknown_dimensions)}")
    invalid_pages = [str(dimension.get("pagina")) for dimension in dimensions if not valid_page(dimension.get("pagina"))]
    if invalid_pages:
        anomalies.append("dimension_con_pagina_invalida")

    certificate = REPO_DIR / record["ruta_certificado"] if record.get("ruta_certificado") else None
    certificate_hash_ok = bool(certificate and certificate.is_file() and record.get("sha256_certificado") == sha256(certificate))
    if record.get("certificado_disponible") and not certificate_hash_ok:
        anomalies.append("certificado_no_coincide_con_inventario")
    if certificate and certificate.is_file():
        sealed = json.loads(certificate.read_text(encoding="utf-8"))
        if sealed.get("result_sha256") != sha256(path):
            anomalies.append("certificado_no_coincide_con_json")

    return {
        "handle": record["handle"],
        "titulo": document.get("titulo"),
        "origen": record["origen"],
        "ruta_json": record["ruta_json"],
        "num_muestra": document.get("num_muestra"),
        "fecha": document.get("fecha"),
        "nivel_aplicacion": tipologia.get("nivel_aplicacion"),
        "transformacion_primaria": (tipologia.get("transformacion_primaria") or {}).get("nombre"),
        "transformacion_secundaria": (tipologia.get("transformacion_secundaria") or {}).get("nombre"),
        "ambito_aplicacion": (data.get("resumen_enriquecido", {}).get("alcance") or {}).get("ambito_aplicacion"),
        "secciones": len(sections),
        "dimensiones": len(dimensions),
        "citas_dimension": len([citation for citation in citations if citation]),
        "veredictos_interpelacion": Counter(verdicts),
        "certificado_disponible": bool(certificate and certificate.is_file()),
        "anomalies": anomalies,
    }, anomalies


def build_report(inventory_path: Path, exclusions_path: Path) -> dict:
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    exclusions = load_exclusions(exclusions_path)
    records = [record for record in inventory["documentos"] if record["handle"] not in exclusions]
    documents = []
    anomalies = []
    for record in records:
        summary, document_anomalies = audit_document(record, exclusions)
        summary["veredictos_interpelacion"] = dict(summary["veredictos_interpelacion"])
        documents.append(summary)
        anomalies.extend({"handle": record["handle"], "issues": document_anomalies} for _ in [0] if document_anomalies)

    return {
        "version": "auditoria-transversal-v1",
        "generado_en": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "fuentes": {
            "inventario": inventory_path.relative_to(REPO_DIR).as_posix(),
            "exclusiones": exclusions_path.relative_to(REPO_DIR).as_posix(),
        },
        "denominador": {
            "historico": len(inventory["documentos"]),
            "exclusiones_aplicadas": len(exclusions),
            "activo": len(records),
        },
        "cardinalidades": {
            "origen": dict(Counter(document["origen"] for document in documents)),
            "transformacion_primaria": dict(Counter(document["transformacion_primaria"] for document in documents)),
            "transformacion_secundaria": dict(Counter(document["transformacion_secundaria"] for document in documents)),
            "nivel_aplicacion": dict(Counter(document["nivel_aplicacion"] for document in documents)),
            "fecha": dict(Counter(document["fecha"] for document in documents)),
            "veredictos_interpelacion": dict(Counter(
                verdict
                for document in documents
                for verdicts in [document["veredictos_interpelacion"]]
                for verdict, count in verdicts.items()
                for _ in range(count)
            )),
        },
        "totales": {
            "secciones": sum(document["secciones"] for document in documents),
            "dimensiones": sum(document["dimensiones"] for document in documents),
            "citas_dimension": sum(document["citas_dimension"] for document in documents),
            "certificados": sum(document["certificado_disponible"] for document in documents),
        },
        "anomalies": anomalies,
        "documentos": documents,
    }


def write_markdown(report: dict, path: Path) -> None:
    lines = [
        "# Auditoría transversal v1",
        "",
        f"Generada: `{report['generado_en']}`",
        "",
        "## Denominador",
        "",
        f"- Histórico: **{report['denominador']['historico']}**",
        f"- Exclusiones aplicadas: **{report['denominador']['exclusiones_aplicadas']}**",
        f"- Corpus activo auditado: **{report['denominador']['activo']}**",
        "",
        "## Totales",
        "",
    ]
    lines.extend(f"- {key}: **{value}**" for key, value in report["totales"].items())
    lines.extend(["", "## Anomalías", ""])
    if report["anomalies"]:
        lines.extend(f"- `{item['handle']}`: {', '.join(item['issues'])}" for item in report["anomalies"])
    else:
        lines.append("Sin anomalías estructurales detectadas por esta auditoría.")
    lines.extend(["", "## Cardinalidades", ""])
    for category, values in report["cardinalidades"].items():
        lines.append(f"### {category}")
        lines.extend(f"- {key}: {value}" for key, value in sorted(values.items(), key=lambda item: str(item[0])))
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--exclusions", type=Path, default=DEFAULT_EXCLUSIONS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = build_report(args.inventory, args.exclusions)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    markdown = args.output.with_suffix(".md")
    write_markdown(report, markdown)
    print(json.dumps({"output": args.output.as_posix(), **report["denominador"], **report["totales"], "anomalies": len(report["anomalies"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()