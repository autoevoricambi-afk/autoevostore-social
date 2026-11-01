"""Ecosistema storie 8/11-14/12/2026, stesso stile cinematografico dei Reel (1080x1920).
Ogni giorno: 12:30 + 19:00 legate al contenuto feed del giorno (teaser -> Reel -> recap sigle / servizio).
Output: media/stories-cine/<data>_<ora>.jpg + data/ecosistema_plan.json
Uso: python3 tools/gen_ecosistema.py"""
import os, sys, json, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from cine_lib import render
import cine_type as T
from cal_lib import add_brt
from pilot_common import save_srgb, fit_size
from reel_prodotto import P
from reel_serie import S as SERIE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = ROOT + '/media/stories-cine'
RAW = 'https://raw.githubusercontent.com/autoevoricambi-afk/autoevostore-social/main/media/stories-cine/'
W, H = 1080, 1920

# contenuto feed del giorno: ('R', chiave reel prodotto) | ('S', chiave serie) | ('Q', domanda) | ('C', carosello) | ('T', fiducia)
FEED = {
 '2026-11-08': ('Q', 'Cosa guardi per primo?'), '2026-11-09': ('R', 'wr_forward'), '2026-11-10': ('C', 'Cambio e differenziale'),
 '2026-11-11': ('C', 'Tre 0W-30, tre specifiche'), '2026-11-12': ('R', 'magnatec_a5'), '2026-11-13': ('S', 'c2_c3'),
 '2026-11-14': ('R', 'digitek_0w30'), '2026-11-15': ('Q', 'Stessa viscosità, stesso olio?'), '2026-11-16': ('R', 'wr_diesel'),
 '2026-11-17': ('T', 'Reso entro 14 giorni'), '2026-11-18': ('S', 'non_solo_motore'), '2026-11-19': ('R', 'mannol_ll'),
 '2026-11-20': ('R', 'wr_pure'), '2026-11-21': ('R', 'ineo_mc3'), '2026-11-22': ('R', 'multipower_gas'),
 '2026-11-23': ('R', '20k_10w40'), '2026-11-24': ('S', 'stesso_5w30'), '2026-11-25': ('R', 'magnatec_prof_d'),
 '2026-11-26': ('R', 'edge_td'), '2026-11-27': ('S', 'magazzino'), '2026-11-28': ('R', 'edge_0w20'),
 '2026-11-29': ('Q', 'Che auto guidi?'), '2026-11-30': ('S', 'stesso_5w40'),
 '2026-12-01': ('R', 'petronas_xs'), '2026-12-02': ('R', 'edge_ll3'), '2026-12-03': ('R', 'mobil1_esp'),
 '2026-12-04': ('R', 'transmax'), '2026-12-05': ('R', 'power1_2t'), '2026-12-06': ('R', 'k_pure'),
 '2026-12-07': ('R', 'petronas_av'), '2026-12-08': ('R', 'bmw_ll04'), '2026-12-09': ('R', 'mannol_8118'),
 '2026-12-10': ('R', 'gm_dexos2'), '2026-12-11': ('R', 'edge_ll_0w30'), '2026-12-12': ('R', 'outboard'),
 '2026-12-13': ('R', 'mannol_atf'), '2026-12-14': ('R', 'magnatec_0w30_d'),
}
LINEUPS = [['castrol_edge_ll3_5w30', 'mobil1_esp_5w30', 'petronas_xs_5w30'], ['selenia_wr_forward_0w30', 'total_ineo_mc3', 'mannol_longlife_504_507'],
           ['castrol_magnatec_5w30_a5', 'selenia_multipower_gas', 'castrol_edge_td_5w40'], ['bmw_twinpower_ll04_0w30', 'castrol_edge_0w20_c5', 'selenia_20k_10w40'],
           ['mannol_8118', 'castrol_transmax_axle_80w90', 'mannol_atf_dexron3']]
PALS = ['cyan', 'violet', 'amber']
SERV = [  # (kicker, titolo, sotto, brt)
 ('Spedizione gratuita in Italia', ['24/48 ore.'], 'Con corriere BRT, fino a casa tua.', True),
 ('Spediamo anche in Europa', ['3-7 giorni', 'lavorativi.'], 'Escluse Cipro e Malta.', False),
 ('Acquista sereno', ['Reso entro', '14 giorni.'], 'Condizioni su autoevostore.it', False),
 ('Assistenza vera', ['Lun-ven', '9:00-18:00.'], 'Scrivici in DM targa, modello e anno: verifichiamo noi la specifica giusta.', False),
 ('Tutti i nostri link', ['Un tocco,', 'il prodotto.'], 'Prodotti in evidenza e verifica compatibilità: link in bio.', False),
]


def scene(keys, pal, seed, mode):
    if mode == 'hero':   # flacone grande in basso al centro
        return render(W, H, keys, palette=pal, seed=seed, heights=[0.46], xs=[0.5], cx=0.5, base_y=0.90, logo_w=0.40)
    if mode == 'side':   # flacone a destra
        return render(W, H, keys, palette=pal, seed=seed, heights=[0.44], xs=[0.72], cx=0.72, base_y=0.88, light='right', logo_w=0.40)
    return render(W, H, keys, palette=pal, seed=seed, heights=[0.26, 0.30, 0.26], xs=[0.22, 0.5, 0.78], base_y=0.90, logo_w=0.40)


def story_teaser(k, when, seed):
    foto, pa, pb, hook, kicker, name, specs, handle, _ = P[k]
    im = scene([foto], pa, seed, 'hero').convert('RGBA')
    y = T.block(im, 0, 330, kicker=when, align='c', subsize=40)
    y = T.block(im, 0, y + 10, lines=hook, align='c', size=fit_size(hook, 920, 104))
    T.pill(im, 0, y + 30, 'Nuovo Reel sul profilo', size=34, align='c')
    return im, f"Storia: {when}, nuovo Reel. {' '.join(hook)} Flacone {kicker} {' '.join(name)}."


def story_recap(k, seed):
    foto, pa, pb, hook, kicker, name, specs, handle, _ = P[k]
    im = scene([foto], pb, seed, 'side').convert('RGBA')
    y = T.block(im, 70, 360, kicker=f'{kicker} {" ".join(name)}', lines=['Le sigle', 'in etichetta.'], size=86, subsize=30, maxw=560)
    for s in specs:
        T.pill(im, 70, y + 20, s, size=36); y += 110
    T.block(im, 70, y + 40, sub='È quello giusto per la tua auto?\nScrivici targa e modello in DM.', subsize=34, maxw=560)
    return im, f"Storia: sigle in etichetta di {kicker} {' '.join(name)}: {', '.join(specs)}. Scrivici targa e modello in DM."


def story_serie(k, when, seed):
    hook, scenes, close, sub = SERIE[k]
    im = scene([s[0] for s in scenes], PALS[seed % 3], seed, 'lineup').convert('RGBA')
    y = T.block(im, 0, 330, kicker=when, align='c', subsize=40)
    y = T.block(im, 0, y + 10, lines=hook, align='c', size=fit_size(hook, 920, 104))
    T.pill(im, 0, y + 30, 'Nuovo Reel sul profilo', size=34, align='c')
    return im, f"Storia: {when}, nuovo Reel. {' '.join(hook)} Tre flaconi in scena."


def story_serv(i, seed):
    kick, title, sub, brt = SERV[i % len(SERV)]
    im = scene(LINEUPS[(seed * 7 + seed // 3) % len(LINEUPS)], PALS[(seed + 1) % 3], seed, 'lineup').convert('RGBA')
    y = T.block(im, 0, 360, kicker=kick, lines=title, sub=sub, align='c', size=110, subsize=36, maxw=900)
    if brt: im = add_brt(im, y + 120, scale=0.7).convert('RGBA')
    return im, f"Storia AUTO EVO STORE: {kick}. {' '.join(title)} {sub}"


def story_engage(q, seed):
    im = scene(LINEUPS[(seed * 7 + seed // 3) % len(LINEUPS)], PALS[seed % 3], seed, 'lineup').convert('RGBA')
    y = T.block(im, 0, 360, kicker='Il post di oggi', lines=[q], align='c', size=fit_size([q], 940, 92), subsize=36)
    T.block(im, 0, y + 20, sub='Rispondi nei commenti del post.\nDubbi sulla tua auto? Scrivici in DM.', align='c', subsize=36, maxw=900)
    return im, f"Storia: rispondi al post di oggi. {q}"


def build():
    os.makedirs(OUT, exist_ok=True)
    plan = []; si = 0
    for n, (date, (kind, val)) in enumerate(sorted(FEED.items())):
        d = dt.date.fromisoformat(date); sat = d.weekday() == 5
        seed = 200 + n * 3
        if kind == 'R':
            if sat:   # Reel alle 12:00: recap alle 12:30, servizio alle 19:00
                a = story_recap(val, seed); b = story_serv(si, seed + 1); si += 1
            else:
                a = story_teaser(val, 'Stasera alle 18:30', seed); b = story_recap(val, seed + 1)
        elif kind == 'S':
            a = story_serie(val, 'Stasera alle 18:30', seed); b = story_serv(si, seed + 1); si += 1
        elif kind == 'Q':
            a = story_serv(si, seed); si += 1; b = story_engage(val, seed + 1)
        else:  # C, T
            a = story_serv(si, seed); si += 1; b = story_engage(val, seed + 1) if kind == 'C' else story_serv(si, seed + 1); si += kind == 'T'
        for hour, (im, alt) in (('12:30', a), ('19:00', b)):
            name = f"{date}_{hour.replace(':', '')}.jpg"
            save_srgb(im, f'{OUT}/{name}', jpg=True)
            plan.append({'date': date, 'hour': hour, 'media': RAW + name, 'alt': alt})
        print(date, flush=True)
    json.dump(plan, open(ROOT + '/data/ecosistema_plan.json', 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    build()
