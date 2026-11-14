import matplotlib
matplotlib.use("Agg")
import numpy as np, matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 11})
# x^2 + b x + 1 = 0, small root exactly ~ -1/b for large b. Use exact via stable formula in long double.
b = 10.0 ** np.arange(1, 9, 0.25)
d = np.sqrt(b * b - 4.0)
naive = (-b + d) / 2
stable = (-2.0) / (b + d)
from decimal import Decimal, getcontext
getcontext().prec = 60
exact = np.array([float(Decimal(-2) / (Decimal(float(v)) + (Decimal(float(v)) ** 2 - 4).sqrt())) for v in b])
rn = np.abs((naive - exact) / exact).astype(float)
rs = np.abs((stable - exact) / exact).astype(float)
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.loglog(b, np.maximum(rn, 1e-17), color="#aa2d26", lw=2, label="naive (-b + sqrt(D)) / 2")
ax.loglog(b, np.maximum(rs, 1e-17), color="#357a70", lw=2, label="stable -2 / (b + sqrt(D))")
ax.set_xlabel("b (size of the big coefficient)"); ax.set_ylabel("relative error of the small root")
ax.set_title("Cancellation destroys digits in the textbook formula"); ax.legend(); ax.grid(alpha=.3, which="both")
plt.tight_layout(); plt.savefig("ch01_stability.png", dpi=110)
