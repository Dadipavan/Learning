import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.rcParams.update({"font.size":13,"axes.titlesize":15,"axes.spines.top":False,"axes.spines.right":False})
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"

rng=np.random.default_rng(2)
rows=[]
for c in range(6):
    size=300-20*c
    r=np.array([1,0.55,0.42,0.35,0.31,0.28])*rng.uniform(0.95,1.05,6); r[0]=1
    for k in range(6-c): rows.append((f"2025-{c+1:02d}",k,min(r[k],1)))
d=pd.DataFrame(rows,columns=["cohort","month","ret"]).pivot(index="cohort",columns="month",values="ret")
fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
im=ax.imshow(d.values,cmap="Blues",vmin=0,vmax=1,aspect="auto")
for i in range(d.shape[0]):
    for j in range(d.shape[1]):
        v=d.values[i,j]
        if not np.isnan(v): ax.text(j,i,f"{v:.0%}",ha="center",va="center",color="white" if v>.55 else "black",fontsize=12)
ax.set_xticks(range(6)); ax.set_yticks(range(6)); ax.set_yticklabels(d.index); ax.set_xlabel("months since first order"); ax.set_title("Cohort retention (illustrative data)")
for s in ax.spines.values(): s.set_visible(False)
plt.savefig("lib17_cohort.png",bbox_inches="tight")
