---
title: 'Attività 6.1 e 6.2: verifica con Faiss e letteratura recente'
status: done
created: 2026-11-22
---

# Attività 6.1 e 6.2

## 6.1 L'uso ingenuo rompe l'indice anche con il codice di Faiss

`check_faiss_naive.py` ripete l'aggiornamento sui soli articoli nuovi chiamando `NumpyEmeans.train(nuovi, init_centroids=vecchi)` di Faiss 1.16.0, senza toccare alcuna impostazione. Recall@10 leggendo l'1% dell'indice, mediana su 3 seed (tabella completa in `results/check_faiss_naive.md`):

| Aggiornamento | Dopo 1 giro | Dopo 5 | Dopo 10 |
|---|---|---|---|
| mai aggiornare | 0,829 | 0,806 | 0,781 |
| e-means riscritto a mano | 0,153 | 0,072 | 0,052 |
| e-means di Faiss | 0,144 | 0,070 | 0,052 |

Il crollo non dipende dalla nostra riscrittura. Il risultato 2 del piano è confermato e si può scrivere riferendolo al codice distribuito.

## 6.2 Letteratura e progetti usciti dopo il paper

Ricerca fatta il 22 novembre 2026, sedici giorni dopo il paper. Non ho trovato alcuno studio su e-means usato in modo incrementale, con partenza dai centroidi esistenti di un indice, o sotto deriva dei dati. Ho trovato quattro cose pertinenti:

| Fonte | Cosa fa | Cosa copre dei nostri risultati |
|---|---|---|
| [h-means](https://github.com/heldernoid/hmeans), progetto indipendente | Partenza gerarchica costruita sopra e-means: prima pochi centroidi, poi divisioni. Gira su CPU; dichiara un errore di addestramento più basso dello 0,03-6,7% rispetto a e-means a 5 passate. | "Partenza a caldo" in un altro senso: dentro una sola costruzione, non da un indice esistente. Nessun aggiornamento, nessuna deriva. |
| [PISCES](https://huggingface.co/Nabidnur/PISCES), rapporto tecnico indipendente | Variante di e-means. Critica la rianimazione dei cluster morti: il centroide rinato è una copia quasi identica del donatore. Misura il recall di un indice IVF su DEEP1B: pari a e-means entro 0,02 punti in media. Gira su una CPU a 4 core. | Tocca la rianimazione, ma per un difetto diverso dal nostro (copie sovrapposte, non riciclo di cluster ancora in uso). Recall su immagini, non su testo. Nessun aggiornamento. |
| [Richiesta in Milvus](https://github.com/milvus-io/milvus/issues/55762), aperta il 20 novembre 2026 | Chiede di offrire e-means come opzione per costruire indici IVF. Un contributore risponde che Faiss verrà aggiornato "in circa una settimana". | Nessuno. Mostra però che i motori vettoriali stanno per adottarlo: l'avviso sull'uso incrementale arriva nel momento giusto. La richiesta stessa nota che i tempi dichiarati dal paper non garantiscono un guadagno in Milvus. |
| [Paper e-means](https://arxiv.org/abs/2611.09501), Appendice M | Parla di "deriva" dell'indice approssimato usato durante l'addestramento a scala molto grande. | È un altro fenomeno, con lo stesso nome. Va chiarito nel testo per non confondere. |

Restano i lavori sulla deriva precedenti a e-means, già noti: [DeDrift](https://arxiv.org/abs/2308.02752), [Ada-IVF](https://arxiv.org/abs/2411.00970), [SPFresh](https://arxiv.org/abs/2410.14452). Nessuno usa e-means.

**Esito.** Il tema non risulta coperto. Lo studio si può presentare come: replica indipendente su testo e su portatile, più un avviso e un risultato negativo sull'uso incrementale che nessuno ha ancora documentato.

**Limiti della ricerca.** Motore di ricerca generale, tre interrogazioni, più la lettura di tre pagine. Non ho consultato l'elenco delle citazioni del paper su Semantic Scholar o Google Scholar, né le discussioni nel repository di Faiss successive al rilascio. Sedici giorni sono pochi: va ripetuta prima di pubblicare.
