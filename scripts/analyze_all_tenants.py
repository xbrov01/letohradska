# -*- coding: utf-8 -*-
import os, sys, zipfile, re
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\nikan\Documents"

# Find Společenství folder dynamically
spol_dir = None
for name in os.listdir(base_dir):
    if "spole" in name.lower():
        spol_dir = os.path.join(base_dir, name)
        break

print(f"Společenství dir: {spol_dir}")

def extract_text_from_doc(path):
    try:
        with open(path, 'rb') as f:
            data = f.read()
        t1 = data.decode('cp1250', errors='ignore')
        t2 = data.decode('utf-16le', errors='ignore')
        # Let's clean up
        def clean(s):
            chunks = re.findall(r'[\w\s.,;:/\-–—()"\'+%#@!?§€Kč]+', s)
            return ' '.join(c for c in chunks if len(c.strip()) > 3)
        c1 = clean(t1)
        c2 = clean(t2)
        return c2 if len(c2) > len(c1) else c1
    except Exception as e:
        return f"Error: {e}"

def extract_text_from_odt(path):
    try:
        with zipfile.ZipFile(path) as z:
            content = z.read('content.xml')
            root = ET.fromstring(content)
            return ' '.join(root.itertext())
    except Exception as e:
        return f"Error: {e}"

def extract_text_from_docx(path):
    try:
        with zipfile.ZipFile(path) as z:
            content = z.read('word/document.xml')
            root = ET.fromstring(content)
            return ' '.join(root.itertext())
    except Exception as e:
        return f"Error: {e}"

# Walk and collect all contract-like files
contracts = []
for root, dirs, files in os.walk(spol_dir):
    for f in files:
        fl = f.lower()
        if any(w in fl for w in ['kopeck', 'ddaann', 'onari', 'ladova', 'smlouv', 'sklep', 'bosch']):
            ext = os.path.splitext(f)[1].lower()
            if ext in ['.doc', '.docx', '.odt']:
                contracts.append(os.path.join(root, f))

print(f"Found {len(contracts)} matching files.")
for cp in contracts:
    fn = os.path.basename(cp)
    print(f"\n==================================================")
    print(f"SOUBOR: {fn}")
    print(f"CESTA: {cp}")
    print(f"==================================================")
    ext = os.path.splitext(fn)[1].lower()
    if ext == '.odt':
        text = extract_text_from_odt(cp)
    elif ext == '.docx':
        text = extract_text_from_docx(cp)
    elif ext == '.doc':
        text = extract_text_from_doc(cp)
    else:
        continue
    
    # Check inflation
    has_inflation = 'infla' in text.lower()
    print(f"-> Obsahuje 'inflac...': {'*** ANO ***' if has_inflation else 'NE'}")
    
    # Print paragraphs mentioning rent, inflation, or duration
    # Split by common sentence / paragraph markers
    paragraphs = re.split(r'\n+|\r+|(?<=[.?!;])\s{2,}', text)
    for p in paragraphs:
        p_clean = ' '.join(p.split())
        pl = p_clean.lower()
        if any(k in pl for k in ['infla', 'nájemné činí', 'nájemné ve výši', 'výše nájemného', 'měsíční nájemné', 'doba nájmu', 'se uzavírá na dobu', 'zvýš', 'zvyš', 'revaloriz']):
            print(f"  [TEXT]: {p_clean}\n")
