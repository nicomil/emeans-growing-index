---
title: 'Passo 2: verifica contro e-means di Faiss'
type: 'feature'
created: '2026-11-22'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/spec-1-emeans-numpy-2d.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Il confronto tra `emeans.py` e l'implementazione di Faiss è stato fatto una volta sola, in un ambiente temporaneo fuori dal progetto. Se il codice cambia, nulla avvisa che non equivale più all'originale.

**Approach:** Portare il confronto dentro la suite di test del progetto: stessi dati, stessa ricetta, stesso numero di epoche, errore mediano entro l'1%.

</frozen-after-approval>

## Implementation Notes

- `faiss-cpu==1.16.0` aggiunto alle dipendenze di sviluppo, con versione fissata: i coefficienti delle leggi di scala sono quelli di questa versione.
- Nuovo test `test_matches_faiss_emeans` in `test_emeans.py`: 30.000 punti gaussiani a 32 dimensioni, 128 cluster, 3 epoche, 7 seed. Controlla anche che batch e passo iniziale coincidano con il campo `recipe` di Faiss.
- Faiss viene chiamato con `unused_threshold=0.1` per allinearlo alla nostra scelta; sopra le 2 dimensioni è anche il suo valore di serie.
- Dati gaussiani e non a gruppi netti, per il motivo descritto nella sezione Sorpresa della spec del passo 1.
- Risultato: errore mediano 24,8958 contro 24,8972 di Faiss, differenza dello 0,006%.

Non c'è uno script di confronto separato: il test basta e gira con il resto della suite.

La revisione di questo passo è stata fatta insieme a quella del passo 3; il registro è in `spec-3-partenza-a-caldo.md`.
