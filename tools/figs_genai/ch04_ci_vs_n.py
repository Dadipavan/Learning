import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"

n = np.arange(5, 801)
fig, ax = plt.subplots(figsize=(8, 4.2))
for p, c in [(0.9, B), (0.7, O), (0.5, T)]:
    ax.plot(n, 100 * 1.96 * np.sqrt(p * (1 - p) / n), color=c, lw=2, label=f"true accuracy {p}")
for k in [6, 50, 100, 400]:
    y = 100 * 1.96 * np.sqrt(0.7 * 0.3 / k)
    ax.scatter([k], [y], color=R, zorder=5); ax.text(k + 8, y + 1.5, f"n={k}: +/-{y:.0f}", fontsize=8, color=R)
ax.set_ylim(0, 45); ax.set_xlabel("number of eval cases (n)"); ax.set_ylabel("95% margin of error (points)")
ax.set_title("An eval set of 6 cannot tell prompts apart")
ax.legend(frameon=False); ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig("ch04d_ci_vs_n.png", dpi=110)
