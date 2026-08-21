# Preparación de fuente — Preflight determinista L0001 (docs 15–17)

Fecha: 2026-08-12

## Metodología

1. Resolución de handle vía `cepal_repositorio.py` (DSpace 7 API REST).
2. Descarga del bundle TEXT (texto plano autoextraído por DSpace).
3. Ejecución de `preflight_endpoint_text.py` con `--pages-per-chunk 25`.
4. Los tres documentos resultaron **aptos** (`usable: true`) y con **saltos de página** (`page_boundaries_usable: true`), por lo que se selecciona **endpoint_apto** como fuente. No se descargó PDF ni se ejecutó OCR.

---

## 11362/39286 — The Caribbean and the post-2015 development agenda (num_muestra: 15)

| Métrica | Valor |
|---|---|
| Fuente seleccionada | **endpoint_apto** (bundle TEXT de DSpace) |
| Caracteres | 254 732 |
| Páginas | 78 (form feeds: 77) |
| Páginas con texto | 72/78 |
| Control chars ratio | 0.000306 |
| Mojibake | 0 |
| Near limit | no |
| Tramos generados | 4 (`tramo_001_025.txt` … `tramo_076_078.txt`) |
| Manifest | `corpus/intermedios/11362/39286/tramos_endpoint/manifest.json` |
| Revisión visual | **No requerida** |

## 11362/39360 — Emisiones de GEI y mitigación en el sector residuos: economía del cambio climático en la Argentina (num_muestra: 16)

| Métrica | Valor |
|---|---|
| Fuente seleccionada | **endpoint_apto** (bundle TEXT de DSpace) |
| Caracteres | 135 878 |
| Páginas | 70 (form feeds: 69) |
| Páginas con texto | 65/70 |
| Control chars ratio | 0.000508 |
| Mojibake | 0 |
| Near limit | no |
| Tramos generados | 3 (`tramo_001_025.txt` … `tramo_051_070.txt`) |
| Manifest | `corpus/intermedios/11362/39360/tramos_endpoint/manifest.json` |
| Revisión visual | **No requerida** |

## 11362/39367 — Financiamiento para el Cambio Climático en América Latina y el Caribe en 2014 (num_muestra: 17)

| Métrica | Valor |
|---|---|
| Fuente seleccionada | **endpoint_apto** (bundle TEXT de DSpace) |
| Caracteres | 321 226 |
| Páginas | 110 (form feeds: 109) |
| Páginas con texto | 103/110 |
| Control chars ratio | 0.000822 |
| Mojibake | 0 |
| Near limit | no |
| Tramos generados | 5 (`tramo_001_025.txt` … `tramo_101_110.txt`) |
| Manifest | `corpus/intermedios/11362/39367/tramos_endpoint/manifest.json` |
| Revisión visual | **No requerida** |

---

## Bloqueos

Ninguno. Los tres documentos están aptos para enriquecimiento.

## Rutas de artefactos

```
corpus/intermedios/11362/
├── 39286/
│   ├── texto.txt
│   ├── preflight_endpoint.json
│   └── tramos_endpoint/
│       ├── manifest.json
│       ├── tramo_001_025.txt
│       ├── tramo_026_050.txt
│       ├── tramo_051_075.txt
│       └── tramo_076_078.txt
├── 39360/
│   ├── texto.txt
│   ├── preflight_endpoint.json
│   └── tramos_endpoint/
│       ├── manifest.json
│       ├── tramo_001_025.txt
│       ├── tramo_026_050.txt
│       └── tramo_051_070.txt
└── 39367/
    ├── texto.txt
    ├── preflight_endpoint.json
    └── tramos_endpoint/
        ├── manifest.json
        ├── tramo_001_025.txt
        ├── tramo_026_050.txt
        ├── tramo_051_075.txt
        ├── tramo_076_100.txt
        └── tramo_101_110.txt
```
