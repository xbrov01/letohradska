# -*- coding: utf-8 -*-
import os, sys, xlrd, docx

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\nikan\Documents"
spol_dir = None
for name in os.listdir(base_dir):
    if "spole" in name.lower():
        spol_dir = os.path.join(base_dir, name)
        break

# 1. Get co-owners list from Vyúčtování FO 2023.xls sheet 'Podíl - 1,2,3,101,102'
fp_xls = os.path.join(spol_dir, "2023", "Vyúčtování FO 2023.xls")
coowners = []
if os.path.exists(fp_xls):
    book = xlrd.open_workbook(fp_xls)
    sheet = book.sheet_by_name("Podíl - 1,2,3,101,102")
    for rx in range(sheet.nrows):
        row = sheet.row_values(rx)
        # Look for rows with names / units
        row_str = " | ".join(str(v).strip() for v in row if str(v).strip())
        if rx > 3 and len(row) > 2 and row[1]:
            name = str(row[1]).strip()
            if name and not any(k in name.lower() for k in ['celkem', 'spoluvlastník', 'jméno', 'příjmení']):
                coowners.append((str(row[0]).strip(), name))

print(f"Co-owners found in excel: {len(coowners)}")
for u, n in coowners:
    print(f"  Unit/ID: {u} | {n}")
