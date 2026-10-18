"""
Skript pro synchronizaci potvrzených akcí, revizí a shromáždění SVJ Letohradská 367/5
s Google Kalendářem předsedy SVJ a generování standardního iCalendar (.ics) souboru.

Zdroje dat:
- agenda/udalosti.md
- agenda/revize.md

Podporovaná autentizace:
- Google Service Account (service_account.json)
- Google OAuth2 (token.json / credentials.json)
- Lokální export (.ics)
"""

import os
import sys
import re
import argparse
from datetime import datetime, date, time
from zoneinfo import ZoneInfo
import icalendar

# Kódování pro Windows konzoli
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

TZ_PRAGUE = ZoneInfo("Europe/Prague")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_env(env_path=None):
    """Načte proměnné prostředí ze souboru .env bez nutnosti python-dotenv."""
    if not env_path:
        env_path = os.path.join(BASE_DIR, ".env")
    
    config = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    config[key.strip()] = val.strip().strip('"').strip("'")
    return config

def parse_events_from_markdown():
    """
    Parsuje strukturované události ze souboru agenda/udalosti.md.
    Formát sekcí v souboru:
    ### Název události
    - **ID**: `svj-id`
    - **Datum a čas**: `YYYY-MM-DD HH:MM - HH:MM` nebo `YYYY-MM-DD`
    - **Místo**: Text
    - **Popis**: Text
    """
    events_file = os.path.join(BASE_DIR, "agenda", "udalosti.md")
    if not os.path.exists(events_file):
        print(f"⚠️ Soubor {events_file} nebyl nalezen.")
        return []

    events = []
    with open(events_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Rozdělení podle sekcí úrovně 3 (###)
    sections = re.split(r'\n(?=###\s+)', content)
    for section in sections:
        if not section.strip().startswith("###"):
            continue
        
        lines = section.strip().split("\n")
        title_match = re.match(r'###\s+(.+)', lines[0])
        if not title_match:
            continue
        title = title_match.group(1).strip()

        event_data = {
            "summary": title,
            "id": None,
            "start": None,
            "end": None,
            "location": "",
            "description": ""
        }

        for line in lines[1:]:
            line_str = line.strip()
            id_m = re.match(r'-\s*\*\*ID\*\*:\s*`?([a-zA-Z0-9_\-]+)`?', line_str)
            if id_m:
                event_data["id"] = id_m.group(1)
                continue

            loc_m = re.match(r'-\s*\*\*Místo\*\*:\s*(.+)', line_str)
            if loc_m:
                event_data["location"] = loc_m.group(1).strip()
                continue

            desc_m = re.match(r'-\s*\*\*Popis\*\*:\s*(.+)', line_str)
            if desc_m:
                event_data["description"] = desc_m.group(1).strip()
                continue

            # Datum a čas
            dt_m = re.match(r'-\s*\*\*Datum a čas\*\*:\s*`?([^`]+)`?', line_str)
            if dt_m:
                dt_raw = dt_m.group(1).strip()
                # Formát: YYYY-MM-DD HH:MM - HH:MM
                m_range = re.match(r'(\d{4}-\d{2}-\d{2})\s+(\d{1,2}:\d{2})\s*-\s*(\d{1,2}:\d{2})', dt_raw)
                if m_range:
                    d_str, t1_str, t2_str = m_range.groups()
                    dt_start = datetime.strptime(f"{d_str} {t1_str}", "%Y-%m-%d %H:%M").replace(tzinfo=TZ_PRAGUE)
                    dt_end = datetime.strptime(f"{d_str} {t2_str}", "%Y-%m-%d %H:%M").replace(tzinfo=TZ_PRAGUE)
                    event_data["start"] = dt_start
                    event_data["end"] = dt_end
                    continue

                # Formát: YYYY-MM-DD HH:MM
                m_single = re.match(r'(\d{4}-\d{2}-\d{2})\s+(\d{1,2}:\d{2})', dt_raw)
                if m_single:
                    d_str, t1_str = m_single.groups()
                    dt_start = datetime.strptime(f"{d_str} {t1_str}", "%Y-%m-%d %H:%M").replace(tzinfo=TZ_PRAGUE)
                    dt_end = dt_start.replace(hour=(dt_start.hour + 1) % 24)
                    event_data["start"] = dt_start
                    event_data["end"] = dt_end
                    continue

                # Formát: Celodenní YYYY-MM-DD
                m_day = re.match(r'(\d{4}-\d{2}-\d{2})', dt_raw)
                if m_day:
                    d_str = m_day.group(1)
                    dt_day = datetime.strptime(d_str, "%Y-%m-%d").date()
                    event_data["start"] = dt_day
                    event_data["end"] = dt_day
                    continue

        if event_data["start"] and event_data["summary"]:
            if not event_data["id"]:
                # Generovat stabilní ID ze summary a data
                safe_slug = re.sub(r'[^a-zA-Z0-9]+', '-', event_data["summary"].lower()).strip('-')
                start_str = event_data["start"].strftime("%Y%m%d") if isinstance(event_data["start"], (datetime, date)) else "event"
                event_data["id"] = f"svj-{safe_slug[:20]}-{start_str}"
            events.append(event_data)

    return events

def generate_ics_file(events, output_path):
    """Vytvoří standardní iCalendar (.ics) soubor se všemi událostmi."""
    cal = icalendar.Calendar()
    cal.add('prodid', '-//SVJ Letohradska 367/5//Praha 7//CZ')
    cal.add('version', '2.0')
    cal.add('x-wr-calname', 'SVJ Letohradská 367/5')
    cal.add('x-wr-timezone', 'Europe/Prague')

    for ev in events:
        event = icalendar.Event()
        event.add('uid', ev['id'] + '@svj-letohradska.cz')
        event.add('summary', ev['summary'])
        event.add('dtstart', ev['start'])
        if ev.get('end'):
            event.add('dtend', ev['end'])
        event.add('dtstamp', datetime.now(tz=TZ_PRAGUE))
        if ev.get('location'):
            event.add('location', ev['location'])
        if ev.get('description'):
            event.add('description', ev['description'])
        cal.add_component(event)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(cal.to_ical())
    print(f"✅ Vygenerován soubor iCalendar (.ics): {output_path}")

def get_google_calendar_service(config):
    """
    Inicializuje službu Google Calendar API v3 pomocí Service Accountu nebo OAuth2.
    """
    import json
    scopes = ['https://www.googleapis.com/auth/calendar']

    # 1. Hledání existujícího tokenu OAuth2
    token_file = os.path.join(BASE_DIR, "token.json")
    if os.path.exists(token_file):
        try:
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import Request
            import googleapiclient.discovery

            creds = Credentials.from_authorized_user_file(token_file, scopes)
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open(token_file, 'w') as f:
                    f.write(creds.to_json())
            if creds and creds.valid:
                service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
                print("🔑 Použito existující OAuth2 ověření (token.json)")
                return service
        except Exception as e:
            print(f"⚠️ Chyba při načítání token.json: {e}")

    # 2. Kontrola přihlašovacích JSON souborů (Service Account)
    candidate_files = [
        config.get("GOOGLE_SERVICE_ACCOUNT_FILE", "service_account.json"),
        config.get("GOOGLE_CREDENTIALS_FILE", "credentials.json"),
        "service_account.json",
        "credentials.json"
    ]

    key_file = None
    for cand in candidate_files:
        if cand:
            path = cand if os.path.isabs(cand) else os.path.join(BASE_DIR, cand)
            if os.path.exists(path):
                key_file = path
                break

    if not key_file:
        return None

    try:
        with open(key_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"⚠️ Nelze přečíst {os.path.basename(key_file)}: {e}")
        return None

    # Typ A: Service Account
    if data.get("type") == "service_account":
        try:
            from google.oauth2 import service_account
            import googleapiclient.discovery
            creds = service_account.Credentials.from_service_account_file(key_file, scopes=scopes)
            service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
            print(f"🔑 Použit Google Service Account: {data.get('client_email', os.path.basename(key_file))}")
            return service
        except Exception as e:
            print(f"⚠️ Chyba při inicializaci Service Account: {e}")
            return None

    # Typ B: OAuth 2.0 Client ID
    elif "installed" in data or "web" in data:
        try:
            from google_auth_oauthlib.flow import InstalledAppFlow
            import googleapiclient.discovery
            print(f"🔑 Nalezeny přihlašovací údaje OAuth 2.0 ({os.path.basename(key_file)}).", flush=True)
            flow = InstalledAppFlow.from_client_secrets_file(key_file, scopes)
            creds = flow.run_local_server(port=0, prompt='consent')
            if creds:
                with open(token_file, 'w') as f:
                    f.write(creds.to_json())
                service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
                print("✅ Úspěšně ověřeno a uloženo do token.json!", flush=True)
                return service
        except Exception as e:
            print(f"⚠️ Chyba při OAuth 2.0 autorizaci: {e}", flush=True)
            return None

    return None

def sync_events_via_api(service, calendar_id, events, prune=False):
    """Synchronizuje události přímo do Google Kalendáře přes API v3."""
    print(f"\n📡 Připojuji ke Google Calendar API (Kalendář ID: {calendar_id})...")

    try:
        events_result = service.events().list(
            calendarId=calendar_id,
            maxResults=250,
            singleEvents=False
        ).execute()
        existing_items = events_result.get('items', [])
        print(f"Nalezeno {len(existing_items)} stávajících položek v Google Kalendáři.")
    except Exception as e:
        print(f"❌ Nelze načíst události z kalendáře: {e}")
        print("💡 Zkontrolujte, zda je kalendář nasdílený pro e-mail servisního účtu s právem 'Provádět změny v událostech'.")
        return False

    existing_by_summary = {item.get('summary'): item for item in existing_items if item.get('summary')}

    synced_count = 0
    updated_count = 0

    for ev in events:
        is_all_day = isinstance(ev['start'], date) and not isinstance(ev['start'], datetime)
        
        if is_all_day:
            start_payload = {'date': ev['start'].strftime('%Y-%m-%d')}
            end_payload = {'date': ev['end'].strftime('%Y-%m-%d')}
        else:
            start_payload = {'dateTime': ev['start'].isoformat(), 'timeZone': 'Europe/Prague'}
            end_payload = {'dateTime': ev['end'].isoformat(), 'timeZone': 'Europe/Prague'}

        event_body = {
            'summary': ev['summary'],
            'location': ev.get('location', ''),
            'description': ev.get('description', ''),
            'start': start_payload,
            'end': end_payload,
        }

        existing = existing_by_summary.get(ev['summary'])

        if existing:
            changed = False
            if (existing.get('location') or '').strip() != (ev.get('location') or '').strip():
                changed = True
            if (existing.get('description') or '').strip() != (ev.get('description') or '').strip():
                changed = True

            if changed:
                try:
                    service.events().patch(calendarId=calendar_id, eventId=existing['id'], body=event_body).execute()
                    print(f"  🔄 Aktualizováno: {ev['summary']}")
                    updated_count += 1
                except Exception as e:
                    print(f"  ❌ Chyba při aktualizaci '{ev['summary']}': {e}")
            else:
                print(f"  ✓ Beze změny: {ev['summary']}")
        else:
            try:
                service.events().insert(calendarId=calendar_id, body=event_body).execute()
                print(f"  ➕ Vloženo do kalendáře: {ev['summary']}")
                synced_count += 1
            except Exception as e:
                print(f"  ❌ Chyba při vkládání '{ev['summary']}': {e}")

    # Odstranění položek, které již v agendě nejsou
    deleted_count = 0
    if prune:
        current_summaries = {ev['summary'] for ev in events}
        for item in existing_items:
            sum_title = item.get('summary')
            if sum_title and sum_title not in current_summaries:
                try:
                    service.events().delete(calendarId=calendar_id, eventId=item['id']).execute()
                    print(f"  🗑️ Odstraněno z kalendáře: {sum_title}")
                    deleted_count += 1
                except Exception as e:
                    print(f"  ❌ Nelze smazat '{sum_title}': {e}")

    print(f"\n✨ Synchronizace dokončena: {synced_count} přidáno, {updated_count} upraveno, {deleted_count} smazáno.")
    return True

def main():
    parser = argparse.ArgumentParser(description="Synchronizace kalendáře SVJ Letohradská 367/5")
    parser.add_argument("--ics-only", action="store_true", help="Pouze vygenerovat .ics soubor")
    parser.add_argument("--list", action="store_true", help="Vypsat nalezené události ze souborů agendy")
    parser.add_argument("--prune", action="store_true", help="Smazat z kalendáře položky, které již nejsou v souboru udalosti.md")
    args = parser.parse_args()

    config = load_env()
    calendar_id = config.get("GOOGLE_CALENDAR_ID")

    print("=" * 60)
    print("📅 KALENDÁŘ SVJ LETOHRADSKÁ 367/5 – SYNCHRONIZACE")
    print("=" * 60)

    events = parse_events_from_markdown()
    print(f"Nalezeno {len(events)} událostí v souboru agenda/udalosti.md:\n")

    for idx, ev in enumerate(events, 1):
        if isinstance(ev['start'], datetime):
            time_str = f"{ev['start'].strftime('%d. %m. %Y %H:%M')} - {ev['end'].strftime('%H:%M')}"
        else:
            time_str = f"{ev['start'].strftime('%d. %m. %Y')} (celý den)"
        print(f"  {idx}. {ev['summary']} ({time_str})")
        if ev.get('location'):
            print(f"     Místo: {ev['location']}")

    if args.list:
        return

    # 1. Generování .ics souboru
    ics_path = os.path.join(BASE_DIR, "kalendar", "svj_letohradska.ics")
    generate_ics_file(events, ics_path)

    if args.ics_only:
        return

    # 2. Google Calendar API synchronizace
    service = get_google_calendar_service(config)
    if not service:
        print("\n💡 Přímá synchronizace s Google API nebyla spuštěna:")
        print("   - Chybí soubor 'service_account.json' nebo 'token.json' v kořeni projektu.")
        print("   - Po stažení JSON klíče servisního účtu uložte soubor jako 'service_account.json'.")
        print("   - Soubor .ics byl v pořádku vygenerován a lze jej importovat do jakéhokoliv kalendáře.")
        return

    if not calendar_id or calendar_id.startswith("vase-svj-kalendar-id"):
        print("\n⚠️ Není nastaveno platné GOOGLE_CALENDAR_ID v souboru .env.")
        print("   Zkopírujte ID vašeho Google Kalendáře do souboru .env:")
        print("   GOOGLE_CALENDAR_ID=xxxxxxxxxxxx@group.calendar.google.com")
        return

    sync_events_via_api(service, calendar_id, events, prune=args.prune)

if __name__ == "__main__":
    main()
