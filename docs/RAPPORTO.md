# Rapporto della notte tra il 22 e il 23 novembre 2026

## In una riga

I risultati reggono su tre insiemi di dati e due modelli di embedding, con misure controllate; due affermazioni che avevo fatto vanno però ridimensionate. Le bozze del post e della segnalazione sono pronte e nessuna è stata inviata.

## Cosa trovi

| Cosa | Dove |
|---|---|
| Risultati con intervalli di confidenza | `results/SINTESI.md` |
| Bozza del post LinkedIn, con la fonte di ogni numero | `docs/linkedin-post-bozza.md` |
| Bozza della segnalazione per Faiss, in inglese | `docs/faiss-issue-bozza.md` |
| Riproduzione minima da allegare alla segnalazione | `docs/repro_emeans_init_centroids.py` |
| Come rifare tutto | `README.md` |
| Registro dei lavori notturni | `data/night.log` |

## Cosa è stato fatto

- **Secondo corpus**: 210.000 abstract di arXiv, 2007-2021, testi lunghi.
- **Secondo modello di embedding**: `bge-base-en-v1.5`, 768 dimensioni, sulle notizie.
- **Esperimento rifatto da capo su tutti e tre gli insiemi**, con: due livelli di costo della ricerca (0,1% e 1% dell'indice letto), risultati salvati interrogazione per interrogazione, intervalli di confidenza, scomposizione delle cause del danno, misura anche con le liste ricostruite.
- **Tempi misurati a macchina libera**, un lavoro alla volta: sei ripetizioni in ordine alternato, carico della macchina registrato, k-means a sette numeri di iterazioni diversi.
- **Controllo della misura**: a parità di liste sondate, il recall calcolato dal nostro codice coincide con quello di un vero indice IVF di Faiss fino alla quarta cifra, su tutti e tre gli insiemi. La lettura a quota fissa usata nelle tabelle non ha un equivalente in Faiss: è verificata da un test contro una versione ovvia e lenta.
- **Correzione dimostrata con il codice di Faiss**, non solo con la nostra riscrittura.
- **Confronto generico e dimensione dell'aggiornamento**: lo stesso aggiornamento fatto con k-means, e con 50.000 testi nuovi invece di 10.000.
- **Tre revisioni indipendenti**: del codice notturno, della bozza della segnalazione letta "da manutentore", e una finale sui documenti. Hanno portato decine di correzioni; gli esiti sono in `_bmad-output/implementation-artifacts/spec-6-consolidamento.md`.

## Cosa regge

Recall@10 leggendo l'1% dell'indice, dopo dieci aggiornamenti (indice raddoppiato). In questa tabella i valori sono medie su tre seed, come in `results/SINTESI.md`; i file `exp_real_*.md`, la segnalazione e i controlli riportano mediane, che possono differire di un millesimo. Gli intervalli al 95% sulle interrogazioni sono in `results/SINTESI.md`: circa ±0,008 sulle notizie, ±0,005 su arXiv.

| | Notizie, 384 dim. | arXiv, 384 dim. | Notizie, 768 dim. |
|---|---|---|---|
| Mai aggiornare | 0,781 | 0,918 | 0,746 |
| Stessi testi in ordine casuale (senza deriva) | 0,830 | 0,939 | 0,807 |
| Uso ingenuo di e-means, liste ricostruite | 0,434 | 0,744 | 0,389 |
| Uso ingenuo, liste lasciate come sono | 0,052 | 0,069 | 0,049 |
| Mini-batch classico sui soli testi nuovi | 0,804 | 0,930 | 0,770 |
| Ricalcolo da zero, e-means 3 epoche | 0,839 | 0,943 | 0,814 |
| Ricalcolo da zero, e-means 10 epoche | 0,843 | 0,945 | 0,821 |

1. **La deriva costa**, in misura diversa secondo il corpus: 6 punti di recall sulle notizie, quasi 8 con il modello più grande, meno di 3 su arXiv. La maggior parte è deriva vera, non semplice crescita dell'indice.
2. **L'uso ingenuo di e-means rovina l'indice**, su tutti e tre gli insiemi e anche ricostruendo le liste. Dopo un solo aggiornamento da 10.000 testi il recall perde tra il 30% e il 58%.
3. **Il danno è in buona parte specifico di e-means.** Un solo aggiornamento, liste ricostruite, recall mediano:

   | Centroidi aggiornati sui soli testi nuovi | Notizie, 384 dim. | arXiv, 384 dim. | Notizie, 768 dim. |
   |---|---|---|---|
   | nessun aggiornamento | 0,828 | 0,931 | 0,792 |
   | e-means dai centroidi vecchi (uso ingenuo) | 0,417 | 0,656 | 0,332 |
   | e-means da righe a caso, senza centroidi vecchi | 0,472 | 0,733 | 0,381 |
   | k-means, una iterazione dai centroidi vecchi | 0,680 | 0,881 | 0,604 |
   | e-means di Faiss con massa iniziale e media mobile | 0,827 | 0,932 | 0,792 |

   Adattare 2.048 centroidi a 10.000 testi peggiora con qualunque algoritmo, ma e-means perde molto più di k-means e non fa meglio di una partenza senza centroidi vecchi. Con 50.000 testi nuovi il danno si riduce e resta: 0,723 contro 0,806 sulle notizie, 0,892 contro 0,929 su arXiv, 0,657 contro 0,773 con il modello a 768 dimensioni.
4. **La correzione è dimostrata con il codice di Faiss.** I centroidi di partenza hanno un peso quasi nullo, e il risultato restituito è la media dei soli testi nuovi. Dando un peso ai centroidi e leggendo la media mobile, lo stesso codice di Faiss passa, dopo dieci aggiornamenti, da 0,052 a 0,807 sulle notizie e da 0,069 a 0,930 su arXiv (mediane). Quanto pesa ciascuna delle due modifiche, e quanto la rianimazione dei cluster, è misurato solo con la nostra riscrittura: il peso iniziale conta di più, togliere le medie finali da solo non cambia nulla, la rianimazione peggiora le cose con le liste lasciate come sono e le migliora con le liste ricostruite.
5. **Corretto il difetto, e-means vale quanto il mini-batch classico**: la differenza è tra 1 e 5 millesimi di recall, in un caso a sfavore di e-means; a volte distinguibile dal rumore, mai di peso pratico.
6. **Ricalcolare da zero è la scelta giusta**: tre epoche arrivano a 0,2-0,7 punti dal riferimento a dieci epoche. Addestrare i centroidi richiede 4-7 secondi; la riassegnazione dei vettori non è compresa in quel tempo.
7. **Partire dai centroidi vecchi rileggendo tutto cambia poco o nulla.** Con il modello a 384 dimensioni, su entrambi i corpus, nessuna differenza di recall rispetto alla partenza da zero. Con il modello a 768 dimensioni, dando ai centroidi vecchi la massa a regime si guadagna mezzo punto (0,819 contro 0,814), poco ma coerente tra i seed. Il prezzo è rifare tre epoche a ogni aggiornamento.

## Cosa va ridimensionato

**"e-means è 5 volte più veloce."** È vero per l'errore di quantizzazione: tre epoche di e-means (4,3 secondi di addestramento dei centroidi) danno un errore che k-means non raggiunge in 25 iterazioni (22,6 secondi). La differenza di errore è piccola, lo 0,16%, ma si ripete in tutte le sei ripetizioni. Per il recall dipende da quanto indice si legge:

| A parità di recall | Notizie, 384 dim. | arXiv, 384 dim. | Notizie, 768 dim. |
|---|---|---|---|
| leggendo lo 0,1% dell'indice, k-means impiega | da 3,2 a 4,2 volte | da 2,5 a 3,2 volte | oltre 4,4 volte |
| leggendo l'1% dell'indice, k-means impiega | da 0,6 a 1,1 volte | da 1,1 a 2,1 volte | da 0,5 a 0,9 volte |

Con l'1% dell'indice letto il vantaggio sparisce sulle notizie e resta, fino a un fattore 2, su arXiv. Con lo 0,1% le differenze di recall su cui poggiano i rapporti sono di pochi millesimi: solo su arXiv il distacco è più grande della variabilità tra seed. Il post lo dice in questi termini.

Il confronto dei tempi è tra un ciclo in Python (e-means in Faiss) e codice C++ (k-means): penalizza e-means.

**"Il recall crolla da 0,83 a 0,05."** Quel numero vale se dopo l'aggiornamento i vettori restano nelle liste in cui erano, cosa che Faiss non offre e che un lettore esperto contesterebbe. Il numero difendibile è con le liste ricostruite: da 0,83 a 0,42 dopo un aggiornamento. Post e segnalazione usano quello.

## Come è cambiata la segnalazione

La revisione "da manutentore" ha mostrato che la prima stesura sarebbe stata liquidata come uso improprio. Ora:

- è una **richiesta di documentazione**, con una proposta facoltativa, non una segnalazione di difetto: il comportamento è coerente con il paper, che dichiara di dare alla partenza un peso minimo;
- riconosce che i due fatti sono già scritti nel codice, e chiede di scriverne la conseguenza;
- mostra la causa con il codice di Faiss;
- ammette che la correzione serve a poco in pratica, perché ricalcolare è meglio: per questo la nota conta più della funzione.

## Cosa non è stato fatto

1. **La prova sul codice più recente di Faiss.** Dopo il rilascio 1.16.0 il ramo principale ha cambiato la rianimazione dei cluster. Ho scaricato i sorgenti, ma il sistema ha bloccato l'esecuzione di codice appena scaricato e non ho aggirato il blocco. Inoltre quel codice richiede funzioni native che la versione installata non ha: serve compilare Faiss. Leggendo il sorgente, il peso iniziale è invariato e il risultato restituito è ancora la media dell'ultima epoca (con in più un passaggio di consegna per i centroidi rianimati), quindi mi aspetto lo stesso comportamento, ma non l'ho misurato. **È la prima cosa che i manutentori chiederanno: va fatta prima di inviare la segnalazione.**
2. **arXiv con il secondo modello.** L'embedding di testi lunghi con il modello grande richiede alcune ore; è stato messo in coda per ultimo. Lo stato è nella sezione finale.
3. **Scale più grandi di 200.000 vettori**, interrogazioni di utenti veri, confronto con i metodi della letteratura sulla deriva.

## Limiti che restano

- Un portatile, indici da 200.000 vettori, tre seed per insieme di dati.
- Gli intervalli di confidenza riguardano le interrogazioni, non la variabilità tra corpus.
- Le interrogazioni sono testi del corpus tenuti fuori, non domande.
- "Liste ricostruite" significa ricostruite una volta, al momento della misura, e non dopo ogni aggiornamento. Chi ricostruisce le liste ha in mano tutti i vettori e potrebbe riaddestrare su tutti: è il caso più favorevole all'uso ingenuo, non il più realistico.
- L'aggiornamento da 10.000 testi con 2.048 centroidi (circa 5 testi per centroide) è sotto l'intervallo su cui sono state tarate le leggi di scala di e-means (da 100.000 righe in su).
- Un solo punto di lavoro per la ricerca: indice IVF senza compressione, due quote di vettori letti.
- Dataset e modelli non sono fissati a una revisione.

## Cosa decidere

1. **Il post**: va bene il testo? Preferisci la versione lunga o la breve? Il repository va reso pubblico prima, perché il post lo cita.
2. **La segnalazione**: la invii tu, dopo la prova sul ramo principale. Posso preparare le istruzioni per compilare Faiss, ma serve il tuo permesso per eseguire quel codice.
3. **L'articolo lungo** previsto dal piano: i materiali ci sono tutti; non è stato scritto questa notte.

## Stato della coda al momento della scrittura

STATO_CODA
