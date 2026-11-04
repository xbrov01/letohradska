#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automatizovaný generátor návrhů na zápis/změnu v rejstříku (or.justice.cz/ias/iform)
Používá Playwright pro interakci s Apache Wicket formulářem.
"""

import os
import sys
import json
import argparse
from typing import Dict, Any, Optional
from playwright.sync_api import sync_playwright, Page, Browser


def wait_ajax(page: Page, timeout_ms: int = 1500):
    page.wait_for_timeout(timeout_ms)


def check_feedback_errors(page: Page, step_name: str) -> list:
    err_elements = page.locator('.feedbackPanelERROR')
    errors = []
    if err_elements.count() > 0:
        for text in err_elements.all_text_contents():
            t = text.strip()
            if t:
                errors.append(t)
    if errors:
        print(f"[VAROVÁNÍ/CHYBA] {step_name} vykázal chyby formuláře: {errors}", file=sys.stderr)
    return errors


def start_or_resume_proposal(page: Page, ico: Optional[str] = None, return_code: Optional[str] = None) -> str:
    page.goto('https://or.justice.cz/ias/iform')
    page.wait_for_load_state('domcontentloaded')

    if return_code:
        print(f"-> Načítám existující rozpracovaný návrh s kódem: {return_code}...")
        input_code = page.locator('input[name*="kodProNavrat"], input[name*="navratovyKod"]').first
        input_code.fill(return_code)
        page.locator('button:has-text("Pokračovat"), input[type="submit"]:has-text("Pokračovat")').first.click()
        page.wait_for_load_state('domcontentloaded')
        wait_ajax(page, 2000)
        return return_code
    elif ico:
        print(f"-> Zahajuji nový návrh pro IČO: {ico}...")
        page.locator('input[name*="initSubjektPanel:ico"]').first.fill(ico)
        page.locator('button[type="submit"]:has-text("Vytvořit návrh"), input[type="submit"]:has-text("Vytvořit návrh")').first.click()
        page.wait_for_load_state('domcontentloaded')
        wait_ajax(page, 2500)

        code_el = page.locator('#kodProNavratValue, .kod-pro-navrat, span[id*="kodProNavrat"]').first
        captured_code = ""
        if code_el.count() > 0:
            captured_code = code_el.text_content().strip()
        print(f"-> Přidělen návratový kód: {captured_code}")
        return captured_code
    else:
        raise ValueError("Musí být zadáno buď IČO nebo návratový kód.")


def process_statutarni_organ(page: Page, config: Dict[str, Any]):
    print("-> Otevírám Předmětnou část...")
    page.locator('#predmetna-cast-0').click()
    page.wait_for_load_state('domcontentloaded')
    wait_ajax(page, 2000)

    # 1. Výmazy
    deletions = config.get("deletions", [])
    if deletions:
        del_date = deletions[0].get("date", "")
        vymaz_btns = page.locator('button[data-tooltip-data="Vymazat údaj"]')
        total_to_delete = vymaz_btns.count()
        print(f"-> Nalezeno {total_to_delete} existujících záznamů k výmazu...")

        for i in range(total_to_delete):
            btn = page.locator('button[data-tooltip-data="Vymazat údaj"]').first
            btn.click()
            wait_ajax(page, 1000)

            # Nastavení data zániku funkce (pokud existuje)
            f_sel = page.locator('select[name*="editaceFunkce:denZaniku:dateType"]')
            if f_sel.count() > 0:
                f_sel.last.select_option(value='PRESNY')
                wait_ajax(page, 300)
                f_date = page.locator('input[name*="editaceFunkce:denZaniku:dateContainer:dateField"]').last
                if f_date.count() > 0 and del_date:
                    f_date.fill(del_date)

            # Nastavení data zániku členství
            c_sel = page.locator('select[name*="editaceClenstvi:denZaniku:dateType"]').last
            c_sel.select_option(value='PRESNY')
            wait_ajax(page, 300)
            if del_date:
                page.locator('input[name*="editaceClenstvi:denZaniku:dateContainer:dateField"]').last.fill(del_date)

            # Uložit jednotlivý výmaz
            save_btn = page.locator('button:has-text("Uložit"):not(.big-button)').last
            save_btn.click()
            wait_ajax(page, 1500)
            print(f"   Úspěšně označen k výmazu záznam {i + 1}/{total_to_delete}")

    # 2. Zápisy nových / znovuzvolených členů
    additions = config.get("additions", [])
    for idx, person in enumerate(additions, 1):
        name = person.get("search_name")
        funkce = person.get("funkce", "člen výboru")
        print(f"-> Zapisuji člena: {name} ({funkce})...")

        # Výběr osoby ze subjektu
        page.locator('button:has-text("Vybrat osobu")').first.click()
        wait_ajax(page, 1000)

        match_opt = page.locator(f'div[id*="searchResult"] li:has-text("{name}")').first
        if match_opt.count() == 0:
            raise RuntimeError(f"Osoba s textem '{name}' nebyla nalezena ve výběru subjektu!")
        match_opt.click()
        wait_ajax(page, 1000)

        # Klik na opravit údaje pro zadání RČ a detailů
        page.locator('button[name*="editPersonalDataComponent:opravitButton"]').last.click()
        wait_ajax(page, 1000)

        # Doplnění rodného čísla a občanství
        if person.get("rodne_cislo"):
            page.locator('input[name*="rodneCislo"]').last.fill(person["rodne_cislo"])
        page.locator('select[name*="obcanstvi"]').last.select_option(value=person.get("obcanstvi", "Stat[293]"))
        wait_ajax(page, 300)

        # Dodatečné údaje (rodné příjmení, místo narození)
        if person.get("rodne_prijmeni"):
            page.locator('input[name*="dodatecneUdaje:rodnePrijmeni"]').last.fill(person["rodne_prijmeni"])
        page.locator('select[name*="dodatecneUdaje:statNarozeni"]').last.select_option(value=person.get("stat_narozeni", "cz"))
        wait_ajax(page, 300)

        if person.get("okres_narozeni"):
            page.locator('input[name*="dodatecneUdaje:okresNarozeni"]').last.fill(person["okres_narozeni"])
        if person.get("misto_narozeni"):
            page.locator('input[name*="dodatecneUdaje:mistoNarozeni"]').last.fill(person["misto_narozeni"])

        # Název funkce
        page.locator('input[name*="editaceFunkce:hlavicka"]').last.fill(funkce)

        # Datum vzniku funkce (POZOR: u obyčejného člena výboru bez zvláštní funkce MUSÍ být Nezadáno '')
        funkce_od = person.get("funkce_od")
        f_sel = page.locator('select[name*="editaceFunkce:denVzniku:dateType"]').last
        if funkce_od:
            f_sel.select_option(value='PRESNY')
            wait_ajax(page, 300)
            page.locator('input[name*="editaceFunkce:denVzniku:dateContainer:dateField"]').last.fill(funkce_od)
        else:
            f_sel.select_option(value='')
            wait_ajax(page, 300)

        # Datum vzniku členství
        clenstvi_od = person.get("clenstvi_od")
        c_sel = page.locator('select[name*="editaceClenstvi:denVzniku:dateType"]').last
        if clenstvi_od:
            c_sel.select_option(value='PRESNY')
            wait_ajax(page, 300)
            page.locator('input[name*="editaceClenstvi:denVzniku:dateContainer:dateField"]').last.fill(clenstvi_od)

        # Uložit dílčí osobu
        page.locator('button:has-text("Uložit"):not(.big-button)').last.click()
        wait_ajax(page, 2000)
        print(f"   Uložena osoba: {name}")

    # Uložit celou předmětnou část velkým tlačítkem
    print("-> Ukládám Předmětnou část hlavním tlačítkem Uložit...")
    big_btn = page.locator('button.big-button:has-text("Uložit")').first
    big_btn.click()
    page.wait_for_load_state('domcontentloaded')
    wait_ajax(page, 3000)

    errs = check_feedback_errors(page, "Předmětná část")
    if errs:
        raise RuntimeError(f"Chyba při ukládání předmětné části: {errs}")


def process_zaverecna_cast(page: Page, config: Dict[str, Any]):
    print("-> Otevírám Závěrečnou část...")
    page.locator('#zaverecnaCast').click()
    page.wait_for_load_state('domcontentloaded')
    wait_ajax(page, 2000)

    # 1. RÚIAN validace adresy navrhovatele
    dohl_navrh = page.locator('//div[contains(@class, "section") and .//h2[contains(., "Navrhovatel")]]//button[contains(., "Dohledat adresu")]')
    if dohl_navrh.count() > 0:
        print("-> Ověřuji adresu navrhovatele v RÚIAN...")
        dohl_navrh.first.click()
        wait_ajax(page, 1500)

    # 2. Jednající osoba
    signatory = config.get("signatory", {})
    sig_name = signatory.get("search_name")
    if sig_name:
        print(f"-> Výběr jednající osoby: {sig_name}...")
        podava_sec = page.locator('//div[contains(@class, "section") and .//h2[contains(., "Tento návrh podává za navrhovatele")]]').first
        vybrat_btn = podava_sec.locator('button:has-text("Vybrat osobu ze subjektu")').first
        vybrat_btn.click()
        wait_ajax(page, 1500)

        match_item = page.locator(f'div[id*="searchResult"] li:has-text("{sig_name}")').first
        match_item.click()
        wait_ajax(page, 2000)

        # Ověření adresy jednající osoby v RÚIAN
        if signatory.get("validate_ruian", True):
            print("-> Ověřuji adresu jednající osoby v RÚIAN...")
            dohl_btn = podava_sec.locator('button:has-text("Dohledat adresu")').first
            dohl_btn.click()
            wait_ajax(page, 2000)

            filter_text = signatory.get("ruian_filter", "")
            if filter_text:
                addr_match_btn = podava_sec.locator(f'button[name*="ruianVysledkyHledani"]:has-text("{filter_text}"), button[id*="id"]:has-text("{filter_text}")').first
            else:
                addr_match_btn = podava_sec.locator('button[name*="ruianVysledkyHledani"], button[id*="id"]').first

            if addr_match_btn.count() > 0:
                print(f"   RÚIAN adresa potvrzena: {addr_match_btn.text_content().strip()}")
                addr_match_btn.click()
                wait_ajax(page, 2000)

    # 3. Přílohy
    attachments = config.get("attachments", [])
    if attachments:
        print(f"-> Zadávám {len(attachments)} příloh...")
        prilohy_sec = page.locator('//div[contains(@class, "section") and .//h2[contains(., "Přílohy")]]').first
        add_p_btn = prilohy_sec.locator('button:has-text("Přidat údaj")').first

        for att in attachments:
            add_p_btn.click()
            wait_ajax(page, 1200)
            prilohy_sec.locator('input[name*="content:listina"]').last.fill(att.get("name", ""))
            prilohy_sec.locator('input[name*="content:pocet"]').last.fill(str(att.get("count", 1)))
            wait_ajax(page, 500)

    # Uložit celou závěrečnou část
    print("-> Ukládám Závěrečnou část hlavním tlačítkem Uložit...")
    save_zav = page.locator('button.big-button:has-text("Uložit"), button[type="submit"]:has-text("Uložit")').last
    save_zav.click()
    page.wait_for_load_state('domcontentloaded')
    wait_ajax(page, 3000)

    errs = check_feedback_errors(page, "Závěrečná část")
    if errs:
        raise RuntimeError(f"Chyba při ukládání Závěrečné části: {errs}")


def finalize_and_download(page: Page, output_pdf_path: str, signing_method: str = "DATOVA_SCHRANKA") -> str:
    print("-> Provádím trvalé uložení celého návrhu...")
    ulozit_main = page.locator('#ulozit').first
    if ulozit_main.count() > 0:
        ulozit_main.click()
        wait_ajax(page, 2000)

    code_el = page.locator('#kodProNavratValue, .kod-pro-navrat, span[id*="kodProNavrat"]').first
    return_code = ""
    if code_el.count() > 0:
        return_code = code_el.text_content().strip()
    print(f"-> Finální návratový kód: {return_code}")

    gen_btn = page.locator('#generateSubmission').first
    tag = gen_btn.evaluate('e => e.tagName')
    if tag != 'A':
        errs = check_feedback_errors(page, "Před generováním podání")
        raise RuntimeError(f"Tlačítko #generateSubmission není aktivní odkaz (tag={tag}). Chyby: {errs}")

    print("-> Přechod na generování podání...")
    gen_btn.click()
    page.wait_for_load_state('domcontentloaded')
    wait_ajax(page, 3000)

    print(f"-> Nastavení způsobu odeslání / podpisu: {signing_method}...")
    page.locator('select[name="zpusobPodepsani"]').select_option(value=signing_method)
    wait_ajax(page, 1000)

    print("-> Potvrzení tlačítkem Hotovo...")
    page.locator('button:has-text("Hotovo")').first.click()
    page.wait_for_load_state('domcontentloaded')
    wait_ajax(page, 3000)

    abs_output = os.path.abspath(output_pdf_path)
    os.makedirs(os.path.dirname(abs_output), exist_ok=True)
    print(f"-> Stahování oficiálního PDF podání do: {abs_output}...")

    with page.expect_download(timeout=20000) as d_info:
        page.locator('#downloadPdf2, #downloadPdf1').first.click()
    download = d_info.value
    download.save_as(abs_output)

    size = os.path.getsize(abs_output)
    print(f"-> PDF úspěšně uloženo ({size} B).")
    return return_code


def run_automation(config: Dict[str, Any], output_pdf: str, headless: bool = True) -> Dict[str, Any]:
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=headless)
        page: Page = browser.new_page()
        page.on("dialog", lambda d: d.accept())

        try:
            return_code = start_or_resume_proposal(
                page,
                ico=config.get("ico"),
                return_code=config.get("return_code")
            )

            # Pokud konfigurace obsahuje statutární orgán
            if "deletions" in config or "additions" in config:
                process_statutarni_organ(page, config)

            # Závěrečná část
            if "signatory" in config or "attachments" in config:
                process_zaverecna_cast(page, config)

            # Generování a stažení
            method = config.get("signing_method", "DATOVA_SCHRANKA")
            final_code = finalize_and_download(page, output_pdf, signing_method=method)

            return {
                "success": True,
                "return_code": final_code,
                "output_pdf": os.path.abspath(output_pdf),
                "pdf_size_bytes": os.path.getsize(os.path.abspath(output_pdf))
            }
        finally:
            browser.close()


def main():
    parser = argparse.ArgumentParser(description="Automatizace podání na or.justice.cz/ias/iform")
    parser.add_argument("--config", "-c", required=True, help="Cesta ke konfiguračnímu JSON souboru")
    parser.add_argument("--output-pdf", "-o", default="navrh_rejstrik_podani.pdf", help="Cesta pro uložení staženého PDF")
    parser.add_argument("--headed", action="store_true", help="Spustit prohlížeč s viditelným oknem")

    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    res = run_automation(cfg, args.output_pdf, headless=not args.headed)
    print("\nVýsledek:")
    print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
