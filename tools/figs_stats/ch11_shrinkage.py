import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
exec(open("/Users/c2487352/Personal/Career/final/tools/figs_stats/snip/ch11_slopes.py").read().replace("print(", "(lambda *a, **k: None)("))
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, Rd, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
fig, ax = plt.subplots(1, 2, figsize=(9.5, 4.4))
xs = np.array([0, 10])
for g in range(G):
    ax[0].plot(xs, [200 + true_a[g], 200 + true_a[g] + 10 * (8 + true_b[g])], color="#bbbbbb", lw=.8) if False else None
order = np.argsort(raw)
ax[0].scatter(np.zeros(G), raw, color=O, s=28, label="separate line per depot", zorder=3)
ax[0].scatter(np.ones(G), pooled, color=B, s=28, label="partially pooled", zorder=3)
for g in range(G): ax[0].plot([0, 1], [raw[g], pooled[g]], color="#999999", lw=.8)
ax[0].axhline(b1, color="k", ls="--", lw=1); ax[0].text(1.03, b1, "overall slope", va="center", fontsize=9)
ax[0].set_xticks([0, 1]); ax[0].set_xticklabels(["no pooling", "partial pooling"]); ax[0].set_xlim(-.2, 1.5)
ax[0].set_ylabel("estimated slope (minutes per unit of volume)"); ax[0].set_title("Slopes are pulled toward the centre")
ax[1].scatter(true_slopes, raw, color=O, s=28, label="separate lines"); ax[1].scatter(true_slopes, pooled, color=B, s=28, label="partial pooling")
lo, hi = true_slopes.min() - 1, true_slopes.max() + 1
ax[1].plot([lo, hi], [lo, hi], "k--", lw=1); ax[1].set_xlabel("true slope"); ax[1].set_ylabel("estimate"); ax[1].set_title("Closer to the truth on average")
ax[1].legend(frameon=False, fontsize=9)
plt.tight_layout(); plt.savefig("ch11_shrinkage.png", dpi=110)
