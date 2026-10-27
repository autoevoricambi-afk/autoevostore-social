"""Pilota 2: carosello educativo 5 slide (1080x1350 sRGB) - 'Come scegliere l'olio: tre controlli'.
Prodotti: flaconi reali. Specifiche citate solo da titolo/tag Shopify dei prodotti attivi:
 - Castrol EDGE LongLife III 5W-30: ACEA C3, VW 504.00/507.00, MB 229.52, Porsche C30
 - Selenia WR Pure Energy 5W-30: ACEA C2 (FIAT/Mopar)
 - Mobil 1 ESP 5W-30: ACEA C3, BMW LL-04, MB 229.52, VW 504/507"""
from pilot_common import *
from cine_lib import render
import cine_type as T
from ae_lib import font, CY
from PIL import ImageDraw

W, H = 1080, 1350
OUT = f'{PK}/02_carosello'


def dots(im, n, i):
    d = ImageDraw.Draw(im)
    x0 = W / 2 - (n - 1) * 22
    for k in range(n):
        r = 7 if k == i else 5
        col = CY + (255,) if k == i else (120, 140, 160, 200)
        d.ellipse([x0 + k * 44 - r, H - 52 - r, x0 + k * 44 + r, H - 52 + r], fill=col)


def slide(i, key, palette, side, kicker, lines, sub, pill=None, size=92, seed=3, light=None):
    bx = 0.72 if side == 'right' else 0.28
    im = render(W, H, [key], palette=palette, heights=[0.56], xs=[bx], cx=bx, base_y=0.86, logo_w=0.30,
                seed=seed, light=light or ('left' if side == 'right' else 'right')).convert('RGBA')
    maxw = 520
    sz = fit_size(lines, maxw, size)
    x = 64 if side == 'right' else W - 64 - maxw
    # testo allineato a sinistra nella colonna scelta
    y = T.block(im, x, 470, kicker=kicker, lines=lines, sub=sub, maxw=maxw, size=sz, subsize=30)
    if pill: T.pill(im, x, y + 34, pill, size=26)
    dots(im, 5, i)
    return im


S = []
# 1 copertina
S.append(slide(0, 'mobil1_esp_5w30', 'cyan', 'right', 'Guida · scorri', ['Non scegliere', "l'olio dalla", 'sola viscosità.'],
               'Tre controlli da fare sul libretto, prima di aprire il carrello.', size=70, seed=3))
# 2 viscosità
S.append(slide(1, 'castrol_edge_ll3_5w30', 'cyan', 'left', 'Controllo 1 di 3', ['Viscosità', '5W-30.'],
               "Dice come scorre l'olio a freddo (5W) e a caldo (30). Non dice per quale motore è approvato.", size=96, seed=5))
# 3 ACEA
S.append(slide(2, 'selenia_wr_pure_energy_5w30', 'violet', 'right', 'Controllo 2 di 3', ['Categoria', 'ACEA.'],
               'La lettera indica il tipo di impiego: A/B, C, E. Le categorie C (ad esempio C2, C3) sono per motori con catalizzatore e filtro antiparticolato.',
               size=96, seed=7))
# 4 omologazione
S.append(slide(3, 'mobil1_esp_5w30', 'amber', 'left', 'Controllo 3 di 3', ['Omologazione', 'costruttore.'],
               'È il costruttore a indicare quale olio va bene: ad esempio VW 504.00/507.00, MB 229.52, BMW LL-04. La trovi sul libretto e sull’etichetta.',
               size=84, seed=9))
# 5 chiusura: tre flaconi, un solo invito
im = render(W, H, ['selenia_wr_pure_energy_5w30', 'castrol_edge_ll3_5w30', 'mobil1_esp_5w30'], palette='cyan',
            heights=[0.35, 0.41, 0.35], xs=[0.26, 0.50, 0.74], base_y=0.90, logo_w=0.30, seed=11).convert('RGBA')
y = T.block(im, 0, 285, kicker='Da tenere a portata di mano', lines=['Salva la guida.'], sub='Viscosità, ACEA e omologazione devono coincidere con il libretto.',
            maxw=860, size=88, subsize=32, align='c')
T.pill(im, 0, y + 30, 'Salva il post', size=28, align='c')
dots(im, 5, 4)
S.append(im)

for k, im in enumerate(S, 1):
    save_srgb(im, f'{OUT}/AEV_carosello-scelta-olio_s{k}_v1_1080x1350.png')
    save_srgb(im, f'{OUT}/AEV_carosello-scelta-olio_s{k}_v1_1080x1350.jpg', jpg=True)
print('ok', len(S))
