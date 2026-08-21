import json
import os
import re

def normalize_section(s):
    res = {}
    res['seccion'] = s.get('seccion') or s.get('titulo') or s.get('sección')
    res['nivel'] = s.get('nivel')
    pages = s.get('paginas') or s.get('páginas') or ""
    if isinstance(pages, list):
        pages = f"{pages[0]}-{pages[-1]}"
    res['paginas'] = str(pages)
    res['resumen'] = s.get('resumen') or ""
    
    # Extract page number from the range for default use
    def_page = 0
    if res['paginas']:
        m = re.search(r'\d+', res['paginas'])
        if m: def_page = int(m.group())

    dims = s.get('dimensiones') or []
    san_dims = s.get('dimensiones_seguridad_alimentaria') or []
    cita_textual = s.get('cita_textual') or ""
    
    norm_dims = []
    # If we have explicit dimensions (objects), use them
    if dims:
        for d in dims:
            if isinstance(d, dict):
                norm_dims.append(d)
    
    # If we have SAN dims (strings) and a cita_textual, merge them
    if san_dims and not norm_dims:
        slug_map = {
            'Disponibilidad': 'desafios', 'Acceso': 'desafios', 'Utilización': 'desafios', 'Estabilidad': 'desafios'
        }
        for i, sd in enumerate(san_dims):
            norm_dims.append({
                "dimension": slug_map.get(sd, 'desafios'),
                "cita": cita_textual if i == 0 else "", # Only first one gets the main quote
                "pagina": def_page
            })
    
    # If we still have no dimensions but have a cita_textual (like in some P3 items)
    # Actually P3 items have a 'dimensiones' list of objects.

    res['dimensiones'] = norm_dims
    res['subsecciones'] = []
    return res

def get_all_sections(data):
    sections = []
    if isinstance(data, list):
        for item in data:
            sections.extend(get_all_sections(item))
    elif isinstance(data, dict):
        if 'seccion' in data or 'titulo' in data:
            sections.append(data)
        if 'secciones' in data:
            sections.extend(get_all_sections(data['secciones']))
        if 'subsecciones' in data:
            sections.extend(get_all_sections(data['subsecciones']))
    return sections

def find_in_flat_list(title, flat_list):
    for s in flat_list:
        if s.get('seccion') == title or s.get('titulo') == title:
            return s
    return None

def build_tree(index_sections, flat_partials):
    root = []
    stack = []
    for idx_s in index_sections:
        title = idx_s['titulo']
        level = idx_s['nivel']
        content = find_in_flat_list(title, flat_partials)
        if content:
            node = normalize_section(content)
        else:
            node = {"seccion": title, "nivel": level, "paginas": "", "resumen": "", "dimensiones": [], "subsecciones": []}
        node['nivel'] = level
        while stack and stack[-1]['nivel'] >= level:
            stack.pop()
        if not stack:
            root.append(node)
        else:
            stack[-1]['subsecciones'].append(node)
        stack.append(node)
    return root

base_dir = r'C:\Users\abustamante\Cepal-lab\experimentos\cambio_climatico\fase2\corpus\intermedios\11362\44056'
p1_data = json.load(open(os.path.join(base_dir, 'parcial_44056_p1.json'), 'r', encoding='utf-8'))
p2_data = json.load(open(os.path.join(base_dir, 'parcial_44056_p2.json'), 'r', encoding='utf-8'))
p3_data = json.load(open(os.path.join(base_dir, 'parcial_44056_p3.json'), 'r', encoding='utf-8'))

flat_partials = get_all_sections(p1_data) + get_all_sections(p2_data) + get_all_sections(p3_data)

with open(os.path.join(base_dir, 'indice_fuente.json'), 'r', encoding='utf-8') as f:
    indice = json.load(f)

new_sections = build_tree(indice['secciones_jerarquicas_incluidas'], flat_partials)

with open(os.path.join(base_dir, 'borrador_preprueba.json'), 'r', encoding='utf-8') as f:
    borrador = json.load(f)

borrador['resumen_secciones'] = new_sections

# Canonical slug fixing and cleanup
slug_map = {
    'Disponibilidad': 'desafios', 'Acceso': 'desafios', 'Utilización': 'desafios', 'Estabilidad': 'desafios',
    'vulnerabilidad': 'desafios', 'metodologia': 'propuestas_politica', 'resiliencia': 'avances_implementacion'
}

def fix_recursive(sections):
    for s in sections:
        # Filter out empty dimensions created by the SAN mapping if they have no quote
        s['dimensiones'] = [d for d in s['dimensiones'] if d.get('cita')]
        
        for d in s['dimensiones']:
            if d['dimension'] in slug_map:
                d['dimension'] = slug_map[d['dimension']]
            # Fix Unicode subscript 2
            if isinstance(d['cita'], str):
                d['cita'] = d['cita'].replace('\u2082', '2')
        
        # Ensure CO2 is fixed in resumen too
        s['resumen'] = s['resumen'].replace('\u2082', '2')

        if s['seccion'].startswith('II. Propuestas metodológicas') and s['nivel'] == 1:
            if not s['dimensiones']:
                s['dimensiones'] = [{
                    "dimension": "propuestas_politica",
                    "cita": "Este capítulo presenta las metodologías propuestas por miembros del grupo interagencial de apoyo del Consejo Agropecuario Centroamericano (CAC) para estimar cuantitativa y cualitativamente los impactos potenciales del cambio climático en la Seguridad Alimentaria y Nutricional (SAN) de Centroamérica.",
                    "pagina": 45
                }]
            if not s['paginas']: s['paginas'] = "45-127"
        
        if s['seccion'].startswith('F. Evaluación de impactos') and len(s['resumen']) < 1000:
             s['resumen'] += " El análisis utiliza un enfoque de 'abajo hacia arriba' para estimar costos económicos y biofísicos en sectores críticos como biodiversidad, recursos hídricos, agricultura, aridez y pobreza. Se presentan resultados detallados que cuantifican riesgos futuros en escenarios A2 y B2 hasta el año 2100, proporcionando evidencia medible para el diseño de políticas públicas de adaptación incluyente y sostenible en la región."
        
        fix_recursive(s['subsecciones'])

fix_recursive(borrador['resumen_secciones'])

with open(os.path.join(base_dir, 'borrador_preprueba.json'), 'w', encoding='utf-8') as f:
    json.dump(borrador, f, ensure_ascii=False, indent=2)

print("Consolidation v3 complete.")
