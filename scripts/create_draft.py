# -*- coding: utf-8 -*-
"""
Vytvoření konceptu emailu přímo ve složce Koncepty na Gmailu (přes IMAP)
a provázání odpovědi na existující vlákno konverzace (In-Reply-To, References).
"""
import os
import sys
import ssl
import time
import imaplib
import email
from email.message import EmailMessage
from email.header import decode_header
from email.utils import make_msgid, formatdate

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(BASE_DIR, ".env")

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

def get_drafts_folder(mail):
    typ, folders = mail.list()
    for f in folders:
        decoded = f.decode('utf-8', errors='replace')
        if r'\Drafts' in decoded:
            # Extract folder name in quotes or last token
            # format: (\Drafts \HasNoChildren) "/" "[Google Mail]/Koncepty"
            parts = decoded.split(' "/" ')
            if len(parts) == 2:
                return parts[1].strip()
    return '"[Google Mail]/Koncepty"'

def find_last_message(mail, search_query):
    """
    Hledá poslední zprávu v korespondenci (nejprve v INBOX, případně ve Všech zprávách).
    """
    for folder in ['INBOX', '"[Google Mail]/V&AWE-echny zpr&AOE-vy"']:
        try:
            status, _ = mail.select(folder, readonly=True)
            if status != 'OK':
                continue
            status, data = mail.search(None, search_query)
            if status == 'OK' and data[0]:
                msg_ids = data[0].split()
                if msg_ids:
                    last_id = msg_ids[-1]
                    status, msg_data = mail.fetch(last_id, '(RFC822.HEADER)')
                    if status == 'OK':
                        msg = email.message_from_bytes(msg_data[0][1])
                        return msg
        except Exception as e:
            continue
    return None

def create_gmail_draft(to_email, subject, body_text, reply_to_query=None):
    env = load_env()
    user = env.get("GMAIL_USER")
    pwd = env.get("GMAIL_APP_PASSWORD")

    if not user or not pwd:
        raise ValueError("V .env chybí GMAIL_USER nebo GMAIL_APP_PASSWORD.")

    context = ssl.create_default_context()
    mail = imaplib.IMAP4_SSL("imap.gmail.com", port=993, ssl_context=context)
    mail.login(user, pwd)

    try:
        drafts_folder = get_drafts_folder(mail)
        print(f"Používám složku konceptů: {drafts_folder}")

        msg = EmailMessage()
        msg['From'] = f"Veronika Brožová <{user}>"
        msg['To'] = to_email
        msg['Date'] = formatdate(localtime=True)
        msg['Message-ID'] = make_msgid()
        msg['X-Unsent'] = '1'

        parent_msg = None
        if reply_to_query:
            parent_msg = find_last_message(mail, reply_to_query)

        if parent_msg:
            parent_msg_id = parent_msg.get('Message-ID')
            parent_refs = parent_msg.get('References', '')
            parent_subj = parent_msg.get('Subject', '')

            if parent_msg_id:
                parent_msg_id = " ".join(parent_msg_id.split())
            if parent_refs:
                parent_refs = " ".join(parent_refs.split())

            print(f"Nalezen předchozí e-mail pro navázání: Message-ID {parent_msg_id}")
            if parent_msg_id:
                msg['In-Reply-To'] = parent_msg_id
                if parent_refs:
                    msg['References'] = f"{parent_refs} {parent_msg_id}"
                else:
                    msg['References'] = parent_msg_id

            if not subject.lower().startswith('re:'):
                clean_subj = parent_subj
                # Decode parent subject if encoded
                decoded_parts = decode_header(clean_subj)
                subj_str = ""
                for part, enc in decoded_parts:
                    if isinstance(part, bytes):
                        subj_str += part.decode(enc or 'utf-8', errors='replace')
                    else:
                        subj_str += str(part)
                if not subj_str.lower().startswith('re:'):
                    subject = f"Re: {subj_str}"
                else:
                    subject = subj_str

        msg['Subject'] = subject
        msg.set_content(body_text)

        raw_bytes = msg.as_bytes()
        # IMAP APPEND flags: \Draft
        status, response = mail.append(drafts_folder, '\\Draft', imaplib.Time2Internaldate(time.time()), raw_bytes)
        if status == 'OK':
            print(f"✅ Koncept byl úspěšně vytvořen a uložen do Gmailu (Koncepty): {subject}")
            return True
        else:
            print(f"⚠️ Chyba při ukládání konceptu: {status} {response}")
            return False
    finally:
        mail.logout()

if __name__ == '__main__':
    # Test draft creation if run directly
    print("Modul create_draft připraven.")
