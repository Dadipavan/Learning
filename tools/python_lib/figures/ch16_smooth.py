import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13,"axes.titlesize":15})

rng=np.random.default_rng(3)
d=np.arange(120);y=10+0.05*d+2*np.sin(d/9)+rng.normal(0,1.2,120)
def ma(x,w): c=np.cumsum(np.insert(x,0,0.0));return (c[w:]-c[:-w])/w
fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
ax.plot(d,y,color="#999",lw=1.5,label="daily values (noisy)")
ax.plot(d[6:],ma(y,7),color=B,lw=3,label="7-day moving average")
ax.plot(d[19:],ma(y,20),color=O,lw=3,label="20-day moving average")
ax.set_xlabel("day");ax.set_ylabel("value");ax.legend(fontsize=11);ax.set_title("Longer window = smoother, later")
plt.savefig("lib16_smooth.png",bbox_inches="tight")
