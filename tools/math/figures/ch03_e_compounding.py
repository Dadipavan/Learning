import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 11})
n = np.arange(1, 61)
v = (1 + 1 / n) ** n
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(n, v, "o-", color="#2b4fd6", ms=4, label="(1 + 1/n)$^n$")
ax.axhline(np.e, color="#aa2d26", ls="--", label="e = 2.71828...")
ax.set_xlabel("compounding periods per year, n"); ax.set_ylabel("value of 1 after one year")
ax.set_title("Compounding more often converges to e"); ax.legend(); ax.grid(alpha=.3)
plt.tight_layout(); plt.savefig("ch03_e_compounding.png", dpi=110)
