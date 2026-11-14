import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
fig, ax = plt.subplots(figsize=(8, 4.2))
cols = {"base image": [1000, 130], "compilers + build cache": [450, 0], "libraries": [600, 600], "code + model": [120, 120]}
colors = [B, R, T, O]
left = [0, 0]
labels = ["single stage", "multi stage + slim"]
for (name, vals), c in zip(cols.items(), colors):
    ax.barh(labels, vals, left=left, color=c, label=name, height=.5)
    left = [l + v for l, v in zip(left, vals)]
ax.text(left[0] + 30, 0, "2170 MB, 43 s to pull", va="center", fontsize=10)
ax.text(left[1] + 30, 1, "850 MB, 17 s to pull", va="center", fontsize=10)
ax.set_xlim(0, 3300); ax.set_xlabel("Image size (MB, illustrative; pull at 50 MB/s)")
ax.set_title("Multi-stage build on a slim base removes about 61% of the image")
ax.legend(loc="center right", fontsize=8.5); ax.grid(alpha=.25, axis="x")
fig.tight_layout(); fig.savefig("ch02d_image_size.png", dpi=110)
