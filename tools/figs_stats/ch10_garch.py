import io, contextlib, os, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
g = {}
with contextlib.redirect_stdout(io.StringIO()): exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "snip/ch10_garch.py")).read(), g)
r, v, acf = g["r"], g["v"], g["acf"]
fig = plt.figure(figsize=(10.5, 4.4)); gs = fig.add_gridspec(1, 3, width_ratios=[2.2, 1, 1])
a = fig.add_subplot(gs[0]); a.plot(r[:500], color="#999", lw=.7, label="daily return")
a.plot(2 * np.sqrt(v[:500]), color="#b84a22", lw=1.5, label="+/- 2 x GARCH volatility"); a.plot(-2 * np.sqrt(v[:500]), color="#b84a22", lw=1.5)
a.set_xlabel("day"); a.set_title("Volatility comes in clusters"); a.legend(frameon=False, fontsize=8, loc="upper right")
for k, (x, ttl) in enumerate([(r, "ACF of returns"), (r ** 2, "ACF of squared returns")]):
    b = fig.add_subplot(gs[k + 1]); b.bar(range(1, 21), acf(x, 20), color="#2b4fd6" if k == 0 else "#357a70")
    b.axhline(1.96 / np.sqrt(len(r)), color="#aa2d26", ls="--"); b.axhline(-1.96 / np.sqrt(len(r)), color="#aa2d26", ls="--")
    b.set_title(ttl, fontsize=10); b.set_xlabel("lag"); b.set_ylim(-0.1, 0.35)
plt.tight_layout(); plt.savefig("ch10_garch.png", dpi=110)
