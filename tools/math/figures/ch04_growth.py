import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from math import factorial
n = np.arange(1, 26)
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(n, n, label="n", color="#357a70")
ax.plot(n, n * np.log2(n), label="n log n", color="#2b4fd6")
ax.plot(n, n ** 2.0, label="n²", color="#6a2fd0")
ax.plot(n, 2.0 ** n, label="2ⁿ", color="#b84a22")
ax.plot(n, [float(factorial(int(i))) for i in n], label="n!", color="#aa2d26")
ax.set_yscale("log"); ax.set_xlabel("n"); ax.set_ylabel("value (log scale)")
ax.set_title("How fast common counts grow", fontsize=11); ax.legend(); ax.grid(alpha=.3, which="both")
plt.tight_layout(); plt.savefig("ch04_growth.png", dpi=110)
