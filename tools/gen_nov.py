"""Grafiche 8-21 novembre 2026: schede, caroselli, storie. Specifiche solo da titolo/tag Shopify o già pubblicate."""
import sys,os; sys.path.insert(0,os.path.dirname(__file__))
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
H=1920
def cta(img,y=None,txt='Dubbi? Scrivici targa e modello in DM.'):
    ctext(img,txt,y or (img.height-175),font('Regular',34),SOFT); return img

# ---------- FEED singoli
# 8/11 domenica: domanda
save(bold_slide('Domanda della domenica',['Cosa guardi','per prima?'],fonts=84,bullets=['A) La viscosità (5W-30, 5W-40...)','B) Il marchio','C) L’omologazione del costruttore','D) Non lo so: mi affido a chi lo sa']),O+'dom08.jpg')
# 9/11 lunedì: scheda Selenia WR Forward
save(bigspec('selenia_wr_forward_0w30','0W-30','Selenia',['WR Forward'],chips=('ACEA C2','FIAT 955535-DS1/DH1'),fonts=76),O+'prod09_forward.jpg')
# 12/11 giovedì: scheda Magnatec A5
save(split('castrol_magnatec_5w30_a5','Castrol MAGNATEC',['5W-30','A5'],['Olio motore','ACEA A5/B5','Ford WSS-M2C913']),O+'prod12_magnatec.jpg')
# 14/11 sabato: cosa ci serve
save(bold_slide('Come lavoriamo',['Tre dati,','una specifica.'],body='Per scegliere l’olio giusto ci servono targa, modello e anno. Scrivici in DM: con questi dati controlliamo insieme a te la specifica sul libretto.',fonts=84,chips=('Targa','Modello','Anno')),O+'sab14.jpg')
# 15/11 domenica: vero o falso
save(bold_slide('Vero o falso?',['“Se la viscosità','è giusta, va bene','qualsiasi olio.”'],body='Rispondi nei commenti: V o F. La risposta domani nelle storie.',fonts=78),O+'dom15.jpg')
# 16/11 lunedì: scheda Selenia WR 5W-40 Diesel
save(bigspec('selenia_wr_5w40_diesel','5W-40','Selenia WR',['Diesel'],chips=('ACEA A3/B4','API SN/CF','FIAT 9.55535-N2/N3'),fonts=76),O+'prod16_diesel.jpg')
# 19/11 giovedì: scheda Mannol Longlife
save(hero('mannol_longlife_504_507','MANNOL',['Longlife 504/507'],chips=('5W-30','ACEA C3','VW 504.00 / 507.00','Porsche C30'),fonts=78),O+'prod19_mannol.jpg')
# 21/11 sabato: guida alle sigle
save(bold_slide('Sul sito',['Non ricordi cosa','significa ACEA?'],body='Sul nostro sito c’è la guida alle sigle: ACEA, API e omologazioni dei costruttori spiegate in modo semplice. Cerca “Guida alle sigle” su autoevostore.it.',fonts=76,chips=('ACEA','API','OEM')),O+'sab21.jpg')

# ---------- CAROSELLO 10/11: cambio e differenziale (5)
save(duo('castrol_transmax_axle_80w90','mannol_8118','Cambio e differenziale',['Non è tutto','olio motore.'],['Castrol Transmax Axle EPX','80W-90 · API GL-5'],['MANNOL Ultra Gear 8118','75W-90 · API GL-5'],fonts=72),O+'car10_1.jpg')
save(hero('castrol_transmax_axle_80w90','Castrol Transmax Axle EPX',['80W-90'],chips=('API GL-5','ZF TE-ML'),fonts=78),O+'car10_2.jpg')
save(hero('mannol_8118','MANNOL Ultra Gear Oil 8118',['75W-90'],chips=('Semisintetico','API GL-5','SAE J2360'),fonts=78),O+'car10_3.jpg')
save(bold_slide('Attenzione',['GL-5 non è adatta','a tutti i cambi.'],body='La classe GL-5 non va bene per tutti i cambi manuali sincronizzati: alcuni costruttori richiedono solo GL-4. Il libretto decide.',fonts=72),O+'car10_4.jpg')
save(text_slide('Il prossimo passo',['Targa, modello','e anno.'],body='Mandaceli in DM: verifichiamo noi la specifica giusta. Spedizione gratuita in Italia, consegna in 24/48 ore.',key='castrol_transmax_axle_80w90',fonts=76),O+'car10_5.jpg')

# ---------- CAROSELLO 11/11: tre 0W-30 (5)
save(lineup(['castrol_edge_ll_0w30','castrol_magnatec_0w30_d','selenia_wr_forward_0w30'],'Stesso grado: 0W-30',['Tre 0W-30,','tre specifiche.'],cap='Cambia l’omologazione, non il grado.',fonts=78),O+'car11_1.jpg')
save(hero('castrol_edge_ll_0w30','Castrol EDGE',['0W-30 LL'],chips=('ACEA C3','VW 504.00 / 507.00'),fonts=78),O+'car11_2.jpg')
save(hero('castrol_magnatec_0w30_d','Castrol MAGNATEC',['0W-30 D'],chips=('ACEA C2','Ford WSS-M2C950-A'),fonts=78),O+'car11_3.jpg')
save(hero('selenia_wr_forward_0w30','Selenia WR Forward',['0W-30'],chips=('ACEA C2','FIAT 955535-DS1/DH1'),fonts=78),O+'car11_4.jpg')
save(text_slide('Il prossimo passo',['Quale serve','alla tua auto?'],body='Il libretto indica l’omologazione richiesta. Scrivici targa, modello e anno in DM: verifichiamo noi la specifica giusta.',key='castrol_edge_ll_0w30',fonts=76),O+'car11_5.jpg')

# ---------- CAROSELLO 17/11: domande frequenti (6)
save(bold_slide('Domande frequenti',['Le cinque domande','che ci fanno di più.'],fonts=80,body='Spedizione, reso, assistenza e come scegliamo l’olio giusto. Scorri.'),O+'car17_1.jpg')
s=bold_slide('1 · Spedizione in Italia',['Gratuita,','24/48 ore.'],body='Spediamo con BRT. Il tuo ordine arriva in 24/48 ore, senza costi di spedizione.',fonts=84)
save(add_brt(s,s.height-330,1.0),O+'car17_2.jpg')
save(bold_slide('2 · Spedizione in Europa',['3-7 giorni','lavorativi.'],body='Spedizione tracciata, costo calcolato al checkout. Escluse Cipro e Malta.',fonts=84),O+'car17_3.jpg')
save(bold_slide('3 · Reso',['Entro','14 giorni.'],body='Se hai cambiato idea, puoi rendere l’ordine entro 14 giorni.',fonts=84),O+'car17_4.jpg')
save(bold_slide('4 · Assistenza',['Lunedì-venerdì,','9:00-18:00.'],body='Scrivici prima di ordinare: rispondiamo in orario di assistenza.',fonts=84),O+'car17_5.jpg')
save(text_slide('5 · Come scegliamo',['Targa, modello','e anno in DM.'],body='Con questi dati verifichiamo noi la specifica giusta sul libretto. Poi ordini su autoevostore.it.',key='mobil1_esp_5w30',fonts=76),O+'car17_6.jpg')

# ---------- STORIE 12:30 (8-21 nov)
S=[]
def st(n,img): save(cta(img) if False else img,O+f'st{n}.jpg')
st('08',text_slide('Lo sapevi?',['MB 229.51 e 229.52','sono omologazioni','Mercedes-Benz.'],body='Se il libretto le richiede, cercale in etichetta. Targa e modello in DM.',key='mobil1_esp_5w30',W=1080,H=H,fonts=64))
s=bold_slide('Spedizione',['Gratis in Italia.','24/48 ore.'],body='Spediamo con BRT. Europa in 3-7 giorni lavorativi (escluse Cipro e Malta).',W=1080,H=H,fonts=72); st('09',add_brt(s,H-420,1.1))
st('10',text_slide('Lo sapevi?',['VW 504.00 e 507.00','sono norme Volkswagen.'],body='La prima è per i motori a benzina, la seconda per i diesel. Controlla il libretto.',key='castrol_edge_ll_0w30',W=1080,H=H,fonts=64))
st('11',lineup(['castrol_edge_ll_0w30','castrol_magnatec_0w30_d','castrol_transmax_axle_80w90'],'Marchio',['Castrol'],cap='Motore, cambio, differenziale.',W=1080,H=H,fonts=76))
st('12',bold_slide('Reso',['Entro','14 giorni.'],body='Acquisti con serenità su autoevostore.it. Assistenza lunedì-venerdì, 9:00-18:00.',W=1080,H=H,fonts=84))
st('13',text_slide('Lo sapevi?',['BMW Longlife-04','è un’omologazione','BMW.'],body='La trovi anche su alcuni oli di altri marchi, come Mobil 1 ESP 5W-30. Il libretto dice se serve.',key='mobil1_esp_5w30',W=1080,H=H,fonts=64))
st('14',bold_slide('Weekend',['Scrivici anche','il sabato.'],body='Targa, modello e anno in DM: ti rispondiamo dal lunedì, dalle 9:00.',W=1080,H=H,fonts=76))
st('15',bold_slide('Domanda',['Hai il libretto','a portata di mano?'],body='Cerca la sigla dell’olio richiesto (ad esempio 5W-30) e le omologazioni. Non le trovi? Scrivici.',W=1080,H=H,fonts=72))
st('16',text_slide('Risposta di ieri',['Falso.'],body='La viscosità dice come scorre l’olio. L’omologazione dice per quali motori è approvato. Servono entrambe.',key='petronas_prime_av',W=1080,H=H,fonts=96))
s=bold_slide('Europa',['Spediamo','anche fuori Italia.'],body='3-7 giorni lavorativi, spedizione tracciata, costo calcolato al checkout. Escluse Cipro e Malta.',W=1080,H=H,fonts=72); st('17',s)
st('18',lineup(['selenia_wr_forward_0w30','selenia_digitek_0w30','selenia_wr_pure_energy_5w30'],'Marchio',['Selenia'],cap='Specifiche per i motori FIAT.',W=1080,H=H,fonts=76) if False else lineup(['selenia_wr_forward_0w30','selenia_digitek_0w30','selenia_wr_pure_energy_5w30'],'Marchio',['Selenia'],cap='Specifiche FIAT e Mopar.',W=1080,H=H,fonts=76))
st('19',text_slide('Lo sapevi?',['FIAT 9.55535 è una','famiglia di specifiche.'],body='Dopo il numero conta la sigla (S2, N2, G2...): controlla quella del libretto.',key='selenia_wr_5w40_diesel',W=1080,H=H,fonts=64))
st('20',bold_slide('Assistenza',['Lunedì-venerdì,','9:00-18:00.'],body='Scrivici prima di ordinare: targa, modello e anno in DM.',W=1080,H=H,fonts=80))
st('21',bold_slide('Il weekend è per la guida',['Sul sito trovi','la guida alle sigle.'],body='ACEA, API e omologazioni spiegate. Cerca “Guida alle sigle” su autoevostore.it.',W=1080,H=H,fonts=68))
print('ok')
# 20/11 venerdì: scheda Selenia WR Pure Energy
save(bigspec('selenia_wr_pure_energy_5w30','5W-30','Petronas Selenia',['WR Pure Energy'],chips=('ACEA C2','FIAT / Mopar'),fonts=70),O+'prod20_pure.jpg')
