"""Tipografia coerente per le creatività cinematografiche (Poppins, dagli assets del repo).
Un solo sistema: kicker ciano spaziato, titolo bianco Bold, testo Regular, CTA a pillola."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from ae_lib import font, CY

WHITE = (246, 249, 252, 255); SOFT = (196, 210, 224, 255)


def _tracked(d, x, y, txt, f, fill, track):
    for ch in txt:
        d.text((x, y), ch, font=f, fill=fill); x += d.textlength(ch, font=f) + track
    return x


def tracked_w(d, txt, f, track):
    return sum(d.textlength(c, font=f) + track for c in txt) - track


def wrap(d, txt, f, maxw):
    out, cur = [], ''
    for w in txt.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: out.append(cur); cur = w
    if cur: out.append(cur)
    return out


def shadow_text(img, xy, txt, f, fill, blur=10, alpha=170, anchor='la'):
    """testo con ombra morbida per staccarlo dal fondo (leggibilità)."""
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((xy[0], xy[1] + 4), txt, font=f, fill=(0, 0, 0, alpha), anchor=anchor)
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))
    ImageDraw.Draw(img).text(xy, txt, font=f, fill=fill, anchor=anchor)


def block(img, x, y, kicker=None, lines=(), sub=None, maxw=520, size=104, subsize=34, align='l', gap=1.04, kcol=CY + (255,)):
    """Blocco di testo: kicker, titolo (righe), sottotitolo. Ritorna y finale."""
    W = img.width; d = ImageDraw.Draw(img)
    if kicker:
        fk = font('Medium', int(subsize * 0.82)); tw = tracked_w(d, kicker.upper(), fk, 5)
        xx = x if align == 'l' else (W - tw) / 2
        sh = Image.new('RGBA', img.size, (0, 0, 0, 0)); _tracked(ImageDraw.Draw(sh), xx, y, kicker.upper(), fk, (0, 0, 0, 190), 5)
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
        _tracked(d, xx, y, kicker.upper(), fk, kcol, 5); y += int(subsize * 1.75)
    f = font('Bold', size)
    for ln in lines:
        tw = d.textlength(ln, font=f)
        xx = x if align == 'l' else (W - tw) / 2
        shadow_text(img, (xx, y), ln, f, WHITE, blur=14, alpha=200); y += int(size * gap * 1.12)
    if sub:
        y += int(subsize * 0.45); fs = font('Regular', subsize)
        for ln in [l for para in sub.split('\n') for l in wrap(d, para, fs, maxw)]:
            tw = d.textlength(ln, font=fs); xx = x if align == 'l' else (W - tw) / 2
            shadow_text(img, (xx, y), ln, fs, SOFT, blur=8, alpha=190); y += int(subsize * 1.42)
    return y


def pill(img, x, y, txt, size=30, align='l', fill=(8, 22, 38, 235), line=CY + (255,), tcol=WHITE):
    d = ImageDraw.Draw(img); f = font('Medium', size)
    tw = d.textlength(txt, font=f); pw = int(tw + size * 2.2); ph = int(size * 2.1)
    if align == 'c': x = (img.width - pw) / 2
    gl = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(gl).rounded_rectangle([x, y, x + pw, y + ph], radius=ph // 2, outline=line[:3] + (150,), width=3)
    img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(7)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x, y, x + pw, y + ph], radius=ph // 2, fill=fill, outline=line, width=2)
    d.text((x + pw / 2, y + ph / 2), txt, font=f, fill=tcol, anchor='mm')
    return y + ph
