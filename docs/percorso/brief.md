---
title: "e-means a caldo: quanto fidarsi dei centroidi vecchi"
status: draft
created: 2026-11-22
updated: 2026-11-22
---

# Brief di progetto: e-means a caldo

## Sintesi

e-means è una variante di k-means pubblicata da Meta FAIR il 6 novembre 2026 (arXiv 2611.09501) e distribuita in Faiss 1.16.0. Raggiunge la qualità di k-means classico a 25 epoche in 1-3 epoche, usando piccoli batch e una media mobile esponenziale per aggiornare i centroidi. Il paper la studia in un solo scenario: si parte da centroidi casuali e si raggruppa un insieme di dati fermo.

Questo progetto studia lo scenario che il paper non copre: ripartire da centroidi già buoni quando i dati sono cambiati in parte. È la situazione di chi ha un indice vettoriale in produzione e riceve documenti nuovi. La domanda è una sola: **quanto bisogna fidarsi dei centroidi vecchi, in funzione di quanto è cambiato il corpus?**

Il progetto ha due scopi dichiarati, in quest'ordine: capire a fondo come funziona l'algoritmo, e produrre un risultato che non esiste ancora e che si possa pubblicare come studio.

## Il problema

Negli indici vettoriali a cluster (IVF) i vettori sono divisi in gruppi, ognuno rappresentato da un centroide. Quando il corpus cambia, i centroidi invecchiano e la ricerca peggiora. Per rimediare si ricalcolano i centroidi.

Con e-means si può passare i centroidi vecchi come punto di partenza (`init_centroids`), ma l'implementazione assegna loro una massa iniziale di 2⁻¹⁶, cioè quasi zero. In pratica il primo batch li sovrascrive: del passato resta solo l'assegnazione iniziale dei punti. Inoltre il passo iniziale della media mobile è scelto da leggi di scala tarate su circa 75.000 esecuzioni, tutte partite da zero.

Una prova preliminare su dati sintetici (200.000 vettori più 60.000 nuovi, 1.024 cluster, un seed) conferma il sospetto: con le impostazioni di serie, una epoca a caldo dà un errore leggermente peggiore di una epoca da zero (62,90 contro 62,76) e più cluster vuoti (52 contro 39).

## La soluzione

Due parametri controllano quanto pesa il passato:

| Parametro | Significato | Valore di serie |
|---|---|---|
| Massa iniziale | quanto contano i centroidi vecchi rispetto ai dati nuovi | 2⁻¹⁶ (nulla) |
| Passo iniziale | quanto in fretta l'algoritmo dimentica | dalla legge di scala per partenza da zero |

L'ipotesi è che i valori giusti dipendano dalla frazione di dati nuovi: con il 5% di dati nuovi conviene molta massa e un passo piccolo, con il 50% conviene comportarsi quasi come una partenza da zero.

Il progetto misura questa dipendenza con una griglia di esperimenti (massa × passo × frazione di dati nuovi) e cerca una regola semplice, nello stesso spirito delle leggi di scala del paper originale ma per il caso incrementale.

## Cosa lo distingue

- Il paper e-means usa solo l'inizializzazione casuale e non tratta né la partenza a caldo né i dati che cambiano.
- La deriva dei dati negli indici IVF è già studiata (DeDrift, ICCV 2023; Ada-IVF, 2024; SPFresh, SOSP 2023), ma con k-means classico e su immagini, video o raccomandazioni. Nessuno di questi lavori usa e-means, che è uscito dopo.
- L'effetto di e-means sul recall di un indice IVF statico è già misurato nell'Appendice L del paper: non va rifatto.

Il vantaggio non è una barriera tecnica: è il tempismo (il paper ha due settimane) e il fatto che l'esperimento gira su un portatile.

## A chi serve

- **All'autore**, per capire l'algoritmo abbastanza da modificarlo.
- **A chi sviluppa motori vettoriali a cluster o gestisce Faiss a grande scala**, che deve decidere come ricalcolare i centroidi quando arrivano dati nuovi.
- **A chi fa ricerca sulla ricerca approssimata**, come riferimento sul comportamento di e-means fuori dal caso studiato dagli autori.

Non serve a chi usa indici a grafo (HNSW), cioè alla maggior parte dei progetti RAG piccoli e medi.

## Criteri di successo

1. L'implementazione scritta a mano riproduce l'errore di quella di Faiss sugli stessi dati, entro la variabilità tra seed.
2. Esiste una risposta netta, in un senso o nell'altro: o una regola che lega massa e passo alla frazione di dati nuovi e batte la partenza da zero a parità di costo, o la prova che la partenza a caldo non conviene mai.
3. L'autore sa spiegare a voce, senza appunti, perché ogni parametro produce l'effetto osservato.

## Perimetro

**Dentro**, in cinque passi:

1. e-means scritto a mano in NumPy, su punti in due dimensioni, con visualizzazione.
2. Verifica contro l'implementazione di Faiss.
3. Aggiunta della massa iniziale; prove su dati sintetici con deriva controllata.
4. Griglia massa × passo × frazione di dati nuovi; ricerca della regola.
5. Controllo su embedding reali di testo.

**Fuori**: GPU, confronto di velocità con altre librerie, recall su indici statici, corpus italiano, deduplicazione semantica, una libreria da distribuire. Alcuni di questi punti possono rientrare dopo il passo 5.

## Rischi e incognite

- La regola potrebbe non esistere. Sarebbe comunque un risultato, ma meno interessante.
- Il guadagno potrebbe essere piccolo, perché e-means da zero costa già poco.
- Le prove preliminari usano un solo seed e dati sintetici.
- Non è stato verificato se dopo il 6 novembre 2026 qualcuno abbia pubblicato sullo stesso tema.
- Le leggi di scala sono dichiarate non ottimali per dati a bassa dimensione o molto piccoli: i risultati in 2D servono a capire, non a concludere.

## Dove può arrivare

Se la regola esiste, il passo naturale è verificarla su un corpus testuale con date reali e misurare l'effetto sul recall di un indice IVF nel tempo, confrontandola con il ricalcolo completo e con gli aggiornamenti incrementali di DeDrift. A quel punto lo studio risponde a una domanda pratica: con e-means, conviene ancora la manutenzione incrementale?
