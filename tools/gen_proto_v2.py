"""Prototipo v2: foto reali in scena + titoli metallici giganti (stile approvato dal titolare)."""
import sys, os
from pilot_common import save_srgb
from cine_lib import render, PR
import cine_type as T
from ae_lib import font, CY, ROOT
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

def grad_text(im, cx, y, txt, size, top=(255,255,255), bot=(150,165,180), glow=None):
    f = font('Bold', size); d = ImageDraw.Draw(im)
    tw = d.textlength(txt, font=f)
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).text((cx - tw/2, y), txt, font=f, fill=255)
    bbox = m.getbbox(); h = bbox[3]-bbox[1]
    sh = Image.new('RGBA', im.size, (0,0,0,0)); sh.putalpha(m.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v*0.8)))
    im.alpha_composite(Image.new('RGBA', im.size, (0,0,0,0)))
    dark = Image.new('RGBA', im.size, (0,0,0,255)); dark.putalpha(m.filter(ImageFilter.GaussianBlur(16)).point(lambda v: int(v*0.75)))
    im.alpha_composite(dark)
    if glow:
        g = Image.new('RGBA', im.size, glow+(255,)); g.putalpha(m.filter(ImageFilter.GaussianBlur(26)).point(lambda v: int(v*0.35)))
        im.alpha_composite(g)
    ys = np.linspace(0, 1, im.height)[:, None]
    arr = np.zeros((im.height, im.width, 4), np.uint8)
    for c in range(3):
        col = np.array(top[c]) * (1 - np.clip((ys - bbox[1]/im.height) / (h/im.height), 0, 1)**1.1) + np.array(bot[c]) * np.clip((ys - bbox[1]/im.height) / (h/im.height), 0, 1)**1.1
        arr[:, :, c] = np.broadcast_to(col, (im.height, im.width)).astype(np.uint8)
    arr[:, :, 3] = 255
    layer = Image.fromarray(arr, 'RGBA'); layer.putalpha(m)
    im.alpha_composite(layer)
    return y + int(size * 1.12)

def cta(im, y, txt):
    T.pill(im, 0, y, txt, size=32, align='c', fill=(6,18,30,215))

def feed_due_oli(W=1080, H=1350):
    p = render(W, H, ['castrol_edge_ll3_5w30', 'mobil1_esp_5w30'], palette='amber', heights=[0.37, 0.37], xs=[0.34, 0.66], cx=0.5, base_y=0.89, logo_w=0.30, seed=11)
    im = p.convert('RGBA')
    y = grad_text(im, W/2, 235, 'DUE OLI.', 140)
    y = grad_text(im, W/2, y - 10, 'UN DUBBIO?', 140, top=(60,230,245), bot=(10,140,170), glow=(20,200,240))
    T.block(im, 0, y + 6, sub='Modello, anno, motorizzazione.\nTi aiutiamo a confrontarli.', maxw=900, subsize=38, align='c')
    cta(im, 1190, 'SCRIVICI IN PRIVATO')
    return im

def feed_casa(W=1080, H=1350):
    p = render(W, H, ['petronas_prime_av'], palette='amber', heights=[0.40], xs=[0.5], cx=0.5, base_y=0.87, logo_w=0.30, seed=5, light='right')
    im = p.convert('RGBA')
    y = grad_text(im, W/2, 235, 'IL TUO OLIO.', 124)
    y = grad_text(im, W/2, y - 10, 'FINO A CASA.', 124, top=(255,190,90), bot=(230,120,30), glow=(255,150,40))
    T.block(im, 0, y + 4, sub='Spedizione gratuita in Italia, 24/48 ore.', maxw=900, subsize=36, align='c')
    brt = Image.open(ROOT + '/assets/brt_logo.png').convert('RGBA'); brt=brt.crop(brt.getbbox()); brt.thumbnail((170, 90))
    pl = Image.new('RGBA', (brt.width + 40, brt.height + 24), (0,0,0,0)); ImageDraw.Draw(pl).rounded_rectangle([0,0,pl.width-1,pl.height-1], radius=18, fill=(255,255,255,240)); pl.alpha_composite(brt, (20, 12))
    im.alpha_composite(pl, (70, 1232))
    T.pill(im, 0, 1235, 'SCOPRI IL CATALOGO', size=30, align='r') if False else None
    d = ImageDraw.Draw(im); f = font('Medium', 30)
    T.pill(im, 560, 1228, 'SCOPRI IL CATALOGO  ›', size=30)
    return im

def story_dubbio(W=1080, H=1920):
    p = render(W, H, ['mannol_longlife_504_507'], palette='violet', heights=[0.30], xs=[0.5], cx=0.5, base_y=0.86, logo_w=0.30, logo_top=0.07, seed=21)
    im = p.convert('RGBA')
    y = grad_text(im, W/2, 400, 'PRIMA', 160)
    y = grad_text(im, W/2, y - 10, 'LA SIGLA.', 160, top=(60,230,245), bot=(10,140,170), glow=(20,200,240))
    T.block(im, 0, y + 6, sub='Controlla il libretto,\npoi scegli l\'olio.', maxw=900, subsize=40, align='c')
    cta(im, 1640, 'TARGA E MODELLO IN DM')
    return im

for name, fn in [('A_due_oli_feed', feed_due_oli), ('B_fino_a_casa_feed', feed_casa), ('C_storia_sigla', story_dubbio)]:
    save_srgb(fn(), f'../media/2026-10/proto/{name}.jpg', jpg=True); print(name)
