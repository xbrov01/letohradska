# Architektura formuláře or.justice.cz/ias/iform a známá úskalí (Pitfalls)

Tento dokument detailně popisuje technické a procesní náležitosti automatizace elektronických podání do veřejného rejstříku (rejstřík SVJ, obchodní rejstřík) na oficiálním portálu Ministerstva spravedlnosti ČR.

---

## 1. Technická architektura portálu

### 1.1 Apache Wicket Framework a dynamické stavy
- Portál je postaven na frameworku **Apache Wicket**.
- Každá interakce (změna selectboxu, kliknutí na tlačítko, výběr osoby) vyvolává AJAX volání, které překresluje dílčí části DOM stromu (`Wicket.Ajax.ajax(...)`).
- URL adresy obsahují proměnlivé session tokeny a parametry komponent (např. `?0-1.IBehaviorListener.0-form-...`). Z tohoto důvodu **nelze používat přímé statické URL odkazy do podformulářů**; navigace musí vždy probíhat sekvenčně přes prvky stránky nebo pomocí **Návratového kódu**.

### 1.2 Návratový kód (`kodProNavratValue`)
- Každý nově vytvořený nebo rozpracovaný návrh má jednoznačný alfanumerický identifikátor ve formátu:
  `XXXX-XXX-XXXXX` (např. `G719-274-5AG1W`).
- Návratový kód se zobrazuje v záhlaví formuláře (selektor `#kodProNavratValue`, `.kod-pro-navrat`).
- **Trvalé uložení**: Kliknutím na horní/spodní tlačítko `#ulozit` se stav návrhu zapíše na serveru justice.cz.
- **Opětovné otevření**: Z úvodní stránky `https://or.justice.cz/ias/iform` lze kdykoliv zadat tento kód do pole `input[name*="kodProNavrat"]` a pokračovat v editaci.

---

## 2. Kritická úskalí a pravidla při vyplňování

### 2.1 Dvoufázový životní cyklus statutárního orgánu (Výmaz a Zápis)
Při volbě nového statutárního orgánu (či znovuzvolení stávajících členů na další funkční období) formulář vyžaduje striktní postup:

1. **Efekt mizení z našeptávače (Autocomplete disappearance):**
   - V seznamu osob subjektu (`div[id*="searchResult"]`) se zobrazují pouze osoby, které v daném kontextu ještě nebyly přiřazeny nebo smazány.
   - **Správný postup:** Nejprve provést výmaz všech dosavadních funkcionářů, kterým skončilo funkční období, a teprve poté provést zápis nových/znovuzvolených členů.

2. **Výmaz končících členů:**
   - U každého člena kliknout na `button[data-tooltip-data="Vymazat údaj"]`.
   - V editačním panelu nastavit datum zániku funkce i datum zániku členství na `PRESNY` a vyplnit datum (např. den předcházející volbě nebo den volby, dle usnesení shromáždění, např. `18.11.2025`).
   - Uložit dílčím tlačítkem `button:has-text("Uložit"):not(.big-button)`.

3. **Zápis nových a znovuzvolených členů:**
   - Kliknout na `button:has-text("Vybrat osobu")`, vybrat osobu ze seznamu subjektu.
   - Kliknout na `button[name*="editPersonalDataComponent:opravitButton"]`.
   - Doplnit povinné identifikační údaje:
     - Rodné číslo (`input[name*="rodneCislo"]`),
     - Státní občanství (`select[name*="obcanstvi"]`, např. `Stat[293]` pro ČR),
     - Rodné příjmení (`input[name*="dodatecneUdaje:rodnePrijmeni"]`),
     - Stát narození (`select[name*="dodatecneUdaje:statNarozeni"]`, např. `cz`),
     - Místo a okres narození (`input[name*="dodatecneUdaje:mistoNarozeni"]`, `okresNarozeni`),
     - Název funkce (`input[name*="editaceFunkce:hlavicka"]`, např. `předseda výboru`, `místopředseda výboru`, `člen výboru`).

4. **Kritická past u řadových členů výboru ("člen výboru"):**
   - U funkce `člen výboru` se **NEZADÁVÁ datum vzniku funkce**, protože řadový člen nemá samostatnou funkci odlišnou od členství.
   - Pole `select[name*="editaceFunkce:denVzniku:dateType"]` MUSÍ mít hodnotu `''` (Nezadáno).
   - Pokud je ponecháno `PRESNY` a datum nevyplněno, formulář zhavaruje na chybě `Pole 'Datum vzniku funkce' je povinné`.
   - Vyplňuje se pouze `select[name*="editaceClenstvi:denVzniku:dateType"]` = `PRESNY` s příslušným datem.

---

### 2.2 Závěrečná část a RÚIAN validace

1. **Povinná validace adresy v RÚIAN (Registr územní identifikace, adres a nemovitostí):**
   - Portál justice.cz nepovolí vygenerovat podání, pokud navrhovatel i jednající osoba nemají adresu spárovanou s RÚIAN kódem.
   - **Postup:** V sekci Navrhovatele i v sekci Jednající osoby kliknout na `button:has-text("Dohledat adresu")`.
   - Následně kliknout na nabídnutou tlačítkovou položku s platnou adresou (`button[name*="ruianVysledkyHledani"]`). Tím se do skrytého pole `ruianKod` zapíše kód prvku RÚIAN.
   - Pokud validace neproběhne, formulář hlásí chybu v `.feedbackPanelERROR` a zablokuje tlačítko generování návrhu.

2. **Výběr jednající osoby:**
   - V sekci "Tento návrh podává za navrhovatele" kliknout na `button:has-text("Vybrat osobu ze subjektu")`.
   - Vybrat nově zapsaného předsedu výboru (nebo jiného oprávněného zástupce).

3. **Seznam příloh:**
   - Přidat jednotlivé listiny tlačítkem `button:has-text("Přidat údaj")`.
   - Zadat název listiny (`input[name*="content:listina"]`) a počet vyhotovení (`input[name*="content:pocet"]`, obvykle `1`).

---

### 2.3 Generování podání a kontrola chyb

1. **Aktivace tlačítka `#generateSubmission`:**
   - Po uložení Závěrečné části se v dolní liště aktivuje prvek `#generateSubmission`.
   - **Indikátor bezchybnosti:** Pokud je prvek tagem `<a>` (odkaz), návrh je validní a připraven ke generování. Pokud zůstává neaktivním `<span>`, existují neuložené či chybové položky v některé části formuláře (nutno zkontrolovat `.feedbackPanelERROR`).

2. **Volba způsobu podepsání a odeslání:**
   - V dialogu generování vybrat `select[name="zpusobPodepsani"]`:
     - `DATOVA_SCHRANKA` – určeno pro odeslání z datové schránky SVJ.
     - `ELEKTRONICKY_PODPIS` – pro podepsání kvalifikovaným certifikátem.
   - Potvrdit tlačítkem `Hotovo`.

3. **Stažení finálního PDF:**
   - Kliknout na `#downloadPdf2` nebo `#downloadPdf1` a zachytit stahovaný soubor přes Playwright `page.expect_download()`.
   - Výsledkem je úřední vícesránkový dokument (např. 8 stran) s detailním rozpisem výmazů, zápisů a soupisem příloh.

---

## 3. Právní náležitosti a podání na soud

### 3.1 Osvobození SVJ od soudního poplatku
- Podle **§ 11 odst. 2 písm. v) zákona č. 549/1991 Sb., o soudních poplatcích**, jsou řízení ve věcech veřejného rejstříku, jde-li o zápis společenství vlastníků jednotek nebo zápis změny údajů o společenství vlastníků jednotek, **zcela osvobozena od soudního poplatku** (poplatek činí **0 Kč**).
- V návrhu není potřeba dokládat úhradu poplatku ani vylepovat kolek.

### 3.2 Doručení přes Datovou schránku (bez uznávaného el. podpisu)
- Podle **§ 22 zákona č. 304/2013 Sb.** (o veřejných rejstřících) a **§ 18 odst. 2 zákona č. 300/2008 Sb.** (o elektronických úkonech):
  - Pokud je návrh odeslán přímo z datové schránky navrhovatele (SVJ) do datové schránky příslušného rejstříkového soudu, **nemusí být vygenerované PDF opatřeno uznávaným elektronickým podpisem**.
  - Přihlášení do datové schránky oprávněnou osobou nahrazuje vlastnoruční podpis.

### 3.3 Příslušnost soudu a IDDS pro Prahu
- Pro subjekty se sídlem v Praze:
  - **Městský soud v Praze**
  - ID datové schránky: **`snkabbm`**
  - Spisová značka: oddíl S (např. `S 13411` pro SVJ Letohradská 367/5).
