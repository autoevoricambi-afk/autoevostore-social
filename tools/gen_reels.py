from ae_slides import *
import subprocess, os
CYc=CY+(255,)
def sc(**k): return slide(W=1080,H=1920,logo_w=520,logo_top=110,sc=1.25,**k)
reels={
'r16_olio':[
 dict(lines=[('CHE OLIO SERVE',WHITE,84),('ALLA MIA AUTO?',CYc,92)],body='4 passaggi, due minuti.'),
 dict(icon='book',lines=[('1 · APRI IL LIBRETTO',WHITE,70)],body='Cerca la viscosità richiesta.',big=('es. 5W-30',84)),
 dict(icon='check',lines=[('2 · LE SPECIFICHE',WHITE,70)],body='ACEA, API e omologazioni del costruttore devono coincidere.'),
 dict(icon='chat',lines=[('3 · NON SEI SICURO?',WHITE,70)],body='Scrivici targa e modello in DM.',body2='Verifichiamo noi la specifica giusta.'),
 dict(icon='truck',lines=[('4 · ORDINA',WHITE,76),('E RICEVI IN 24/48H',CYc,60)],body='Spedizione gratuita in Italia.',cta='autoevostore.it'),
],
'r23_consegna':[
 dict(lines=[("DALL'ORDINE",WHITE,92),('ALLA CONSEGNA.',CYc,92)],body='Come funziona, in 4 mosse.'),
 dict(icon='check',lines=[('1 · ORDINI',WHITE,76)],body='Scegli l\'olio su autoevostore.it.'),
 dict(icon='chat',lines=[('2 · CONTROLLIAMO',WHITE,70)],body='Assistenza lun-ven 9:00-18:00.',body2='Dubbi? Targa e modello in DM.'),
 dict(icon='truck',lines=[('3 · SPEDIAMO',WHITE,76)],body='Gratis in Italia in 24/48h.',body2='Europa in 3-7 giorni lavorativi.'),
 dict(icon='return',lines=[('4 · RESO ENTRO',WHITE,70),('14 GIORNI',CYc,84)],body='Acquisti con serenità.',cta='autoevostore.it'),
],
'r30_targa':[
 dict(lines=[('NON SAI',WHITE,92),("CHE OLIO SCEGLIERE?",CYc,66)],body='C\'è un modo semplice.'),
 dict(icon='chat',lines=[('SCRIVICI IN DM',WHITE,76)],body='Targa e modello della tua auto.',body2='Esempio: "AB123CD, Fiat Panda 1.2"'),
 dict(icon='check',lines=[('TI DICIAMO',WHITE,76),('LA SPECIFICA GIUSTA',CYc,60)],body='Viscosità, ACEA, API e omologazioni.'),
 dict(icon='truck',lines=[('POI ORDINI',WHITE,76)],body='Spedizione gratuita in Italia, 24/48h.',cta='autoevostore.it'),
],
'r06_marchi':[
 dict(lines=[('SOLO OLI',WHITE,92),('E LUBRIFICANTI.',CYc,84)],body='I marchi su autoevostore.it'),
 dict(icon='drop',lines=[('I MARCHI',WHITE,80)],body='Castrol · Mobil · Total',body2='Petronas · Selenia · Mannol\nWRC · BMW · Opel GM'),
 dict(icon='book',lines=[('SCEGLI PER',WHITE,70),('VISCOSITÀ E SPECIFICA',CYc,52)],body='Controlla il libretto della tua auto.'),
 dict(icon='chat',lines=[('LA SCELTA GIUSTA',WHITE,66)],body='Scrivici targa e modello in DM.'),
 dict(icon='truck',lines=[('SPEDIZIONE GRATUITA',WHITE,56),('IN ITALIA 24/48H',CYc,62)],body='Europa 3-7 giorni lavorativi.',cta='autoevostore.it'),
],
}
for name,scenes in reels.items():
    d='reels/'+name; os.makedirs(d,exist_ok=True)
    for i,s in enumerate(scenes): sc(seed=100+i*3,cover=False,**s).save(f'{d}/s{i}.png')
