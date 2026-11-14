import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
def box(ax,x,y,w,h,txt,c,fs=9,fc=None):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc or "white",ec=c,lw=2))
    ax.text(x+w/2,y+h/2,txt,ha="center",va="center",fontsize=fs,color="#222")
def arrow(ax,a,b,c="#444",txt=None,off=(0,0.12),fs=8):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle="->",color=c,lw=1.8))
    if txt: ax.text((a[0]+b[0])/2+off[0],(a[1]+b[1])/2+off[1],txt,ha="center",fontsize=fs,color=c)

import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
X,y=make_classification(n_samples=3000,n_features=10,n_informative=5,random_state=11)
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=0.3,random_state=0)
rng=np.random.default_rng(5); keep=(ytr==0)|(rng.random(len(ytr))<0.2)
def sc(C,d):
    Xa,ya=(Xtr,ytr) if d==1 else (Xtr[keep],ytr[keep])
    return LogisticRegression(C=C,max_iter=200).fit(Xa,ya).score(Xte,yte)
fig,ax=plt.subplots(figsize=(8,4.2)); w=0.35
for i,(C,col) in enumerate([(1.0,B),(0.01,O)]):
    vals=[sc(C,1),sc(C,2)]; ax.bar(np.arange(2)+i*w,vals,w,color=col,label=f"C = {C}")
    for j,v in enumerate(vals): ax.text(j+i*w,v+0.01,f"{v:.3f}",ha="center",fontsize=9)
ax.set_xticks(np.arange(2)+w/2); ax.set_xticklabels(["data v1 (positive rate 0.50)","data v2 (positive rate 0.17)"])
ax.set_ylim(0,0.8); ax.set_ylabel("test accuracy"); ax.legend()
ax.set_title("Change one pin at a time: the data change moves accuracy far more than the code change",fontsize=9.5)
for s in ("top","right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig("ch04d_ablation.png",dpi=110)
