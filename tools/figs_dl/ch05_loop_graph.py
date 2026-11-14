import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
BL,OR,TE,PU,CR="#2b4fd6","#b84a22","#357a70","#6a2fd0","#f1e6c8"
def base(w,h,size=(9,4.2)):
    fig,ax=plt.subplots(figsize=size); ax.set_xlim(0,w); ax.set_ylim(0,h); ax.axis("off"); return fig,ax
def box(ax,x,y,w,h,t,c,fs=11):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.3",fc=c,ec="#222",lw=1.5))
    ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=fs,color="white" if c!=CR else "black")
def arrow(ax,x1,y1,x2,y2,col="#222"): ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="->",lw=2,color=col))
# training loop
fig,ax=base(100,50)
box(ax,2,34,16,10,"next batch\n(xb, yb)",CR); box(ax,24,34,16,10,"forward\npred = model(xb)",BL)
box(ax,46,34,16,10,"loss\nloss_fn(pred, yb)",BL); box(ax,68,34,16,10,"backward\nloss.backward()",OR)
box(ax,68,10,16,10,"update\nopt.step()",TE); box(ax,24,10,16,10,"clear\nopt.zero_grad()",PU)
for a,b in [(18,24),(40,46),(62,68)]: arrow(ax,a,39,b,39)
arrow(ax,76,34,76,20); arrow(ax,68,15,40,15); arrow(ax,32,20,32,34)
ax.text(50,2,"repeat for every batch; one pass over the data is one epoch",ha="center",fontsize=11)
ax.text(50,24,"zero_grad can also go first in the loop",ha="center",fontsize=10)
fig.tight_layout(); fig.savefig("pytorch_train_loop.png",dpi=110); plt.close(fig)
# autograd graph
fig,ax=base(100,50)
box(ax,2,36,10,8,"a = 2",CR); box(ax,2,22,10,8,"b = 3",CR); box(ax,2,6,10,8,"c = 1",CR)
box(ax,28,29,14,8,"u = a*b = 6",BL); box(ax,50,12,14,8,"v = u+c = 7",BL); box(ax,74,12,14,8,"f = v*v = 49",BL)
arrow(ax,12,40,28,34); arrow(ax,12,26,28,32); arrow(ax,42,31,50,18); arrow(ax,12,10,50,14); arrow(ax,64,16,74,16)
ax.text(52,45,"forward: values flow left to right",fontsize=11,color=BL)
ax.text(52,40,"backward: gradients flow right to left",fontsize=11,color=OR)
ax.text(76,6,"df/df = 1\ndf/dv = 2v = 14",fontsize=10,color=OR,ha="left")
ax.text(44,3,"df/du = 14, df/dc = 14",fontsize=10,color=OR)
ax.text(14,47,"df/da = 14*b = 42   df/db = 14*a = 28",fontsize=10,color=OR)
fig.tight_layout(); fig.savefig("autograd_graph.png",dpi=110)
