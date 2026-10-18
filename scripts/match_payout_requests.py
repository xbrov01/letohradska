# -*- coding: utf-8 -*-
import sqlite3, sys

sys.stdout.reconfigure(encoding='utf-8')

db_path = r"C:\Users\nikan\AppData\Roaming\Thunderbird\Profiles\aofl1o4o.default-release\global-messages-db.sqlite"
conn = sqlite3.connect(f"file:{db_path}?immutable=1", uri=True)
c = conn.cursor()

# Get the campaign email sent on 16.02.2026
c.execute("""
SELECT c3author, c4recipients, c1subject, c0body
FROM messagesText_content
WHERE c1subject LIKE 'Výnosy ze společně vlastněných jednotek za rok 2025'
  AND c3author LIKE '%Brožová%'
LIMIT 1
""")
r = c.fetchone()
recipients = r[1] if r else ""
print("Recipients string:")
print(recipients)

# Let's find all replies to this campaign in 2026
c.execute("""
SELECT m.date, c.c3author, c.c1subject, c.c0body
FROM messages m
JOIN messagesText_content c ON m.id = c.docid
WHERE c.c1subject LIKE '%Výnosy ze společně vlastněných jednotek za rok 2025%'
  AND c3author NOT LIKE '%Brožová%'
ORDER BY m.date ASC
""")
replies = c.fetchall()
print(f"\nTotal incoming replies: {len(replies)}")
import datetime
repliers = {}
for rep in replies:
    dt = datetime.datetime.fromtimestamp(rep[0] / 1000000.0) if rep[0] else None
    dt_str = dt.strftime('%d.%m.%Y') if dt else 'N/A'
    author = rep[1]
    body = rep[3]
    has_request = any(w in body.lower() for w in ['žádost', 'podklad k výplatě', 'zadost', 'převod', 'účet', 'zaslat výnosy'])
    repliers[author] = (dt_str, has_request, body[:100].replace('\n', ' '))

for auth, info in repliers.items():
    print(f"  REPLY: {auth} | Date: {info[0]} | Has request: {info[1]} | Snippet: {info[2]}")
