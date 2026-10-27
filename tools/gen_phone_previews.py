"""Anteprime 'in telefono' (approssimate): cornice + interfaccia simulata di feed/carosello/Reel di Instagram.
Servono a controllare tagli, leggibilità e zone occupate dall'interfaccia. La resa reale varia per dispositivo e versione dell'app."""
import math, os
from pilot_common import *
from ae_lib import font, CY, ROOT
from PIL import Image, ImageDraw, ImageFilter

CW, CH = 900, 1800
SX0, SY0, SX1, SY1 = 100, 90, 800, 1710          # schermo 700x1620
SW, SH = SX1 - SX0, SY1 - SY0
WHITE = (245, 247, 250, 255); GREY = (150, 158, 168, 255)


def body():
    im = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([70, 60, 830, 1740], radius=112, fill=(24, 26, 31, 255), outline=(76, 80, 90, 255), width=4)
    d.rounded_rectangle([SX0 - 6, SY0 - 6, SX1 + 6, SY1 + 6], radius=88, fill=(0, 0, 0, 255))
    return im


def screen_mask():
    m = Image.new('L', (SW, SH), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, SW - 1, SH - 1], radius=82, fill=255)
    return m


def heart(d, cx, cy, s, fill=None, outline=WHITE, w=4):
    pts = []
    for k in range(0, 360, 6):
        a = math.radians(k)
        x = 16 * math.sin(a) ** 3
        y = -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))
        pts.append((cx + x * s / 18, cy + y * s / 18))
    d.polygon(pts, fill=fill, outline=outline, width=w) if fill else d.line(pts + [pts[0]], fill=outline, width=w, joint='curve')


def bubble(d, cx, cy, s, w=4):
    d.ellipse([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2], outline=WHITE, width=w)
    d.polygon([(cx - s * 0.30, cy + s * 0.36), (cx - s * 0.62, cy + s * 0.62), (cx - s * 0.05, cy + s * 0.48)], fill=(0, 0, 0, 255), outline=WHITE)


def plane(d, cx, cy, s, w=4):
    d.polygon([(cx - s / 2, cy - s * 0.1), (cx + s / 2, cy - s * 0.5), (cx + s * 0.1, cy + s / 2), (cx - s * 0.05, cy + s * 0.08)], outline=WHITE, width=w)


def bookmark(d, cx, cy, s, w=4):
    d.polygon([(cx - s * 0.32, cy - s / 2), (cx + s * 0.32, cy - s / 2), (cx + s * 0.32, cy + s / 2), (cx, cy + s * 0.22), (cx - s * 0.32, cy + s / 2)], outline=WHITE, width=w)


def status_bar(d, y=18):
    d.text((44, y), '9:41', font=font('Medium', 26), fill=WHITE)
    d.rounded_rectangle([SW - 96, y + 6, SW - 52, y + 28], radius=7, outline=WHITE, width=3)
    d.rectangle([SW - 91, y + 11, SW - 62, y + 23], fill=WHITE)
    for k in range(4):
        d.rectangle([SW - 168 + k * 12, y + 24 - 6 - k * 4, SW - 160 + k * 12, y + 24], fill=WHITE)


def avatar(size):
    lg = Image.open(ROOT + '/assets/logo.png').convert('RGBA')
    bg = Image.new('RGBA', lg.size, (10, 20, 34, 255)); bg.alpha_composite(lg)
    w, h = bg.size; s = min(w, h)
    c = bg.crop(((w - s) // 2, (h - s) // 2 - 60, (w + s) // 2, (h + s) // 2 - 60)).resize((size, size), Image.LANCZOS)
    m = Image.new('L', (size, size), 0); ImageDraw.Draw(m).ellipse([0, 0, size - 1, size - 1], fill=255)
    c.putalpha(m); return c


def nav(d):
    y = SH - 70
    d.line([0, y - 18, SW, y - 18], fill=(40, 42, 48, 255), width=2)
    xs = [SW * (k + 0.5) / 5 for k in range(5)]
    d.polygon([(xs[0] - 17, y + 6), (xs[0], y - 12), (xs[0] + 17, y + 6), (xs[0] + 17, y + 22), (xs[0] - 17, y + 22)], outline=WHITE, width=3)
    d.ellipse([xs[1] - 13, y - 12, xs[1] + 11, y + 12], outline=WHITE, width=3); d.line([xs[1] + 8, y + 9, xs[1] + 20, y + 21], fill=WHITE, width=3)
    d.rounded_rectangle([xs[2] - 18, y - 14, xs[2] + 18, y + 22], radius=8, outline=WHITE, width=3); d.line([xs[2], y - 4, xs[2], y + 12], fill=WHITE, width=3); d.line([xs[2] - 8, y + 4, xs[2] + 8, y + 4], fill=WHITE, width=3)
    d.rounded_rectangle([xs[3] - 18, y - 14, xs[3] + 18, y + 22], radius=8, outline=WHITE, width=3); d.polygon([(xs[3] - 5, y - 2), (xs[3] - 5, y + 14), (xs[3] + 9, y + 6)], fill=WHITE)
    d.ellipse([xs[4] - 16, y - 12, xs[4] + 16, y + 20], outline=WHITE, width=3)


def wrap_lines(d, txt, f, maxw, maxlines):
    out, cur = [], ''
    for w in txt.replace('\n', ' \n ').split(' '):
        if w == '\n':
            out.append(cur); cur = ''; continue
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: out.append(cur); cur = w
        if len(out) >= maxlines: break
    if cur and len(out) < maxlines: out.append(cur)
    return out[:maxlines]


def feed_phone(img, caption, carousel_n=0, idx=0, name='autoevostore'):
    scr = Image.new('RGBA', (SW, SH), (0, 0, 0, 255)); d = ImageDraw.Draw(scr)
    status_bar(d)
    d.text((28, 78), 'Instagram', font=font('Bold', 36), fill=WHITE)
    heart(d, SW - 100, 98, 30); plane(d, SW - 44, 98, 30, w=3)
    scr.alpha_composite(avatar(58), (22, 142)); d.text((92, 148), name, font=font('Medium', 26), fill=WHITE); d.text((92, 180), 'Italia', font=font('Regular', 20), fill=GREY)
    d.text((SW - 58, 146), '···', font=font('Bold', 34), fill=WHITE)
    ih = int(SW * 1350 / 1080); y0 = 222
    scr.paste(img.convert('RGB').resize((SW, ih), Image.LANCZOS), (0, y0))
    if carousel_n:
        d.rounded_rectangle([SW - 96, y0 + 18, SW - 18, y0 + 56], radius=19, fill=(20, 20, 20, 190))
        d.text((SW - 57, y0 + 37), f'{idx + 1}/{carousel_n}', font=font('Medium', 22), fill=WHITE, anchor='mm')
    y = y0 + ih + 30
    heart(d, 44, y + 16, 34); bubble(d, 112, y + 16, 34); plane(d, 178, y + 16, 34); bookmark(d, SW - 38, y + 16, 34)
    if carousel_n:
        for k in range(carousel_n):
            r = 5 if k == idx else 4
            c = (60, 160, 255, 255) if k == idx else (110, 114, 120, 255)
            d.ellipse([SW / 2 - (carousel_n - 1) * 12 + k * 24 - r, y + 16 - r, SW / 2 - (carousel_n - 1) * 12 + k * 24 + r, y + 16 + r], fill=c)
    y += 62
    f = font('Regular', 24); fb = font('Medium', 24)
    d.text((24, y), name, font=fb, fill=WHITE)
    x = 24 + d.textlength(name + ' ', font=fb)
    words = caption.replace('\n', ' ').split(); lines = []; cur = ''; lim = SW - 24 - x
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= lim: cur = t
        else:
            lines.append(cur); cur = w; lim = SW - 48
    lines.append(cur)
    d.text((x, y), lines[0], font=f, fill=WHITE)
    d.text((24, y + 34), lines[1] if len(lines) > 1 else '', font=f, fill=WHITE)
    d.text((24, y + 68), '\u2026 altro', font=f, fill=GREY)
    nav(d)
    return scr


def place(scr):
    ph = body(); m = screen_mask(); ph.paste(scr, (SX0, SY0), m)
    d = ImageDraw.Draw(ph); d.rounded_rectangle([CW / 2 - 62, SY0 + 22, CW / 2 + 62, SY0 + 58], radius=18, fill=(0, 0, 0, 255))
    return ph


def reel_ui(caption, zones=False, name='autoevostore'):
    ov = Image.new('RGBA', (SW, SH), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    vh = int(SW * 16 / 9); vy = (SH - vh) // 2          # area video 9:16 contenuta nello schermo
    # gradienti per leggibilità dell'interfaccia
    g = Image.new('RGBA', (SW, 260), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    for k in range(260): gd.line([0, k, SW, k], fill=(0, 0, 0, int(150 * (1 - k / 260) ** 1.6)))
    ov.alpha_composite(g, (0, vy)); ov.alpha_composite(g.transpose(Image.FLIP_TOP_BOTTOM), (0, vy + vh - 330))
    d = ImageDraw.Draw(ov)
    status_bar(d)
    d.text((28, 78), 'Reels', font=font('Bold', 36), fill=WHITE)
    # colonna azioni a destra
    x = SW - 56
    for k, fn in enumerate((heart, bubble, plane)):
        cy = vy + vh - 560 + k * 118
        fn(d, x, cy, 40)
        d.text((x, cy + 40), '•••', font=font('Medium', 18), fill=WHITE, anchor='mm')
    d.text((x, vy + vh - 560 + 3 * 118 + 6), '···', font=font('Bold', 40), fill=WHITE, anchor='mm')
    # blocco in basso
    y = vy + vh - 250
    ov.alpha_composite(avatar(56), (24, y)); d.text((94, y + 6), name, font=font('Medium', 26), fill=WHITE)
    d.rounded_rectangle([94 + d.textlength(name, font=font('Medium', 26)) + 18, y + 4, 94 + d.textlength(name, font=font('Medium', 26)) + 112, y + 44], radius=10, outline=WHITE, width=2)
    d.text((94 + d.textlength(name, font=font('Medium', 26)) + 65, y + 24), 'Segui', font=font('Medium', 20), fill=WHITE, anchor='mm')
    for k, ln in enumerate(wrap_lines(d, caption.replace('\n', ' '), font('Regular', 24), SW - 130, 2)):
        d.text((24, y + 74 + k * 32), ln, font=font('Regular', 24), fill=WHITE)
    d.text((24, y + 150), 'Audio originale \u00b7 autoevostore', font=font('Regular', 22), fill=(220, 224, 230, 255))
    nav(d)
    if zones:  # zone da non usare per testi (stima): alto 14%, basso 20%, destra 12%
        z = Image.new('RGBA', (SW, SH), (0, 0, 0, 0)); zd = ImageDraw.Draw(z); red = (255, 60, 60, 70)
        zd.rectangle([0, vy, SW, vy + int(vh * 0.14)], fill=red); zd.rectangle([0, vy + int(vh * 0.80), SW, vy + vh], fill=red)
        zd.rectangle([int(SW * 0.88), vy, SW, vy + vh], fill=red)
        ov.alpha_composite(z)
    return ov, vy, vh


def reel_phone(frame, caption, zones=False):
    scr = Image.new('RGBA', (SW, SH), (0, 0, 0, 255))
    ov, vy, vh = reel_ui(caption, zones)
    scr.paste(frame.convert('RGB').resize((SW, vh), Image.LANCZOS), (0, vy))
    scr.alpha_composite(ov)
    return scr


def montage(phones, path, scale=0.62, gap=10, bg=(14, 18, 26, 255)):
    w = int(CW * scale); h = int(CH * scale)
    out = Image.new('RGBA', (len(phones) * (w + gap) + gap, h + 2 * gap), bg)
    for k, ph in enumerate(phones):
        out.alpha_composite(ph.resize((w, h), Image.LANCZOS), (gap + k * (w + gap), gap))
    out.convert('RGB').save(path)


if __name__ == '__main__':
    import sys, glob
    OUTD = f'{PK}/06_anteprime_telefono'
    os.makedirs(OUTD, exist_ok=True)
    cap_c = ('Prima la sigla, poi l\u2019olio. Castrol EDGE LongLife III 5W-30 \u00e8 indicato nella scheda con ACEA C3, '
             'VW 504.00/507.00, MB 229.52. Controlla il libretto e scopri la scheda dal link nel profilo.')
    cap_k = ('Non scegliere l\u2019olio dalla sola viscosit\u00e0. Tre controlli da fare sul libretto: viscosit\u00e0, categoria ACEA, '
             'omologazione del costruttore. Devono coincidere tutte e tre. Salva la guida per il prossimo tagliando.')
    cap_r = ('AUTO EVO STORE: oli e lubrificanti Castrol, Mobil, Selenia e MANNOL, con la specifica controllata sul libretto. '
             'Visita il profilo e scopri il catalogo.')
    p = f'{PK}/01_castrol/AEV_castrol-edge-ll3_feed_v1_1080x1350.png'
    place(feed_phone(Image.open(p), cap_c)).save(f'{OUTD}/castrol_feed_telefono_v1.png')
    ph = []
    for k in range(1, 6):
        im = Image.open(f'{PK}/02_carosello/AEV_carosello-scelta-olio_s{k}_v1_1080x1350.png')
        t = place(feed_phone(im, cap_k, carousel_n=5, idx=k - 1)); ph.append(t)
        t.save(f'{OUTD}/carosello_s{k}_telefono_v1.png')
    montage(ph, f'{OUTD}/carosello_5slide_montaggio_telefono_v1.jpg', scale=0.5)
    rp = []
    for k in range(1, 6):
        fr = Image.open(f'{PK}/05_sorgenti/reel_chiave/chiave_{k}.png')
        t = place(reel_phone(fr, cap_r)); rp.append(t); t.save(f'{OUTD}/reel_chiave{k}_telefono_v1.png')
        if k in (2, 5): place(reel_phone(fr, cap_r, zones=True)).save(f'{OUTD}/reel_chiave{k}_zone-interfaccia_v1.png')
    montage(rp, f'{OUTD}/reel_5inquadrature_montaggio_telefono_v1.jpg', scale=0.5)
    print('ok')
