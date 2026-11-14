import io, contextlib, os, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
g = {}
with contextlib.redirect_stdout(io.StringIO()): exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "snip/ch09_rhat.py")).read(), g)
res = g["res"]; cols = ["#2b4fd6", "#b84a22", "#357a70", "#6a2fd0"]
fig, ax = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
for a, (name, ch) in zip(ax, res.items()):
    for c, col in zip(ch, cols): a.plot(c[:1500], color=col, lw=.8)
    a.set_title(name + f": R-hat {g['split_rhat'](ch):.2f}"); a.set_xlabel("iteration")
ax[0].set_ylabel("sampled value")
plt.tight_layout(); plt.savefig("ch09_chains.png", dpi=110)
