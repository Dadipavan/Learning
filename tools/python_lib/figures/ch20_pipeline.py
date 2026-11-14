import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
def box(x, y, w, h, txt, c):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc=c, ec="none", alpha=0.95))
    ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", color="white", fontsize=11, fontweight="bold")
srcs = [("Files\ncsv json yaml xlsx", B), ("Database\nsqlite3 SQLAlchemy", B), ("Web API\nrequests httpx", B), ("HTML pages\nBeautifulSoup", B)]
for i, (t, c) in enumerate(srcs):
    box(0.1, 4.6 - i * 1.4, 2.6, 1.0, t, c)
    ax.annotate("", xy=(3.8, 3.0), xytext=(2.8, 5.1 - i * 1.4), arrowprops=dict(arrowstyle="->", color="#555", lw=1.5))
box(3.8, 2.2, 2.4, 1.6, "Validate\nand clean\n(dataclass, pydantic)", O)
box(7.2, 4.0, 2.6, 1.0, "DataFrame\n(pandas)", T)
box(7.2, 2.5, 2.6, 1.0, "Parquet / Arrow\n(columnar files)", P)
box(7.2, 1.0, 2.6, 1.0, "SQLite / SQL\nwarehouse", R)
for y in (4.5, 3.0, 1.5):
    ax.annotate("", xy=(7.1, y), xytext=(6.3, 3.0), arrowprops=dict(arrowstyle="->", color="#555", lw=1.5))
ax.text(5, 0.3, "log every step; chunk what does not fit in memory", ha="center", fontsize=11, style="italic")
ax.set_title("Data in, checked, then data out")
fig.tight_layout(); fig.savefig("lib20_pipeline.png"); 
