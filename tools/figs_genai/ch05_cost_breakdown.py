import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
pin, pout = 1.0, 4.0
def parts(tin, tout, cached=0.0, retry=0.0):
    i_unc = tin * (1 - cached) * pin
    i_c = tin * cached * pin * 0.1
    o = tout * pout
    base = i_unc + i_c + o
    return [i_unc / 1e6, i_c / 1e6, o / 1e6, base * retry / 1e6]
scen = [("baseline", parts(1500, 300, 0, 0.10)),
        ("prefix cache\n80%", parts(1500, 300, 0.8, 0.10)),
        ("+ output\nlimited to 150", parts(1500, 150, 0.8, 0.10)),
        ("+ fewer retries\n(1%)", parts(1500, 150, 0.8, 0.01))]
labels = ["input (full price)", "input (cached, 10%)", "output", "wasted on retries"]
cols = ["#2b4fd6", "#6a2fd0", "#b84a22", "#aa2d26"]
fig, ax = plt.subplots(figsize=(8, 4.2))
bottom = [0] * len(scen)
for j in range(4):
    vals = [s[1][j] * 1000 for s in scen]
    ax.bar([s[0] for s in scen], vals, bottom=bottom, color=cols[j], label=labels[j])
    bottom = [b + v for b, v in zip(bottom, vals)]
for k, b in enumerate(bottom):
    ax.text(k, b + 0.05, f"{b:.3f}", ha="center", fontsize=9)
ax.set_ylabel("cost per 1,000 requests (units)")
ax.set_title("Where the money goes (made-up prices 1 in / 4 out per million)", fontsize=10)
ax.legend(frameon=False, fontsize=8); ax.spines[["top", "right"]].set_visible(False)
ax.set_ylim(0, max(bottom) * 1.15)
fig.tight_layout(); fig.savefig("ch05d_cost_breakdown.png", dpi=110)
print([round(b, 4) for b in bottom])
