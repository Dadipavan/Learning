import matplotlib
matplotlib.use("Agg")
import pandas as pd

sales = pd.Series([350, 330, 375, 405], index=["Jan", "Feb", "Mar", "Apr"])
print("BUG  (sort_index on text)  :", sales.sort_index().index.tolist())
order = pd.CategoricalIndex(sales.index, categories=["Jan", "Feb", "Mar", "Apr"], ordered=True)
print("FIX  (ordered categories)  :", pd.Series(sales.values, index=order).sort_index().index.tolist())
dates = pd.to_datetime(["2025-01-01", "2025-02-01", "2025-03-01", "2025-04-01"])
print("BEST (real dates)          :", pd.Series(sales.values, index=dates).sort_index().index.strftime("%b").tolist())
