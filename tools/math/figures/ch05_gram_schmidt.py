import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
B,O,T,R="#2b4fd6","#b84a22","#357a70","#aa2d26"
v1=np.array([3.0,1.0]); v2=np.array([2.0,2.0])
u1=v1/np.linalg.norm(v1); w=v2-(v2@u1)*u1; u2=w/np.linalg.norm(w)
fig,axs=plt.subplots(1,2,figsize=(8,4.2))
def arr(ax,v,c,lab,off=(0.05,0.05),o=(0,0),lw=2.5):
    ax.annotate("",xy=np.array(o)+v,xytext=o,arrowprops=dict(arrowstyle="-|>",color=c,lw=lw))
    ax.text(o[0]+v[0]+off[0],o[1]+v[1]+off[1],lab,color=c,fontsize=11)
ax=axs[0]
arr(ax,v1,B,"v₁ = (3, 1)"); arr(ax,v2,O,"v₂ = (2, 2)")
ax.set_title("Input: two vectors, not perpendicular")
ax=axs[1]
arr(ax,v1,B,"q₁ = v₁",(0.05,-0.3)); arr(ax,(v2@u1)*u1,T,"shadow",(0.05,-0.35),lw=2)
arr(ax,w,R,"q₂ = v₂ − shadow",(-2.3,0.5),o=(v2@u1)*u1)
arr(ax,v2,O,"v₂",(0.1,0.05),lw=1.5)
ax.set_title("Output: perpendicular pair q₁, q₂")
for ax in axs:
    ax.set_xlim(-1,4.2); ax.set_ylim(-0.8,3.2); ax.set_aspect("equal"); ax.grid(alpha=.25)
    ax.axhline(0,color="#999",lw=.8); ax.axvline(0,color="#999",lw=.8)
fig.tight_layout(); fig.savefig("ch05_gram_schmidt.png",dpi=110)
