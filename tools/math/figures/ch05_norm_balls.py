import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
cols={"1":"#2b4fd6","2":"#b84a22","inf":"#357a70","0.5":"#6a2fd0"}
t=np.linspace(0,2*np.pi,2000)
fig,axs=plt.subplots(1,2,figsize=(8,4.2))
ax=axs[0]
for p,c in [("0.5",cols["0.5"]),("1",cols["1"]),("2",cols["2"]),("inf",cols["inf"])]:
    pp=np.inf if p=="inf" else float(p)
    d=np.stack([np.cos(t),np.sin(t)])
    if np.isinf(pp): n=np.abs(d).max(0)
    else: n=(np.abs(d)**pp).sum(0)**(1/pp)
    u=d/n
    ax.plot(u[0],u[1],color=c,lw=2,label=f"p = {p}")
ax.set_aspect("equal"); ax.legend(loc="upper right",fontsize=8); ax.grid(alpha=.25)
ax.set_title("Points with norm = 1"); ax.set_xlim(-1.4,1.4); ax.set_ylim(-1.4,1.4)
ax=axs[1]
ax.scatter([0],[0],color="k",zorder=3); ax.scatter([3],[4],color="k",zorder=3)
ax.plot([0,3],[0,4],color="#b84a22",lw=2.5,label="Euclidean = 5")
ax.plot([0,3,3],[0,0,4],color="#2b4fd6",lw=2.5,label="Manhattan = 7")
ax.plot([],[],lw=0,label="Chebyshev = 4 (largest gap)")
ax.text(1.0,2.4,"5",color="#b84a22",fontsize=12); ax.text(1.4,-0.5,"3",color="#2b4fd6",fontsize=12); ax.text(3.15,2,"4",color="#2b4fd6",fontsize=12)
ax.set_aspect("equal"); ax.legend(fontsize=8,loc="upper left"); ax.grid(alpha=.25)
ax.set_title("Three distances from (0,0) to (3,4)"); ax.set_xlim(-1,5); ax.set_ylim(-1,5)
fig.tight_layout(); fig.savefig("ch05_norm_balls.png",dpi=110)
