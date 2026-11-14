import matplotlib
matplotlib.use("Agg")
import numpy as np
rng = np.random.default_rng(8)
amt = np.round(rng.lognormal(6.8, 0.8, 300))
q1, q3 = np.percentile(amt, [25, 75])
iqr = q3 - q1
n = len(amt)
fd_width = 2 * iqr / n ** (1 / 3)
print(f"n={n}  Q1={q1:.0f}  Q3={q3:.0f}  IQR={iqr:.0f}")
print(f"Freedman-Diaconis width = 2 x {iqr:.0f} / {n}^(1/3) = {fd_width:.0f}")
print("Sturges bins:", int(np.ceil(np.log2(n) + 1)))
print("numpy 'fd' bins:", len(np.histogram_bin_edges(amt, bins="fd")) - 1,
      "| numpy 'sturges' bins:", len(np.histogram_bin_edges(amt, bins="sturges")) - 1)
