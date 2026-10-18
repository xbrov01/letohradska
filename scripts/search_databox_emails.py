# -*- coding: utf-8 -*-
import sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')

db_path = r"C:\Users\nikan\AppData\Roaming\Thunderbird\Profiles\aofl1o4o.default-release\global-messages-db.sqlite"
conn = sqlite3.connect(f"file:{db_path}?immutable=1", uri=True)
c = conn.cursor()

c.execute("""
SELECT c3author, c4recipients, c1subject, c0body 
FROM messagesText_content 
WHERE c0body LIKE '%datov%schránk%' 
   OR c1subject LIKE '%datov%schránk%' 
   OR c0body LIKE '%mojedatovaschranka%'
   OR c3author LIKE '%datovaschranka%'
   OR c0body LIKE '%g8z5iva%'
""")
rows = c.fetchall()
print(f"Found datova schranka emails: {len(rows)}")
for r in rows:
    print("-----------------------------------------")
    print("FROM:", r[0])
    print("SUBJ:", r[2])
    body = (r[3] or "").replace("\n", " ")
    print("BODY:", body[:300])
