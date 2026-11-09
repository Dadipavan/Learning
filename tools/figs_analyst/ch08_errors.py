import matplotlib
matplotlib.use("Agg")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def attempt(label, fn):
    try:
        fn()
    except Exception as e:
        print(f"{label}\n   {type(e).__name__}: {str(e)[:110]}")

fig, ax = plt.subplots()
attempt("1 title on the Figure", lambda: fig.set_title("x"))
attempt("2 x and y lengths differ", lambda: ax.plot([1, 2, 3], [1, 2, 3, 4]))
axs = plt.subplots(2, 2)[1]
attempt("3 indexing a 2D array of axes as one", lambda: axs.plot([1, 2]))
df = pd.DataFrame({"amount": [1, 2]})
attempt("4 column name typo", lambda: ax.hist(df["Amount"]))
attempt("5 style name typo", lambda: plt.style.use("ggplotx"))
attempt("6 bar with text heights", lambda: ax.bar(["a", "b"], [1, "two"]))
