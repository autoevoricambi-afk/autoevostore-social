# Strategia contenuti AUTO EVO STORE — Reel prodotto (dal 1° novembre 2026)

## Perché i Reel
- Dati reali Metricool (set-ott 2026). Il Reel "GM dexos2 5W-30 5 L" del 23/10 ha fatto 126 visualizzazioni IG (reach 115) e 25 su FB. Gli altri Reel ne hanno fatte 21-30 su IG e 0-4 su FB. I post statici raggiungono 2-5 persone.
- Era l'unico Reel dedicato a **un solo prodotto**, con foto reali (dettaglio → fronte → retro). Gli altri erano temi generici: marchi, etichetta, errori.
- Instagram distribuisce un Reel nuovo prima a un piccolo gruppo di chi non ci segue. I segnali che contano sono tempo di visione, like e condivisioni via DM rispetto alla copertura (Mosseri, gennaio 2025). Con 8 follower è l'unico modo realistico per crescere.

## Cosa copiamo dai grandi (e come facciamo meglio)
- **Ferrari (teaser Hamilton 2025):** un dettaglio alla volta, "far intuire prima di mostrare". Per noi: apertura sul dettaglio dell'etichetta, poi il flacone intero.
- **Porsche:** pochi contenuti, molto curati, serie riconoscibili, primi piani. Nel secondo trimestre 2026 è prima per interazioni con meno post dei concorrenti (Emplifi). Per noi: un formato fisso, sempre di qualità cinematografica, mai due grafiche uguali di fila.
- **Petronas "F1 Uncovered":** spiega i fluidi uno alla volta. Per noi: ogni Reel insegna a leggere una sigla (ACEA, VW 504/507, dexos, FIAT 9.55535…).
- **Il nostro "meglio":** loro vendono un sogno, noi la certezza dell'olio giusto. Ogni Reel chiude con il servizio che i grandi marchi non danno: "targa, modello e anno in DM, verifichiamo noi la specifica". Seguono spedizione gratuita 24/48 ore BRT e reso entro 14 giorni.

## Formato standard "Reel prodotto" (tools/reel_prodotto.py)
| Secondi | Scena | Regola |
|---|---|---|
| 0-2 | Macro dell'etichetta + domanda di 3-5 parole | Il gancio deve essere leggibile dal primo fotogramma |
| 2-5,2 | Flacone intero, avvicinamento lento, marchio e nome | Una sola idea |
| 5,2-8,4 | Le sigle dell'etichetta, una alla volta | Solo sigle presenti nel titolo o nei tag Shopify |
| 8,4-10,6 | Spedizione gratuita 24/48 ore BRT, Europa 3-7 giorni, reso 14 giorni | Fiducia |
| 10,6-13 | "Mandalo a chi deve fare il tagliando" + DM + link in bio | Condivisione + conversione |

- Formato 1080x1920, 24 fps, 13 secondi, audio originale (nessuna licenza). Testi grandi, dentro le zone sicure. Copertina = flacone con il nome.
- Caption: prima riga = gancio, poi nome completo e sigle, la CTA per i DM, il servizio. **Al massimo 5 hashtag** (limite Instagram da dicembre 2025).
- IG: "autoevostore.it (link in bio)", che porta alla pagina https://www.autoevostore.it/pages/link. FB: link cliccabile alla scheda prodotto con UTM `utm_campaign=autoevo_ott_nov_2026`, `utm_content=ae-AAAA-MM-GG-HHMM-reel`.

## Calendario
- Un Reel prodotto al giorno nello slot feed (18:30; sabato 12:00), a rotazione su **tutti** i prodotti attivi con scorta e foto in `products/`. Ogni prodotto torna dopo almeno 4 settimane con un gancio diverso.
- I contenuti di domanda, carosello e consiglio restano 2-3 volte a settimana. Le storie 12:30 e 19:00 rilanciano il Reel del giorno: aggiungere a mano dall'app lo sticker link alla scheda.
- Piano attuale: `data/reel_prodotto_plan.json` (9/11-14/12).

## Serie ricorrenti (prossimi sviluppi)
1. **Leggi l'etichetta:** una sigla spiegata a partire dal flacone reale.
2. **Che sigla è?:** si mostra un dettaglio parziale, la risposta arriva alla fine del Reel.
3. **Mito o verità:** frasi verificabili, risposta nell'ultimo fotogramma.
4. **Dal magazzino a te:** pacco, BRT, tempi di consegna, reso.
5. **Due flaconi, stessa viscosità:** confronto di omologazioni. Mai affermare compatibilità dalla sola viscosità.

## Misura (ogni domenica, routine)
- Per ogni Reel, da Metricool: visualizzazioni (IGRE23), copertura (IGRE11), tempo medio di visione (IGRE24), condivisioni (IGRE21), salvataggi (IGRE12). Su FB: FBRE10 e FBRE11.
- Benchmark da battere: 126 visualizzazioni IG (GM dexos2). Si tengono i ganci migliori e si cambia **una sola cosa alla volta** (gancio, durata o audio).
- Si annota tutto in `data/ledger.md`.

## Cosa richiede il titolare
- Impostare il link del profilo IG/FB su https://www.autoevostore.it/pages/link.
- Opzionale: scegliere un audio di tendenza dal catalogo Instagram (Metricool `audioConfiguration`) per i Reel con più resa.
- I Trial Reels richiedono 1.000 follower: per ora non sono disponibili.
- Instagram Shopping (tag prodotto cliccabili sulle foto): da attivare con il canale "Facebook e Instagram" di Shopify.
