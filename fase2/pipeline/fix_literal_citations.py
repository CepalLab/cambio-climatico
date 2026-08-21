import json
import os
import re
import unicodedata

def normalize(text):
    if not text: return ""
    text = unicodedata.normalize("NFKC", text).replace("\u00ad", "")
    text = re.sub(r"(?<=\w)-\s+(?=\w)", "", text)
    return re.sub(r"\s+", " ", text).strip().casefold()

def find_literal(fragment, source_raw, source_norm):
    frag_norm = normalize(fragment)
    if len(frag_norm) < 15: return fragment
    
    # Try to find the normalized fragment
    pos = source_norm.find(frag_norm)
    if pos != -1:
        # It's already literal in terms of normalized text. 
        # But we want the RAW text to preserve the original line breaks/chars if possible,
        # or at least the non-normalized version.
        # Actually, if it matches normalized, it's usually good enough for the validator
        # UNLESS the raw text has some weird chars.
        return fragment
    
    # If not found, try to find a sub-fragment
    best_match = fragment
    # Try to find the longest prefix that matches
    for i in range(len(frag_norm), 15, -5):
        sub = frag_norm[:i]
        pos = source_norm.find(sub)
        if pos != -1:
            # We found a match for a prefix. 
            # Let's take a chunk of raw text from there.
            # We need to map pos (normalized) back to raw.
            # Simple approximation:
            raw_pos = 0
            curr_norm_pos = 0
            while curr_norm_pos < pos and raw_pos < len(source_raw):
                char = source_raw[raw_pos]
                norm_char = normalize(char)
                if norm_char:
                    curr_norm_pos += len(norm_char)
                raw_pos += 1
            
            # Now take a chunk
            chunk_raw = source_raw[raw_pos : raw_pos + len(fragment) + 100]
            # Normalize the chunk and see where the frag_norm should end
            chunk_norm = normalize(chunk_raw)
            # Find the best match in chunk_norm
            # This is still fuzzy. 
            # Let's just return the chunk of raw text that matches frag_norm length
            # and clean it up.
            best_match = re.sub(r'\s+', ' ', chunk_raw[:len(fragment)]).strip()
            return best_match
            
    return fragment

def fix_all():
    base_dir = r'C:\Users\abustamante\Cepal-lab\experimentos\cambio_climatico\fase2\corpus\intermedios\11362\44056'
    json_path = os.path.join(base_dir, 'borrador_preprueba.json')
    text_path = os.path.join(base_dir, 'texto.txt')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open(text_path, 'r', encoding='utf-8') as f:
        source_raw = f.read()
    source_norm = normalize(source_raw)

    def process_sections(sections):
        for s in sections:
            for d in s.get('dimensiones', []):
                old = d['cita']
                d['cita'] = find_literal(old, source_raw, source_norm)
            if s.get('subsecciones'):
                process_sections(s['subsecciones'])

    process_sections(data['resumen_secciones'])
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fix_all()
