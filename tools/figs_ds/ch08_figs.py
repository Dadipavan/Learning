import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *
import numpy as np
from matplotlib.patches import FancyArrowPatch
# --- DAG patterns
fig, axes = plt.subplots(1, 3, figsize=(10, 3.6))
def node(ax, xy, label, color=BLUE):
    ax.text(xy[0], xy[1], label, ha="center", va="center", fontsize=11, color="white", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", fc=color, ec="none"))
def arrow(ax, a, b, color="#333"):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=16, color=color, lw=1.8, shrinkA=22, shrinkB=22))
specs = [("Confounder: adjust", "Engagement", ORANGE, "up", "ok"),
         ("Mediator: do not adjust (total effect)", "App opens", TEAL, "mid", "ok"),
         ("Collider: do not adjust", "Complaint", RED, "down", "no")]
for ax, (title, mid, col, pos, _) in zip(axes, specs):
    ax.set_xlim(0, 4); ax.set_ylim(0, 3); ax.axis("off"); ax.set_title(title, fontsize=10.5)
    T, Y = (0.5, 0.8), (3.5, 0.8)
    if pos == "up":
        M = (2, 2.4); node(ax, M, mid, col); node(ax, T, "Offer"); node(ax, Y, "Orders")
        arrow(ax, M, T); arrow(ax, M, Y); arrow(ax, T, Y)
    elif pos == "mid":
        M = (2, 2.4); node(ax, M, mid, col); node(ax, T, "Offer"); node(ax, Y, "Orders")
        arrow(ax, T, M); arrow(ax, M, Y); arrow(ax, T, Y)
    else:
        M = (2, 0.6); node(ax, M, mid, col); node(ax, (0.5, 2.2), "Offer"); node(ax, (3.5, 2.2), "Late order")
        arrow(ax, (0.5, 2.2), M); arrow(ax, (3.5, 2.2), M)
save("ds_ch08_dag_patterns.png")
# --- CausalImpact style
rng = np.random.default_rng(5)
T, T0 = 100, 70
common = np.cumsum(rng.normal(0, 1, T)) + 0.05*np.arange(T)
c1 = common + rng.normal(0, 0.8, T) + 10
c2 = 0.8*common + rng.normal(0, 0.8, T) + 20
c3 = 1.2*common + rng.normal(0, 0.8, T) + 5
treated = 1.0*common + rng.normal(0, 0.8, T) + 15
treated[T0:] += 3.0
C = np.c_[np.ones(T), c1, c2, c3]
beta = np.linalg.lstsq(C[:T0], treated[:T0], rcond=None)[0]
sd = (treated[:T0] - C[:T0] @ beta).std(ddof=4)
cf = C @ beta
fig, ax = plt.subplots(figsize=(8, 4.2))
d = np.arange(T)
ax.plot(d, treated, color=BLUE, lw=2, label="observed (treated region)")
ax.plot(d[T0:], cf[T0:], color=ORANGE, lw=2, ls="--", label="counterfactual from control regions")
ax.fill_between(d[T0:], cf[T0:] - 1.96*sd, cf[T0:] + 1.96*sd, color=ORANGE, alpha=0.2)
ax.axvline(T0, color=GREY, ls=":"); ax.text(T0 + 1, treated.min(), "launch", color=GREY)
ax.set_xlabel("day"); ax.set_ylabel("daily orders (index)"); ax.set_title("Counterfactual from control series: the gap after launch is the effect")
ax.legend(loc="upper left", fontsize=9); save("ds_ch08_counterfactual.png")
# --- TWFE bias
fig, ax = plt.subplots(figsize=(6.5, 3.8))
vals = [1.667, 0.883, 1.703]; labs = ["truth", "two-way fixed\neffects", "cohort-by-cohort\nvs never treated"]
bars = ax.bar(labs, vals, color=[GREY, RED, TEAL])
for b, v in zip(bars, vals): ax.text(b.get_x() + b.get_width()/2, v + 0.03, f"{v:.2f}", ha="center")
ax.set_ylabel("average effect on treated cells"); ax.set_title("Staggered rollout with changing effects"); ax.grid(axis="x", alpha=0)
save("ds_ch08_twfe_bias.png")
