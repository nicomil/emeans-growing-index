---
title: 'Passo 4: aggiornare i centroidi leggendo solo i punti nuovi'
type: 'feature'
created: '2026-11-22'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/planning-artifacts/briefs/brief-rag_emean-2026-11-22/brief.md'
  - '{project-root}/_bmad-output/implementation-artifacts/spec-3-partenza-a-caldo.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Nel passo 3 tutte le strategie rileggevano l'intero insieme di dati, e lì la massa iniziale contava poco. Il caso d'uso reale è un altro: i dati vecchi non si vogliono rileggere e si aggiornano i centroidi con i soli punti nuovi, a un costo proporzionale a quanti sono. In quel caso non è stato misurato nulla.

**Approach:** Un esperimento in cui e-means parte dai centroidi vecchi e legge una volta i soli punti nuovi, con una griglia su massa iniziale, passo e soglia di rianimazione. L'errore si misura su tutti i dati, separato tra punti vecchi e nuovi, e si confronta con la media incrementale esatta e con le strategie che rileggono tutto. Vale per dati senza gruppi netti e per dati a gruppi netti.

</frozen-after-approval>

## Implementation Notes

**Codice**

- `exp_new_only.py`: l'esperimento. `uv run exp_new_only.py sovrapposti`, `netti` oppure `senza-deriva`, tre-quattro minuti ciascuno. Numeri grezzi in `results/exp_new_only_<tipo>.json`, tabelle complete in `results/exp_new_only_<tipo>.md`.
- `exp_warm.py`: `mixture` ha un parametro in più, la dispersione delle medie.
- `test_emeans.py`: un test nuovo sul legame tra e-means e il mini-batch k-means classico.
- `emeans.py` non è cambiato.

**Unità delle manopole**

- Massa m: massa iniziale = m × passo iniziale × numero di punti vecchi del cluster. A passo costante e molto piccolo, m = 1 rende e-means uguale al mini-batch k-means classico che parte dai conteggi veri: un punto vecchio pesa quanto uno nuovo (è un test). Con il passo a coseno di e-means i punti nuovi pesano da 1 a 0,1 volte un punto vecchio lungo la passata, in media 0,55: m = 1 trattiene il passato circa 1,8 volte più di quanto farebbe il peso pari.
- Passo s: passo iniziale = s × quello della legge di scala calcolata sul numero di punti nuovi.
- Soglia tau: 0,1 come nel paper, oppure 0 (rianimazione spenta).

**Disegno**

- 50.000 punti vecchi a 32 dimensioni, 256 centroidi, punti nuovi al 5%, 20% e 50% del totale. Tre tipi di dati: punti nuovi da una zona spostata con componenti sovrapposte; lo stesso con gruppi netti; punti nuovi dalla stessa distribuzione dei vecchi (senza deriva).
- Dei dati vecchi si usano solo i centroidi e il numero di punti per cluster, che un indice IVF conosce. Nell'esperimento i conteggi vengono da una riassegnazione dei dati vecchi; i centroidi escono dalla finalizzazione di e-means e non sono esattamente le medie dei punti contati.
- 5 insiemi di dati × 2 seed dell'algoritmo. Le 10 esecuzioni non sono indipendenti: i centroidi vecchi e le strategie senza casualità cambiano solo con l'insieme di dati.
- Riferimento: e-means da zero su tutti i dati, 10 epoche. Ogni eccesso è calcolato rispetto al riferimento della stessa esecuzione.
- Confronti a pari costo: Lloyd sui punti nuovi con le statistiche vecchie congelate; mini-batch k-means classico che parte dai conteggi veri, con gli stessi batch di e-means.
- e-means: una configurazione fissa per tutte le colonne e tutti i tipi di dati (m 0,3, s 1/4, senza rianimazione), scelta al centro della griglia dopo la prima esecuzione e non ritoccata; più la griglia m in {0,03; 0,1; 0,3; 1; 3}, s in {1/64; 1/16; 1/4; 1}, tau in {0,1; 0}. Sempre senza finalizzazione.

**Risultati con deriva, dati senza gruppi netti**

Errore in eccesso su tutti i dati, mediana [minimo; massimo]. La seconda colonna è la quota di dati letta.

| Strategia | Letture | 5% nuovi | 20% nuovi | 50% nuovi |
|---|---|---|---|---|
| centroidi vecchi, nessun ricalcolo | 0 | +2,35% [2,15; 2,50] | +12,65% [12,06; 12,84] | +31,48% [29,81; 32,71] |
| e-means, massa quasi nulla e finalizzazione | f | +66,40% [63,48; 68,35] | +54,78% [51,79; 58,12] | +31,54% [29,25; 33,20] |
| Lloyd con statistiche vecchie congelate | f | +1,69% [1,48; 1,90] | +7,09% [6,77; 7,54] | +12,62% [11,79; 13,55] |
| mini-batch k-means con conteggi veri | f | +1,29% [1,14; 1,45] | +6,37% [5,70; 6,56] | +9,01% [7,85; 10,16] |
| e-means, configurazione fissa | f | +1,27% [1,07; 1,37] | +4,89% [4,41; 5,37] | +3,25% [2,53; 4,53] |
| Lloyd congelato, 3 passate | 3f | +1,27% [1,08; 1,42] | +5,46% [5,26; 5,84] | +6,32% [5,08; 7,10] |
| e-means, configurazione fissa, 3 epoche | 3f | +1,65% [1,36; 1,91] | +4,41% [3,54; 5,09] | +7,27% [6,03; 8,21] |
| a caldo su tutti i dati, 1 epoca | 1 | +1,36% [1,22; 1,64] | +1,98% [1,71; 2,27] | +0,25% [−0,15; 0,74] |

Griglia con rianimazione spenta, eccesso mediano; tra parentesi in quante esecuzioni su 10 batte il mini-batch k-means con conteggi veri.

| m | 5%: s 1/64 | 1/4 | 1 | 20%: s 1/64 | 1/4 | 1 | 50%: s 1/64 | 1/4 | 1 |
|---|---|---|---|---|---|---|---|---|---|
| 0,03 | +2,67 (0) | +2,94 (0) | +4,39 (0) | +5,21 (10) | +5,52 (10) | +10,99 (0) | +4,00 (10) | +5,70 (10) | +15,66 (0) |
| 0,1 | +1,48 (0) | +1,59 (0) | +2,29 (0) | +4,54 (10) | +4,23 (10) | +6,80 (0) | +3,17 (10) | +2,77 (10) | +13,77 (0) |
| 0,3 | +1,27 (9) | +1,27 (9) | +1,39 (1) | +5,46 (10) | +4,89 (10) | +4,60 (10) | +5,91 (10) | +3,25 (10) | +11,56 (0) |
| 1 | +1,43 (0) | +1,35 (0) | +1,24 (10) | +7,03 (0) | +6,45 (0) | +4,37 (10) | +11,13 (0) | +7,05 (10) | +8,40 (8) |
| 3 | +2,02 (0) | +1,91 (0) | +1,45 (0) | +8,02 (0) | +7,63 (0) | +5,22 (10) | +15,85 (0) | +12,04 (0) | +5,37 (10) |

Con la rianimazione accesa le celle sono uguali al 5%; al 20% e al 50% peggiorano dove il passo è grande, fino a +30 punti. Nessuna migliora.

**Risultati senza deriva**

| Strategia | Letture | 5% nuovi | 20% nuovi | 50% nuovi |
|---|---|---|---|---|
| centroidi vecchi, nessun ricalcolo | 0 | +0,14% | +0,28% | +0,49% |
| e-means, massa quasi nulla e finalizzazione | f | +17,86% | +7,54% | +1,08% |
| mini-batch k-means con conteggi veri | f | +0,11% | +0,16% | +0,17% |
| e-means, configurazione fissa | f | +0,16% | +0,29% | +0,27% |
| e-means, migliore cella della griglia | f | +0,12% | +0,17% | +0,17% |

Nessuna cella della griglia batte il mini-batch k-means con conteggi veri, in nessuna esecuzione. Le celle migliori hanno m tra 1 e 3; con m sotto 0,3 l'errore sale. La configurazione fissa con il 5% e il 20% di punti nuovi non fa meglio che lasciare i centroidi vecchi.

**Cosa regge**

1. **L'uso ingenuo danneggia sempre.** Passare i centroidi vecchi a e-means e addestrarlo sui soli punti nuovi con la massa quasi nulla di serie alza l'errore in tutti i casi provati, anche senza deriva (+17,86% con il 5% di punti nuovi) e anche rispetto a non fare nulla. Con deriva l'errore sui punti vecchi sale del 63-75%.
2. **Senza deriva e-means non serve.** Il mini-batch k-means classico con i conteggi veri è il migliore e basta.
3. **Con deriva, dare meno peso al passato aiuta, e qui e-means con massa ridotta batte i confronti a pari costo.** Con il 20% e il 50% di punti nuovi la configurazione fissa fa +4,89% e +3,25% contro +6,37% e +9,01% del mini-batch classico, con intervalli disgiunti. Con il 5% sono alla pari. Il vantaggio non viene dall'algoritmo in sé: viene dal poter dimenticare, che lascia migrare i centroidi verso la zona nuova.
4. **La massa migliore dipende da quanta deriva c'è.** Senza deriva m tra 1 e 3; con deriva e 5% di punti nuovi circa 0,3; con 20% e 50% circa 0,1. È la risposta, in direzione, alla domanda del brief. Non è una formula: la griglia procede a salti di un fattore 3 e c'è un solo tipo di deriva.
5. **Massa e passo si compensano.** Un passo più grande fa dimenticare più in fretta e regge una massa più alta.
6. **La rianimazione di e-means è inadatta a questo scenario.** Sconta la massa di tutti i cluster a ogni passo, anche di quelli che non ricevono punti. Un cluster vecchio senza punti nuovi finisce sotto soglia e viene riciclato benché i suoi punti esistano ancora. Spenta non peggiora mai; accesa costa fino a 30 punti.
7. **Più passate sui soli punti nuovi non aiutano e-means**: con tre epoche dimentica di più (al 50%, errore sui punti vecchi +13%). Aiutano invece il Lloyd congelato, che con tre passate raggiunge la configurazione fissa al 5% ma non al 20% e al 50%.
8. **Rileggere tutto resta meglio quando i punti nuovi sono tanti**: una epoca a caldo su tutti i dati dà +1,98% e +0,25% contro +4,89% e +3,25%. Con il 5% di punti nuovi non c'è differenza, a un ventesimo delle letture.

**Su dati a gruppi netti**

Il riferimento è instabile (viene battuto fino al 20% da strategie che dovrebbe limitare) e i valori assoluti non si possono usare. I confronti appaiati vanno nella stessa direzione: l'uso ingenuo porta l'errore a +438%, +371%, +177%; la configurazione fissa batte il mini-batch classico in 9-10 esecuzioni su 10; la massa migliore scende con i punti nuovi fino a 0,03 con il 50%, che è il bordo della griglia. Con il 50% tre passate di Lloyd congelato fanno meglio della configurazione fissa a una passata.

**Il punto aperto**

La massa giusta dipende dalla deriva, che in pratica non si conosce in anticipo. I dati suggeriscono un segnale misurabile senza rileggere i vecchi: l'errore dei punti nuovi sui centroidi vecchi, confrontato con quello tipico dei punti vecchi. Senza deriva è +1-2%; con deriva +45-72%. Scegliere la massa da quel segnale è il passo successivo naturale.

**Limiti**

- Una sola combinazione di n, k e dimensione; un solo tipo di deriva (zona spostata, tutti i punti nuovi dalla zona nuova). Mancano i casi misti.
- La griglia non racchiude il minimo in più punti: s = 1 con il 5% di punti nuovi, m = 0,03 con il 50% sui gruppi netti.
- La configurazione fissa è stata scelta dopo aver visto la prima griglia, sugli stessi dati.
- Le celle della griglia riportano solo mediana e numero di vittorie; differenze di pochi centesimi di punto non sono distinguibili.
- Errore sui dati di addestramento; nessun recall, nessun embedding reale.
- I confronti sono metodi semplici. La letteratura sulla deriva (DeDrift, Ada-IVF, SPFresh) divide e riassegna i cluster.

## Review Triage Log

Un revisore senza contesto (Blind Hunter), 13 rilievi. Ha verificato con codice proprio.

| # | Rilievo | Verdetto | Evidenza ed esito |
|---|---|---|---|
| 1 | La frase sul limite (m = 1 dà la media incrementale esatta) è falsa con il passo a coseno | high | Vero: i punti nuovi pesano in media 0,55. Corretto il docstring; aggiunto un test che mostra entrambe le cose (uguaglianza a passo costante, scarto con il coseno). |
| 2 | Anche a passo costante il limite non è il confronto usato | medium | Vero: il limite è la media online con centroidi che si muovono. Aggiunto quel confronto e rinominato il precedente. |
| 3 | Manca il confronto più naturale: mini-batch k-means con conteggi veri | high | Vero, ed è più forte di quello che usavo. Aggiunto; la griglia ora si confronta con questo. La conclusione "e-means batte la media incrementale" è stata ristretta ai casi con il 20% e il 50% di punti nuovi. |
| 4 | Il confronto si fermava a una iterazione | medium | Vero. Aggiunti Lloyd congelato a 3 passate ed e-means a 3 epoche, con il costo dichiarato. |
| 5 | "Migliore della griglia" scelto sulle stesse esecuzioni | high | Vero. Sostituito con una configurazione fissa per tutte le colonne e i tipi di dati. Resta scelta dopo la prima griglia: dichiarato nei limiti. |
| 6 | La griglia non racchiude il minimo | medium, rinviato | Vero. Dichiarato nei limiti; estensione registrata in `deferred-work.md`. |
| 7 | Le 10 esecuzioni non sono indipendenti | low | Vero. Dichiarato nell'intestazione delle tabelle e nel disegno. |
| 8 | Riferimento troppo rumoroso sui gruppi netti | medium, rinviato | Vero e già noto. Su quei dati si usano solo i confronti appaiati; riferimento più solido registrato in `deferred-work.md`. |
| 9 | Le celle mostrano solo la mediana | low | Vero. Il conteggio delle vittorie dà il segno; dichiarato nei limiti che differenze minime non sono distinguibili. |
| 10 | L'etichetta del migliore attribuiva un ruolo a tau senza motivo | low | Superato: la riga è stata tolta. |
| 11 | La rianimazione non è un confronto equo e non è un oblio neutro | medium | Vero. Riformulata la conclusione 6 come "inadatta a questo scenario"; variante che sconta solo i cluster colpiti registrata in `deferred-work.md`. |
| 12 | Conteggi e centroidi vecchi non coerenti; i conteggi costano una passata | low | Vero. Dichiarata l'ipotesi che l'indice conosca i conteggi e l'incoerenza con i centroidi finalizzati. |
| 13 | Scenario unico e favorevole all'oblio; nessun controllo senza deriva | high | Vero. Aggiunto il tipo di dati senza deriva, che ha cambiato le conclusioni 2 e 3. I casi misti restano nei limiti. |

## Avvertenza aggiunta dopo il passo D

I risultati di questa spec misurano l'errore riassegnando ogni punto al centroide più vicino. Un indice che legge solo i punti nuovi non lo fa: i vettori già inseriti restano nelle loro liste. Con quella misura, al passo D, il vantaggio della massa ridotta sul mini-batch k-means classico sparisce (vedi `spec-d-aggiornamenti-in-sequenza.md`). Le conclusioni di questa spec sulla massa migliore valgono quindi solo se dopo l'aggiornamento si riassegnano tutti i vettori, operazione che costa quanto una epoca. Restano valide in ogni caso la conclusione sull'uso ingenuo e quella sulla rianimazione.
