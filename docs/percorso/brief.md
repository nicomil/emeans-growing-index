---
title: "e-means e gli indici che cambiano: aggiornare o ricalcolare?"
status: approved
created: 2026-11-22
updated: 2026-11-23
---

# Brief di progetto: e-means e gli indici che cambiano

## Sintesi

e-means è una variante di k-means pubblicata da Meta FAIR il 6 novembre 2026 (arXiv 2611.09501) e distribuita in Faiss 1.16.0. Promette di costruire i gruppi di un indice vettoriale in un decimo delle passate sui dati. Il paper la studia su insiemi di dati fermi.

Questo studio la prova nella situazione in cui un indice vive davvero: i documenti continuano ad arrivare e gli argomenti cambiano. La domanda di partenza era quanto ci si possa fidare dei centroidi vecchi per evitare di ricalcolarli. Dopo cinque passi di esperimenti, su dati sintetici e su 200.000 articoli di giornale reali, la risposta è un'altra: non conviene cercare scorciatoie. Con e-means il ricalcolo completo costa così poco che è la scelta giusta, e il modo più ovvio di usarlo per aggiornare un indice lo rovina.

Lo studio vale per tre cose: una verifica indipendente di e-means su testo reale e su un portatile, un avviso pratico che nessuno ha ancora documentato, e il racconto onesto delle strade provate e abbandonate.

## Il problema

Un indice a cluster (IVF) divide i vettori in liste, ognuna rappresentata da un centroide. Quando arrivano documenti nuovi su argomenti nuovi, i centroidi smettono di descrivere bene i dati e la ricerca peggiora. Per rimediare si ricalcolano i centroidi, operazione che con il k-means classico è costosa e che per questo si rimanda.

e-means riduce quel costo. Restano però tre domande a cui il paper non risponde:

- Quanto si perde davvero a non ricalcolare, su un corpus testuale reale?
- Si può usare e-means per aggiornare un indice leggendo solo i documenti nuovi?
- Partire dai centroidi vecchi fa risparmiare qualcosa?

Sono domande pratiche, e diventano urgenti perché i motori vettoriali stanno adottando e-means: in Milvus la richiesta è stata aperta il 20 novembre 2026.

## Cosa abbiamo fatto

- Riscritto e-means in un file NumPy breve, verificato contro l'implementazione di Faiss, per poter cambiare ciò che Faiss non espone.
- Misurato le strategie di aggiornamento su dati sintetici con deriva controllata, e poi su titoli e sommari di HuffPost dal 2012 al 2019, inseriti in ordine di data in un indice che raddoppia da 100.000 a 200.000 articoli.
- Misurato l'errore nel modo in cui lo vede un indice vero, con ogni documento fermo nella lista in cui è stato inserito, e il recall di una ricerca a costo fisso.
- Sottoposto ogni passo a una revisione indipendente, che ha fatto cadere quattro conclusioni intermedie.

## Cosa abbiamo trovato

1. **e-means mantiene la promessa anche su un portatile e su testo.** Su 200.000 vettori, tre epoche impiegano 4,4 secondi; il k-means classico per arrivare allo stesso errore ne impiega 22,7. Il recall dell'indice ricalcolato con tre epoche è 0,838, contro 0,843 con dieci.
2. **Non aggiornare ha un costo misurabile.** In quattro anni e mezzo il recall scende da 0,843 a 0,781; sulle interrogazioni recenti perde quasi 11 punti. Cinque dei sei punti persi sono deriva degli argomenti, uno viene dalla semplice crescita dell'indice.
3. **L'uso incrementale più ovvio distrugge l'indice.** Passare a e-means i centroidi vecchi e addestrarlo sui soli documenti nuovi porta il recall da 0,83 a 0,15 al primo aggiornamento e a 0,05 dopo dieci. Succede anche con il codice di Faiss, senza toccare nulla. Le cause sono due: i centroidi di partenza hanno un peso quasi nullo, e il meccanismo che recupera i cluster vuoti ricicla quelli che non ricevono documenti nuovi, benché contengano ancora i vecchi.
4. **Le scorciatoie non reggono.** Corretto il difetto, e-means sui soli documenti nuovi non fa meglio del mini-batch k-means classico: entrambi recuperano circa il 40% del recall perso. Una regola che scelga quanto fidarsi dei centroidi vecchi in base alla deriva non è stata trovata. Partire dai centroidi vecchi rileggendo tutto abbassa un po' l'errore ma non cambia il recall.

La conseguenza pratica è una sola: ricalcolare l'indice da zero con e-means, con almeno tre epoche, ogni volta che serve.

## Come si racconta

Filo ibrido, approvato il 23 novembre 2026. Titolo e apertura sono pratici: aggiornare o ricalcolare? Le sezioni centrali seguono invece la domanda da cui il progetto è partito, "ho già dei centroidi buoni, posso riusarli?", attraverso i tre modi provati:

1. passarli a e-means e addestrare sui soli documenti nuovi: l'indice si rompe;
2. lo stesso, dando loro un peso: funziona, ma non meglio del mini-batch classico;
3. passarli a e-means rileggendo tutto: errore un po' più basso, recall identico alla partenza da zero.

La risposta pratica chiude il percorso: ricalcolare.

## Cosa lo distingue

- La letteratura sulla deriva degli indici (DeDrift, Ada-IVF, SPFresh) precede e-means e usa immagini, video o raccomandazioni. I lavori usciti dopo il paper, per quanto trovato al 22 novembre 2026, non trattano aggiornamenti né deriva.
- Tutto gira su un portatile e si rifà con pochi comandi.
- Racconta anche gli errori: tra questi, una misura dell'errore che per due passi ci ha fatto credere a un vantaggio inesistente.

Non c'è un contributo teorico. Il valore è nella verifica, nell'avviso e nel tempismo.

## A chi serve

- **A chi gestisce un indice vettoriale a cluster** e deve decidere se e come adottare e-means.
- **A chi sviluppa motori vettoriali**, perché l'avviso riguarda un uso che verrà spontaneo ai loro utenti.
- **A chi studia o insegna questi sistemi**: il codice breve e l'animazione mostrano come funziona l'algoritmo.

Chi usa indici a grafo (HNSW), cioè la maggior parte dei progetti RAG piccoli e medi, non è toccato direttamente. Per questo l'articolo si apre con un cappello di contesto: cos'è un sistema RAG, come funzionano i due tipi di indice, quando si passa dall'uno all'altro, e dove si colloca lo studio.

## Criteri di successo

1. I quattro risultati si ripetono su un secondo corpus, oppure è dichiarato dove non si ripetono.
2. Ogni numero del testo ha un intervallo di incertezza e una fonte nel repository.
3. Un lettore può rifare ogni tabella con un comando.
4. Esiste un articolo in italiano che un tecnico legge fino in fondo e da cui esce sapendo cosa fare.

## Perimetro

**Dentro:** secondo corpus (abstract di arXiv); intervalli sul recall; recall a due livelli di costo; tempi ripetuti; scrittura dell'articolo; revisione finale.

**Fuori:** massa diversa per ogni cluster; riassegnazione dei soli cluster che cambiano; legge di scala per il caso incrementale; confronto diretto con DeDrift, Ada-IVF e SPFresh; corpus italiano; GPU. Vanno citati come lavoro futuro.

## Rischi e incognite

- Tutti i risultati su dati veri vengono per ora da un solo corpus di testi brevi. Su testi più lunghi potrebbero cambiare.
- A scale molto più grandi di 200.000 vettori il ricalcolo completo costa di più e la conclusione pratica può non valere.
- La ricerca della letteratura recente è stata rapida e sedici giorni dopo il paper sono pochi: va ripetuta prima di pubblicare.
- Le interrogazioni usate sono articoli tenuti fuori dall'indice, non domande di utenti.

## Dove può arrivare

Se il secondo corpus conferma i risultati, il passo naturale è una versione in inglese e una segnalazione nel repository di Faiss sull'uso incrementale. La direzione di ricerca rimasta aperta è la riassegnazione locale: aggiornare con i documenti nuovi e rileggere solo le liste i cui centroidi si sono spostati.
