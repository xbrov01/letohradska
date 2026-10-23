# -*- coding: utf-8 -*-
"""
Kompletní generátor nájemních smluv a průvodních dopisů:
  1. DDAANN s.r.o. (Nebytový prostor č. 367/101) - doba neurčitá, výpověď 6 měs., nájem 13 000 Kč, služby 876 Kč, celkem 13 876 Kč, VS 367101
  2. Ivo Boschofsky (Byt č. 367/1) - doba určitá 1 rok s prolongací a výhradou neplnění, nájem 12 000 Kč, služby 559 Kč, celkem 12 559 Kč, VS 3671, důraz na účet a PRE
  3. Tetsu Onari (Byt č. 367/3) - doba určitá 1 rok s prolongací a výhradou neplnění, nájem 7 700 Kč, služby 2 150 Kč, celkem 9 850 Kč, VS 3673
Vše generováno ve formátech .docx i .md a uloženo do cílových adresářů.
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

# Autorizovaný seznam podílových spoluvlastníků (autorita: vlastnici.docx)
CO_OWNERS = [
    ("Barbora Andělová", "Voděradská 390/11, Strašnice, 100 00 Praha 10"),
    ("Gianluca Bertuzzi", "Pplk. Sochora 694/24, Holešovice, 170 00 Praha 7"),
    ("SJM Ing. Vojtěch Brož a Veronika Brožová", "Letohradská 367/5, Holešovice, 170 00 Praha 7"),
    ("SJM Ing. Vladimír Bukač a Svatava Bukačová", "Letohradská 367/5, Holešovice, 170 00 Praha 7"),
    ("Ing. Kateřina Hábová", "Chopinova 1521/26, Vinohrady, 120 00 Praha 2"),
    ("Vlastimil Jalový", "Bubenská 1158/17, Holešovice, 170 00 Praha 7"),
    ("Jiří Kaifosz, akademický sochař", "Dobrovského 872/28, Holešovice, 170 00 Praha 7"),
    ("MUDr. Eva Kitzlerová", "Ovenecká 363/30, Bubeneč, 170 00 Praha 7"),
    ("MgA. Iva Kopecká", "Letohradská 367/5, Holešovice, 170 00 Praha 7"),
    ("Božena Mandelíková", "Letohradská 367/5, Holešovice, 170 00 Praha 7"),
    ("Jaroslav Ouředníček", "Letohradská 367/5, Holešovice, 170 00 Praha 7"),
    ("Mgr. Lucie Pavlíčková", "Nad Turbovou 1191/15, Košíře, 150 00 Praha 5"),
    ("Mgr. Aleš Pořízka", "Letohradská 367/5, Holešovice, 170 00 Praha 7"),
    ("Mgr. Hana Pořízková", "Kamenická 654/52, Holešovice, 170 00 Praha 7"),
    ("Karel Procházka", "Letohradská 367/5, Holešovice, 170 00 Praha 7"),
    ("Roman Procházka", "Babákova 2161/24, Chodov, 148 00 Praha 4"),
    ("Libuše Procházková", "Letohradská 367/5, Holešovice, 170 00 Praha 7"),
    ("SJM Stanislav Rumler a Ivana Rumlerová", "Letohradská 367/5, Holešovice, 170 00 Praha 7"),
    ("Ing. Ivo Sebera", "Letohradská 367/5, Holešovice, 170 00 Praha 7"),
    ("Radovan Soldát", "Pod altánem 89/93, Strašnice, 100 00 Praha 10"),
    ("Martin Soppé", "č. p. 130, 783 44 Drahanovice"),
    ("Božena Spurná", "Letohradská 367/5, Holešovice, 170 00 Praha 7"),
    ("SJM Ing. Zbyněk Šole a Monika Šoleová", "Letohradská 367/5, Holešovice, 170 00 Praha 7"),
    ("SJM Milan Trefný a Milena Trefná", "Letohradská 367/5, Holešovice, 170 00 Praha 7"),
    ("David Večeřa", "Ovenecká 1072/17, Holešovice, 170 00 Praha 7"),
    ("Jitka Zímová", "Letohradská 367/5, Holešovice, 170 00 Praha 7"),
]

def style_document(doc):
    for section in doc.sections:
        section.top_margin = Inches(0.85)
        section.bottom_margin = Inches(0.85)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
    
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Calibri'
    font.size = Pt(10.5)
    font.color.rgb = RGBColor(30, 30, 30)
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(4)

def add_header_title(doc, title_text, subtitle_text=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(title_text)
    run.font.name = 'Calibri'
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = RGBColor(20, 20, 20)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(0)
    
    if subtitle_text:
        p2 = doc.add_paragraph()
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run2 = p2.add_run(subtitle_text)
        run2.font.name = 'Calibri'
        run2.font.size = Pt(10.5)
        run2.font.italic = True
        run2.font.color.rgb = RGBColor(80, 80, 80)
        p2.paragraph_format.space_after = Pt(10)

def add_article_heading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(9)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor(20, 50, 90)

def add_paragraph_styled(doc, text, bold_prefix=None, space_after=4, bullet=False):
    p = doc.add_paragraph(style='List Bullet' if bullet else 'Normal')
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = 'Calibri'
        r_bold.font.size = Pt(10)
        r_bold.font.bold = True
    if text:
        r_text = p.add_run(text)
        r_text.font.name = 'Calibri'
        r_text.font.size = Pt(10)
    return p

def add_co_owners_table(doc, unit_label):
    add_paragraph_styled(doc, f"1. Podíloví spoluvlastníci {unit_label}:", bold_prefix=None, space_after=2)
    
    table = doc.add_table(rows=0, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    
    half = (len(CO_OWNERS) + 1) // 2
    for i in range(half):
        row = table.add_row()
        name1, addr1 = CO_OWNERS[i]
        c1 = row.cells[0]
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(1)
        p1.paragraph_format.line_spacing = 1.05
        r1 = p1.add_run(f"• {name1}, ")
        r1.font.size = Pt(8.5)
        r1.font.bold = True
        r1_addr = p1.add_run(addr1)
        r1_addr.font.size = Pt(8.5)
        
        c2 = row.cells[1]
        p2 = c2.paragraphs[0]
        p2.paragraph_format.space_after = Pt(1)
        p2.paragraph_format.line_spacing = 1.05
        if i + half < len(CO_OWNERS):
            name2, addr2 = CO_OWNERS[i + half]
            r2 = p2.add_run(f"• {name2}, ")
            r2.font.size = Pt(8.5)
            r2.font.bold = True
            r2_addr = p2.add_run(addr2)
            r2_addr.font.size = Pt(8.5)
            
    p_rep = doc.add_paragraph()
    p_rep.paragraph_format.space_before = Pt(4)
    p_rep.paragraph_format.space_after = Pt(4)
    p_rep.paragraph_format.line_spacing = 1.15
    r = p_rep.add_run("na základě plné moci zastoupeni správcem nemovitosti:\n")
    r.font.size = Pt(9.5)
    r2 = p_rep.add_run("Veronika Brožová")
    r2.font.size = Pt(9.5)
    r2.font.bold = True
    r3 = p_rep.add_run(", bytem Letohradská 367/5, Holešovice, 170 00 Praha 7\n")
    r3.font.size = Pt(9.5)
    r4 = p_rep.add_run("Prostředky spojené se správou a užíváním prostoru spravuje na svém účtu:\n")
    r4.font.size = Pt(9.5)
    r5 = p_rep.add_run("Společenství vlastníků Letohradská 367, Praha 7")
    r5.font.size = Pt(9.5)
    r5.font.bold = True
    r6 = p_rep.add_run(", se sídlem Letohradská 5/367, 170 00 Praha 7, IČ: 24239178, č. ú. ")
    r6.font.size = Pt(9.5)
    r7 = p_rep.add_run("2844175379/0800")
    r7.font.size = Pt(9.5)
    r7.font.bold = True
    r8 = p_rep.add_run(", vedený u České spořitelny a.s.\n(dále jen „pronajímatel“ na straně jedné)")
    r8.font.size = Pt(9.5)

def add_signature_block(doc, left_title, left_name, right_title, right_name):
    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(12)
    p_space.paragraph_format.space_after = Pt(8)
    
    table = doc.add_table(rows=3, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    for row in table.rows:
        row.cells[0].width = Inches(3.2)
        row.cells[1].width = Inches(3.2)
        
    c00 = table.cell(0, 0)
    p00 = c00.paragraphs[0]
    p00.add_run("V Praze dne .............................. 2026")
    
    c01 = table.cell(0, 1)
    p01 = c01.paragraphs[0]
    p01.add_run("V Praze dne .............................. 2026")
    
    c10 = table.cell(1, 0)
    p10 = c10.paragraphs[0]
    p10.paragraph_format.space_before = Pt(26)
    p10.add_run(".............................................................")
    
    c11 = table.cell(1, 1)
    p11 = c11.paragraphs[0]
    p11.paragraph_format.space_before = Pt(26)
    p11.add_run(".............................................................")
    
    c20 = table.cell(2, 0)
    p20 = c20.paragraphs[0]
    r_l_name = p20.add_run(left_name + "\n")
    r_l_name.font.bold = True
    r_l_title = p20.add_run(left_title)
    r_l_title.font.size = Pt(9.5)
    r_l_title.font.italic = True
    
    c21 = table.cell(2, 1)
    p21 = c21.paragraphs[0]
    r_r_name = p21.add_run(right_name + "\n")
    r_r_name.font.bold = True
    r_r_title = p21.add_run(right_title)
    r_r_title.font.size = Pt(9.5)
    r_r_title.font.italic = True


# ==============================================================================
# 1. SMLOUVA DDAANN s.r.o. (.docx)
# ==============================================================================
def build_docx_ddaann_contract():
    doc = docx.Document()
    style_document(doc)
    
    add_header_title(doc, "SMLOUVA O NÁJMU PROSTORU SLOUŽÍCÍHO PODNIKÁNÍ", 
                     "(nebytový prostor č. 367/101 v domě Letohradská 367/5, Praha 7)")
    
    add_paragraph_styled(doc, "uzavřená níže uvedeného dne, měsíce a roku podle ustanovení § 2302 a násl. zákona č. 89/2012 Sb., občanský zákoník, v platném znění (dále jen „občanský zákoník“), mezi smluvními stranami:")
    
    add_article_heading(doc, "Smluvní strany:")
    add_co_owners_table(doc, "nebytové jednotky č. 367/101")
    
    add_paragraph_styled(doc, "a", bold_prefix=None, space_after=2)
    add_paragraph_styled(doc, "DDAANN s.r.o.", bold_prefix="2. Nájemce: ")
    add_paragraph_styled(doc, "se sídlem Letohradská 367/5, Holešovice, 170 00 Praha 7\n"
                              "IČ: 14042967, DIČ: CZ14042967\n"
                              "Zapsaná v obchodním rejstříku vedeném Městským soudem v Praze, oddíl C, vložka 359424\n"
                              "Zastoupená jednateli: Ing. arch. Danem Mertou / MgA. Danielem Baudisem\n"
                              "Číslo bankovního účtu nájemce: [Doplní nájemce]\n"
                              "(dále jen „nájemce“ na straně druhé)")
    
    add_article_heading(doc, "Čl. 1 – Předmět a účel nájmu")
    add_paragraph_styled(doc, "1. Předmětem nájmu je nebytový prostor č. 367/101 nacházející se v 1. nadzemním podlaží (přízemí) domu čp. 367, Letohradská 5, Praha 7, o celkové výměře 65,0 m². Jde o prostor s vlastním vchodem přímo z Letohradské ulice, situovaný vlevo od hlavního vstupu do domu. Sociální zařízení je přístupné ze společné chodby.")
    add_paragraph_styled(doc, "2. Předmět nájmu je pronajímán jako prostor sloužící podnikání za účelem provozování architektonické, projekční, designérské a kancelářské činnosti nájemce v souladu s předmětem jeho podnikání zapsaným v obchodním rejstříku.")
    add_paragraph_styled(doc, "3. Společné prostory domu je nájemce oprávněn užívat v rozsahu přiměřeném řádnému užívání předmětu nájmu.")
    add_paragraph_styled(doc, "4. Změna sjednaného účelu užívání je možná pouze s předchozím písemným souhlasem pronajímatele.")

    add_article_heading(doc, "Čl. 2 – Stav předmětu nájmu")
    add_paragraph_styled(doc, "1. Nájemce prohlašuje, že je mu stav předmětu nájmu z titulu jeho dosavadního dlouhodobého užívání detailně znám, seznámil se s jeho technickým i stavebním stavem a v tomto stavu jej bez výhrad do nájmu přejímá.")
    add_paragraph_styled(doc, "2. Po skončení nájmu je nájemce povinen předat předmět nájmu pronajímateli ve stavu, v jakém jej převzal, s přihlédnutím k běžnému opotřebení a odsouhlaseným stavebním úpravám. Předání se uskuteční na základě oboustranně podepsaného předávacího protokolu.")

    add_article_heading(doc, "Čl. 3 – Práva a povinnosti smluvních stran")
    add_paragraph_styled(doc, "Nájemce je povinen zejména:", bold_prefix="1. ")
    add_paragraph_styled(doc, "užívat předmět nájmu výhradně k dohodnutému účelu a pečovat o něj s péčí řádného hospodáře;", bullet=True)
    add_paragraph_styled(doc, "neprovádět žádné stavební úpravy ani zásahy do dispozice, rozvodů a konstrukcí bez předchozího písemného souhlasu pronajímatele;", bullet=True)
    add_paragraph_styled(doc, "bez zbytečného odkladu oznámit pronajímateli potřebu nezbytných oprav jdoucích k tíži pronajímatele a umožnit jejich provedení;", bullet=True)
    add_paragraph_styled(doc, "běžnou údržbu a drobné opravy v předmětu nájmu provádět na vlastní náklad;", bullet=True)
    add_paragraph_styled(doc, "předcházet vzniku škod a pojistit svou činnost i majetek v předmětu nájmu proti případným škodám způsobeným třetím osobám;", bullet=True)
    add_paragraph_styled(doc, "neumožnit užívání předmětu nájmu ani jeho části třetím osobám (podnájem) bez předchozího písemného souhlasu pronajímatele;", bullet=True)
    add_paragraph_styled(doc, "bez předchozího písemného souhlasu pronajímatele neumisťovat na fasádu domu, společné chodby či okna reklamní tabule nebo zařízení přesahující obvyklé označení sídla/provozovny. Po ukončení nájmu je povinen zrušit sídlo společnosti na této adrese;", bullet=True)
    add_paragraph_styled(doc, "umožnit pronajímateli přístup do předmětu nájmu za účelem kontroly stavu a způsobu užívání, provádění odečtů a revizí, a to po předchozím včasném oznámení pronajímatelem. V případě havárie nebo bezprostředního nebezpečí je přístup možný ihned.", bullet=True)
    
    add_paragraph_styled(doc, "Dodávka elektrické energie a plynu není součástí služeb poskytovaných pronajímatelem. Odběrné místo elektřiny a plynu pro prostor č. 367/101 je/bude vedeno na základě smluv o sdružených službách dodávky uzavřených přímo mezi nájemcem a příslušnými dodavateli (PRE, PPAS) na účet a jméno nájemce. Po ukončení nájmu se nájemce zavazuje poskytnout veškerou součinnost k převodu odběrných míst zpět na pronajímatele bez jakýchkoliv nedoplatků.", bold_prefix="2. Dodávka energií (elektřina a plyn): ")
    add_paragraph_styled(doc, "Pronajímatel je povinen zajistit nájemci nerušený výkon práv spojených s užíváním předmětu nájmu a zajistit dodávku služeb spojených s užíváním domu (vodné a stočné, osvětlení a úklid společných prostor, odvoz odpadu).", bold_prefix="3. Povinnosti pronajímatele: ")

    add_article_heading(doc, "Čl. 4 – Nájemné a úhrada za služby")
    add_paragraph_styled(doc, "Nájemné se sjednává dohodou smluvních stran a činí 13 000,- Kč měsíčně (slovy: třináct tisíc korun českých).", bold_prefix="1. Výše nájemného: ")
    add_paragraph_styled(doc, "Společně s nájemným se nájemce zavazuje hradit měsíční zálohy na služby poskytované v souvislosti s užíváním prostoru (vodné a stočné, úklid a osvětlení společných prostor). Výše záloh je stanovena platným Výpočtovým listem a k datu podpisu smlouvy činí 876,- Kč měsíčně. Pronajímatel je oprávněn výši záloh upravit v návaznosti na změny cen dodavatelů služeb nebo změnu počtu osob. Zálohy podléhají ročnímu vyúčtování.", bold_prefix="2. Zálohy na služby: ")
    add_paragraph_styled(doc, "Celková měsíční platba (nájemné + zálohy na služby) ve výši 13 876,- Kč je splatná výhradně bezhotovostním převodem na bankovní účet č. 2844175379/0800, vedený u České spořitelny a.s. Platba je splatná měsíčně dopředu, vždy nejpozději do 15. dne příslušného kalendářního měsíce, za který se hradí. Jako variabilní symbol je nájemce povinen uvádět: 367101. Platby v hotovosti nejsou přípustné.", bold_prefix="3. Závazek bezhotovostní platby na účet: ")
    add_paragraph_styled(doc, "V případě prodlení s úhradou nájemného nebo záloh na služby se sjednává smluvní pokuta ve výši 0,1 % z dlužné částky za každý den prodlení. Přesáhne-li prodlení 30 kalendářních dnů, je pronajímatel oprávněn smlouvu jednostranně vypovědět.", bold_prefix="4. Prodlení a smluvní pokuta: ")

    add_article_heading(doc, "Čl. 5 – Inflační doložka")
    add_paragraph_styled(doc, "1. Smluvní strany se dohodly, že pronajímatel je oprávněn jednostranně zvýšit nájemné jednou ročně o míru inflace vyjádřenou přírůstkem průměrného ročního indexu spotřebitelských cen, vyhlašovaným Českým statistickým úřadem za předchozí kalendářní rok.")
    add_paragraph_styled(doc, "2. Překročí-li míra inflace 3 %, je pronajímatel oprávněn upravit nájemné k 1. říjnu kalendářního roku (nebo od měsíce následujícího po doručení písemného oznámení pronajímatele o zvýšení nájemného), poprvé od roku 2028.")

    add_article_heading(doc, "Čl. 6 – Doba nájmu a skončení nájmu")
    add_paragraph_styled(doc, "Tato smlouva se uzavírá na dobu neurčitou s účinností ode dne 1. 1. 2027.", bold_prefix="1. Doba nájmu: ")
    add_paragraph_styled(doc, "Nájemní vztah může zaniknout:", bold_prefix="2. Zánik nájmu: ")
    add_paragraph_styled(doc, "písemnou dohodou smluvních stran;", bullet=True)
    add_paragraph_styled(doc, "písemnou výpovědí kterékoliv ze smluvních stran bez uvedení důvodu s výpovědní lhůtou 6 měsíců v souladu s § 2312 občanského zákoníku, která počíná běžet prvním dnem kalendářního měsíce následujícího po doručení výpovědi druhé smluvní straně. Má-li strana k výpovědi vážný důvod, činí výpovědní doba 3 měsíce;", bullet=True)
    add_paragraph_styled(doc, "písemnou výpovědí pronajímatele bez výpovědní doby v případě podstatného porušení smlouvy nájemcem (zejména prodlení s platbou nájemného či záloh delší než 30 dnů po splatnosti, neoprávněný podnájem nebo užívání prostoru v rozporu se sjednaným účelem), pokud nájemce nezjedná nápravu ani v přiměřené lhůtě po písemné výzvě.", bullet=True)
    add_paragraph_styled(doc, "3. Vypovídaná strana má právo vznášet písemné námitky proti výpovědi v souladu s § 2314 občanského zákoníku do 1 měsíce od doručení výpovědi.")
    add_paragraph_styled(doc, "4. Smluvní strany se výslovně dohodly na vyloučení aplikace ustanovení § 2315 občanského zákoníku; nájemce nemá při skončení nájmu právo na náhradu za případné převzetí zákaznické základny.")

    add_article_heading(doc, "Čl. 7 – Jistina (kauce)")
    add_paragraph_styled(doc, "1. Nájemce složil při zahájení nájmu na účet pronajímatele peněžitou jistinu ve výši 18 000,- Kč (slovy: osmnáct tisíc korun českých).")
    add_paragraph_styled(doc, "2. Smluvní strany potvrzují, že tato jistina zůstává uložena na účtu pronajímatele po celou dobu trvání nájmu. Pronajímatel je oprávněn jistinu použít k úhradě případných pohledávek za nájemcem vzniklých z titulu neuhrazeného nájemného, záloh, nedoplatků vyúčtování služeb či náhrady škody. Jistina bude vyúčtována a její zůstatek vrácen nájemci do 30 dnů od vyklizení a předání prostoru po skončení nájmu.")

    add_article_heading(doc, "Čl. 8 – Závěrečná ustanovení")
    add_paragraph_styled(doc, "1. Vztahy touto smlouvou výslovně neupravené se řídí příslušnými ustanoveními občanského zákoníku.")
    add_paragraph_styled(doc, "2. Tuto smlouvu lze měnit či doplňovat pouze formou písemných, vzestupně číslovaných dodatků podepsaných oběma smluvními stranami.")
    add_paragraph_styled(doc, "3. Smlouva se vyhotovuje ve dvou stejnopisech s platností originálu, z nichž po jednom obdrží každá smluvní strana.")
    add_paragraph_styled(doc, "4. Smluvní strany prohlašují, že si tuto smlouvu před jejím podpisem řádně přečetly, jejímu obsahu porozuměly a uzavřely ji ze své svobodné a vážné vůle, což stvrzují svými podpisy.")
    add_paragraph_styled(doc, "Příloha č. 1: Výpočtový list měsíčních plateb", bold_prefix=None, space_after=6)

    add_signature_block(doc, "zástupce podílových spoluvlastníků\n(pronajímatel)", "Veronika Brožová",
                             "jednatel DDAANN s.r.o.\n(nájemce)", "Ing. arch. Dan Merta / MgA. Daniel Baudis")
    return doc


# ==============================================================================
# 2. PRŮVODNÍ DOPIS DDAANN s.r.o. (.docx)
# ==============================================================================
def build_docx_ddaann_letter():
    doc = docx.Document()
    style_document(doc)
    
    # Hlavička odesílatele a adresáta
    p_head = doc.add_paragraph()
    r = p_head.add_run("Veronika Brožová\n")
    r.font.bold = True
    r.font.size = Pt(11)
    p_head.add_run("zástupce podílových spoluvlastníků domu Letohradská 367/5 na základě plné moci\n"
                   "Letohradská 367/5, 170 00 Praha 7 – Holešovice\n"
                   "E-mail: nikabrozova@gmail.com\n")
    p_head.paragraph_format.space_after = Pt(12)
    
    p_rec = doc.add_paragraph()
    p_rec.paragraph_format.space_after = Pt(14)
    r_rec = p_rec.add_run("DDAANN s.r.o.\n")
    r_rec.font.bold = True
    p_rec.add_run("k rukám jednatelů: Ing. arch. Dan Merta, MgA. Daniel Baudis\n"
                  "Letohradská 367/5\n"
                  "170 00 Praha 7 – Holešovice\n\n"
                  "V Praze dne 23. října 2026")
    
    add_header_title(doc, "Věc: Návrh nové nájemní smlouvy od 1. 1. 2027 a úprava podmínek nájmu", 
                     "Nebytový prostor č. 367/101 (ateliér 65,0 m²), Letohradská 367/5, Praha 7")
    
    add_paragraph_styled(doc, "Vážení páni jednatelé, vážený pane architekte Merto, vážený pane Baudisi,")
    add_paragraph_styled(doc, "obracím se na Vás jménem všech podílových spoluvlastníků domu Letohradská 367/5, Praha 7, které zastupuji na základě plné moci při správě pronajímaných prostor.")
    add_paragraph_styled(doc, "Velmi si vážíme naší dlouhodobé a bezproblémové spolupráce a vzájemné důvěry. Naším cílem je, aby Vaše působení a užívání prostor ateliéru v našem domě pokračovalo v klidné, stabilní a oboustranně spokojené atmosféře i v dalších letech.")
    add_paragraph_styled(doc, "Vzhledem k tomu, že stávající smluvní dokumentace pochází z roku 2021 a původně sjednaná doba určitá již uplynula, přistoupili jsme v zájmu právní jistoty ke sjednocení a aktualizaci nájemních smluv pro všechny nájemce v domě s jednotnou účinností od 1. ledna 2027.")
    
    add_article_heading(doc, "Hlavní body nové smlouvy:")
    add_paragraph_styled(doc, "Smlouva je uzavřena na dobu neurčitou se standardní zákonnou šestiměsíční výpovědní lhůtou (§ 2312 občanského zákoníku). Poskytuje Vám dlouhodobou stabilitu a dostatečný časový prostor pro jakékoliv plánování.", bold_prefix="• Doba nájmu a výpovědní lhůta: ")
    add_paragraph_styled(doc, "Původní čisté nájemné ve výši 10 000 Kč měsíčně bylo sjednáno v roce 2021 a za posledních téměř 6 let nebylo upravováno, ačkoliv kumulovaná míra inflace za toto období přesáhla 30 % a náklady na správu a provoz domu vzrostly. Nové čisté nájemné navrhujeme ve výši 13 000 Kč měsíčně (zvýšení o 3 000 Kč, tj. cca 200 Kč/m²). Tato částka zůstává na poměry Holešovic a u komerčního prostoru s přímým vstupem z ulice hluboko pod tržní hladinou a vyjadřuje náš zájem na zachování Vašeho ateliéru v domě.", bold_prefix="• Úprava výše nájemného: ")
    add_paragraph_styled(doc, "Do smlouvy je nově zakotvena standardní roční inflační doložka (vázaná na index spotřebitelských cen ČSÚ). Tím se předejde velkým skokovým úpravám v budoucnu – nájemné se bude případně valorizovat plynule jednou ročně, poprvé od roku 2028.", bold_prefix="• Inflační doložka: ")
    add_paragraph_styled(doc, "Měsíční zálohy na služby spojené s užíváním prostor (vodné, osvětlení a úklid spol. prostor) činí dle aktuálního výpočtového listu 876 Kč měsíčně a podléhají ročnímu vyúčtování. Celková měsíční platba činí 13 876 Kč. Z důvodu transparentního účetnictví spoluvlastníků je platba splatná výhradně bezhotovostním převodem na účet č. 2844175379/0800 pod variabilním symbolem 367101 nejpozději do 15. dne v měsíci.", bold_prefix="• Služby a bezhotovostní platba: ")
    add_paragraph_styled(doc, "Odběr elektřiny a plynu zůstává veden přímo na Vaši společnost u dodavatelů PRE a PPAS, což Vám zaručuje plnou kontrolu nad spotřebou.", bold_prefix="• Dodávka energií: ")
    
    add_paragraph_styled(doc, "V příloze tohoto dopisu Vám zasílám návrh nové nájemní smlouvy ve dvou vyhotoveních. Prosím Vás o její prostudování, podpis a zaslání jednoho stejnopisu zpět nejpozději do 30. listopadu 2026. V případě jakýchkoliv dotazů nebo potřeby upřesnění jsem Vám plně k dispozici.")
    add_paragraph_styled(doc, "Předem Vám děkuji za vstřícnost a věcné jednání a těším se na pokračování naší vynikající spolupráce.")
    
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(16)
    p_sign.add_run("S přátelským pozdravem,\n\n\n"
                   ".............................................................\n")
    r_v = p_sign.add_run("Veronika Brožová\n")
    r_v.font.bold = True
    p_sign.add_run("zástupce podílových spoluvlastníků domu Letohradská 367/5")
    return doc


# ==============================================================================
# 3. SMLOUVA Ivo Boschofsky (.docx)
# ==============================================================================
def build_docx_boschofsky_contract():
    doc = docx.Document()
    style_document(doc)
    
    add_header_title(doc, "SMLOUVA O NÁJMU BYTU", 
                     "(bytová jednotka č. 367/1 v domě Letohradská 367/5, Praha 7)")
    
    add_paragraph_styled(doc, "uzavřená podle ustanovení § 2235 a násl. zákona č. 89/2012 Sb., občanský zákoník, v platném znění (dále jen „občanský zákoník“), mezi smluvními stranami:")
    
    add_article_heading(doc, "Smluvní strany:")
    add_co_owners_table(doc, "bytové jednotky č. 367/1")
    
    add_paragraph_styled(doc, "a", bold_prefix=None, space_after=2)
    add_paragraph_styled(doc, "Ivo Boschofsky", bold_prefix="2. Nájemce: Pan ")
    add_paragraph_styled(doc, "Narozen: [Doplnit datum narození / RČ]\n"
                              "IČ: 63439573\n"
                              "Bytem: Letohradská 367/5, Holešovice, 170 00 Praha 7\n"
                              "Číslo bankovního účtu nájemce: [Doplní nájemce]\n"
                              "(dále jen „nájemce“ na straně druhé)")
    
    add_article_heading(doc, "Čl. 1 – Předmět a účel nájmu")
    add_paragraph_styled(doc, "1. Pronajímatel přenechává nájemci do užívání bytovou jednotku č. 367/1 nacházející se v 1. nadzemním podlaží (přízemí) domu čp. 367, Letohradská 5, Praha 7, o celkové podlahové ploše 71,50 m².")
    add_paragraph_styled(doc, "2. Smluvní strany konstatují, že byt sestává z obytných místností, předsíně, WC a umyvadla; v bytě se ke dni podpisu smlouvy nenachází standardní koupelna se sprchou či vanou, což je oběma stranám známo a tato skutečnost je plně zohledněna ve sjednané výši nájemného a ve sníženém směrném čísle roční spotřeby vody pro vyúčtování služeb.")
    add_paragraph_styled(doc, "3. Byt je přenecháván k zajištění bytových a osobních potřeb nájemce.")
    add_paragraph_styled(doc, "4. Společné prostory domu je nájemce oprávněn užívat v rozsahu přiměřeném řádnému užívání bytu.")

    add_article_heading(doc, "Čl. 2 – Stav bytu")
    add_paragraph_styled(doc, "1. Nájemce prohlašuje, že byt dlouhodobě užívá, jeho stavební a technický stav i specifické vybavení jsou mu detailně známy a v tomto stavu jej bez výhrad do nájmu přejímá.")
    add_paragraph_styled(doc, "2. Po skončení nájmu je nájemce povinen předat byt pronajímateli vyklizený a ve stavu odpovídajícím běžnému opotřebení s přihlédnutím ke smluveným a pronajímatelem písemně schváleným úpravám.")

    add_article_heading(doc, "Čl. 3 – Práva a povinnosti smluvních stran")
    add_paragraph_styled(doc, "Nájemce je povinen zejména:", bold_prefix="1. Povinnosti nájemce: ")
    add_paragraph_styled(doc, "užívat byt řádně a s péčí řádného hospodáře, dodržovat noční klid, domovní řád a dobré mravy a nerušit ostatní obyvatele domu;", bullet=True)
    add_paragraph_styled(doc, "provádět běžnou údržbu a drobné opravy v bytě v souladu s nařízením vlády č. 308/2015 Sb., ve znění nařízení vlády č. 493/2025 Sb. (s limitem do 1 500 Kč na jednotlivou opravu a ročním limitem 150 Kč/m² podlahové plochy bytu) na vlastní náklad;", bullet=True)
    add_paragraph_styled(doc, "neprovádět žádné stavební úpravy, zásahy do rozvodů (elektřina, plyn, voda, odpady) ani bourací práce bez předchozího písemného souhlasu pronajímatele;", bullet=True)
    add_paragraph_styled(doc, "písemně nahlásit pronajímateli případné změny v počtu osob užívajících byt pro účely rozúčtování služeb;", bullet=True)
    add_paragraph_styled(doc, "nepřenechat byt ani jeho část do podnájmu třetí osobě bez předchozího písemného souhlasu pronajímatele;", bullet=True)
    add_paragraph_styled(doc, "umožnit pronajímateli po předchozím ohlášení přístup do bytu za účelem kontroly stavu, revizí komínů, elektřiny a plynu nebo odečtů měřidel;", bullet=True)
    add_paragraph_styled(doc, "neodkládat nábytek, materiál ani odpad ve společných prostorách domu (chodby, dvůr, sklepní chodby).", bullet=True)
    
    add_paragraph_styled(doc, "Dodávka elektrické energie (a plynu) do bytu není součástí služeb zajišťovaných pronajímatelem. Nájemce se výslovně zavazuje uzavřít na své vlastní jméno smlouvu o sdružených službách dodávky elektrické energie s příslušným dodavatelem (Pražská energetika, a.s. – PRE) a zajistit přepis elektroměru pro byt č. 367/1 na svou osobu nejpozději do 31. ledna 2027. Pronajímatel poskytne nájemci veškerou nezbytnou součinnost a podklady potřebné k provedení tohoto přepisu. Nájemce hradí spotřebu elektřiny přímo dodavateli. Po ukončení nájmu se nájemce zavazuje převést elektroměr zpět na pronajímatele bez jakýchkoliv nedoplatků.", bold_prefix="2. Povinný převod měřidel elektrické energie (PRE) na nájemce: ")
    add_paragraph_styled(doc, "Pronajímatel je povinen zajistit nájemci nerušený výkon práv spojených s užíváním bytu a dodávku základních služeb spojených s domem (vodné a stočné, úklid a osvětlení společných prostor, odvoz komunálního odpadu).", bold_prefix="3. Povinnosti pronajímatele: ")

    add_article_heading(doc, "Čl. 4 – Nájemné a úhrada za služby")
    add_paragraph_styled(doc, "Nájemné se sjednává dohodou smluvních stran a činí 12 000,- Kč měsíčně (slovy: dvanáct tisíc korun českých).", bold_prefix="1. Výše nájemného: ")
    add_paragraph_styled(doc, "Společně s nájemným se nájemce zavazuje hradit měsíční zálohy na služby (vodné a stočné dle sníženého směrného čísla pro byt bez koupelny, úklid společných prostor, osvětlení domu, svoz odpadu). Výše záloh je stanovena platným Výpočtovým listem a k datu podpisu činí 559,- Kč měsíčně (pro 1 osobu). Zálohy podléhají ročnímu zúčtování v souladu se zákonem č. 67/2013 Sb.", bold_prefix="2. Zálohy na služby: ")
    add_paragraph_styled(doc, "Celková měsíční platba (nájemné + zálohy na služby) ve výši 12 559,- Kč je splatná výhradně bezhotovostním převodem na bankovní účet č. 2844175379/0800, vedený u České spořitelny a.s. Platba je splatná měsíčně dopředu, vždy nejpozději do 15. dne příslušného kalendářního měsíce. Nájemce se zavazuje zřídit u své banky trvalý platební příkaz a jako variabilní symbol uvádět: 3671. Platby v hotovosti nejsou přípustné.", bold_prefix="3. Závazek výhradně bezhotovostní platby na bankovní účet: ")
    add_paragraph_styled(doc, "V případě prodlení s úhradou nájemného nebo záloh na služby se sjednává smluvní pokuta ve výši 0,1 % z dlužné částky za každý den prodlení. V souladu s ustanovením § 2254 odst. 1 občanského zákoníku nesmí peněžitá jistota a právo pronajímatele na zaplacení smluvní pokuty v souhrnu přesáhnout trojnásobek měsíčního nájemného.", bold_prefix="4. Prodlení a smluvní pokuta: ")

    add_article_heading(doc, "Čl. 5 – Inflační doložka")
    add_paragraph_styled(doc, "1. Smluvní strany sjednávají v souladu s § 2248 občanského zákoníku inflační doložku. Pronajímatel je oprávněn jednostranně zvýšit sjednané nájemné jednou ročně o míru inflace vyjádřenou přírůstkem průměrného ročního indexu spotřebitelských cen za uplynulý kalendářní rok, vyhlašovaným Českým statistickým úřadem, a to poprvé od roku 2028.")
    add_paragraph_styled(doc, "2. Zvýšení nájemného je pronajímatel oprávněn uplatnit písemným oznámením zaslaným nájemci (zpravidla k 1. říjnu kalendářního roku), přičemž upravené nájemné je nájemce povinen platit počínaje měsícem následujícím po doručení tohoto oznámení.")

    add_article_heading(doc, "Čl. 6 – Doba nájmu, automatická prolongace a skončení nájmu")
    add_paragraph_styled(doc, "Tato smlouva se uzavírá na dobu určitou v trvání jednoho (1) roku, počínaje dnem 1. 1. 2027 a konče dnem 31. 12. 2027.", bold_prefix="1. Doba nájmu: ")
    add_paragraph_styled(doc, "Neoznámí-li kterákoliv ze smluvních stran písemně druhé smluvní straně nejpozději dva (2) měsíce před uplynutím sjednané doby nájmu (tj. nejpozději do 31. října příslušného kalendářního roku), že trvá na ukončení nájmu nebo že si jeho prodloužení nepřeje, prodlužuje se doba nájmu automaticky o dalších dvanáct (12) měsíců (vždy o jeden kalendářní rok), a to i opakovaně.", bold_prefix="2. Automatická prolongace: ")
    add_paragraph_styled(doc, "K automatickému prodloužení nájmu dle odstavce 2 tohoto článku v žádném případě nedojde a nájem skončí uplynutím doby k 31. prosinci daného roku, pokud:\n"
                              "a) nájemce k 31. říjnu nebo k 31. prosinci příslušného roku eviduje vůči pronajímateli jakýkoliv splatný dluh na nájemném, zálohách na služby či nedoplatku z ročního vyúčtování služeb, nebo\n"
                              "b) nájemce porušuje povinnost hradit platby bezhotovostním převodem na bankovní účet domu dle Čl. 4 odst. 3 této smlouvy, nebo\n"
                              "c) nájemce v průběhu roku závažně nebo opakovaně porušil povinnosti vyplývající z této smlouvy či domovního řádu a byl pronajímatelem písemně vyzván k nápravě, nebo\n"
                              "d) nájemce řádně nepřevedl elektroměr na své jméno u Pražské energetiky, a.s. (PRE) v souladu s Čl. 3 odst. 2 této smlouvy.\n"
                              "Nastane-li některá z výše uvedených skutečností, nájem končí bez dalšího uplynutím sjednané doby a nájemce je povinen byt k 31. prosinci vyklidit a protokolárně předat pronajímateli.", bold_prefix="3. Výhrada neplnění (vyloučení prolongace): ")
    add_paragraph_styled(doc, "Smluvní strany výslovně vylučují aplikaci ustanovení § 2285 občanského zákoníku. Užívá-li nájemce byt i po skončení nájmu, nájemní smlouva se v žádném případě neprodlužuje.", bold_prefix="4. Vyloučení konkludentního prodloužení: ")
    add_paragraph_styled(doc, "Nájem lze před uplynutím sjednané doby ukončit písemnou dohodou, výpovědí nájemce dle § 2287 OZ při podstatné změně okolností (výpovědní doba 3 měsíce), písemnou výpovědí pronajímatele ze zákonných důvodů dle § 2288 odst. 1 OZ (3 měsíce s poučením dle § 2286 odst. 2 OZ), nebo výpovědí bez výpovědní doby pro zvlášť závažné porušení dle § 2291 OZ po předchozí písemné výzvě.", bold_prefix="5. Skončení nájmu v průběhu doby: ")

    add_article_heading(doc, "Čl. 7 – Jistina (kauce)")
    add_paragraph_styled(doc, "1. Nájemce složí na bankovní účet pronajímatele peněžitou jistinu ve výši 10 000,- Kč (slovy: deset tisíc korun českých) nejpozději do 15 dnů od podpisu této smlouvy (případně se započte jistina již složená).")
    add_paragraph_styled(doc, "2. Jistina slouží k zajištění úhrady nájemného, záloh na služby, nedoplatků z vyúčtování služeb a případné náhrady škody. Jistina bude nájemci vyúčtována a vrácena do 15 dnů po protokolárním vyklizení a předání bytu při skončení nájmu, spolu se zákonným úrokem v souladu s § 2254 odst. 2 občanského zákoníku. Pronajímatel je oprávněn si před vrácením jistiny započíst veškeré splatné pohledávky z nájmu.")

    add_article_heading(doc, "Čl. 8 – Závěrečná ustanovení")
    add_paragraph_styled(doc, "1. Práva a povinnosti stran neupravené touto smlouvou se řídí občanským zákoníkem.")
    add_paragraph_styled(doc, "2. Změny a doplňky této smlouvy jsou platné pouze v písemné formě jako vzestupně číslované dodatky.")
    add_paragraph_styled(doc, "3. Smlouva je vyhotovena ve dvou stejnopisech s platností originálu, z nichž každá smluvní strana obdrží po jednom vyhotovení.")
    add_paragraph_styled(doc, "4. Smluvní strany prohlašují, že si smlouvu přečetly, s jejím obsahem souhlasí a na důkaz toho připojují své podpisy.")
    add_paragraph_styled(doc, "Příloha č. 1: Výpočtový list nájemného a záloh na služby", bold_prefix=None, space_after=6)

    add_signature_block(doc, "zástupce podílových spoluvlastníků\n(pronajímatel)", "Veronika Brožová",
                             "nájemce", "Ivo Boschofsky")
    return doc


# ==============================================================================
# 4. PRŮVODNÍ DOPIS Ivo Boschofsky (.docx) - NEFORMÁLNÍ, TYKÁNÍ, PŘÁTELSKÝ
# ==============================================================================
def build_docx_boschofsky_letter():
    doc = docx.Document()
    style_document(doc)
    
    # Hlavička
    p_head = doc.add_paragraph()
    r = p_head.add_run("Veronika Brožová\n")
    r.font.bold = True
    p_head.add_run("Letohradská 367/5, 170 00 Praha 7\n"
                   "E-mail: nikabrozova@gmail.com\n\n"
                   "V Praze dne 23. října 2026\n")
    p_head.paragraph_format.space_after = Pt(10)
    
    p_rec = doc.add_paragraph()
    p_rec.paragraph_format.space_after = Pt(14)
    r_rec = p_rec.add_run("Ivo Boschofsky\n")
    r_rec.font.bold = True
    p_rec.add_run("Byt č. 367/1, Letohradská 367/5\n170 00 Praha 7")
    
    add_header_title(doc, "Nová nájemní smlouva od 1. 1. 2027 a pár důležitých věcí k bytu", None)
    
    add_paragraph_styled(doc, "Ahoj Ivo,")
    add_paragraph_styled(doc, "obracím se na tebe ohledně tvého bytu v přízemí (č. 367/1). Známe se v baráku už roky a víš, že si zakládám na tom, abychom spolu vždycky vycházeli férově, lidsky a v sousedské pohodě. Právě proto ti píšu napřímo a bez zbytečných právnických kliček, abychom si v klidu řekli, co a proč potřebujeme od nového roku nastavit.")
    add_paragraph_styled(doc, "Jak víš, dům má 32 podílových spoluvlastníků, za které mám plnou moc a zodpovídám jim za řádnou správu. Před úřady i před majiteli musíme mít veškeré smlouvy v pořádku a aktuální. Staré smlouvy už formálně neodpovídají zákonům, a proto teď připravujeme novou smlouvu pro všechny nájemce v domě s platností od 1. ledna 2027.")
    
    add_article_heading(doc, "Co je potřeba upravit a na čem se domluvit:")
    
    add_paragraph_styled(doc, "Tohle je pro mě úplně zásadní věc. Hromadí se mi tu hotovost, pak s těmi penězi musím běhat do banky a vkládat je na účet, musím tě pořád hlídat a upomínat. Navíc účetní z plateb v hotovosti šílí a spoluvlastníci potřebují mít ve výpisech z účtu naprosto čisté, doložitelné a transparentní položky kvůli ročnímu zúčtování a daním. Když si v bance nastavíš trvalej příkaz na účet domu: 2844175379/0800, variabilní symbol 3671, se splatností vždy k 15. dni v měsíci, bude to pro nás pro všechny mnohem jednodušší a ušetří to čas i starosti. Od 1. ledna už proto v hotovosti platby přebírat nebudu.", bold_prefix="1. Konec hotovosti a trvalý příkaz na účet: ")
    
    add_paragraph_styled(doc, "Do konce ledna 2027 je potřeba formálně přepsat elektroměr na tebe přímo u Pražské energetiky (PRE), abys měl spotřebu elektřiny plně ve svých rukách. Nemusíš se bát žádného složitého běhání – já ti připravím veškeré formuláře i plné moci, ty to jen podepíšeš a buď to u PRE vyřídím já, nebo tam skočíme společně. Je to jen administrativní formalita, ale musí být hotová.", bold_prefix="2. Přepis elektřiny u PRE na tvoje jméno: ")
    
    add_paragraph_styled(doc, "Doteď platíš čistý nájem 10 000 Kč měsíčně. Všichni vidíme, jak za poslední roky strašně vyrostly všechny ceny okolo, pojištění domu i náklady na řemeslníky a údržbu. Proto nájem od 1. ledna zvedáme o 2 000 Kč na 12 000 Kč měsíčně. K tomu jsou zálohy na služby domu (voda, popelnice, úklid a světlo na chodbě) ve výši 559 Kč měsíčně – máš tam samozřejmě zohledněné snížené vodné, protože v bytě není klasická koupelna. Celková měsíční platba na účet tedy bude 12 559 Kč. Určitě sám uznáš, že 12 tisíc za 71,5 m² na Letné je i po tomto zvýšení naprosto symbolická a kamarádská cena, která plně bere ohled na specifika tvého bytu.", bold_prefix="3. Úprava nájmu o 2 000 Kč: ")
    
    add_paragraph_styled(doc, "Abychom se nemuseli každý rok zdržovat sepisováním nových papírů a dodatků, dali jsme do smlouvy automatické prodlužování. Smlouva se uzavírá na 1 rok (do 31. 12. 2027), ale pokud je všechno v pořádku – tj. nájem řádně a včas chodí na účet a je přepsaná elektřina – smlouva se sama automaticky prodlužuje o další rok. Nemusíme na ni dál sahat a můžeš v klidu bydlet.", bold_prefix="4. Žádné zbytečné papírování – smlouva na rok s automatickým prodloužením: ")
    
    add_paragraph_styled(doc, "V příloze ti dávám novou smlouvu ve dvou vyhotoveních. V klidu si ji pročti, jedno vyhotovení podepiš a hoď mi ho do schránky (nebo mi ho předej osobně). Kdyby ti v textu cokoliv nebylo jasné nebo ses chtěl na cokoliv zeptat, stav se u mě, dáme kafe a všechno si v pohodě řekneme.")
    add_paragraph_styled(doc, "Díky moc za pochopení a spolupráci, vážím si toho!")
    
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(16)
    p_sign.add_run("Měj se fajn,\n\n\n"
                   ".............................................................\n")
    r_v = p_sign.add_run("Veronika Brožová\n")
    r_v.font.bold = True
    p_sign.add_run("Letohradská 367/5")
    return doc


# ==============================================================================
# 5. SMLOUVA Tetsu Onari (.docx)
# ==============================================================================
def build_docx_onari_contract():
    doc = docx.Document()
    style_document(doc)
    
    add_header_title(doc, "SMLOUVA O NÁJMU BYTU", 
                     "(bytová jednotka č. 367/3 v domě Letohradská 367/5, Praha 7)")
    
    add_paragraph_styled(doc, "uzavřená podle ustanovení § 2235 a násl. zákona č. 89/2012 Sb., občanský zákoník, v platném znění (dále jen „občanský zákoník“), mezi smluvními stranami:")
    
    add_article_heading(doc, "Smluvní strany:")
    add_co_owners_table(doc, "bytové jednotky č. 367/3")
    
    add_paragraph_styled(doc, "a", bold_prefix=None, space_after=2)
    add_paragraph_styled(doc, "Tetsu Onari", bold_prefix="2. Nájemce: Pan ")
    add_paragraph_styled(doc, "Narozen: 30. 6. 1980\n"
                              "Státní příslušnost: Japonsko\n"
                              "Číslo cestovního pasu / dokladu pobytu: TG 2453612\n"
                              "Bytem v ČR: Letohradská 367/5, Holešovice, 170 00 Praha 7\n"
                              "(Trvalé bydliště: 2-29-8 kuboyama-ch Hachioji-city Tokyo 192-0023, Japan)\n"
                              "Číslo bankovního účtu nájemce: [Doplní nájemce]\n"
                              "(dále jen „nájemce“ na straně druhé)")
    
    add_article_heading(doc, "Čl. 1 – Předmět a účel nájmu")
    add_paragraph_styled(doc, "1. Pronajímatel přenechává nájemci do užívání bytovou jednotku č. 367/3 nacházející se v 1. nadzemním podlaží (přízemí) domu čp. 367, Letohradská 5, Praha 7, o celkové podlahové ploše 50,40 m².")
    add_paragraph_styled(doc, "2. Byt sestává z obytného pokoje, kuchyně, předsíně a sociálního zařízení (koupelna a WC).")
    add_paragraph_styled(doc, "3. Byt je pronajímán k zajištění bytových potřeb nájemce a členů jeho společné domácnosti. Nájemce je oprávněn část bytu přiměřeně využívat též ke své tvůrčí umělecké činnosti za předpokladu, že tato činnost nezpůsobí zvýšené zatížení domu, hluk ani neruší ostatní obyvatele domu.")
    add_paragraph_styled(doc, "4. Společné prostory domu je nájemce oprávněn užívat v rozsahu obvyklém a přiměřeném řádnému užívání bytu.")

    add_article_heading(doc, "Čl. 2 – Stav bytu")
    add_paragraph_styled(doc, "1. Nájemce prohlašuje, že byt dlouhodobě užívá, jeho stavební a technický stav je mu detailně znám a v tomto stavu jej bez výhrad do nájmu přejímá.")
    add_paragraph_styled(doc, "2. Po skončení nájmu je nájemce povinen předat byt pronajímateli vyklizený a ve stavu odpovídajícím běžnému opotřebení s přihlédnutím k provedeným a pronajímatelem schváleným opravám.")

    add_article_heading(doc, "Čl. 3 – Práva a povinnosti smluvních stran")
    add_paragraph_styled(doc, "Nájemce je povinen zejména:", bold_prefix="1. Povinnosti nájemce: ")
    add_paragraph_styled(doc, "užívat byt řádně a v souladu s dobrými mravy, dodržovat domovní řád a nerušit ostatní uživatele bytů v domě;", bullet=True)
    add_paragraph_styled(doc, "hradit běžnou údržbu a drobné opravy v bytě v souladu s nařízením vlády č. 308/2015 Sb., ve znění nařízení vlády č. 493/2025 Sb. (s limitem do 1 500 Kč na jednotlivou opravu a ročním limitem 150 Kč/m² podlahové plochy bytu);", bullet=True)
    add_paragraph_styled(doc, "neprovádět žádné stavební úpravy ani podstatné změny v bytě bez předchozího písemného souhlasu pronajímatele;", bullet=True)
    add_paragraph_styled(doc, "písemně oznámit pronajímateli změnu v počtu osob žijících v bytě nejpozději do 2 měsíců od okamžiku, kdy změna nastala (pro správné stanovení záloh na služby);", bullet=True)
    add_paragraph_styled(doc, "nepřenechat byt ani jeho část do podnájmu třetí osobě bez předchozího písemného souhlasu pronajímatele;", bullet=True)
    add_paragraph_styled(doc, "umožnit pronajímateli po předchozím oznámení přístup do bytu za účelem kontroly technického stavu, provádění odečtů měřidel nebo zákonných revizí;", bullet=True)
    add_paragraph_styled(doc, "neodkládat věci a neskladovat materiál ve společných prostorách domu (chodby, dvůr, sklepní chodby).", bullet=True)
    
    add_paragraph_styled(doc, "Dodávka elektřiny a plynu není zahrnuta v zálohách na služby poskytované pronajímatelem. Nájemce hradí spotřebu elektřiny a plynu přímo dodavatelům na základě smluv vedených na své jméno dle samostatných podružných či fakturačních měřidel. Pronajímatel poskytne veškerou nezbytnou součinnost k vedení/přepisu těchto smluv.", bold_prefix="2. Převod energií (elektřina a plyn): ")
    add_paragraph_styled(doc, "Pronajímatel je povinen udržovat dům a jeho společné části ve stavu způsobilém k řádnému užívání a zajistit nájemci plný a nerušený výkon práv spojených s nájmem bytu.", bold_prefix="3. Povinnosti pronajímatele: ")

    add_article_heading(doc, "Čl. 4 – Nájemné a úhrada za plnění spojená s užíváním bytu (služby)")
    add_paragraph_styled(doc, "Nájemné se sjednává dohodou smluvních stran a činí 8 000,- Kč měsíčně (slovy: osm tisíc korun českých).", bold_prefix="1. Výše nájemného: ")
    add_paragraph_styled(doc, "Společně s nájemným se nájemce zavazuje hradit měsíční zálohy na nezbytné služby (vodné a stočné, úklid společných prostor, osvětlení společných prostor, odvoz komunálního odpadu). Výše záloh je stanovena platným Výpočtovým listem a k datu podpisu činí 2 150,- Kč měsíčně (pro hlášený počet osob v bytě). Zálohy podléhají ročnímu vyúčtování vždy do 30. dubna následujícího roku v souladu se zákonem č. 67/2013 Sb.", bold_prefix="2. Zálohy na služby: ")
    add_paragraph_styled(doc, "Celková měsíční platba (nájemné + zálohy na služby) ve výši 10 150,- Kč je splatná výhradně bezhotovostním převodem na bankovní účet č. 2844175379/0800, vedený u České spořitelny a.s. Platba je splatná měsíčně dopředu, nejpozději do 15. dne příslušného kalendářního měsíce. Variabilní symbol platby: 3673. Platby v hotovosti nejsou přípustné.", bold_prefix="3. Závazek výhradně bezhotovostní platby na bankovní účet: ")
    add_paragraph_styled(doc, "V případě prodlení s úhradou nájemného nebo záloh na služby se sjednává smluvní pokuta ve výši 0,1 % z dlužné částky za každý den prodlení. V souladu s ustanovením § 2254 odst. 1 občanského zákoníku nesmí peněžitá jistota a právo pronajímatele na zaplacení smluvní pokuty v souhrnu přesáhnout trojnásobek měsíčního nájemného.", bold_prefix="4. Prodlení a smluvní pokuta: ")

    add_article_heading(doc, "Čl. 5 – Inflační doložka")
    add_paragraph_styled(doc, "1. Smluvní strany sjednávají v souladu s § 2248 občanského zákoníku inflační doložku. Pronajímatel je oprávněn jednostranně zvýšit sjednané nájemné jednou ročně o míru inflace vyjádřenou přírůstkem průměrného ročního indexu spotřebitelských cen za uplynulý kalendářní rok, vyhlašovaným Českým statistickým úřadem, a to poprvé od roku 2028.")
    add_paragraph_styled(doc, "2. Zvýšení nájemného je pronajímatel oprávněn uplatnit písemným oznámením zaslaným nájemci, přičemž upravené nájemné je nájemce povinen platit počínaje měsícem následujícím po doručení tohoto oznámení (zpravidla k 1. říjnu kalendářního roku).")

    add_article_heading(doc, "Čl. 6 – Doba nájmu, automatická prolongace a skončení nájmu")
    add_paragraph_styled(doc, "Tato smlouva se uzavírá na dobu určitou v trvání jednoho (1) roku, počínaje dnem 1. 1. 2027 a konče dnem 31. 12. 2027.", bold_prefix="1. Doba nájmu: ")
    add_paragraph_styled(doc, "Neoznámí-li kterákoliv ze smluvních stran písemně druhé smluvní straně nejpozději dva (2) měsíce před uplynutím sjednané doby nájmu (tj. nejpozději do 31. října příslušného kalendářního roku), že trvá na ukončení nájmu nebo že si jeho prodloužení nepřeje, prodlužuje se doba nájmu automaticky o dalších dvanáct (12) měsíců (vždy o jeden kalendářní rok), a to i opakovaně.", bold_prefix="2. Automatická prolongace: ")
    add_paragraph_styled(doc, "K automatickému prodloužení nájmu dle odstavce 2 tohoto článku v žádném případě nedojde a nájem skončí uplynutím doby k 31. prosinci daného roku, pokud:\n"
                              "a) nájemce k 31. říjnu nebo k 31. prosinci příslušného roku eviduje vůči pronajímateli jakýkoliv splatný dluh na nájemném, zálohách na služby či nedoplatku z ročního vyúčtování služeb, nebo\n"
                              "b) nájemce v průběhu roku závažně nebo opakovaně porušil povinnosti vyplývající z této smlouvy či domovního řádu a byl pronajímatelem písemně vyzván k nápravě, nebo\n"
                              "c) nájemce řádně nepřevedl měřidla energií na své jméno v souladu s Čl. 3 odst. 2 této smlouvy.\n"
                              "Nastane-li některá z výše uvedených skutečností, nájem končí bez dalšího uplynutím sjednané doby a nájemce je povinen byt k 31. prosinci vyklidit a protokolárně předat pronajímateli.", bold_prefix="3. Výhrada neplnění (vyloučení prolongace): ")
    add_paragraph_styled(doc, "Smluvní strany výslovně vylučují aplikaci ustanovení § 2285 občanského zákoníku. Užívá-li nájemce byt i po skončení nájmu, nájemní smlouva se v žádném případě neprodlužuje.", bold_prefix="4. Vyloučení konkludentního prodloužení: ")
    add_paragraph_styled(doc, "Nájem lze před uplynutím doby skončit písemnou dohodou, výpovědí nájemce dle § 2287 OZ při závažné změně okolností (výpovědní doba 3 měsíce), písemnou výpovědí pronajímatele ze zákonných důvodů dle § 2288 odst. 1 OZ (3 měsíce s poučením dle § 2286 odst. 2 OZ), nebo výpovědí bez výpovědní doby pro zvlášť závažné porušení dle § 2291 OZ po předchozí písemné výzvě.", bold_prefix="5. Skončení nájmu v průběhu doby: ")

    add_article_heading(doc, "Čl. 7 – Jistina (kauce)")
    add_paragraph_styled(doc, "1. Nájemce složil na účet pronajímatele peněžitou jistinu ve výši 10 000,- Kč (slovy: deset tisíc korun českých).")
    add_paragraph_styled(doc, "2. Jistina slouží k zajištění úhrady nájemného, záloh na služby, nedoplatků z vyúčtování služeb a případné náhrady škody. Jistina bude nájemci vyúčtována a vrácena do 15 dnů po protokolárním vyklizení a předání bytu při skončení nájmu, spolu se zákonným úrokem v souladu s § 2254 odst. 2 občanského zákoníku. Pronajímatel je oprávněn si před vrácením jistiny započíst veškeré splatné pohledávky z nájmu.")

    add_article_heading(doc, "Čl. 8 – Závěrečná ustanovení")
    add_paragraph_styled(doc, "1. Práva a povinnosti stran neupravené touto smlouvou se řídí občanským zákoníkem.")
    add_paragraph_styled(doc, "2. Změny a doplňky této smlouvy jsou platné pouze v písemné formě jako vzestupně číslované dodatky.")
    add_paragraph_styled(doc, "3. Smlouva je vyhotovena ve dvou stejnopisech s platností originálu, z nichž každá smluvní strana obdrží po jednom vyhotovení.")
    add_paragraph_styled(doc, "4. Smluvní strany prohlašují, že si smlouvu přečetly, s jejím obsahem souhlasí a na důkaz toho připojují své podpisy.")
    add_paragraph_styled(doc, "Příloha č. 1: Výpočtový list nájemného a záloh na služby", bold_prefix=None, space_after=6)

    add_signature_block(doc, "zástupce podílových spoluvlastníků\n(pronajímatel)", "Veronika Brožová",
                             "nájemce", "Tetsu Onari")
    return doc


# ==============================================================================
# 6. PRŮVODNÍ DOPIS Tetsu Onari (.docx) - NEFORMÁLNÍ, TYKÁNÍ, PŘÁTELSKÝ
# ==============================================================================
def build_docx_onari_letter():
    doc = docx.Document()
    style_document(doc)
    
    # Hlavička
    p_head = doc.add_paragraph()
    r = p_head.add_run("Veronika Brožová\n")
    r.font.bold = True
    p_head.add_run("Letohradská 367/5, 170 00 Praha 7\n"
                   "E-mail: nikabrozova@gmail.com\n\n"
                   "V Praze dne 23. října 2026\n")
    p_head.paragraph_format.space_after = Pt(10)
    
    p_rec = doc.add_paragraph()
    p_rec.paragraph_format.space_after = Pt(14)
    r_rec = p_rec.add_run("Tetsu Onari\n")
    r_rec.font.bold = True
    p_rec.add_run("Byt č. 367/3, Letohradská 367/5\n170 00 Praha 7")
    
    add_header_title(doc, "Nová nájemní smlouva od 1. 1. 2027 a úprava podmínek nájmu", None)
    
    add_paragraph_styled(doc, "Ahoj Tetsu,")
    add_paragraph_styled(doc, "obracím se na tebe ohledně tvého bytu č. 367/3 v přízemí domu Letohradská 5. Jak víš, dům má 32 podílových spoluvlastníků a já pro ně pronajímané byty spravuji na základě udělené plné moci. Od 1. ledna 2027 přistupujeme ke sjednocení a aktualizaci všech nájemních smluv v domě tak, aby odpovídaly platným zákonům i ekonomické realitě.")
    
    add_article_heading(doc, "Důvody nové smlouvy a úpravy nájemného:")
    
    add_paragraph_styled(doc, "Tvoje stávající nájemní smlouva byla uzavřena v roce 2014 s čistým nájemným 5 700 Kč měsíčně. Za celých dlouhých 12 let se nájemné vůbec nezměnilo. Držet dál po 12 letech takto nízký nájem je z pohledu správy domu i všech 32 spoluvlastníků naprosto neudržitelné. Veškeré náklady na provoz domu, údržbu, opravy, pojištění i služby za tu dobu zásadně vzrostly a kumulovaná inflace v ČR byla enormní.", bold_prefix="1. Dvanáct let takto nízkého nájemného je již neudržitelných: ")
    
    add_paragraph_styled(doc, "Čisté nájemné se od 1. 1. 2027 upravuje na 8 000 Kč měsíčně. K tomu jsou měsíční zálohy na služby spojené s užíváním bytu (vodné a stočné, odvoz odpadu, osvětlení a úklid společných prostor pro nahlášený počet osob v rodině) ve výši 2 150 Kč měsíčně. Celková měsíční platba činí 10 150 Kč. I po této úpravě zůstává částka 8 000 Kč za byt o ploše 50,4 m² na Letné hluboko pod běžnou tržní hladinou.", bold_prefix="2. Nová výše nájemného na 8 000 Kč měsíčně: ")
    
    add_paragraph_styled(doc, "Smlouva se uzavírá na dobu určitou 1 rok (do 31. 12. 2027) s mechanismem automatického prodlužování o dalších 12 měsíců. Pokud je nájem řádně a včas hrazen na bankovní účet domu a plněny povinnosti, smlouva se automaticky prodlužuje bez nutnosti každoročního sepisování nových dodatků.", bold_prefix="3. Smlouva na 1 rok s automatickým prodlužováním: ")
    
    add_paragraph_styled(doc, "Do smlouvy je vložena standardní inflační doložka vázaná na oficiální index Českého statistického úřadu, která se poprvé může uplatnit od roku 2028. Tím se předejde tomu, aby se nájemné po dalších letech muselo upravovat skokově.", bold_prefix="4. Inflační doložka od roku 2028: ")
    
    add_paragraph_styled(doc, "Celková platba 10 150 Kč měsíčně je splatná výhradně bezhotovostním převodem (trvalým příkazem) na účet domu: 2844175379/0800, variabilní symbol 3673, se splatností vždy nejpozději do 15. dne v měsíci.", bold_prefix="5. Platby bezhotovostně na účet: ")
    
    add_paragraph_styled(doc, "V příloze ti předávám návrh nové nájemní smlouvy ve dvou vyhotoveních. V klidu si ji prosím projdi, jedno vyhotovení podepiš a vrať mi ho do konce listopadu 2026. Kdyby ses chtěl na cokoliv zeptat, stav se u mě doma v bytě č. 5 nebo mi napiš.")
    add_paragraph_styled(doc, "Díky za pochopení.")
    
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(16)
    p_sign.add_run("Měj se hezky,\n\n\n"
                   ".............................................................\n")
    r_v = p_sign.add_run("Veronika Brožová\n")
    r_v.font.bold = True
    p_sign.add_run("Letohradská 367/5")
    return doc


# ==============================================================================
# 7. MARKDOWN BUILDERS
# ==============================================================================
def get_co_owners_md(unit_label):
    lines = [f"**1. Podíloví spoluvlastníci {unit_label}:**"]
    for name, addr in CO_OWNERS:
        lines.append(f"* {name}, bytem {addr}")
    lines.append("\nNa základě udělené plné moci spoluvlastníky zastupuje správce nemovitosti:  ")
    lines.append("**Veronika Brožová**, bytem Letohradská 367/5, Holešovice, 170 00 Praha 7.  ")
    lines.append("Prostředky spojené se správou a užíváním prostoru spravuje na svém účtu:  ")
    lines.append("**Společenství vlastníků Letohradská 367, Praha 7**, se sídlem Letohradská 5/367, 170 00 Praha 7, IČ: 24239178, č. ú. **2844175379/0800**, vedený u České spořitelny a.s.  ")
    lines.append("*(dále jen „pronajímatel“ na straně jedné)*\n")
    return "\n".join(lines)


def build_md_ddaann_contract():
    return f"""# SMLOUVA O NÁJMU PROSTORU SLOUŽÍCÍHO PODNIKÁNÍ
(nebytový prostor č. 367/101 v domě Letohradská 367/5, Praha 7)

uzavřená níže uvedeného dne, měsíce a roku podle ustanovení § 2302 a násl. zákona č. 89/2012 Sb., občanský zákoník, v platném znění (dále jen „občanský zákoník“), mezi smluvními stranami:

---

### Smluvní strany:

{get_co_owners_md("nebytové jednotky č. 367/101")}
a

**2. Nájemce:**  
**DDAANN s.r.o.**  
se sídlem Letohradská 367/5, Holešovice, 170 00 Praha 7  
IČ: 14042967  
DIČ: CZ14042967  
Zapsaná v obchodním rejstříku vedeném Městským soudem v Praze, oddíl C, vložka 359424  
Zastoupená jednateli: Ing. arch. Danem Mertou / MgA. Danielem Baudisem  
Číslo bankovního účtu nájemce: [Doplní nájemce]  
*(dále jen „nájemce“ na straně druhé)*

---

### Čl. 1 – Předmět a účel nájmu
1. Předmětem nájmu je nebytový prostor č. **367/101** nacházející se v 1. nadzemním podlaží (přízemí) domu čp. 367, Letohradská 5, Praha 7, o celkové výměře **65,0 m²**. Jde o prostor s vlastním vchodem přímo z Letohradské ulice, situovaný vlevo od hlavního vstupu do domu. Sociální zařízení je přístupné ze společné chodby.
2. Předmět nájmu je pronajímán jako prostor sloužící podnikání za účelem provozování architektonické, projekční, designérské a kancelářské činnosti nájemce v souladu s předmětem jeho podnikání zapsaným v obchodním rejstříku.
3. Společné prostory domu je nájemce oprávněn užívat v rozsahu přiměřeném řádnému užívání předmětu nájmu.
4. Změna sjednaného účelu užívání je možná pouze s předchozím písemným souhlasem pronajímatele.

---

### Čl. 2 – Stav předmětu nájmu
1. Nájemce prohlašuje, že je mu stav předmětu nájmu z titulu jeho dosavadního dlouhodobého užívání detailně znám, seznámil se s jeho technickým i stavebním stavem a v tomto stavu jej bez výhrad do nájmu přejímá.
2. Po skončení nájmu je nájemce povinen předat předmět nájmu pronajímateli ve stavu, v jakém jej převzal, s přihlédnutím k běžnému opotřebení a odsouhlaseným stavebním úpravám. Předání se uskuteční na základě oboustranně podepsaného předávacího protokolu.

---

### Čl. 3 – Práva a povinnosti smluvních stran
1. **Nájemce je povinen zejména:**
   * a) Užívat předmět nájmu výhradně k dohodnutému účelu a pečovat o něj s péčí řádného hospodáře.
   * b) Neprovádět žádné stavební úpravy ani zásahy do dispozice, rozvodů a konstrukcí bez předchozího písemného souhlasu pronajímatele.
   * c) Bez zbytečného odkladu oznámit pronajímateli potřebu nezbytných oprav jdoucích k tíži pronajímatele a umožnit jejich provedení.
   * d) Běžnou údržbu a drobné opravy v předmětu nájmu provádět na vlastní náklad.
   * e) Předcházet vzniku škod a pojistit svou činnost i majetek v předmětu nájmu proti případným škodám způsobeným třetím osobám.
   * f) Neumožnit užívání předmětu nájmu ani jeho části třetím osobám (podnájem) bez předchozího písemného souhlasu pronajímatele.
   * g) Bez předchozího písemného souhlasu pronajímatele neumisťovat na fasádu domu, společné chodby či okna reklamní tabule nebo zařízení přesahující obvyklé označení sídla/provozovny. Po ukončení nájmu je povinen zrušit sídlo společnosti na této adrese.
   * h) Umožnit pronajímateli přístup do předmětu nájmu za účelem kontroly stavu a způsobu užívání, provádění odečtů a revizí, a to po předchozím včasném oznámení pronajímatelem. V případě havárie nebo bezprostředního nebezpečí je přístup možný ihned.
2. **Dodávka energií (elektřina a plyn):**
   * Dodávka elektrické energie a plynu není součástí služeb poskytovaných pronajímatelem. Odběrné místo elektřiny a plynu pro prostor č. 367/101 je/bude vedeno na základě smluv o sdružených službách dodávky uzavřených přímo mezi nájemcem a příslušnými dodavateli (PRE, PPAS) na účet a jméno nájemce.
   * Po ukončení nájmu se nájemce zavazuje poskytnout veškerou součinnost k převodu odběrných míst zpět na pronajímatele bez jakýchkoliv nedoplatků.
3. **Pronajímatel je povinen:**
   * Zajistit nájemci nerušený výkon práv spojených s užíváním předmětu nájmu a zajistit dodávku služeb spojených s užíváním domu (vodné a stočné, osvětlení a úklid společných prostor, odvoz odpadu).

---

### Čl. 4 – Nájemné a úhrada za služby
1. **Výše nájemného:** Nájemné se sjednává dohodou smluvních stran a činí **13 000,- Kč měsíčně** (slovy: třináct tisíc korun českých).
2. **Zálohy na služby:** Společně s nájemným se nájemce zavazuje hradit měsíční zálohy na služby poskytované v souvislosti s užíváním prostoru (vodné a stočné, úklid a osvětlení společných prostor). Výše záloh je stanovena platným Výpočtovým listem a k datu podpisu smlouvy činí **876,- Kč měsíčně**. Pronajímatel je oprávněn výši záloh upravit v návaznosti na změny cen dodavatelů služeb nebo změnu počtu osob. Zálohy podléhají ročnímu vyúčtování.
3. **Závazek bezhotovostní platby na účet:**
   * Celková měsíční platba (nájemné + zálohy na služby) ve výši **13 876,- Kč** je splatná **výhradně bezhotovostním převodem na bankovní účet č. 2844175379/0800**, vedený u České spořitelny a.s.
   * Platba je splatná měsíčně dopředu, **vždy nejpozději do 15. dne příslušného kalendářního měsíce**, za který se hradí.
   * Jako variabilní symbol je nájemce povinen uvádět: **367101**. Platby v hotovosti nejsou přípustné.
4. **Prodlení a smluvní pokuta:** V případě prodlení s úhradou nájemného nebo záloh na služby se sjednává smluvní pokuta ve výši 0,1 % z dlužné částky za každý den prodlení. Přesáhne-li prodlení 30 kalendářních dnů, je pronajímatel oprávněn smlouvu jednostranně vypovědět.

---

### Čl. 5 – Inflační doložka
1. Smluvní strany se dohodly, že pronajímatel je oprávněn jednostranně zvýšit nájemné jednou ročně o míru inflace vyjádřenou přírůstkem průměrného ročního indexu spotřebitelských cen, vyhlašovaným Českým statistickým úřadem za předchozí kalendářní rok, a to poprvé od roku 2028.
2. Překročí-li míra inflace 3 %, je pronajímatel oprávněn upravit nájemné k 1. říjnu kalendářního roku (nebo od měsíce následujícího po doručení písemného oznámení pronajímatele o zvýšení nájemného).

---

### Čl. 6 – Doba nájmu a skončení nájmu
1. Tato smlouva se uzavírá na **dobu neurčitou** s účinností ode dne **1. 1. 2027**.
2. Nájemní vztah může zaniknout:
   * a) Písemnou dohodou smluvních stran.
   * b) Písemnou výpovědí kterékoliv ze smluvních stran bez uvedení důvodu s **výpovědní lhůtou 6 měsíců** v souladu s § 2312 občanského zákoníku, která počíná běžet prvním dnem kalendářního měsíce následujícího po doručení výpovědi druhé smluvní straně. Má-li strana k výpovědi vážný důvod, činí výpovědní doba 3 měsíce.
   * c) Písemnou výpovědí pronajímatele bez výpovědní doby v případě podstatného porušení smlouvy nájemcem (zejména prodlení s platbou nájemného či záloh delší než 30 dnů po splatnosti, neoprávněný podnájem nebo užívání prostoru v rozporu se sjednaným účelem), pokud nájemce nezjedná nápravu ani v přiměřené lhůtě po písemné výzvě.
3. Vypovídaná strana má právo vznášet písemné námitky proti výpovědi v souladu s § 2314 občanského zákoníku do 1 měsíce od doručení výpovědi.
4. Smluvní strany se výslovně dohodly na **vyloučení aplikace ustanovení § 2315 občanského zákoníku**; nájemce nemá při skončení nájmu právo na náhradu za případné převzetí zákaznické základny.

---

### Čl. 7 – Jistina (kauce)
1. Nájemce složil při zahájení nájmu na účet pronajímatele peněžitou jistinu ve výši **18 000,- Kč** (slovy: osmnáct tisíc korun českých).
2. Smluvní strany potvrzují, že tato jistina zůstává uložena na účtu pronajímatele po celou dobu trvání nájmu. Pronajímatel je oprávněn jistinu použít k úhradě případných pohledávek za nájemcem vzniklých z titulu neuhrazeného nájemného, záloh, nedoplatků vyúčtování služeb či náhrady škody. Jistina bude vyúčtována a její zůstatek vrácen nájemci do 30 dnů od vyklizení a předání prostoru po skončení nájmu.

---

### Čl. 8 – Závěrečná ustanovení
1. Vztahy touto smlouvou výslovně neupravené se řídí příslušnými ustanoveními občanského zákoníku.
2. Tuto smlouvu lze měnit či doplňovat pouze formou písemných, vzestupně číslovaných dodatků podepsaných oběma smluvními stranami.
3. Smlouva se vyhotovuje ve dvou stejnopisech s platností originálu, z nichž po jednom obdrží každá smluvní strana.
4. Smluvní strany prohlašují, že si tuto smlouvu před jejím podpisem řádně přečetly, jejímu obsahu porozuměly a uzavřely ji ze své svobodné a vážné vůle, což stvrzují svými podpisy.

Příloha č. 1: Výpočtový list měsíčních plateb

V Praze dne .............................. 2026



....................................................................                    ....................................................................  
**Veronika Brožová**                                                **DDAANN s.r.o.**  
v zastoupení podílových spoluvlastníků                                    Ing. arch. Dan Merta / MgA. Daniel Baudis  
*(pronajímatel)*                                                          *(nájemce)*
"""

def build_md_ddaann_letter():
    return """# Průvodní dopis k návrhu nové nájemní smlouvy

**Odesílatel:**  
Veronika Brožová  
správce nemovitosti zastupující podílové spoluvlastníky domu na základě plné moci  
Letohradská 367/5, 170 00 Praha 7 – Holešovice  
E-mail: nikabrozova@gmail.com  

**Adresát:**  
**DDAANN s.r.o.**  
k rukám jednatelů: Ing. arch. Dan Merta, MgA. Daniel Baudis  
Letohradská 367/5  
170 00 Praha 7 – Holešovice  

V Praze dne 23. října 2026

---

### Věc: Návrh nové nájemní smlouvy od 1. 1. 2027 a úprava podmínek nájmu
*(nebytový prostor č. 367/101 – ateliér 65,0 m²)*

Vážení páni jednatelé, vážený pane architekte Merto, vážený pane Baudisi,

obracím se na Vás jménem všech podílových spoluvlastníků domu Letohradská 367/5, Praha 7, které zastupuji na základě plné moci při správě pronajímaných prostor.

Velmi si vážíme naší dlouhodobé a bezproblémové spolupráce a vzájemné důvěry. Naším cílem je, aby Vaše působení a užívání prostor ateliéru v našem domě pokračovalo v klidné, stabilní a oboustranně spokojené atmosféře i v dalších letech.

Vzhledem k tomu, že stávající smluvní dokumentace pochází z roku 2021 a původně sjednaná doba určitá již uplynula, přistoupili jsme v zájmu právní jistoty ke **sjednocení a aktualizaci nájemních smluv pro všechny nájemce v domě** s jednotnou účinností od **1. ledna 2027**.

#### Hlavní body nové smlouvy:
* **Doba nájmu a výpovědní lhůta:** Smlouva je uzavřena na **dobu neurčitou** se standardní zákonnou šestiměsíční výpovědní lhůtou (§ 2312 občanského zákoníku). Poskytuje Vám dlouhodobou stabilitu a dostatečný časový prostor pro jakékoliv budoucí plánování.
* **Úprava výše nájemného:** Původní čisté nájemné ve výši 10 000 Kč měsíčně bylo sjednáno v roce 2021 a za posledních téměř 6 let nebylo upravováno, ačkoliv kumulovaná míra inflace za toto období přesáhla 30 % a náklady na správu a provoz domu vzrostly. Nové čisté nájemné navrhujeme ve výši **13 000 Kč měsíčně** (zvýšení o 3 000 Kč, tj. cca 200 Kč/m²). Tato částka zůstává na poměry Holešovic a u komerčního prostoru s přímým vstupem z ulice hluboko pod tržní hladinou a vyjadřuje náš zájem na zachování Vašeho ateliéru v domě.
* **Inflační doložka:** Do smlouvy je nově zakotvena standardní roční inflační doložka (vázaná na index spotřebitelských cen ČSÚ). Tím se předejde velkým skokovým úpravám v budoucnu – nájemné se bude případně valorizovat plynule jednou ročně, poprvé od roku 2028.
* **Služby a bezhotovostní platba:** Měsíční zálohy na služby spojené s užíváním prostor (vodné, osvětlení a úklid spol. prostor) činí dle aktuálního výpočtového listu **876 Kč měsíčně** a podléhají ročnímu vyúčtování. Celková měsíční platba činí **13 876 Kč**. Z důvodu transparentního účetnictví spoluvlastníků je platba splatná **výhradně bezhotovostním převodem** na účet č. **2844175379/0800** pod variabilním symbolem **367101** nejpozději do 15. dne v měsíci.
* **Dodávka energií:** Odběr elektřiny a plynu zůstává veden přímo na Vaši společnost u dodavatelů PRE a PPAS, což Vám zaručuje plnou kontrolu nad spotřebou.

V příloze tohoto dopisu Vám zasílám návrh nové nájemní smlouvy ve dvou vyhotoveních. Prosím Vás o její prostudování, podpis a zaslání jednoho stejnopisu zpět nejpozději do **30. listopadu 2026**. V případě jakýchkoliv dotazů nebo potřeby upřesnění jsem Vám plně k dispozici.

Předem Vám děkuji za vstřícnost a věcné jednání a těším se na pokračování naší vynikající spolupráce.

S přátelským pozdravem,



**Veronika Brožová**  
zástupce podílových spoluvlastníků domu Letohradská 367/5
"""

def build_md_boschofsky_contract():
    return f"""# SMLOUVA O NÁJMU BYTU
(bytová jednotka č. 367/1 v domě Letohradská 367/5, Praha 7)

uzavřená podle ustanovení § 2235 a násl. zákona č. 89/2012 Sb., občanský zákoník, v platném znění (dále jen „občanský zákoník“), mezi smluvními stranami:

---

### Smluvní strany:

{get_co_owners_md("bytové jednotky č. 367/1")}
a

**2. Nájemce:**  
**Pan Ivo Boschofsky**  
Narozen: [Doplnit datum narození / RČ]  
IČ: 63439573  
Bytem: Letohradská 367/5, Holešovice, 170 00 Praha 7  
Číslo bankovního účtu nájemce: [Doplní nájemce]  
*(dále jen „nájemce“ na straně druhé)*

---

### Čl. 1 – Předmět a účel nájmu
1. Pronajímatel přenechává nájemci do užívání bytovou jednotku č. **367/1** nacházející se v 1. nadzemním podlaží (přízemí) domu čp. 367, Letohradská 5, Praha 7, o celkové podlahové ploše **71,50 m²**.
2. Smluvní strany konstatují, že byt sestává z obytných místností, předsíně, WC a umyvadla; v bytě se ke dni podpisu smlouvy nenachází standardní koupelna se sprchou či vanou, což je oběma stranám známo a tato skutečnost je plně zohledněna ve sjednané výši nájemného a ve sníženém směrném čísle roční spotřeby vody pro vyúčtování služeb.
3. Byt je přenecháván k zajištění bytových a osobních potřeb nájemce.
4. Společné prostory domu je nájemce oprávněn užívat v rozsahu přiměřeném řádnému užívání bytu.

---

### Čl. 2 – Stav bytu
1. Nájemce prohlašuje, že byt dlouhodobě užívá, jeho stavební a technický stav i specifické vybavení jsou mu detailně známy a v tomto stavu jej bez výhrad do nájmu přejímá.
2. Po skončení nájmu je nájemce povinen předat byt pronajímateli vyklizený a ve stavu odpovídajícím běžnému opotřebení s přihlédnutím ke smluveným a pronajímatelem písemně schváleným úpravám.

---

### Čl. 3 – Práva a povinnosti smluvních stran
1. **Nájemce je povinen zejména:**
   * a) Užívat byt řádně a s péčí řádného hospodáře, dodržovat noční klid, domovní řád a dobré mravy a nerušit ostatní obyvatele domu.
   * b) Provádět běžnou údržbu a drobné opravy v bytě v souladu s nařízením vlády č. 308/2015 Sb., ve znění nařízení vlády č. 493/2025 Sb. (s limitem do 1 500 Kč na jednotlivou opravu a ročním limitem 150 Kč/m² podlahové plochy bytu) na vlastní náklad.
   * c) Neprovádět žádné stavební úpravy, zásahy do rozvodů (elektřina, plyn, voda, odpady) ani bourací práce bez předchozího písemného souhlasu pronajímatele.
   * d) Písemně nahlásit pronajímateli případné změny v počtu osob užívajících byt pro účely rozúčtování služeb.
   * e) Nepřenechat byt ani jeho část do podnájmu třetí osobě bez předchozího písemného souhlasu pronajímatele.
   * f) Umožnit pronajímateli po předchozím ohlášení přístup do bytu za účelem kontroly stavu, revizí komínů, elektřiny a plynu nebo odečtů měřidel.
   * g) Neodkládat nábytek, materiál ani odpad ve společných prostorách domu (chodby, dvůr, sklepní chodby).
2. **Povinný převod měřidel elektrické energie (PRE) na nájemce:**
   * Dodávka elektrické energie (a plynu) do bytu není součástí služeb zajišťovaných pronajímatelem.
   * **Nájemce se výslovně zavazuje uzavřít na své vlastní jméno smlouvu o sdružených službách dodávky elektrické energie** s příslušným dodavatelem (Pražská energetika, a.s. – PRE) a zajistit přepis elektroměru pro byt č. 367/1 na svou osobu **nejpozději do 31. ledna 2027**.
   * Pronajímatel poskytne nájemci veškerou nezbytnou součinnost a podklady potřebné k provedení tohoto přepisu.
   * Nájemce hradí spotřebu elektřiny přímo dodavateli. Po ukončení nájmu se nájemce zavazuje převést elektroměr zpět na pronajímatele bez jakýchkoliv nedoplatků.
3. **Pronajímatel je povinen:**
   * Zajistit nájemci nerušený výkon práv spojených s užíváním bytu a dodávku základních služeb spojených s domem (vodné a stočné, úklid a osvětlení společných prostor, odvoz komunálního odpadu).

---

### Čl. 4 – Nájemné a úhrada za služby
1. **Výše nájemného:** Nájemné se sjednává dohodou smluvních stran a činí **12 000,- Kč měsíčně** (slovy: dvanáct tisíc korun českých).
2. **Zálohy na služby:** Společně s nájemným se nájemce zavazuje hradit měsíční zálohy na služby (vodné a stočné dle sníženého směrného čísla pro byt bez koupelny, úklid společných prostor, osvětlení domu, svoz odpadu). Výše záloh je stanovena platným Výpočtovým listem a k datu podpisu činí **559,- Kč měsíčně** (pro 1 osobu). Zálohy podléhají ročnímu zúčtování v souladu se zákonem č. 67/2013 Sb.
3. **Závazek výhradně bezhotovostní platby na bankovní účet:**
   * Celková měsíční platba (nájemné + zálohy na služby) ve výši **12 559,- Kč** je splatná **výhradně bezhotovostním převodem na bankovní účet č. 2844175379/0800**, vedený u České spořitelny a.s.
   * Platba je splatná měsíčně dopředu, **vždy nejpozději do 15. dne příslušného kalendářního měsíce**.
   * Nájemce se zavazuje zřídit u své banky trvalý platební příkaz a jako variabilní symbol uvádět: **3671**.
   * **Platby v hotovosti nejsou přípustné.**
4. **Prodlení a smluvní pokuta:** V případě prodlení s úhradou nájemného nebo záloh na služby se sjednává smluvní pokuta ve výši 0,1 % z dlužné částky za každý den prodlení. V souladu s ustanovením § 2254 odst. 1 občanského zákoníku nesmí peněžitá jistota a právo pronajímatele na zaplacení smluvní pokuty v souhrnu přesáhnout trojnásobek měsíčního nájemného.

---

### Čl. 5 – Inflační doložka
1. Smluvní strany sjednávají v souladu s § 2248 občanského zákoníku inflační doložku. Pronajímatel je oprávněn jednostranně zvýšit sjednané nájemné jednou ročně o míru inflace vyjádřenou přírůstkem průměrného ročního indexu spotřebitelských cen za uplynulý kalendářní rok, vyhlašovaným Českým statistickým úřadem, a to poprvé od roku 2028.
2. Zvýšení nájemného je pronajímatel oprávněn uplatnit písemným oznámením zaslaným nájemci (zpravidla k 1. říjnu kalendářního roku), přičemž upravené nájemné je nájemce povinen platit počínaje měsícem následujícím po doručení tohoto oznámení.

---

### Čl. 6 – Doba nájmu, automatická prolongace a skončení nájmu
1. **Doba nájmu:** Tato smlouva se uzavírá na **dobu určitou v trvání jednoho (1) roku**, počínaje dnem **1. 1. 2027** a konče dnem **31. 12. 2027**.
2. **Automatická prolongace:**
   * Neoznámí-li kterákoliv ze smluvních stran písemně druhé smluvní straně nejpozději **dva (2) měsíce před uplynutím sjednané doby nájmu** (tj. nejpozději do 31. října příslušného kalendářního roku), že trvá na ukončení nájmu nebo že si jeho prodloužení nepřeje, **prodlužuje se doba nájmu automaticky o dalších dvanáct (12) měsíců** (vždy o jeden kalendářní rok), a to i opakovaně.
3. **Výhrada neplnění (vyloučení prolongace):**
   * K automatickému prodloužení nájmu dle odstavce 2 tohoto článku **v žádném případě nedojde** a nájem skončí uplynutím doby k 31. prosinci daného roku, pokud:
     * a) nájemce k 31. říjnu nebo k 31. prosinci příslušného roku eviduje vůči pronajímateli **jakýkoliv splatný dluh** na nájemném, zálohách na služby či nedoplatku z ročního vyúčtování služeb, nebo
     * b) nájemce porušuje povinnost hradit platby bezhotovostním převodem na bankovní účet domu dle Čl. 4 odst. 3 této smlouvy, nebo
     * c) nájemce v průběhu roku závažně nebo opakovaně porušil povinnosti vyplývající z této smlouvy či domovního řádu a byl pronajímatelem písemně vyzván k nápravě, nebo
     * d) nájemce řádně nepřevedl elektroměr na své jméno u Pražské energetiky, a.s. (PRE) v souladu s Čl. 3 odst. 2 této smlouvy.
   * Nastane-li některá z výše uvedených skutečností, nájem končí bez dalšího uplynutím sjednané doby a nájemce je povinen byt k 31. prosinci vyklidit a protokolárně předat pronajímateli.
4. **Vyloučení konkludentního prodloužení:** Smluvní strany výslovně vylučují aplikaci ustanovení § 2285 občanského zákoníku. Užívá-li nájemce byt i po skončení nájmu, nájemní smlouva se v žádném případě neprodlužuje.
5. **Skončení nájmu v průběhu sjednané doby:**
   * a) Písemnou dohodou smluvních stran.
   * b) Písemnou výpovědí nájemce podle § 2287 občanského zákoníku, změní-li se okolnosti, z nichž strany při vzniku nájmu vycházely, do té míry, že po nájemci nelze rozumně požadovat setrvání v nájmu; výpovědní doba činí 3 měsíce.
   * c) Písemnou výpovědí pronajímatele ze zákonných důvodů dle § 2288 odst. 1 občanského zákoníku (zejména hrubé porušení povinností nájemcem) s tříměsíční výpovědní dobou a zákonným poučením o právu podat námitky a obrátit se na soud (§ 2286 odst. 2 OZ).
   * d) Písemnou výpovědí pronajímatele bez výpovědní doby pro zvlášť závažné porušení povinností nájemcem ve smyslu § 2291 občanského zákoníku (zejména dluh na nájemném a službách za dobu alespoň 3 měsíců či devastace bytu/domu) po předchozí marné písemné výzvě k nápravě.

---

### Čl. 7 – Jistina (kauce)
1. Nájemce složí na bankovní účet pronajímatele peněžitou jistinu ve výši **10 000,- Kč** (slovy: deset tisíc korun českých) nejpozději do 15 dnů od podpisu této smlouvy (případně se započte jistina již dříve složená).
2. Jistina slouží k zajištění úhrady nájemného, záloh na služby, nedoplatků z vyúčtování služeb a případné náhrady škody. Jistina bude nájemci vyúčtována a vrácena do 15 dnů po protokolárním vyklizení a předání bytu při skončení nájmu, spolu se zákonným úrokem v souladu s § 2254 odst. 2 občanského zákoníku. Pronajímatel je oprávněn si před vrácením jistiny započíst veškeré splatné pohledávky z nájmu.

---

### Čl. 8 – Závěrečná ustanovení
1. Práva a povinnosti stran neupravené touto smlouvou se řídí občanským zákoníkem.
2. Změny a doplňky této smlouvy jsou platné pouze v písemné formě jako vzestupně číslované dodatky.
3. Smlouva je vyhotovena ve dvou stejnopisech s platností originálu, z nichž každá smluvní strana obdrží po jednom vyhotovení.
4. Smluvní strany prohlašují, že si smlouvu přečetly, s jejím obsahem souhlasí a na důkaz toho připojují své podpisy.

Příloha č. 1: Výpočtový list nájemného a záloh na služby

V Praze dne .............................. 2026



....................................................................                    ....................................................................  
**Veronika Brožová**                                                **Ivo Boschofsky**  
v zastoupení podílových spoluvlastníků                                    *(nájemce)*  
*(pronajímatel)*
"""

def build_md_boschofsky_letter():
    return """# Průvodní dopis k nové nájemní smlouvě

**Od:** Veronika Brožová, Letohradská 367/5, 170 00 Praha 7 (nikabrozova@gmail.com)  
**Pro:** Ivo Boschofsky, Byt č. 367/1, Letohradská 367/5, 170 00 Praha 7  
**Datum:** 23. října 2026  

---

### Nová nájemní smlouva od 1. 1. 2027 a pár důležitých věcí k bytu

Ahoj Ivo,

obracím se na tebe ohledně tvého bytu v přízemí (č. 367/1). Známe se v baráku už roky a víš, že si zakládám na tom, abychom spolu vždycky vycházeli férově, lidsky a v sousedské pohodě. Právě proto ti píšu napřímo a bez zbytečných právnických kliček, abychom si v klidu řekli, co a proč potřebujeme od nového roku nastavit.

Jak víš, dům má 32 podílových spoluvlastníků, za které mám plnou moc a zodpovídám jim za řádnou správu. Před úřady i před majiteli musíme mít veškeré smlouvy v pořádku a aktuální. Staré smlouvy už formálně neodpovídají zákonům, a proto teď připravujeme novou smlouvu pro všechny nájemce v domě s platností od 1. ledna 2027.

#### Co je potřeba upravit a na čem se domluvit:

1. **Konec plateb v hotovosti a trvalý příkaz na účet:**  
   Tohle je pro mě úplně zásadní věc. Hromadí se mi tu hotovost, pak s těmi penězi musím běhat do banky a vkládat je na účet, musím tě pořád hlídat a upomínat. Navíc účetní z plateb v hotovosti šílí a spoluvlastníci potřebují mít ve výpisech z účtu naprosto čisté, doložitelné a transparentní položky kvůli ročnímu zúčtování a daním. Když si v bance nastavíš trvalej příkaz na účet domu: **2844175379/0800**, variabilní symbol **3671**, se splatností vždy k **15. dni v měsíci**, bude to pro nás pro všechny mnohem jednodušší a ušetří to čas i starosti nám oběma. Od 1. ledna už proto v hotovosti platby přebírat nebudu.

2. **Přepis elektřiny u PRE na tvoje jméno:**  
   Do konce ledna 2027 je potřeba formálně přepsat elektroměr na tebe přímo u Pražské energetiky (PRE), abys měl spotřebu elektřiny plně ve svých rukách. Nemusíš se bát žádného složitého běhání – já ti připravím veškeré formuláře i plné moci, ty to jen podepíšeš a buď to u PRE vyřídím já, nebo tam skočíme společně. Je to jen administrativní formalita, ale musí být hotová.

3. **Úprava nájmu o 2 000 Kč:**  
   Doteď platíš čistý nájem 10 000 Kč měsíčně. Všichni vidíme, jak za poslední roky strašně vyrostly všechny ceny okolo, pojištění domu i náklady na řemeslníky a údržbu. Proto nájem od 1. ledna zvedáme o 2 000 Kč na **12 000 Kč měsíčně**. K tomu jsou zálohy na služby domu (voda, popelnice, úklid a světlo na chodbě) ve výši **559 Kč měsíčně** – máš tam samozřejmě zohledněné snížené vodné, protože v bytě není klasická koupelna. Celková měsíční platba na účet tedy bude **12 559 Kč**. Určitě sám uznáš, že 12 tisíc za 71,5 m² na Letné je i po tomto zvýšení naprosto symbolická a kamarádská cena, která plně bere ohled na specifika tvého bytu.

4. **Žádné zbytečné papírování – smlouva na rok s automatickým prodloužením:**  
   Abychom se nemuseli každý rok zdržovat sepisováním nových papírů a dodatků, dali jsme do smlouvy **automatické prodlužování**. Smlouva se uzavírá na 1 rok (do 31. 12. 2027), ale pokud je všechno v pořádku – tj. nájem řádně a včas chodí na účet a je přepsaná elektřina – smlouva se sama automaticky prodlužuje o další rok. Nemusíme na ni dál sahat a můžeš v klidu bydlet.

V příloze ti dávám novou smlouvu ve dvou vyhotoveních. V klidu si ji pročti, jedno vyhotovení podepiš a hoď mi ho do schránky (nebo mi ho předej osobně). Kdyby ti v textu cokoliv nebylo jasné nebo ses chtěl na cokoliv zeptat, stav se u mě, dáme kafe a všechno si v pohodě řekneme.

Díky moc za pochopení a spolupráci, vážím si toho!

Měj se fajn,



**Veronika Brožová**  
Letohradská 367/5
"""

def build_md_onari_contract():
    return f"""# SMLOUVA O NÁJMU BYTU
(bytová jednotka č. 367/3 v domě Letohradská 367/5, Praha 7)

uzavřená podle ustanovení § 2235 a násl. zákona č. 89/2012 Sb., občanský zákoník, v platném znění (dále jen „občanský zákoník“), mezi smluvními stranami:

---

### Smluvní strany:

{get_co_owners_md("bytové jednotky č. 367/3")}
a

**2. Nájemce:**  
**Pan Tetsu Onari**  
Narozen: 30. 6. 1980  
Státní příslušnost: Japonsko  
Číslo cestovního pasu / průkazu pobytu: TG 2453612  
Bytem v ČR: Letohradská 367/5, Holešovice, 170 00 Praha 7  
(Trvalé bydliště: 2-29-8 kuboyama-ch Hachioji-city Tokyo 192-0023, Japan)  
Číslo bankovního účtu nájemce: [Doplní nájemce]  
*(dále jen „nájemce“ na straně druhé)*

---

### Čl. 1 – Předmět a účel nájmu
1. Pronajímatel přenechává nájemci do užívání bytovou jednotku č. **367/3** nacházející se v 1. nadzemním podlaží (přízemí) domu čp. 367, Letohradská 5, Praha 7, o celkové podlahové ploše **50,40 m²**.
2. Byt sestává z obytného pokoje, kuchyně, předsíně a sociálního zařízení (koupelna a WC).
3. Byt je pronajímán výhradně k zajištění bytových potřeb nájemce a členů jeho společné domácnosti. Nájemce je oprávněn část bytu přiměřeně využívat též ke své tvůrčí umělecké činnosti za předpokladu, že tato činnost nezpůsobí zvýšené zatížení domu, hluk ani neruší ostatní obyvatele domu.
4. Společné prostory domu je nájemce oprávněn užívat v rozsahu obvyklém a přiměřeném řádnému užívání bytu.

---

### Čl. 2 – Stav bytu
1. Nájemce prohlašuje, že byt dlouhodobě užívá, jeho stavební a technický stav je mu detailně znám a v tomto stavu jej bez výhrad do nájmu přejímá.
2. Po skončení nájmu je nájemce povinen předat byt pronajímateli vyklizený a ve stavu odpovídajícím běžnému opotřebení s přihlédnutím k provedeným a pronajímatelem schváleným opravám.

---

### Čl. 3 – Práva a povinnosti smluvních stran
1. **Nájemce je povinen zejména:**
   * a) Užívat byt řádně a v souladu s dobrými mravy, dodržovat domovní řád a nerušit ostatní uživatele bytů v domě.
   * b) Hradit běžnou údržbu a drobné opravy v bytě v souladu s nařízením vlády č. 308/2015 Sb., ve znění nařízení vlády č. 493/2025 Sb. (s limitem do 1 500 Kč na jednotlivou opravu a ročním limitem 150 Kč/m² podlahové plochy bytu).
   * c) Neprovádět žádné stavební úpravy ani podstatné změny v bytě bez předchozího písemného souhlasu pronajímatele.
   * d) Písemně oznámit pronajímateli změnu v počtu osob žijících v bytě nejpozději do 2 měsíců od okamžiku, kdy změna nastala (pro správné stanovení záloh na služby).
   * e) Nepřenechat byt ani jeho část do podnájmu třetí osobě bez předchozího písemného souhlasu pronajímatele.
   * f) Umožnit pronajímateli po předchozím oznámení přístup do bytu za účelem kontroly technického stavu, provádění odečtů měřidel nebo zákonných revizí.
   * g) Neodkládat věci a neskladovat materiál ve společných prostorách domu (chodby, dvůr, sklepní chodby).
2. **Převod energií (elektřina a plyn):**
   * Dodávka elektřiny a plynu není zahrnuta v zálohách na služby poskytované pronajímatelem. 
   * Nájemce hradí spotřebu elektřiny a plynu přímo dodavatelům na základě smluv vedených na své jméno dle samostatných podružných či fakturačních měřidel. Pronajímatel poskytne veškerou nezbytnou součinnost k vedení/přepisu těchto smluv.
3. **Pronajímatel je povinen:**
   * Udržovat dům a jeho společné části ve stavu způsobilém k řádnému užívání a zajistit nájemci plný a nerušený výkon práv spojených s nájmem bytu.

---

### Čl. 4 – Nájemné a úhrada za plnění spojená s užíváním bytu (služby)
1. **Výše nájemného:** Nájemné se sjednává dohodou smluvních stran a činí **8 000,- Kč měsíčně** (slovy: osm tisíc korun českých).
2. **Zálohy na služby:** Společně s nájemným se nájemce zavazuje hradit měsíční zálohy na nezbytné služby (vodné a stočné, úklid společných prostor, osvětlení společných prostor, odvoz komunálního odpadu). Výše záloh je stanovena platným Výpočtovým listem a k datu podpisu činí **2 150,- Kč měsíčně** (pro hlášený počet osob v bytě). Zálohy podléhají ročnímu vyúčtování vždy do 30. dubna následujícího roku v souladu se zákonem č. 67/2013 Sb.
3. **Závazek výhradně bezhotovostní platby na bankovní účet:**
   * Celková měsíční platba (nájemné + zálohy na služby) ve výši **10 150,- Kč** je splatná **výhradně bezhotovostním převodem na bankovní účet č. 2844175379/0800**, vedený u České spořitelny a.s.
   * Platba je splatná měsíčně dopředu, **nejpozději do 15. dne příslušného kalendářního měsíce**.
   * Variabilní symbol platby: **3673**. Platby v hotovosti nejsou přípustné.
4. **Prodlení a smluvní pokuta:** V případě prodlení s úhradou nájemného nebo záloh na služby se sjednává smluvní pokuta ve výši 0,1 % z dlužné částky za každý den prodlení. V souladu s ustanovením § 2254 odst. 1 občanského zákoníku nesmí peněžitá jistota a právo pronajímatele na zaplacení smluvní pokuty v souhrnu přesáhnout trojnásobek měsíčního nájemného.

---

### Čl. 5 – Inflační doložka
1. Smluvní strany sjednávají v souladu s § 2248 občanského zákoníku inflační doložku. Pronajímatel je oprávněn jednostranně zvýšit sjednané nájemné jednou ročně o míru inflace vyjádřenou přírůstkem průměrného ročního indexu spotřebitelských cen za uplynulý kalendářní rok, vyhlašovaným Českým statistickým úřadem, a to poprvé od roku 2028.
2. Zvýšení nájemného je pronajímatel oprávněn uplatnit písemným oznámením zaslaným nájemci, přičemž upravené nájemné je nájemce povinen platit počínaje měsícem následujícím po doručení tohoto oznámení (zpravidla k 1. říjnu kalendářního roku).

---

### Čl. 6 – Doba nájmu, automatická prolongace a skončení nájmu
1. **Doba nájmu:** Tato smlouva se uzavírá na **dobu určitou v trvání jednoho (1) roku**, počínaje dnem **1. 1. 2027** a konče dnem **31. 12. 2027**.
2. **Automatická prolongace:**
   * Neoznámí-li kterákoliv ze smluvních stran písemně druhé smluvní straně nejpozději **dva (2) měsíce před uplynutím sjednané doby nájmu** (tj. nejpozději do 31. října příslušného kalendářního roku), že trvá na ukončení nájmu nebo že si jeho prodloužení nepřeje, **prodlužuje se doba nájmu automaticky o dalších dvanáct (12) měsíců** (vždy o jeden kalendářní rok), a to i opakovaně.
3. **Výhrada neplnění (vyloučení prolongace):**
   * K automatickému prodloužení nájmu dle odstavce 2 tohoto článku **v žádném případě nedojde** a nájem skončí uplynutím doby k 31. prosinci daného roku, pokud:
     * a) nájemce k 31. říjnu nebo k 31. prosinci příslušného roku eviduje vůči pronajímateli **jakýkoliv splatný dluh** na nájemném, zálohách na služby či nedoplatku z ročního vyúčtování služeb, nebo
     * b) nájemce v průběhu roku závažně nebo opakovaně porušil povinnosti vyplývající z této smlouvy či domovního řádu a byl pronajímatelem písemně vyzván k nápravě, nebo
     * c) nájemce řádně nepřevedl měřidla energií na své jméno v souladu s Čl. 3 odst. 2 této smlouvy.
   * Nastane-li některá z výše uvedených skutečností, nájem končí bez dalšího uplynutím sjednané doby a nájemce je povinen byt k 31. prosinci vyklidit a protokolárně předat pronajímateli.
4. **Vyloučení konkludentního prodloužení:** Smluvní strany výslovně vylučují aplikaci ustanovení § 2285 občanského zákoníku. Užívá-li nájemce byt i po skončení nájmu, nájemní smlouva se v žádném případě neprodlužuje.
5. **Skončení nájmu v průběhu sjednané doby:**
   * a) Písemnou dohodou smluvních stran.
   * b) Písemnou výpovědí nájemce podle § 2287 občanského zákoníku, změní-li se okolnosti, z nichž strany při vzniku nájmu vycházely, do té míry, že po nájemci nelze rozumně požadovat setrvání v nájmu; výpovědní doba činí 3 měsíce.
   * c) Písemnou výpovědí pronajímatele ze zákonných důvodů dle § 2288 odst. 1 občanského zákoníku (zejména hrubé porušení povinností nájemcem) s tříměsíční výpovědní dobou a zákonným poučením o právu podat námitky a obrátit se na soud (§ 2286 odst. 2 OZ).
   * d) Písemnou výpovědí pronajímatele bez výpovědní doby pro zvlášť závažné porušení povinností nájemcem ve smyslu § 2291 občanského zákoníku (zejména dluh na nájemném a službách za dobu alespoň 3 měsíců či devastace bytu/domu) po předchozí marné písemné výzvě k nápravě.

---

### Čl. 7 – Jistina (kauce)
1. Nájemce složil na účet pronajímatele peněžitou jistinu ve výši **10 000,- Kč** (slovy: deset tisíc korun českých).
2. Jistina slouží k zajištění úhrady nájemného, záloh na služby, nedoplatků z vyúčtování služeb a případné náhrady škody. Jistina bude nájemci vyúčtována a vrácena do 15 dnů po protokolárním vyklizení a předání bytu při skončení nájmu, spolu se zákonným úrokem v souladu s § 2254 odst. 2 občanského zákoníku. Pronajímatel je oprávněn si před vrácením jistiny započíst veškeré splatné pohledávky z nájmu.

---

### Čl. 8 – Závěrečná ustanovení
1. Práva a povinnosti stran neupravené touto smlouvou se řídí občanským zákoníkem.
2. Změny a doplňky této smlouvy jsou platné pouze v písemné formě jako vzestupně číslované dodatky.
3. Smlouva je vyhotovena ve dvou stejnopisech s platností originálu, z nichž každá smluvní strana obdrží po jednom vyhotovení.
4. Smluvní strany prohlašují, že si smlouvu přečetly, s jejím obsahem souhlasí a na důkaz toho připojují své podpisy.

Příloha č. 1: Výpočtový list nájemného a záloh na služby

V Praze dne .............................. 2026



....................................................................                    ....................................................................  
**Veronika Brožová**                                                **Tetsu Onari**  
v zastoupení podílových spoluvlastníků                                    *(nájemce)*  
*(pronajímatel)*
"""

def build_md_onari_letter():
    return """# Průvodní dopis k nové nájemní smlouvě

**Od:** Veronika Brožová, Letohradská 367/5, 170 00 Praha 7 (nikabrozova@gmail.com)  
**Pro:** Tetsu Onari, Byt č. 367/3, Letohradská 367/5, 170 00 Praha 7  
**Datum:** 23. října 2026  

---

### Nová nájemní smlouva od 1. 1. 2027 a úprava podmínek nájmu

Ahoj Tetsu,

obracím se na tebe ohledně tvého bytu č. 367/3 v přízemí domu Letohradská 5. Jak víš, dům má 32 podílových spoluvlastníků a já pro ně pronajímané byty spravuji na základě udělené plné moci. Od 1. ledna 2027 přistupujeme ke sjednocení a aktualizaci všech nájemních smluv v domě tak, aby odpovídaly platným zákonům i ekonomické realitě.

#### Důvody nové smlouvy a úpravy nájemného:

1. **Dvanáct let takto nízkého nájemného je již neudržitelných:**  
   Tvoje stávající nájemní smlouva byla uzavřena v roce 2014 s čistým nájemným 5 700 Kč měsíčně. Za celých dlouhých 12 let se nájemné vůbec nezměnilo. Držet dál po 12 letech takto nízký nájem je z pohledu správy domu i všech 32 spoluvlastníků naprosto neudržitelné. Veškeré náklady na provoz domu, údržbu, opravy, pojištění i služby za tu dobu zásadně vzrostly a kumulovaná inflace v ČR byla enormní.

2. **Nová výše nájemného na 8 000 Kč měsíčně:**  
   Čisté nájemné se od 1. 1. 2027 upravuje na **8 000 Kč měsíčně**. K tomu jsou měsíční zálohy na služby spojené s užíváním bytu (vodné a stočné, odvoz odpadu, osvětlení a úklid společných prostor pro nahlášený počet osob v rodině) ve výši **2 150 Kč měsíčně**. Celková měsíční platba činí **10 150 Kč**. I po této úpravě zůstává částka 8 000 Kč za byt o ploše 50,4 m² na Letné hluboko pod běžnou tržní hladinou.

3. **Smlouva na 1 rok s automatickým prodlužováním:**  
   Smlouva se uzavírá na dobu určitou 1 rok (do 31. 12. 2027) s mechanismem **automatického prodlužování** o dalších 12 měsíců. Pokud je nájem řádně a včas hrazen na bankovní účet domu a plněny povinnosti, smlouva se automaticky prodlužuje bez nutnosti každoročního sepisování nových dodatků.

4. **Inflační doložka od roku 2028:**  
   Do smlouvy je vložena standardní inflační doložka vázaná na oficiální index Českého statistického úřadu, která se poprvé může uplatnit od roku 2028. Tím se předejde tomu, aby se nájemné po dalších letech muselo upravovat skokově.

5. **Platby bezhotovostně na účet:**  
   Celková platba **10 150 Kč měsíčně** je splatná výhradně bezhotovostním převodem (trvalým příkazem) na účet domu: **2844175379/0800**, variabilní symbol **3673**, se splatností vždy nejpozději do **15. dne v měsíci**.

V příloze ti předávám návrh nové nájemní smlouvy ve dvou vyhotoveních. V klidu si ji prosím projdi, jedno vyhotovení podepiš a vrať mi ho do konce listopadu 2026. Kdyby ses chtěl na cokoliv zeptat, stav se u mě doma v bytě č. 5 nebo mi napiš.

Díky za pochopení.

Měj se hezky,



**Veronika Brožová**  
Letohradská 367/5
"""

# ==============================================================================
# MAIN EXECUTION & SAVING
# ==============================================================================
def main():
    # 1. Zjistit cesty k Documents
    user_home = os.path.expanduser('~')
    docs_base = os.path.join(user_home, 'Documents')
    
    # Hledáme složku Společenství
    spol_candidates = [os.path.join(docs_base, d) for d in os.listdir(docs_base) 
                       if os.path.isdir(os.path.join(docs_base, d)) and d.lower().startswith('spole')]
    if not spol_candidates:
        raise FileNotFoundError("Složka Společenství nebyla nalezena v Documents!")
    spol_dir = spol_candidates[0]
    
    smlouvy_candidates = [os.path.join(spol_dir, d) for d in os.listdir(spol_dir) 
                          if os.path.isdir(os.path.join(spol_dir, d)) and d.lower().startswith('smlou')]
    if not smlouvy_candidates:
        smlouvy_dir = os.path.join(spol_dir, 'Smlouvy')
        os.makedirs(smlouvy_dir, exist_ok=True)
    else:
        smlouvy_dir = smlouvy_candidates[0]
        
    najemne_candidates = [os.path.join(smlouvy_dir, d) for d in os.listdir(smlouvy_dir) 
                          if os.path.isdir(os.path.join(smlouvy_dir, d)) and d.lower().startswith('n')]
    if not najemne_candidates:
        najemne_dir = os.path.join(smlouvy_dir, 'Nájemné')
        os.makedirs(najemne_dir, exist_ok=True)
    else:
        najemne_dir = najemne_candidates[0]

    # Cesta k agenda/koncepty v repozitáři
    repo_koncepty = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agenda', 'koncepty'))
    os.makedirs(repo_koncepty, exist_ok=True)

    print(f"Cílové adresáře pro uložení:")
    print(f"  1. Documents/Společenství/Smlouvy/Nájemné: {najemne_dir}")
    print(f"  2. Documents/Společenství/Smlouvy:         {smlouvy_dir}")
    print(f"  3. Repo agenda/koncepty:                   {repo_koncepty}")

    # Definice generovaných souborů
    files_to_build = [
        # (id, filename_base, docx_builder, md_builder)
        ("DDAANN Smlouva", "101_DDAANN_Smlouva_2027", build_docx_ddaann_contract, build_md_ddaann_contract, "smlouva_DDAANN_2027.md"),
        ("DDAANN Průvodní dopis", "101_DDAANN_Pruvodni_dopis_2027", build_docx_ddaann_letter, build_md_ddaann_letter, "pruvodni_dopis_DDAANN_2027.md"),
        ("Boschofsky Smlouva", "1_Boschofsky_Smlouva_2027", build_docx_boschofsky_contract, build_md_boschofsky_contract, "smlouva_Boschofsky_2027.md"),
        ("Boschofsky Průvodní dopis", "1_Boschofsky_Pruvodni_dopis_2027", build_docx_boschofsky_letter, build_md_boschofsky_letter, "pruvodni_dopis_Boschofsky_2027.md"),
        ("Onari Smlouva", "3_Onari_Smlouva_2027", build_docx_onari_contract, build_md_onari_contract, "smlouva_Onari_2027.md"),
        ("Onari Průvodní dopis", "3_Onari_Pruvodni_dopis_2027", build_docx_onari_letter, build_md_onari_letter, "pruvodni_dopis_Onari_2027.md"),
    ]

    for label, base_name, docx_builder, md_builder, repo_md_name in files_to_build:
        print(f"\nGeneruji: {label} ({base_name})...")
        
        # 1. DOCX
        doc = docx_builder()
        docx_najemne_path = os.path.join(najemne_dir, f"{base_name}.docx")
        docx_smlouvy_path = os.path.join(smlouvy_dir, f"{base_name}.docx")
        doc.save(docx_najemne_path)
        doc.save(docx_smlouvy_path)
        print(f"  -> Uloženo DOCX do Nájemné i Smlouvy.")
        
        # 2. Markdown
        md_content = md_builder()
        # Do Nájemné
        with open(os.path.join(najemne_dir, f"{base_name}.md"), 'w', encoding='utf-8') as f:
            f.write(md_content)
        # Do Smlouvy
        with open(os.path.join(smlouvy_dir, f"{base_name}.md"), 'w', encoding='utf-8') as f:
            f.write(md_content)
        # Do repo agenda/koncepty
        with open(os.path.join(repo_koncepty, repo_md_name), 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"  -> Uloženo MD do Nájemné, Smlouvy a {repo_md_name}.")

    print("\nGenerování všech 6 dokumentů proběhlo úspěšně!")

if __name__ == '__main__':
    main()
