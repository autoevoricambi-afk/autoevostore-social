"""Contenuti con foto reali: carosello 9/10, storie 9/10, schede prodotto sostitutive."""
import sys,os; sys.path.insert(0,os.path.dirname(__file__))
from photo_lib import *
O='2026-10/'
# --- carosello di oggi (5 slide)
K='petronas_prime_av'; S='selenia_k_pure_energy_5w40'
save(duo(K,S,'Stesso grado: 5W-40',['Non tutti i 5W-40','sono uguali.'],['Petronas Syntium Prime AV','MB 229.51 · VW 505.01'],['Selenia K Pure Energy','FIAT 9.55535-S2']),O+'car09_1.jpg')
save(hero(K,'Petronas Syntium Prime AV',['5W-40'],chips=('ACEA C3','MB 229.51','VW 505.01')),O+'car09_2.jpg')
save(hero(S,'Selenia K Pure Energy',['5W-40'],chips=('ACEA C3','FIAT 9.55535-S2')),O+'car09_3.jpg')
save(text_slide('Cosa dice il numero',['La viscosità','è solo metà della scelta.'],body='5W-40 indica come scorre l’olio. Le omologazioni (MB, VW, FIAT...) indicano per quali motori l’olio è approvato. Cerca quella scritta nel libretto.',fonts=64,chips=('MB 229.51','VW 505.01','FIAT 9.55535-S2')),O+'car09_4.jpg')
save(text_slide('Il prossimo passo',['Targa, modello','e anno.'],body='Mandaceli in DM: verifichiamo noi la specifica giusta. Spedizione gratuita in Italia, consegna in 24/48 ore.',key='mobil1_esp_5w30',fonts=70),O+'car09_5.jpg')
# --- sequenza storie 9/10 (4)
H=1920
save(text_slide('Domanda',['Sai quale specifica','richiede la tua auto?'],body='Rispondi a questa storia: ti diciamo cosa controllare.',W=1080,H=H,fonts=68),O+'st09_1.jpg')
save(text_slide('Attenzione',['5W-30 o 5W-40','non bastano.'],body='Conta l’omologazione indicata dal costruttore nel libretto.',W=1080,H=H,fonts=72),O+'st09_2.jpg')
save(hero(K,'Un esempio',['Petronas 5W-40 AV'],chips=('ACEA C3','MB 229.51','VW 505.01'),H=H,fonts=64),O+'st09_3.jpg')
save(text_slide('Scrivici in DM',['Targa + modello','+ anno.'],body='Verifichiamo noi la specifica giusta. Spedizione gratuita in Italia, 24/48 ore.',key='castrol_edge_0w20_c5',W=1080,H=H,fonts=76),O+'st09_4.jpg')
# --- schede prodotto (feed)
save(hero('petronas_xs_5w30','Petronas Syntium Prime XS',['5W-30'],chips=('ACEA C3','dexos2 / dexos D','API SN')),O+'prod14_xs.jpg')
save(split('mobil1_esp_5w30','Mobil 1',['ESP','5W-30'],['Olio motore sintetico','ACEA C3','BMW LL-04','MB 229.52','VW 504.00 / 507.00']),O+'prod15_mobil.jpg')
save(bigspec('castrol_edge_ll3_5w30','5W-30','Castrol EDGE Professional',['LongLife III'],chips=('ACEA C3','VW 504.00/507.00','MB 229.52')),O+'prod19_castrol.jpg')
save(bigspec('castrol_edge_0w20_c5','0W-20','Castrol EDGE',['C5'],chips=('ACEA C5/C6','dexos1 Gen 3','MB 229.71'),fonts=70),O+'prod22_c5.jpg')
save(hero('mannol_atf_dexron3','MANNOL Automatic Plus ATF',['Dexron III'],chips=('Cambi automatici','Servosterzo','TO-2')),O+'prod26_atf.jpg')
save(bigspec('total_ineo_mc3','5W-30','TotalEnergies Quartz',['Ineo MC3'],chips=('ACEA C3','API SN PLUS','Low SAPS')),O+'prod29_total.jpg')
save(split('mannol_8118','MANNOL',['Ultra Gear','Oil 8118'],['Olio semisintetico','SAE 75W-90','API GL-5','SAE J2360','Cambi e differenziali']),O+'prod02_8118.jpg')
save(bigspec('petronas_prime_av','5W-40','Petronas Syntium Prime',['AV'],chips=('ACEA C3','MB 229.51','VW 505.01'),fonts=70),O+'prod04_av.jpg')
print('ok')
