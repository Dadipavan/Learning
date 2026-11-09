import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, Rd, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
rng = np.random.default_rng(1)
n = 2000
def one(effect=1.0):
    out = []
    for e in (0.0, effect):
        x = rng.gamma(4, 5, n); y = 0.6 * x + rng.normal(0, 9, n) + e
        out.append((x, y))
    return out
(xc, yc), (xt, yt) = one()
fig, ax = plt.subplots(1, 2, figsize=(9, 4.2))
ax[0].scatter(xc[:600], yc[:600], s=6, alpha=.45, color=B)
xs = np.linspace(0, 70, 2)
ax[0].plot(xs, 0.6 * xs, color=O, lw=2, label="what pre-period spend explains")
ax[0].set_xlabel("pre-experiment spend (X)"); ax[0].set_ylabel("experiment spend (Y)")
ax[0].set_title("X explains part of the noise in Y"); ax[0].legend(frameon=False, fontsize=9)
naive, cup = [], []
for _ in range(1500):
    (xc, yc), (xt, yt) = one()
    x = np.concatenate([xc, xt]); y = np.concatenate([yc, yt])
    th = np.cov(x, y)[0, 1] / x.var(ddof=1)
    naive.append(yt.mean() - yc.mean())
    cup.append((yt - th * (xt - x.mean())).mean() - (yc - th * (xc - x.mean())).mean())
bins = np.linspace(-1.5, 3.5, 50)
ax[1].hist(naive, bins, alpha=.6, color=O, label=f"naive (SD {np.std(naive):.2f})")
ax[1].hist(cup, bins, alpha=.6, color=T, label=f"CUPED (SD {np.std(cup):.2f})")
ax[1].axvline(1.0, color="k", ls="--", lw=1); ax[1].text(1.05, ax[1].get_ylim()[1]*.92, "true lift", fontsize=9)
ax[1].set_xlabel("estimated lift over 1,500 repeated experiments"); ax[1].set_yticks([])
ax[1].set_title("Same unbiased answer, narrower spread"); ax[1].legend(frameon=False, fontsize=9)
plt.tight_layout(); plt.savefig("ch12_cuped.png", dpi=110)
