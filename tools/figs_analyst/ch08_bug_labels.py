import matplotlib
matplotlib.use("Agg")
import pandas as pd

by_city = pd.Series({"Delhi": 3298, "Mumbai": 3047, "Pune": 2995})
labels = sorted(by_city.index)                       # alphabetical: Delhi, Mumbai, Pune
values = by_city.sort_values().values.tolist()       # ascending by value: 2995, 3047, 3298
print("BUG : ", list(zip(labels, values)))
fixed = by_city.sort_values()                        # sort once, keep labels and values together
print("FIX : ", list(zip(fixed.index, fixed.values.tolist())))
