import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 2, figsize=(10, 4.2))
ax = axs[0]
for ratio, c in [(0.4, "#2b4fd6"), (0.8, "#357a70"), (0.95, "#b84a22")]:
    k = np.arange(0, 60)
    ax.semilogy(k, ratio**k, color=c, lw=2, label=f"|λ2/λ1| = {ratio}")
ax.set_xlabel("iteration k"); ax.set_ylabel("error (relative scale)"); ax.set_title("Power iteration error shrinks like (λ2/λ1)^k"); ax.legend(); ax.grid(alpha=.3)
ax = axs[1]
P = np.array([[0.8, 0.4], [0.2, 0.6]])
x = np.array([1., 0.]); s = [x[0]]
for _ in range(10):
    x = P @ x; s.append(x[0])
ax.plot(range(11), s, "o-", color="#2b4fd6", lw=2, label="P(sunny) from sunny start")
x = np.array([0., 1.]); s = [x[0]]
for _ in range(10):
    x = P @ x; s.append(x[0])
ax.plot(range(11), s, "s-", color="#b84a22", lw=2, label="P(sunny) from rainy start")
ax.axhline(2 / 3, color="k", ls="--", lw=1); ax.text(6.3, 0.69, "steady state 2/3", fontsize=10)
ax.set_xlabel("day"); ax.set_ylabel("probability of sun"); ax.set_title("Markov chain forgets its start"); ax.legend(); ax.grid(alpha=.3)
plt.tight_layout(); plt.savefig("ch08_power_markov.png", dpi=110)
