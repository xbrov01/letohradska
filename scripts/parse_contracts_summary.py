# -*- coding: utf-8 -*-
import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/contract_dump.txt', 'r', encoding='utf-8') as f:
    content = f.read()

sections = content.split('='*70)
for s in sections:
    lines = s.strip().splitlines()
    if not lines or len(lines) < 2: 
        continue
    file_info = lines[0]
    path_info = lines[1] if len(lines) > 1 else ''
    text = '\n'.join(lines[2:])
    
    # identify tenant / unit
    print(f"\n==================================================")
    print(file_info)
    print(path_info)
    has_inf = 'infla' in text.lower()
    print(f"Obsahuje inflační doložku: {'*** ANO ***' if has_inf else 'NE'}")
    
    # Find sentences
    sentences = re.split(r'\. |\n', text)
    matched = []
    for sent in sentences:
        s_clean = ' '.join(sent.split())
        s_low = s_clean.lower()
        if any(w in s_low for w in ['infla', 'nájemné činí', 'nájemné se sjednává', 'výše nájemného', 'měsíční nájemné', 'doba nájmu', 'se uzavírá na dobu', 'doba určitá', 'doba neurčitá']):
            matched.append(s_clean)
    
    for m in matched[:10]:
        print(f"  • {m}")
