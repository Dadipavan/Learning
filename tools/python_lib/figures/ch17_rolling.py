import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.rcParams.update({"font.size":13,"axes.titlesize":15,"axes.spines.top":False,"axes.spines.right":False})
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"

rng=np.random.default_rng(1); idx=pd.date_range("2025-01-01",periods=120,freq="D")
s=pd.Series(100+np.cumsum(rng.normal(0,3,120)),index=idx)
fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
ax.plot(s,color="#999999",lw=1,label="daily")
ax.plot(s.rolling(7).mean(),color=B,lw=2.5,label="rolling(7).mean()")
ax.plot(s.expanding().mean(),color=O,lw=2.5,label="expanding().mean()")
w=s.resample("W").mean(); ax.step(w.index,w.values,color=T,lw=2.5,where="mid",label="resample('W').mean()")
ax.legend(fontsize=11); ax.set_title("Three ways to smooth one series"); fig.autofmt_xdate()
plt.savefig("lib17_rolling.png",bbox_inches="tight")
