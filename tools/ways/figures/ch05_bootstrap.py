import sys, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
DATA = "/Users/c2487352/Personal/Career/final/study/ways/data/"
sys.path.insert(0, DATA); import prep
o, c, p = prep.load_clean(DATA)
rng = np.random.default_rng(7)
r = o.dropna(subset=["late"])
a = r[r.channel == "App"].late.values; w = r[r.channel == "Web"].late.values
diffs = np.array([rng.choice(w, len(w)).mean() - rng.choice(a, len(a)).mean() for _ in range(4000)])
lo, hi = np.percentile(diffs, [2.5, 97.5])
fig, ax = plt.subplots(figsize=(7.5, 3.8))
ax.hist(diffs * 100, bins=45, color="#2b4fd6", edgecolor="white")
ax.axvline(lo * 100, color="#b84a22"); ax.axvline(hi * 100, color="#b84a22"); ax.axvline(0, color="black", ls="--")
ax.set_xlabel("Web late rate minus App late rate (percentage points)"); ax.set_ylabel("bootstrap samples")
ax.set_title("Bootstrap distribution of the difference (95% interval in orange)")
ax.spines[["top", "right"]].set_visible(False); fig.tight_layout(); fig.savefig("ch05_bootstrap.png", dpi=110)
