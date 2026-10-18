# -*- coding: utf-8 -*-
import pypdf, sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"C:\Users\nikan\Documents\Společenství\2025\Přehled podílů na výnosech 2025.pdf"
reader = pypdf.PdfReader(pdf_path)
print(f"Total pages: {len(reader.pages)}")
for i, page in enumerate(reader.pages):
    print(f"\n--- PAGE {i+1} ---")
    txt = page.extract_text()
    for line in txt.splitlines():
        print(line)
