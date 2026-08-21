import json
import os

def manual_fix():
    base_dir = r'C:\Users\abustamante\Cepal-lab\experimentos\cambio_climatico\fase2\corpus\intermedios\11362\44056'
    json_path = os.path.join(base_dir, 'borrador_preprueba.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    def find_and_fix(sections):
        for s in sections:
            # Fix Chapter II Nivel 1
            if s['seccion'].startswith('II. Propuestas metodológicas') and s['nivel'] == 1:
                s['dimensiones'][0]['cita'] = "presenta las metodologías propuestas por miembros del grupo interagencial de apoyo del Consejo Agropecuario Centroamericano (CAC) para estimar cuantitativa y cualitativamente los impactos potenciales del cambio climático en la Seguridad Alimentaria"
            
            # Fix INCAP 6
            if s['seccion'].startswith('6. Efecto en la calidad y cantidad del agua'):
                s['dimensiones'][0]['cita'] = "Para estimar el IA en los escenarios de cambio climático hasta 2100 se utilizaron los promedios de los modelos ECHAM4 y HADCM3 (para B2) y ECHAM4 y HADGEM (para A2). Para identificar la tendencia con mayor claridad se calculó el IA para cada año de corte: 2020, 2030, 2050, 2070 y 2100."
            
            # Fix PROGRESAN 1
            if s['seccion'].startswith('E. Monitoreo y evaluacion') and s['nivel'] == 2:
                s['dimensiones'][0]['cita'] = "informar sobre el valor nutricional en la salud, formar a los meteorólogos con ayuda de las instituciones, incluir en la agenda de adaptación el tema de inversión pública en la infraestructura agrícola frente al cambio climático, y crear una red científico-técnica para la SAN y la acción climática."

            # Fix PROGRESAN 2
            if s['seccion'].startswith('2. Metodologías y enfoques analíticos'):
                s['dimensiones'][0]['cita'] = "Kakwani (1989) fue el primero en desarrollar un procedimiento para separar ambos efectos con una técnica de descomposición estática que permite computar coeficientes de elasticidad para medir la sensibilidad de la tasa de pobreza ante variaciones porcentuales del PIB por habitante y de la desigualdad."

            if s.get('subsecciones'):
                find_and_fix(s['subsecciones'])

    find_and_fix(data['resumen_secciones'])
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    manual_fix()
