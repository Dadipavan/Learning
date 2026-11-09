import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 11})
n = np.arange(1, 31)
fig, ax = plt.subplots(figsize=(8, 4.2))
for y, lab, c in [(np.log2(n), "log n", "#357a70"), (n, "n", "#2b4fd6"), (n * np.log2(n), "n log n", "#6a2fd0"),
                  (n ** 2, "n$^2$", "#b84a22"), (2.0 ** n, "2$^n$", "#aa2d26")]:
    ax.plot(n, y, lw=2.4, label=lab, color=c)
ax.set_yscale("log"); ax.set_xlabel("input size n"); ax.set_ylabel("operations (log scale)")
ax.set_title("Big-O growth rates (log y-axis)"); ax.legend(); ax.grid(alpha=.3, which="both")
plt.tight_layout(); plt.savefig("ch03_bigo.png", dpi=110)
