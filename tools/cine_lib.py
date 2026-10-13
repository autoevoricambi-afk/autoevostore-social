"""Motore 'cinematografico' per le pubblicità: flaconi REALI (products/*.png) in una scena illuminata
(luce volumetrica, pavimento lucido con riflesso, bokeh, bloom, grana). Niente scritte sovrapposte:
solo il logo del brand. Parametri di scena: palette, posizione, altezza, seed."""
import os, numpy as np, cv2
from PIL import Image
from ae_lib import ROOT

PR = ROOT + '/products'
PALETTES = {
    # accent = luce principale, accent2 = controluce, warm = riflesso caldo (olio)
    'cyan':   dict(accent=(0.10, 0.80, 0.98), accent2=(1.00, 0.52, 0.16), warm=(1.00, 0.72, 0.30)),
    'violet': dict(accent=(0.60, 0.35, 1.00), accent2=(0.10, 0.75, 0.95), warm=(1.00, 0.55, 0.35)),
    'amber':  dict(accent=(1.00, 0.66, 0.22), accent2=(0.10, 0.70, 0.95), warm=(1.00, 0.80, 0.45)),
}


def _fbm(h, w, seed, octaves=5, base=3):
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32); amp = 1.0; tot = 0
    for o in range(octaves):
        s = base * 2 ** o
        n = rng.random((max(2, int(s * h / w)), s)).astype(np.float32)
        out += amp * cv2.resize(n, (w, h), interpolation=cv2.INTER_CUBIC); tot += amp; amp *= 0.5
    out /= tot
    return (out - out.min()) / (out.max() - out.min() + 1e-6)


def _radial(h, w, cx, cy, rx, ry, p=2.0):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    d = (np.abs((x - cx) / rx) ** p + np.abs((y - cy) / ry) ** p) ** (1.0 / p)
    return np.exp(-d * d * 2.2).astype(np.float32)


def _blur(a, s):
    if s < 0.5: return a
    k = int(s * 6) | 1
    return cv2.GaussianBlur(a, (k, k), s)


def _bottle(key, h):
    im = Image.open(f'{PR}/{key}.png').convert('RGBA')
    im = im.resize((max(2, int(im.width * h / im.height)), int(h)), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255.0
    return a  # h,w,4 (non premoltiplicato)


def _paste(dst, src_rgb, src_a, x, y, mode='over', gain=1.0):
    """dst float HxWx3. src_rgb hxwx3, src_a hxw (0..1). Ritaglia ai bordi."""
    H, W = dst.shape[:2]; h, w = src_a.shape
    x0, y0 = max(0, x), max(0, y); x1, y1 = min(W, x + w), min(H, y + h)
    if x0 >= x1 or y0 >= y1: return
    sa = src_a[y0 - y:y1 - y, x0 - x:x1 - x] * gain
    sr = src_rgb[y0 - y:y1 - y, x0 - x:x1 - x]
    d = dst[y0:y1, x0:x1]
    if mode == 'over': d[:] = d * (1 - sa[..., None]) + sr * sa[..., None]
    else: d[:] = 1 - (1 - d) * (1 - sr * sa[..., None])  # screen


def render(W, H, keys, palette='cyan', seed=3, cx=0.5, heights=None, xs=None, base_y=0.82,
           logo_w=0.30, logo_top=0.03, tag=None, light='left', mood=1.0, depth_blur=True):
    """keys: lista di prodotti (1 = eroe, più = gruppo). heights: altezza in frazione di H per ciascuno.
    xs: centri x in frazione di W. Restituisce PIL RGB."""
    P = PALETTES[palette]; ac = np.array(P['accent'], np.float32); ac2 = np.array(P['accent2'], np.float32)
    wm = np.array(P['warm'], np.float32)
    sgn = 1 if light == 'left' else -1
    hz = int(H * (base_y - 0.075)); yb = int(H * base_y)   # orizzonte e linea di appoggio
    heights = heights or [0.60] * len(keys)
    xs = xs or ([cx] * len(keys))

    # ---------- sfondo: gradiente + bagliore dietro il prodotto
    ys = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    top = np.array((0.006, 0.012, 0.028), np.float32); mid = np.array((0.012, 0.030, 0.052), np.float32)
    bg = top * (1 - ys) + mid * ys
    bg = np.broadcast_to(bg, (H, W, 3)).copy()
    gx = np.mean(xs) * W
    bg += _radial(H, W, gx, H * 0.50, W * 0.60, H * 0.34)[..., None] * ac * 0.34 * mood
    bg += _radial(H, W, gx + sgn * W * 0.38, H * 0.30, W * 0.30, H * 0.20)[..., None] * ac2 * 0.22 * mood

    # ---------- fasci di luce volumetrica (da un lato) modulati da foschia
    cone = np.zeros((H, W), np.float32)
    src = np.array([[-0.05 * W if sgn > 0 else 1.05 * W, -0.06 * H]])
    spread = 0.30 * W
    poly = np.array([[src[0][0] - sgn * 0.02 * W, -0.08 * H], [src[0][0] + sgn * 0.20 * W, -0.08 * H],
                     [gx + sgn * spread, yb + 0.02 * H], [gx - sgn * spread * 0.2, yb + 0.02 * H]], np.int32)
    cv2.fillPoly(cone, [poly], 1.0)
    cone = _blur(cone, W * 0.028)
    haze = _fbm(H, W, seed + 11, 5, 3)
    cone *= 0.35 + 1.1 * haze
    bg += cone[..., None] * np.array((0.80, 0.95, 1.0), np.float32) * 0.30 * mood
    # nebbiolina bassa vicino all'orizzonte
    band = _radial(H, W, W * 0.5, hz, W * 0.9, H * 0.10)
    bg += (band * (0.5 + haze))[..., None] * ac * 0.12 * mood

    # ---------- bokeh (profondità): dischi sfocati sopra l'orizzonte
    rng = np.random.default_rng(seed)
    bok = np.zeros((H, W, 3), np.float32)
    for _ in range(16):
        x = rng.uniform(0, W); y = rng.uniform(0.30 * H, hz * 0.97); r = rng.uniform(14, 46)
        col = [ac, ac, ac2, np.array((0.9, 0.97, 1), np.float32), wm][rng.integers(0, 5)] * rng.uniform(0.05, 0.16)
        cv2.circle(bok, (int(x), int(y)), int(r), tuple(float(c) for c in col), -1, cv2.LINE_AA)
    bok = _blur(bok, 5.5)
    bg += bok * mood
    # coppia di fari lontani all'orizzonte
    far = np.zeros((H, W, 3), np.float32)
    for dx in (-0.10, 0.10):
        cv2.circle(far, (int(gx + dx * W + (0.30 * sgn * W)), int(hz - 0.012 * H)), 12, (1, 1, 1), -1, cv2.LINE_AA)
    bg += _blur(far, 9) * 0.5 * mood

    # ---------- pavimento lucido
    fl = np.zeros((H, W, 3), np.float32)
    fy = np.clip((np.arange(H, dtype=np.float32) - hz) / max(1, H - hz), 0, 1)[:, None]
    floor_base = (np.array((0.008, 0.016, 0.030), np.float32) * (1 - fy[..., None])
                  + np.array((0.003, 0.006, 0.012), np.float32) * fy[..., None])
    fl += np.broadcast_to(floor_base, (H, W, 3))
    gloss = _fbm(max(8, (H - hz) // 6), W // 2, seed + 5, 5, 6)
    gloss = cv2.resize(gloss, (W, H - hz), interpolation=cv2.INTER_CUBIC)
    gl = np.zeros((H, W), np.float32); gl[hz:] = gloss
    pool = _radial(H, W, gx, yb + 0.012 * H, W * 0.62, H * 0.095)
    fl += (pool * (0.45 + 0.9 * gl))[..., None] * (ac * 0.75 + 0.14)
    fl += (_radial(H, W, gx + sgn * W * 0.22, yb + 0.03 * H, W * 0.30, H * 0.05) * gl)[..., None] * wm * 0.12
    mask_floor = np.zeros((H, W), np.float32); mask_floor[hz:] = 1; mask_floor = _blur(mask_floor, 2.5)
    img = bg * (1 - mask_floor[..., None]) + (fl + bg * 0.15) * mask_floor[..., None]
    # linea d'orizzonte luminosa
    hl = np.zeros((H, W), np.float32); hl[hz, :] = 1.0
    img += _blur(hl, 2.0)[..., None] * ac * 0.10 * mood

    # ---------- geometria prodotti + alone dietro (prima del post)
    items = []
    for i in np.argsort(heights):
        key, hh, xc = keys[i], heights[i], xs[i]
        bh = int(H * hh); b = _bottle(key, bh); bw = b.shape[1]
        ybase = yb - int((0.60 - hh) * H * 0.10) if len(keys) > 1 else yb
        items.append((b, bh, bw, xc, ybase, ybase - bh, int(xc * W - bw / 2)))
        img += _radial(H, W, xc * W, ybase - bh * 0.50, bw * 1.15, bh * 0.58)[..., None] * ac * 0.17 * mood
        img += _radial(H, W, xc * W, ybase - bh * 0.50, bw * 0.50, bh * 0.50)[..., None] * np.array((1, 1, 1), np.float32) * 0.05 * mood

    # ---------- particelle in primo piano / sospese
    pt = np.zeros((H, W, 3), np.float32)
    for _ in range(90):
        x = rng.uniform(0, W); y = rng.uniform(0.05 * H, H * 0.95); r = rng.uniform(0.8, 2.6)
        cv2.circle(pt, (int(x), int(y)), int(np.ceil(r)), (1, 1, 1), -1, cv2.LINE_AA)
    pt = _blur(pt, 0.9) * (0.15 + 0.35 * _fbm(H, W, seed + 21, 3, 4))[..., None]
    img += pt * (ac * 0.7 + 0.3) * 0.9 * mood
    for _ in range(7):  # pochi dischi sfocati in primissimo piano
        x = rng.uniform(0, W); y = rng.uniform(0.55 * H, 0.98 * H); r = rng.uniform(26, 70)
        d = np.zeros((H, W, 3), np.float32)
        cv2.circle(d, (int(x), int(y)), int(r), tuple(float(c) for c in ac * 0.08), -1, cv2.LINE_AA)
        img += _blur(d, 14)

    # ---------- post: bloom, streak anamorfico, aberrazione cromatica, vignetta, grana
    hi = np.clip(img - 0.62, 0, None)
    img += _blur(hi, 30) * 1.4 + _blur(hi, 9) * 0.6
    streak = cv2.GaussianBlur(hi, (0, 0), sigmaX=W * 0.10, sigmaY=2.2)
    img += streak * 1.2 * np.array((0.55, 0.9, 1.0), np.float32)
    # vignetta
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    v = 1 - 0.55 * (((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.48) / (H * 0.78)) ** 2)
    img *= np.clip(v, 0.25, 1)[..., None]
    # tone map + curva cinematografica (nero denso, alte luci morbide)
    img = img / (1 + img * 0.55)
    img = np.clip(img, 0, 1) ** 0.96
    # color grade: ombre blu-teal, alte luci neutre
    lum = img.mean(2, keepdims=True)
    img = img + (1 - lum) ** 3 * np.array((-0.006, 0.004, 0.018), np.float32)
    img = np.clip(img, 0, 1)

    # ---------- prodotti (dal più lontano/piccolo al più vicino)
    for (b, bh, bw, xc, ybase, y, x) in items:
        rgb = b[..., :3]; al = b[..., 3]
        # grading del flacone: contrasto morbido + tinta fredda leggera
        rgb = np.clip((rgb - 0.5) * 1.06 + 0.5, 0, 1)
        # illuminazione: gradiente laterale (luce dal lato) + fondo più scuro
        xs_ = np.linspace(-1, 1, bw, dtype=np.float32)[None, :]
        ys_ = np.linspace(0, 1, bh, dtype=np.float32)[:, None]
        shade = 0.80 + 0.30 * np.clip(-sgn * xs_, -1, 1) + 0.0 * ys_
        shade *= (1.0 - 0.32 * ys_ ** 2.4)
        rgb = rgb * shade[..., None]
        # bordo luce (rim): derivata orizzontale dell'alpha -> colore accent sul lato luce, accent2 sull'altro
        ab = cv2.GaussianBlur(al, (0, 0), 3.0)
        gxl = cv2.Sobel(ab, cv2.CV_32F, 1, 0, ksize=3)
        rim_l = np.clip(-sgn * gxl, 0, None); rim_r = np.clip(sgn * gxl, 0, None)
        edge = np.clip(rim_l, 0, 1)[..., None] * ac * 2.4 + np.clip(rim_r, 0, 1)[..., None] * ac2 * 1.6
        # lama di luce speculare verticale
        sx = (0.30 if sgn > 0 else 0.70)
        spec = np.exp(-((np.linspace(0, 1, bw)[None, :] - sx) / 0.045) ** 2) * (0.35 + 0.65 * (1 - ys_))
        spec = spec * al
        # riflesso sul pavimento
        rh = int(bh * 0.55)
        rf_rgb = np.flipud(rgb)[:rh]; rf_a = np.flipud(al)[:rh]
        fade = (np.linspace(1, 0, rh, dtype=np.float32) ** 1.5)[:, None] * 0.62
        rf_a = rf_a * fade
        rf_rgb = cv2.GaussianBlur(rf_rgb, (0, 0), 2.2)
        rf_a_b = cv2.GaussianBlur(rf_a, (0, 0), 2.0)
        # velo sfocato progressivo: mix di due livelli di blur
        rf_a2 = cv2.GaussianBlur(rf_a, (0, 0), 7.0)
        t = np.linspace(0, 1, rh, dtype=np.float32)[:, None]
        rf_a = rf_a_b * (1 - t) + rf_a2 * t
        rf_rgb = rf_rgb * 0.8 + ac * 0.06
        _paste(img, rf_rgb, rf_a, x, ybase + 2, 'over')
        # ombra a contatto + ombra lunga
        sh = np.zeros((H, W), np.float32)
        cv2.ellipse(sh, (int(xc * W), ybase + 6), (int(bw * 0.56), int(H * 0.012)), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
        sh = _blur(sh, 10)
        long_ = np.zeros((H, W), np.float32)
        cv2.ellipse(long_, (int(xc * W - sgn * bw * 0.9), ybase + 10), (int(bw * 1.15), int(H * 0.010)), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
        long_ = _blur(long_, 22) * 0.55
        img *= (1 - np.clip(sh * 0.85 + long_, 0, 0.92))[..., None]
        # flacone
        _paste(img, np.clip(rgb, 0, 1), al, x, y, 'over')
        # rim e speculare (screen) solo dentro la sagoma
        er = np.clip(edge, 0, 1) * np.clip(ab * 1.5, 0, 1)[..., None]
        _paste(img, er, al, x, y, 'screen', gain=0.9)
        _paste(img, np.dstack([spec] * 3) * np.array((0.9, 0.98, 1.0), np.float32), al, x, y, 'screen', gain=0.55)

    img = np.clip(img, 0, 1)
    img = img * img * (3 - 2 * img) * 0.45 + img * 0.55
    # ---------- finale: bloom lieve sulle alte luci, grana
    lum = img.mean(2, keepdims=True)
    hi = np.clip(img - 0.80, 0, None)
    img = np.clip(img + _blur(hi, 14) * 0.9, 0, 1)
    g = np.random.default_rng(seed + 99).normal(0, 0.012, (H, W, 1)).astype(np.float32)
    img = np.clip(img + g * (0.5 + 0.7 * (1 - lum)), 0, 1)
    out = Image.fromarray((img * 255).astype(np.uint8)).convert('RGBA')

    # ---------- logo del brand (unica scritta) + dominio discreto
    lg = Image.open(ROOT + '/assets/logo.png').convert('RGBA')
    lw = int(W * logo_w); lg = lg.resize((lw, int(lg.height * lw / lg.width)), Image.LANCZOS)
    out.alpha_composite(lg, ((W - lw) // 2, int(H * logo_top)))
    if tag:
        from PIL import ImageDraw
        from ae_lib import font
        d = ImageDraw.Draw(out); f = font('Medium', int(W * 0.030)); t = tag
        w = d.textlength(t, font=f); d.text(((W - w) / 2, H - int(H * 0.045)), t, font=f, fill=(200, 215, 230, 170))
    return out.convert('RGB')
