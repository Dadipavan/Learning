import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.rcParams.update({"font.size":13,"axes.titlesize":15,"axes.spines.top":False,"axes.spines.right":False})
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"

rng=np.random.default_rng(0); n=200_000
s=pd.Series(rng.choice(["alpha","beta","gamma","delta"],n))
df=pd.DataFrame({"object-like str":s,"category":s.astype("category")})
ints=pd.Series(rng.integers(0,100,n))
m={"str column":s.memory_usage(deep=True),"category":s.astype("category").memory_usage(deep=True),"int64":ints.memory_usage(deep=True),"int8":ints.astype("int8").memory_usage(deep=True),"float64":ints.astype("float64").memory_usage(deep=True)}
fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
ax.barh(list(m)[::-1],[v/1e6 for v in list(m.values())[::-1]],color=[T,O,B,P,R][::-1] if False else [R,P,B,O,T])
for i,v in enumerate(list(m.values())[::-1]): ax.text(v/1e6+.02,i,f"{v/1e6:.2f} MB",va="center",fontsize=12)
ax.set_xlabel("memory (MB), 200,000 rows"); ax.set_xlim(0,max(m.values())/1e6*1.35); ax.set_title("Same data, different dtypes")
plt.savefig("lib17_dtypes.png",bbox_inches="tight")
