---
title: 'Passo 3: massa iniziale e partenza a caldo su deriva sintetica'
type: 'feature'
created: '2026-11-22'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/planning-artifacts/briefs/brief-rag_emean-2026-11-22/brief.md'
  - '{project-root}/_bmad-output/implementation-artifacts/spec-1-emeans-numpy-2d.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `emeans.py` parte sempre da centroidi casuali con massa quasi nulla. Non si può ripartire da centroidi esistenti né decidere quanto pesano, quindi la domanda del progetto non è ancora misurabile.

**Approach:** Aggiungere a `emeans` i centroidi iniziali, la loro massa e la possibilità di saltare la finalizzazione. Poi un primo esperimento su dati sintetici in cui la quota di punti nuovi è nota, per vedere se la partenza a caldo conviene e in che direzione si muovono massa e passo. La griglia completa e la ricerca della regola restano al passo 4.

</frozen-after-approval>

## Implementation Notes

**Codice**

- `emeans.py`: tre parametri nuovi in `emeans`. `init` sono i centroidi da cui ripartire; `init_mass` è un numero o un vettore di k valori; `finalize=False` salta la riga 11 dell'Algoritmo 1. Senza questi parametri il comportamento è quello di prima.
- `test_emeans.py`: tre test nuovi: effetto della massa, argomenti sbagliati, equivalenza tra massa enorme con finalizzazione e una passata di Lloyd.
- `exp_warm.py`: l'esperimento. Si lancia con `uv run exp_warm.py` e dura circa un minuto.

**Unità della massa**

La massa di un cluster è la media mobile del numero di punti che riceve per batch. A regime vale circa `batch_size × quota`, dove la quota è la frazione di punti che spetta al cluster. Nell'esperimento "massa m" significa `m × batch_size × quota × (1 − f)`, con la quota misurata sui dati vecchi e f la frazione di dati nuovi: in un batch dei dati aggiornati i punti vecchi sono solo una parte. Massa 1 equivale a una corsa già avviata; massa 0 è una massa quasi nulla, come quella che Faiss assegna ai centroidi iniziali (2⁻¹⁶; qui 10⁻¹⁰, il valore del paper).

**Disegno dell'esperimento**

- Dati vecchi: 50.000 punti a 32 dimensioni da una miscela di 200 gaussiane sovrapposte. Dati nuovi: 40 gaussiane spostate di 1,5 in 8 dimensioni, in quantità tale da essere il 5%, il 20% o il 50% del totale.
- Centroidi vecchi: e-means da zero, 5 epoche, sui soli dati vecchi. 256 cluster.
- Tutte le strategie messe a confronto spendono una passata in più sui dati aggiornati; quelle a caldo ereditano le 5 epoche già spese sui dati vecchi. Il riferimento è e-means da zero con 3 epoche: è un termine di paragone, non il minimo raggiungibile.
- 10 seed; dati e centroidi vecchi cambiano con il seed. L'eccesso rispetto al riferimento è calcolato seed per seed, sugli stessi dati; si riportano mediana, minimo e massimo.

**Risultati**

Errore in eccesso rispetto al riferimento, con finalizzazione: mediana [minimo; massimo] su 10 seed.

| Strategia | 5% nuovi | 20% nuovi | 50% nuovi |
|---|---|---|---|
| centroidi vecchi, nessun ricalcolo | +1,85% [+1,68; +2,16] | +12,03% [+10,98; +12,67] | +30,92% [+28,39; +32,45] |
| una passata di Lloyd dai vecchi | +1,24% [+1,00; +1,47] | +6,70% [+5,82; +7,24] | +12,45% [+10,80; +13,16] |
| da zero, 1 epoca | +3,44% [+3,00; +3,65] | +3,45% [+3,22; +3,59] | +2,06% [+1,85; +2,32] |
| a caldo, massa 0 | +1,05% [+0,76; +1,34] | +1,85% [+1,42; +2,36] | +0,12% [−0,06; +0,45] |
| a caldo, massa 1 | +0,65% [+0,44; +0,82] | +2,35% [+1,57; +2,67] | +0,03% [−0,19; +0,25] |
| a caldo, massa 10 | +0,61% [+0,51; +0,96] | +3,13% [+2,88; +3,78] | +1,06% [+0,51; +1,56] |
| a caldo, massa 100 | +0,65% [+0,49; +1,03] | +4,04% [+3,63; +4,88] | +2,60% [+2,16; +3,90] |
| a caldo, massa 1, passo/4 | +0,71% [+0,51; +0,92] | +4,39% [+4,07; +4,90] | +3,41% [+2,77; +4,62] |
| a caldo, massa 10, passo/4 | +0,85% [+0,69; +1,12] | +6,05% [+5,36; +6,46] | +9,18% [+8,48; +10,09] |

Senza finalizzazione l'ordine è lo stesso. Le righe più utili: da zero, 1 epoca dà +2,16% [+1,86; +2,32], +2,07% [+1,95; +2,21], +1,21% [+1,11; +1,56]; a caldo con massa 0 dà +0,83%, +1,28%, −0,15%.

Le tre colonne non differiscono solo per la quota di dati nuovi: la legge di scala sceglie batch 1024 e passo 0,25 al 5%, 1024 e 0,23 al 20%, 2048 e 0,34 al 50%. L'andamento non regolare lungo le colonne non si può quindi attribuire alla sola deriva.

**Cosa regge**

1. A parità di costo in più, la partenza a caldo batte la partenza da zero. Gli intervalli non si toccano in nessuna colonna, già con la massa quasi nulla, che non è una variante scelta a posteriori.
2. Con il 20% e il 50% di dati nuovi batte nettamente anche la singola passata di Lloyd dai centroidi vecchi. Con il 5% la distingue solo la massa 1; con massa 0 gli intervalli si sovrappongono.
3. Massa 100 e passo ridotto a un quarto peggiorano con il 20% e il 50% di dati nuovi.
4. Con una sola epoca da zero la finalizzazione peggiora l'errore, con intervalli disgiunti in tutte le colonne. Con una sola epoca "l'ultima epoca" è l'intera corsa, quindi la media comprende i punti assegnati quando i centroidi erano ancora lontani.

**Cosa non regge ancora**

- Che la massa 1 sia meglio della massa 0 con pochi dati nuovi e peggio con tanti. Le mediane vanno in quella direzione (+0,65% contro +1,05% al 5%; +2,35% contro +1,85% al 20%), ma gli intervalli si sovrappongono. Serve un test sulle differenze seed per seed.
- Che ridurre il passo peggiori sempre: con il 5% di dati nuovi non c'è differenza misurabile.

**Capito grazie alla revisione**

Con la finalizzazione attiva la massa non misura "quanto resto vicino ai centroidi vecchi". Il risultato sono le medie dell'ultima epoca. Con massa enorme i centroidi non si muovono durante l'epoca e la finalizzazione produce esattamente una passata di Lloyd dai centroidi vecchi (verificato, ora è un test). Nella tabella con finalizzazione, quindi, aumentare la massa sposta il risultato dalla riga "massa 0" verso la riga "una passata di Lloyd", che è peggiore. La massa come manopola di fiducia nel passato ha senso pieno solo senza finalizzazione.

**Sorpresa**

La prima versione dei dati aveva le medie delle gaussiane troppo sparse: 240 gruppi netti per 256 centroidi. In quel regime il riferimento stesso variava del 4-8% da un seed all'altro, 10 epoche davano un errore peggiore di 3, e la partenza a caldo sembrava battere il riferimento del 18%. I dati attuali hanno medie più vicine del raggio del rumore e il riferimento varia dello 0,4%.

Questo ha un costo: i risultati valgono per dati senza gruppi netti. Il regime a gruppi netti, dove contano i cluster rimasti senza centroide, è stato escluso dopo aver visto i numeri, non studiato. Va ripreso con più seed.

La prova fatta prima di iniziare il progetto (partenza a caldo peggiore di quella da zero, 62,90 contro 62,76) era su gruppi netti e con un solo seed: non è una smentita valida di questi risultati, e questi non la smentiscono per quel regime.

**Limiti**

- Un solo tipo di dati sintetici, una sola combinazione di n, k e dimensione.
- Tutte le strategie rileggono l'intero insieme di dati. Manca il caso d'uso incrementale vero: partire a caldo leggendo solo i punti nuovi, con costo proporzionale a quanti sono.
- Si misura l'errore complessivo sui dati di addestramento. Non è separato tra punti vecchi e nuovi, non c'è errore su dati mai visti né recall di un indice.
- Lo stesso seed guida dati e algoritmo, quindi le due fonti di variabilità non sono separate.
- Il passo è stato solo ridotto, mai aumentato.

## Review Triage Log

Un revisore senza contesto (Blind Hunter), 19 rilievi, sui passi 2 e 3 insieme. Ha rieseguito l'esperimento.

| # | Rilievo | Verdetto | Evidenza ed esito |
|---|---|---|---|
| 1 | Rapporto di mediane invece di confronto appaiato | medium | Vero: ogni seed ha dati propri. Ora l'eccesso è calcolato seed per seed. |
| 2 | Nessuna misura di dispersione | medium | Vero, e alcune mie conclusioni non reggevano. La tabella riporta minimo e massimo; le conclusioni sono state divise tra ciò che regge e ciò che no. |
| 3 | Il riferimento a 3 epoche non è un minimo | medium, rinviato | Vero: il revisore misura −0,25% con 10 epoche. Chiarito nel testo che è un termine di paragone; riferimento a convergenza rinviato al passo 4. |
| 4 | "Costo uguale" non conta le epoche già spese | low | Vero. Corretto il docstring e l'etichetta della strategia a costo zero. |
| 5 | Manca la strategia a costo proporzionale ai dati nuovi | medium, rinviato | Vero ed è il caso d'uso reale. Registrato in `deferred-work.md`. |
| 6 | La quota di dati nuovi è confusa con batch e passo | medium, rinviato | Vero: la legge di scala cambia batch e passo tra colonne. Dichiarato accanto ai risultati; colonne a ricetta fissa rinviate al passo 4. |
| 7 | "Massa 1" non significa lo stesso tra colonne | medium | Vero: mancava il fattore 1 − f. Corretto; i numeri sono stati ricalcolati. |
| 8 | Dati scelti dopo aver visto i risultati, regime critico escluso | medium, rinviato | Vero. Dichiarato nella sezione Sorpresa; regime a gruppi netti registrato in `deferred-work.md`. |
| 9 | Colonna dei cluster vuoti sempre a zero | low | Vero. Tolta. |
| 10 | L'errore complessivo nasconde il compromesso tra punti vecchi e nuovi | medium, rinviato | Vero: il revisore mostra che i centroidi vecchi fanno 30,5 sui vecchi e 52,2 sui nuovi. Registrato in `deferred-work.md`. |
| 11 | Sei varianti a caldo contro una da zero, scelta a posteriori | low | Vero in generale; la conclusione 1 ora poggia sulla sola massa 0, fissata in partenza. |
| 12 | Lo stesso seed guida dati e algoritmo | low, rinviato | Vero. Registrato in `deferred-work.md`. |
| 13 | Con finalizzazione, massa enorme equivale a una passata di Lloyd | medium | Vero, verificato. Aggiunto il test e la sezione "Capito grazie alla revisione". |
| 14 | Il docstring non avverte che con la finalizzazione la massa non limita lo spostamento | medium | Vero. Aggiunto l'avviso. |
| 15 | L'etichetta "Faiss di serie" non è verificata | low | Vero: Faiss usa 2⁻¹⁶, non 10⁻¹⁰. Etichetta cambiata, costante `INIT_MASS` riusata. Il confronto diretto con `NumpyEmeans.begin` non è stato fatto. |
| 16 | Convalida incompleta dei parametri nuovi | low | Corretto il caso `init_mass=nan`, con test. Respinti gli altri: errori già espliciti o casi innocui. |
| 17 | Tolleranza dell'1% nel test contro Faiss troppo larga | medium | Vero: con la rianimazione spenta lo scarto è 0,8% e il test passava. Portata a 0,2%; tolto il `print`. |
| 18 | Test della partenza a caldo poco estesi | low | Aggiunti massa vettoriale, finalizzazione attiva e verifica che `init` non venga modificato, nel test del punto 13. Respinto il resto. |
| 19 | Lavoro doppio tra le due tabelle | low | Vero. Le due varianti ora si calcolano nella stessa esecuzione: da 95 a 54 secondi. |
