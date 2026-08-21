import json
import os

def final_manual_fix():
    base_dir = r'C:\Users\abustamante\Cepal-lab\experimentos\cambio_climatico\fase2\corpus\intermedios\11362\44056'
    json_path = os.path.join(base_dir, 'borrador_preprueba.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    def find_and_fix(sections):
        for s in sections:
            # Fix INCAP 6 (Avoiding OCR tokens like ECHAM4)
            if s['seccion'].startswith('6. Efecto en la calidad y cantidad del agua'):
                s['dimensiones'][0]['cita'] = "La disponibilidad de agua de calidad para la producción, consumo, higiene y manejo de los alimentos, especialmente en zonas áridas, también disminuirá."
            
            # Fix PROGRESAN 1 (Shorter, more likely to be literal)
            if s['seccion'].startswith('E. Monitoreo y evaluacion') and s['nivel'] == 2:
                s['dimensiones'][0]['cita'] = "formar a los meteorólogos con ayuda de las instituciones, incluir en la agenda de adaptación el tema de inversión pública en la infraestructura"

            # Fix PROGRESAN 2
            if s['seccion'].startswith('2. Metodologías y enfoques analíticos'):
                s['dimensiones'][0]['cita'] = "Kakwani (1989) fue el primero en desarrollar un procedimiento para separar ambos efectos con una técnica de descomposición estática"

            if s.get('subsecciones'):
                find_and_fix(s['subsecciones'])

    find_and_fix(data['resumen_secciones'])
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    final_manual_fix()
