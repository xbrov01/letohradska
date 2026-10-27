# -*- coding: utf-8 -*-
import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PDF = os.path.join(BASE_DIR, "agenda", "zapisy", "2026-10-27_navrh_na_zapis_do_rejstriku_svj.pdf")

# Register Arial for full Czech support
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Italic', 'C:/Windows/Fonts/ariali.ttf'))

def generate_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    style_normal = ParagraphStyle(
        'NormalCzech',
        fontName='Arial',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#222222')
    )
    style_bold = ParagraphStyle(
        'BoldCzech',
        fontName='Arial-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#111111')
    )
    style_title = ParagraphStyle(
        'TitleCzech',
        fontName='Arial-Bold',
        fontSize=14,
        leading=18,
        alignment=1, # Center
        textColor=colors.HexColor('#111111')
    )
    style_subtitle = ParagraphStyle(
        'SubTitleCzech',
        fontName='Arial-Bold',
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.HexColor('#333333')
    )
    style_header_box = ParagraphStyle(
        'HeaderBox',
        fontName='Arial',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#222222')
    )

    elements = []

    # Header: Adresát a Navrhovatel
    header_data = [
        [
            Paragraph("<b>PŘÍJEMCE (REJSTŘÍKOVÝ SOUD):</b><br/>"
                      "<b>Městský soud v Praze</b><br/>"
                      "Rejstříkový úsek<br/>"
                      "Spálená 2, 112 16 Praha 2<br/>"
                      "<b>ID datové schránky: snkabbm</b>", style_header_box),
            Paragraph("<b>NAVRHOVATEL (ZAPSANÁ OSOBA):</b><br/>"
                      "<b>Společenství vlastníků Letohradská 367, Praha 7</b><br/>"
                      "Sídlo: Letohradská 367/5, Holešovice, 170 00 Praha 7<br/>"
                      "<b>IČO: 242 39 178</b><br/>"
                      "<b>Spisová značka: S 14107</b> vedená u MSPH<br/>"
                      "<b>ID datové schránky: g8z5iva</b>", style_header_box)
        ]
    ]

    t_header = Table(header_data, colWidths=[245, 260])
    t_header.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cccccc')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fcfcfc')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t_header)
    elements.append(Spacer(1, 15))

    # Titul podání
    elements.append(Paragraph("NÁVRH NA ZÁPIS ZMĚN DO REJSTŘÍKU SVJ", style_title))
    elements.append(Paragraph("a žádost o aktualizaci údajů statutárního orgánu (sp. zn. S 14107)", style_subtitle))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#333333'), spaceAfter=12))

    # Text podání
    p1 = ("Společenství vlastníků Letohradská 367, Praha 7, IČO: 242 39 178, zastoupené předsedkyní výboru "
          "Veronikou Brožovou, tímto v souladu se zákonem č. 304/2013 Sb., o veřejných rejstřících právnických a fyzických osob, "
          "a zákonem č. 89/2012 Sb., občanský zákoník, podává tento")
    elements.append(Paragraph(p1, style_normal))
    elements.append(Spacer(1, 6))

    p2 = ("<b>návrh na zápis změn v osobách statutárního orgánu (výboru) společenství na další funkční období</b> "
          "a doložení schválených dokumentů do Sbírky listin.")
    elements.append(Paragraph(p2, style_bold))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("<b>I. Skutkový stav a rozhodnutí shromáždění SVJ</b>", style_bold))
    p3 = ("1. Dne <b>18. 11. 2025</b> se konalo řádné 14. shromáždění Společenství vlastníků Letohradská 367, Praha 7. "
          "Shromáždění bylo řádně svoláno a bylo usnášeníschopné za účasti 23 spoluvlastníků disponujících celkem "
          "17 322 podíly z 21 075 (tj. 82,19 % všech hlasů).<br/>"
          "2. V <b>bodu 11)</b> programu shromáždění proběhla volba členů statutárního orgánu (výboru) a kontrolní komise "
          "z důvodu uplynutí dosavadního funkčního období. Shromáždění <b>jednomyslně 100 % přítomných hlasů</b> "
          "(23 hlasů pro, 0 proti, 0 se zdrželo) zvolilo na následující funkční období (dle stanov 5 let) tyto členy výboru:<br/>"
          "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Veronika Brožová</b>, nar. 08. 06. 1970, bytem Letohradská 367/5, 170 00 Praha 7<br/>"
          "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Milan Trefný</b>, nar. 13. 07. 1957, bytem Letohradská 367/5, 170 00 Praha 7<br/>"
          "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Ing. arch. Lenka Holubová Mikolášová</b>, nar. 06. 06. 1969, bytem Letohradská 367/5, 170 00 Praha 7<br/>"
          "3. Následně na schůzi výboru společenství dne <b>18. 11. 2025</b> došlo k rozdělení funkcí tak, že byla zvolena:<br/>"
          "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Veronika Brožová</b> jako <b>předsedkyně výboru</b><br/>"
          "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Milan Trefný</b> jako <b>místopředseda výboru</b><br/>"
          "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Ing. arch. Lenka Holubová Mikolášová</b> jako <b>členka výboru</b><br/>"
          "Všichni navržení kandidáti své funkce výslovně a jednomyslně přijali, což stvrdili svými podpisy.<br/>"
          "4. Všichni tři výše uvedení členové výboru <b>již jsou ve veřejném rejstříku zapsáni</b>. "
          "Jedná se o jejich znovuzvolení a pokračování ve funkci statutárního orgánu na nové funkční období.")
    elements.append(Paragraph(p3, style_normal))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("<b>II. Návrh na zápis (Návrhový petit)</b>", style_bold))
    p4 = ("Navrhovatel navrhuje, aby Městský soud v Praze jako soud rejstříkový vydal usnesení, kterým v Rejstříku "
          "společenství vlastníků jednotek, oddíl S, vložka 14107, <b>provede zápis následujících změn</b>:<br/><br/>"
          "<b>Statutární orgán – výbor:</b><br/>"
          "Zapisují se údaje o novém funkčním období stávajících členů výboru s datem vzniku:<br/>"
          "&nbsp;&nbsp;• <b>Veronika Brožová</b>: předsedkyně výboru, den vzniku členství: 18. 11. 2025, den vzniku funkce: 18. 11. 2025<br/>"
          "&nbsp;&nbsp;• <b>Milan Trefný</b>: místopředseda výboru, den vzniku členství: 18. 11. 2025, den vzniku funkce: 18. 11. 2025<br/>"
          "&nbsp;&nbsp;• <b>Ing. arch. Lenka Holubová Mikolášová</b>: členka výboru, den vzniku členství: 18. 11. 2025<br/>"
          "(s výmazem údajů o předchozích uplynulých mandátech zapsaných k historickým datům).")
    elements.append(Paragraph(p4, style_normal))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("<b>III. Založení do Sbírky listin</b>", style_bold))
    p5 = ("Současně navrhovatel žádá o založení přiloženého zápisu ze 14. shromáždění SVJ do Sbírky listin.")
    elements.append(Paragraph(p5, style_normal))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("<b>IV. Osvobození od soudního poplatku a forma podání</b>", style_bold))
    p6 = ("1. Dle zákona č. 549/1991 Sb., o soudních poplatcích (Položka 11 odst. 1 písm. e) sazebníku poplatků) "
          "je řízení ve věcech veřejného rejstříku týkající se společenství vlastníků jednotek <b>osvobozeno od soudního poplatku</b>.<br/>"
          "2. Podání je učiněno elektronicky přímo z <b>datové schránky navrhovatele (ID: g8z5iva)</b>, "
          "což v souladu se zákonem plně nahrazuje úřední ověření podpisů navrhovatelů. V případě, že by rejstříkový soud "
          "z formálních důvodů požadoval doplnění výstupního formuláře, navrhovatel žádá o zápis shora uvedených nesporných "
          "skutečností z moci úřední dle § 101 zákona č. 304/2013 Sb., popř. o zaslání konkrétní výzvy.")
    elements.append(Paragraph(p6, style_normal))
    elements.append(Spacer(1, 12))

    # Přílohy
    elements.append(Paragraph("<b>Seznam připojených listin (příloh):</b>", style_bold))
    prilohy = ("1. <b>Zápis ze 14. shromáždění SVJ konaného dne 18. 11. 2025</b> včetně prezenční listiny s podpisy vlastníků a přehledu hlasování (soubor PDF).<br/>"
               "2. <b>Zápis ze schůze výboru SVJ ze dne 18. 11. 2025</b> o volbě předsedy a místopředsedy výboru s podpisy členů výboru (soubor PDF).")
    elements.append(Paragraph(prilohy, style_normal))
    elements.append(Spacer(1, 18))

    # Podpis
    elements.append(Paragraph("V Praze dne 27. 10. 2026", style_normal))
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("<b>Společenství vlastníků Letohradská 367, Praha 7</b><br/>"
                              "Veronika Brožová, v. r.<br/>"
                              "<i>předsedkyně výboru SVJ</i><br/>"
                              "(podáno elektronicky prostřednictvím datové schránky SVJ ID: g8z5iva)", style_bold))

    doc.build(elements)
    print(f"✅ Hotovo, PDF vygenerováno do: {OUTPUT_PDF}")

if __name__ == '__main__':
    generate_pdf()
