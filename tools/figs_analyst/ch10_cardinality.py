import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
rng = np.random.default_rng(1); n = 1_000_000
seconds = rng.integers(0, 365 * 24 * 3600, n)
cols = {"timestamp\nto the second": seconds, "date only": seconds // 86400, "hour of day": (seconds // 3600) % 24, "city\n(50 values)": rng.integers(0, 50, n)}
names, sizes = [], []
for k, c in cols.items():
    d = len(np.unique(c)); bits = int(np.ceil(np.log2(d))); names.append(k); sizes.append((n * bits / 8 + d * 8) / 1e6)
fig, ax = plt.subplots(figsize=(8, 3.8), dpi=110)
bars = ax.bar(names, sizes, color=["#aa2d26", "#357a70", "#2b4fd6", "#6a2fd0"])
ax.set_yscale("log"); ax.set_ylabel("approx. size (MB, log scale)", fontsize=11)
for b, v in zip(bars, sizes): ax.text(b.get_x() + b.get_width()/2, v * 1.15, f"{v:.2f} MB", ha="center", fontsize=11)
ax.set_ylim(0.05, 20); ax.tick_params(labelsize=10)
for s in ("top", "right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig("ch10_cardinality.png")
