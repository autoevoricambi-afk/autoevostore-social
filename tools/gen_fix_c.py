"""Grafiche 8-21 novembre 2026: schede, caroselli, storie. Specifiche solo da titolo/tag Shopify o già pubblicate."""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from photo_lib import *
from cal_lib import add_brt

MARKS={'Domanda della domenica':'?','Come lavoriamo':'3','Vero o falso?':'V/F','Sul sito':'ACEA','Attenzione':'GL-5','Domande frequenti':'FAQ','1 · Spedizione in Italia':'24/48','2 · Spedizione in Europa':'3-7','3 · Reso':'14','4 · Assistenza':'9-18','Spedizione':'24/48','Reso':'14','Weekend':'DM','Domanda':'?','Europa':'3-7','Assistenza':'9-18','Il weekend è per la guida':'ACEA','Risposta di ieri':'F'}
def bold_slide(kick,lines,body=None,W=1080,H=1350,fonts=84,bullets=(),chips=(),**k):
    """Solo testo: scritta gigante di sfondo, titolo grande al centro ottico."""
    story=H>1500
    img,y=base(W,H,logo_w=460 if not story else 540,glows=((0.5,0.56,0.62,0.42,0.26),))
    mark=MARKS.get(kick,'')
    if mark:
        sz=420
        while ImageDraw.Draw(Image.new('RGBA',(5,5))).textlength(mark,font=font('Bold',sz))>W*0.92: sz-=10
        wm=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(wm); fw=font('Bold',sz); tw=d.textlength(mark,font=fw)
        d.text(((W-tw)/2,int(H*(0.70 if not story else 0.64))-sz*0.62),mark,font=fw,fill=(255,255,255,34)); img=Image.alpha_composite(img,wm)
    y=int(H*(0.27 if not story else 0.25)); img=kicker(img,kick,y,size=36); y+=76
    img,y=title(img,lines,y,size=int(fonts*1.12))
    y+=24
    if body: y=paragraph(img,body,y,font('Regular',44),(225,235,246,255),maxw=900) or y
    d=ImageDraw.Draw(img); fb=font('Medium',46)
    for b in bullets:
        d.ellipse([130,y+18,150,y+38],fill=CY+(255,)); d.text((180,y),b,font=fb,fill=(235,242,250,255)); y+=82
    if chips: img=chips_row(img,chips,(H-300) if not story else (H-420),size=34,h=70)
    return foot(img)
O='2026-11/'
O='2026-10/fix/'
# ---------- CAROSELLO 10/11: cambio e differenziale (5)
save(duo('castrol_transmax_axle_80w90','mannol_8118','Cambio e differenziale',['Non è tutto','olio motore.'],['Castrol Transmax Axle EPX','80W-90 · API GL-5'],['MANNOL Ultra Gear 8118','75W-90 · API GL-5'],fonts=72),O+'n_car10_1.jpg')
save(hero('castrol_transmax_axle_80w90','Castrol Transmax Axle EPX',['80W-90'],chips=('API GL-5','ZF TE-ML'),fonts=78),O+'n_car10_2.jpg')
save(hero('mannol_8118','MANNOL Ultra Gear Oil 8118',['75W-90'],chips=('Semisintetico','API GL-5','SAE J2360'),fonts=78),O+'n_car10_3.jpg')
save(bold_slide('Attenzione',['GL-5 non è adatta','a tutti i cambi.'],body='La classe GL-5 non va bene per tutti i cambi manuali sincronizzati: alcuni costruttori richiedono solo GL-4. Il libretto decide.',fonts=72),O+'n_car10_4.jpg')
save(text_slide('Il prossimo passo',['Targa, modello','e anno.'],body='Mandaceli in DM: verifichiamo noi la specifica giusta. Spedizione gratuita in Italia, consegna in 24/48 ore.',key='castrol_transmax_axle_80w90',fonts=76),O+'n_car10_5.jpg')

# ---------- CAROSELLO 11/11: tre 0W-30 (5)
save(lineup(['castrol_edge_ll_0w30','castrol_magnatec_0w30_d','selenia_wr_forward_0w30'],'Stesso grado: 0W-30',['Tre 0W-30,','tre specifiche.'],cap='Cambia l’omologazione, non il grado.',fonts=78),O+'n_car11_1.jpg')
save(hero('castrol_edge_ll_0w30','Castrol EDGE',['0W-30 LL'],chips=('ACEA C3','VW 504.00 / 507.00'),fonts=78),O+'n_car11_2.jpg')
save(hero('castrol_magnatec_0w30_d','Castrol MAGNATEC',['0W-30 D'],chips=('ACEA C2','Ford WSS-M2C950-A'),fonts=78),O+'n_car11_3.jpg')
save(hero('selenia_wr_forward_0w30','Selenia WR Forward',['0W-30'],chips=('ACEA C2','FIAT 955535-DS1/DH1'),fonts=78),O+'n_car11_4.jpg')
save(text_slide('Il prossimo passo',['Quale serve','alla tua auto?'],body='Il libretto indica l’omologazione richiesta. Scrivici targa, modello e anno in DM: verifichiamo noi la specifica giusta.',key='castrol_edge_ll_0w30',fonts=76),O+'n_car11_5.jpg')
