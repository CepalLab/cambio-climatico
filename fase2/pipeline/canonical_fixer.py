import json
import os
import sys
import re
from collections import OrderedDict

def reorder_section(sec):
    """Reordena las claves de una sección y sus subsecciones recursivamente."""
    key_order = ["seccion", "nivel", "paginas", "resumen", "dimensiones", "subsecciones"]
    
    # Limpiar dimensiones: quitar campos extra como 'texto'
    if "dimensiones" in sec:
        clean_dims = []
        for d in sec["dimensiones"]:
            d_ordered = OrderedDict()
            # Orden para dimensiones: dimension, cita, pagina, subtipo_brecha
            for k in ["dimension", "cita", "pagina", "subtipo_brecha"]:
                if k in d:
                    d_ordered[k] = d[k]
            clean_dims.append(d_ordered)
        sec["dimensiones"] = clean_dims

    # Ordenar claves de la sección
    new_sec = OrderedDict()
    for k in key_order:
        if k in sec:
            if k == "subsecciones" and sec[k]:
                new_sec[k] = [reorder_section(sub) for sub in sec[k]]
            else:
                new_sec[k] = sec[k]
        elif k == "subsecciones":
            new_sec[k] = []
    return new_sec

def reorder_tipologia(tip):
    """Reordena las claves del objeto tipologia y razonamiento_5_pasos."""
    if not isinstance(tip, dict):
        return tip
    
    # 1. Orden para razonamiento_5_pasos
    if "razonamiento_5_pasos" in tip and isinstance(tip["razonamiento_5_pasos"], dict):
        r5 = tip["razonamiento_5_pasos"]
        r5_order = ["tension_dialectica", "filtro_categoria_primaria", "secundaria_obligatoria", "justificacion_anti_copia", "validacion_anclas"]
        new_r5 = OrderedDict()
        for k in r5_order:
            if k in r5:
                new_r5[k] = r5[k]
        tip["razonamiento_5_pasos"] = new_r5

    # 2. Orden para tipologia
    tip_order = [
        "transformacion_primaria", 
        "transformacion_secundaria", 
        "razonamiento_5_pasos", 
        "tipo_documento_climatico", 
        "nivel_aplicacion", 
        "ambiguedad_pendiente_validacion"
    ]
    new_tip = OrderedDict()
    for k in tip_order:
        if k in tip:
            new_tip[k] = tip[k]
    
    # Mantener claves extra al final
    for k in tip:
        if k not in tip_order:
            new_tip[k] = tip[k]
            
    return new_tip

def fix_json_file(file_path):
    if not os.path.exists(file_path):
        return False, f"Archivo no encontrado: {file_path}"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 1. Limpieza de secciones
        if "resumen_secciones" in data:
            data["resumen_secciones"] = [reorder_section(s) for s in data["resumen_secciones"]]
        
        # 2. Reordenar tipologia
        if "tipologia" in data:
            data["tipologia"] = reorder_tipologia(data["tipologia"])

        # 3. Orden de claves principales
        key_order = ["documento", "resumen_enriquecido", "resumen_secciones", "interpelacion", "tipologia"]
        new_data = OrderedDict()
        
        for k in key_order:
            if k in data:
                new_data[k] = data[k]
        
        # Mantener cualquier otra clave al final
        for k in data:
            if k not in key_order:
                new_data[k] = data[k]

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=2, ensure_ascii=False)
        
        return True, "OK"
    except Exception as e:
        return False, str(e)

def main():
    if len(sys.argv) < 2:
        print("Uso: python pipeline/canonical_fixer.py <ID1> <ID2> ...")
        sys.exit(1)

    ids = sys.argv[1:]
    
    for doc_id in ids:
        print(f"Procesando ID {doc_id}...")
        
        # Rutas posibles
        paths = [
            f"corpus/resultados/json/doc_{doc_id}.json",
            f"corpus/resultados/borrador_{doc_id}.json",
            f"corpus/intermedios/11362/{doc_id}/borrador_preprueba.json"
        ]
        
        found_any = False
        for p in paths:
            success, msg = fix_json_file(p)
            if success:
                print(f"  [FIXED] {p}")
                found_any = True
            elif "no encontrado" not in msg.lower():
                print(f"  [ERROR] {p}: {msg}")
        
        if not found_any:
            print(f"  [WARN] No se encontraron archivos para el ID {doc_id}")

if __name__ == "__main__":
    main()
