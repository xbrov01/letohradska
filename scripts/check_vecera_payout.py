# -*- coding: utf-8 -*-
import openpyxl, sys

sys.stdout.reconfigure(encoding='utf-8')

fp = r"C:\Users\nikan\Documents\Společenství\Výpisy\Vypisy_2026_Komplet.xlsx"
wb = openpyxl.load_workbook(fp, data_only=True)

all_tx = []
for sname in wb.sheetnames:
    if not sname.startswith("Výpis"):
        continue
    ws = wb[sname]
    for r in range(12, ws.max_row + 1):
        datum = ws.cell(r, 2).value
        prijem = ws.cell(r, 11).value
        vydaj = ws.cell(r, 12).value
        protiucet = ws.cell(r, 5).value
        nazev = ws.cell(r, 6).value
        popis = ws.cell(r, 7).value
        vs = ws.cell(r, 8).value
        if datum is not None or prijem is not None or vydaj is not None:
            all_tx.append({
                'sheet': sname,
                'datum': datum,
                'prijem': prijem,
                'vydaj': vydaj,
                'protiucet': str(protiucet).strip() if protiucet else '',
                'nazev': str(nazev).strip() if nazev else '',
                'popis': str(popis).strip() if popis else '',
                'vs': str(vs).strip() if vs else '',
            })

# Find the 30.06.2026 payment from Vecera
vecera_in = [tx for tx in all_tx if tx['prijem'] == 32632 or 'd.vecera' in tx['popis'].lower()]
print("Příchozí platba p. Večeři:")
for v in vecera_in:
    print(v)
    acc = v['protiucet']
    print(f"Účet p. Večeři: '{acc}'")
    
    # Now find all transactions with this account
    print(f"\nVšechny transakce s účtem {acc}:")
    for tx in all_tx:
        if tx['protiucet'] == acc:
            print(f"  {tx['datum']} | Příjem: {tx['prijem']} | Výdaj: {tx['vydaj']} | Popis: {tx['popis']} | VS: {tx['vs']}")

# Also let's check July / August / September expenses around the amount of shares (~20 000 - 25 000 Kč or similar)
print("\nVýdaje v červenci, srpnu a září 2026:")
for tx in all_tx:
    if tx['vydaj'] is not None and tx['vydaj'] < -1000:
        if tx['datum'] and any(m in tx['datum'] for m in ['.06.', '.07.', '.08.', '.09.']):
            print(f"  {tx['datum']} | {tx['vydaj']} Kč | Protiúčet: {tx['protiucet']} | Popis: {tx['popis']} | VS: {tx['vs']}")
