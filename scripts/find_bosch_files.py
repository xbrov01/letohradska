# -*- coding: utf-8 -*-
import os, sys

sys.stdout.reconfigure(encoding='utf-8')
base_dir = r"C:\Users\nikan\Documents"
spol_dir = None
for name in os.listdir(base_dir):
    if "spole" in name.lower():
        spol_dir = os.path.join(base_dir, name)
        break

print("Searching for files with bosch in path or content...")
for root, dirs, files in os.walk(spol_dir):
    for f in files:
        if "bosch" in f.lower():
            print("File match:", os.path.join(root, f))
