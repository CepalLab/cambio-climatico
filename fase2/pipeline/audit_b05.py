import json
import os

filepath = "corpus/intermedios/11362/45023/parcial_B05_CAP_III_P3_CONCL.json"
with open(filepath, "r", encoding="utf-8") as f:
    data = json.load(f)

tramo_dir = "corpus/intermedios/11362/45023/tramos"

total_sections = 0
leaf_sections = 0
total_dimensions = 0
total_citations = 0

all_valid = True

def inspect_section(s):
    global total_sections, leaf_sections, total_dimensions, total_citations, all_valid
    total_sections += 1
    subs = s.get("subsecciones", [])
    dims = s.get("dimensiones", [])
    
    if not subs:
        leaf_sections += 1
        
    for d in dims:
        total_dimensions += 1
        total_citations += 1
        quote = d.get("cita", "")
        page = d.get("pagina", 0)
        
        # Check page range
        if not (231 <= page <= 262):
            print(f"ERROR: Page {page} out of block range (231-262) for section {s.get('seccion')}")
            all_valid = False
            
        # Verify citation in tramos
        if 226 <= page <= 250:
            tf = os.path.join(tramo_dir, "tramo_226_250.txt")
        else:
            tf = os.path.join(tramo_dir, "tramo_251_268.txt")
            
        with open(tf, "r", encoding="utf-8") as tf_in:
            c = tf_in.read()
            
        pm = f"=== PÁGINA PDF {page} ==="
        npm = f"=== PÁGINA PDF {page+1} ==="
        p_start = c.find(pm)
        p_end = c.find(npm, p_start) if p_start != -1 else -1
        p_text = c[p_start:p_end] if (p_start != -1 and p_end != -1) else c[p_start:]
        
        norm_q = " ".join(quote.split())
        norm_t = " ".join(p_text.split())
        
        if norm_q not in norm_t:
            print(f"ERROR: Citation not found on p.{page}: {norm_q[:60]}...")
            all_valid = False

    for sub in subs:
        inspect_section(sub)

for s in data["resumen_secciones"]:
    inspect_section(s)

print(f"Total Secciones: {total_sections}")
print(f"Secciones Hoja: {leaf_sections}")
print(f"Total Dimensiones: {total_dimensions}")
print(f"Total Citas: {total_citations}")
print(f"All citations strictly in range and verified: {all_valid}")
