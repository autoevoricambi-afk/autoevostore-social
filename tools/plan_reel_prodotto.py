"""Piano Reel prodotto nov-dic 2026 -> payload Metricool (IG e FB separati: su FB link prodotto cliccabile con UTM).
Uso: python3 tools/plan_reel_prodotto.py > data/reel_prodotto_plan.json"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_prodotto import P

RAW = 'https://raw.githubusercontent.com/autoevoricambi-afk/autoevostore-social/main/media/reels-prodotto/'
SITE = 'https://www.autoevostore.it/products/'

# data, ora, chiave, (id IG, uuid IG), (id FB, uuid FB) — None = da creare
PLAN = [
 ('2026-11-09', '18:30', 'wr_forward', ('406389115', '-2625437624587958771'), ('406389207', '-3347190468452856472')),
 ('2026-11-12', '18:30', 'magnatec_a5', ('406389652', '-3962139983210659364'), ('406389749', '-4323734336752236525')),
 ('2026-11-14', '12:00', 'digitek_0w30', ('406533942', '5444657597713891818'), ('410892001', '-2705981150913082902')),
 ('2026-11-16', '18:30', 'wr_diesel', ('406392798', '1838804896777324929'), ('406392862', '2742757974301036119')),
 ('2026-11-19', '18:30', 'mannol_ll', ('406535052', '4512172593427661149'), ('406535147', '-9009898735743315994')),
 ('2026-11-20', '18:30', 'wr_pure', ('406535316', '-5554863138553181083'), ('406535428', '-7014647564559954425')),
 ('2026-11-21', '12:00', 'ineo_mc3', ('406535532', '-5403096970385339392'), ('410893449', '668330550046707509')),
 ('2026-11-22', '18:30', 'multipower_gas', None, None),
 ('2026-11-23', '18:30', '20k_10w40', ('406538586', '-2289043682129918686'), ('406538678', '49445649407035121')),
 ('2026-11-25', '18:30', 'magnatec_prof_d', ('406539025', '3151682553353752459'), ('410896411', '-7679587966592987742')),
 ('2026-11-26', '18:30', 'edge_td', ('406539288', '7974062257469411171'), ('406539792', '6766542908755559849')),
 ('2026-11-28', '12:00', 'edge_0w20', None, None),
 ('2026-12-01', '18:30', 'petronas_xs', None, None),
 ('2026-12-02', '18:30', 'edge_ll3', None, None),
 ('2026-12-03', '18:30', 'mobil1_esp', None, None),
 ('2026-12-04', '18:30', 'transmax', None, None),
 ('2026-12-05', '12:00', 'power1_2t', None, None),
 ('2026-12-06', '18:30', 'k_pure', None, None),
 ('2026-12-07', '18:30', 'petronas_av', None, None),
 ('2026-12-08', '18:30', 'bmw_ll04', None, None),
 ('2026-12-09', '18:30', 'mannol_8118', None, None),
 ('2026-12-10', '18:30', 'gm_dexos2', None, None),
 ('2026-12-11', '18:30', 'edge_ll_0w30', None, None),
 ('2026-12-12', '12:00', 'outboard', None, None),
 ('2026-12-13', '18:30', 'mannol_atf', None, None),
 ('2026-12-14', '18:30', 'magnatec_0w30_d', None, None),
]


def tags(k):
    t = [x for x in P[k][8].replace('#olio cambio', '#oliocambio').split() if x.startswith('#')][:3]
    return ' '.join(['#autoevostore', '#oliomotore'] + t)  # max 5 hashtag (limite Instagram dic 2025)


def caption(k, link):
    foto, pa, pb, hook, kicker, name, specs, handle, _ = P[k]
    full = f"{kicker} {' '.join(name)}"
    return (f"{' '.join(hook)}\n\n{full}: {' · '.join(specs)}.\n"
            f"Nel Reel: etichetta da vicino, flacone intero e le sigle da confrontare con il libretto.\n\n"
            f"Non sai se è quello giusto per la tua auto? Scrivici targa e modello in DM: verifichiamo noi la specifica giusta.\n"
            f"Mandalo a chi deve fare il tagliando.\n\n"
            f"Spedizione gratuita in Italia 24/48 ore con BRT · reso entro 14 giorni.\n\n"
            f"{link}\n\n{tags(k)}"), full


def payload(date, hour, k, net):
    foto, pa, pb, hook, kicker, name, specs, handle, _ = P[k]
    utm = f"?utm_source=facebook&utm_medium=organic_social&utm_campaign=autoevo_ott_nov_2026&utm_content=ae-{date}-{hour.replace(':', '')}-reel"
    link = 'autoevostore.it (link in bio)' if net == 'instagram' else f"Scheda prodotto: {SITE}{handle}{utm}\nautoevostore.it"
    text, full = caption(k, link)
    d = {"autoPublish": True, "descendants": [], "draft": False, "firstCommentText": "", "hasNotReadNotes": False,
         "media": [RAW + k + '.mp4'], "mediaAltText": [f"Reel {full}: etichetta, flacone e sigle {', '.join(specs)}."],
         "videoThumbnailUrl": RAW + k + '.jpg', "providers": [{"network": net}],
         "publicationDate": {"dateTime": f"{date}T{hour}:00", "timezone": "Europe/Rome"}, "shortener": False,
         "smartLinkData": {"ids": []}, "text": text}
    if net == 'instagram': d["instagramData"] = {"type": "REEL", "showReelOnFeed": True, "isAiGenerated": False}
    else: d["facebookData"] = {"type": "REEL", "title": full}
    return d


if __name__ == '__main__':
    out = []
    for date, hour, k, ig, fb in PLAN:
        for net, ref in (('instagram', ig), ('facebook', fb)):
            out.append({"date": date, "hour": hour, "key": k, "net": net, "id": ref[0] if ref else None,
                        "uuid": ref[1] if ref else None, "info": payload(date, hour, k, net)})
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
