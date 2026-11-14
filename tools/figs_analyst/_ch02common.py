import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
BLUE, ORANGE, TEAL, RED, PURPLE = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
LIGHT = {BLUE: "#dfe5fa", ORANGE: "#f6e1d8", TEAL: "#d9ebe7", RED: "#f3d9d7", PURPLE: "#e6dcf8"}
ROWS = [(1001,"2025-01-03","Pune","Fashion",2,499,"Delivered"),
        (1002,"2025-01-03","Mumbai","Electronics",1,1299,"Delivered"),
        (1003,"2025-01-04","Pune","Grocery",3,199,"Returned"),
        (1004,"2025-01-05","Delhi","Fashion",1,799,"Delivered"),
        (1005,"2025-01-06","Mumbai","Grocery",5,90,"Cancelled"),
        (1006,"2025-01-07","Mumbai","Fashion",2,649,"Delivered"),
        (1007,"2025-01-09","Delhi","Electronics",1,2499,"Delivered"),
        (1008,"2025-01-10","Pune","Fashion",4,350,"Delivered")]
def newfig():
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
    return fig, ax
def clean(ax):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=10)
def box(ax, x, y, w, h, text, color=BLUE, fs=10, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                 fc=LIGHT[color], ec=color, lw=1.6))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", color="#1b1b1b")
def arrow(ax, x1, y1, x2, y2, color="#444", style="-|>"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=1.6))
