import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, axs = plt.subplots(2, 1, figsize=(8, 4.2), gridspec_kw={"height_ratios": [1, 1.2]})
ax = axs[0]; ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 40)
def bar(y, parts):
    x = 0
    for w, c, t in parts:
        ax.barh(y, w, left=x, height=9, color=c, alpha=0.85, ec="white")
        ax.text(x + w / 2, y, t, ha="center", va="center", fontsize=8, color="white")
        x += w
bar(30, [(15, "#357a70", "system"), (25, "#357a70", "tools + examples"), (35, "#357a70", "policy docs"), (25, "#b84a22", "user question")])
ax.text(0, 36, "Good order: stable first, changing last (first 75% reusable)", fontsize=9)
bar(8, [(8, "#b84a22", "time"), (15, "#aa2d26", "system"), (25, "#aa2d26", "tools + examples"), (35, "#aa2d26", "policy docs"), (17, "#b84a22", "question")])
ax.text(0, 14.5, "Bad order: a timestamp on top changes every call (nothing reusable)", fontsize=9)
ax = axs[1]
import numpy as np
f = np.linspace(0, 1, 50)
tin, tout = 3000, 300
def cost(reuse): return (tin * (1 - reuse) + tin * reuse * 0.1 + tout * 4) / 1e6 * 1000
ax.plot(f * 100, [cost(x) for x in f], color="#357a70", lw=2, label="stable prefix first")
ax.axhline(cost(0), color="#aa2d26", lw=2, ls="--", label="timestamp first (0% reused)")
ax.set_xlabel("share of the input that is a stable prefix (%)"); ax.set_ylabel("cost per 1,000 calls")
ax.legend(frameon=False, fontsize=8); ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig("ch05d_prefix_cache.png", dpi=110)
