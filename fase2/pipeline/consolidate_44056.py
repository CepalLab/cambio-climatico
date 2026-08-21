import json
import os

def normalize_section(s):
    # Normalize keys to 'seccion', 'nivel', 'paginas', 'resumen', 'dimensiones', 'subsecciones'
    res = {}
    res['seccion'] = s.get('seccion') or s.get('titulo') or s.get('sección')
    res['nivel'] = s.get('nivel')
    res['paginas'] = s.get('paginas') or s.get('páginas')
    res['resumen'] = s.get('resumen')
    res['dimensiones'] = s.get('dimensiones') or s.get('dimensiones_seguridad_alimentaria') or []
    
    # Handle dimensions format (normalize to list of objects if they are just strings)
    norm_dims = []
    for d in res['dimensiones']:
        if isinstance(d, str):
            # This shouldn't happen based on partials, but just in case
            norm_dims.append({"dimension": d, "cita": "", "pagina": 0})
        else:
            norm_dims.append(d)
    res['dimensiones'] = norm_dims
    
    res['subsecciones'] = []
    # We will handle subsecciones separately during tree building
    return res

def find_in_partials(title, partials):
    for p in partials:
        for s in p.get('secciones', []):
            if s.get('seccion') == title or s.get('titulo') == title:
                return s
    return None

def build_tree(index_sections, partials):
    root = []
    stack = []
    
    for idx_s in index_sections:
        title = idx_s['titulo']
        level = idx_s['nivel']
        
        # Find content in partials
        content = find_in_partials(title, partials)
        if content:
            node = normalize_section(content)
        else:
            # Create empty node if not found (should not happen for core sections)
            node = {
                "seccion": title,
                "nivel": level,
                "paginas": "",
                "resumen": "",
                "dimensiones": [],
                "subsecciones": []
            }
        
        # Re-assign level from index to be sure
        node['nivel'] = level
        
        # Adjust stack to find parent
        while stack and stack[-1]['nivel'] >= level:
            stack.pop()
        
        if not stack:
            root.append(node)
        else:
            stack[-1]['subsecciones'].append(node)
        
        stack.append(node)
        
    return root

# Load files
base_dir = r'C:\Users\abustamante\Cepal-lab\experimentos\cambio_climatico\fase2\corpus\intermedios\11362\44056'
with open(os.path.join(base_dir, 'indice_fuente.json'), 'r', encoding='utf-8') as f:
    indice = json.load(f)

with open(os.path.join(base_dir, 'parcial_44056_p1.json'), 'r', encoding='utf-8') as f:
    p1 = {"secciones": json.load(f)}

with open(os.path.join(base_dir, 'parcial_44056_p2.json'), 'r', encoding='utf-8') as f:
    p2 = json.load(f) # Already a dict with 'secciones'

with open(os.path.join(base_dir, 'parcial_44056_p3.json'), 'r', encoding='utf-8') as f:
    p3 = json.load(f) # Already a dict with 'secciones'

with open(os.path.join(base_dir, 'borrador_preprueba.json'), 'r', encoding='utf-8') as f:
    borrador = json.load(f)

# Consolidate sections
all_partials = [p1, p2, p3]
new_sections = build_tree(indice['secciones_jerarquicas_incluidas'], all_partials)

# Update borrador
borrador['resumen_secciones'] = new_sections

# Save updated borrador
with open(os.path.join(base_dir, 'borrador_preprueba.json'), 'w', encoding='utf-8') as f:
    json.dump(borrador, f, ensure_ascii=False, indent=2)

print("Consolidation complete.")
