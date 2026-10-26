# Project Guidelines – SVJ Letohradská 367/5

Tento projekt slouží jako inteligentní asistent pro správu agendy předsedy Společenství vlastníků jednotek domu **Letohradská 367/5, Praha 7**.

---

## 1. Customizations Scope (Skills, MCP Servers, and Agents)
- Veškeré úpravy, konfigurace nebo doplňky týkající se **skillů**, **MCP serverů** a **agentů** musí být prováděny v rámci tohoto projektu (ve složce `.agents/` nebo v kořeni projektu), nikoliv globálně.
  - **Skills**: Ukládat do `.agents/skills/<skill-name>/` se souborem `SKILL.md`.
  - **MCP Servery**: Konfigurace na úrovni projektu v `.agents/` nebo v konfiguračních souborech projektu.
  - **Rules / Agenti**: Zaznamenávat v `GEMINI.md` nebo v `.agents/`.

---

## 2. Git Workflow (GitHub Repozitář)
- **Repozitář**: `git@github.com:xbrov01/letohradska.git` (větev `main`).
- **Pravidlo commitů a pushování**: Po každé významnější změně, dokončení úkolu, aktualizaci agendy nebo vytvoření nových záznamů VŽDY provést popisný Git commit a okamžitě odeslat změny do vzdáleného repozitáře pomocí:
  ```bash
  git add .
  git commit -m "Popis provedených změn"
  git push origin main
  ```
- **Ochrana citlivých údajů**: Do repozitáře se NIKDY nesmí commitovat tajné klíče a přístupové údaje (`.env`, `service_account.json`, `credentials.json`, `token.json` apod.). Tyto soubory jsou striktně vedeny v `.gitignore`.

---

## 3. Pravidla pro ukládání dat (Markdown)
- **Výhradní formát Markdown (`.md`)**: Veškerá data, evidence, dokumenty a záznamy agendy předsedy SVJ se ukládají a spravují výhradně v souborech formátu Markdown.
- **Struktura agendy v projektu**:
  - `agenda/jednotky.md` – evidence bytových a nebytových jednotek, vlastníků, spoluvlastnických podílů a kontaktů.
  - `agenda/revize.md` – přehled a termíny pravidelných zákonných revizí (plyn, elektro, hromosvody, komíny, požární ochrana, hydranty, hasicí přístroje atd.), lhůty a historie.
  - `agenda/udalosti.md` – kalendářní události, plánovaná shromáždění SVJ, odečty měřidel, schůzky s dodavateli a správcovskou firmou.
  - `agenda/ukoly.md` – seznam otevřených, probíhajících a vyřešených úkolů předsedy SVJ.
  - `agenda/koncepty/` – připravené koncepty emailů a korespondence k ručnímu odeslání.
  - `agenda/zapisy/` – zápisy ze shromáždění vlastníků, jednání výboru/předsedy a korespondence.
  - `kalendar/` – generovaný iCalendar (`svj_letohradska.ics`) a související kalendářní exporty.
- **Přehlednost a struktura**: V souborech markdownu používat tabulky, kontrolní seznamy (checkboxy `- [ ]`), tučné zvýraznění klíčových údajů (termíny, částky, kontakty) a standardní hlavičky pro snadné strojové i lidské čtení.

---

## 4. Pravidla pro přístup a synchronizaci s Google Kalendářem
- **Identifikace kalendáře**: ID Google Kalendáře pro SVJ je uloženo v souboru `.env` pod proměnnou `GOOGLE_CALENDAR_ID`.
- **Autentizace**:
  - Primárně přes Google **Service Account** uložený v souboru `service_account.json` (cesta definována v `.env` jako `GOOGLE_SERVICE_ACCOUNT_FILE=service_account.json`).
  - Podporována je také autentizace přes OAuth 2.0 (`token.json` / `credentials.json`).
- **Pravidlo synchronizace**:
  - Asistent VŽDY udržuje Google Kalendář synchronizovaný se všemi termíny zapsanými v agendě (zejména `agenda/udalosti.md` a `agenda/revize.md`).
  - Synchronizace probíhá pomocí skriptu `python scripts/sync_calendar.py`, který:
    1. Načte termíny a události z Markdown souborů agendy.
    2. Vygeneruje standardní iCalendar soubor `kalendar/svj_letohradska.ics`.
    3. Pokud je dostupný `service_account.json` (či OAuth token) a nastaveno `GOOGLE_CALENDAR_ID`, provede přímou synchronizaci do Google Kalendáře přes Google Calendar API v3.
- **Kdy synchronizovat**:
  - Kdykoliv je vytvořen, upraven nebo potvrzen nový termín (shromáždění, revize, odečet měřidel, schůzka).
  - Při týdenním/pravidelném přehledu a při volbě z interaktivního menu.

---

## 5. Spouštění skriptů, PowerShellu a příkazové řádky
- **Automatické spouštění příkazů a skriptů**: Asistent má v tomto projektu plné oprávnění spouštět python skripty (`python scripts/...`, `python ...`), veškeré běžné příkazy PowerShellu (všechny cmdlety `Get-*`, `Set-*`, `New-*`, `Remove-*`, `Test-*`, `Select-*` atd.), aliasy a nástroje příkazové řádky (`git`, `dir`, `ls`, `cd`, `cat`, `type`, `echo`, `findstr`, `tree`, `whoami`, `curl` apod.) přímo a autonomně bez vyžadování zbytečného potvrzování.

---

## 6. Zahájení nové konverzace (Interaktivní menu)
- **Automatická nabídka hlavních akcí**: Při zahájení nové konverzace v tomto projektu (při prvním vstupu uživatele, obecném pozdravu typu „Ahoj“, stisku Enteru apod., pokud uživatel nezadá přímo jiný konkrétní specifický úkol) asistent VŽDY okamžitě zobrazí interaktivní výběrová tlačítka (`ask_question`) s hlavními akcemi pro správu SVJ Letohradská 367/5:
  1. `(Doporučeno) Zobrazit přehled nadcházejících termínů, revizí a událostí`
  2. `Zkontrolovat stav otevřených úkolů a závad v domě`
  3. `Synchronizovat agendu a termíny s Google Kalendářem`
  4. `Otevřít evidenci jednotek a kontaktů na vlastníky`
  5. `Zaznamenat nový zápis, úkol nebo termín revize`
- Po volbě uživatele asistent ihned provede požadovanou akci nebo zobrazí strukturovaný přehled.

---

## 7. Zobrazování úkolů a práce s emaily
- **Přehled úkolů**: Při dotazu na seznam úkolů vytvořit VŽDY **krátký a přehledný souhrn seřazený podle priorit a urgence** (urgentní termíny nejblíže, bezodkladné právní/zákonné lhůty, následně strategické a provozní úkoly).
- **Striktní zákaz samostatného odesílání emailů (pouze koncepty)**:
  - Pokud je třeba poslat jakýkoliv email, asistent ho **NIKDY neodesílá samostatně ani automaticky**.
  - Asistent VŽDY vytvoří pouze **koncept emailu** (příjemce, předmět, text těla) a uloží jej do složky `agenda/koncepty/` ve formátu Markdown (s metadaty a jasnou výzvou ke schválení/odeslání uživatelem).
  - **Přímé vytváření konceptů v Gmailu s napojením na vlákno**: Asistent vytvoří koncept emailu ROVNOU PŘÍMO DO GMAILU (do složky Koncepty / `[Google Mail]/Koncepty` přes IMAP skript `scripts/create_draft.py`) a napojí odpověď na poslední vyměněný email v daném vlákně (pomocí hlaviček `In-Reply-To` a `References`). Uživatel tak má koncept rovnou připravený ve své schránce (web, mobil či aplikace) a může jej zkontrolovat a pouhým kliknutím odeslat.

---

## 8. Striktní oddělení agendy SVJ a správy spoluvlastněných jednotek
- **Právní základ správy spoluvlastněných jednotek**: Správu jednotek v podílovém spoluvlastnictví (byty č. 367/1, 367/2, 367/3, 367/9 a nebytové prostory č. 367/101 a 367/102) vykonáváte **výhradně na základě plné moci udělené jednotlivými spoluvlastníky** (cca 32 spoluvlastníků, bývalých družstevníků), nikoliv z titulu funkce předsedkyně výboru SVJ Letohradská 367/5. Tyto jednotky nevlastní SVJ jako právnická osoba.
- **Pravidlo striktního oddělení ve výstupech**:
  - Ve všech přehledech, úkolech, zápisech, souborech a výstupech tuto skutečnost VŽDY výslovně zdůraznit.
  - Informace, akce, události, smluvní vztahy a finance obou agend VŽDY striktně oddělovat do samostatných celků:
    1. **Agenda SVJ** (správa společných částí budovy a pozemku, revize domu, výtah, pojištění budovy, shromáždění vlastníků SVJ, volené orgány, Rejstřík SVJ u Městského soudu v Praze, datová schránka SVJ).
    2. **Agenda správy spoluvlastněných jednotek na základě plné moci** (nájemní smlouvy a nájemci bytů 1, 2, 3 a nebytů 101, 102, inflační doložky, hospodaření a vyúčtování výnosů podílovým spoluvlastníkům, řešení bytu č. 9 a sporů s Davidem Večeřou, samostatná zasedání spoluvlastníků jednotek).

---

## 9. Automatická kontrola notifikací datové schránky z emailu
- Notifikace z datové schránky SVJ (`g8z5iva`) jsou zasílány na email `nikabrozova@gmail.com` z adres `notifikace@datovka.gov.cz` a `notifikace@mojedatovaschranka.cz`.
- Asistent při každé analýze a přípravě seznamu úkolů automaticky prověřuje tyto emailové notifikace.
- Pokud je doručena nová datová zpráva, asistent ji **VŽDY zařadí na nejvyšší úroveň urgence v rámci agendy SVJ** s uvedením odesílatele, předmětu zprávy, data doručení a zbývající lhůty do fikce doručení (10 kalendářních dnů od dodání).

---

## 10. Zpracování bankovních výpisů (Excel)
- Bankovní výpisy účtu domu u České spořitelny za rok 2026 jsou uloženy v Excelových tabulkách ve složce `C:\Users\nikan\Documents\Společenství\Výpisy\` (zejména souhrnný soubor `Vypisy_2026_Komplet.xlsx` a jednotlivé měsíční výpisy `vypis01.xlsx` až `vypis09.xlsx`).
- Tyto Excelové tabulky slouží jako **primární a autoritativní zdroj pro veškeré finanční analýzy**, sledování plateb záloh vlastníků, kontrolu dlužníků, inkaso nájemného a výplaty podílů na výnosech podílovým spoluvlastníkům.
- Není nutné zpracovávat původní naskenované PDF soubory výpisů.
