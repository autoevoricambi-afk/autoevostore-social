"""Pilota 3: Reel 'identità AUTO EVO' 16 s, 1080x1920, 24 fps. Frame renderizzati con cine_lib (flaconi reali),
testi in sovrimpressione dentro le zone sicure dell'interfaccia di Instagram (y 270-1530, x 60-960).
Uso:  python3 gen_pilot_reel.py frames [start end]   -> JPEG in FRAMES
      python3 gen_pilot_reel.py poster              -> fotogrammi chiave
Poi ffmpeg (vedi encode_reel.sh)."""
import sys, os, math
from pilot_common import *
from cine_lib import render, add_logo
import cine_type as T
from ae_lib import font, ROOT, CY
from PIL import Image, ImageDraw

W, H = 1080, 1920
FPS = 24; DUR = 16.0; NF = int(FPS * DUR)
CUTS = [3.2, 7.2, 11.2, 14.4]
FRAMES = os.environ.get('AEV_FRAMES', '/tmp/aev_reel_frames')


def ease(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def seg(t, a, b): return ease((t - a) / (b - a))


def text_layer(fn, alpha, rise=22):
    """Disegna con fn(layer, dy) su un livello trasparente e applica alpha (dissolvenza + salita)."""
    ly = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    fn(ly, int((1 - alpha) * rise))
    if alpha < 1.0:
        import numpy as np
        a = np.asarray(ly.split()[3]).astype('float32') * alpha
        ly.putalpha(Image.fromarray(a.astype('uint8')))
    return ly


def cut_fade(t):
    """Dissolvenza a nero rapida attorno ai tagli (0.14 s)."""
    f = 1.0
    for c in CUTS:
        d = abs(t - c)
        if d < 0.14: f = min(f, 0.15 + 0.85 * (d / 0.14))
    if t < 0.25: f = min(f, t / 0.25)
    if t > DUR - 0.9: f = min(f, max(0.0, (DUR - t) / 0.9))
    return f


def brt():
    lg = Image.open(ROOT + '/assets/brt_logo.png').convert('RGBA')
    return lg


def frame(i):
    t = i / FPS
    f = cut_fade(t)
    an = dict(drift=t * 40, fade=f, grain=1000 + i)
    if t < CUTS[0]:                                         # ---- 1 apertura: logo
        p = t / CUTS[0]
        an['sweep'] = -0.5 + p
        im = render(W, H, [], palette='cyan', base_y=0.80, seed=3, logo=False, anim=an).convert('RGBA')
        la = seg(t, 0.35, 1.5)
        im = add_logo(im, W, H, 0.66, 0.32 + (1 - la) * 0.012, alpha=la)
        sa = seg(t, 1.7, 2.3)
        if sa > 0:
            im.alpha_composite(text_layer(lambda ly, dy: T.block(ly, 0, 1050 + dy, kicker='Oli e lubrificanti', align='c', subsize=34, kcol=T.WHITE), sa))
    elif t < CUTS[1]:                                       # ---- 2 prodotto Castrol
        p = (t - CUTS[0]) / (CUTS[1] - CUTS[0])
        an['sweep'] = -0.2 + 0.4 * p; an['spec_x'] = 0.12 + 0.76 * ease(p)
        hgt = 0.40 + 0.075 * ease(p)
        im = render(W, H, ['castrol_edge_ll3_5w30'], palette='cyan', heights=[hgt], xs=[0.5 - 0.01 * p], cx=0.5, base_y=0.80,
                    seed=3, logo=False, anim=an).convert('RGBA')
        im = add_logo(im, W, H, 0.26, 0.145, alpha=1.0)
        a1 = seg(t, CUTS[0] + 0.5, CUTS[0] + 1.0); a2 = seg(t, CUTS[0] + 0.9, CUTS[0] + 1.5)
        if a1 > 0: im.alpha_composite(text_layer(lambda ly, dy: T.block(ly, 0, 505 + dy, kicker='Castrol EDGE 5W-30', align='c', subsize=34), a1))
        if a2 > 0: im.alpha_composite(text_layer(lambda ly, dy: T.block(ly, 0, 575 + dy, lines=['Prima la sigla.'], align='c', size=86), a2))
    elif t < CUTS[2]:                                       # ---- 3 tre marchi, carrellata
        p = (t - CUTS[1]) / (CUTS[2] - CUTS[1])
        an['sweep'] = 0.2 - 0.4 * p
        sh = 0.045 * ease(p)
        im = render(W, H, ['selenia_wr_pure_energy_5w30', 'castrol_edge_ll3_5w30', 'mobil1_esp_5w30'], palette='violet',
                    heights=[0.31, 0.37, 0.31], xs=[0.22 - sh * 0.6, 0.50 - sh * 1.0, 0.78 - sh * 1.4], base_y=0.80, seed=11, light='right',
                    logo=False, anim=an).convert('RGBA')
        im = add_logo(im, W, H, 0.26, 0.145)
        a1 = seg(t, CUTS[1] + 0.4, CUTS[1] + 0.95); a2 = seg(t, CUTS[1] + 0.8, CUTS[1] + 1.4)
        if a1 > 0: im.alpha_composite(text_layer(lambda ly, dy: T.block(ly, 0, 480 + dy, lines=['Marchi che conosci.'], align='c', size=72), a1))
        if a2 > 0: im.alpha_composite(text_layer(lambda ly, dy: T.block(ly, 0, 590 + dy, sub='La specifica giusta, controllata sul libretto.', maxw=860, subsize=34, align='c'), a2))
    elif t < CUTS[3]:                                       # ---- 4 servizio
        p = (t - CUTS[2]) / (CUTS[3] - CUTS[2])
        an['sweep'] = -0.15 + 0.3 * p
        im = render(W, H, ['mannol_longlife_504_507'], palette='amber', heights=[0.26], xs=[0.5], cx=0.5, base_y=0.80, seed=21,
                    logo=False, anim=an).convert('RGBA')
        im = add_logo(im, W, H, 0.26, 0.145)
        rows = [('Spedizione gratuita', 'in Italia · 24/48 ore', True), ('Reso', 'entro 14 giorni', False), ('Assistenza', 'lun-ven · 9:00-18:00', False)]
        for k, (a, b, has_brt) in enumerate(rows):
            al = seg(t, CUTS[2] + 0.35 + 0.45 * k, CUTS[2] + 0.85 + 0.45 * k)
            if al <= 0: continue
            y0 = 470 + k * 138

            def draw(ly, dy, a=a, b=b, y0=y0, has_brt=has_brt):
                d = ImageDraw.Draw(ly)
                d.rounded_rectangle([90, y0 + dy, 990, y0 + dy + 118], radius=30, fill=(6, 20, 34, 205), outline=CY + (230,), width=2)
                T.shadow_text(ly, (130, y0 + dy + 18), a, font('Bold', 40), T.WHITE, blur=6, alpha=140)
                T.shadow_text(ly, (130, y0 + dy + 66), b, font('Regular', 32), T.SOFT, blur=5, alpha=120)
                if has_brt:
                    lg = brt(); lw = 150; lh = int(lg.height * lw / lg.width); lg = lg.resize((lw, lh), Image.LANCZOS)
                    ly.alpha_composite(lg, (990 - 40 - lw, y0 + dy + 59 - lh // 2))
            im.alpha_composite(text_layer(draw, al, rise=18))
    else:                                                   # ---- 5 chiusura
        p = (t - CUTS[3]) / (DUR - CUTS[3])
        an['sweep'] = 0.0
        im = render(W, H, [], palette='cyan', base_y=0.80, seed=3, logo=False, anim=an).convert('RGBA')
        im = add_logo(im, W, H, 0.62, 0.34)
        a1 = seg(t, CUTS[3] + 0.35, CUTS[3] + 0.8)
        if a1 > 0:
            def draw(ly, dy): T.pill(ly, 0, 1085 + dy, 'Visita il profilo', size=40, align='c')
            im.alpha_composite(text_layer(draw, a1))
        a2 = seg(t, CUTS[3] + 0.6, CUTS[3] + 1.0)
        if a2 > 0: im.alpha_composite(text_layer(lambda ly, dy: T.shadow_text(ly, (W / 2, 1250 + dy), 'autoevostore.it', font('Medium', 36), T.WHITE, blur=8, alpha=200, anchor='mt'), a2))
    return im.convert('RGB')


def run(a, b):
    os.makedirs(FRAMES, exist_ok=True)
    for i in range(a, b):
        p = f'{FRAMES}/{i:04d}.jpg'
        if os.path.exists(p): continue
        frame(i).save(p, 'JPEG', quality=95, subsampling=0)


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'frames'
    if mode == 'frames':
        a = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        b = int(sys.argv[3]) if len(sys.argv) > 3 else NF
        run(a, b)
    elif mode == 'poster':
        os.makedirs(f'{PK}/05_sorgenti/reel_chiave', exist_ok=True)
        for k, tt in enumerate([1.9, 5.4, 9.0, 13.2, 15.2]):
            save_srgb(frame(int(tt * FPS)), f'{PK}/05_sorgenti/reel_chiave/chiave_{k + 1}.png')
    print('done')
