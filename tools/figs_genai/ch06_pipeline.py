import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
fig,ax=plt.subplots(figsize=(8,4.2)); ax.set_xlim(0,100); ax.set_ylim(0,66); ax.axis("off")
def box(x,y,w,h,txt,col,sub=""):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.4,rounding_size=1.5",fc="white",ec=col,lw=2))
    ax.text(x+w/2,y+h/2+(2 if sub else 0),txt,ha="center",va="center",fontsize=9,fontweight="bold",color=col)
    if sub: ax.text(x+w/2,y+h/2-3.2,sub,ha="center",va="center",fontsize=7.5,color="#333")
def arrow(x1,y1,x2,y2,col="#444"):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=12,lw=1.6,color=col))
box(1,40,16,12,"Query",B,"text from user")
box(22,40,16,12,"Embed",B,"query becomes 1 vector")
box(43,48,19,10,"Filter + ANN",T,"vector index")
box(43,31,19,10,"BM25",O,"keyword index")
box(68,40,14,12,"RRF merge",P,"ranks only")
box(86,40,13,12,"Rerank",R,"cross-encoder")
arrow(17,46,22,46); arrow(38,46,43,52); arrow(38,44,43,37); arrow(62,52,68,48); arrow(62,36,68,44); arrow(82,46,86,46)
ax.text(52,24,"candidate counts (illustrative)",ha="center",fontsize=9,color="#444")
steps=[("50,000,000","chunks in index",B),("top 100","from ANN",T),("top 100","from BM25",O),("about 150","after merge",P),("top 5","after rerank",R)]
x=4
for n,s,c in steps:
    ax.add_patch(FancyBboxPatch((x,6),17,12,boxstyle="round,pad=0.3,rounding_size=1",fc=c,ec=c,alpha=0.12))
    ax.text(x+8.5,13,n,ha="center",fontsize=10,fontweight="bold",color=c); ax.text(x+8.5,9,s,ha="center",fontsize=8,color="#333")
    x+=19.5
for i in range(4): ax.text(4+17+i*19.5+1.25,12,">",fontsize=14,color="#888",ha="center",va="center")
ax.text(50,63.5,"Retrieval is a funnel: wide and cheap first, narrow and expensive last",ha="center",fontsize=10.5,fontweight="bold")
fig.tight_layout(); fig.savefig("ch06d_pipeline.png",dpi=110)
