---
title: 'Passo 6: consolidamento dei risultati e bozze per la pubblicazione'
type: 'feature'
created: '2026-11-23'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/planning-artifacts/piano-passo-6-consolidamento.md'
  - '{project-root}/_bmad-output/planning-artifacts/briefs/brief-rag_emean-2026-11-22/brief.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** I risultati del passo 5 poggiavano su un corpus, un modello di embedding, tre seed senza intervalli e tempi misurati una volta. L'obiettivo è un piccolo post su LinkedIn e poi una segnalazione nel repository di Faiss: servono dati accurati ed esperimenti validi prima di arrivarci.

**Approach:** In una notte di lavoro senza sovrapposizioni tra i calcoli: secondo corpus, secondo modello di embedding, intervalli di confidenza, tempi puliti, controllo della misura contro Faiss, dimostrazione della causa con il codice di Faiss, e le bozze dei due testi. Nessun testo viene pubblicato: l'invio è una decisione dell'utente.

</frozen-after-approval>

## Implementation Notes

**Cosa è stato eseguito**

Lavori in fila, uno alla volta, registrati in `data/night.log`: embedding, esperimento su ogni insieme di dati, controllo del recall, tempi per ultimi a macchina libera. Zero lavori falliti nella prima parte.

| Attività del piano | Esito |
|---|---|
| 6.0 Brief | approvato il 23 novembre, filo ibrido |
| 6.1 Avviso verificato con il codice di Faiss | confermato; in più, la correzione fatta con il codice di Faiss ripristina il recall |
| 6.2 Letteratura recente | tema non coperto; trovato lavoro attivo sulla rianimazione nel repository di Faiss (#5907, #5915) |
| 6.3 Secondo corpus | arXiv, risultati concordi, deriva più debole |
| 6.4 Rinforzi alla misura | intervalli, due livelli di costo, tempi ripetuti, secondo modello di embedding, controllo contro IndexIVFFlat |
| 6.5 Scrittura | bozza del post e della segnalazione; l'articolo lungo non è stato scritto |
| 6.6 Revisione finale | fatta sui tre documenti brevi |

**File nuovi o riscritti**

`exp_real.py`, `bench_rebuild.py`, `check_recall_vs_faiss.py`, `check_faiss_naive.py`, `analyze.py`, `embed_corpus.py`, `run_night2.sh`, `README.md`, `docs/RAPPORTO.md`, `docs/linkedin-post-bozza.md`, `docs/faiss-issue-bozza.md`, `docs/repro_emeans_init_centroids.py`, `results/SINTESI.md` e i file di risultati per insieme di dati.

**Risultati**

Sono in `results/SINTESI.md`; il riassunto ragionato è in `docs/RAPPORTO.md`. In breve, su tre insiemi di dati:

- l'uso ingenuo di e-means (centroidi vecchi come partenza, addestramento sui soli testi nuovi) abbassa il recall del 30-58% dopo un solo aggiornamento da 10.000 testi anche ricostruendo le liste, quanto una partenza da righe a caso; k-means usato allo stesso modo perde il 5-24%; con 50.000 testi nuovi e-means perde il 4-15%;
- le cause sono il peso quasi nullo dei centroidi di partenza e le medie finali calcolate sui soli testi nuovi; corrette entrambe con il codice di Faiss, il recall torna al livello del mini-batch k-means classico;
- il ricalcolo completo con e-means a tre epoche arriva a 0,2-0,7 punti di recall dal riferimento in 4-7 secondi;
- e-means è oltre 4-5 volte più veloce di k-means a parità di errore, 2,5-4 volte a parità di recall con lo 0,1% dell'indice letto, e non è più veloce a parità di recall con l'1% letto.

**Due affermazioni precedenti corrette da questo passo**

- "e-means è 5 volte più veloce" valeva per l'errore, non per il recall in generale.
- "il recall crolla da 0,83 a 0,05" valeva con le liste lasciate come sono; con le liste ricostruite, che è il caso realistico, scende a 0,42 dopo un aggiornamento.

**Sorprese**

- Con il modello a 768 dimensioni la partenza a caldo con massa a regime dà mezzo punto di recall in più della partenza da zero, differenza piccola ma coerente tra i seed; con il modello a 384 dimensioni non dà nulla.
- Un file di tempi rimasto da una prova a scala ridotta stava per entrare nella sintesi: lo ha notato la revisione. Ora ogni uscita è scritta su un file provvisorio e sostituisce la precedente solo se il lavoro riesce.

**Non fatto**

- La prova sul ramo principale di Faiss non è stata fatta nella notte: il sistema ha negato l'esecuzione dei sorgenti appena scaricati e il blocco non è stato aggirato. È stata fatta la mattina del 23 novembre con l'autorizzazione dell'utente, compilando Faiss al commit 16a95d6: il danno dell'uso ingenuo resta (dal 16% al 47% di recall in meno) e, con la nuova rianimazione, massa iniziale e media mobile non bastano più a toglierlo.
- arXiv con il secondo modello di embedding: in coda per ultimo, per via della durata dell'embedding.
- L'articolo lungo previsto dal piano.

## Review Triage Log

Tre revisioni in questo passo. I rilievi sono tanti: qui gli esiti per gruppo; il dettaglio è nei messaggi di commit `5d3dd4a` e successivi.

| Revisione | Rilievi | Corretti | Esito dei principali |
|---|---|---|---|
| Codice notturno (Blind Hunter) | 16 | 13 | Lettura casuale dentro le liste parziali; salvataggio per seed; due unità di "massa" nominate; partenza a caldo senza medie finali aggiunta; ripetizioni dei tempi bilanciate con carico registrato; confronto a parità di errore come forchetta e non per interpolazione; test del recall contro una versione ovvia; riga con k-means nella riproduzione. Respinti: blocco contro una seconda istanza della coda, correzione per confronti multipli (dichiarata nei limiti), revisioni fissate di dataset e modelli (dichiarate nei limiti). |
| Bozza della segnalazione, letta da manutentore | 30 circa | quasi tutti | Riscritta come richiesta di documentazione; riconosciuto ciò che il codice già documenta; causa mostrata con il codice di Faiss; liste ricostruite in primo piano; percentuali corrette (dal 30% al 58%); unità della massa precisata; dichiarato che la correzione serve a poco in pratica. Non fatto: prova sul ramo principale. |
| Documenti finali, numero per numero | 45 circa | quasi tutti | Nessun numero inventato, ma: numeri delle notizie presentati come generali, tempi di addestramento chiamati "ricalcolo dell'indice", rapporti di tempo a parità di recall fondati su differenze di pochi millesimi, e soprattutto nessun confronto generico sui dati veri. Aggiunto `check_naive_baselines.py`: k-means usato allo stesso modo perde dal 5% al 24%, e-means dal 30% al 58% e quanto una partenza da righe a caso; con aggiornamenti da 50.000 testi il danno scende al 4-15%. Post, segnalazione e rapporto riscritti di conseguenza. Verdetto del revisore sulla segnalazione prima delle correzioni: non pronta. Dopo: resta aperta la prova sul ramo principale di Faiss. |
