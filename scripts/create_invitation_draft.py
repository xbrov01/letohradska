# -*- coding: utf-8 -*-
import os
import sys
import ssl
import time
import imaplib
from email.message import EmailMessage
from email.utils import make_msgid, formatdate

sys.path.insert(0, os.path.abspath('.'))
from scripts.create_draft import load_env, get_drafts_folder

def main():
    env = load_env()
    user = env.get("GMAIL_USER")
    pwd = env.get("GMAIL_APP_PASSWORD")

    if not user or not pwd:
        raise ValueError("V .env chybí GMAIL_USER nebo GMAIL_APP_PASSWORD.")

    context = ssl.create_default_context()
    mail = imaplib.IMAP4_SSL("imap.gmail.com", port=993, ssl_context=context)
    mail.login(user, pwd)

    try:
        drafts_folder = get_drafts_folder(mail)
        print(f"Složka konceptů: {drafts_folder}")

        msg = EmailMessage()
        msg['From'] = f"Veronika Brožová <{user}>"
        msg['To'] = f"Veronika Brožová <{user}>"
        
        # Bcc skupina SV (27 adres vlastníků SVJ Letohradská)
        bcc_list = [
            "jaou@centrum.cz", "jholub@email.cz", "LenkaHM@seznam.cz", 
            "iva.mesickova@gmail.com", "ivamachacova@seznam.cz", 
            "monika.soleova@unicreditgroup.cz", "porizkovah@seznam.cz", 
            "vladimir.bukac@seznam.cz", "ekitzlerova@centrum.cz", 
            "Roman.Prochazka@hochtief.cz", "rumleriva@seznam.cz", 
            "bonobak@seznam.cz", "bertuzzig@gmail.com", "milan.trefny@seznam.cz", 
            "soppejana5@gmail.com", "ivosebera@seznam.cz", "barandel@seznam.cz", 
            "habovaka@volny.cz", "jiri@kaifosz.cz", "lucie.pavlicek@seznam.cz", 
            "jalovy@gmail.com", "jnyvltova@tiscali.cz", "rusprg@yahoo.com", 
            "malirhorak@seznam.cz", "radovan.soldat@yahoo.com", 
            "dubovaschranka@volny.cz", "porizka@seznam.cz", "a@visualio.cz"
        ]
        msg['Bcc'] = ", ".join(bcc_list)
        msg['Subject'] = "pozvánka na 15. shromáždění SV Letohradská"
        msg['Date'] = formatdate(localtime=True)
        msg['Message-ID'] = make_msgid()
        msg['X-Unsent'] = '1'

        body_text = (
            "Dobrý den,\n\n"
            "v příloze Vám zasílám pozvánku na 15. shromáždění vlastníků jednotek SV Letohradská 367/5, "
            "které se bude konat v pondělí 30. listopadu 2026 od 18:30 hodin v bytě č. 367/9 (přízemí vpravo).\n\n"
            "Kdo máte možnost, přineste si prosím s sebou židli.\n\n"
            "Součástí přílohy je i formulář plné moci. Připomínám, že plná moc je potřeba i v případě společného jmění manželů (SJM) "
            "a spoluvlastnictví – pokud dorazí pouze jeden z manželů či spoluvlastníků, nechte si ji prosím předem podepsat, "
            "aby bylo možné za jednotku platně hlasovat. Případně můžete někoho zplnomocnit, pokud již víte, že se nebudete moci zúčastnit osobně. "
            "Plná moc nemusí být úředně ověřena.\n\n"
            "Děkuji a těším se na setkání.\n\n"
            "Hezké dny,\n"
            "Veronika Brožová\n"
        )
        msg.set_content(body_text)

        # Attach docx
        docx_path = os.path.abspath('agenda/zapisy/2026-11-30_pozvanka_15_shromazdeni.docx')
        if os.path.exists(docx_path):
            with open(docx_path, 'rb') as f:
                data = f.read()
            msg.add_attachment(
                data,
                maintype='application',
                subtype='vnd.openxmlformats-officedocument.wordprocessingml.document',
                filename='2026-11-30_pozvanka_15_shromazdeni.docx'
            )
            print(f"Připojena příloha: {docx_path} ({len(data)} bajtů)")

        raw_bytes = msg.as_bytes()
        status, response = mail.append(drafts_folder, '\\Draft', imaplib.Time2Internaldate(time.time()), raw_bytes)
        if status == 'OK':
            print("✅ Koncept úspěšně vytvořen v Gmailu!")
            return True
        else:
            print(f"❌ Chyba při vytváření konceptu: {status} {response}")
            return False
    finally:
        mail.logout()

if __name__ == '__main__':
    main()
