"""Reel di SERIE (educativi / fiducia) nello stesso stile dei Reel prodotto: 1080x1920, 24 fps, 13 s.
Struttura: 0-2 s gancio (macro etichetta) | 3 scene da 2,6 s (un flacone + una sigla grande) | 9,8-13 chiusura CTA.
Sigle SOLO da titolo/tag Shopify. Uso: python3 tools/reel_serie.py [chiave ...]"""
import os, sys, subprocess, shutil
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from cine_lib import render, add_logo
import cine_type as T
from ae_lib import font, ROOT, CY
from pilot_common import fit_size
from reel_prodotto import crop_resize, layer, comp, ease, seg, darken, top_grad, AUDIO, W, H, FPS

OUT = ROOT + '/media/reels-serie'
CUT = [2.0, 4.6, 7.2, 9.8, 13.0]; DUR = CUT[-1]; NF = int(DUR * FPS)

# chiave: gancio, [(foto, palette, kicker, grande, piccolo, brt)], chiusura (righe), sottotitolo chiusura
S = {
 'c2_c3': (['ACEA C2', 'o C3?'], [
     ('selenia_wr_forward_0w30', 'violet', 'Selenia WR Forward 0W-30', 'ACEA C2', 'FIAT 9.55535-DS1 / DH1', False),
     ('castrol_edge_ll3_5w30', 'cyan', 'Castrol EDGE LongLife III 5W-30', 'ACEA C3', 'VW 504.00 / 507.00', False),
     ('castrol_edge_0w20_c5', 'amber', 'Castrol EDGE 0W-20 C5', 'ACEA C5 / C6', 'dexos1 Gen 3 · MB 229.71', False)],
     ['Categorie diverse.', 'Il libretto decide.'], 'Targa, modello e anno in DM: verifichiamo noi.'),
 'non_solo_motore': (['Non è tutto', 'olio motore.'], [
     ('castrol_transmax_axle_80w90', 'amber', 'Castrol Transmax Axle EPX 80W-90', 'Differenziale', 'API GL-5', False),
     ('mannol_atf_dexron3', 'violet', 'Mannol Automatic Plus ATF', 'Cambio automatico', 'Dexron III · servosterzo', False),
     ('castrol_power1_2t', 'cyan', 'Castrol Power 1 Ultimate 2T', 'Moto 2 tempi', '100% sintetico', False)],
     ['Ogni componente', 'ha il suo olio.'], 'Dimmi cosa devi lubrificare: ti indichiamo la specifica.'),
 'stesso_5w30': (['Stesso 5W-30.', 'Sigle diverse.'], [
     ('petronas_xs_5w30', 'cyan', 'Petronas Syntium Prime XS 5W-30', 'dexos2', 'ACEA C3', False),
     ('mannol_longlife_504_507', 'violet', 'Mannol Longlife 504/507 5W-30', 'VW 504.00 / 507.00', 'ACEA C3 · Porsche C30', False),
     ('castrol_magnatec_5w30_a5', 'amber', 'Castrol Magnatec A5 5W-30', 'Ford WSS-M2C913', 'ACEA A5/B5', False)],
     ['La viscosità', 'non basta.'], 'Conta l’omologazione del costruttore.'),
 'magazzino': (['Ordini oggi.', 'Quando arriva?'], [
     ('mobil1_esp_5w30', 'cyan', 'Spedizione gratuita in Italia', '24/48 ore', 'con corriere BRT', True),
     ('castrol_edge_td_5w40', 'amber', 'Europa', '3-7 giorni', 'lavorativi · escluse Cipro e Malta', False),
     ('total_ineo_mc3', 'violet', 'Acquista sereno', 'Reso 14 giorni', 'assistenza lun-ven 9:00-18:00', False)],
     ['Dal nostro magazzino', 'a casa tua.'], 'Oli e lubrificanti selezionati su autoevostore.it'),
 'stesso_5w40': (['Stesso 5W-40.', 'Sigle diverse.'], [
     ('castrol_edge_td_5w40', 'amber', 'Castrol EDGE Turbo Diesel 5W-40', 'VW 505.01', 'ACEA C3 · FIAT 9.55535-S2', False),
     ('petronas_prime_av', 'violet', 'Petronas Syntium Prime AV 5W-40', 'MB 229.51', 'ACEA C3 · VW 505.01', False),
     ('selenia_multipower_gas', 'cyan', 'Selenia Multipower Gas 5W-40', 'FIAT 9.55535-T2', 'GPL / Metano · ACEA C3', False)],
     ['La viscosità', 'non basta.'], 'Conta l’omologazione del costruttore.'),
}


def build(key):
    hook, scenes, close, close_sub = S[key]
    seed = sum(map(ord, key)) % 89
    A = np.asarray(render(1620, 2880, [scenes[0][0]], palette=scenes[0][1], heights=[0.50], xs=[0.5], cx=0.5, base_y=0.88,
                          logo=False, seed=seed).convert('RGB'))
    plates = []
    for k, (foto, pal, *_r) in enumerate(scenes):
        right = k % 2 == 0
        plates.append(np.asarray(render(1242, 2208, [foto], palette=pal, heights=[0.48], xs=[0.70 if right else 0.30],
                                        cx=0.70 if right else 0.30, base_y=0.86, light='right' if right else 'left',
                                        logo=False, seed=seed + 5 * k).convert('RGB')))
    L = np.asarray(render(1242, 2208, [s[0] for s in scenes], palette='cyan', heights=[0.30, 0.34, 0.30],
                          xs=[0.24, 0.50, 0.76], base_y=0.80, logo=False, seed=seed + 31).convert('RGB'))
    CL = [cv2.GaussianBlur(darken(crop_resize(L, 0.5, 0.5, 1.0 - 0.04 * q / 10), 0.50), (0, 0), 10) for q in range(10)]

    L_hook = layer(lambda ly: T.block(ly, 0, 300, lines=hook, align='c', size=100))
    brt = Image.open(ROOT + '/assets/brt_logo.png').convert('RGBA')
    LS = []
    for k, (foto, pal, kick, big, small, hb) in enumerate(scenes):
        right = k % 2 == 0; x = 70 if right else 520
        def draw(ly, kick=kick, big=big, small=small, x=x, hb=hb):
            fs = fit_size(big.split('\n'), 470, 92, minsize=48)
            y = T.block(ly, x, 560, kicker=f'{k + 1}/3', lines=[], subsize=34)
            y = T.block(ly, x, 620, lines=big.split('\n'), size=fs)
            T.block(ly, x, y + 10, sub=f'{kick}\n{small}', maxw=480, subsize=32)
            if hb:
                bw = 190; lg = brt.resize((bw, int(brt.height * bw / brt.width)), Image.LANCZOS)
                bg = Image.new('RGBA', (bw + 28, lg.height + 20), (255, 255, 255, 255)); bg.alpha_composite(lg, (14, 10))
                ly.alpha_composite(bg, (x, 1040))
        LS.append(layer(draw))
    L_c1 = layer(lambda ly: T.block(ly, 0, 900, lines=close, align='c', size=82))
    L_c2 = layer(lambda ly: T.block(ly, 0, 1130, sub=close_sub, align='c', subsize=34, maxw=900))
    L_c3 = layer(lambda ly: T.pill(ly, 0, 1250, 'Link in bio · autoevostore.it', size=36, align='c'))

    def frame(i):
        t = i / FPS
        if t < CUT[0]:
            p = t / CUT[0]
            im = Image.fromarray(top_grad(crop_resize(A, 0.5, 0.64, 0.46 + 0.10 * ease(p)))).convert('RGBA')
            comp(im, L_hook, 1.0, rise=0)
        elif t < CUT[3]:
            k = 0 if t < CUT[1] else (1 if t < CUT[2] else 2)
            t0 = CUT[k]; p = (t - t0) / (CUT[k + 1] - t0)
            im = Image.fromarray(crop_resize(plates[k], 0.5 + (0.02 if k % 2 == 0 else -0.02) * p, 0.5, 1.0 - 0.06 * ease(p))).convert('RGBA')
            im = add_logo(im, W, H, 0.26, 0.05)
            comp(im, LS[k], seg(t, t0 + 0.08, t0 + 0.5), rise=30)
        else:
            p = (t - CUT[3]) / (DUR - CUT[3])
            im = Image.fromarray(CL[min(9, int(p * 10))]).convert('RGBA')
            im = add_logo(im, W, H, 0.50, 0.20)
            comp(im, L_c1, seg(t, CUT[3] + 0.1, CUT[3] + 0.5)); comp(im, L_c2, seg(t, CUT[3] + 0.4, CUT[3] + 0.8))
            comp(im, L_c3, seg(t, CUT[3] + 0.6, CUT[3] + 1.0))
        f = 1.0
        for c in CUT[:-1]:
            d = abs(t - c)
            if d < 0.10: f = min(f, 0.25 + 0.75 * d / 0.10)
        if t > DUR - 0.5: f = min(f, (DUR - t) / 0.5)
        rgb = np.asarray(im.convert('RGB'))
        return rgb if f >= 1 else (rgb.astype(np.float32) * f).astype(np.uint8)

    tmp = f'/tmp/rs_{key}'; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    for i in range(NF):
        cv2.imwrite(f'{tmp}/{i:04d}.jpg', cv2.cvtColor(frame(i), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 93])
    os.makedirs(OUT, exist_ok=True)
    mp4 = f'{OUT}/{key}.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{tmp}/%04d.jpg', '-i', AUDIO,
                    '-t', str(DUR), '-af', f'afade=t=out:st={DUR - 1.2}:d=1.2', '-c:v', 'libx264', '-preset', 'medium', '-crf', '21',
                    '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', mp4], check=True)
    Image.open(f'{tmp}/{int(1.0 * FPS):04d}.jpg').save(f'{OUT}/{key}.jpg', quality=92)
    shutil.rmtree(tmp)
    return mp4


if __name__ == '__main__':
    for k in (sys.argv[1:] or list(S)):
        print(build(k), flush=True)
