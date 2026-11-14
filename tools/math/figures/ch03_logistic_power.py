import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 11})
t = np.linspace(0, 20, 300)
K, r, t0 = 10000, 0.6, 10
logi = K / (1 + np.exp(-r * (t - t0)))
expo = K / (1 + np.exp(r * t0)) * np.exp(r * t)
fig, ax = plt.subplots(1, 2, figsize=(8.6, 4.2))
ax[0].plot(t, logi, color="#2b4fd6", lw=2.4, label="logistic (S-curve)")
ax[0].plot(t, expo, color="#b84a22", lw=2.2, ls="--", label="pure exponential")
ax[0].set_ylim(0, 12000); ax[0].axhline(K, color="gray", lw=.8, ls=":")
ax[0].set_xlabel("time"); ax[0].set_ylabel("adopters"); ax[0].legend(fontsize=9); ax[0].grid(alpha=.3)
ax[0].set_title("Same start, different ending")
x = np.logspace(0, 3, 200)
ax[1].loglog(x, x ** -2.0, color="#357a70", lw=2.4, label="power law x$^{-2}$")
ax[1].loglog(x, np.exp(-x / 20), color="#aa2d26", lw=2.4, label="exponential e$^{-x/20}$")
ax[1].set_ylim(1e-12, 2); ax[1].set_xlabel("x (log)"); ax[1].set_ylabel("tail (log)")
ax[1].legend(fontsize=9); ax[1].grid(alpha=.3, which="both"); ax[1].set_title("Log-log: power law is a straight line")
plt.tight_layout(); plt.savefig("ch03_logistic_power.png", dpi=110)
