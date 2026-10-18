# -*- coding: utf-8 -*-
import sqlite3, sys, datetime

sys.stdout.reconfigure(encoding='utf-8')

db_path = r"C:\Users\nikan\AppData\Roaming\Thunderbird\Profiles\aofl1o4o.default-release\global-messages-db.sqlite"
conn = sqlite3.connect(f"file:{db_path}?immutable=1", uri=True)
c = conn.cursor()

# Filter for recent years (2024 - 2026)
# 2024-01-01 in timestamp microseconds
ts_2024 = int(datetime.datetime(2024, 1, 1).timestamp() * 1000000)

query = f"""
SELECT m.date, c.c3author, c.c4recipients, c.c1subject, c.c0body 
FROM messages m
JOIN messagesText_content c ON m.id = c.docid
WHERE m.date >= {ts_2024}
  AND (c.c0body LIKE '%výnos%' OR c.c1subject LIKE '%výnos%' OR c.c0body LIKE '%podíl%' OR c.c0body LIKE '%nevyplac%')
  AND (c.c0body LIKE '%bursov%' OR c.c1subject LIKE '%podklad%' OR c.c1subject LIKE '%výnos%' OR c.c0body LIKE '%mandelík%' OR c.c0body LIKE '%hábov%' OR c.c0body LIKE '%andělov%')
ORDER BY m.date DESC
"""

c.execute(query)
rows = c.fetchall()
print(f"Recent emails found: {len(rows)}")

seen = set()
for r in rows:
    dt = datetime.datetime.fromtimestamp(r[0] / 1000000.0) if r[0] else None
    dt_str = dt.strftime('%d.%m.%Y %H:%M') if dt else 'N/A'
    subj = r[3] or ''
    key = (dt_str, subj)
    if key in seen:
        continue
    seen.add(key)
    
    author = r[1] or ''
    body = r[4] or ''
    
    print("\n" + "="*70)
    print(f"DATUM: {dt_str} | OD: {author} | PŘEDMĚT: {subj}")
    print("="*70)
    # print all lines mentioning money, share, unpaid, names
    for line in body.splitlines():
        l_low = line.lower()
        if any(k in l_low for k in ['výnos', 'podíl', 'vyplat', 'kč', 'andělov', 'hábov', 'mandelík', 'večeř', 'zimová', 'bertuzzi', 'měsíčkov', 'soldát']):
            print("  *", line.strip())
