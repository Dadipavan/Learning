import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
B,O,T,R="#2b4fd6","#b84a22","#357a70","#aa2d26"
a=np.array([4.0,1.0]); b=np.array([2.0,3.0])
p=(a@b)/(b@b)*b
fig,ax=plt.subplots(figsize=(8,4.2))
def arr(v,c,l,lw=2.5,ls="-"):
    ax.annotate("",xy=v,xytext=(0,0),arrowprops=dict(arrowstyle="-|>",color=c,lw=lw,ls=ls))
arr(a,B,"a"); arr(b,O,"b"); arr(p,T,"p",lw=3)
ax.plot([a[0],p[0]],[a[1],p[1]],color=R,ls="--",lw=1.8)
ax.text(a[0]+0.1,a[1]-0.05,"a = (4, 1)",color=B,fontsize=12)
ax.text(b[0]-1.2,b[1]+0.2,"b = (2, 3)",color=O,fontsize=12)
ax.text(0.1,3.6,"proj of a on b = (1.69, 2.54)",color=T,fontsize=11)
ax.text(2.2,0.15,"angle θ ≈ 42.3°",fontsize=11)
ax.text(3.1,2.2,"a − p\n(perpendicular to b)",color=R,fontsize=10)
ax.set_xlim(-0.5,5.5); ax.set_ylim(-0.5,4); ax.set_aspect("equal")
ax.axhline(0,color="#999",lw=.8); ax.axvline(0,color="#999",lw=.8); ax.grid(alpha=.25)
ax.set_xlabel("x₁"); ax.set_ylabel("x₂"); ax.set_title("Projection of a onto b: the shadow of a on the line through b")
fig.tight_layout(); fig.savefig("ch05_dot_projection.png",dpi=110)
