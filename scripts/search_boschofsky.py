# -*- coding: utf-8 -*-
import sqlite3, os, sys

sys.stdout.reconfigure(encoding='utf-8')

db_path = r"C:\Users\nikan\AppData\Roaming\Thunderbird\Profiles\aofl1o4o.default-release\global-messages-db.sqlite"
conn = sqlite3.connect(f"file:{db_path}?immutable=1", uri=True)
c = conn.cursor()

c.execute("SELECT c3author, c4recipients, c1subject, c0body FROM messagesText_content WHERE c0body LIKE '%bosch%' OR c1subject LIKE '%bosch%' OR c0body LIKE '%boschof%'")
rows = c.fetchall()
print(f"Thunderbird messages found: {len(rows)}")
for r in rows:
    print("--------------------------------------------------")
    print("AUTOR:", r[0])
    print("KOMU:", r[1])
    print("PŘEDMĚT:", r[2])
    # print snippet
    body = r[3] or ""
    idx = body.lower().find("bosch")
    snippet = body[max(0, idx-100):min(len(body), idx+300)].replace('\n', ' ')
    print("ÚRYVEK:", snippet)
