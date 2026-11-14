import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
sns.set_theme(style="white", font_scale=1.1, rc={"figure.figsize": (8, 4.2), "figure.dpi": 110,
              "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
              "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
rng = np.random.default_rng(8)
cohorts = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
size = [520, 560, 610, 580, 640, 700]
base = np.array([1.0, 0.46, 0.36, 0.31, 0.28, 0.26])
rows = []
for i in range(6):
    r = base.copy()
    r[1:] = np.clip(r[1:] * (1 + 0.04 * i) + rng.normal(0, 0.012, 5), 0, 1)     # later cohorts retain a bit better
    r = np.concatenate([r[: 6 - i], np.full(i, np.nan)])                         # months not observed yet stay empty
    rows.append(r)
ret = pd.DataFrame(rows, index=[f"{c} (n={n})" for c, n in zip(cohorts, size)], columns=[f"M{k}" for k in range(6)])
print((ret * 100).round(0).to_string(na_rep="-"))
m1 = ret["M1"]
ax = sns.heatmap(ret.drop(columns="M0") * 100, annot=True, fmt=".0f", cmap="Blues", vmin=20, vmax=60,
                 linewidths=1.5, linecolor="white", cbar_kws={"label": "Customers still active (%)"},
                 annot_kws={"fontsize": 12, "fontweight": "bold"})
ax.set(xlabel="Months since joining", ylabel="Cohort (month joined)",
       title=f"Month-1 retention rose from {m1.iloc[0]:.0%} to {m1.iloc[4]:.0%}")
ax.tick_params(length=0)
ax.figure.savefig("ch08v_cohort.png", dpi=110, bbox_inches="tight")
print("saved")
