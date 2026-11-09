import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

f = lambda x: x**2
x = np.linspace(-4, 4, 300)
fig, ax = plt.subplots(2, 2, figsize=(8, 5.6), sharex=True, sharey=True)
cases = [("shift right 2: f(x − 2)", lambda x: f(x - 2), "#2b4fd6"),
         ("shift up 3: f(x) + 3", lambda x: f(x) + 3, "#357a70"),
         ("stretch: 2·f(x) and f(2x)", None, "#b84a22"),
         ("reflect: −f(x)", lambda x: -f(x), "#aa2d26")]
for a, (t, g, c) in zip(ax.ravel(), cases):
    a.plot(x, f(x), color="grey", lw=1.5, ls="--", label="f(x) = x²")
    if g is None:
        a.plot(x, 2 * f(x), color="#b84a22", lw=2, label="2·f(x)")
        a.plot(x, f(2 * x), color="#6a2fd0", lw=2, label="f(2x)")
    else:
        a.plot(x, g(x), color=c, lw=2, label="new graph")
    a.set_title(t, fontsize=10); a.set_ylim(-8, 12); a.legend(fontsize=8, loc="upper center")
    a.axhline(0, color="k", lw=0.5); a.axvline(0, color="k", lw=0.5)
plt.tight_layout(); plt.savefig("ch02_transforms.png", dpi=110)
