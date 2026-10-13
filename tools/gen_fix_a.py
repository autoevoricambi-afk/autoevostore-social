"""Rifacimento feed 24/10 -> 5/11 con flaconi reali, testo coerente con caption/alt text programmati."""
import sys,os; sys.path.insert(0,os.path.dirname(__file__))
from photo_lib import *
O='2026-10/fix/'
# 24/10 12:00
save(text_slide('Prima di ordinare',['Un dubbio prima.','Una scelta più sicura.'],body='Scrivici modello, anno e motorizzazione.\nAssistenza lun–ven · 9:00–18:00',key='petronas_prime_av',fonts=62),O+'f24.png')
# 25/10 18:30
save(hero('total_ineo_mc3','Rabbocco',['Prima verifica.'],chips=('Controlla il libretto','Prodotto già usato'),sub='Non scegliere un olio solo perché ha la stessa gradazione.',fonts=72),O+'f25.png')
# 27/10 carosello GPL/metano
G='selenia_multipower_gas'
save(hero(G,'GPL o metano?',['Parti dal veicolo.'],sub='Controlla le indicazioni del costruttore e dell\'impianto.',fonts=70),O+'c27_1.png')
save(hero(G,'Selenia Multipower Gas',['5W-40'],chips=('Consulta la scheda prodotto',),fonts=84),O+'c27_2.png')
save(framed('../products/wrc_ultraplus_5w40_gas_graphic.jpg','WRC Ultraplus 5W-40 Gas',['Formato 1 L'],sub='Consulta la scheda prodotto.',fonts=64),O+'c27_3.png')
save(duo(G,'petronas_prime_av','Confronta i dati',['Gradazione e specifiche','devono essere quelle previste.'],['Selenia Multipower Gas','5W-40 · ACEA C3'],['Petronas Prime AV','5W-40 · ACEA C3'],fonts=56),O+'c27_4.png')
save(text_slide('Scegli con supporto',['Scrivici modello, anno','e motorizzazione.'],body='In privato: ti aiutiamo a verificare la scelta.',key='petronas_xs_5w30',fonts=64),O+'c27_5.png')
# 28/10 carosello ACEA e API
save(lineup(['petronas_prime_av','total_ineo_mc3','mobil1_esp_5w30'],'ACEA e API',['Leggiamole insieme.'],cap='Tre famiglie di indicazioni da distinguere',fonts=70),O+'c28_1.png')
save(bigspec('petronas_prime_av','5W-40','SAE · Gradazione',['Una sigla come 5W-40','descrive la viscosità.'],fonts=58),O+'c28_2.png')
save(split('total_ineo_mc3','ACEA e API',['Categorie','prestazionali.'],['Identificano categorie prestazionali degli oli','Esempio: ACEA C3, API SN PLUS'],fonts=58),O+'c28_3.png')
save(split('petronas_prime_av','Specifiche OEM',['Indicazioni','del costruttore.'],['Da confrontare con il libretto','Esempio: MB 229.51, VW 505.01'],fonts=58),O+'c28_4.png')
save(duo('selenia_wr_pure_energy_5w30','total_ineo_mc3','La categoria corretta',['Scegli quella prevista.'],['Selenia WR Pure Energy','ACEA C2'],['Quartz Ineo MC3','ACEA C3'],fonts=60),O+'c28_5.png')
# 31/10 catalogo
save(lineup(['castrol_edge_ll3_5w30','mannol_atf_dexron3','mannol_8118','castrol_power1_2t'],'Catalogo',['Ogni impiego,','il suo lubrificante.'],cap='Motore · Trasmissione · ATF · 2 tempi',fonts=68),O+'f31.png')
# 1/11 Europa
save(text_slide('Spedizioni in Europa',['18 Paesi UE.','Costi trasparenti.'],body='Destinazioni e tariffe sul sito.\nCosto esatto al checkout per gli ordini serviti.',key='castrol_edge_ll3_5w30',fonts=72),O+'f01n.png')
# 2/11 8118
save(split('mannol_8118','MANNOL',['Ultra Gear','Oil 8118'],['75W-90 · API GL-5','Controlla l\'impiego','Verifica la specifica della trasmissione'],fonts=60),O+'f02n.png')
# 3/11 carosello dexos
D='opel_gm_dexos2_1l'
save(hero(D,'dexos',['Conta la sigla completa.'],sub='Controlla la versione richiesta dal tuo veicolo.',fonts=68),O+'c03_1.png')
save(text_slide('Parti dal libretto',['Annota la specifica','completa.'],body='È quella prevista dal costruttore.',key='castrol_edge_0w20_c5',fonts=64),O+'c03_2.png')
save(split(D,'Poi leggi la scheda',['Nome,','gradazione,','indicazioni.'],['Confronta nome, gradazione e indicazioni del prodotto','Esempio: dexos2 · ACEA C3'],fonts=58),O+'c03_3.png')
save(duo('opel_gm_dexos2_1l','total_ineo_mc3','Non fermarti al 5W-30',['Stessa gradazione,','indicazioni diverse.'],['GM Opel Dexos2','5W-30 · dexos2'],['Quartz Ineo MC3','5W-30 · API SN PLUS'],fonts=56),O+'c03_4.png')
save(text_slide('Un confronto utile',['Scrivici in privato','prima dell\'ordine.'],body='Modello, anno e motorizzazione: verifichiamo insieme.',key='castrol_edge_ll3_5w30',fonts=64),O+'c03_5.png')
# 5/11 BMW
save(bigspec('bmw_twinpower_ll04_0w30','0W-30','BMW TwinPower Turbo',['Longlife-04'],chips=('ACEA C3','API SN','BMW LL-04'),fonts=72),O+'f05n.png')
print('ok')
