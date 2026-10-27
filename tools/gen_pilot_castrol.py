"""Pilota 1: creatività Castrol EDGE LongLife III 5W-30 (feed 1080x1350, sRGB).
Dati: titolo/tag Shopify del prodotto attivo (ACEA C3, VW 504.00/507.00, MB 229.52, Porsche C30)."""
from pilot_common import *
from cine_lib import render
import cine_type as T

W, H = 1080, 1350
KW = dict(palette='cyan', heights=[0.62], xs=[0.70], cx=0.70, base_y=0.86, logo_w=0.36, seed=3)
plate = render(W, H, ['castrol_edge_ll3_5w30'], **KW)
save_srgb(plate, f'{PK}/05_sorgenti/castrol_v1_senza_testo.png')
im = plate.convert('RGBA')
y = T.block(im, 70, 520, kicker='Castrol EDGE 5W-30', lines=['Prima la', 'sigla.'],
            sub='LongLife III · ACEA C3\nVW 504.00/507.00 · MB 229.52\nPoi controlla il libretto.',
            maxw=470, size=96, subsize=29)
T.pill(im, 70, y + 36, 'Scopri la scheda · autoevostore.it', size=26)
save_srgb(im, f'{PK}/01_castrol/AEV_castrol-edge-ll3_feed_v1_1080x1350.png')
save_srgb(im, f'{PK}/01_castrol/AEV_castrol-edge-ll3_feed_v1_1080x1350.jpg', jpg=True)
print('ok')
