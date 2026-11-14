import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")
def box(x, y, w, h, t, c, fs=12):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc="white", ec=c, lw=2.5))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs)
def arr(a, b): ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="->", lw=2))
box(0.2, 2.4, 2.6, 1.2, "log.info(...)\nlog.error(...)", B)
box(3.6, 2.4, 2.6, 1.2, "Logger 'etl'\nlevel DEBUG", O)
box(7.2, 4.0, 2.4, 1.1, "Handler: console\nlevel WARNING", T)
box(7.2, 0.9, 2.4, 1.1, "Handler: file\nlevel DEBUG", P)
box(10.0, 4.0, 1.9, 1.1, "Formatter\ntime level msg", R, 11)
box(10.0, 0.9, 1.9, 1.1, "Formatter\nJSON line", R, 11)
arr((2.85, 3.0), (3.55, 3.0)); arr((6.25, 3.2), (7.15, 4.4)); arr((6.25, 2.8), (7.15, 1.6))
arr((9.65, 4.55), (9.95, 4.55)); arr((9.65, 1.45), (9.95, 1.45))
ax.text(6.0, 5.5, "A record passes the logger level, then each handler level", ha="center", fontsize=13)
fig.tight_layout(); fig.savefig("lib23_logging_flow.png")
