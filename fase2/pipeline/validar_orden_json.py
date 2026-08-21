"""Valida el orden canónico de las claves del JSON analítico.

No reescribe el artefacto: informa cualquier reordenamiento para que se corrija
en el generador o en la sesión de enriquecimiento.
"""

import argparse
import json
import sys
from pathlib import Path

ORDEN = {
    "raiz": ["documento", "resumen_enriquecido", "resumen_secciones", "interpelacion", "tipologia"],
    "documento": ["num_muestra", "titulo", "autoria", "handle", "simbolo", "isbn", "fecha", "tipo_documento", "paginas_cuerpo", "paginas_totales", "idioma", "tiene_resumen_ejecutivo", "tiene_anexos"],
    "resumen_enriquecido": ["pregunta_investigacion", "alcance", "hallazgos_principales", "conclusiones_recomendaciones", "resumen_narrativo"],
    "alcance": ["ambito_aplicacion", "referentes_dependencias", "sectorial", "temporal"],
    "conclusiones_recomendaciones": ["conclusiones", "recomendaciones", "nota"],
    "seccion": ["seccion", "nivel", "paginas", "resumen", "dimensiones", "subsecciones"],
    "dimension": ["dimension", "cita", "pagina", "subtipo_brecha"],
    "interpelacion": ["gran_impulso_ambiental_concreto", "articulacion_actores", "oportunidades_productivas_sostenibles", "como_hacerlo_concreto"],
    "criterio": ["veredicto", "evidencia", "citas", "desglose_items", "tally", "nota"],
    "tipologia": ["transformacion_primaria", "transformacion_secundaria", "razonamiento_5_pasos", "tipo_documento_climatico", "nivel_aplicacion", "ambiguedad_pendiente_validacion"],
    "transformacion": ["numero", "nombre", "certeza"],
    "razonamiento_5_pasos": ["tension_dialectica", "filtro_categoria_primaria", "secundaria_obligatoria", "justificacion_anti_copia", "validacion_anclas"],
    "desglose_item": ["item", "clasificacion", "pagina"],
    "cita": ["cita", "pagina"],
}


def comprobar(obj, orden, ruta, errores):
    if not isinstance(obj, dict):
        return
    posiciones = {clave: i for i, clave in enumerate(orden)}
    conocidas = [clave for clave in obj if clave in posiciones]
    indices = [posiciones[clave] for clave in conocidas]
    if indices != sorted(indices):
        errores.append(f"{ruta}: claves fuera de orden; observadas {list(obj)!r}")
    ultima = max(indices, default=-1)
    intercaladas = [clave for i, clave in enumerate(obj) if clave not in posiciones and i < ultima]
    if intercaladas:
        errores.append(f"{ruta}: claves no canónicas intercaladas antes del final: {intercaladas!r}")


def validar(data):
    errores = []
    comprobar(data, ORDEN["raiz"], "raíz", errores)
    comprobar(data.get("documento"), ORDEN["documento"], "documento", errores)
    enriquecido = data.get("resumen_enriquecido") or {}
    comprobar(enriquecido, ORDEN["resumen_enriquecido"], "resumen_enriquecido", errores)
    comprobar(enriquecido.get("alcance"), ORDEN["alcance"], "resumen_enriquecido.alcance", errores)
    cr = enriquecido.get("conclusiones_recomendaciones")
    if isinstance(cr, dict):
        comprobar(cr, ORDEN["conclusiones_recomendaciones"], "conclusiones_recomendaciones", errores)

    def secciones(lista, ruta):
        for i, seccion in enumerate(lista or []):
            sruta = f"{ruta}[{i}]"
            comprobar(seccion, ORDEN["seccion"], sruta, errores)
            for j, dimension in enumerate(seccion.get("dimensiones") or []):
                comprobar(dimension, ORDEN["dimension"], f"{sruta}.dimensiones[{j}]", errores)
                if isinstance(dimension.get("cita"), dict):
                    comprobar(dimension["cita"], ORDEN["cita"], f"{sruta}.dimensiones[{j}].cita", errores)
            secciones(seccion.get("subsecciones"), f"{sruta}.subsecciones")

    secciones(data.get("resumen_secciones"), "resumen_secciones")
    interpelacion = data.get("interpelacion") or {}
    comprobar(interpelacion, ORDEN["interpelacion"], "interpelacion", errores)
    for criterio, valor in interpelacion.items():
        if not isinstance(valor, dict):
            continue
        comprobar(valor, ORDEN["criterio"], f"interpelacion.{criterio}", errores)
        for i, cita in enumerate(valor.get("citas") or []):
            comprobar(cita, ORDEN["cita"], f"interpelacion.{criterio}.citas[{i}]", errores)
        for i, item in enumerate(valor.get("desglose_items") or []):
            comprobar(item, ORDEN["desglose_item"], f"interpelacion.{criterio}.desglose_items[{i}]", errores)
    tipologia = data.get("tipologia") or {}
    comprobar(tipologia, ORDEN["tipologia"], "tipologia", errores)
    comprobar(tipologia.get("transformacion_primaria"), ORDEN["transformacion"], "tipologia.transformacion_primaria", errores)
    comprobar(tipologia.get("transformacion_secundaria"), ORDEN["transformacion"], "tipologia.transformacion_secundaria", errores)
    comprobar(tipologia.get("razonamiento_5_pasos"), ORDEN["razonamiento_5_pasos"], "tipologia.razonamiento_5_pasos", errores)
    return errores


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("documento", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.documento.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        parser.error(str(error))
    errores = validar(data)
    if errores:
        print("VALIDACIÓN DE ORDEN JSON: ERROR")
        for error in errores:
            print(f" - {error}")
        return 1
    print("VALIDACIÓN DE ORDEN JSON: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
