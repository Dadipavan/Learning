import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13,"axes.titlesize":15})

import time
def best(f,rep=3):
    t=1e9
    for _ in range(rep):
        s=time.perf_counter();f();t=min(t,time.perf_counter()-s)
    return t
ns=[1000,10000,100000,1000000]
tl=[];tv=[]
for n in ns:
    x=np.random.default_rng(0).random(n);xl=x.tolist()
    tl.append(best(lambda: sum(v*v for v in xl)))
    tv.append(best(lambda: float(x@x)))
fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
ax.loglog(ns,tl,"o-",color=O,lw=2.5,ms=8,label="Python loop (sum of squares)")
ax.loglog(ns,tv,"s-",color=B,lw=2.5,ms=8,label="NumPy x @ x")
ax.set_xlabel("array length n");ax.set_ylabel("seconds (best of 3)")
ax.set_title("Loop vs vectorised: both grow, one is far lower")
ax.legend();ax.grid(alpha=.3)
plt.savefig("lib16_speed.png",bbox_inches="tight")
