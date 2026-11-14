import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

rate, cap = 2.0, 5.0   # tokens per second, bucket size
dt = 0.1
t = np.arange(0, 10, dt)
rng = np.random.default_rng(1)
tokens = cap; level = []; sent = []; blocked = []
for ti in t:
    tokens = min(cap, tokens + rate * dt)
    burst = (2.0 <= ti < 3.0) or (6.0 <= ti < 6.4)
    want = burst and rng.random() < 0.8
    if want and tokens >= 1:
        tokens -= 1; sent.append(ti)
    elif want:
        blocked.append(ti)
    level.append(tokens)
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ax.plot(t, level, color=B, lw=2.5, label="tokens in bucket")
ax.scatter(sent, np.full(len(sent), -0.4), color=T, s=40, label="request sent")
ax.scatter(blocked, np.full(len(blocked), -0.4), color=R, s=40, marker="x", label="must wait (429 avoided)")
ax.set_xlabel("time (s)"); ax.set_ylabel("tokens"); ax.set_ylim(-0.9, 5.6)
ax.set_title("Token bucket: 2 requests/s refill, burst up to 5")
ax.legend(fontsize=10, loc="lower right")
fig.tight_layout(); fig.savefig("lib20_tokenbucket.png")
