import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
n = np.arange(1, 201)
H = np.cumsum(1 / n)
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.step(n, H, where="post", color="#2b4fd6", label="H(n) = 1 + 1/2 + ... + 1/n")
ax.plot(n, np.log(n) + 0.5772156649, color="#b84a22", ls="--", label="ln n + 0.5772")
ax.plot(n, np.log(n), color="#357a70", ls=":", label="ln n")
ax.set_xlabel("n"); ax.set_ylabel("value"); ax.set_title("The harmonic series grows like ln n", fontsize=11)
ax.legend(); ax.grid(alpha=.3)
plt.tight_layout(); plt.savefig("ch04_harmonic.png", dpi=110)
