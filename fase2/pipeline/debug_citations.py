import glob
import re

tramos = sorted(glob.glob('corpus/intermedios/11362/42140/tramos/tramo_*.txt'))

queries = [
    "generación de electricidad a partir de combustibles",
    "42,8%",
    "flota vehicular",
    "intensidad energética del PIB",
    "resultados validan la tendencia",
    "conglomerados, que",
    "Cuentas de Energía",
    "Banco de Guatemala pusieron",
    "99,7",
    "pese a conocer las consecuencias"
]

print("Searching queries in tramos:")
for q in queries:
    print(f"\n--- QUERY: {q} ---")
    found = False
    for fpath in tramos:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        pos = content.lower().find(q.lower())
        if pos != -1:
            found = True
            # Find closest previous page marker
            markers = list(re.finditer(r'=== PÁGINA (?:PDF|IMPRESA) (\d+) ===', content))
            page = "unknown"
            for i, m in enumerate(markers):
                if pos >= m.start() and (i == len(markers)-1 or pos < markers[i+1].start()):
                    page = m.group(1)
            print(f"Found in {fpath} on Page {page}:")
            snippet = content[max(0, pos-100):min(len(content), pos+250)]
            print(repr(snippet.strip()))
    if not found:
        print("NOT FOUND ANYWHERE!")
