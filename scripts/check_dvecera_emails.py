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
WHERE (c.c3author LIKE '%dvecera%' OR c.c4recipients LIKE '%dvecera%')
ORDER BY m.date DESC
""")
rows = c.fetchall()
print(f"Emails with dvecera@volny.cz: {len(rows)}")
import datetime
for r in rows[:10]:
    dt = datetime.datetime.fromtimestamp(r[0] / 1000000.0) if r[0] else None
    print(dt, '|', r[1], '|', r[2], '|', r[3])
