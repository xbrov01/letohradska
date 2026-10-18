# -*- coding: utf-8 -*-
import sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')
db_path = r'C:\Users\nikan\AppData\Roaming\Thunderbird\Profiles\aofl1o4o.default-release\global-messages-db.sqlite'
conn = sqlite3.connect(f'file:{db_path}?immutable=1', uri=True)
c = conn.cursor()
c.execute("""
SELECT c3author, c4recipients, c1subject, c0body 
FROM messagesText_content 
WHERE (c0body LIKE '%bosch%' OR c1subject LIKE '%bosch%') 
  AND (c0body LIKE '%smlouv%' OR c0body LIKE '%nájem%' OR c0body LIKE '%dohod%')
""")
rows = c.fetchall()
print('Found:', len(rows))
for r in rows:
    print('-----------------------------------------')
    print('SUBJ:', r[2])
    print('FROM:', r[0])
    for line in r[3].splitlines():
        if any(w in line.lower() for w in ['bosch', 'smlouv', 'nájem', 'inflac', 'plat']):
            print('  ', line.strip()[:200])
