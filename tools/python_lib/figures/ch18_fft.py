import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

from scipy import fft
rng = np.random.default_rng(2)
fs = 200
t = np.arange(0, 2, 1 / fs)
x = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 30 * t) + rng.normal(0, 0.3, t.size)
X = np.abs(fft.rfft(x)) * 2 / t.size
f = fft.rfftfreq(t.size, 1 / fs)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8, 4.2), dpi=110)
a1.plot(t, x, color=B, lw=1.3); a1.set_xlabel("time (s)"); a1.set_ylabel("signal"); a1.set_title("Time domain")
a2.plot(f, X, color=O, lw=1.8); a2.set_xlim(0, 60); a2.set_xlabel("frequency (Hz)"); a2.set_ylabel("amplitude"); a2.set_title("Frequency domain")
for fr in (5, 30): a2.annotate(f"{fr} Hz", (fr, X[np.argmin(abs(f - fr))]), xytext=(fr + 4, X[np.argmin(abs(f - fr))]), fontsize=12)
fig.tight_layout(); fig.savefig("lib18_fft.png")
