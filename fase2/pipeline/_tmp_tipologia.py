# Uso interno de la adjudicación (temporal, borrar al terminar):
# vuelca el razonamiento de 5 pasos de tipología del ejecutor en los docs disputados.
import glob
import io
import json
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
MULTI = tuple(f"_{k:02d}.json" for k in range(1, 6))

for n in (sys.argv[1:] or ["02", "04", "06", "08", "10", "12", "14", "15"]):
    ej = [p for p in glob.glob(f"fase2/pilot/doc{n}_*.json") if not p.endswith(MULTI)]
    with open(ej[0], encoding="utf-8") as f:
        t = json.load(f).get("tipologia", {})
    print("=" * 90)
    p, s = t.get("transformacion_primaria", {}), t.get("transformacion_secundaria", {})
    print(f"DOC{n}: prim=#{p.get('numero')} {p.get('nombre')} ({p.get('certeza')}) | "
          f"sec=#{s.get('numero')} {s.get('nombre')} ({s.get('certeza')})")
    r5 = t.get("razonamiento_5_pasos", {})
    for k, v in r5.items():
        print(f"  [{k}] {str(v)[:700]}")
    print(f"  [ambiguedad] {str(t.get('ambiguedad_pendiente_validacion'))[:400]}")
