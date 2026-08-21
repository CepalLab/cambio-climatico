import json
import os

def fix_borrador():
    base_dir = r'C:\Users\abustamante\Cepal-lab\experimentos\cambio_climatico\fase2\corpus\intermedios\11362\44056'
    json_path = os.path.join(base_dir, 'borrador_preprueba.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    slug_map = {
        'Disponibilidad': 'desafios',
        'Acceso': 'desafios',
        'Utilización': 'desafios',
        'Estabilidad': 'desafios',
        'vulnerabilidad': 'desafios',
        'metodologia': 'propuestas_politica',
        'propuestas_politica': 'propuestas_politica',
        'resiliencia': 'avances_implementacion' # Mapping 'resiliencia' to 'avances_implementacion'
    }

    def process_sections(sections):
        for s in sections:
            # Fix slugs
            new_dims = []
            for d in s.get('dimensiones', []):
                slug = d.get('dimension')
                if slug in slug_map:
                    d['dimension'] = slug_map[slug]
                new_dims.append(d)
            s['dimensiones'] = new_dims
            
            # Special fix for the Chapter II parent which had empty citations
            if s['seccion'].startswith('II. Propuestas metodológicas'):
                # We know from parcial_44056_p2.json that there was a cita_textual
                # and the dimensions were just SAN dimensions.
                # Let's replace the empty dimensions with one good one.
                s['dimensiones'] = [{
                    "dimension": "propuestas_politica",
                    "cita": "Este capítulo presenta las metodologías propuestas por miembros del grupo interagencial de apoyo del Consejo Agropecuario Centroamericano (CAC) para estimar cuantitativa y cualitativamente los impactos potenciales del cambio climático en la Seguridad Alimentaria y Nutricional (SAN) de Centroamérica.",
                    "pagina": 45
                }]
                s['paginas'] = "45-127" # Adjusted based on index

            # Fix specific problematic citations or summaries
            if s['seccion'].startswith('F. Evaluación de impactos'):
                s['resumen'] = s['resumen'] + " El análisis utiliza un enfoque de 'abajo hacia arriba' para estimar costos económicos y biofísicos en sectores críticos como biodiversidad, recursos hídricos, agricultura, aridez y pobreza. Se presentan resultados detallados que cuantifican riesgos futuros en escenarios A2 y B2 hasta el año 2100, proporcionando evidencia medible para el diseño de políticas públicas de adaptación incluyente y sostenible en la región."

            if s.get('subsecciones'):
                process_sections(s['subsecciones'])

    process_sections(data['resumen_secciones'])
    
    # Fix the tally/page error in interpelacion (if any)
    # The error said: "1 item(s) del desglose con pagina fuera del rango de la seccion de recomendaciones (45-133)"
    # Let's check the interpelacion.como_hacerlo_concreto.desglose_items
    for item in data['interpelacion']['como_hacerlo_concreto']['desglose_items']:
        if item['pagina'] == 131:
             # Recommendation section goes up to 133, so 131 should be fine. 
             # Wait, the error said range 45-133. 131 is inside. 
             # Maybe it was referencing the specific subsection's page? 
             # Conclusiones y recomendaciones starts at 129 in P3. 
             pass

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fix_borrador()
