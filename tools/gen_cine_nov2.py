"""Nuovo set cinematografico novembre 2026 (feed 1080x1350 + storie 1080x1920).
Flaconi reali (products/*.png) in scena con cine_lib.render; testi da titolo/tag Shopify.
Ogni creatività ha composizione, palette e luce diverse dalla precedente."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from cine_lib import render
import cine_type as T
from cal_lib import add_brt
from pilot_common import save_srgb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = ROOT + '/media/2026-11c'
W, H = 1080, 1350

# key, scene, testo
S = [
 # 08/11 dom domanda
 dict(k='n08', keys=['selenia_digitek_0w30', 'castrol_edge_td_5w40', 'selenia_20k_10w40'], pal='violet', seed=21,
      heights=[0.33, 0.39, 0.33], xs=[0.22, 0.50, 0.78], base_y=0.93, light='right',
      txt=dict(x=0, y=290, align='c', kicker='Domanda della domenica', lines=['Cosa guardi', 'per primo?'],
               sub='A) viscosità   B) marchio   C) omologazione', size=92, maxw=900),
      pill=('Rispondi nei commenti', 'c', None)),
 # 09/11 Selenia Digitek Pure Energy 0W-30 (nuovo)
 dict(k='n09', keys=['selenia_digitek_0w30'], pal='cyan', seed=31, heights=[0.64], xs=[0.70], cx=0.70, base_y=0.88,
      txt=dict(x=70, y=330, kicker='Selenia Digitek Pure Energy', lines=['0W-30.', 'Leggi il', 'suffisso.'],
               sub='ACEA C2 · API SN\nFIAT 9.55535-GS1', size=100, maxw=470), pill=('Scheda su autoevostore.it', 'l', None)),
 # 12/11 Castrol EDGE Turbo Diesel 5W-40 (nuovo)
 dict(k='n12', keys=['castrol_edge_td_5w40'], pal='amber', seed=11, heights=[0.66], xs=[0.30], cx=0.30, base_y=0.88,
      light='right',
      txt=dict(x=560, y=330, kicker='Castrol EDGE Turbo Diesel', lines=['5W-40', 'per chi', 'chiede 505.'],
               sub='ACEA C3\nVW 505.00 / 505.01\nFIAT 9.55535-S2', size=92, maxw=460), pill=('Scheda su autoevostore.it', 'l', None)),
 # 14/11 sab fiducia: spedizione
 dict(k='n14', keys=['castrol_edge_ll3_5w30', 'mobil1_esp_5w30'], pal='cyan', seed=44, heights=[0.40, 0.46],
      xs=[0.36, 0.64], base_y=0.92, light='left',
      txt=dict(x=0, y=240, align='c', kicker='Spedizione gratuita in Italia', lines=['Ordini oggi.', 'Arriva in 24/48 ore.'],
               sub='Corriere BRT · Europa 3-7 giorni lavorativi (escluse Cipro e Malta)', size=84, maxw=880),
      brt=560),
 # 15/11 dom vero o falso
 dict(k='n15', keys=['selenia_multipower_gas'], pal='violet', seed=52, heights=[0.44], xs=[0.5], cx=0.5, base_y=0.95,
      mood=0.85,
      txt=dict(x=0, y=290, align='c', kicker='Vero o falso?', lines=['“Stessa viscosità,', 'stesso olio.”'],
               sub='Rispondi V o F nei commenti. Domani la risposta nelle storie.', size=80, maxw=860)),
 # 16/11 Selenia WR 5W-40 Diesel
 dict(k='n16', keys=['selenia_wr_5w40_diesel'], pal='amber', seed=63, heights=[0.70], xs=[0.66], cx=0.66, base_y=0.90,
      txt=dict(x=70, y=330, kicker='Selenia WR Diesel', lines=['5W-40.', 'Il diesel', 'FIAT.'],
               sub='ACEA A3/B4 · API SN/CF\nFIAT 9.55535-N2/N3', size=100, maxw=460), pill=('Scheda su autoevostore.it', 'l', None)),
 # 17/11 consiglio: reso
 dict(k='n17', keys=['total_ineo_mc3'], pal='cyan', seed=71, heights=[0.56], xs=[0.74], cx=0.74, base_y=0.90, light='right',
      txt=dict(x=70, y=300, kicker='Acquista sereno', lines=['Reso entro', '14 giorni.'],
               sub='Assistenza dal lunedì al venerdì, 9:00-18:00.\nDubbi sulla specifica? Scrivici targa, modello e anno in DM.',
               size=100, maxw=520), pill=('Condizioni su autoevostore.it', 'l', None)),
 # 19/11 Mannol Longlife 504/507
 dict(k='n19', keys=['mannol_longlife_504_507'], pal='violet', seed=83, heights=[0.68], xs=[0.32], cx=0.32, base_y=0.89,
      light='right',
      txt=dict(x=570, y=330, kicker='Mannol Longlife', lines=['504/507.', 'Due sigle,', 'un flacone.'],
               sub='5W-30 · ACEA C3\nVW 504.00 / 507.00\nPorsche C30', size=92, maxw=450), pill=('Scheda su autoevostore.it', 'l', None)),
 # 20/11 Selenia WR Pure Energy 5W-30
 dict(k='n20', keys=['selenia_wr_pure_energy_5w30'], pal='cyan', seed=95, heights=[0.74], xs=[0.5], cx=0.5, base_y=0.95,
      txt=dict(x=0, y=215, align='c', kicker='Selenia WR Pure Energy', lines=['5W-30 · ACEA C2'],
               sub='FIAT / Mopar', size=78, maxw=880)),
 # 21/11 sab: tre dati
 dict(k='n21', keys=['castrol_magnatec_prof_d_0w30', 'selenia_multipower_gas'], pal='amber', seed=101,
      heights=[0.44, 0.50], xs=[0.28, 0.72], base_y=0.92,
      txt=dict(x=0, y=240, align='c', kicker='Prima di ordinare', lines=['Targa. Modello.', 'Anno.'],
               sub='Mandaceli in DM: verifichiamo noi la specifica giusta per la tua auto.', size=92, maxw=860)),
 # 22/11 dom: GPL/metano (nuovo prodotto Multipower Gas)
 dict(k='n22', keys=['selenia_multipower_gas'], pal='cyan', seed=112, heights=[0.66], xs=[0.70], cx=0.70, base_y=0.89,
      txt=dict(x=70, y=330, kicker='Selenia Multipower Gas', lines=['Viaggi a', 'GPL o', 'metano?'],
               sub='5W-40 · ACEA C3 · API SP\nFIAT 9.55535-T2', size=100, maxw=470), pill=('Scheda su autoevostore.it', 'l', None)),
 # 23/11 Selenia 20K 10W-40 (nuovo)
 dict(k='n23', keys=['selenia_20k_10w40'], pal='amber', seed=123, heights=[0.68], xs=[0.30], cx=0.30, base_y=0.89,
      light='right',
      txt=dict(x=560, y=330, kicker='Selenia 20K', lines=['10W-40.', 'Semisintetico,', 'specifica FCA.'],
               sub='ACEA A3/B4\nFIAT 9.55535-G2 / D2', size=80, maxw=470), pill=('Scheda su autoevostore.it', 'l', None)),
 # 25/11 Magnatec Professional D 0W-30 (nuovo)
 dict(k='n25', keys=['castrol_magnatec_prof_d_0w30'], pal='violet', seed=134, heights=[0.70], xs=[0.68], cx=0.68,
      base_y=0.90,
      txt=dict(x=70, y=330, kicker='Castrol Magnatec Professional D', lines=['Ford?', 'Cerca la', 'WSS.'],
               sub='0W-30 · ACEA C2\nFord WSS-M2C950-A', size=100, maxw=460), pill=('Scheda su autoevostore.it', 'l', None)),
 # 26/11 educativo: i numeri
 dict(k='n26', keys=['selenia_digitek_0w30', 'castrol_edge_td_5w40', 'selenia_20k_10w40'], pal='cyan', seed=145,
      heights=[0.40, 0.44, 0.48], xs=[0.20, 0.50, 0.80], base_y=0.92, light='right',
      txt=dict(x=0, y=230, align='c', kicker='0W-30 · 5W-40 · 10W-40', lines=['I numeri dicono', 'la viscosità.'],
               sub='Non dicono se è l’olio giusto: quello lo dice l’omologazione del costruttore.', size=84, maxw=880)),
 # 28/11 sab fiducia: assistenza
 dict(k='n28', keys=['castrol_edge_0w20_c5'], pal='amber', seed=156, heights=[0.62], xs=[0.72], cx=0.72, base_y=0.90,
      light='right',
      txt=dict(x=70, y=320, kicker='Assistenza vera', lines=['Ti risponde', 'chi conosce', 'gli oli.'],
               sub='Lun-ven 9:00-18:00.\nScrivici in DM targa, modello e anno.', size=92, maxw=500)),
 # 29/11 dom domanda
 dict(k='n29', keys=['petronas_xs_5w30', 'castrol_magnatec_prof_d_0w30', 'mannol_longlife_504_507', 'selenia_wr_forward_0w30'],
      pal='violet', seed=167, heights=[0.36, 0.40, 0.40, 0.36], xs=[0.16, 0.39, 0.61, 0.84], base_y=0.93,
      txt=dict(x=0, y=290, align='c', kicker='Domanda della domenica', lines=['Che auto guidi?'],
               sub='Scrivi marca, modello e anno nei commenti: ti diciamo quale specifica cercare.', size=96, maxw=860)),
]


def build(s, w=W, h=H, story=False):
    kw = dict(palette=s['pal'], seed=s['seed'], heights=s['heights'], xs=s['xs'], base_y=s['base_y'],
              light=s.get('light', 'left'), mood=s.get('mood', 1.0), logo_w=0.36)
    if 'cx' in s: kw['cx'] = s['cx']
    im = render(w, h, s['keys'], **kw).convert('RGBA')
    t = dict(s['txt']); sc = 1.0
    y0 = t.pop('y') + (300 if story else 0)
    y = T.block(im, t.pop('x'), y0, kicker=t.pop('kicker'), lines=t.pop('lines'), sub=t.pop('sub'),
                size=t.pop('size'), maxw=t.pop('maxw'), align=t.pop('align', 'l'), subsize=30)
    if s.get('pill'):
        txt, al, py = s['pill']
        T.pill(im, 70, (py + (300 if story else 0)) if py else y + 30, txt, size=26, align=al)
    if s.get('brt'):
        add_brt(im, s['brt'] + (300 if story else 0), scale=0.6)
    return im


if __name__ == '__main__':
    only = sys.argv[1:]
    os.makedirs(OUT, exist_ok=True)
    for s in S:
        if only and s['k'] not in only: continue
        im = build(s)
        save_srgb(im, f"{OUT}/{s['k']}.jpg", jpg=True)
        print(s['k'])
