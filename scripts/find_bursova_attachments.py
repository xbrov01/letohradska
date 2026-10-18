# -*- coding: utf-8 -*-
import mailbox, os, sys

sys.stdout.reconfigure(encoding='utf-8')
inbox_path = r"C:\Users\nikan\AppData\Roaming\Thunderbird\Profiles\aofl1o4o.default-release\ImapMail\imap.gmail.com\INBOX"

mbox = mailbox.mbox(inbox_path)
print("Scanning inbox attachments...")

found_attachments = []

for i in range(len(mbox)-1, max(-1, len(mbox)-400), -1):
    msg = mbox[i]
    from_hdr = str(msg.get('From', ''))
    if 'bursova' in from_hdr.lower():
        subj = str(msg.get('Subject', ''))
        date_hdr = str(msg.get('Date', ''))
        if msg.is_multipart():
            for part in msg.walk():
                fn = part.get_filename()
                if fn:
                    found_attachments.append((date_hdr, subj, fn, len(part.get_payload(decode=True) or b'')))

for a in found_attachments:
    print(f"DATE: {a[0]} | SUBJ: {a[1]} | ATTACHMENT: {a[2]} ({a[3]} bytes)")
