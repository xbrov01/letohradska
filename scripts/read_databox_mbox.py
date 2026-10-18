# -*- coding: utf-8 -*-
import mailbox, sys

sys.stdout.reconfigure(encoding='utf-8')
inbox_path = r"C:\Users\nikan\AppData\Roaming\Thunderbird\Profiles\aofl1o4o.default-release\ImapMail\imap.gmail.com\INBOX"

mbox = mailbox.mbox(inbox_path)
print("Total messages in INBOX:", len(mbox))

# Search backwards for datova schranka
for i in range(len(mbox)-1, max(-1, len(mbox)-50), -1):
    msg = mbox[i]
    subj = msg.get('Subject', '')
    if 'datov' in subj.lower() or 'schránk' in subj.lower() or 'notifikace' in str(msg.get('From', '')).lower():
        print(f"\n==========================================")
        print(f"Index: {i}")
        print(f"Date: {msg.get('Date')}")
        print(f"From: {msg.get('From')}")
        print(f"Subject: {subj}")
        # body
        payload = ""
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                if ctype == 'text/plain':
                    payload = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
                elif ctype == 'text/html' and not payload:
                    payload = part.get_payload(decode=True).decode('utf-8', errors='ignore')
        else:
            payload = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        
        print("Body snippet:")
        print(payload[:600])
