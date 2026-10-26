# -*- coding: utf-8 -*-
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.create_draft import create_gmail_draft

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 1. Zdeněk Křivský
body_krivsky = """Ahoj Zdeňku,

shromáždění vlastníků budeme mít koncem listopadu nebo začátkem prosince, takže tam nechám schválit zadání projektu (projektovou dokumentaci té jižní fasády).

Pokud to na shromáždění schválíme, bylo by super to hned zadat, aby se na tom mohlo začít dělat v tom lednu nebo únoru, jak jsi psal, že mívá kolega projektant nejvíc prostoru před sezónou.

Hned po shromáždění se ti ozvu s výsledkem a domluvíme další postup.

Díky moc a měj se fajn,

Nika

--  
Veronika Brožová  
Předsedkyně výboru SVJ Letohradská 367/5, Praha 7  
Tel.: +420 603 527 274  
Email: nikabrozova@gmail.com
"""

print("\n--- Vytvářím koncept pro: Zdeněk Křivský ---")
create_gmail_draft(
    to_email="Zdeněk Křivský <krivsky@porsenna.cz>",
    subject="Re: Fwd: Letohradská",
    body_text=body_krivsky,
    reply_to_query='FROM "krivsky@porsenna.cz"'
)

# 2. Lenka Holubová Mikolášová
body_mikolasova = """Ahoj Lenko,

pomalu dávám dohromady podklady a program pro podzimní shromáždění vlastníků, které plánuji na přelom listopadu a prosince (konec listopadu).

V té souvislosti bych se tě chtěla zeptat, jestli sis náhodou s odstupem času nerozmyslela své odstoupení z výboru. Byla bych moc ráda, kdybys ve výboru zůstala a pokračovala s námi. Potřebuji vědět, jak na tom jsme při přípravě pozvánky a programu – abych věděla, zda mám mezi vlastníky hledat a oslovovat někoho nového na volbu 3. člena výboru, nebo jestli můžeme dál počítat s tebou.

Zároveň bych ještě jednou chtěla zdůraznit, že mě celá ta věc kolem břečťanu opravdu moc mrzí. Z mé strany v tom rozhodně nebyl žádný záměr ani to nebylo nic naschvál – prostě se to tehdy takhle nešťastně semlelo a stalo. Byla by velká škoda, kdyby to mezi námi mělo zanechat pachuť nebo narušit fungování domu.

Dej mi prosím vědět, jak to vidíš a jaké je tvé aktuální rozhodnutí, abychom se podle toho mohli zařídit. Kdybys to chtěla ještě probrat osobně u kávy, ráda se domluvím.

Měj se moc hezky,

Nika

--  
Veronika Brožová  
Předsedkyně výboru SVJ Letohradská 367/5, Praha 7  
Tel.: +420 603 527 274  
Email: nikabrozova@gmail.com
"""

print("\n--- Vytvářím koncept pro: Lenka Holubová Mikolášová ---")
create_gmail_draft(
    to_email="Lenka Holubová Mikolášová <LenkaHM@seznam.cz>",
    subject="Re: Odstoupení z funkce člena výboru společesntví",
    body_text=body_mikolasova,
    reply_to_query='FROM "LenkaHM@seznam.cz"'
)
