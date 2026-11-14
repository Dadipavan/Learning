import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig,ax=plt.subplots(figsize=(8,4.6)); ax.set_xlim(0,100); ax.set_ylim(0,60); ax.axis("off")
def box(x,y,w,h,t,c,fill=False):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.3,rounding_size=1.2",fc=(c if fill else "white"),ec=c,lw=1.8,alpha=1))
    ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=8,color=("white" if fill else c),fontweight="bold")
def arr(x1,y1,x2,y2,t=""):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=11,lw=1.4,color="#444"))
    if t: ax.text((x1+x2)/2+1,(y1+y2)/2+1,t,fontsize=7.5,color="#444")
box(35,51,30,7,"What is wrong or asked?","#2b4fd6",True)
cols=[("Numbers: size,\nmemory, cost","#aa2d26",5),("Wrong or missing\nresults","#b84a22",24),("Slow or\nrecall too low","#357a70",43),("Merging or\nranking math","#6a2fd0",62),("Metric or\nA/B question","#2b4fd6",81)]
for t,c,x in cols:
    box(x,36,17,9,t,c); arr(50,51,x+8.5,45)
leaf=[("Formula in 6.10:\nN x dim x bytes,\nplus links,\nthen shards","#aa2d26",5),
      ("Doctor checks 6.11:\nnorms, dims,\nself-retrieval,\nfilter, threshold","#b84a22",24),
      ("Measure recall@k\nvs exact, then\nturn ONE knob:\nnprobe / efSearch","#357a70",43),
      ("RRF: add up\n1/(k+rank)\nBM25 by hand,\nthen check in code","#6a2fd0",62),
      ("recall@k, MRR,\nnDCG on labelled\nqueries; compare\nsame query set","#2b4fd6",81)]
for t,c,x in leaf:
    box(x,10,17,19,t,c); arr(x+8.5,36,x+8.5,29)
ax.text(50,3.5,"Always finish: sanity-check units and bounds, then compare against the exact baseline",ha="center",fontsize=8.5,color="#333",style="italic")
ax.text(50,59.5,"",ha="center")
fig.tight_layout(); fig.savefig("ch06d_decision_flow.png",dpi=110)
