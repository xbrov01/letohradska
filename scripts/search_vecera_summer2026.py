# -*- coding: utf-8 -*-
import sqlite3, sys

sys.stdout.reconfigure(encoding='utf-8')

db_path = r"C:\Users\nikan\AppData\Roaming\Thunderbird\Profiles\aofl1o4o.default-release\global-messages-db.sqlite"
conn = sqlite3.connect(f"file:{db_path}?immutable=1", uri=True)
c = conn.cursor()

c.execute("""
SELECT m.date, c.c3author, c.c4recipients, c.c1subject, c.c0body
FROM messages m
JOIN messagesText_content c ON m.id = c.docid
WHERE (c.c0body LIKE '%večeř%' OR c.c1subject LIKE '%večeř%' OR c.c0body LIKE '%32632%' OR c.c0body LIKE '%1630%' OR c.c0body LIKE '%464441023%')
ORDER BY m.date DESC LIMIT 15
""")

rows = c.fetchall()
import datetime
print(f"Emails found: {len(rows)}")
for r in rows:
    dt = datetime.datetime.fromtimestamp(r[0] / 1000000.0) if r[0] else None
    dt_str = dt.strftime('%d.%m.%Y %H:%M') if dt else 'N/A'
    print("--------------------------------------------------")
    print(f"DATUM: {dt_str} | OD: {r[1]} | PŘEDMĚT: {r[3]}")
    body = (r[4] or "").replace('\n', ' ')
    print(f"TEXT: {body[:350]}")
