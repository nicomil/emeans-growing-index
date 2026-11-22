"""Genera emeans_2d.gif: i centroidi di e-means che si muovono su punti 2D.

Uso: uv run demo_2d.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from emeans import emeans, mse

N, K, EPOCHS, FRAME_EVERY = 20_000, 64, 5, 8

rng = np.random.default_rng(0)
means = rng.uniform(-10, 10, (40, 2))
x = means[rng.integers(0, 40, N)] + rng.normal(0, 0.6, (N, 2))

frames = []


def record(step, centroids, mass, alpha):
    if step == 1 or step % FRAME_EVERY == 0:
        frames.append((step, centroids.copy(), mass.copy(), alpha))


final = emeans(x, K, epochs=EPOCHS, on_step=record)
frames.append((frames[-1][0], final, frames[-1][2], 0.0))  # dopo la finalizzazione

fig, ax = plt.subplots(figsize=(7, 7))
ax.scatter(x[::10, 0], x[::10, 1], s=2, c="#bbbbbb")
dots = ax.scatter([], [], c="#d62728", edgecolors="black", linewidths=0.5)
ax.set_xticks([])
ax.set_yticks([])


def draw(i):
    step, centroids, mass, alpha = frames[i]
    dots.set_offsets(centroids)
    # area del punto proporzionale alla massa: i cluster "pesanti" si vedono
    dots.set_sizes(20 + 200 * mass / mass.max())
    label = "finalizzato" if i == len(frames) - 1 else f"passo {step}, alpha {alpha:.3f}"
    ax.set_title(f"e-means, {label}, MSE {mse(x, centroids):.3f}")
    return (dots,)


FuncAnimation(fig, draw, frames=len(frames)).save("emeans_2d.gif", fps=12)
print(f"emeans_2d.gif: {len(frames)} fotogrammi, MSE finale {mse(x, final):.4f}")
