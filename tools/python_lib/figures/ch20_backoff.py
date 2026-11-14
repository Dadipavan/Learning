import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

rng = np.random.default_rng(3)
attempt = np.arange(1, 8)
base, cap = 0.5, 20.0
plain = np.minimum(cap, base * 2.0 ** (attempt - 1))
jit = rng.uniform(0, plain)
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ax.plot(attempt, plain, "-o", color=B, lw=2.5, label="exponential: 0.5 * 2^(n-1), capped at 20 s")
ax.plot(attempt, np.full(7, base), "-s", color=R, lw=2.5, label="fixed delay of 0.5 s (hammers the server)")
ax.scatter(attempt, jit, color=O, s=90, zorder=3, label="full jitter: random in [0, delay]")
ax.set_xlabel("retry number"); ax.set_ylabel("seconds to wait")
ax.set_title("Backoff schedules"); ax.legend(fontsize=10, loc="upper left")
fig.tight_layout(); fig.savefig("lib20_backoff.png")
