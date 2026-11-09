import sys, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, pandas as pd, numpy as np
DATA = "/Users/c2487352/Personal/Career/final/study/ways/data/"
sys.path.insert(0, DATA); import prep
o, c, p = prep.load_clean(DATA)
o["m"] = o.order_date.dt.to_period("M")
first = o.groupby("customer_id").m.min().rename("cohort")
x = o.join(first, on="customer_id"); x["k"] = (x.m - x.cohort).apply(lambda v: v.n)
mat = x.groupby(["cohort", "k"]).customer_id.nunique().unstack()
ret = mat.div(mat[0], axis=0)[range(0, 7)] * 100
fig, ax = plt.subplots(figsize=(8, 4.4))
im = ax.imshow(ret.values, cmap="Blues", aspect="auto", vmin=0, vmax=60)
ax.set_xticks(range(7)); ax.set_yticks(range(len(ret))); ax.set_yticklabels([str(i) for i in ret.index])
ax.set_xlabel("months since first order"); ax.set_ylabel("cohort (first-order month)")
for i in range(ret.shape[0]):
    for j in range(7):
        v = ret.values[i, j]
        if v == v: ax.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=7, color="white" if v > 35 else "black")
ax.set_title("Retention % by cohort (share of cohort ordering in month k)")
fig.colorbar(im, ax=ax); fig.tight_layout(); fig.savefig("ch04_retention.png", dpi=110)
