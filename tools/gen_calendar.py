"""Genera grafiche + calendario 10 ott - 8 nov 2026 (feed + storie). Output: media/2026-10/*.png e data/calendar_2026-10.json"""
from cal_lib import *
CAL=[]
def post(key,date,slides,caption,alts):
    CAL.append(dict(key=key,kind='post',dt=date,media=slides,caption=caption,alts=alts))
def st(key,date,alt): CAL.append(dict(key=key,kind='story',dt=date,media=[key],caption='',alts=[alt]))
END='\n\nautoevostore.it (link in bio)'
SPED='Spedizione gratuita in Italia, consegna in 24/48 ore.'
DM='Scrivici targa e modello in DM: verifichiamo noi la specifica giusta.'
def car(prefix,seed,slds):
    keys=[]
    for k,d in enumerate(slds):
        key=f'{prefix}_{k+1}'; save(slide(n=len(slds),i=k,seed=seed+k,**d),key); keys.append(key)
    return keys
CTA=dict(icon='chat',lines=[('NON SEI SICURO',WHITE,84),("DELL'OLIO?",CYc,84)],body='Scrivici targa e modello in DM:',body2='controlliamo noi la specifica giusta.',cta='autoevostore.it  (link in bio)')
# ---------- Martedi: caroselli consigli
k=car('tip13',200,[
 dict(cover=True,lines=[('SINTETICO,',WHITE,84),('SEMISINTETICO',CYc,70),('O MINERALE?',WHITE,84)],body='Le tre basi, in due minuti.',body2='Scorri per capirle'),
 dict(icon='drop',lines=[('SINTETICO',WHITE,80)],body='Base sintetica. È la scelta di molti oli moderni con specifiche severe.',chips=['Es. Petronas Syntium Prime AV 5W-40']),
 dict(icon='drop',lines=[('SEMISINTETICO',WHITE,66)],body='Miscela di basi minerali e sintetiche.',chips=['Es. WRC Premium 10W-40']),
 dict(icon='drop',lines=[('MINERALE',WHITE,80)],body='Deriva dalla raffinazione del petrolio. Si usa su motori che lo prevedono.',chips=['Es. WRC Logor 20W-60']),
 dict(CTA)])
post('tip13','2026-10-13T18:30',k,"Sintetico, semisintetico o minerale: che differenza c'è?\n\nSintetico: base sintetica, tipico di molti oli moderni con specifiche severe (es. Petronas Syntium Prime AV 5W-40).\nSemisintetico: miscela di basi minerali e sintetiche (es. WRC Premium 10W-40).\nMinerale: deriva dalla raffinazione del petrolio (es. WRC Logor 20W-60).\n\nQuale scegliere lo decide il libretto del tuo veicolo. "+DM+"\n\n"+SPED+END+"\n\n#oliomotore #lubrificanti #autoevostore #sintetico #manutenzioneauto",
 ['Sintetico, semisintetico o minerale?','Olio sintetico: base sintetica','Olio semisintetico: miscela di basi','Olio minerale: da raffinazione del petrolio','Scrivici targa e modello in DM'])
k=car('tip20',210,[
 dict(cover=True,lines=[('QUANDO CAMBIARE',WHITE,76),("L'OLIO MOTORE?",CYc,80)],body='Tre cose da sapere.',body2='Scorri'),
 dict(icon='book',lines=[('1 · IL LIBRETTO',WHITE,72)],body="Indica l'intervallo di cambio: in chilometri o in tempo, vale quello che arriva prima."),
 dict(icon='clock',lines=[('2 · COME USI L\'AUTO',WHITE,66)],body="Se il libretto prevede condizioni d'uso severe (città, tragitti brevi, traino), segui l'intervallo indicato per quel caso."),
 dict(icon='check',lines=[('3 · L\'OLIO GIUSTO',WHITE,72)],body='Usa la viscosità e la specifica indicate dal costruttore. Sono scritte in etichetta.'),
 dict(CTA)])
post('tip20','2026-10-20T18:30',k,"Quando cambiare l'olio motore? Tre cose da sapere.\n\n1) Il libretto indica l'intervallo: chilometri o tempo, vale quello che arriva prima.\n2) Se prevede condizioni d'uso severe (città, tragitti brevi, traino), segui l'intervallo indicato per quel caso.\n3) Usa viscosità e specifica richieste dal costruttore.\n\n"+DM+"\n\n"+SPED+END+"\n\n#cambioolio #oliomotore #autoevostore #lubrificanti #manutenzioneauto",
 ["Quando cambiare l'olio motore?",'Il libretto indica intervallo','Condizioni di uso severe','Usa viscosità e specifica giuste','Scrivici targa e modello in DM'])
k=car('tip27',220,[
 dict(cover=True,lines=[('AUTO A GPL',WHITE,84),('O METANO?',CYc,84)],body='Esistono oli pensati per te.',body2='Scorri'),
 dict(icon='drop',lines=[('OLIO DEDICATO',WHITE,72)],body='Per i motori a gas esistono oli formulati per questo impiego.'),
 dict(icon='check',lines=[('DUE ESEMPI REALI',WHITE,64)],body='Entrambi 5W-40 sintetici per GPL e metano.',chips=['Selenia Multipower Gas 5W-40 · ACEA C3','WRC Ultraplus 5W-40 Gas']),
 dict(icon='book',lines=[('CONTROLLA',WHITE,80)],body="Verifica sempre le indicazioni del costruttore dell'auto e dell'impianto a gas."),
 dict(CTA)])
post('tip27','2026-10-27T18:30',k,"Auto a GPL o metano: serve un olio dedicato?\n\nPer i motori a gas esistono oli formulati per questo impiego. Due esempi nel nostro catalogo, entrambi 5W-40 sintetici:\n- Selenia Multipower Gas 5W-40, ACEA C3\n- WRC Ultraplus 5W-40 Gas\n\nControlla sempre le indicazioni del costruttore dell'auto e dell'impianto. "+DM+"\n\n"+SPED+END+"\n\n#gpl #metano #oliomotore #autoevostore #lubrificanti #selenia",
 ['Auto a GPL o metano?','Olio dedicato per motori a gas','Selenia Multipower Gas e WRC Ultraplus 5W-40 Gas','Controlla le indicazioni del costruttore','Scrivici targa e modello in DM'])
k=car('tip03',230,[
 dict(cover=True,lines=[('DEXOS:',WHITE,96),('COS\'È?',CYc,96)],body='Una sigla che trovi su molti oli.',body2='Scorri'),
 dict(icon='book',lines=[('UNA SPECIFICA GM',WHITE,72)],body='Dexos è una specifica di General Motors, richiesta da molti veicoli del gruppo.'),
 dict(icon='check',lines=[('NEL LIBRETTO',WHITE,76)],body='Se il tuo richiede dexos2 o dexos D, la stessa dicitura deve comparire in etichetta.'),
 dict(icon='drop',lines=[('ESEMPI REALI',WHITE,76)],chips=['Petronas Syntium Prime XS 5W-30','GM Opel Dexos2 5W-30']),
 dict(CTA)])
post('tip03','2026-11-03T18:30',k,"Dexos: cosa significa?\n\nDexos è una specifica di General Motors. Se il libretto della tua auto richiede dexos2 o dexos D, la stessa dicitura deve essere riportata in etichetta.\n\nEsempi reali nel nostro catalogo: Petronas Syntium Prime XS 5W-30 (ACEA C3, dexos2, dexos D) e GM Opel Dexos2 5W-30.\n\n"+DM+"\n\n"+SPED+END+"\n\n#dexos #opel #oliomotore #autoevostore #petronas #lubrificanti",
 ['Dexos: cos\'è?','Dexos è una specifica General Motors','Controlla il libretto','Petronas Syntium Prime XS e GM Opel Dexos2','Scrivici targa e modello in DM'])
# ---------- Sabato: fiducia
img=add_brt(slide(lines=[('SPEDIZIONE',WHITE,84),('GRATUITA.',CYc,92)],body='In tutta Italia, consegna in 24/48 ore.',body2='Europa in 3-7 giorni lavorativi.',foot='Spediamo con BRT  ·  autoevostore.it',seed=101),1015)
save(img,'sat10_brt')
post('sat10_brt','2026-10-10T12:00',['sat10_brt'],"Spedizione gratuita in tutta Italia, consegna in 24/48 ore. Spediamo con BRT.\n\nEuropa in 3-7 giorni lavorativi (escluse Cipro e Malta). Reso entro 14 giorni.\n\nNon sei sicuro dell'olio giusto? "+DM+END+"\n\n#spedizionegratuita #brt #oliomotore #autoevostore #lubrificanti #ecommerce",['Spedizione gratuita in Italia in 24/48 ore con BRT, Europa 3-7 giorni lavorativi'])
save(slide(icon='chat',lines=[('PRIMA DI ORDINARE,',WHITE,64),('SCRIVICI.',CYc,92)],body='Targa e modello in DM: controlliamo noi la specifica giusta.',chips=['Assistenza lun-ven 9:00-18:00','Reso entro 14 giorni'],seed=102),'sat24_assistenza')
post('sat24_assistenza','2026-10-24T12:00',['sat24_assistenza'],"Prima di ordinare, scrivici.\n\nTarga e modello in DM: controlliamo noi la specifica giusta. Assistenza dal lunedì al venerdì, dalle 9:00 alle 18:00.\n\nReso entro 14 giorni. "+SPED+END+"\n\n#assistenzaclienti #oliomotore #autoevostore #lubrificanti #acquistionline",['Prima di ordinare scrivici: assistenza lun-ven 9:00-18:00'])
save(slide(lines=[('COSA TROVI SU',WHITE,64),('AUTOEVOSTORE.IT',CYc,72)],chips=['Olio motore auto','Olio cambio e differenziale','Fluidi ATF','Olio moto e 2 tempi','Olio idraulico'],seed=103),'sat31_catalogo')
post('sat31_catalogo','2026-10-31T12:00',['sat31_catalogo'],"Cosa trovi su autoevostore.it: solo oli e lubrificanti.\n\nOlio motore per auto, olio cambio e differenziale, fluidi ATF, olio moto e 2 tempi, olio idraulico. Marchi: Castrol, Mobil, Total, Petronas, Selenia, Mannol, WRC, BMW, Opel GM.\n\n"+DM+"\n\n"+SPED+END+"\n\n#oliomotore #lubrificanti #autoevostore #castrol #mobil #mannol #wrc",['Cosa trovi su autoevostore.it: olio motore, cambio, ATF, moto e 2 tempi, idraulico'])
# ---------- Domenica: domanda
save(slide(icon='check',lines=[('AUTO CON FILTRO',WHITE,70),('ANTIPARTICOLATO?',CYc,66)],big=('CERCA ACEA C',72),body='Gli oli della categoria C sono pensati per motori con filtro antiparticolato e catalizzatore.',seed=104),'sun11_dpf')
post('sun11_dpf','2026-10-11T18:30',['sun11_dpf'],"Auto con filtro antiparticolato (DPF/FAP)? Cerca ACEA C.\n\nGli oli della categoria C sono pensati per motori con filtro antiparticolato e catalizzatore. Poi controlla sempre viscosità e omologazioni richieste dal libretto.\n\n"+DM+"\n\n"+SPED+END+"\n\n#dpf #acea #oliomotore #autoevostore #lubrificanti #manutenzioneauto",['Auto con filtro antiparticolato? Cerca ACEA C'])
save(slide(icon='book',lines=[('DOVE TROVO',WHITE,76),('LA VISCOSITÀ?',CYc,80)],body='Nel libretto di uso e manutenzione, di solito nella sezione rifornimenti o dati tecnici.',body2='Cerca una sigla come 5W-30.',seed=105),'sun18_viscosita')
post('sun18_viscosita','2026-10-18T18:30',['sun18_viscosita'],"Dove trovo la viscosità giusta per la mia auto?\n\nNel libretto di uso e manutenzione, di solito nella sezione rifornimenti o dati tecnici. Cerca una sigla come 5W-30 o 5W-40.\n\nNon la trovi? "+DM+"\n\n"+SPED+END+"\n\n#viscosita #oliomotore #autoevostore #lubrificanti #manutenzioneauto",['Dove trovo la viscosità? Nel libretto di uso e manutenzione'])
save(slide(icon='check',lines=[('DEVI FARE',WHITE,76),('UN RABBOCCO?',CYc,80)],body="Controlla che viscosità e specifica siano quelle indicate nel libretto, prima di aggiungere olio.",seed=106),'sun25_rabbocco')
post('sun25_rabbocco','2026-10-25T18:30',['sun25_rabbocco'],"Devi fare un rabbocco? Prima controlla.\n\nViscosità e specifica dell'olio da aggiungere devono essere quelle indicate nel libretto del tuo veicolo.\n\n"+DM+"\n\n"+SPED+END+"\n\n#rabbocco #oliomotore #autoevostore #lubrificanti #manutenzioneauto",['Rabbocco olio: controlla viscosità e specifica nel libretto'])
# ---------- Storie
def S(key,date,alt,**kw):
    save(story(seed=300+len(CAL),**kw),key); st(key,date,alt)
T='T12:30'
bs=story(lines=[('SPEDIZIONE',WHITE,84),('GRATUITA',CYc,84)],body='Italia in 24/48 ore.',foot='Spediamo con BRT  ·  autoevostore.it',seed=399)
save(add_brt(bs,1380,1.1),'st10'); st('st10','2026-10-10'+T,'Spedizione gratuita in Italia con BRT')
S('st11','2026-10-11'+T,'Filtro antiparticolato? Cerca ACEA C',lines=[('LO SAPEVI?',CYc,56),('FILTRO',WHITE,76),('ANTIPARTICOLATO?',WHITE,60)],big=('ACEA C',112),body='Oli pensati per motori con DPF.',foot='autoevostore.it')
S('st12','2026-10-12'+T,'Che olio serve alla tua auto? Scrivici targa e modello',lines=[('CHE OLIO SERVE',WHITE,72),('ALLA TUA AUTO?',CYc,72)],body='Scrivici targa e modello in DM.',body2='Controlliamo noi la specifica giusta.',icon='chat')
S('st13','2026-10-13'+T,'Sintetico, semisintetico o minerale: lo dice il libretto',lines=[('SINTETICO',WHITE,76),('SEMISINTETICO',WHITE,60),('MINERALE',WHITE,76)],body='Quale serve alla tua auto?',body2='Lo dice il libretto.',foot='autoevostore.it')
S('st14','2026-10-14'+T,'Petronas su autoevostore.it',lines=[('PETRONAS',CYc,96)],chips=['Syntium Prime AV 5W-40','Syntium Prime XS 5W-30','Selenia WR Pure Energy 5W-30'],foot='autoevostore.it')
S('st15','2026-10-15'+T,'Reso entro 14 giorni',icon='return',lines=[('RESO ENTRO',WHITE,84),('14 GIORNI',CYc,92)],body='Acquisti con serenità.')
S('st16','2026-10-16'+T,'Dexos è una specifica General Motors',lines=[('LO SAPEVI?',CYc,56),('DEXOS È UNA',WHITE,72),('SPECIFICA GM',CYc,76)],body='Se il libretto la richiede, deve essere in etichetta.',foot='autoevostore.it')
S('st17','2026-10-17'+T,'Castrol su autoevostore.it',lines=[('CASTROL',CYc,96)],chips=['EDGE LongLife III 5W-30','EDGE 0W-20 C5','MAGNATEC 5W-30 A5','Transmax Axle EPX 80W-90'],foot='autoevostore.it')
S('st19','2026-10-19'+T,'Assistenza lunedì-venerdì 9:00-18:00',icon='chat',lines=[('ASSISTENZA',WHITE,84),('LUN-VEN',CYc,92)],body='Dalle 9:00 alle 18:00.',body2='Targa e modello in DM.')
S('st20','2026-10-20'+T,'GL-5: olio per cambi e differenziali, controlla il libretto',lines=[('LO SAPEVI?',CYc,56),('API GL-5',WHITE,92)],body='Olio per cambi e differenziali.',body2='Non tutti i cambi manuali lo ammettono: controlla il libretto.',foot='autoevostore.it')
S('st21','2026-10-21'+T,'Mannol su autoevostore.it',lines=[('MANNOL',CYc,96)],chips=['Longlife 504/507 5W-30','Classic 10W-40','Automatic Plus ATF','Ultra Gear Oil 8118 75W-90'],foot='autoevostore.it')
S('st22','2026-10-22'+T,'Spediamo anche in Europa in 3-7 giorni lavorativi',icon='globe',lines=[('SPEDIAMO ANCHE',WHITE,68),('IN EUROPA',CYc,84)],body='3-7 giorni lavorativi.',body2='Escluse Cipro e Malta.')
S('st23','2026-10-23'+T,'ATF: fluido per cambi automatici e servosterzi',lines=[('LO SAPEVI?',CYc,56),('ATF',WHITE,112)],body='Fluido per cambi automatici e servosterzi.',body2='Ogni cambio vuole il suo.',foot='autoevostore.it')
S('st24','2026-10-24'+T,'Selenia su autoevostore.it',lines=[('SELENIA',CYc,96)],chips=['WR Forward 0W-30','WR Pure Energy 5W-30','Multipower Gas 5W-40','20K 10W-40'],foot='autoevostore.it')
bs=story(lines=[('SPEDIZIONE',WHITE,84),('GRATUITA',CYc,84)],body='Italia in 24/48 ore.',foot='Spediamo con BRT  ·  autoevostore.it',seed=398)
save(add_brt(bs,1380,1.1),'st26'); st('st26','2026-10-26'+T,'Spedizione gratuita in Italia con BRT')
S('st27','2026-10-27'+T,'Per GPL e metano esistono oli dedicati',lines=[('LO SAPEVI?',CYc,56),('GPL E METANO:',WHITE,72)],body='esistono oli pensati per i motori a gas.',body2='Es. Selenia Multipower Gas 5W-40.',foot='autoevostore.it')
S('st28','2026-10-28'+T,'WRC su autoevostore.it',lines=[('WRC',CYc,110)],chips=['Olio motore','Olio cambio','ATF','Olio 2 tempi','Olio idraulico'],foot='autoevostore.it')
S('st29','2026-10-29'+T,'Dubbi sull olio? Scrivici targa e modello',icon='chat',lines=[('DUBBI SULL\'OLIO?',WHITE,68)],body='Scrivici targa e modello in DM.',body2='Assistenza lun-ven 9:00-18:00.')
S('st30','2026-10-30'+T,'0W-20 solo se prescritto dal libretto',lines=[('LO SAPEVI?',CYc,56),('0W-20',WHITE,120)],body='È una viscosità molto fluida.',body2='Usala solo se il libretto la prescrive.',foot='autoevostore.it')
S('st31','2026-10-31'+T,'Mobil, Total, BMW e Opel GM su autoevostore.it',lines=[('ANCHE QUI',CYc,60)],chips=['Mobil 1 ESP 5W-30','Total Quartz Ineo MC3 5W-30','BMW TwinPower Turbo 0W-30','Opel GM Dexos2 5W-30'],foot='autoevostore.it')
S('st32','2026-11-02'+T,'Reso entro 14 giorni',icon='return',lines=[('RESO ENTRO',WHITE,84),('14 GIORNI',CYc,92)],body='Acquisti con serenità.')
S('st33','2026-11-03'+T,'Olio 2 tempi per moto e motori marini',lines=[('OLIO 2 TEMPI',WHITE,76)],body='Moto e motori marini.',chips=['Castrol Power 1 Ultimate 2T','WRC Premix 2T+','MANNOL 7207 Outboard Marine'],foot='autoevostore.it')
S('st34','2026-11-04'+T,'Assistenza lunedì-venerdì 9:00-18:00',icon='chat',lines=[('ASSISTENZA',WHITE,84),('LUN-VEN',CYc,92)],body='Dalle 9:00 alle 18:00.',body2='Targa e modello in DM.')
S('st35','2026-11-05'+T,'Il libretto ha l ultima parola',icon='book',lines=[('IL LIBRETTO',WHITE,80),('HA L\'ULTIMA PAROLA',CYc,56)],body='Viscosità e specifica: confrontale sempre.')
bs=story(lines=[('SPEDIZIONE',WHITE,84),('GRATUITA',CYc,84)],body='Italia in 24/48 ore.',foot='Spediamo con BRT  ·  autoevostore.it',seed=397)
save(add_brt(bs,1380,1.1),'st36'); st('st36','2026-11-06'+T,'Spedizione gratuita in Italia con BRT')
S('st37','2026-11-07'+T,'Weekend: scrivici targa e modello',icon='chat',lines=[('BUON WEEKEND',WHITE,72)],body='Scrivici targa e modello in DM:',body2='controlliamo noi la specifica giusta.')
CAL.sort(key=lambda c:(c['dt'],c['kind']))
json.dump(CAL,open(ROOT+'/data/calendar_2026-10.json','w'),ensure_ascii=False,indent=1)
print(len(CAL),'items')
