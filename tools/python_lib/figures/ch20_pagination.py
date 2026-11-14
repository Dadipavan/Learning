import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

ids = list(range(100, 0, -1))   # newest first
size = 10
def offset_pages():
    data = ids[:]; out = []
    for p in range(5):
        out.append(data[p * size:(p + 1) * size])
        if p == 1:
            data = [101, 102, 103] + data   # three new rows arrive
    return out
def cursor_pages():
    data = ids[:]; out = []; cur = None
    for p in range(5):
        page = [i for i in data if cur is None or i < cur][:size]
        out.append(page); cur = page[-1]
        if p == 1:
            data = [101, 102, 103] + data
    return out
fig, axes = plt.subplots(1, 2, figsize=(8, 4.2), dpi=110, sharey=True)
for ax, pages, title in zip(axes, [offset_pages(), cursor_pages()], ["offset / page number", "cursor (id below last seen)"]):
    seen = set()
    for k, pg in enumerate(pages):
        for i in pg:
            dup = i in seen; seen.add(i)
            ax.scatter(k + 1, i, color=R if dup else B, s=22, marker="x" if dup else "o")
    ax.set_xlabel("request number"); ax.set_title(title, fontsize=12)
axes[0].set_ylabel("row id returned")
axes[0].text(0.7, 56, "red x = duplicate row", color=R, fontsize=11)
fig.suptitle("New rows arrive after request 2", fontsize=13)
fig.tight_layout(); fig.savefig("lib20_pagination.png")
