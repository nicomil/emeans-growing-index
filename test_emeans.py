import numpy as np

import pytest

from emeans import assign, batch_law, emeans, mse, revive, scheduled_alpha, step_law


def blobs(n=20_000, d=2, centers=40, seed=0):
    rng = np.random.default_rng(seed)
    means = rng.uniform(-10, 10, (centers, d))
    return means[rng.integers(0, centers, n)] + rng.normal(0, 0.6, (n, d))


def lloyd(x, k, iters=25, seed=0):
    rng = np.random.default_rng(seed)
    c = x[rng.choice(len(x), k, replace=False)].copy()
    for _ in range(iters):
        labels, _ = assign(x, c)
        for j in np.unique(labels):
            c[j] = x[labels == j].mean(0)
    return c


def test_matches_plain_lloyd_25_iterations_in_5_epochs():
    x = blobs()
    ours = np.median([mse(x, emeans(x, 64, epochs=5, seed=s)) for s in range(5)])
    reference = np.median([mse(x, lloyd(x, 64, seed=s)) for s in range(5)])
    assert ours < reference * 1.05


def test_works_in_higher_dimension():
    x = blobs(n=10_000, d=32, centers=100)
    c = emeans(x, 128, epochs=3)
    assert c.shape == (128, 32) and np.isfinite(c).all()
    assert mse(x, c) < mse(x, x[:128])  # meglio di 128 punti qualsiasi usati come centroidi


def test_step_of_one_keeps_empty_clusters_finite():
    x = blobs(n=2_000)
    assert np.isfinite(emeans(x, 200, epochs=2, batch_size=50, alpha0=1.0)).all()


def test_alpha_schedule_endpoints():
    assert scheduled_alpha(0.4, 0, 100) == 0.4
    assert np.isclose(scheduled_alpha(0.4, 100, 100), 0.04)


def test_revive_splits_a_heavy_cluster():
    centroids = np.array([[1.0, 1.0], [5.0, 5.0], [9.0, 9.0]])
    mass = np.array([10.0, 0.0, 10.0])
    assert revive(centroids, mass, 0.1, np.random.default_rng(0)) == 1
    assert mass.sum() == 20.0 and sorted(mass) == [5.0, 5.0, 10.0]
    # il cluster morto ora sta accanto a uno dei due vivi
    assert min(np.abs(centroids[1] - 1.0).max(), np.abs(centroids[1] - 9.0).max()) < 1e-2


def test_revive_separates_a_parent_at_the_origin():
    centroids = np.zeros((2, 2))
    revive(centroids, np.array([10.0, 0.0]), 0.1, np.random.default_rng(0))
    assert not (centroids[0] == centroids[1]).all()


# Valori ottenuti da NumpyEmeans di Faiss 1.16.0 (campo recipe) sugli stessi n, k, T, d.
@pytest.mark.parametrize(
    "n, k, epochs, d, batch, alpha0",
    [(20_000, 64, 5, 2, 128, 0.0935), (50_000, 256, 3, 32, 2048, 0.4182), (100_000, 512, 3, 64, 4096, 0.4150)],
)
def test_scaling_laws_match_faiss(n, k, epochs, d, batch, alpha0):
    assert batch_law(n, k, epochs, d) == batch
    assert step_law(n, k, epochs, batch) == pytest.approx(alpha0, abs=5e-5)


@pytest.mark.parametrize("bad", [{"epochs": 0}, {"batch_size": 0}, {"alpha0": 2.0}, {"k": 0}])
def test_rejects_bad_arguments(bad):
    with pytest.raises(ValueError):
        emeans(blobs(n=500), **{"k": 8, **bad})


def test_matches_faiss_emeans():
    # Passo 2: stessa ricetta, stessi dati, errore entro lo 0,2% da NumpyEmeans di Faiss.
    # Dati gaussiani: su gruppi netti l'errore varia troppo da un seed all'altro.
    from faiss.contrib.e_means.e_means import NumpyEmeans

    x = np.random.default_rng(0).standard_normal((30_000, 32)).astype(np.float32)
    ours, theirs = [], []
    for seed in range(7):
        ours.append(mse(x, emeans(x, 128, epochs=3, seed=seed)))
        faiss_run = NumpyEmeans(32, 128, nepochs=3, seed=seed, unused_threshold=0.1)
        theirs.append(mse(x, faiss_run.train(x)[0]))
        assert faiss_run.recipe["batch_size"] == batch_law(30_000, 128, 3, 32)
        assert faiss_run.recipe["alpha0"] == pytest.approx(step_law(30_000, 128, 3, faiss_run.recipe["batch_size"]))
    # Osservato 0,006%. Con la rianimazione spenta lo scarto sale a 0,8%: 0,2% lo coglie.
    assert np.median(ours) == pytest.approx(np.median(theirs), rel=0.002)


def test_warm_start_mass_controls_how_far_centroids_move():
    x = blobs(n=5_000)
    start = emeans(x, 32, epochs=3)
    moved = {
        m: np.abs(emeans(x, 32, epochs=1, init=start, init_mass=m, finalize=False, tau=0) - start).max()
        for m in (1e-10, 1e6)
    }
    assert moved[1e6] < 1e-3 < moved[1e-10]


def test_warm_start_rejects_wrong_init():
    with pytest.raises(ValueError):
        emeans(blobs(n=500), 8, init=np.zeros((7, 2)))
    with pytest.raises(ValueError):
        emeans(blobs(n=500), 8, init=np.zeros((8, 2)), init_mass=-1.0)
    with pytest.raises(ValueError):
        emeans(blobs(n=500), 8, init=np.zeros((8, 2)), init_mass=float("nan"))


def test_huge_mass_with_finalization_is_one_lloyd_pass():
    # Con massa enorme i centroidi non si muovono durante l'epoca: la finalizzazione
    # media i punti assegnati ai centroidi di partenza, cioè fa una passata di Lloyd.
    x = blobs(n=5_000)
    start = emeans(x, 32, epochs=3)
    before = start.copy()
    ours = emeans(x, 32, epochs=1, init=start, init_mass=np.full(32, 1e15), tau=0)
    labels, _ = assign(x, start)
    one_pass = np.array([x[labels == j].mean(0) for j in range(32)])
    assert np.allclose(ours, one_pass) and (start == before).all()


def test_constant_small_step_with_count_mass_is_the_online_mean(monkeypatch):
    # A passo costante e minuscolo, massa = passo × conteggi vecchi rende e-means uguale
    # al mini-batch k-means classico che parte dai conteggi veri. Con il passo a coseno no.
    import emeans as module
    from exp_new_only import K, online_mean

    rng = np.random.default_rng(0)
    start = rng.normal(0, 1, (K, 4))
    counts = rng.integers(50, 500, K).astype(np.float64)
    added = rng.normal(0.5, 1, (3_000, 4))
    expected = online_mean(added, start, counts, 100, seed=7)
    run = lambda: emeans(
        added, K, epochs=1, batch_size=100, alpha0=1e-6, init=start, init_mass=1e-6 * counts,
        tau=0, seed=7, finalize=False,
    )
    assert np.abs(run() - expected).max() > 1e-2  # coseno: i punti nuovi pesano meno
    monkeypatch.setattr(module, "ALPHA_MIN_FACTOR", 1.0)
    assert np.abs(run() - expected).max() < 1e-3


def test_rule_fit_recovers_a_known_rule():
    from exp_rule import MASSES, fit, predict

    target = lambda signal: 0.1 * signal**-0.5  # log m = log 0,1 − 0,5 · log(segnale)
    curve = lambda signal: 1 + (np.log(MASSES) - np.log(target(signal))) ** 2
    # Segnali scelti perché le masse giuste (1; 0,2; 0,1) cadano sulla griglia: tra un punto
    # e l'altro la curva è interpolata, quindi la taratura non distingue masse intermedie.
    signals = (0.01, 0.25, 1.0)
    scenarios = [(signal, f, curve(signal)) for signal in signals for f in (0.05, 0.5)]
    fitted = fit(scenarios)["dal segnale"]
    assert all(predict(fitted, s, 0.2) == pytest.approx(target(s), rel=0.15) for s in signals)


def test_recall_budget_mode_matches_brute_force(monkeypatch):
    # La funzione di recall degli esperimenti, contro una versione ovvia e lenta.
    import exp_real

    rng = np.random.default_rng(0)
    k, top = 16, exp_real.TOP
    monkeypatch.setattr(exp_real, "K", k)
    index = rng.normal(size=(600, 8)).astype(np.float32)
    index /= np.linalg.norm(index, axis=1, keepdims=True)
    queries = index[:40] + 0.05 * rng.normal(size=(40, 8)).astype(np.float32)
    centroids = index[rng.choice(600, k, replace=False)].astype(np.float64)
    centroids[3] = centroids[4]  # centroidi quasi coincidenti, come dopo una rianimazione
    labels = assign(index.astype(np.float64), centroids)[0]
    labels[labels == 7] = 6  # una lista vuota
    threshold = exp_real.tenth_score(index, queries)
    budgets = (0.05, 0.2)
    found = exp_real.recall(index, labels, centroids, queries, threshold, budgets=budgets)

    within = np.lexsort((np.random.default_rng(0).random(len(labels)), labels))  # stesso ordine dentro le liste
    for i, query in enumerate(queries):
        distance = ((centroids - query) ** 2).sum(1)
        scanned = np.concatenate([within[labels[within] == j] for j in np.argsort(distance, kind="stable")])
        for b, budget in enumerate(budgets):
            read = scanned[: int(budget * len(index))]
            expected = min(int((index[read] @ query >= threshold[i] - 1e-6).sum()), top)
            assert abs(int(found[b, i]) - expected) <= 1  # tolleranza per pareggi tra centroidi in float32
    assert found[1].mean() > found[0].mean()
