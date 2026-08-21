import json
import re

def check_quote(quote, page, filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # find page marker
    page_marker = f"=== PÁGINA PDF {page} ==="
    next_page_marker = f"=== PÁGINA PDF {page+1} ==="
    
    pos = text.find(page_marker)
    if pos == -1:
        print(f"ERROR: Page marker {page_marker} not found in {filepath}")
        return False
        
    next_pos = text.find(next_page_marker, pos)
    page_text = text[pos:next_pos] if next_pos != -1 else text[pos:]
    
    # clean whitespaces
    norm_quote = " ".join(quote.split())
    norm_page_text = " ".join(page_text.split())
    
    if norm_quote in norm_page_text:
        print(f"OK [p.{page}]: {norm_quote[:60]}...")
        return True
    else:
        print(f"FAILED [p.{page}]: Quote not found in page text!")
        print(f"Searched: {norm_quote}")
        return False

# Test run
print("Verifying quote tester...")
