"""e-means scritto a mano: mini-batch k-means con media mobile esponenziale.

Segue l'Algoritmo 1 di "e-means: outperforming k-means (in one-tenth the
epochs)", arXiv 2611.09501. I numeri di riga nei commenti sono quelli
dell'algoritmo nel paper.

Idea in tre frasi. Ogni centroide ha una posizione c e una massa N, che dice
quanti punti "ricorda". A ogni batch il centroide si sposta verso la media dei
punti che gli sono stati assegnati, tanto più quanto più quei punti pesano
rispetto alla massa che aveva. La massa vecchia viene scontata a ogni passo,
quindi i primi batch, visti con centroidi ancora sbagliati, vengono dimenticati.
"""

import math

import numpy as np

INIT_MASS = 1e-10  # riga 2: massa iniziale quasi nulla, il primo batch decide tutto
REVIVE_EVERY = 5  # riga 9
SPLIT_EPSILON = 1e-4  # di quanto si separano donatore e figlio dopo una divisione
ALPHA_MIN_FACTOR = 0.1  # il passo scende fino a un decimo del valore iniziale

# Coefficienti distribuiti in faiss/contrib/e_means/base.py (Faiss 1.16.0).
# Sono diversi da quelli della Tabella 2 del paper.
_BATCH_LAWS = {  # B = C * k^a * n^b * T^c  (Equazione 7)
    "throughput": (0.035134, 0.134749, 0.876473, 0.813344),
    "quality": (0.00439175, 0.134749, 0.876473, 0.813344),
}
_STEP_LAW = (0.8244, -0.4617, 0.9003, -0.4498, -0.1057)  # Equazione 6


def batch_law(n, k, epochs, d):
    """Dimensione del batch scelta dalla legge di scala, potenza di due."""
    law = "quality" if d <= 16 else "throughput"
    c, a_k, a_n, a_t = _BATCH_LAWS[law]
    batch = 2 ** round(math.log2(c * k**a_k * n**a_n * epochs**a_t))
    cap = n // 2 if law == "quality" else 2 ** round(math.log2(n / 2))
    return max(1, min(batch, cap, n))


def step_law(n, k, epochs, batch):
    """Passo iniziale alpha0: frazione di strada verso i punti in un batch."""
    c, a_k, a_b, a_n, a_t = _STEP_LAW
    return min(max(c * k**a_k * batch**a_b * n**a_n * epochs**a_t, 1e-4), 1.0)


def scheduled_alpha(alpha0, step, total_steps):
    """Coseno decrescente da alpha0 a un decimo di alpha0 (Equazione 5)."""
    cosine = 0.5 * (1.0 + math.cos(math.pi * min(step, total_steps) / max(1, total_steps)))
    return alpha0 * (ALPHA_MIN_FACTOR + (1.0 - ALPHA_MIN_FACTOR) * cosine)


def assign(x, centroids):
    """Indice del centroide più vicino e distanza al quadrato, per ogni punto."""
    # ||x - c||^2 = ||x||^2 - 2 x·c + ||c||^2
    d2 = (x**2).sum(1)[:, None] - 2.0 * x @ centroids.T + (centroids**2).sum(1)[None, :]
    labels = d2.argmin(1)
    return labels, np.maximum(d2[np.arange(len(x)), labels], 0.0)


def revive(centroids, mass, tau, rng):
    """Riga 10: i cluster quasi vuoti rinascono dividendo in due un cluster pieno.

    Modifica centroids e mass sul posto. Restituisce quante divisioni ha fatto.
    """
    dead = mass < tau * mass.mean()
    donors = np.flatnonzero(~dead & (mass > 0))
    targets = np.flatnonzero(dead)
    nsplit = min(len(targets), len(donors))
    if nsplit == 0:
        return 0
    # Donatori estratti in proporzione alla massa: i cluster affollati si dividono di più.
    source = rng.choice(donors, nsplit, replace=False, p=mass[donors] / mass[donors].sum())
    target = targets[:nsplit]
    sign = np.ones(centroids.shape[1])
    sign[1::2] = -1.0
    offset = SPLIT_EPSILON * sign
    parent = centroids[source]
    # Due copie quasi sovrapposte: i batch successivi le allontanano.
    centroids[target] = parent * (1.0 + offset)
    centroids[source] = parent * (1.0 - offset)
    # Un genitore esattamente sull'origine darebbe due copie identiche, mai più separabili.
    same = (centroids[target] == centroids[source]).all(1)
    centroids[target[same], 0] = np.nextafter(centroids[target[same], 0], np.inf)
    mass[target] = mass[source] = mass[source] / 2.0
    return nsplit


def emeans(
    x,
    k,
    epochs=5,
    batch_size=None,
    alpha0=None,
    tau=0.1,
    seed=0,
    on_step=None,
    init=None,
    init_mass=INIT_MASS,
    finalize=True,
):
    """Raggruppa le righe di x in k cluster. Restituisce i centroidi (k, d).

    batch_size e alpha0, se non dati, vengono dalle leggi di scala.
    tau è la soglia di rianimazione; 0 la spegne.

    Partenza a caldo: init sono i centroidi da cui ripartire, di forma (k, d), e
    init_mass è quanto pesano, come numero solo o come vettore di k valori. L'unità
    è "punti per batch": a regime la massa di un cluster vale circa batch_size per
    la quota di punti che gli spetta. Con quella massa il primo batch sposta il
    centroide di una frazione alpha, come in una corsa già avviata; con la massa
    quasi nulla di serie lo sostituisce con la media del batch.

    finalize=False salta la riga 11 e restituisce i centroidi della media mobile.
    Attenzione: con finalize=True il risultato sono le medie dell'ultima epoca, quindi
    la massa non limita di quanto si spostano i centroidi. Con massa enorme e tau=0 i
    centroidi restano fermi durante l'epoca e il risultato è una passata di Lloyd.
    on_step(step, centroids, mass, alpha) viene chiamata dopo ogni aggiornamento,
    prima della finalizzazione. Riceve gli array di lavoro: chi li conserva li copi.
    """
    x = np.asarray(x, dtype=np.float64)
    n, d = x.shape
    if not 1 <= k <= n:
        raise ValueError(f"k deve stare tra 1 e n={n}, ricevuto {k}")
    if epochs < 1 or int(epochs) != epochs:
        raise ValueError(f"epochs deve essere un intero >= 1, ricevuto {epochs}")
    if batch_size is None:
        batch_size = batch_law(n, k, epochs, d)
    if alpha0 is None:
        alpha0 = step_law(n, k, epochs, batch_size)
    if batch_size < 1 or not 0 < alpha0 <= 1:
        raise ValueError(f"servono batch_size >= 1 e 0 < alpha0 <= 1, ricevuti {batch_size} e {alpha0}")
    if init is not None and np.shape(init) != (k, d):
        raise ValueError(f"init deve avere forma {(k, d)}, ricevuta {np.shape(init)}")
    rng = np.random.default_rng(seed)
    batch_size = min(batch_size, n)
    starts = range(0, n, batch_size)
    total_steps = epochs * len(starts)

    if init is None:
        centroids = x[rng.choice(n, k, replace=False)].copy()  # riga 1
    else:
        centroids = np.array(init, dtype=np.float64)
    mass = np.broadcast_to(np.asarray(init_mass, dtype=np.float64), (k,)).copy()  # riga 2
    if not (mass >= 0).all():  # rifiuta anche NaN
        raise ValueError("init_mass non può essere negativa")
    step = 0
    for epoch in range(epochs):  # riga 3
        order = rng.permutation(n)
        # Conteggi e somme dell'epoca: servono solo alla finalizzazione (riga 11).
        epoch_counts = np.zeros(k)
        epoch_sums = np.zeros((k, d))
        for start in starts:  # riga 4
            batch = x[order[start : start + batch_size]]
            alpha = scheduled_alpha(alpha0, step, total_steps)  # riga 5
            labels, _ = assign(batch, centroids)  # riga 6
            counts = np.bincount(labels, minlength=k).astype(np.float64)  # riga 7
            sums = np.zeros((k, d))
            np.add.at(sums, labels, batch)
            epoch_counts += counts
            epoch_sums += sums

            # Riga 8. Il paper scrive N <- gamma N + alpha n, S <- gamma S + alpha s
            # con gamma = 1 - alpha e c = S / N. Qui la stessa cosa è scritta su c e N,
            # così un cluster senza punti resta fermo anche quando alpha vale 1.
            mass *= 1.0 - alpha
            hit = counts > 0
            new_mass = mass[hit] + alpha * counts[hit]
            weight = alpha * counts[hit] / new_mass  # quanto conta il batch rispetto al passato
            batch_mean = sums[hit] / counts[hit, None]
            centroids[hit] += weight[:, None] * (batch_mean - centroids[hit])
            mass[hit] = new_mass

            step += 1
            # Riga 9. Come in Faiss, le somme d'epoca non vengono corrette dopo una divisione.
            if tau > 0 and step % REVIVE_EVERY == 0:
                revive(centroids, mass, tau, rng)
            if on_step is not None:
                on_step(step, centroids, mass, alpha)

    if finalize:
        # Riga 11: media semplice dei punti assegnati durante l'ultima epoca.
        seen = epoch_counts > 0
        centroids[seen] = epoch_sums[seen] / epoch_counts[seen, None]
    return centroids


def mse(x, centroids):
    """Distanza al quadrato media tra ogni punto e il suo centroide."""
    x = np.asarray(x, dtype=np.float64)
    # A blocchi: la matrice delle distanze intera occuperebbe 8 * n * k byte.
    return float(sum(assign(x[i : i + 65536], centroids)[1].sum() for i in range(0, len(x), 65536)) / len(x))
