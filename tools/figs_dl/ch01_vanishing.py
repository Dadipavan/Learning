import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
BL,OR,TE,RE,PU,CR="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0","#f1e6c8"
plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
def box(ax,x,y,w,h,t,c,fs=9.5,tc=None):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.25",fc=c,ec="#222",lw=1.2))
    ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=fs,color=tc or ("black" if c==CR else "white"))
def arrow(ax,x1,y1,x2,y2,col="#222"): ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="->",lw=1.6,color=col))

def grads(kind,L=10,n=50,seed=0):
    rng=np.random.default_rng(seed); Ws=[]
    for _ in range(L): Ws.append(rng.normal(size=(n,n))*(np.sqrt(2/n) if kind=="relu" else np.sqrt(1/n)))
    h=rng.normal(size=n); acts=[h]; zs=[]
    for W in Ws:
        z=W@h; zs.append(z); h=np.maximum(0,z) if kind=="relu" else 1/(1+np.exp(-z)); acts.append(h)
    g=np.ones(n); out=[]
    for i in reversed(range(L)):
        d=(zs[i]>0).astype(float) if kind=="relu" else acts[i+1]*(1-acts[i+1])
        g=g*d; out.append(np.linalg.norm(g)); g=Ws[i].T@g
    return out[::-1]
fig,axs=plt.subplots(1,2,figsize=(8,4.2))
L=np.arange(1,11)
for k,c in [("sigmoid",RE),("relu",TE)]: axs[0].semilogy(L,grads(k),"o-",color=c,label=k)
axs[0].set_xlabel("layer (1 = closest to input)"); axs[0].set_ylabel("gradient norm at layer's pre-activation"); axs[0].legend(); axs[0].set_title("Measured, 10-layer net",fontsize=10)
d=np.arange(1,11)
axs[1].semilogy(d,0.25**d,"o-",color=RE,label="sigmoid best case 0.25^L"); axs[1].semilogy(d,0.045**d,"s-",color=OR,label="sigmoid at z=3: 0.045^L")
axs[1].semilogy(d,np.ones(10),"^-",color=TE,label="ReLU active: 1^L"); axs[1].set_xlabel("layers the gradient crosses"); axs[1].set_title("Product of slopes",fontsize=10); axs[1].legend(fontsize=8)
fig.tight_layout(); fig.savefig("ch01d_vanishing.png",dpi=110)
