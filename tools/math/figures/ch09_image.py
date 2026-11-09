import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
def make_image(n=64):
    y, x = np.mgrid[0:n, 0:n] / (n - 1)
    img = 0.5 * x + 0.3 * y                      # smooth gradient
    img += 0.4 * (((x - 0.65)**2 + (y - 0.4)**2) < 0.04)   # bright disc
    img += 0.25 * (np.sin(8 * np.pi * x) > 0) * (y > 0.7)  # stripes in the bottom band
    img += 0.2 * ((x > 0.1) & (x < 0.3) & (y > 0.1) & (y < 0.35))  # square
    img = img + 0.02 * np.random.default_rng(0).normal(size=(n, n))  # sensor noise
    return img
img = make_image()
U, s, Vt = np.linalg.svd(img, full_matrices=False)
ks = [1, 2, 5, 10, 20]
fig, axs = plt.subplots(1, 6, figsize=(11, 2.4))
axs[0].imshow(img, cmap="gray"); axs[0].set_title("original 64x64", fontsize=8)
for ax, k in zip(axs[1:], ks):
    r = (U[:, :k] * s[:k]) @ Vt[:k]
    ax.imshow(r, cmap="gray", vmin=img.min(), vmax=img.max()); ax.set_title("rank %d" % k, fontsize=8)
for ax in axs: ax.axis("off")
fig.tight_layout()
fig.savefig("ch09_image.png", dpi=110)
