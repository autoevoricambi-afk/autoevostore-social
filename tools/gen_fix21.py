"""Carosello 21/10: 5 controlli prima di ordinare (coerente con caption e alt text), con flaconi reali."""
import sys,os; sys.path.insert(0,os.path.dirname(__file__))
from photo_lib import *
O='2026-10/fix/'
M='mobil1_esp_5w30'
save(hero(M,'Guida',['Cinque controlli.','Un ordine preciso.'],sub='Una guida da tenere a portata di mano.',fonts=66),O+'car21_1.png')
save(split(M,'01 · Nome completo',['Marca,','linea e','versione.'],['Esempio: Mobil 1 ESP 5W-30','Il nome completo identifica il prodotto esatto.'],fonts=60),O+'car21_2.png')
save(bigspec(M,'5W-30','02 · Gradazione',['Confronta la sigla SAE','con il libretto.'],fonts=62),O+'car21_3.png')
save(split('castrol_edge_ll3_5w30','03 · Specifiche',['Indicazioni','del','costruttore.'],['Esempio: ACEA C3, VW 504.00/507.00, MB 229.52','Confrontale con il libretto.'],fonts=60),O+'car21_4.png')
save(hero('petronas_xs_5w30','04 · Formato',['Verifica i litri','del singolo flacone.'],chips=('Esempio: flacone da 1 litro',),fonts=64),O+'car21_5.png')
save(lineup([M]*5,'05 · Quantità',['Controlla quanti','flaconi ordini.'],cap='5 flaconi da 1 litro = 5 litri in totale',fonts=64),O+'car21_6.png')
save(text_slide('Ora puoi scegliere',['Qualcosa non coincide?','Scrivici prima.'],body='Targa e modello in DM: verifichiamo noi la specifica giusta.',key='castrol_edge_0w20_c5',fonts=64),O+'car21_7.png')
