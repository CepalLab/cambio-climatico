"""Compuerta bloqueante entre documento JSON e indice_fuente.json.

Uso: python validar_indice.py documento.json --indice indice_fuente.json
"""
import argparse, json, re, sys, unicodedata

EXCLUIDO = re.compile(r"^(?:(?:\d+(?:\.\d+)*|[IVXLCDM]+)\.?\s*)?(?:resumen(?!\s+(?:de\s+recomendaciones|y\s+conclusiones)\b)(?!\s*,\s*\w)|resumen\s+ejecutivo|resumo(?:\s+executivo)?|sum[aá]rio\s+executivo|abstract|executive\s+summary|bibliograf[ií]a|bibliography|referencias?(?:\s+bibliogr[aá]ficas?)?|references?|(?:lista\s+de\s+)?(?:siglas?|abrevi(?:aturas?|aciones?))(?:\s+y\s+acr[o\u00f3]nimos?)?|acr[o\u00f3]nimos?|acronyms?|list\s+of\s+acronyms|glosario|glossary|unidades\s+de\s+medida(?:\s+y\s+equivalencias)?|pr[oó]logo|prologue|foreword|prefacio|preface|mensajes?(?:\s+(?:del|de\s+la|clave|institucional|principal(?:es)?))?|(?:key\s+)?messages?(?:\s+from)?|message\s+from|recuadros?|mapas?|anexos?|boxes?)\b", re.I)
REQUERIDAS = {"fuente_inspeccionada", "has_executive_summary", "secciones_nivel_1_incluidas", "secciones_jerarquicas_incluidas", "titulos_excluidos"}

def normalizar(titulo):
    """Solo NFC y espacios/saltos; letras, signos y numeración son significativos."""
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", titulo)).strip()

def recorrer(secciones):
    for seccion in secciones:
        yield seccion
        yield from recorrer(seccion.get("subsecciones") or [])

def jerarquia_documento(secciones):
    return [{"titulo": str(seccion.get("seccion") or ""), "nivel": seccion.get("nivel")} for seccion in recorrer(secciones)]

def normalizar_jerarquia(entradas):
    if not isinstance(entradas, list) or not all(isinstance(entrada, dict) and isinstance(entrada.get("titulo"), str) and isinstance(entrada.get("nivel"), int) for entrada in entradas):
        return None
    return [{"titulo": normalizar(entrada["titulo"]), "nivel": entrada["nivel"]} for entrada in entradas]

def validar(documento, indice):
    from pathlib import Path
    data = json.loads(Path(documento).read_text(encoding="utf-8"))
    manifiesto = json.loads(Path(indice).read_text(encoding="utf-8"))
    faltantes = REQUERIDAS - set(manifiesto)
    if faltantes:
        return [f"manifiesto incompleto: faltan {sorted(faltantes)}"]
    errores = []
    esperado = manifiesto["has_executive_summary"]
    observado = data.get("documento", {}).get("tiene_resumen_ejecutivo")
    if not isinstance(esperado, bool):
        errores.append("has_executive_summary del manifiesto debe ser booleano")
    if not isinstance(observado, bool):
        errores.append("documento.tiene_resumen_ejecutivo debe ser booleano")
    elif isinstance(esperado, bool) and observado != esperado:
        errores.append(f"tiene_resumen_ejecutivo={observado!r} difiere del manifiesto ({esperado!r})")
    for seccion in recorrer(data.get("resumen_secciones") or []):
        titulo = str(seccion.get("seccion") or "")
        if EXCLUIDO.search(normalizar(titulo)):
            errores.append(f"sección excluida en resumen_secciones: '{titulo}'")
    esperadas = manifiesto["secciones_nivel_1_incluidas"]
    if not isinstance(esperadas, list) or not all(isinstance(titulo, str) for titulo in esperadas):
        return errores + ["secciones_nivel_1_incluidas debe ser lista de títulos"]
    observadas = [str(seccion.get("seccion") or "") for seccion in data.get("resumen_secciones") or [] if seccion.get("nivel") == 1]
    if list(map(normalizar, observadas)) != list(map(normalizar, esperadas)):
        errores.extend(["títulos, orden o cobertura de secciones de nivel 1 difieren del índice", f"índice: {esperadas!r}", f"documento: {observadas!r}"])
    esperada_jerarquia = normalizar_jerarquia(manifiesto["secciones_jerarquicas_incluidas"])
    observada_jerarquia = normalizar_jerarquia(jerarquia_documento(data.get("resumen_secciones") or []))
    if esperada_jerarquia is None:
        errores.append("secciones_jerarquicas_incluidas debe ser lista de objetos {titulo, nivel}")
    elif observada_jerarquia != esperada_jerarquia:
        errores.extend(["títulos, niveles, orden o cobertura de la jerarquía de secciones difieren del índice", f"índice jerárquico: {esperada_jerarquia!r}", f"documento jerárquico: {observada_jerarquia!r}"])
    return errores

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("documento")
    parser.add_argument("--indice", required=True)
    args = parser.parse_args()
    try:
        errores = validar(args.documento, args.indice)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    if errores:
        print("VALIDACIÓN DE ÍNDICE: ERROR")
        for error in errores:
            print(f" - {error}")
        sys.exit(1)
    print("VALIDACIÓN DE ÍNDICE: OK")

if __name__ == "__main__":
    main()
