import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
def make_image(n=64):
    y, x = np.mgrid[0:n, 0:n] / (n - 1)
    img = 0.5 * x + 0.3 * y
    img += 0.4 * (((x - 0.65)**2 + (y - 0.4)**2) < 0.04)
    img += 0.25 * (np.sin(8 * np.pi * x) > 0) * (y > 0.7)
    img += 0.2 * ((x > 0.1) & (x < 0.3) & (y > 0.1) & (y < 0.35))
    img = img + 0.02 * np.random.default_rng(0).normal(size=(n, n))  # sensor noise
    return img
img = make_image()
U, s, Vt = np.linalg.svd(img, full_matrices=False)
fig, axs = plt.subplots(1, 3, figsize=(11, 3.4))
axs[0].plot(range(1, 31), s[:30], "o-", color="#2b4fd6", ms=4)
axs[0].set_yscale("log"); axs[0].set_title("Scree plot (log scale)"); axs[0].set_xlabel("component k"); axs[0].set_ylabel("singular value")
cum = np.cumsum(s**2) / np.sum(s**2)
axs[1].plot(range(1, 31), cum[:30], "o-", color="#357a70", ms=4)
axs[1].axhline(0.99, color="#aa2d26", ls="--", lw=1)
axs[1].set_title("Energy kept (s² share)"); axs[1].set_xlabel("rank k"); axs[1].set_ylim(0.5, 1.01)
ks = np.arange(1, 41)
err = [np.linalg.norm(img - (U[:, :k]*s[:k]) @ Vt[:k]) / np.linalg.norm(img) for k in ks]
ratio = [64*64 / (k*(64+64+1)) for k in ks]
axs[2].plot(ks, err, color="#b84a22", lw=2, label="relative error")
axs[2].set_xlabel("rank k"); axs[2].set_ylabel("relative error", color="#b84a22"); axs[2].set_yscale("log")
ax2 = axs[2].twinx(); ax2.plot(ks, ratio, color="#6a2fd0", lw=2, label="compression ratio"); ax2.set_ylabel("compression ratio", color="#6a2fd0"); ax2.set_ylim(0, 35)
axs[2].set_title("Error versus compression")
fig.tight_layout(); fig.savefig("ch09_scree.png", dpi=110)
