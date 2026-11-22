---
title: 'Passo 1: e-means scritto a mano in NumPy, con animazione 2D'
type: 'feature'
created: '2026-11-22'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/planning-artifacts/briefs/brief-rag_emean-2026-11-22/brief.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** L'implementazione di e-means in Faiss 1.16.0 fissa la massa iniziale dei centroidi a 2⁻¹⁶ e distribuisce l'algoritmo su molti file pensati per GPU e calcolo distribuito. Così non si può né studiare la partenza a caldo né capire l'algoritmo leggendolo.

**Approach:** Riscrivere l'Algoritmo 1 del paper (arXiv 2611.09501) in un solo file NumPy breve e leggibile, valido per qualunque dimensione, e produrre un'animazione su punti 2D in cui si vedono i centroidi muoversi. La massa iniziale e la partenza a caldo restano fuori: sono il passo 3.

</frozen-after-approval>

## Implementation Notes

**Scelte fatte**

- Stato tenuto come posizione `c` e massa `N` invece che come somma `S` e massa `N`. È la stessa forma usata da Faiss ed è algebricamente equivalente all'Equazione 2 del paper. Evita la divisione 0/0 che la forma `S/N` produce quando il passo vale 1 e un cluster non riceve punti.
- Leggi di scala (batch e passo) copiate con i coefficienti distribuiti in `faiss/contrib/e_means/base.py`, che differiscono da quelli della Tabella 2 del paper. Servono al passo 2, per confrontarsi con Faiss a parità di ricetta.
- Rianimazione dei cluster morti attiva con soglia 0,1 come nel paper. Faiss la spegne quando la dimensione è ≤ 2, perché su dati 2D peggiora l'errore su dati mai visti; qui resta accesa perché lo scopo in 2D è vedere il meccanismo.
- Donatori estratti con `rng.choice` pesato sulla massa, senza reinserimento. Faiss usa il trucco di Gumbel: stessa distribuzione, codice meno leggibile.
- Animazione salvata come GIF, un fotogramma ogni pochi aggiornamenti.

**File**

- `emeans.py` — algoritmo e leggi di scala.
- `test_emeans.py` — controlli.
- `demo_2d.py` — genera `emeans_2d.gif`.
- `pyproject.toml` — dipendenze.

**Verifiche eseguite**

- `uv run pytest -q`: 13 test superati (5 prima della revisione, 8 aggiunti dopo).
- `uv run demo_2d.py`: GIF di 100 fotogrammi, errore da 0,809 al primo passo a 0,442 dopo la finalizzazione.
- Anteprima del passo 2, contro `NumpyEmeans` di Faiss 1.16.0 con rianimazione a 0,1: batch e passo iniziale identici in tutti i casi provati (128 e 0,0935 in 2D; 2048 e 0,4182 a 32 dimensioni; 4096 e 0,4150 a 64). Errore mediano su dati gaussiani a 32 dimensioni, 10 seed: 23,7905 contro 23,7771 di Faiss, con intervalli sovrapposti.

**Sorpresa**

Su dati a gruppi ben separati l'errore cambia molto da un seed all'altro, per entrambe le implementazioni: a 32 dimensioni, su 20 seed, da 11,15 a 29,07 la nostra e da 11,16 a 33,81 quella di Faiss. Dipende da quanti gruppi restano senza centroide. Con 5 seed sembrava una differenza del 4,5% tra le due implementazioni; con 20 seed e su dati gaussiani non c'è. Per il passo 2 e per la griglia del passo 4 servono molti seed, oppure dati senza gruppi netti.

**Osservazione utile per il passo 3**

La finalizzazione (riga 11 dell'Algoritmo 1) sostituisce ogni centroide con la media semplice dei punti che gli sono stati assegnati durante l'ultima epoca. La massa iniziale quindi non entra direttamente nel risultato finale: può influenzarlo solo attraverso il percorso, cioè attraverso quali punti finiscono assegnati a quale centroide. Negli esperimenti a caldo andrà misurato l'effetto con e senza finalizzazione.

## Review Triage Log

Un revisore senza contesto (Blind Hunter), 12 rilievi.

| # | Rilievo | Verdetto | Evidenza ed esito |
|---|---|---|---|
| 1 | La divisione moltiplicativa non separa un genitore sull'origine | low | Vero: `[0,0] * (1 ± eps)` dà due copie identiche. Faiss lo gestisce con `_separate_splits`. Corretto con `nextafter` sulla prima coordinata; test aggiunto. |
| 2 | `epochs`, `batch_size`, `alpha0` non validati, errori criptici | medium | Vero: `epochs=0` dava `math domain error`, `alpha0=2` rendeva negativa la massa. Aggiunti i controlli; test aggiunto. |
| 3 | `batch_size or ...` e `alpha0 or ...` trattano lo zero come assente | low | Vero. Sostituiti con `is None`; lo zero ora è rifiutato dal controllo del punto 2. |
| 4 | Forma e contenuto di `x` non controllati | low, respinto | Un array 1D fallisce subito con un errore esplicito; il controllo sui NaN costerebbe una passata in più su dati che in questo progetto generiamo noi. |
| 5 | La rianimazione non corregge le somme d'epoca | medium, rinviato | Vero, ma è lo stesso comportamento di Faiss (`_apply_splits` non tocca `_pass_sums`) e il passo 2 richiede fedeltà. Aggiunto un commento; registrato in `deferred-work.md` come variante da misurare. |
| 6 | La descrizione in `pyproject.toml` promette la partenza a caldo | false | La descrizione è del progetto, non della funzione; la partenza a caldo è il passo 3 dichiarato nella spec. |
| 7 | `batch_law` e `step_law` senza test | medium | Vero: un refuso in un coefficiente sarebbe passato inosservato. Aggiunto un test con i valori letti dal campo `recipe` di Faiss in tre configurazioni. |
| 8 | Mancano test per `tau=0`, `on_step`, determinismo, `k == n`, duplicati | low, respinto | Rami brevi e senza logica propria; l'errore su `k` è ora coperto dal test del punto 2. |
| 9 | Confronti di qualità deboli e commento fuorviante | low | Vero per nome e commento: rinominato il test in "plain lloyd" e corretto il commento. Il test sullo scarto con `tau=0` non è stato aggiunto: su un seed solo sarebbe instabile, vedi la sezione Sorpresa. |
| 10 | `mse` alloca la matrice n×k intera | medium | Vero: 1,6 GB già con 200.000 punti e 1.024 centroidi, cioè al passo 5. `mse` ora lavora a blocchi di 65.536 righe. |
| 11 | `on_step` riceve gli array vivi e non vede la finalizzazione | low | Vero. Documentato nella docstring; la firma resta invariata. |
| 12 | Demo senza `__main__`, dati duplicati, `matplotlib` tra le dipendenze di esecuzione | low, respinto | È uno script da lanciare, non un modulo da importare; quattro righe duplicate non giustificano un modulo condiviso. |
