# -*- coding: utf-8 -*-
import sqlite3, sys, datetime

sys.stdout.reconfigure(encoding='utf-8')

db_path = r"C:\Users\nikan\AppData\Roaming\Thunderbird\Profiles\aofl1o4o.default-release\global-messages-db.sqlite"
conn = sqlite3.connect(f"file:{db_path}?immutable=1", uri=True)
c = conn.cursor()

ts_feb2026 = int(datetime.datetime(2026, 2, 13).timestamp() * 1000000)

query = f"""
SELECT m.date, c.c3author, c.c4recipients, c.c1subject, c.c0body 
FROM messages m
JOIN messagesText_content c ON m.id = c.docid
WHERE m.date >= {ts_feb2026}
  AND (
       c.c0body LIKE '%soldát%' OR c.c0body LIKE '%sebera%' OR c.c0body LIKE '%andělov%' OR c.c0body LIKE '%hábov%' 
    OR c.c0body LIKE '%mandelík%' OR c.c0body LIKE '%výnos%' OR c.c0body LIKE '%podíl%'
  )
ORDER BY m.date ASC
"""

c.execute(query)
rows = c.fetchall()
print(f"Messages found after 13.02.2026: {len(rows)}")
for r in rows:
    dt = datetime.datetime.fromtimestamp(r[0] / 1000000.0) if r[0] else None
    dt_str = dt.strftime('%d.%m.%Y %H:%M') if dt else 'N/A'
    subj = r[3] or ''
    author = r[1] or ''
    body = r[4] or ''
    
    # check if relevant to payout
    matches = [line.strip() for line in body.splitlines() if any(k in line.lower() for k in ['vyplat', 'podíl', 'výnos', 'soldát', 'sebera', 'andělov', 'hábov', 'mandelík', 'žádost'])]
    if matches:
        print(f"\n--------------------------------------------------")
        print(f"DATUM: {dt_str} | OD: {author} | PŘEDMĚT: {subj}")
        for m in matches[:6]:
            print(f"  > {m[:180]}")
