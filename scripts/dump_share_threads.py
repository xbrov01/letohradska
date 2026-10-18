# -*- coding: utf-8 -*-
import sqlite3, sys

sys.stdout.reconfigure(encoding='utf-8')

db_path = r"C:\Users\nikan\AppData\Roaming\Thunderbird\Profiles\aofl1o4o.default-release\global-messages-db.sqlite"
conn = sqlite3.connect(f"file:{db_path}?immutable=1", uri=True)
c = conn.cursor()

query = """
SELECT m.date, c.c3author, c.c1subject, c.c0body 
FROM messages m
JOIN messagesText_content c ON m.id = c.docid
WHERE c.c1subject LIKE '%další podklady%' 
   OR c.c1subject LIKE '%vyplacení výnosů%'
   OR c.c1subject LIKE '%Upravené protokoly%'
   OR (c.c0body LIKE '%výnosy a nebyly jim vyplaceny%' OR c.c0body LIKE '%84 057%')
ORDER BY m.date ASC
"""

c.execute(query)
import datetime
for r in c.fetchall():
    dt = datetime.datetime.fromtimestamp(r[0] / 1000000.0) if r[0] else None
    dt_str = dt.strftime('%d.%m.%Y %H:%M') if dt else 'N/A'
    print("\n" + "="*80)
    print(f"DATUM: {dt_str} | OD: {r[1]} | PŘEDMĚT: {r[2]}")
    print("="*80)
    print(r[3])
