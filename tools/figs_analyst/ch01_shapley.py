import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import itertools
f0 = {"visitors": 20000, "conversion": 0.0125, "AOV": 400}; f1 = {"visitors": 16000, "conversion": 0.015, "AOV": 450}
rev = lambda s: s["visitors"] * s["conversion"] * s["AOV"]
res = {k: [] for k in f0}
for order in itertools.permutations(f0):
    cur = dict(f0); prev = rev(cur)
    for k in order:
        cur[k] = f1[k]; new = rev(cur); res[k].append(new - prev); prev = new
fig, ax = plt.subplots(figsize=(8, 3.8), dpi=110)
for i, k in enumerate(res):
    v = res[k]; ax.plot([min(v), max(v)], [i, i], color="#bbbbbb", lw=8, solid_capstyle="round")
    ax.scatter(v, [i]*len(v), color="#2b4fd6", s=25, zorder=3)
    ax.scatter([sum(v)/6], [i], color="#b84a22", s=120, marker="D", zorder=4)
    ax.text(max(v) + 1200, i, f"Shapley {sum(v)/6:,.0f}", va="center", fontsize=10)
ax.axvline(0, color="black", lw=1)
ax.set_yticks(range(3)); ax.set_yticklabels(list(res), fontsize=11); ax.set_xlim(-32000, 42000)
ax.set_xlabel("effect on monthly revenue (Rs) depending on the order in which factors are switched", fontsize=10)
ax.tick_params(axis="x", labelsize=10)
for s in ("top", "right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig("ch01_shapley.png")
