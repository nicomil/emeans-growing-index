---
title: 'Piano del passo 6: consolidare e scrivere'
status: draft
created: 2026-11-22
---

# Piano del passo 6: consolidare e scrivere

## Dove siamo

Cinque passi sperimentali chiusi, ognuno con spec e revisione. La domanda del brief era quanto fidarsi dei centroidi vecchi in funzione della deriva. La risposta trovata è diversa da quella cercata.

Quattro risultati reggono, su dati sintetici e su embedding veri:

1. e-means ricalcola un indice in una frazione del tempo del k-means classico, anche su un portatile e su testo reale: 5 volte più veloce a parità di errore, recall a mezzo punto dal riferimento con 3 epoche.
2. Usare e-means in modo incrementale nel modo più ovvio (centroidi vecchi come partenza, solo dati nuovi) distrugge l'indice: recall da 0,83 a 0,05.
3. Senza rileggere i vettori già inseriti, nessuna variante di e-means fa meglio del mini-batch k-means classico. Si recupera circa il 40% del recall perso.
4. Su 200.000 articoli e quattro anni e mezzo, non aggiornare costa 6 punti di recall, 11 sulle interrogazioni recenti; 5 dei 6 sono deriva.

Due cose non hanno retto: una legge che scelga la massa iniziale dalla deriva, e il vantaggio della partenza a caldo nella ricerca.

Il brief non è stato aggiornato: descrive ancora l'ipotesi iniziale. Va riallineato prima di scrivere (attività 6.0).

## Obiettivo del passo

Trasformare i risultati in uno studio pubblicabile, dopo aver chiuso i tre punti che un lettore esperto contesterebbe per primi.

## Attività, in ordine

Ogni attività ha un criterio di uscita. Se un criterio fallisce, il piano dice cosa cambia.

### 6.0 Riallineare il brief — fatto, approvato il 23 novembre 2026 con filo ibrido

Riscrivere sintesi, soluzione e criteri di successo del brief sulla base dei risultati. Le ipotesi abbandonate restano nel registro delle decisioni.

- Fatto quando: il brief descrive lo studio che scriveremo, e tu lo riconosci come tuo.

### 6.1 Verificare l'avviso con il codice di Faiss — fatto, confermato (vedi `letteratura-recente.md`)

Il risultato 2 è il più utile al lettore ed è stato misurato con `emeans.py`, la nostra riscrittura. Va ripetuto chiamando direttamente `NumpyEmeans.train(nuovi, init_centroids=vecchi)` di Faiss sugli embedding veri.

- Fatto quando: il recall con il codice di Faiss è riportato accanto al nostro.
- Se Faiss non mostra il crollo: il risultato 2 diventa "un'implementazione fedele all'algoritmo del paper lo mostra, quella distribuita no", e va capito perché prima di scrivere una riga.

### 6.2 Controllare la letteratura recente — fatto, tema non coperto (vedi `letteratura-recente.md`)

Cercare lavori usciti dopo il 6 novembre 2026 su e-means in scenari incrementali, a caldo o con deriva, e le discussioni nel repository di Faiss. Rileggere come DeDrift, Ada-IVF e SPFresh misurano la deriva, per usare gli stessi termini.

- Fatto quando: c'è un elenco di lavori con una riga ciascuno su cosa coprono e cosa no.
- Se qualcuno ha già pubblicato gli stessi risultati: lo studio si presenta come replica indipendente su testo e su portatile, non come novità.

### 6.3 Secondo corpus — fatto (vedi `spec-6-consolidamento.md`)

Tutto il risultato su dati veri poggia su HuffPost: testi brevi, un solo dominio. Ripetere `exp_real.py` su abstract di arXiv (`gfissore/arxiv-abstracts-2021`, la data si ricava dall'identificativo): testi più lunghi, vicini ai pezzi di documento di un sistema RAG, e deriva tematica forte.

- Lavoro: rendere `embed_news.py` ed `exp_real.py` indipendenti dal corpus; estrarre circa 300.000 abstract in ordine di data; rieseguire.
- Fatto quando: la tabella del passo 5 esiste per entrambi i corpus.
- Se un risultato non si ripete: si riporta così, con il corpus su cui vale.

### 6.4 Rinforzi alla misura — fatto, con in più un secondo modello di embedding

Solo quelli che toccano i quattro risultati principali:

- intervallo di confidenza sulle interrogazioni (ricampionamento), per dire quali differenze di recall sono reali;
- recall a due livelli di costo, 0,1% e 1% dell'indice, come nell'Appendice L del paper;
- tempi ripetuti tre volte in ordine alternato, con il recall accanto.

- Fatto quando: ogni numero citato nel testo ha il suo intervallo.

Fuori dal piano, di proposito: massa per cluster, riassegnazione locale, legge di scala, confronto diretto con DeDrift o SPFresh, corpus italiano. Vanno citati come lavoro futuro.

### 6.5 Scrivere — fatte le bozze del post e della segnalazione; l'articolo lungo resta da scrivere

Struttura proposta:

0. Cappello di contesto, per chi non lavora con questi indici: cos'è un sistema RAG e dove sta l'indice vettoriale; i due modi di costruirlo, a grafo (HNSW) e a cluster (IVF); pregi e limiti di ciascuno e a che scala si usa l'uno o l'altro; dove si colloca questo studio (solo indici a cluster) e cosa cambia per chi usa HNSW.
1. Cosa promette e-means e cosa abbiamo voluto verificare.
2. Replica su testo reale e su un portatile: tempi, errore, recall.
3. Quanto costa non aggiornare un indice: la deriva misurata.
4. "Ho già dei centroidi buoni, posso riusarli?" Primo modo, il più ovvio: addestrare e-means sui soli documenti nuovi. Perché rompe l'indice (massa iniziale nulla, rianimazione dei cluster).
5. Secondo modo: dare un peso ai centroidi vecchi. Massa ridotta, regola dal segnale, e l'errore di misura che ci aveva fatto credere a un vantaggio.
6. Terzo modo: riusarli rileggendo tutto. Cosa cambia nell'errore e cosa no nella ricerca.
7. Cosa fare in pratica: ricalcolare, con quante epoche, ogni quanto.
8. Limiti e lavoro futuro.

Figure: tempo contro errore per i due algoritmi; recall nel tempo per strategia; l'animazione 2D come illustrazione del meccanismo; recall prima e dopo l'uso ingenuo.

Le sezioni 4-6 seguono il filo della partenza a caldo; la 5 è il punto che distingue lo studio da un riassunto del paper: racconta anche le conclusioni ritirate dopo revisione.

- Fatto quando: esiste una bozza completa e un README che permette di rifare ogni tabella con un comando.

### 6.6 Revisione finale — fatta sui due testi brevi, due passaggi

Revisione del testo con `bmad-review` (struttura e prosa) e una verifica che ogni numero del testo coincida con i file in `results/`.

- Fatto quando: nessun numero del testo è privo di fonte nel repository.

## Decisioni prese (22 novembre 2026)

1. **Lingua e sede:** per ora italiano.
2. **Repository:** pubblico, ma più avanti.
3. **Strade abbandonate:** una sezione nel corpo del testo, non un'appendice.
4. **Secondo corpus:** abstract di arXiv.

## Stima

Circa tre giorni di lavoro: mezza giornata per 6.0-6.2, una per 6.3-6.4, una e mezza per 6.5-6.6. Le attività 6.1 e 6.2 vanno fatte per prime perché possono cambiare cosa si scrive.

## Rischi

- 6.1 può mostrare che il crollo dipende da un dettaglio della nostra riscrittura. È il rischio più serio, per questo è la prima attività.
- 6.2 può togliere novità. Lo studio resta utile come replica.
- 6.3 può dare risultati diversi su testi lunghi. Va riportato, non nascosto.
