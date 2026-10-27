# Allineamento ChatGPT (grafica) + Claude (programmazione e controlli) — AUTO EVO STORE

Nessun dato sensibile in questo file: il repo e' pubblico.

## Ruoli
- ChatGPT: idee, sfondi e grafiche nello stile "pubblicitario" approvato dal titolare (prodotto protagonista, titoli grandi, luce e scena cinematografica, bottone in basso).
- Claude: verifica prodotti su Shopify (status ACTIVE, scorta > 0), testi/caption, programmazione Metricool, controllo qualita', ledger.
- Fonte unica di verita': Metricool (getScheduledPosts) + `data/ledger.md`. Prima di creare qualsiasi contenuto leggere entrambi; dopo, annotare nel ledger data, ora, prodotto/tema.

## Regole comuni (da CLAUDE.md, valgono per tutti)
- Solo prodotti reali attivi con scorta; flacone da 1 L o lattina singola, mai multipack; mai Selenia 0W-20. Nessun prezzo, nessun nome personale, logo AUTO EVO STORE su ogni grafica.
- Nessuna affermazione di compatibilita' dalla sola viscosita': citare omologazione e invitare a mandare targa/modello/anno in DM. Fatti tecnici solo da titolo/tag Shopify o etichetta.
- Servizio: spedizione gratuita Italia 24/48 ore; Europa 3-7 giorni lavorativi (escluse Cipro e Malta); reso 14 giorni; assistenza lun-ven 9-18; corriere BRT. Mai "sostituzione gratuita".
- Non ripetere prodotto/tema entro 8 settimane (vedi ledger). Layout sempre diversi tra contenuti consecutivi.

## Convenzioni tecniche uniche (oggi divergono: da uniformare)
- Chiusura caption IG: "autoevostore.it (link in bio)" + hashtag; FB: link con UTM.
- UTM: `utm_campaign=autoevo_ott_nov_2026` per tutto il calendario (non `autoevo_novembre_2026_v2`), `utm_content=ae-AAAA-MM-GG-HHMM`.
- Hashtag: stessa forma ovunque, minuscolo (#autoevostore #oliomotore ...).
- Storie: campo testo VUOTO. IG `isAiGenerated=true` quando lo sfondo e' generato con AI.
- Ritmo: feed 18:30 (sabato 12:00), storie 12:30 e 19:00; ogni settimana 3 Reel, 2 caroselli educativi, 1 contenuto fiducia.

## Prima di programmare (checklist)
1. Il prodotto e' nel ledger negli ultimi 56 giorni? Se si', cambiarlo.
2. Il giorno e' gia' coperto su Metricool? Se si', non duplicare: aggiornare quel post.
3. File pushati su main (Metricool legge da raw.githubusercontent.com)? Poi createScheduledPost.
