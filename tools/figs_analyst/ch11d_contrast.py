import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
def box(ax,x,y,w,h,txt,col,fs=9.5,fc=None,tc="white"):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc or col,ec=col,lw=1.5))
    ax.text(x+w/2,y+h/2,txt,ha="center",va="center",fontsize=fs,color=tc,fontweight="bold")
def arrow(ax,x1,y1,x2,y2,col="#444",lw=1.8):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=16,color=col,lw=lw))

def lum(h):
    h=h.lstrip("#"); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    c=[x/12.92 if x<=0.03928 else ((x+0.055)/1.055)**2.4 for x in c]
    return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
def ratio(a,b):
    l1,l2=sorted([lum(a),lum(b)],reverse=True); return (l1+0.05)/(l2+0.05)
cols=[("#9aa5b1","light grey"),("#767676","mid grey"),("#595959","dark grey"),("#1f6feb","blue"),("#b84a22","orange"),("#2b4fd6","house blue"),("#357a70","teal")]
r=[ratio(c,"#ffffff") for c,_ in cols]
fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
bars=ax.bar(range(len(cols)),r,color=[c for c,_ in cols],edgecolor="#333")
ax.axhline(4.5,color="#aa2d26",ls="--",lw=1.5); ax.text(6.45,4.6,"4.5 text",color="#aa2d26",ha="right",fontsize=10)
ax.axhline(3,color="#6a2fd0",ls=":",lw=1.5); ax.text(6.45,3.1,"3.0 large text / graphics",color="#6a2fd0",ha="right",fontsize=10)
for b,v in zip(bars,r): ax.text(b.get_x()+b.get_width()/2,v+0.12,f"{v:.2f}",ha="center",fontsize=10)
ax.set_xticks(range(len(cols))); ax.set_xticklabels([f"{n}\n{c}" for c,n in cols],fontsize=8.5)
ax.set_ylabel("contrast ratio vs white",fontsize=11); ax.set_title("Which colours pass as text on a white page",fontsize=12)
for s in ("top","right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig("ch11d_contrast.png")
