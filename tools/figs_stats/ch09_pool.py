import io, contextlib, os, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
B, O, T = "#2b4fd6", "#b84a22", "#357a70"
g = {}
with contextlib.redirect_stdout(io.StringIO()): exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "snip/ch09_pool.py")).read(), g)
n, raw, partial, pooled, true_p = g["n"], g["raw"], g["partial"], g["pooled"], g["true_p"]
fig, ax = plt.subplots(figsize=(9, 4.6))
for i in range(8):
    ax.plot([0, 1], [raw[i], partial[i]], color="#bbb", lw=1)
ax.scatter(np.zeros(8), raw, s=20 + n / 6, color=B, label="no pooling (dot size = store traffic)", zorder=3)
ax.scatter(np.ones(8), partial, s=20 + n / 6, color=O, label="partial pooling", zorder=3)
ax.axhline(pooled, color=T, ls="--", label=f"complete pooling ({pooled:.3f})")
ax.scatter(np.full(8, 1.12), true_p, marker="x", color="k", label="true rate", zorder=3)
ax.set_xticks([0, 1, 1.12]); ax.set_xticklabels(["raw rate", "partial pooling", "truth"]); ax.set_xlim(-0.2, 1.3)
ax.set_ylabel("conversion rate"); ax.set_title("Small stores are pulled toward the group rate; big stores barely move")
ax.legend(frameon=False, fontsize=9, loc="upper left", bbox_to_anchor=(1.0, 1.0))
plt.tight_layout(); plt.savefig("ch09_pool.png", dpi=110)
