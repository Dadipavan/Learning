import matplotlib
matplotlib.use("Agg")
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

orders = pd.DataFrame({"city": ["Delhi", "Delhi", "Pune", "Pune", "Pune", "Mumbai"],
                       "amount": [799, 2499, 998, 1400, 597, 1299]})
fig, ax = plt.subplots()
sns.barplot(data=orders, x="city", y="amount", order=["Delhi", "Mumbai", "Pune"], estimator="sum", errorbar=None, ax=ax)
heights = [round(p.get_height()) for p in ax.patches]
print("bars (Delhi, Mumbai, Pune):", heights)
print("groupby :", orders.groupby("city")["amount"].sum().loc[["Delhi", "Mumbai", "Pune"]].tolist())
print("mean (the default would show):", orders.groupby("city")["amount"].mean().loc[["Delhi", "Mumbai", "Pune"]].round(0).tolist())
