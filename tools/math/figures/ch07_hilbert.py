import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.linalg import hilbert
B, O = "#2b4fd6", "#b84a22"
plt.rcParams.update({"font.size": 11})
ns = list(range(2, 14)); conds = []; errs = []
for n in ns:
    H = hilbert(n); xt = np.ones(n); xs = np.linalg.solve(H, H @ xt)
    conds.append(np.linalg.cond(H)); errs.append(np.linalg.norm(xs - xt) / np.linalg.norm(xt))
fig, a = plt.subplots(figsize=(8, 4.2))
a.semilogy(ns, conds, "o-", color=B, lw=2, label="condition number of H")
a.semilogy(ns, np.maximum(errs, 1e-17), "s-", color=O, lw=2, label="relative error of solve")
a.axhline(1e16, color="#888", ls=":"); a.text(2.1, 2e16, "1 / machine epsilon", color="#555", fontsize=9)
a.set_xlabel("size n of the Hilbert matrix"); a.set_ylabel("value (log scale)"); a.set_title("Error grows with the condition number")
a.legend(loc="center left"); a.grid(alpha=.25, which="both")
fig.tight_layout(); fig.savefig("ch07_hilbert.png", dpi=110)
