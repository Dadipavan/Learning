import matplotlib
matplotlib.use("Agg")
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(8)
tidy = pd.DataFrame({"month": np.tile(pd.date_range("2025-01-01", periods=6, freq="MS"), 3),
                     "city": np.repeat(["Delhi", "Mumbai", "Pune"], 6),
                     "sales_k": np.round(np.concatenate([np.linspace(15, 30, 6), np.linspace(23, 10, 6), np.linspace(5, 7, 6)])
                                         + rng.normal(0, 1, 18), 1)})
g = sns.relplot(data=tidy, x="month", y="sales_k", col="city", kind="line", height=2.4, aspect=1.2, color="#2b4fd6")
g.set_titles("{col_name}")
g.set_axis_labels("", "Sales (Rs thousand)")
g.figure.savefig("ch08v_practice_facets.png", dpi=110)
print(type(g).__name__, "| panels:", g.axes.shape, "| shared y range:", tuple(round(v) for v in g.axes[0, 0].get_ylim()))
