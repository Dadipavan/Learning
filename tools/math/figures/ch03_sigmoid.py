import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 11})
z = np.linspace(-8, 8, 400)
s = 1 / (1 + np.exp(-z)); th = np.tanh(z)
fig, ax = plt.subplots(1, 2, figsize=(8.6, 4.2))
ax[0].plot(z, s, color="#2b4fd6", lw=2.4, label="sigmoid(z)")
ax[0].plot(z, th, color="#b84a22", lw=2.4, label="tanh(z)")
ax[0].axhline(0, color="gray", lw=.8); ax[0].axhline(.5, color="gray", lw=.8, ls=":")
ax[0].set_xlabel("z"); ax[0].legend(); ax[0].grid(alpha=.3); ax[0].set_title("Squashing functions")
ax[1].plot(z, s * (1 - s), color="#2b4fd6", lw=2.4, label="sigmoid'(z) (max 0.25)")
ax[1].plot(z, 1 - th ** 2, color="#b84a22", lw=2.4, label="tanh'(z) (max 1)")
ax[1].set_xlabel("z"); ax[1].legend(); ax[1].grid(alpha=.3); ax[1].set_title("Slopes vanish in the tails")
plt.tight_layout(); plt.savefig("ch03_sigmoid.png", dpi=110)
