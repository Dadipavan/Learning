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

import hashlib, numpy as np
data=np.random.default_rng(1).bytes(400_000); edited=b"X"+data
def fixed(b,s=4096): return [b[i:i+s] for i in range(0,len(b),s)]
GEAR=[int(v) for v in np.random.default_rng(7).integers(0,2**32,256,dtype=np.uint64)]
def cdc(b,mask=0x0FFF,lo=1024,hi=16384):
    ch,st,h=[],0,0
    for i,x in enumerate(b):
        h=((h<<1)+GEAR[x])&0xFFFFFFFF; n=i-st+1
        if (n>=lo and (h&mask)==0) or n>=hi: ch.append(b[st:i+1]); st,h=i+1,0
    if st<len(b): ch.append(b[st:])
    return ch
ids=lambda c:[hashlib.md5(x).hexdigest() for x in c]
res=[]
for fn in (fixed,cdc):
    o,n=ids(fn(data)),ids(fn(edited)); r=len(set(o)&set(n)); res.append((r,len(n)-r))
fig,ax=plt.subplots(figsize=(8,4.2))
names=["fixed 4 KB chunks","content-defined chunks"]
ax.barh(names,[r[0] for r in res],color=T,label="chunks reused (already stored)")
ax.barh(names,[r[1] for r in res],left=[r[0] for r in res],color=R,label="chunks to upload")
for i,(a,b) in enumerate(res): ax.text(a+b+1,i,f"{b} new of {a+b}",va="center",fontsize=9)
ax.set_xlim(0,125); ax.set_xlabel("chunks in the edited file"); ax.legend(loc="center right",fontsize=8)
ax.set_title("Insert ONE byte at the start of a 400 KB file: what must be re-stored?",fontsize=10)
for s in ("top","right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig("ch04d_chunks.png",dpi=110)
