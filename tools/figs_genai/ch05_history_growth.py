import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
SYS, USER, REPLY, N = 200, 50, 150, 20
turns = np.arange(1, N + 1)
full = np.array([SYS + (k - 1) * (USER + REPLY) + USER for k in turns])
win = np.array([SYS + min(k - 1, 4) * (USER + REPLY) + USER for k in turns])
summ = np.array([SYS + (150 if k > 5 else 0) + min(k - 1, 4) * (USER + REPLY) + USER if k > 1 else SYS + USER for k in turns])
fig, axs = plt.subplots(1, 2, figsize=(8, 4.2))
ax = axs[0]
ax.plot(turns, full, color="#aa2d26", lw=2, marker="o", ms=3, label="full history")
ax.plot(turns, summ, color="#357a70", lw=2, marker="s", ms=3, label="last 4 turns + 150-token summary")
ax.plot(turns, win, color="#2b4fd6", lw=2, marker="^", ms=3, label="last 4 turns only")
ax.set_xlabel("turn number"); ax.set_ylabel("input tokens in this call")
ax.set_title("Tokens sent per call", fontsize=10); ax.legend(frameon=False, fontsize=7.5)
ax = axs[1]
tot = [np.cumsum(a)[-1] for a in (full, summ, win)]
bars = ax.bar(["full", "summary", "window"], tot, color=["#aa2d26", "#357a70", "#2b4fd6"])
for b, t in zip(bars, tot):
    ax.text(b.get_x() + b.get_width() / 2, t + 400, f"{t:,}", ha="center", fontsize=9)
ax.set_title("Total input tokens over 20 turns", fontsize=10); ax.set_ylim(0, max(tot) * 1.15)
for a in axs: a.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig("ch05d_history_growth.png", dpi=110)
print(tot)
