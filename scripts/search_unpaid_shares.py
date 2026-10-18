# -*- coding: utf-8 -*-
import sqlite3, os, sys, re

sys.stdout.reconfigure(encoding='utf-8')

print("=== 1. SEARCHING THUNDERBIRD EMAILS ===")
db_path = r"C:\Users\nikan\AppData\Roaming\Thunderbird\Profiles\aofl1o4o.default-release\global-messages-db.sqlite"
conn = sqlite3.connect(f"file:{db_path}?immutable=1", uri=True)
c = conn.cursor()

query = """
SELECT m.date, c.c3author, c.c4recipients, c.c1subject, c.c0body 
FROM messages m
JOIN messagesText_content c ON m.id = c.docid
WHERE (c.c0body LIKE '%výnos%' OR c.c1subject LIKE '%výnos%' OR c.c0body LIKE '%nevyplac%' OR c.c0body LIKE '%podíl%')
  AND (c.c0body LIKE '%spoluvlastn%' OR c.c0body LIKE '%Letohradsk%' OR c.c0body LIKE '%bursov%' OR c.c1subject LIKE '%výnos%')
ORDER BY m.date DESC
"""

c.execute(query)
rows = c.fetchall()
print(f"Emails found: {len(rows)}")

import datetime
for r in rows:
    dt = datetime.datetime.fromtimestamp(r[0] / 1000000.0) if r[0] else None
    dt_str = dt.strftime('%d.%m.%Y %H:%M') if dt else 'N/A'
    subj = r[3] or ''
    author = r[1] or ''
    body = r[4] or ''
    
    # Check if mentions unpaid shares or specific persons
    matches = [line.strip() for line in body.splitlines() if any(k in line.lower() for k in ['nevyplac', 'výnos', 'podíl', 'mandelík', 'dědic', 'andělov', 'hábov', 'večeř', 'nebyly'])]
    if matches:
        print(f"\n--------------------------------------------------")
        print(f"DATUM: {dt_str} | OD: {author} | PŘEDMĚT: {subj}")
        for m in matches[:10]:
            print(f"  > {m[:180]}")
