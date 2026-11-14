import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
B, O, T, R = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26"
def clean(ax):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=10)
ad = np.array([10, 20, 30, 40, 50, 60.]); sales = np.array([120, 150, 160, 190, 210, 215.])
n = 6; xm = ad.mean(); sxx = ((ad - xm) ** 2).sum()
b1 = ((ad - xm) * (sales - sales.mean())).sum() / sxx; b0 = sales.mean() - b1 * xm
res = sales - (b0 + b1 * ad); s2 = (res ** 2).sum() / (n - 2); t = stats.t.ppf(0.975, n - 2)
xs = np.linspace(5, 100, 100); fit = b0 + b1 * xs
band = t * np.sqrt(s2 * (1 + 1 / n + (xs - xm) ** 2 / sxx))
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ax.fill_between(xs, fit - band, fit + band, color=B, alpha=0.15, label="95% prediction band")
ax.plot(xs, fit, color=B, lw=2, label="fitted line")
for x, y, yh in zip(ad, sales, b0 + b1 * ad): ax.plot([x, x], [y, yh], color=R, lw=1.5)
ax.scatter(ad, sales, color=O, s=60, zorder=3, label="observed weeks")
ax.axvspan(62, 100, color="grey", alpha=0.08); ax.text(81, 110, "extrapolation:\nno data here", ha="center", fontsize=10)
ax.set_xlabel("ad spend (Rs thousand)", fontsize=11); ax.set_ylabel("sales (Rs thousand)", fontsize=11)
ax.legend(frameon=False, fontsize=9, loc="upper left"); clean(ax)
fig.tight_layout(); fig.savefig("ch07_regression_band.png")
# residual patterns
rng = np.random.default_rng(2); x = np.linspace(0, 10, 80)
y_lin = 5 + 2 * x + rng.normal(0, 2, 80); y_cur = 5 + 0.4 * x ** 2 + rng.normal(0, 2, 80)
fig, axs = plt.subplots(1, 2, figsize=(8, 3.8), dpi=110, sharey=True)
for ax, y, ttl, c in ((axs[0], y_lin, "line is right: residuals look like noise", T), (axs[1], y_cur, "line is wrong: residuals bend", R)):
    f = np.polyfit(x, y, 1); r = y - np.polyval(f, x)
    ax.scatter(np.polyval(f, x), r, color=c, s=18); ax.axhline(0, color="black", lw=1)
    ax.set_title(ttl, fontsize=10); ax.set_xlabel("fitted value", fontsize=10); clean(ax)
axs[0].set_ylabel("residual (actual minus fitted)", fontsize=10)
fig.tight_layout(); fig.savefig("ch07_residuals.png")
