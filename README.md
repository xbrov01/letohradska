# SVJ Letohradská 367/5 – Asistent předsedy SVJ

Tento repozitář slouží jako asistent a digitální kancelář pro správu agendy předsedy **Společenství vlastníků jednotek Letohradská 367/5, Praha 7**.

---

## 📁 Ukládání dat (Markdown)

Veškerá data, evidence, zápisy a provozní záznamy jsou spravovány v textovém formátu Markdown (`.md`) ve složce [`agenda/`](file:///c:/Users/nikan/data/svj/agenda):

- [`agenda/jednotky.md`](file:///c:/Users/nikan/data/svj/agenda/jednotky.md) – Evidence jednotek, podílů, vlastníků a kontaktů.
- [`agenda/udalosti.md`](file:///c:/Users/nikan/data/svj/agenda/udalosti.md) – Kalendářní akce (shromáždění, odečty měřidel, schůzky), které se synchronizují s Google Kalendářem.
- [`agenda/revize.md`](file:///c:/Users/nikan/data/svj/agenda/revize.md) – Zákonné revize domu (plyn, elektro, hromosvody, komíny, hydranty/hasicí přístroje) a jejich platnost.
- [`agenda/ukoly.md`](file:///c:/Users/nikan/data/svj/agenda/ukoly.md) – Seznam otevřených i vyřešených provozních úkolů a oprav.
- [`agenda/zapisy/`](file:///c:/Users/nikan/data/svj/agenda/zapisy) – Zápisy ze shromáždění vlastníků a hlasování per rollam.

---

## 🛠️ Pravidla pro Git a GitHub

- **Repozitář**: `git@github.com:xbrov01/letohradska.git` (hlavní větev: `main`).
- **Pravidlo commitů**: Po každé podstatné změně nebo aktualizaci agendy asistent provede popisný commit a odeslání do repozitáře (`git push`).
- **Tajné klíče a hesla**: Soubory `.env`, `service_account.json` ani jiné přihlašovací údaje se nikdy necommitují (jsou chráněny v `.gitignore`).

---

## 📅 Synchronizace s Google Kalendářem

Události zapsané v [`agenda/udalosti.md`](file:///c:/Users/nikan/data/svj/agenda/udalosti.md) se automaticky synchronizují s Google Kalendářem pomocí:
```bash
python scripts/sync_calendar.py
```
Skript také generuje standardní iCalendar soubor [`kalendar/svj_letohradska.ics`](file:///c:/Users/nikan/data/svj/kalendar/svj_letohradska.ics).

### Jak nastavit Google Service Account:
1. Uložte stažený klíč servisního účtu jako `service_account.json` do kořenové složky projektu.
2. V souboru `.env` nastavte ID vašeho Google Kalendáře:
   ```env
   GOOGLE_CALENDAR_ID=vase-id-kalendare@group.calendar.google.com
   GOOGLE_SERVICE_ACCOUNT_FILE=service_account.json
   ```
3. V Google Kalendáři **nasdílejte daný kalendář s e-mailem vašeho servisního účtu** (udělte oprávnění: *Provádět změny v událostech*).
