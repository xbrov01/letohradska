# -*- coding: utf-8 -*-
import os, glob, zipfile, xml.etree.ElementTree as ET

doc_dir = r"C:\Users\nikan\Documents\Společenství"

def read_odt(path):
    try:
        with zipfile.ZipFile(path) as z:
            content = z.read('content.xml')
            root = ET.fromstring(content)
            return ' '.join(root.itertext())
    except Exception as e:
        return f"Error reading odt: {e}"

def extract_strings_from_doc(path):
    try:
        with open(path, 'rb') as f:
            data = f.read()
        # Decode cp1250 and utf-16le (standard in Word doc)
        text_cp1250 = data.decode('cp1250', errors='ignore')
        text_utf16 = data.decode('utf-16le', errors='ignore')
        return text_cp1250 + "\n" + text_utf16
    except Exception as e:
        return f"Error reading doc: {e}"

print("Searching contracts...")
all_files = []
for root, dirs, files in os.walk(doc_dir):
    for f in files:
        if any(w in f.lower() for w in ['kopeck', 'ddaann', 'onari', 'ladova', 'smlouv', 'sklep', 'bosch']):
            all_files.append(os.path.join(root, f))

for fp in all_files:
    if not (fp.endswith('.doc') or fp.endswith('.docx') or fp.endswith('.odt') or fp.endswith('.pdf')):
        continue
    fn = os.path.basename(fp)
    print(f"\n==========================================")
    print(f"FILE: {fn}")
    print(f"PATH: {fp}")
    print(f"==========================================")
    
    if fp.endswith('.odt'):
        text = read_odt(fp)
    elif fp.endswith('.doc'):
        text = extract_strings_from_doc(fp)
    elif fp.endswith('.docx'):
        # docx is zip with word/document.xml
        try:
            with zipfile.ZipFile(fp) as z:
                content = z.read('word/document.xml')
                root = ET.fromstring(content)
                text = ' '.join(root.itertext())
        except Exception as e:
            text = f"Error: {e}"
    else:
        text = ""

    # Look for key sections
    for kw in ['infla', 'zvyš', 'zvýš', 'výše nájemného', 'nájemné', 'doba', 'výpověd', 'výpověď', 'revaloriz']:
        idx = 0
        found = False
        lower_text = text.lower()
        while True:
            pos = lower_text.find(kw, idx)
            if pos == -1:
                break
            found = True
            start = max(0, pos - 150)
            end = min(len(text), pos + 350)
            snippet = text[start:end].replace('\r', ' ').replace('\n', ' ')
            # clean up multiple spaces and non-printable
            snippet = ' '.join(snippet.split())
            print(f"  [{kw.upper()}] ...{snippet}...\n")
            idx = pos + len(kw) + 100
            if idx > pos + 1000: # limit snippets per keyword
                break
        if found:
            print("-" * 30)
