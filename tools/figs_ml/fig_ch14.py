import os, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "code")
plt.rcParams.update({"font.size": 11})
BLUE, ORANGE, TEAL, RED, PURPLE = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
# Figure 1: time series
ns = {}; src = open(os.path.join(here, "c14_series.py")).read()
exec(src.replace("print(", "(lambda *a, **k: None)("), ns)
y, resid, z, sigma, days = ns["y"], ns["resid"], ns["z"], ns["sigma"], ns["days"]
r, k, h = ns["r"], ns["k"], ns["h"]
S = np.zeros(days); s = 0.0
for t in range(56, days):
    s = max(0.0, s + r[t] - k); S[t] = s
fig, axs = plt.subplots(3, 1, figsize=(8, 7.2), dpi=110, sharex=True)
axs[0].plot(y, color=BLUE, lw=1.5); axs[0].set_ylabel("daily metric"); axs[0].set_title("Raw series: weekly rhythm hides the spike")
axs[1].plot(resid / sigma, color=TEAL, lw=1.3); axs[1].axhline(4, color=RED, ls="--"); axs[1].axhline(-4, color=RED, ls="--")
axs[1].set_ylabel("robust z of residual"); axs[1].set_title("After removing the weekday profile")
axs[2].plot(S / sigma, color=ORANGE, lw=1.8); axs[2].axhline(h / sigma, color=RED, ls="--", label="threshold h = 5 sigma")
axs[2].axvline(100, color="#555555", ls=":", label="true shift (day 100)"); axs[2].set_ylabel("CUSUM (in sigma)"); axs[2].set_xlabel("day"); axs[2].legend(frameon=False, loc="upper left")
axs[2].set_title("CUSUM on the clipped residual")
for a in axs: a.grid(alpha=.3)
fig.tight_layout(); fig.savefig("ch14_series.png"); plt.close(fig)

# Figure 2: Isolation Forest versus LOF on correlated data
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
rng = np.random.default_rng(0)
C = np.array([[1, 0.9], [0.9, 1]]); Xn = rng.multivariate_normal([0, 0], C, 600)
Xa = np.array([[2.0, -2.0], [-1.5, 1.8], [3.2, 3.2]])        # two contextual, one extreme
X = np.vstack([Xn, Xa])
gx, gy = np.meshgrid(np.linspace(-4, 4, 200), np.linspace(-4, 4, 200)); G = np.c_[gx.ravel(), gy.ravel()]
iso = IsolationForest(n_estimators=300, random_state=0).fit(Xn)
lof = LocalOutlierFactor(n_neighbors=30, novelty=True).fit(Xn)
fig, axs = plt.subplots(1, 2, figsize=(11, 4.6), dpi=110, sharey=True)
for ax, sc, title in [(axs[0], -iso.score_samples(G), "Isolation Forest score"), (axs[1], -lof.score_samples(G), "LOF score (30 neighbours)")]:
    cs = ax.contourf(gx, gy, sc.reshape(gx.shape), levels=12, cmap="viridis"); plt.colorbar(cs, ax=ax, shrink=.85)
    ax.scatter(Xn[:, 0], Xn[:, 1], s=5, color="white", alpha=.7); ax.scatter(Xa[:, 0], Xa[:, 1], s=70, color=RED, marker="X", edgecolor="white", label="anomalies")
    ax.set_title(title); ax.set_xlabel("feature 1")
axs[0].set_ylabel("feature 2"); axs[0].legend(frameon=False, loc="upper left")
fig.tight_layout(); fig.savefig("ch14_iso_lof.png"); plt.close(fig)
