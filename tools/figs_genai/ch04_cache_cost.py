import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"

req = np.linspace(0, 100000, 101)
pin, pout, cached = 1.0, 4.0, 0.10
prefix, var, out = 3000, 200, 100
no = req * ((prefix + var) * pin + out * pout) / 1e6
yes = req * (prefix * pin * cached + var * pin + out * pout) / 1e6
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(req / 1000, no, color=O, lw=2, label="no caching")
ax.plot(req / 1000, yes, color=T, lw=2, label="3,000-token prefix cached at 10% price")
ax.fill_between(req / 1000, yes, no, color=T, alpha=0.12)
ax.text(55, (no[55] + yes[55]) / 2 + 0.2, f"saving at 100k/day: {no[-1]-yes[-1]:.1f} units", fontsize=9, color=T)
ax.set_xlabel("requests per day (thousands)"); ax.set_ylabel("cost per day (made-up currency units)")
ax.set_title("Stable prefix first: caching cuts the bill (hypothetical prices 1.00 / 4.00)")
ax.legend(frameon=False); ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig("ch04d_cache_cost.png", dpi=110)
