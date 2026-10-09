#!/usr/bin/env python3
"""Scheda prodotto (post 1080x1350) o storia (1080x1920).
uso: product_card.py post|story KEY "RIGA1" "RIGA2" "chip1|chip2|chip3" [SEED]
Salva in media/<mese>/KEY.png (mese preso da KEY? no: cartella media/auto/)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cal_lib import *
kind,key,l1,l2,chips=sys.argv[1:6]; seed=int(sys.argv[6]) if len(sys.argv)>6 else 500
chips=[c for c in chips.split('|') if c]
os.makedirs(ROOT+'/media/auto',exist_ok=True)
kw=dict(lines=[(l1,WHITE,68 if len(l1)>14 else 80),(l2,CYc,76)],body='Olio motore sintetico.' if kind=='post' else None,chips=chips,seed=seed)
if kind=='post':
    img=slide(icon=('drop' if len(chips)<4 else None),foot='Spedizione gratuita in Italia  ·  autoevostore.it',**kw)
else:
    img=story(foot='autoevostore.it',**kw)
img.save(f'{ROOT}/media/auto/{key}.png',optimize=True); print(f'media/auto/{key}.png')
