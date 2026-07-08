"""
Resuelve handles del repositorio institucional de la CEPAL (DSpace 7) directamente
vía su API REST, sin depender de scraping de HTML.

Flujo: handle -> UUID de ítem (resolución 302) -> metadatos (incluye páginas) ->
bundles -> bitstream PDF (ORIGINAL) y texto plano autoextraído por DSpace (TEXT).

No requiere dependencias externas (solo stdlib) porque este pipeline corre offline,
fuera de la app Streamlit desplegada — no se agrega a requirements.txt.

Uso:
    python cepal_repositorio.py 11362/48603
"""

import json
import sys
import urllib.request

API_BASE = "https://repositorio.cepal.org/server/api"


def _get_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def resolver_handle(handle: str) -> str:
    """Devuelve el UUID del ítem a partir de un handle tipo '11362/48603'.

    /server/api/pid/find redirige (302) a /server/api/core/items/{uuid};
    urllib sigue la redirección solo, así que basta con leer la URL final.
    """
    url = f"{API_BASE}/pid/find?id={handle}"
    with urllib.request.urlopen(url) as resp:
        final_url = resp.geturl()
    return final_url.rstrip("/").split("/")[-1]


def obtener_metadatos(item_uuid: str) -> dict:
    return _get_json(f"{API_BASE}/core/items/{item_uuid}")


def obtener_bitstreams(item_uuid: str) -> dict:
    """Devuelve {'ORIGINAL': [...], 'TEXT': [...], 'THUMBNAIL': [...]} con URLs de descarga directa."""
    bundles = _get_json(f"{API_BASE}/core/items/{item_uuid}/bundles")["_embedded"]["bundles"]

    resultado = {}
    for bundle in bundles:
        nombre = bundle["name"]
        uuid = bundle["uuid"]
        bitstreams = _get_json(f"{API_BASE}/core/bundles/{uuid}/bitstreams")["_embedded"]["bitstreams"]
        resultado[nombre] = [
            {
                "nombre": b["name"],
                "tamano_bytes": b["sizeBytes"],
                "url_contenido": b["_links"]["content"]["href"],
            }
            for b in bitstreams
        ]
    return resultado


def resolver_documento(handle: str) -> dict:
    """Punto de entrada único: handle -> metadatos + URLs de PDF y texto plano."""
    uuid = resolver_handle(handle)
    metadatos = obtener_metadatos(uuid)
    bitstreams = obtener_bitstreams(uuid)

    extent = metadatos.get("metadata", {}).get("dc.format.extent", [{}])
    paginas = extent[0].get("value") if extent else None

    return {
        "handle": handle,
        "uuid": uuid,
        "titulo": metadatos.get("name"),
        "paginas": paginas,
        "pdf": bitstreams.get("ORIGINAL", [None])[0],
        "texto_extraido": bitstreams.get("TEXT", [None])[0],
    }


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        print("Uso: python cepal_repositorio.py <handle, ej. 11362/48603>")
        sys.exit(1)
    print(json.dumps(resolver_documento(sys.argv[1]), indent=2, ensure_ascii=False))
