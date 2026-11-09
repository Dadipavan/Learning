import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 11})
t = np.linspace(0, 24, 200)
users = 1000 * 2 ** (t / 3)           # doubles every 3 months
fig, ax = plt.subplots(1, 2, figsize=(8.6, 4.2))
for a, log in zip(ax, [False, True]):
    a.plot(t, users, color="#2b4fd6", lw=2.4, label="users, doubling every 3 months")
    a.plot(t, 1000 + 20000 * t / 24 * 1.0, color="#b84a22", lw=2.4, label="linear: +833 per month")
    a.set_xlabel("months"); a.grid(alpha=.3)
    if log:
        a.set_yscale("log"); a.set_title("Log y-axis: exponential = straight line")
    else:
        a.set_title("Linear y-axis: exponential explodes")
ax[0].set_ylabel("users"); ax[0].legend(fontsize=8, loc="upper left")
plt.tight_layout(); plt.savefig("ch03_growth.png", dpi=110)
