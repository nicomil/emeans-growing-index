---
title: 'Passo 4b: scegliere la massa iniziale da un segnale di deriva'
type: 'feature'
created: '2026-11-22'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context:
  - '{project-root}/docs/percorso/spec-4-solo-punti-nuovi.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Dal passo 4: aggiornando i centroidi con i soli punti nuovi, la massa iniziale migliore dipende da quanta deriva c'è, da 1-3 senza deriva a circa 0,1 con molta. In pratica la deriva non si conosce, e una massa fissa scelta male peggiora i casi senza deriva.

**Approach:** Misurare un segnale di deriva che non richiede di rileggere i dati vecchi, tarare una regola che ne ricava la massa, e valutarla su insiemi di dati diversi da quelli di taratura, compresi dati di tipo diverso. Il risultato può essere negativo: va riportato comunque.

</frozen-after-approval>

## Implementation Notes

**Codice**

- `exp_rule.py`: `uv run exp_rule.py sovrapposti > results/exp_rule_sovrapposti.md` tara le regole e le valuta (circa un minuto e mezzo); con `netti` valuta le stesse regole, senza ritararle, su dati a gruppi netti. Parametri in `results/exp_rule_fit.json`; griglie complete e valutazioni nei `.json` accanto.
- `test_emeans.py`: un test sulla procedura di taratura.

**Disegno**

- Segnale: errore medio dei punti nuovi sui centroidi vecchi, diviso per l'errore medio dei punti vecchi sugli stessi centroidi, meno 1. Il denominatore è un numero che l'indice può conservare. Leggere il segnale costa una passata in più sui punti nuovi, non contata nei confronti.
- 15 casi: quota di punti nuovi 5%, 20%, 50% × cinque derive (nessuna; un quarto dei punti nuovi dalla zona spostata; metà; tutti, zona spostata di poco; tutti, zona spostata come al passo 4).
- Una sola manopola: la massa m, dieci valori da 0,01 a 10. Passo a un quarto di quello della legge di scala e rianimazione spenta.
- Quattro regole: massa costante; dal segnale; dalla quota di punti nuovi; da entrambi. Tarate sugli insiemi di dati 0, 1, 2; valutate sugli insiemi 5, 6, 7, mai usati prima (gli insiemi 0-4 erano serviti al passo 4).
- Metrica: errore su tutti i dati rispetto al mini-batch k-means con conteggi veri. Negativo significa meglio.
- Oracolo: la migliore massa della griglia, scelta guardando il risultato.

**Regole tarate**

- costante: m = 0,20
- dal segnale: log m = −2,07 − 0,45 · log(segnale): m da 0,8 senza deriva a 0,15 con la deriva più forte
- dalla quota: log m = −1,84 − 0,30 · log(f): m = 0,39 con il 5% di punti nuovi, 0,26 con il 20%, 0,20 con il 50%
- dal segnale e dalla quota: log m = −2,42 − 0,50 · log(segnale) − 0,40 · log(f)

**Risultati**

Riepilogo sui 15 casi: media, caso peggiore, e in quanti casi la regola fa peggio del mini-batch di oltre 0,05 punti.

| Regola | Dati sovrapposti (stesso tipo della taratura) | Dati a gruppi netti (mai usati per tarare) |
|---|---|---|
| oracolo | −1,07%; +0,01%; 0 casi | −5,94%; +0,02%; 0 casi |
| massa costante 0,20 | −0,86%; +0,29%; 7 casi | −2,70%; +1,03%; 7 casi |
| dal segnale | −0,92%; +0,11%; 2 casi | −2,60%; +9,04%; 5 casi |
| dalla quota | −0,87%; +0,18%; 2 casi | −2,88%; +0,23%; 3 casi |
| dal segnale e dalla quota | −0,92%; +0,02%; 0 casi | −3,84%; +2,82%; 4 casi |

Sui gruppi netti il segnale vale da 1,2 a 5,0 nei casi con deriva, contro 0,2-0,7 sui dati di taratura. La regola dal segnale estrapola fuori dall'intervallo su cui è stata tarata e sceglie masse tra 0,06 e 0,12; con il 5% di punti nuovi la massa migliore è 0,5 e l'errore peggiora fino a +9,04%.

**Cosa regge**

1. **Il segnale di deriva, così definito, non serve a scegliere la massa.** Sui dati dello stesso tipo aggiunge 0,06 punti alla massa costante, meno della variabilità tra insiemi di dati. Su dati di tipo diverso fa danni. Il revisore ha verificato che il suo coefficiente non è determinato dalla taratura: qualunque valore tra −1,30 e +0,05 dà lo stesso errore entro 0,05 punti, e ritarando sui gruppi netti il coefficiente migliore è zero.
2. **Perché non serve.** Il segnale è una media. Due casi con lo stesso segnale (metà dei punti nuovi spostati di molto; tutti spostati di poco: 0,36 entrambi) vogliono masse opposte, 0,02 e 0,5. E a parità di scenario il segnale cambia di sette volte passando da dati sovrapposti a gruppi netti: non è una misura della deriva indipendente dai dati.
3. **La quota di punti nuovi, da sola, è una regola migliore.** Non richiede alcuna misura, non costa letture in più, e si trasferisce: sui gruppi netti ha il caso peggiore più basso (+0,23%) e una media migliore della massa costante. Il guadagno sulla massa costante è però piccolo, 0,01 punti sui dati sovrapposti e 0,18 sui gruppi netti.
4. **La massa costante 0,2 resta una scelta ragionevole**: tre quarti del guadagno dell'oracolo sui dati sovrapposti, metà sui gruppi netti. Perde qualcosa senza deriva (fino a +0,34%) e sui gruppi netti con pochi punti nuovi (fino a +1,03%).
5. **Resta margine non spiegato**, soprattutto sui gruppi netti: l'oracolo fa −5,94%, la migliore regola −3,84%. Si concentra nei casi con il 50% di punti nuovi, dove la massa migliore è 0,01-0,02, sul bordo della griglia.

**Risposta alla domanda del progetto, a questo punto**

"Quanto fidarsi dei centroidi vecchi in funzione della deriva": meno di quanto direbbero i conteggi (massa attorno a 0,2-0,4, non 1), un po' meno quando i punti nuovi sono tanti, e pienamente solo se si sa che non c'è deriva. Una regola che legga la deriva dai dati nuovi non è stata trovata.

**Limiti**

- Tre insiemi di dati per la taratura e tre per la valutazione; un solo seed dell'algoritmo per insieme.
- Taratura e valutazione condividono gli stessi 15 scenari: cambiano i dati, non le condizioni. Nessuna quota e nessun livello di deriva è tenuto fuori.
- I dati a gruppi netti cambiano due cose insieme, dispersione dei gruppi e ampiezza dello spostamento.
- La taratura non distingue masse intermedie tra due valori della griglia, che procede a salti di un fattore 2-2,5; in quattro casi il minimo è sotto il bordo inferiore.
- Passo fissato: una regola che muove anche il passo non è stata provata.
- La media sui 15 casi è dominata dai casi con il 50% di punti nuovi.
- Errore sui dati di addestramento; nessun recall, nessun embedding reale.

## Review Triage Log

Un revisore senza contesto (Blind Hunter), 17 rilievi. Ha ricalcolato le griglie e ritarato le regole per conto proprio.

| # | Rilievo | Verdetto | Evidenza ed esito |
|---|---|---|---|
| 1 | Manca la regola dalla sola quota | high | Vero. Aggiunta: è la più robusta. Ha cambiato la conclusione 3. |
| 2 | Il coefficiente del segnale non è determinato | high | Vero, verificato dal revisore. Riportato nella conclusione 1. Nessun intervallo calcolato nello script. |
| 3 | Il segnale è una media e non separa scenari che vogliono masse opposte | high | Vero: 0,36 in entrambi i casi, masse migliori 0,02 e 0,5. Riportato nella conclusione 2. Un segnale per cluster o per quantili non è stato provato: registrato in `deferred-work.md`. |
| 4 | Taratura e valutazione separano solo i dati, non le condizioni | medium, rinviato | Vero. Dichiarato nei limiti; scenari tenuti fuori registrati in `deferred-work.md`. |
| 5 | La valutazione sui gruppi netti misura un'estrapolazione | medium | Vero, ed è il motivo del fallimento. Scritto esplicitamente nei risultati. |
| 6 | I gruppi netti cambiano due cose insieme | low, rinviato | Vero. Dichiarato nei limiti. |
| 7 | Il segnale non è calibrato tra problemi diversi | high | Vero. Riportato nella conclusione 2. |
| 8 | Il minimo 0,01 sul segnale non era documentato | low | Vero. Documentato nel docstring, insieme al limite sulla massa. |
| 9 | Il costo di leggere il segnale non è contato | medium | Vero. Dichiarato nel docstring e nel disegno; rafforza la preferenza per la regola dalla quota, che non lo paga. |
| 10 | L'oracolo è limitato dalla griglia | medium | Vero: in quattro casi la curva scende ancora a 0,01. Dichiarato nei limiti. |
| 11 | Le statistiche di riepilogo non misurano ciò che dicono | medium | Corretta la colonna dei casi peggiori con una soglia di 0,05 punti. Dichiarato che la media è dominata dai casi al 50%. Minimo e massimo per cella non aggiunti. |
| 12 | Gli insiemi 3 e 4 erano già stati usati al passo 4 | high | Vero. La valutazione ora usa gli insiemi 5, 6, 7. I numeri sono cambiati di poco. |
| 13 | Un solo seed dell'algoritmo per insieme di dati | low | Vero. Dichiarato nei limiti. |
| 14 | Mancano il riferimento da zero e la configurazione fissa del passo 4 | low, respinto | La massa costante tarata (0,20) svolge lo stesso ruolo della configurazione fissa (0,3); il riferimento da zero è instabile sui gruppi netti. |
| 15 | I file grezzi non permettevano di ricontrollare taratura e oracolo | medium | Vero. Ora salvano le griglie complete di tutti gli insiemi di dati. |
| 16 | Il file dei parametri non ha provenienza | low, respinto | Vero ma di poco peso in uno studio con due comandi da lanciare in ordine. |
| 17 | Nessun controllo su taratura e previsione | medium | Vero. Aggiunto un test: la taratura ritrova una regola nota. Il test ha mostrato che la taratura non distingue masse tra due punti della griglia. |

## Avvertenza aggiunta dopo il passo D

I risultati di questa spec misurano l'errore riassegnando ogni punto al centroide più vicino. Un indice che legge solo i punti nuovi non lo fa: i vettori già inseriti restano nelle loro liste. Con quella misura, al passo D, il vantaggio della massa ridotta sul mini-batch k-means classico sparisce (vedi `spec-d-aggiornamenti-in-sequenza.md`). Le conclusioni di questa spec sulla massa migliore valgono quindi solo se dopo l'aggiornamento si riassegnano tutti i vettori, operazione che costa quanto una epoca. Restano valide in ogni caso la conclusione sull'uso ingenuo e quella sulla rianimazione.
