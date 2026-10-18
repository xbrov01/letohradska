# -*- coding: utf-8 -*-
import os, sys, re

base_dir = r"C:\Users\nikan\Documents"
spol_dir = None
for name in os.listdir(base_dir):
    if "spole" in name.lower():
        spol_dir = os.path.join(base_dir, name)
        break

def extract_all_text(path):
    with open(path, 'rb') as f:
        data = f.read()
    # decode utf-16le and cp1250
    # in Word .doc, text runs are either 8-bit or 16-bit
    s16 = data.decode('utf-16le', errors='ignore')
    s8 = data.decode('cp1250', errors='ignore')
    
    # filter readable chunks
    chunks16 = re.findall(r'[\w\s.,;:/\-–—()"\'+%#@!?§€Kč]{5,}', s16)
    chunks8 = re.findall(r'[\w\s.,;:/\-–—()"\'+%#@!?§€Kč]{5,}', s8)
    
    t16 = ' '.join(chunks16)
    t8 = ' '.join(chunks8)
    return t16 if len(t16) > len(t8) else t8

out_path = r"c:\Users\nikan\data\svj\scripts\contract_dump.txt"

with open(out_path, 'w', encoding='utf-8') as out:
    for root, dirs, files in os.walk(spol_dir):
        for f in files:
            if f.lower().endswith(('.doc', '.docx', '.odt')) and any(k in f.lower() for k in ['ddaann', 'kopeck', 'onari', 'ladov', 'sklep', 'bosch']):
                fp = os.path.join(root, f)
                out.write(f"\n{'='*70}\nFILE: {f}\nPATH: {fp}\n{'='*70}\n")
                txt = extract_all_text(fp)
                out.write(f"HAS INFLACE: {'infla' in txt.lower()}\n")
                out.write(txt + "\n\n")

print("Dump finished to contract_dump.txt")
