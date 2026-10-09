# AUTO EVO STORE — pipeline social (RUNBOOK)

Archivio di lavoro per i social di AUTO EVO STORE (autoevostore.it, solo oli e lubrificanti). Metricool brand **7275875** (Instagram + Facebook insieme, fuso Europe/Rome). Piano Metricool Starter: pubblicazioni illimitate (soglia Fair Use 600/mese: ne facciamo ~60).

## Regole fisse (non negoziabili)
- Solo prodotti reali, attivi sul sito Shopify con scorta > 0 (usa `data/products.psv` e ricontrolla via Shopify: `status:active`, `totalInventory`). Mai dati inventati. I prodotti Selenia 0W-20 sono archiviati: NON usarli.
- Nessun prezzo nei post. Nessun nome personale. Logo AUTO EVO STORE su ogni grafica (lo mettono già i template).
- Dati di servizio sempre uguali: spedizione gratuita in Italia 24/48 ore; Europa 3-7 giorni lavorativi (escluse Cipro e Malta); reso entro 14 giorni; assistenza lun-ven 9:00-18:00; corriere BRT (logo in `assets/brt_logo.png`, funzione `add_brt`).
- Chiusura caption: "autoevostore.it (link in bio)" + hashtag. Per i dubbi: "Scrivici targa e modello in DM: verifichiamo noi la specifica giusta."
- Non toccare eBay. Non attivare prodotti in bozza su Shopify. Non scrivere "sostituzione gratuita".
- Se un fatto tecnico non è verificabile da titolo/tag Shopify o da fonte ufficiale, NON scriverlo.

## Ritmo giornaliero (1 feed + 1 storia al giorno, tutti i giorni)
Feed 18:30 (sabato 12:00): lun/gio prodotto (scheda), mar consiglio (carosello 5 slide), mer carosello/spec, ven reel, sab fiducia, dom domanda.
Storie 12:30: a rotazione "Lo sapevi?", servizio (BRT/reso/assistenza/Europa), marchio.
Domenica 8 nov e ogni inizio mese: storia "bilancio del mese" con statistiche REALI di Metricool.

## Come si fa
1. `git pull`; guarda `data/calendar_*.json` e `getScheduledPosts` (Metricool) per trovare il primo giorno senza contenuto: coprire sempre almeno i prossimi 14 giorni.
2. Genera le grafiche con `tools/cal_lib.py` (`slide()`, `story()`, `add_brt()`), vedi `tools/gen_calendar.py` come esempio; schede prodotto: `tools/product_card.py`. Per le immagini usa solo i font/logo in `assets/`. Salva in `media/<anno-mese>/`.
3. `git add -A && git commit && git push` (il push deve riuscire PRIMA di programmare: Metricool legge i file da `https://raw.githubusercontent.com/autoevoricambi-afk/autoevostore-social/main/<percorso>`).
4. Programma con `createScheduledPost` (blogId 7275875): providers facebook+instagram; `facebookData.type` / `instagramData.type` = `POST` o `STORY` (storia: `text` vuoto); `publicationDate` in Europe/Rome; `mediaAltText` per ogni immagine; carosello = più URL in `media`.
5. Verifica con `getScheduledPosts` che ogni giorno abbia il suo contenuto; annota in `data/ledger.md` cosa hai usato (prodotto/tema) per non ripetere entro 8 settimane.
6. Alla fine riassumi in 3 righe cosa hai programmato e se qualcosa non ha funzionato.

Prodotti già usati in post (ottobre-novembre 2026): Petronas Syntium Prime XS/AV, Castrol EDGE LongLife III 5W-30, Mannol ATF/8118, Mobil 1 ESP 5W-30, Castrol EDGE 0W-20 C5, Total Quartz Ineo MC3, BMW TwinPower Turbo LL-04. Temi usati: vedi `data/calendar_2026-10.json`.
