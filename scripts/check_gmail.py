# -*- coding: utf-8 -*-
"""
Skript pro přímou kontrolu pošty a notifikací z datové schránky přes Gmail IMAP (SSL).
Nezávislý na poštovním klientovi Thunderbird.
"""
import os
import sys
import ssl
import re
import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
from html.parser import HTMLParser

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(BASE_DIR, ".env")

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []
    def handle_data(self, d):
        self.result.append(d)
    def get_text(self):
        return ''.join(self.result)

def strip_tags(html):
    s = HTMLTextExtractor()
    s.feed(html)
    return s.get_text()

def load_env():
    config = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    config[k.strip()] = v.strip().strip('"').strip("'")
    return config

def decode_mime(s):
    if not s:
        return ''
    parts = decode_header(s)
    res = []
    for val, enc in parts:
        if isinstance(val, bytes):
            try:
                res.append(val.decode(enc or 'utf-8', errors='replace'))
            except Exception:
                res.append(val.decode('latin1', errors='replace'))
        else:
            res.append(str(val))
    return ''.join(res)

def get_gmail_connection():
    env = load_env()
    user = env.get("GMAIL_USER")
    pwd = env.get("GMAIL_APP_PASSWORD")

    if not user or not pwd:
        raise ValueError("V souboru .env chybí GMAIL_USER nebo GMAIL_APP_PASSWORD.")

    context = ssl.create_default_context()
    mail = imaplib.IMAP4_SSL("imap.gmail.com", port=993, ssl_context=context)
    mail.login(user, pwd)
    return mail

def check_databox_notifications(limit=5):
    mail = get_gmail_connection()
    try:
        mail.select("INBOX", readonly=True)
        typ, data = mail.search(None, 'FROM', 'notifikace@datovka.gov.cz')
        if typ != 'OK' or not data[0]:
            print("Nebyly nalezeny žádné notifikace z datové schránky.")
            return []

        ids = data[0].split()
        print(f"Celkem nalezeno {len(ids)} notifikací z datovky. Zobrazuji posledních {min(limit, len(ids))}:\n")

        notifications = []
        for mid in ids[-limit:]:
            typ, msg_data = mail.fetch(mid, '(RFC822)')
            if typ != 'OK':
                continue
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject = decode_mime(msg.get('Subject', ''))
            date_str = msg.get('Date', '')
            
            body_text = ""
            for part in msg.walk():
                ctype = part.get_content_type()
                if ctype in ('text/plain', 'text/html'):
                    payload = part.get_payload(decode=True)
                    if payload:
                        text = payload.decode('utf-8', errors='replace')
                        if ctype == 'text/html':
                            text = strip_tags(text)
                        body_text += "\n" + text

            # Parse sender, recipient, message subject from notification body
            sender_match = re.search(r'Odesílatel:\s*([^\n\r<]+)', body_text)
            recipient_match = re.search(r'Příjemce:\s*([^\n\r<]+)', body_text)
            msg_subj_match = re.search(r'V datové schránce je nová datová zpráva:\s*([^\n\r<]+)', body_text)

            sender = sender_match.group(1).strip() if sender_match else "Neznámý odesílatel"
            recipient = recipient_match.group(1).strip() if recipient_match else ""
            msg_subject = msg_subj_match.group(1).strip() if msg_subj_match else subject

            # Try to parse date
            dt = None
            try:
                dt = email.utils.parsedate_to_datetime(date_str)
            except Exception:
                pass

            deadline_fiction = (dt + timedelta(days=10)).strftime('%d.%m.%Y %H:%M') if dt else "N/A"
            dt_display = dt.strftime('%d.%m.%Y %H:%M') if dt else date_str

            notif = {
                "id": mid.decode(),
                "date": dt_display,
                "fiction_deadline": deadline_fiction,
                "sender": sender,
                "recipient": recipient,
                "subject": msg_subject
            }
            notifications.append(notif)

            print("=" * 75)
            print(f"📅 Doručeno:          {dt_display}")
            print(f"⏳ Fikce doručení do: {deadline_fiction}")
            print(f"🏢 Příjemce:          {recipient}")
            print(f"👤 Odesílatel:        {sender}")
            print(f"✉️  Předmět zprávy:    {msg_subject}")
        print("=" * 75)
        return notifications
    finally:
        mail.logout()

if __name__ == '__main__':
    check_databox_notifications(5)
