---
title: 'Passo 5: verifica su embedding veri, con il recall di una ricerca'
type: 'feature'
created: '2026-11-22'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context:
  - '{project-root}/docs/percorso/brief.md'
  - '{project-root}/docs/percorso/spec-d-aggiornamenti-in-sequenza.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Tutte le conclusioni del progetto vengono da dati sintetici e dall'errore di quantizzazione. Quattro di esse sono cadute in revisione. Non si sa quali reggano su testo reale, né quanto valgano nella misura che interessa a chi usa un indice: il recall di una ricerca.

**Approach:** Ripetere il confronto tra le strategie di aggiornamento su un corpus testuale con date reali, inserito in ordine cronologico, misurando sia l'errore nelle liste sia il recall@10 a costo di ricerca fisso. Aggiungere il confronto diretto tra ricalcolo completo con e-means e con k-means classico.

</frozen-after-approval>

## Implementation Notes

**Codice**

- `embed_news.py`: scarica il corpus e calcola gli embedding. `uv run --group real embed_news.py`, alcuni minuti, una volta sola. Scrive in `data/`, che non è sotto controllo di versione.
- `exp_real.py`: l'esperimento. `uv run exp_real.py > results/exp_real.md`, circa dieci minuti.
- `exp_new_only.py` e `exp_rule.py`: due funzioni ricavano ora numero di centroidi e dimensione dagli argomenti, invece che dalle costanti dei dati sintetici.

**Dati**

- Corpus: titoli e sommari di HuffPost, 209.119 articoli dal 28 gennaio 2012 al 23 settembre 2022 (`heegyu/news-category-dataset` su Hugging Face). Circa 30.000 articoli l'anno fino al 2017, poi molti meno.
- Embedding: `all-MiniLM-L6-v2`, 384 dimensioni, vettori normalizzati.
- 3.000 articoli estratti a caso e tenuti fuori dall'indice fanno da interrogazioni.

**Disegno**

- Indice iniziale: i primi 100.000 articoli, fino all'8 febbraio 2015. Poi dieci giri da 10.000 articoli in ordine di data, fino al primo settembre 2019: l'indice raddoppia. I giri hanno lo stesso numero di articoli, non la stessa durata: il primo copre quattro mesi, gli ultimi cinque tre anni, perché il corpus si dirada dopo il 2017. Gli articoli successivi al settembre 2019 restano fuori.
- 2.048 liste (4 volte la radice di 200.000, arrotondato a potenza di due, come nell'Appendice L del paper): circa 50 articoli per lista all'inizio, 100 alla fine.
- Recall@10: per ogni interrogazione si sondano le liste più vicine fino a leggere esattamente l'1% dell'indice, e si conta quanti candidati sono vicini almeno quanto il decimo articolo vero. Così il costo di ricerca è identico per tutte le strategie, e duplicati e pareggi (il corpus ne contiene) non contano come errori.
- Si usano solo le interrogazioni datate entro il periodo che l'indice copre: 1.536 dopo un giro, 2.136 dopo cinque, 2.898 dopo dieci. Il recall non è quindi confrontabile tra giri diversi, solo tra strategie nello stesso giro.
- Errore nelle liste: ogni articolo resta nella lista in cui è stato inserito, tranne per le strategie che rileggono tutto.
- Controllo senza deriva: gli stessi 200.000 articoli in ordine casuale, in un indice costruito sui primi 100.000 e mai aggiornato.
- 3 seed dell'algoritmo; il corpus e le interrogazioni sono fissi.

**Risultati dopo dieci giri (indice raddoppiato, 2015 → 2019)**

Mediana su 3 seed; [min; max] è la sola variabilità dell'algoritmo. "Periodo aggiunto": le 1.508 interrogazioni datate dopo l'indice iniziale.

| Strategia | Epoche spese in 10 giri | Errore nelle liste | Recall [min; max] | Recall, periodo aggiunto |
|---|---|---|---|---|
| mai aggiornare | 0 | +5,61% | 0,781 [0,779; 0,783] | 0,728 |
| mai aggiornare, ordine casuale (controllo senza deriva) | 0 | +1,99% | 0,831 [0,828; 0,832] | 0,823 |
| e-means, impostazioni di serie (solo nuovi) | 0,5 | +143,66% | 0,052 [0,052; 0,054] | 0,080 |
| mini-batch dalle dimensioni delle liste (solo nuovi) | 0,5 | +2,84% | 0,805 [0,801; 0,806] | 0,765 |
| e-means, massa 0,2 (solo nuovi) | 0,5 | +4,87% | 0,808 [0,805; 0,808] | 0,776 |
| a caldo su tutti i dati, 1 epoca a giro | circa 8 | +2,64% | 0,824 [0,821; 0,825] | 0,811 |
| da zero su tutti i dati, 1 epoca | 1 | +3,33% | 0,822 [0,819; 0,822] | 0,810 |
| a caldo su tutti i dati, 3 epoche a giro | circa 23 | +0,34% | 0,840 [0,837; 0,840] | 0,829 |
| da zero su tutti i dati, 3 epoche | 3 | +0,58% | 0,838 [0,837; 0,842] | 0,828 |
| da zero su tutti i dati, 10 epoche (riferimento) | 10 | 0 | 0,843 [0,842; 0,843] | 0,835 |

Le epoche sono in unità dell'indice finale. Le strategie a caldo ripartono a ogni giro dai propri centroidi, quindi il loro costo si somma; quelle da zero si possono fare una volta sola, quando serve.

Dopo un solo giro (10% di articoli in più, 1.536 interrogazioni): mai aggiornare 0,829; mini-batch 0,827; una epoca a caldo 0,798 e da zero 0,797; tre epoche a caldo 0,826 e da zero 0,825; riferimento 0,834.

Ricalcolo completo dell'indice finale con le implementazioni di Faiss, su un Mac M1 con 8 thread. Una misura per seed, errore sui dati di addestramento.

| Metodo | Tempo mediano | Errore mediano |
|---|---|---|
| e-means, 3 epoche | 4,4 s | 0,6099 |
| k-means classico, 3 iterazioni | 2,8 s | 0,6264 |
| k-means classico, 5 iterazioni | 4,6 s | 0,6192 |
| k-means classico, 10 iterazioni | 9,2 s | 0,6136 |
| k-means classico, 25 iterazioni | 22,7 s | 0,6108 |

**Cosa regge sui dati veri**

1. **La deriva c'è ed è misurabile.** Un indice mai aggiornato arriva a un recall di 0,781 contro 0,843 di uno ricalcolato: 6,2 punti in meno. Il controllo in ordine casuale dà 0,831: di quei 6,2 punti, 1,2 vengono dall'avere centroidi tarati su metà dei dati e 5,0 dalla deriva. Sulle interrogazioni del periodo aggiunto la perdita è di quasi 11 punti (0,728 contro 0,835).
2. **L'uso ingenuo di e-means distrugge l'indice.** Addestrarlo sui soli articoli nuovi partendo dai centroidi vecchi, con le impostazioni di serie, porta il recall a 0,153 dopo un giro e a 0,052 dopo dieci.
3. **Sui soli articoli nuovi, e-means con massa ridotta non si distingue dal mini-batch k-means classico**: recall 0,808 contro 0,805, una differenza che tre seed e interrogazioni fisse non permettono di attribuire, con errore nelle liste più alto (+4,87% contro +2,84%). Entrambi recuperano circa il 40% del recall perso.
4. **Il ricalcolo completo con e-means è la scelta giusta a questa scala.** Tre epoche danno un recall di 0,838, a mezzo punto dal riferimento. Con le implementazioni di Faiss, e-means a 3 epoche impiega 4,4 secondi e raggiunge un errore di 0,6099; il k-means classico nello stesso tempo (5 iterazioni, 4,6 secondi) si ferma a 0,6192, e per arrivare a 0,6108 gliene servono 25, cioè 22,7 secondi. A parità di errore e-means è circa 5 volte più veloce su un portatile; il paper dichiara 8-15 volte su 64 core.
5. **Partire dai centroidi vecchi non si vede nella ricerca.** A pari epoche per giro l'errore è più basso di 0,2-0,9 punti, ma il recall è lo stesso entro la variabilità (0,840 contro 0,838; 0,824 contro 0,822), e la partenza a caldo va ripetuta a ogni giro. La partenza a caldo qui usa la massa quasi nulla di serie: con una massa non nulla non è stata provata su questi dati.
6. **Una epoca sola non basta.** Dopo il primo giro, ricalcolare con una epoca dà un recall di 0,797-0,798, peggio che non aggiornare affatto (0,829). Con 50-100 articoli per lista servono almeno tre epoche.

**Conclusione del progetto, a questo punto**

Con e-means il ricalcolo completo costa così poco che le scorciatoie incrementali non convengono: quelle che non rileggono i vettori recuperano meno della metà del recall perso, e l'unico modo di usare e-means in incrementale senza precauzioni fa danni gravi. La domanda del brief, quanto fidarsi dei centroidi vecchi, ha una risposta pratica diversa da quella cercata: non serve fidarsi, conviene ricalcolare.

**Limiti**

- Un solo corpus, un solo modello di embedding, 200.000 vettori. A scale molto più grandi il ricalcolo completo costa di più e il bilancio può cambiare.
- Tre seed dell'algoritmo con corpus e interrogazioni fissi: la variabilità riportata è quella dell'algoritmo. Differenze di pochi millesimi di recall tra strategie vicine non sono distinguibili; manca un intervallo sulle interrogazioni.
- Dopo il primo giro il recall del periodo aggiunto poggia su 146 interrogazioni.
- L'errore degli articoli nuovi sui centroidi vecchi comprende una parte che non è deriva: con 50 articoli per lista in 384 dimensioni anche articoli dello stesso periodo, non visti in addestramento, hanno un errore più alto del 5% circa (misura del revisore).
- Testi brevi (titolo e sommario), non i pezzi di documento tipici di un sistema RAG. Le interrogazioni sono articoli tenuti fuori, non domande di utenti: il recall vale per "trova articoli simili".
- Recall a un solo livello di costo (1% dell'indice letto).
- Tempi: una misura per seed, sempre nello stesso ordine, nello stesso processo, senza recall associato.
- Non è misurato il costo di riscrivere le liste per le strategie che rileggono tutto.
- La massa 0,2 viene dalla taratura sui dati sintetici; la regola dal segnale del passo 4b non è stata riprovata.
- Dataset e modello non sono fissati a una revisione; gli embedding non sono sotto controllo di versione.
- Nessun confronto con i metodi della letteratura che dividono e riassegnano i cluster.

## Review Triage Log

Un revisore senza contesto (Blind Hunter), 15 rilievi. Ha verificato su un seed con codice proprio.

| # | Rilievo | Verdetto | Evidenza ed esito |
|---|---|---|---|
| 1 | Il numero di interrogazioni dichiarato era sbagliato e cambia tra i giri | medium | Vero: 1.536, 2.136, 2.898, non 3.000. Ora è stampato per ogni giro e dichiarato nel disegno. |
| 2 | Il recall del periodo aggiunto al primo giro poggia su 146 interrogazioni | low | Vero. Stampato e dichiarato nei limiti. |
| 3 | [min; max] misura solo il rumore dell'algoritmo | medium | Vero. Dichiarato in tabella e nei limiti; riformulate le conclusioni 3 e 5 come "non si distingue". Nessun bootstrap sulle interrogazioni. |
| 4 | Manca il controllo senza deriva | high | Vero. Aggiunto l'ordine casuale: 0,831 contro 0,781. La conclusione 1 ora separa i 5,0 punti dovuti alla deriva dagli 1,2 dovuti alla crescita. |
| 5 | Il divario tra dati visti e non visti non è separato dalla deriva | medium | Vero. Dichiarato nei limiti con la misura del revisore. |
| 6 | Il limite dell'1% veniva superato, in misura diversa per strategia | medium | Vero: fino al 6% di letture in più per le liste sbilanciate. Ora l'ultima lista è letta solo in parte. Il recall di chi non aggiorna è sceso da 0,788 a 0,781. |
| 7 | Duplicati e pareggi non gestiti | low | Vero. Il recall ora conta i candidati vicini almeno quanto il decimo vero. |
| 8 | Le righe a caldo non dichiarano il costo cumulato e usano massa quasi nulla | medium | Vero. Aggiunta la colonna delle epoche spese; la massa è dichiarata nella conclusione 5 e nei limiti. |
| 9 | Manca il costo delle strategie incrementali e della riscrittura delle liste | medium | Aggiunta la colonna delle epoche. Il costo di riscrittura resta nei limiti. |
| 10 | Un solo punto per metodo nel confronto dei tempi | medium | Vero. Aggiunto il k-means a 3, 5, 10 e 25 iterazioni: la conclusione 4 ora è espressa a parità di tempo e a parità di errore. |
| 11 | Protocollo dei tempi debole | low | Stampato il numero di thread e dichiarato il protocollo. Ripetizioni e ordine alternato non aggiunti. |
| 12 | Manca il raccordo tra e-means scritto a mano e quello di Faiss | low | Salvato l'errore assoluto del riferimento nel file grezzo. |
| 13 | Le interrogazioni sono articoli, non richieste di utenti | low | Vero. Dichiarato nel docstring e nei limiti. |
| 14 | I giri sono uguali per numero, non per durata; il tratto 2019-2022 resta fuori | low | Vero. Dichiarato nel disegno e in testa alle tabelle. |
| 15 | Riproducibilità e controlli d'ingresso | low | Aggiunti due controlli sul file degli embedding. Revisioni di dataset e modello non fissate: dichiarato nei limiti. |
