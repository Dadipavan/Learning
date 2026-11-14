import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, pandas as pd
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
def clean(ax):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=10)
# 1. bootstrap, mean vs median
rng = np.random.default_rng(7)
a = rng.lognormal(5.0, 1.0, 300).round(0); b = rng.lognormal(5.15, 1.0, 300).round(0)
def boot(x, stat, n=5000, seed=1):
    r = np.random.default_rng(seed); idx = r.integers(0, len(x), (n, len(x))); return stat(x[idx], axis=1)
dm = boot(b, np.mean) - boot(a, np.mean); dd = boot(b, np.median) - boot(a, np.median)
fig, axs = plt.subplots(1, 2, figsize=(8, 3.8), dpi=110, sharey=True)
for ax, d, nm, c in ((axs[0], dm, "difference in means", B), (axs[1], dd, "difference in medians", O)):
    ax.hist(d, bins=40, color=c, alpha=0.85)
    lo, hi = np.percentile(d, [2.5, 97.5])
    ax.axvline(lo, color="black", lw=1.5, ls="--"); ax.axvline(hi, color="black", lw=1.5, ls="--")
    ax.axvline(0, color=R, lw=2)
    ax.set_title(f"{nm}\n95% interval {lo:.1f} to {hi:.1f}", fontsize=11); ax.set_xlabel("bootstrap difference (B minus A), Rs", fontsize=10); clean(ax)
axs[0].set_ylabel("count of resamples", fontsize=10)
fig.tight_layout(); fig.savefig("ch13_bootstrap.png")
# 2. BH
p = np.array([0.001, 0.008, 0.012, 0.030, 0.041, 0.049, 0.20, 0.45, 0.62, 0.90]); m = len(p); k = np.arange(1, m + 1)
fig, ax = plt.subplots(figsize=(8, 4.0), dpi=110)
ax.plot(k, p, "o", color=B, ms=8, label="sorted p-values")
ax.plot(k, 0.05 * k / m, color=T, lw=2, label="Benjamini-Hochberg line  0.05 k / m")
ax.axhline(0.05 / m, color=R, lw=2, ls="--", label="Bonferroni line  0.05 / m")
ax.axhline(0.05, color="grey", lw=1, ls=":", label="no correction  0.05")
ax.set_ylim(0, 0.1); ax.set_xlabel("rank k of the p-value (smallest first)", fontsize=11); ax.set_ylabel("p-value", fontsize=11)
ax.legend(frameon=False, fontsize=9, loc="upper left"); clean(ax)
fig.tight_layout(); fig.savefig("ch13_bh.png")
# 3. DiD
rng = np.random.default_rng(25); rows = []
for s in range(40):
    t = int(s < 20); base = 100 + 10 * t + rng.normal(0, 6)
    for mth in range(12):
        post = int(mth >= 6); rows.append((s, mth, t, post, base + 1.5 * mth + 12 * t * post + rng.normal(0, 4)))
df = pd.DataFrame(rows, columns=["store", "month", "treated", "post", "sales"])
mm = df.groupby(["month", "treated"])["sales"].mean().unstack()
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ax.plot(mm.index, mm[1], "-o", color=O, lw=2, label="treated stores")
ax.plot(mm.index, mm[0], "-o", color=B, lw=2, label="control stores")
cf = mm[1].iloc[5] + (mm[0].loc[5:] - mm[0].loc[5])
ax.plot(cf.index, cf.values, "--", color=O, lw=1.8, label="treated if no programme (counterfactual)")
ax.axvline(5.5, color="grey", lw=1)
ax.text(5.6, mm.values.min() + 1, "programme starts", fontsize=9)
ax.set_xlabel("month (0 to 11)", fontsize=11); ax.set_ylabel("average sales per store", fontsize=11)
ax.legend(frameon=False, fontsize=9, loc="upper left"); clean(ax)
fig.tight_layout(); fig.savefig("ch13_did.png")
