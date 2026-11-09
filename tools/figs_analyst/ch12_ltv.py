import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
arpu, margin = 400, 0.30
months = np.arange(0, 61)
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
for c, col in ((0.05, "#357a70"), (0.08, "#2b4fd6"), (0.12, "#aa2d26")):
    cum = np.cumsum(arpu*margin*(1-c)**months)
    ax.plot(months, cum, color=col, lw=2.2, label=f"monthly churn {int(c*100)}%")
    ax.axhline(arpu*margin/c, color=col, lw=1, ls=":")
    ax.text(61, arpu*margin/c, f" limit {arpu*margin/c:.0f}", color=col, va="center", fontsize=10)
ax.set_xlim(0, 70); ax.set_xlabel("months since signup", fontsize=11); ax.set_ylabel("cumulative margin per customer (Rs)", fontsize=11)
ax.legend(frameon=False, fontsize=10, loc="lower right", bbox_to_anchor=(0.88, 0.12)); ax.tick_params(labelsize=10)
for s in ("top", "right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig("ch12_ltv.png")
