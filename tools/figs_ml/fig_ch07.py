import os, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "code")
plt.rcParams.update({"font.size": 11})
BLUE, ORANGE, TEAL, RED = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26"
fig, axs = plt.subplots(1, 2, figsize=(11, 4.2), dpi=110)
ns = {}; src = open(os.path.join(here, "c07_early_stop.py")).read()
exec(src.replace('print(', '(lambda *a: None)('), ns)
ax = axs[0]
ax.plot(range(1, 601), ns["tr"], color=BLUE, lw=2, label="train MSE")
ax.plot(range(1, 601), ns["va"], color=ORANGE, lw=2, label="validation MSE")
ax.axvline(ns["best"], color=TEAL, ls="--", lw=2, label="best round = %d" % ns["best"])
ax.set_ylim(0, 12); ax.set_xlabel("number of trees"); ax.set_ylabel("MSE"); ax.set_title("Early stopping: boosting on Friedman1"); ax.grid(alpha=.3); ax.legend(frameon=False)
from sklearn.ensemble import HistGradientBoostingRegressor
rng = np.random.default_rng(0)
x = rng.uniform(0, 10, 400); y = 0.5 * x + rng.normal(0, 1.5, 400)
grid = np.linspace(0, 10, 400).reshape(-1, 1)
ax = axs[1]; ax.scatter(x, y, s=8, color="#999999", label="data")
for cst, c, lab in [(None, ORANGE, "unconstrained"), ([1], TEAL, "monotonic_cst=[1]")]:
    m = HistGradientBoostingRegressor(max_iter=300, learning_rate=0.1, monotonic_cst=cst, random_state=0).fit(x.reshape(-1, 1), y)
    ax.plot(grid, m.predict(grid), color=c, lw=2, label=lab)
ax.set_xlabel("x"); ax.set_ylabel("prediction"); ax.set_title("Monotonic constraint on a noisy line"); ax.grid(alpha=.3); ax.legend(frameon=False)
fig.tight_layout(); fig.savefig("ch07_earlystop_mono.png"); plt.close(fig)
