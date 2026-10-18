# -*- coding: utf-8 -*-
import os, sys, re

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\nikan\Documents"
spol_dir = None
for name in os.listdir(base_dir):
    if "spole" in name.lower():
        spol_dir = os.path.join(base_dir, name)
        break

def get_file_path(filename):
    for root, dirs, files in os.walk(spol_dir):
        for f in files:
            if f.lower() == filename.lower():
                return os.path.join(root, f)
    return None

def extract_clean_text(fp):
    with open(fp, 'rb') as f:
        data = f.read()
    t16 = data.decode('utf-16le', errors='ignore')
    t8 = data.decode('cp1250', errors='ignore')
    score16 = sum(1 for w in ['nájem', 'smlouva', 'pronajímatel', 'korun', 'článek', 'měsíc'] if w in t16.lower())
    score8 = sum(1 for w in ['nájem', 'smlouva', 'pronajímatel', 'korun', 'článek', 'měsíc'] if w in t8.lower())
    raw = t16 if score16 >= score8 else t8
    cleaned = []
    for line in raw.splitlines():
        line_clean = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', line).strip()
        if len(line_clean) > 3:
            cleaned.append(line_clean)
    return '\n'.join(cleaned)

files_to_check = [
    "101DDAANN2022.doc",
    "102Kopecky2024.doc",
    "2Kopecký2024.doc",
    "3 Onari.doc",
    "3367sklep.doc"
]

for name in files_to_check:
    fp = get_file_path(name)
    print(f"\n{'='*65}\nSOUBOR: {name}\nCESTA: {fp}\n{'='*65}")
    if not fp:
        print("Soubor nenalezen!")
        continue
    text = extract_clean_text(fp)
    has_inf = 'infla' in text.lower()
    print(f"Obsahuje slovo inflace: {'*** ANO ***' if has_inf else 'NE'}")
    
    # Print relevant sections
    lines = text.splitlines()
    for l in lines:
        ll = l.lower()
        if any(k in ll for k in ['čl. 4', 'čl. 5', 'čl. 6', 'čl. 7', 'nájemné', 'inflac', 'doba nájmu', 'výpověd', 'výpověď', 'zvyš']):
            print("  >>>", l)
