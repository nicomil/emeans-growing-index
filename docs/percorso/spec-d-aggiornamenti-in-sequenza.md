---
title: 'Passo D: aggiornamenti in sequenza'
type: 'feature'
created: '2026-11-22'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context:
  - '{project-root}/docs/percorso/spec-4-solo-punti-nuovi.md'
  - '{project-root}/docs/percorso/spec-4b-regola-della-massa.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Tutti gli esperimenti finora misurano un solo aggiornamento. Con pochi punti nuovi le differenze tra strategie sono di pochi decimi di punto. Il caso reale è un aggiornamento ripetuto, e non si sa se quelle differenze si accumulano o svaniscono: da questo dipende se vale la pena continuare a lavorare sulla massa.

**Approach:** Dieci aggiornamenti in fila, ciascuno con punti nuovi pari al 5% dei dati iniziali, in cui ogni strategia riparte dai propri centroidi del giro precedente. Tre derive: nessuna, zona nuova fissa, zona che si allontana. Si misura l'errore su tutti i dati dopo 1, 5 e 10 giri.

</frozen-after-approval>

## Implementation Notes

**Codice**

- `exp_sequence.py`: `uv run exp_sequence.py > results/exp_sequence.md`, circa cinque minuti. Richiede i parametri scritti da `exp_rule.py sovrapposti`. Tutti i giri e tutti gli insiemi di dati sono in `results/exp_sequence.json`.

**Disegno**

- 50.000 punti iniziali a 32 dimensioni, 256 centroidi, dati senza gruppi netti. Dieci giri da 2.500 punti nuovi: alla fine i punti nuovi sono un terzo del totale.
- Tre derive con le stesse 40 componenti nella zona nuova: nessuna; zona fissa spostata di 1,5; zona che si allontana di 0,15 a ogni giro.
- Strategie sui soli punti nuovi: e-means con le impostazioni di serie; mini-batch k-means che parte dalle dimensioni delle liste; e-means con massa 1, con massa dalla regola della quota (circa 0,4), con massa 0,2. Una strategia che rilegge tutto: una epoca a caldo a ogni giro.
- Riferimento: e-means da zero su tutti i dati, 10 epoche, rifatto a ogni giro. 5 insiemi di dati mai usati prima.
- **Due metriche.** "Liste": ogni punto resta nella lista in cui è stato inserito, come in un indice IVF che non rilegge i vettori già presenti; è la misura realistica per chi legge solo i punti nuovi. "Riassegnando": ogni punto va al centroide più vicino, il che richiede di rileggere tutti i vettori. I passi 4 e 4b avevano usato solo la seconda.
- **Controllo "colpo unico"**: lo stesso aggiornamento fatto una volta sola con tutti i 25.000 punti nuovi.

**Risultati dopo dieci giri**

Errore in eccesso, mediana [minimo; massimo] su 5 insiemi di dati.

Metrica delle liste:

| Strategia | Nessuna deriva | Zona fissa | Zona che si allontana |
|---|---|---|---|
| centroidi iniziali, mai aggiornati | +0,36% [0,35; 0,42] | +19,73% [18,52; 22,53] | +10,48% [9,95; 12,18] |
| e-means, impostazioni di serie | +130,09% [128,04; 133,27] | +166,32% [157,53; 168,17] | +169,87% [164,46; 176,95] |
| mini-batch dalle dimensioni delle liste | +0,18% [0,17; 0,24] | +9,78% [9,39; 11,70] | +6,33% [5,99; 7,50] |
| e-means, massa 1 | +0,20% [0,19; 0,27] | +10,30% [9,90; 12,33] | +6,76% [6,57; 8,00] |
| e-means, massa dalla quota | +0,30% [0,29; 0,36] | +9,29% [8,98; 11,12] | +6,47% [6,13; 7,70] |
| e-means, massa 0,2 | +0,86% [0,85; 0,93] | +10,43% [9,72; 11,55] | +9,55% [9,12; 10,81] |
| a caldo su tutti i dati, 1 epoca | +0,59% [0,51; 0,63] | +0,97% [0,84; 1,23] | +1,30% [1,17; 1,63] |

Metrica che riassegna tutto, per le strategie sui soli punti nuovi:

| Strategia | Nessuna deriva | Zona fissa | Zona che si allontana |
|---|---|---|---|
| mini-batch dalle dimensioni delle liste | +0,15% | +8,08% | +5,23% |
| e-means, massa 1 | +0,19% | +9,39% | +6,20% |
| e-means, massa dalla quota | +0,20% | +5,99% | +3,58% |
| e-means, massa 0,2 | +0,48% | +3,38% | +2,72% |

Dieci giri contro colpo unico, metrica delle liste: mini-batch +9,78% contro +8,75% con la zona fissa e +6,33% contro +6,02% con la zona che si allontana; massa 0,2 +10,43% contro +8,50% e +9,55% contro +7,15%. Senza deriva i due valori coincidono per mini-batch e massa 1.

Letture in dieci giri: 25.000 punti per le strategie sui soli nuovi, 637.500 per quella che rilegge tutto.

**Cosa regge**

1. **Con la metrica realistica il vantaggio della massa ridotta sparisce.** Nelle liste, con la zona fissa, tutte le strategie sui soli punti nuovi stanno tra +9,3% e +10,4% con intervalli sovrapposti; con la zona che si allontana e senza deriva la massa 0,2 è la peggiore. Il mini-batch k-means classico che parte dalle dimensioni delle liste è pari o migliore di e-means con qualunque massa provata.
2. **Il motivo.** Una massa bassa lascia spostare i centroidi verso i punti nuovi. Ma i punti vecchi restano nelle loro liste e non seguono il centroide: l'errore dei punti iniziali nelle loro liste sale di +9,6% e +12,7% con massa 0,2, contro +2,3% con il mini-batch. Il guadagno visto ai passi 4 e 4b esiste solo se dopo l'aggiornamento si riassegnano tutti i vettori.
3. **Riassegnare tutto ha un costo che rende inutile il trucco.** Riassegnare significa rileggere ogni vettore e confrontarlo con tutti i centroidi, cioè quanto costa una epoca. A quel prezzo una epoca a caldo su tutti i dati dà +0,97% e +1,30%, contro +3,38% e +2,72% della massa 0,2 con riassegnazione.
4. **Aggiornare con i soli punti nuovi recupera circa metà del degrado, qualunque metodo si usi.** Con la zona fissa si passa da +19,7% a circa +9,8%; con la zona che si allontana da +10,5% a +6,3%. Rileggere tutto porta a circa +1%.
5. **L'accumulo esiste ma è piccolo.** Dieci giri danno un errore di 0,3-2 punti più alto del colpo unico con gli stessi punti. La crescita dell'errore da un giro all'altro viene soprattutto dall'aumento dei punti spostati. La conclusione scritta prima della revisione ("le differenze si accumulano") era sbagliata.
6. **L'uso ingenuo è ancora peggio di quanto misurato prima.** Nelle liste l'errore va da +130% a +170%, anche senza deriva: i centroidi vengono riscritti e i punti vecchi restano in liste il cui centroide è altrove.

**Conseguenze per il progetto**

- La strada A (massa per cluster) perde la sua motivazione: il limite non è scegliere bene la massa, è che i punti già inseriti non si possono spostare senza rileggerli.
- Si capisce perché la letteratura sulla deriva (SPFresh, Ada-IVF) riassegna localmente i soli cluster che cambiano: è il modo di pagare la rilettura solo dove serve. È l'unica direzione rimasta in cui e-means potrebbe dare qualcosa nello scenario incrementale, e non è stata toccata.
- Restano validi i risultati che non dipendono dalla metrica: la partenza a caldo che rilegge tutto batte la partenza da zero a pari costo (passo 3), e l'uso ingenuo sui soli punti nuovi fa danni.

**Limiti**

- Solo dati senza gruppi netti; una sola combinazione di n, k e dimensione; un solo volume per giro.
- 5 insiemi di dati; seed dei dati e dell'algoritmo legati; nessuna differenza appaiata tra strategie.
- La metrica delle liste è un errore di quantizzazione, non il recall di una ricerca: un punto in una lista "sbagliata" può essere trovato comunque sondando più liste.
- La regola dalla quota è usata sotto l'intervallo su cui è stata tarata ed è di fatto una costante (0,40-0,44).
- La strategia che rilegge tutto usa la massa quasi nulla di serie; con una massa non nulla potrebbe fare meglio.
- Il riferimento vede i punti nuovi mentre si addestra, i centroidi mai aggiornati no: parte del loro eccesso senza deriva è questo.
- Dati sintetici.

## Review Triage Log

Un revisore senza contesto (Blind Hunter), 12 rilievi. Ha verificato su un insieme di dati con codice proprio.

| # | Rilievo | Verdetto | Evidenza ed esito |
|---|---|---|---|
| 1 | Manca il controllo che separa l'accumulo dall'aumento dei punti spostati | high | Vero. Aggiunto il colpo unico: l'accumulo vale 0,3-2 punti, il resto è volume. Ritirata la conclusione sull'accumulo. |
| 2 | L'errore era misurato riassegnando tutti i punti, cosa che un indice che legge solo i nuovi non fa | high | Vero, e ribalta le conclusioni sulla massa. Aggiunta la metrica delle liste come misura principale; aggiunta un'avvertenza alle spec dei passi 4 e 4b. |
| 3 | I conteggi portati avanti non sono quelli che le strategie assumono | medium | Vero. Ora i conteggi sono per definizione le dimensioni delle liste, cioè ciò che l'indice conosce; il confronto è stato rinominato di conseguenza. |
| 4 | "Zona che si allontana" generava dieci zone diverse, non monotone | high | Vero. Le 40 componenti sono estratte una volta e traslate; verificato lo spostamento per giro (da 0,12 a 1,49, regolare). |
| 5 | La colonna dei punti iniziali aveva un denominatore sbagliato | medium | Vero. Ora si confronta con l'errore degli stessi punti sui centroidi iniziali, nelle loro liste. |
| 6 | Il riferimento era usato fuori dal ciclo | low | Vero. Aggiunto un controllo sulla costante. |
| 7 | Solo tre giri riportati e salvati | medium | Vero. Ora il riferimento è rifatto a ogni giro e tutti i giri sono nel file grezzo. |
| 8 | Mancano le differenze appaiate; seed legati | low, rinviato | Vero. Dichiarato nei limiti. |
| 9 | La regola dalla quota è di fatto una costante; manca la regola dal segnale | low | Vero per la prima parte, dichiarato nei limiti. La regola dal segnale è stata scartata al passo 4b. |
| 10 | La strategia che rilegge tutto non è forte e il suo costo era nascosto | medium | Aggiunto il costo cumulato. La variante con massa non nulla resta nei limiti. |
| 11 | Senza deriva la crescita dei centroidi mai aggiornati non è degrado | low | Vero. Dichiarato in testa alla tabella e nei limiti. |
| 12 | Dettagli: funzione duplicata, percorso relativo, nessuna verifica del generatore | low | Tolta la funzione duplicata, documentata la dipendenza da `exp_rule.py`; il generatore è stato verificato a mano, senza test. |
