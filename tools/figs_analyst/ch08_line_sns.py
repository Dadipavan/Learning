import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
sns.set_theme(style="white", font_scale=1.1, rc={"figure.figsize": (8, 4.2), "figure.dpi": 110,
              "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
              "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
months = pd.period_range("2024-01", "2025-06", freq="M").to_timestamp()
monthly = pd.Series([310, 295, 340, 360, 385, 400, 380, 410, 430, 470, 560, 620,
                     350, 330, 375, 405, 430, 455], index=months, name="sales_k")
df = monthly.rename_axis("month").reset_index()
ax = sns.lineplot(data=df, x="month", y="sales_k", color=BLUE, linewidth=2.5, marker="o")
ax.set(ylim=(0, 700), xlabel="", ylabel="Sales (Rs thousand)", title="The festive season lifted sales to 620k in Dec 2024")
ax.figure.autofmt_xdate()
ax.figure.tight_layout()
ax.figure.savefig("ch08v_line_sns.png", dpi=110)
print(df.tail(3).to_string(index=False))
print("saved")
