# -*- coding: utf-8 -*-
import openpyxl, sys

sys.stdout.reconfigure(encoding='utf-8')

fp = r"C:\Users\nikan\Documents\Společenství\Výpisy\Vypisy_2026_Komplet.xlsx"
wb = openpyxl.load_workbook(fp, data_only=True)

print("=== VŠECHNY VÝDAJE V ÚNORU, BŘEZNU A DUBNU 2026 ===")
for sname in ['Výpis 002', 'Výpis 003', 'Výpis 004', 'Výpis 005', 'Výpis 006']:
    ws = wb[sname]
    for r in range(12, ws.max_row + 1):
        vydaj = ws.cell(r, 12).value
        if vydaj is not None and vydaj < 0:
            datum = ws.cell(r, 2).value
            nazev = ws.cell(r, 6).value
            popis = ws.cell(r, 7).value
            vs = ws.cell(r, 8).value
            protiucet = ws.cell(r, 5).value
            print(f"{datum} | {vydaj:>10} Kč | Protiúčet: {protiucet} | Název: {str(nazev)[:30]} | Popis: {str(popis)[:40]} | VS: {vs}")
