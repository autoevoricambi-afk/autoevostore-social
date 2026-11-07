"""Storia 'bilancio del mese' (1080x1920) con numeri REALI Metricool 8/10-6/11/2026 (IG).
Fonti: IGEV05 views account (somma giornaliera = 773), IGEV37 contenuti feed+reel (somma = 45), IGEV23 views Reel (max 126 il 23/10).
Bozza locale: NON programmata."""
import sys
sys.path.insert(0, '.')
from cine_lib import render
import cine_type as T
from ae_lib import font, CY
from PIL import ImageDraw
W, H = 1080, 1920
OUT = '/home/claude/pacchetto_pilota_v1/07_bilancio_8nov'
import os; os.makedirs(OUT, exist_ok=True)
im = render(W, H, [], palette='cyan', logo_w=0.40, logo_top=0.065, seed=21).convert('RGBA')
y = T.block(im, 0, 470, kicker="Il primo mese · ottobre", lines=["Bilancio."], align="c", size=120, subsize=36)
d = ImageDraw.Draw(im)
rows = [('45', 'contenuti pubblicati'), ('773', 'visualizzazioni su Instagram'), ('126', 'visualizzazioni, il Reel più visto')]
y += 40
for num, lab in rows:
    T.shadow_text(im, (W / 2, y), num, font('Bold', 150), T.WHITE, blur=14, alpha=210, anchor='ma')
    T.shadow_text(im, (W / 2, y + 178), lab, font('Regular', 40), T.SOFT, blur=8, alpha=190, anchor='ma')
    y += 285
T.block(im, 0, y + 10, lines=[], sub='Da lunedì un Reel prodotto ogni giorno.', maxw=860, subsize=40, align='c')
T.pill(im, 0, y + 110, 'Visita il profilo', size=40, align='c')
from pilot_common import save_srgb
save_srgb(im, f'{OUT}/AEV_storia-bilancio-mese_v1_1080x1920.png')
save_srgb(im, f'{OUT}/AEV_storia-bilancio-mese_v1_1080x1920.jpg', jpg=True)
print('ok', y)
