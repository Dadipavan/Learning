import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
rng = np.random.default_rng(3)
fig, axs = plt.subplots(1, 2, figsize=(8, 4.2))
ax = axs[0]
att = np.arange(1, 9)
nocap = 1 * 2.0 ** (att - 1)
cap = np.minimum(nocap, 30)
ax.plot(att, nocap, color="#aa2d26", lw=2, marker="o", label="no cap")
ax.plot(att, cap, color="#2b4fd6", lw=2, marker="s", label="cap 30 s")
ax.plot(att, cap * 0.75, color="#357a70", lw=2, ls="--", label="cap + jitter (mean)")
ax.set_xlabel("retry number"); ax.set_ylabel("wait before retry (s)")
ax.set_title("Backoff schedules (base 1 s)", fontsize=10); ax.legend(frameon=False, fontsize=8)
ax = axs[1]
n = 300
fail_at = 0.0
no_j = np.full(n, 1.0) + rng.normal(0, 0.005, n)
full_j = rng.uniform(0, 1.0, n) * 2.0
bins = np.linspace(0, 2.2, 45)
ax.hist(no_j, bins=bins, color="#aa2d26", alpha=0.85, label="no jitter (all wait 1 s)")
ax.hist(full_j, bins=bins, color="#357a70", alpha=0.75, label="full jitter, uniform(0, 2 s)")
ax.set_xlabel("time of the retry after the outage (s)"); ax.set_ylabel("retries arriving in the window")
ax.set_title("300 clients retrying together", fontsize=10); ax.legend(frameon=False, fontsize=7.5, loc="upper left")
for a in axs: a.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig("ch05d_backoff.png", dpi=110)
print(np.histogram(no_j, bins=bins)[0].max(), np.histogram(full_j, bins=bins)[0].max())
