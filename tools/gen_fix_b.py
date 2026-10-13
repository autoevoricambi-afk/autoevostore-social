"""Feed 7/11 e 8/11 coerenti con caption (flaconi reali)."""
import sys,os; sys.path.insert(0,os.path.dirname(__file__))
from photo_lib import *
O='2026-10/fix/'
save(text_slide('Prima la verifica',['Poi l\'ordine.'],body='Hai dubbi sul prodotto? Contattaci prima di acquistare.\nReso entro 14 giorni dalla consegna.',key='castrol_edge_ll3_5w30',fonts=80),O+'f07n.png')
save(text_slide('Domanda della domenica',['Tu da dove cominci?'],bullets=('A · La gradazione','B · La marca','C · La specifica del costruttore'),key='mobil1_esp_5w30',fonts=76),O+'f08n.png')
