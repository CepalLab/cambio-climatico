"""Crea atómicamente el manifiesto literal del índice de una fuente paginada.

Uso: python crear_manifiesto_indice.py <fuente> [--output indice_fuente.json]
"""
import argparse, json, os, re, tempfile, unicodedata
from pathlib import Path

PAGE = re.compile(r"^===\s*P[ÁA]GINA PDF \d+\s*===$", re.M)
INDEX = re.compile(r"^\s*(?:tabla\s+de\s+contenidos?|índice(?:\s+general)?|indice(?:\s+general)?|contents?|table of contents|sumário|sumario|summary)\d*\s*$", re.I | re.M)
LEADER = re.compile(r"(?:\s*(?:\.{2,}|\s{2,}|\.(?:\s*\.){2,})\s*|\s+)\d+\s*$")
EXCLUIDO = re.compile(r"^(?:(?:\d+(?:\.\d+)*|[IVXLCDM]+)\.?\s*)?(?:contents|resumen(?!\s+de\s+recomendaciones\b)(?:\s+ejecutivo)?|resumo(?:\s+executivo)?|sum[aá]rio\s+executivo|apresentaç[ãa]o|revis[ãa]o(?:\s+de\s+pares)?|abstract|executive\s+summary|bibliograf[ií]a|bibliography|referencias?(?:\s+bibliogr[aá]ficas?)?|references?|(?:lista\s+de\s+)?(?:siglas?|abrevi(?:aturas?|aciones?))(?:\s+y\s+acr[o\u00f3]nimos?)?|acr[o\u00f3]nimos?|acronyms?|list\s+of\s+acronyms|glosario|glossary|unidades\s+de\s+medida(?:\s+y\s+equivalencias)?|pr[oó]logo|prologue|foreword|prefacio|preface|mensajes?(?:\s+(?:del|de\s+la|clave|institucional|principal(?:es)?))?|(?:key\s+)?messages?(?:\s+from)?|message\s+from|recuadros?|mapas?|anexos?|apéndices?|appendix|appendices|boxes?|publicaciones\s+recientes(?:\s+de\s+la\s+cepal)?)\b", re.I)
ROMANO_NIVEL_1 = re.compile(r"^[IVXL]+\.\s*", re.I)
SUBSECCION = re.compile(r"^(?:[A-HJ-UW-Z]|\d+)[.:]\s*", re.I)
LISTA_NO_SECCION = re.compile(r"^(?:lista|cuadros?|gr\s*(?:\u00e1|a)\s*ficos?|diagramas?|diagrams?|figuras?|im[áa]genes?|images?|tables?|table\s*[a-z0-9]|charts?|figures?|recuadros?|mapas?|boxes?|box\s*[a-z0-9]|annex(?:es)?|appendix|(?:studies\s+and\s+perspectives?|series\s+international\s+trade).*?issues\s+published|(?:IND|MAP)\s+[TDM]\.\d+|gases de efeito estufa equivalente|list\s+of\s+tables|list\s+of\s+figures)(?:\b|\d|[A-Z])", re.I)
CABECERA_INSTITUCIONAL = re.compile(r"^(?:\d+\s+)?(?:economic commission for latin america and the caribbean \(eclac\)|comisi[oó]n econ[oó]mica para am[eé]rica latina y el caribe \(cepal\)|comiss[aã]o econ[oô]mica para a am[eé]rica latina e o caribe \(cepal\)|a economia da mudan[cç]a clim[aá]tica na am[eé]rica latina e no caribe: uma vis[aã]o gr[aá]fica)(?:,\s*|\s|$)", re.I)
CABECERA_DOCUMENTO = re.compile(r"^(?:.+\s+(?:[\u2022\u00b7\uf09f]|\u00e2\u20ac\u00a2)\s+.+|índices climáticos, políticas de aseguramiento agropecuario y gestión integral de riesgos.*|la emergencia del cambio climático en américa latina y el caribe.*|fortalecimiento\s+de\s+la\s+cadena\s+de\s+valor\s+de\s+caf[eé].*|the bahamas|hurricane matthew|análisis\s+espacial\s+de\s+datos\s+hist[oó]ricos.*)$", re.I)

def ES_LISTA_NO_SECCION(titulo):
    return bool(
        LISTA_NO_SECCION.search(titulo)
        or re.search(r"\b(?:cuadros?|gr[\u00e1a]ficos?|im[áa]genes?|images?|figuras?)\b", titulo, re.I)
        or re.search(r"\bn[úu]meros\s+publicados\b", titulo, re.I)
    )

def incluida(titulo):
    return not (EXCLUIDO.search(titulo) or ES_LISTA_NO_SECCION(titulo) or CABECERA_INSTITUCIONAL.search(titulo) or CABECERA_DOCUMENTO.search(titulo))

def jerarquia_incluida(entradas):
    """Índice completo con nivel estable por numeración y, si falta, sangría."""
    contenido = [(titulo, sangria) for titulo, sangria in entradas if incluida(titulo)]
    if contenido and all(
        re.match(r"^(?:[A-ZÁÉÍÓÚÑ]\.\s+|Apéndice:\s+)", titulo, re.I)
        for titulo, _ in contenido
    ):
        return [{"titulo": titulo, "nivel": 1} for titulo, _ in contenido]
    has_roman = any(ROMANO_NIVEL_1.search(titulo) for titulo, _ in contenido)
    has_letters = any(re.match(r"^[A-ZÁÉÍÓÚÑ][.:]\s*", titulo, re.I) for titulo, _ in contenido)
    sangria_superior = min((sangria for titulo, sangria in contenido if ROMANO_NIVEL_1.search(titulo)), default=min((sangria for _, sangria in contenido), default=0))
    sangria_segundo = min((sangria for titulo, sangria in contenido if re.match(r"^[A-ZÁÉÍÓÚÑ][.:]\s*", titulo, re.I)), default=sangria_superior + 1)
    salida = []
    current_roman = False
    current_letter = False
    current_nivel2 = False
    for titulo, sangria in contenido:
        if ROMANO_NIVEL_1.search(titulo):
            nivel = 1
            current_roman = True
            current_letter = False
            current_nivel2 = False
        elif re.match(r"^[A-ZÁÉÍÓÚÑ][.:]\s*", titulo, re.I):
            # En índices romanos, A./B./C. son hermanos de nivel 2;
            # la numeración hija (1., 2., ...) ocupa el nivel 3.
            nivel = 2 if current_roman else 1
            current_letter = not current_roman
            current_nivel2 = True
        elif re.match(r"^\d+(?:\.\d+){2,}\.?\s+", titulo):
            nivel = 3
        elif re.match(r"^\d+\.\d+\.?\s+", titulo):
            nivel = 2
            current_nivel2 = True
        elif re.match(r"^\d+[.:]\s+", titulo):
            if has_roman and current_roman:
                nivel = 3
            elif current_letter:
                nivel = 2
            else:
                nivel = 1 if sangria <= sangria_superior else (3 if sangria > sangria_segundo else 2)
        else:
            if re.match(r"^(?:Introducci[oó]n|Introduction|Introduç[ãa]o|Consideraciones|Conclusiones|Recomendaç[õo]es|Conclusions?|Final\s+remarks?|Ep[íi]logo)\b", titulo, re.I) and sangria <= sangria_superior:
                nivel = 1
                current_roman = False
                current_letter = False
                current_nivel2 = False
            elif has_roman and current_roman:
                nivel = 2
                current_nivel2 = True
            else:
                nivel = 1 if sangria <= sangria_superior else (3 if sangria > sangria_segundo else 2)
        salida.append({"titulo": titulo, "nivel": nivel})
    return salida

def limpio(texto):
    return unicodedata.normalize("NFC", re.sub(r"\s+", " ", texto)).strip()

def cargar(fuente):
    fuente = Path(fuente)
    if fuente.is_dir():
        manifest = fuente / "manifest.json"
        rutas = [fuente / x["path"] for x in json.loads(manifest.read_text(encoding="utf-8")).get("chunks", [])] if manifest.exists() else sorted(fuente.glob("*.txt"))
    else:
        rutas = [fuente]
    if not rutas or any(not ruta.is_file() for ruta in rutas):
        raise ValueError("fuente sin tramos TXT legibles")
    return fuente, "\n".join(ruta.read_text(encoding="utf-8") for ruta in rutas)

def entradas_indice(texto):
    paginas = PAGE.split(texto)
    inicio = next((i for i, pagina in enumerate(paginas) if INDEX.search(pagina)), None)
    if inicio is None:
        # Policy briefs breves sin índice formal: sus encabezados tipográficos
        # de nivel 1 cuentan como índice (esquema_json_v1.md, regla 1).
        candidatas = []
        patrones = (
            re.compile(r"^(?:Introduction|Background|Methodology|Conclusion|Conclusions?|Final\s+remarks?)\s*$", re.I),
            re.compile(r"^\d+\.\s+[A-Z]\S.*$"),
            re.compile(r"^\d+\.\d+\s+[A-Z]\S.*$"),
            re.compile(r"^[a-h]\.\s+[A-Z]\S.*$"),
            re.compile(r"^A\.\s+Principales hallazgos del estudio\s*$", re.I),
            re.compile(r"^B\.\s+Recomendaciones\s*$", re.I),
            re.compile(r"^Apéndice:\s+Líneas de investigación futura\s*$", re.I),
        )
        lineas = texto.splitlines()
        for indice_linea, linea in enumerate(lineas):
            titulo = limpio(linea)
            if any(p.fullmatch(titulo) for p in patrones):
                # PyMuPDF puede partir un encabezado en dos líneas con una
                # línea vacía entre ambas; la continuación editorial empieza
                # en minúscula (p. ej. "economy in the Caribbean").
                siguiente = indice_linea + 1
                while siguiente < len(lineas) and not lineas[siguiente].strip():
                    siguiente += 1
                if siguiente < len(lineas):
                    continuacion = limpio(lineas[siguiente])
                    if (continuacion and continuacion[0].islower()
                            and not re.match(r"^[a-h]\.\s", continuacion, re.I)
                            and not re.match(r"^(?:Conclusion|Conclusions?)\s*$", titulo, re.I)):
                        titulo = limpio(f"{titulo} {continuacion}")
                if titulo not in [t for t, _ in candidatas]:
                    candidatas.append((titulo, len(linea) - len(linea.lstrip())))
        if not candidatas:
            raise ValueError("no se encontró un índice/contents ni encabezados tipográficos de nivel 1 en la fuente")
        return candidatas
    entradas, pendientes, sangria_pendiente = [], [], None
    categoria_no_seccion = None
    for numero, pagina in enumerate(paginas[inicio:]):
        if numero == 0:
            hallazgo = INDEX.search(pagina)
            pagina = pagina[hallazgo.end():]
        encontradas = 0
        for cruda in pagina.splitlines():
            sangria = len(cruda) - len(cruda.lstrip())
            linea = limpio(cruda)
            if not linea or INDEX.fullmatch(linea) or re.match(r"^(?:CEPAL|ECLAC|NACIONES UNIDAS|UNITED NATIONS)\b|^\d+$", linea, re.I) or CABECERA_INSTITUCIONAL.search(linea) or CABECERA_DOCUMENTO.search(linea):
                continue
            if re.match(r"^\s*(?:índice\s+de\s+(?:figuras|cuadros|tablas|gr[áa]ficos|recuadros|mapas)|indice\s+de\s+(?:figuras|cuadros|tablas|gr[áa]ficos|recuadros|mapas))\b", linea, re.I):
                break
            if re.match(r"^(?:cuadros?|gr\s*(?:\u00e1|a)\s*ficos?|diagramas?|diagrams?|figuras?|tables?|charts?|figures?|recuadros?|mapas?|boxes?)\s*$", linea, re.I):
                categoria_no_seccion = linea
                pendientes, sangria_pendiente = [], None
                continue
            if LEADER.search(cruda):
                titulo = limpio(LEADER.sub("", " ".join(pendientes + [cruda])))
                if categoria_no_seccion and not ES_LISTA_NO_SECCION(titulo):
                    titulo = f"{categoria_no_seccion} {titulo}"
                if titulo and not CABECERA_DOCUMENTO.search(titulo):
                    entradas.append((titulo, sangria_pendiente if sangria_pendiente is not None else sangria))
                    encontradas += 1
                pendientes, sangria_pendiente = [], None
            elif pendientes or re.match(r"^(?:[IVXLCDM]+\.|[A-Z]\. |(?:\d+\.)*\d+[.:]?\s+|[A-ZÁÉÍÓÚÑ][\wÁÉÍÓÚÜÑ¿])", linea):
                if not pendientes:
                    sangria_pendiente = sangria
                pendientes.append(linea)
        if numero and not encontradas:
            break
    if not entradas:
        # OCR: algunos índices conservan los encabezados numerados pero
        # pierden los puntos-guía y los folios. Recuperar únicamente esos
        # encabezados desde la página del índice, sin inferir títulos nuevos.
        paginas = PAGE.split(texto)
        indice = next((pagina for pagina in paginas if INDEX.search(pagina)), "")
        for cruda in indice.splitlines():
            linea = limpio(cruda)
            if not linea or INDEX.fullmatch(linea):
                continue
            match = re.match(r"^([IVXLCDM]+\.)\s+(.+?)\s*(?:\d+)?$", linea, re.I)
            if match:
                titulo = limpio(f"{match.group(1)} {match.group(2)}")
                if incluida(titulo):
                    entradas.append((titulo, len(cruda) - len(cruda.lstrip())))
        if not entradas:
            # Índice OCR con numeración romana aislada y título partido en
            # varias líneas; conservar literalmente el texto recuperable.
            lineas = indice.splitlines()
            pos = 0
            romano_ocr = {"L": "I.", "IL": "II.", "UU": "III.", "IV.": "IV.", "V.": "V."}
            while pos < len(lineas):
                marca = limpio(lineas[pos]).upper()
                if marca in romano_ocr:
                    partes = []
                    pos += 1
                    while pos < len(lineas):
                        siguiente = limpio(lineas[pos])
                        if re.search(r"\d", siguiente) or siguiente.startswith("==="):
                            break
                        if siguiente:
                            partes.append(siguiente)
                        pos += 1
                    titulo = limpio(f"{romano_ocr[marca]} {' '.join(partes)}")
                    if incluida(titulo):
                        entradas.append((titulo, 0))
                pos += 1
        if not entradas:
            raise ValueError("el índice no contiene entradas con puntos-guía ni encabezados OCR recuperables")
    return entradas

def filtrar_entradas(entradas):
    prefijos_excluidos = set()
    for titulo, _ in entradas:
        m = re.match(r"^(\d+|[IVXLCDM]+)\.\s*", titulo)
        if m and (EXCLUIDO.search(titulo) or ES_LISTA_NO_SECCION(titulo)):
            prefijos_excluidos.add(m.group(1))
    filtradas, excluidos = [], []
    en_bloque_excluido = False
    sangria_bloque_excluido = 0
    for titulo, sangria in entradas:
        m = re.match(r"^(\d+|[IVXLCDM]+)(?:\.|\b)", titulo)
        if m and m.group(1) in prefijos_excluidos:
            excluidos.append(titulo)
            continue
        if EXCLUIDO.search(titulo) or ES_LISTA_NO_SECCION(titulo):
            excluidos.append(titulo)
            en_bloque_excluido = True
            sangria_bloque_excluido = sangria
            continue
        if en_bloque_excluido:
            if sangria > sangria_bloque_excluido:
                excluidos.append(titulo)
                continue
            else:
                en_bloque_excluido = False
        if not incluida(titulo):
            excluidos.append(titulo)
            continue
        filtradas.append((titulo, sangria))
    return filtradas, excluidos

def construir(fuente):
    fuente, texto = cargar(fuente)
    entradas = entradas_indice(texto)
    titulos = [titulo for titulo, _ in entradas]
    # Algunos ?ndices cortan antes de las conclusiones; recuperar ?nicamente ese
    # encabezado terminal literal desde el cuerpo, sin inferir otras secciones.
    for linea in texto.splitlines():
        titulo = limpio(linea)
        if re.match(r"^[IVXLCDM]+\.\s*(?:CONCLUSIONES?|CONCLUSIONS?)(?:\s+Y\s+RECOMENDACIONES?)?\b", titulo, re.I):
            if not any(re.match(r"^[IVXLCDM]+\.\s*(?:CONCLUSIONES?|CONCLUSIONS?)\b", t, re.I) for t in titulos):
                entradas.append((titulo, 0))
                titulos.append(titulo)
    
    entradas_validas, excluidos = filtrar_entradas(entradas)
    jerarquia = jerarquia_incluida(entradas_validas)
    incluidos = [e["titulo"] for e in jerarquia if e["nivel"] == 1]
    
    return {"fuente_inspeccionada": str(fuente), "has_executive_summary": any(re.match(r"^(?:(?:\d+(?:\.\d+)*|[IVXLCDM]+)\.?\s*)?(?:resumen\s+ejecutivo|executive\s+summary|resumo\s+executivo|sum[aá]rio\s+executivo)\b", titulo, re.I) for titulo in titulos), "secciones_nivel_1_incluidas": incluidos, "secciones_jerarquicas_incluidas": jerarquia, "titulos_excluidos": excluidos}

def escribir_atomico(destino, contenido):
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=destino.parent, delete=False, suffix=".tmp") as temporal:
        json.dump(contenido, temporal, ensure_ascii=False, indent=2)
        temporal.write("\n")
        nombre = temporal.name
    os.replace(nombre, destino)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("fuente")
    parser.add_argument("--output")
    args = parser.parse_args()
    fuente = Path(args.fuente)
    salida = Path(args.output) if args.output else (fuente / "indice_fuente.json" if fuente.is_dir() else fuente.parent / "indice_fuente.json")
    try:
        escribir_atomico(salida, construir(fuente))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    print(f"Manifiesto de índice creado: {salida}")

if __name__ == "__main__":
    main()
