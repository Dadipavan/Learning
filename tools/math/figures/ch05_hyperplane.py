import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
B,O,T,R="#2b4fd6","#b84a22","#357a70","#aa2d26"
w=np.array([1.0,1.0]); b=-5.0
pos=np.array([[4,3],[5,4],[3.5,3.5],[5,2.5],[4.5,5]]); neg=np.array([[1,1],[2,1.5],[1.5,2.5],[0.5,3],[2.5,0.5]])
fig,ax=plt.subplots(figsize=(8,4.2))
x=np.linspace(-0.5,6,50)
ax.plot(x,-(w[0]*x+b)/w[1],color="k",lw=2.5,label="w·x + b = 0")
for k,ls in [(1,"--"),(-1,"--")]:
    ax.plot(x,-(w[0]*x+b-k)/w[1],color="#888",lw=1.5,ls=ls)
ax.scatter(*pos.T,color=B,s=60,label="class +1"); ax.scatter(*neg.T,color=O,s=60,label="class −1")
q=np.array([5,4.0]); d=(w@q+b)/np.linalg.norm(w)
foot=q-d*w/np.linalg.norm(w)
ax.plot([q[0],foot[0]],[q[1],foot[1]],color=R,lw=2)
ax.text(5.05,3.3,f"distance = {d:.2f}",color=R,fontsize=11)
ax.annotate("",xy=(2.5+0.7,2.5+0.7),xytext=(2.5,2.5),arrowprops=dict(arrowstyle="-|>",color=T,lw=2.5))
ax.text(1.8,3.4,"w = (1, 1)",color=T,fontsize=11)
ax.text(0.2,5.2,"dashed lines: w·x + b = ±1",fontsize=9,color="#555")
ax.set_xlim(-0.5,6); ax.set_ylim(-0.5,6); ax.set_aspect("equal"); ax.grid(alpha=.25); ax.legend(loc="lower left",fontsize=9)
ax.set_xlabel("feature 1"); ax.set_ylabel("feature 2"); ax.set_title("A hyperplane splits space; w points to the positive side")
fig.tight_layout(); fig.savefig("ch05_hyperplane.png",dpi=110)
