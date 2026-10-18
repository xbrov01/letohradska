# -*- coding: utf-8 -*-
import os, sys, xlrd

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\nikan\Documents"
spol_dir = None
for name in os.listdir(base_dir):
    if "spole" in name.lower():
        spol_dir = os.path.join(base_dir, name)
        break

files = [
    os.path.join(spol_dir, "přeplatky nedoplatky.xls"),
    os.path.join(spol_dir, "kontrola úhrady nájemného.xls"),
    os.path.join(spol_dir, "Platby.xls"),
    os.path.join(spol_dir, "2024", "Náklady na opravy, údržbu a správu 2024.xls"),
    os.path.join(spol_dir, "2023", "Vyúčtování FO 2023.xls"),
]

for fp in files:
    if not os.path.exists(fp):
        continue
    print(f"\n{'='*75}\nFILE: {os.path.basename(fp)}\n{'='*75}")
    try:
        book = xlrd.open_workbook(fp)
        for sname in book.sheet_names():
            print(f"--- Sheet: {sname} ---")
            sheet = book.sheet_by_name(sname)
            for rx in range(sheet.nrows):
                row = sheet.row_values(rx)
                row_str = " | ".join(str(v).strip() for v in row if str(v).strip())
                # filter rows
                if any(w in row_str.lower() for w in ['výnos', 'podíl', 'nevyplac', 'soldát', 'sebera', 'andělov', 'hábov', 'mandelík', 'večeř', 'celkem']):
                    print(f"  R{rx:02d}: {row_str}")
    except Exception as e:
        print(f"Error reading {fp}: {e}")
