import matplotlib
matplotlib.use("Agg")
import warnings
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.DataFrame({"city": ["Delhi", "Pune", "Delhi", "Pune"], "amount": [10, 20, 30, 40]})
def attempt(label, fn):
    try:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            fn()
        for item in w:
            print(f"{label}\n   {item.category.__name__}: {' '.join(str(item.message).split())[:100]}")
    except Exception as e:
        print(f"{label}\n   {type(e).__name__}: {str(e)[:110]}")

attempt("1 wrong column name", lambda: sns.barplot(data=df, x="City", y="amount"))
attempt("2 palette without hue", lambda: sns.barplot(data=df, x="city", y="amount", palette="Set2"))
fig, ax = plt.subplots()
attempt("3 ax= on a figure-level function", lambda: sns.displot(data=df, x="amount", ax=ax))
attempt("4 hue column name typo", lambda: sns.scatterplot(data=df, x="amount", y="amount", hue="Amount"))
