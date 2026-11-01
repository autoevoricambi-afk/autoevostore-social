"""Reel PRODOTTO cinematografici (1080x1920, 24 fps, 13 s) — formato del Reel GM dexos2 del 23/10
(il più visto: 126 visualizzazioni IG contro 21-30 degli altri): UN prodotto, foto reale, dettaglio -> intero -> dati.
Struttura: 0-2 s gancio (macro etichetta) | 2-5.2 nome e gradazione | 5.2-8.4 sigle dell'etichetta |
8.4-10.6 servizio (BRT 24/48 h, reso 14 gg) | 10.6-13 CTA DM + link in bio.
Fatti tecnici SOLO da titolo/tag Shopify. Uso: python3 tools/reel_prodotto.py [chiave ...]"""
import os, sys, subprocess, shutil
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from cine_lib import render, add_logo
import cine_type as T
from ae_lib import font, ROOT, CY

W, H, FPS = 1080, 1920, 24
CUT = [2.0, 5.2, 8.4, 10.6, 13.0]; DUR = CUT[-1]; NF = int(DUR * FPS)
OUT = ROOT + '/media/reels-prodotto'
AUDIO = ROOT + '/media/reels-prodotto/_audio_originale.wav'

# key: (foto, palette A, palette B, gancio, kicker, nome (righe), sigle, handle, hashtag)
P = {
 'multipower_gas': ('selenia_multipower_gas', 'cyan', 'amber', ['Viaggi a GPL', 'o metano?'], 'Selenia', ['Multipower Gas', '5W-40'],
                    ['ACEA C3', 'API SP', 'FIAT 9.55535-T2', 'GPL / Metano'], 'selenia-multipower-gas-5w-40-acea-c3-olio-motore-sintetico-per-auto-a-gpl-e-metano', '#gpl #metano #selenia'),
 'digitek_0w30': ('selenia_digitek_0w30', 'violet', 'cyan', ['FIAT 9.55535-GS1', 'sul libretto?'], 'Selenia', ['Digitek Pure Energy', '0W-30'],
                  ['ACEA C2', 'API SN', 'FIAT 9.55535-GS1'], 'selenia-digitek-pure-energy-0w30-acea-c2-fiat-9-55535-gs1', '#selenia #0w30 #fiat'),
 '20k_10w40': ('selenia_20k_10w40', 'amber', 'violet', ['10W-40', 'semisintetico.'], 'Selenia', ['20K', '10W-40'],
               ['ACEA A3/B4', 'FIAT 9.55535-G2', 'FIAT 9.55535-D2'], 'selenia-20k-10w-40-a3-b4-fca-955535-g2-955535-d2-semisintetico', '#selenia #10w40 #fiat'),
 'edge_td': ('castrol_edge_td_5w40', 'amber', 'cyan', ['VW 505.01', 'sul libretto?'], 'Castrol EDGE', ['Turbo Diesel', '5W-40'],
             ['ACEA C3', 'VW 505.00 / 505.01', 'FIAT 9.55535-S2'], 'castrol-edge-5w-40-turbo-diesel-olio-motore-sintetico-acea-c3-vw-505-00-505-01-fiat-9-55535-s2', '#castrol #castroledge #5w40 #diesel'),
 'magnatec_prof_d': ('castrol_magnatec_prof_d_0w30', 'cyan', 'violet', ['Hai una Ford?', 'Cerca la WSS.'], 'Castrol Magnatec', ['Professional D', '0W-30'],
                     ['ACEA C2', 'Ford WSS-M2C950-A'], 'castrol-ford-magnatec-professional-d-0w-30', '#castrol #magnatec #ford #0w30'),
 'wr_forward': ('selenia_wr_forward_0w30', 'violet', 'amber', ['FIAT 9.55535-DS1', 'o DH1?'], 'Selenia WR', ['Forward', '0W-30'],
                ['ACEA C2', 'FIAT 9.55535-DS1', 'FIAT 9.55535-DH1'], 'selenia-wr-forward-0w30-mopar-fiat-955535-ds1-dh1-acea-c2', '#selenia #0w30 #fiat #mopar'),
 'magnatec_a5': ('castrol_magnatec_5w30_a5', 'cyan', 'amber', ['Ford WSS-M2C913', 'sul libretto?'], 'Castrol Magnatec', ['A5', '5W-30'],
                 ['ACEA A5/B5', 'Ford WSS-M2C913'], 'castrol-ford-magnatec-a5-5w-30-a5', '#castrol #magnatec #ford #5w30'),
 'wr_diesel': ('selenia_wr_5w40_diesel', 'amber', 'cyan', ['Diesel FIAT?', 'Leggi N2/N3.'], 'Selenia WR', ['Diesel', '5W-40'],
               ['ACEA A3/B4', 'API SN/CF', 'FIAT 9.55535-N2/N3'], 'selenia-wr-5w40-diesel-fiat-955535-n2-n3-api-sn-acea-a3-b4', '#selenia #diesel #5w40 #fiat'),
 'mannol_ll': ('mannol_longlife_504_507', 'violet', 'cyan', ['Due sigle VW.', 'Un flacone.'], 'Mannol', ['Longlife 504/507', '5W-30'],
               ['ACEA C3', 'VW 504.00 / 507.00', 'Porsche C30'], 'mannol-longlife-5w-30-acea-c3-vw-504-00-507-00-porsche-c30', '#mannol #vw #5w30'),
 'wr_pure': ('selenia_wr_pure_energy_5w30', 'cyan', 'violet', ['Il 5W-30', 'Selenia WR.'], 'Petronas Selenia', ['WR Pure Energy', '5W-30'],
             ['ACEA C2', 'FIAT / Mopar'], 'olio-motore-petronas-selenia-wr-pure-energy-5w30-5l-acea-c3-mopar', '#selenia #5w30 #fiat #mopar'),
 'ineo_mc3': ('total_ineo_mc3', 'amber', 'violet', ['Low SAPS,', 'ACEA C3.'], 'Total Quartz', ['Ineo MC3', '5W-30'],
              ['ACEA C3', 'API SN PLUS', 'Low SAPS'], 'total-quartz-ineo-mc3-5w-30-olio-motore-sintetico-low-saps-acea-c3-api-sn-plus', '#total #totalenergies #5w30'),
 'edge_0w20': ('castrol_edge_0w20_c5', 'violet', 'amber', ['0W-20', 'con dexos1 Gen 3.'], 'Castrol EDGE', ['0W-20 C5'],
               ['ACEA C5 / C6', 'dexos1 Gen 3', 'MB 229.71'], 'castrol-edge-0w-20-c5-olio-motore-acea-c5-c6-dexos1-gen-3-mb-229-71', '#castrol #castroledge #0w20'),
 'petronas_xs': ('petronas_xs_5w30', 'cyan', 'violet', ['dexos2', 'sul libretto?'], 'Petronas Syntium', ['Prime XS', '5W-30'],
                 ['ACEA C3', 'dexos2'], 'petronas-syntium-prime-xs-5w-30-olio-motore-sintetico-acea-c3-dexos2-dexos-d', '#petronas #dexos2 #5w30'),
 'petronas_av': ('petronas_prime_av', 'amber', 'cyan', ['MB 229.51', 'e VW 505.01.'], 'Petronas Syntium', ['Prime AV', '5W-40'],
                 ['ACEA C3', 'MB 229.51', 'VW 505.01'], 'petronas-syntium-prime-av-5w-40-olio-motore-sintetico-acea-c3-mb-229-51-vw-505-01', '#petronas #5w40 #mercedes'),
 'edge_ll3': ('castrol_edge_ll3_5w30', 'cyan', 'amber', ['VW 504.00', 'e 507.00?'], 'Castrol EDGE', ['LongLife III', '5W-30'],
              ['ACEA C3', 'VW 504.00 / 507.00', 'MB 229.52', 'Porsche C30'], 'castrol-edge-longlife-iii-5w-30-olio-motore-originale-vw-audi-seat-skoda-porsche-c30-mb-229-52-acea-c3', '#castrol #castroledge #vw #5w30'),
 'edge_ll_0w30': ('castrol_edge_ll_0w30', 'violet', 'cyan', ['0W-30', 'LongLife.'], 'Castrol EDGE', ['0W-30 LL'],
                  ['ACEA C3', 'VW 504.00 / 507.00'], 'castrol-edge-0w-30-longlife-iii-vw-504-00-507-00-acea-c3', '#castrol #castroledge #0w30 #vw'),
 'mobil1_esp': ('mobil1_esp_5w30', 'cyan', 'violet', ['Tre costruttori.', 'Un flacone.'], 'Mobil 1', ['ESP 5W-30'],
                ['ACEA C3', 'BMW LL-04', 'MB 229.52', 'VW 504 / 507'], 'mobil-1-esp-5w-30-acea-c3-bmw-ll-04-mb-229-52-vw-504-507-psa-rn0710-c30', '#mobil1 #5w30 #bmw'),
 'bmw_ll04': ('bmw_twinpower_ll04_0w30', 'amber', 'cyan', ['Olio originale', 'BMW.'], 'BMW TwinPower Turbo', ['Longlife-04', '0W-30'],
              ['ACEA C3', 'API SN', 'BMW Longlife-04'], 'olio-motore-originale-bmw-twinpower-turbo-longlife-04-0w-30-acea-c3-api-sn', '#bmw #longlife04 #0w30'),
 'transmax': ('castrol_transmax_axle_80w90', 'amber', 'violet', ['Il differenziale', 'ha il suo olio.'], 'Castrol Transmax', ['Axle EPX', '80W-90'],
              ['API GL-5', 'Differenziale'], 'castrol-transmax-axle-epx-80w90-olio-differenziale-trasmissione-api-gl-5-zf', '#castrol #differenziale #80w90'),
 'mannol_8118': ('mannol_8118', 'cyan', 'amber', ['Cambio e', 'differenziale.'], 'Mannol', ['Ultra Gear 8118', '75W-90'],
                 ['API GL-5', 'Semisintetico'], 'mannol-8118-ultra-gear-oil-75w-90-api-gl-5-semisintetico-olio-cambio-e-differenziale', '#mannol #olio cambio #75w90'),
 'mannol_atf': ('mannol_atf_dexron3', 'violet', 'cyan', ['Cambio automatico?', 'Servosterzo?'], 'Mannol', ['Automatic Plus ATF', 'Dexron III'],
                ['Dexron III', 'Cambio automatico', 'Servosterzo'], 'mannol-automatic-plus-atf-dexron-iii-olio-cambio-automatico-e-servosterzo-to-2', '#mannol #atf #cambioautomatico'),
 'power1_2t': ('castrol_power1_2t', 'amber', 'violet', ['Moto', '2 tempi?'], 'Castrol Power 1', ['Ultimate 2T'],
               ['2 tempi', '100% sintetico', 'Moto'], 'castrol-power-1-ultimate-2t-olio-motore-moto-100-sintetico', '#castrol #moto #2tempi'),
 'outboard': ('mannol_outboard_7207', 'cyan', 'amber', ['Fuoribordo', '2 tempi?'], 'Mannol 7207', ['Outboard Marine 2T'],
              ['API TC', 'NMMA TC-W3', 'JASO FC'], 'mannol-7207-outboard-marine-1l', '#mannol #nautica #fuoribordo'),
 'k_pure': ('selenia_k_pure_energy_5w40', 'violet', 'amber', ['5W-40', 'ACEA C3.'], 'Petronas Selenia', ['K Pure Energy', '5W-40'],
            ['ACEA C3'], 'olio-motore-petronas-selenia-k-pure-energy-5w40-4l-acea-c3', '#selenia #5w40'),
 'magnatec_0w30_d': ('castrol_magnatec_0w30_d', 'amber', 'cyan', ['0W-30', 'per Ford.'], 'Castrol Magnatec', ['0W-30 D'],
                     ['ACEA C2', 'Ford WSS-M2C950-A'], 'castrol-ford-magnatec-0w-30-d-olio-motore-specifica-ford-wss-m2c950-a-acea-c2-lubrificante-sintetico-protezione-avanzata', '#castrol #magnatec #ford #0w30'),
 'gm_dexos2': ('opel_gm_dexos2_1l', 'cyan', 'violet', ['Torna il', 'GM dexos2.'], 'GM Opel', ['dexos2', '5W-30'],
               ['ACEA C3', 'dexos2', 'MB 229.51 / 229.52'], 'olio-gm-5w-30-dexos2-acea-c3-mb-229-51-229-52-filtro-dpf-compatibile', '#gm #opel #dexos2 #5w30'),
}


def ease(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def seg(t, a, b): return ease((t - a) / (b - a))


def crop_resize(img, cx, cy, ch):
    """img numpy HxWx3; ritaglio centrato (cx,cy in frazioni) alto ch (frazione di H), rapporto 9:16 -> 1080x1920."""
    h, w = img.shape[:2]; hh = ch * h; ww = hh * 9 / 16
    x0 = int(np.clip(cx * w - ww / 2, 0, w - ww)); y0 = int(np.clip(cy * h - hh / 2, 0, h - hh))
    c = img[y0:y0 + int(hh), x0:x0 + int(ww)]
    return cv2.resize(c, (W, H), interpolation=cv2.INTER_AREA if hh > H else cv2.INTER_CUBIC)


def layer(fn):
    ly = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fn(ly); return ly


def comp(base, ly, a, rise=26):
    if a <= 0: return
    if a < 1:
        ly = ly.copy(); al = np.asarray(ly.split()[3]).astype(np.float32) * a
        ly.putalpha(Image.fromarray(al.astype(np.uint8)))
    base.alpha_composite(ly, (0, int((1 - a) * rise)))


GRAD = None
def top_grad(arr, h0=760, k=0.62):
    g = np.ones((H, 1, 1), np.float32); ramp = np.linspace(1 - k, 1, h0)[:, None, None]; g[:h0] = ramp
    return (arr.astype(np.float32) * g).astype(np.uint8)


def darken(arr, k): return (arr.astype(np.float32) * k).astype(np.uint8)


def build(key):
    foto, pa, pb, hook, kicker, name, specs, handle, _ = P[key]
    seed = sum(map(ord, key)) % 97
    A = np.asarray(render(1620, 2880, [foto], palette=pa, heights=[0.50], xs=[0.5], cx=0.5, base_y=0.88, logo=False, seed=seed).convert('RGB'))
    B = np.asarray(render(1242, 2208, [foto], palette=pb, heights=[0.50], xs=[0.73], cx=0.73, base_y=0.83, light='right',
                          logo=False, seed=seed + 7).convert('RGB'))
    # livelli di testo precalcolati
    L_hook = layer(lambda ly: T.block(ly, 0, 300, lines=hook, align='c', size=100))
    L_kick = layer(lambda ly: T.block(ly, 0, 290, kicker=kicker, align='c', subsize=46))
    L_name = layer(lambda ly: T.block(ly, 0, 375, lines=name, align='c', size=92 if max(len(n) for n in name) < 15 else 76))
    L_specT = layer(lambda ly: T.block(ly, 70, 330, kicker="In etichetta", lines=['Le sigle', 'da confrontare.'], size=70, subsize=32))
    L_chips = []
    for k, s in enumerate(specs):
        L_chips.append(layer(lambda ly, k=k, s=s: T.pill(ly, 70, 620 + k * 112, s, size=34)))
    L_note = layer(lambda ly: T.block(ly, 70, 620 + len(specs) * 112 + 30, sub='Confrontale con il libretto\ndella tua auto.', maxw=520, subsize=32))
    brt = Image.open(ROOT + '/assets/brt_logo.png').convert('RGBA')
    rows = [('Spedizione gratuita', 'in Italia · 24/48 ore', True), ('Europa', '3-7 giorni lavorativi', False),
            ('Reso', 'entro 14 giorni', False)]
    L_rows = []
    for k, (a, b, hb) in enumerate(rows):
        def draw(ly, k=k, a=a, b=b, hb=hb):
            y0 = 560 + k * 150; d = ImageDraw.Draw(ly)
            d.rounded_rectangle([90, y0, 990, y0 + 124], radius=30, fill=(6, 20, 34, 215), outline=CY + (230,), width=2)
            T.shadow_text(ly, (130, y0 + 20), a, font('Bold', 42), T.WHITE, blur=6, alpha=140)
            T.shadow_text(ly, (130, y0 + 70), b, font('Regular', 32), T.SOFT, blur=5, alpha=120)
            if hb:
                bw = 170; lg = brt.resize((bw, int(brt.height * bw / brt.width)), Image.LANCZOS)
                bg = Image.new('RGBA', (bw + 24, lg.height + 16), (255, 255, 255, 255)); bg.alpha_composite(lg, (12, 8))
                ly.alpha_composite(bg, (990 - 36 - bg.width, y0 + 62 - bg.height // 2))
        L_rows.append(layer(draw))
    CTA_BG = [cv2.GaussianBlur(darken(crop_resize(A, 0.5, 0.55, 0.95 - 0.05 * q / 10), 0.42), (0, 0), 22) for q in range(10)]
    L_cta0 = layer(lambda ly: T.block(ly, 0, 760, kicker='Mandalo a chi deve fare il tagliando', align='c', subsize=34))
    L_cta1 = layer(lambda ly: T.block(ly, 0, 980, lines=['Targa, modello', 'e anno in DM.'], align='c', size=80))
    L_cta2 = layer(lambda ly: T.block(ly, 0, 1200, sub='Verifichiamo noi la specifica giusta.', align='c', subsize=34, maxw=900))
    L_cta3 = layer(lambda ly: T.pill(ly, 0, 1310, 'Link in bio · autoevostore.it', size=36, align='c'))

    def frame(i):
        t = i / FPS
        if t < CUT[0]:                         # gancio: macro etichetta che si allarga
            p = t / CUT[0]
            im = Image.fromarray(top_grad(crop_resize(A, 0.5, 0.64, 0.46 + 0.10 * ease(p)))).convert('RGBA')
            im.alpha_composite(Image.fromarray(np.zeros((H, W, 4), np.uint8)))
            comp(im, L_hook, 1.0 if t > 0.08 else t / 0.08, rise=0)
        elif t < CUT[1]:                       # intero: push-in
            p = (t - CUT[0]) / (CUT[1] - CUT[0])
            im = Image.fromarray(crop_resize(A, 0.5, 0.54, 1.0 - 0.08 * ease(p))).convert('RGBA')
            im = add_logo(im, W, H, 0.30, 0.05)
            comp(im, L_kick, seg(t, CUT[0] + 0.15, CUT[0] + 0.6)); comp(im, L_name, seg(t, CUT[0] + 0.4, CUT[0] + 1.0))
        elif t < CUT[2]:                       # sigle
            p = (t - CUT[1]) / (CUT[2] - CUT[1])
            im = Image.fromarray(crop_resize(B, 0.5 + 0.03 * p, 0.5, 1.0 - 0.05 * ease(p))).convert('RGBA')
            im = add_logo(im, W, H, 0.24, 0.045)
            comp(im, L_specT, seg(t, CUT[1] + 0.1, CUT[1] + 0.5))
            for k, L in enumerate(L_chips): comp(im, L, seg(t, CUT[1] + 0.45 + 0.35 * k, CUT[1] + 0.8 + 0.35 * k), rise=18)
            comp(im, L_note, seg(t, CUT[1] + 0.6 + 0.35 * len(specs), CUT[1] + 1.0 + 0.35 * len(specs)))
        elif t < CUT[3]:                       # servizio
            p = (t - CUT[2]) / (CUT[3] - CUT[2])
            im = Image.fromarray(darken(crop_resize(B, 0.56, 0.5, 0.92 - 0.04 * p), 0.55)).convert('RGBA')
            im = add_logo(im, W, H, 0.30, 0.06)
            for k, L in enumerate(L_rows): comp(im, L, seg(t, CUT[2] + 0.1 + 0.3 * k, CUT[2] + 0.5 + 0.3 * k), rise=18)
        else:                                  # CTA
            p = (t - CUT[3]) / (DUR - CUT[3])
            im = Image.fromarray(CTA_BG[int(p * 9.99)]).convert('RGBA')
            im = add_logo(im, W, H, 0.56, 0.17)
            comp(im, L_cta0, seg(t, CUT[3] + 0.05, CUT[3] + 0.4)); comp(im, L_cta1, seg(t, CUT[3] + 0.2, CUT[3] + 0.6)); comp(im, L_cta2, seg(t, CUT[3] + 0.4, CUT[3] + 0.8))
            comp(im, L_cta3, seg(t, CUT[3] + 0.6, CUT[3] + 1.0))
        # dissolvenze rapide sui tagli
        f = 1.0
        for c in CUT[:-1]:
            d = abs(t - c)
            if d < 0.10: f = min(f, 0.25 + 0.75 * d / 0.10)
        if t > DUR - 0.5: f = min(f, (DUR - t) / 0.5)
        rgb = np.asarray(im.convert('RGB'))
        return rgb if f >= 1 else (rgb.astype(np.float32) * f).astype(np.uint8)

    tmp = f'/tmp/rp_{key}'; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    for i in range(NF):
        cv2.imwrite(f'{tmp}/{i:04d}.jpg', cv2.cvtColor(frame(i), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 93])
    os.makedirs(OUT, exist_ok=True)
    mp4 = f'{OUT}/{key}.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{tmp}/%04d.jpg', '-i', AUDIO,
                    '-t', str(DUR), '-af', f'afade=t=out:st={DUR - 1.2}:d=1.2', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19',
                    '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', mp4], check=True)
    # copertina: nome prodotto (t=4.0 s)
    Image.open(f'{tmp}/{int(4.2 * FPS):04d}.jpg').save(f'{OUT}/{key}.jpg', quality=92)
    shutil.rmtree(tmp)
    return mp4


if __name__ == '__main__':
    if not os.path.exists(AUDIO):
        os.makedirs(OUT, exist_ok=True)
        subprocess.run([sys.executable, os.path.dirname(os.path.abspath(__file__)) + '/gen_pilot_audio.py', AUDIO], check=True)
    for k in (sys.argv[1:] or list(P)):
        print(build(k), flush=True)
