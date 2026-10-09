from ae_slides import *
W,H=1080,1350
CYc=CY+(255,)
def save(img,name): img.save('out/'+name+'.png')
# ---- Carosello 21 ott
s=[]
s.append(dict(cover=True,lines=[('5 COSE DA LEGGERE',WHITE,84),('SULLA SCHEDA DI UN OLIO.',CYc,70)],body='Prima di ordinare, controlla queste.',body2='Scorri per vederle'))
s.append(dict(icon='drop',lines=[('1 · VISCOSITÀ',WHITE,80)],big=('5W-30',104),body='Il primo numero, con la W, dice come scorre a freddo. Il secondo, la protezione a caldo.'))
s.append(dict(icon='check',lines=[('2 · SPECIFICA ACEA',WHITE,72)],big=('C3',104),body='Indica il tipo di motore per cui è pensato l\'olio. Esempio: C3 per motori con filtro antiparticolato.'))
s.append(dict(icon='book',lines=[('3 · SPECIFICA API',WHITE,72)],big=('SN',104),body='La S indica i motori a benzina. La seconda lettera è il livello di qualità.'))
s.append(dict(icon='check',lines=[('4 · OMOLOGAZIONI',WHITE,72)],big=('VW · MB · BMW',72),body='Sono i via libera dei costruttori. Se il libretto le cita, devi ritrovarle nella scheda.'))
s.append(dict(icon='book',lines=[('5 · IL LIBRETTO',WHITE,76)],big=('HA L\'ULTIMA PAROLA',54),body='Confronta sempre la scheda con il libretto di uso e manutenzione della tua auto.'))
s.append(dict(icon='chat',lines=[('NON SEI SICURO',WHITE,84),("DELL'OLIO?",CYc,84)],body='Scrivici targa e modello in DM:',body2='controlliamo noi la specifica giusta.',cta='autoevostore.it  (link in bio)'))
for k,d in enumerate(s): save(slide(n=len(s),i=k,seed=40+k,**d),f'car21_{k+1}')
# ---- Carosello 28 ott
s=[]
s.append(dict(cover=True,lines=[('ACEA C3 E API SN',WHITE,84),('COSA SIGNIFICANO.',CYc,76)],body='Due sigle, due minuti.',body2='Scorri per capirle'))
s.append(dict(icon='check',lines=[('ACEA C3',WHITE,80)],big=('LA LETTERA E IL NUMERO',50),body='C: oli per motori con filtro antiparticolato e catalizzatore. Il numero 3 indica il livello di prestazione.'))
s.append(dict(icon='book',lines=[('API SN',WHITE,80)],big=('S + N',96),body='S: motori a benzina. La seconda lettera è il livello di qualità: più avanti nell\'alfabeto, più recente.'))
s.append(dict(icon='drop',lines=[('UN ESEMPIO REALE',WHITE,68)],big=('5W-40',104),body='Petronas Syntium Prime AV.',chips=['SAE 5W-40','API SN/CF','ACEA C3']))
s.append(dict(icon='chat',lines=[('CONTROLLA IL LIBRETTO',WHITE,70),('O SCRIVICI IN DM.',CYc,70)],body='Targa e modello: verifichiamo noi la specifica.',cta='autoevostore.it  (link in bio)'))
for k,d in enumerate(s): save(slide(n=len(s),i=k,seed=60+k,**d),f'car28_{k+1}')
# ---- Post 31 ott Europa
save(slide(icon='globe',lines=[('SPEDIAMO ANCHE',WHITE,84),('IN EUROPA.',CYc,92)],body='Consegna in 3-7 giorni lavorativi.',chips=['Europa 3-7 giorni lavorativi','Spedizione tracciata','Costo calcolato al checkout'],foot='Escluse Cipro e Malta  ·  autoevostore.it',seed=71),'post31_europa')
# ---- Post 7 nov reso e assistenza
save(slide(icon='return',lines=[('RESO ENTRO',WHITE,84),('14 GIORNI.',CYc,92)],body='E assistenza prima di ordinare.',chips=['Reso entro 14 giorni','Assistenza lun-ven 9:00-18:00','Targa e modello in DM'],seed=72),'post07_reso')
# ---- Storie 1080x1920
def story(**k): return slide(W=1080,H=1920,logo_w=560,logo_top=130,sc=1.25,**k)
save(story(lines=[('LO SAPEVI?',CYc,56),('COSA SIGNIFICA',WHITE,74),('5W-30?',CYc,112)],body='5W: come scorre a freddo.',body2='(la W sta per winter)\n30: la viscosità a caldo.',foot='autoevostore.it',seed=81),'story25_5w30')
save(story(lines=[('CAMBIO',WHITE,84),('MANUALE O',CYc,76),('AUTOMATICO?',CYc,76)],body='Ogni cambio vuole il suo olio.',body2='Scrivici targa e modello in DM.',chips=['MANUALE','AUTOMATICO'],seed=82),'story01_cambio')
