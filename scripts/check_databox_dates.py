# -*- coding: utf-8 -*-
import sqlite3, sys, datetime

sys.stdout.reconfigure(encoding='utf-8')

db_path = r"C:\Users\nikan\AppData\Roaming\Thunderbird\Profiles\aofl1o4o.default-release\global-messages-db.sqlite"
conn = sqlite3.connect(f"file:{db_path}?immutable=1", uri=True)
c = conn.cursor()

c.execute("""
SELECT m.id, m.date, c.c3author, c.c1subject, c.c0body 
FROM messages m
JOIN messagesText_content c ON m.id = c.docid
WHERE (c.c1subject LIKE '%Společenství vlastníků Letohradská%' OR c.c0body LIKE '%g8z5iva%')
  AND (c.c3author LIKE '%datovka%' OR c.c3author LIKE '%datovaschranka%' OR c.c1subject LIKE '%datová zpráva%')
ORDER BY m.date DESC
""")

rows = c.fetchall()
print(f"Total SVJ Databox notifications: {len(rows)}")
for r in rows[:10]:
    # Thunderbird stores date in microseconds
    dt = datetime.datetime.fromtimestamp(r[1] / 1000000.0)
    print("-----------------------------------------")
    print(f"DATUM: {dt.strftime('%d.%m.%Y %H:%M:%S')}")
    print(f"PŘEDMĚT: {r[3]}")
    body = (r[4] or "").replace("\n", " ").strip()
    print(f"OBSAH: {body[:250]}")
