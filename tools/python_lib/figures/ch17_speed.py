import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.rcParams.update({"font.size":13,"axes.titlesize":15,"axes.spines.top":False,"axes.spines.right":False})
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"

import time
rng=np.random.default_rng(0); n=100_000
df=pd.DataFrame({"a":rng.normal(size=n),"b":rng.normal(size=n)})
def t(f,k=3):
    best=1e9
    for _ in range(k):
        s=time.perf_counter(); f(); best=min(best,time.perf_counter()-s)
    return best*1000
res={"iterrows loop":t(lambda:[r.a+r.b for _,r in df.iterrows()],1),"apply(axis=1)":t(lambda:df.apply(lambda r:r.a+r.b,axis=1),1),"list comprehension":t(lambda:[x+y for x,y in zip(df.a,df.b)]),"vectorised a + b":t(lambda:df.a+df.b)}
fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
ax.barh(list(res)[::-1],list(res.values())[::-1],color=[T,B,O,R]); ax.set_xscale("log"); ax.set_xlabel("milliseconds (log scale, best of a few runs, your machine differs)")
for i,v in enumerate(list(res.values())[::-1]): ax.text(v*1.15,i,f"{v:.1f} ms",va="center",fontsize=12)
ax.set_xlim(0.01,max(res.values())*8); ax.set_title("Adding two columns, 100,000 rows")
plt.savefig("lib17_speed.png",bbox_inches="tight")
