import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(9,4.2)); ax.set_xlim(0,100); ax.set_ylim(0,50); ax.axis("off")
def box(x,y,w,h,t,c):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.4",fc=c,ec="#222",lw=1.5))
    ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=11,color="white" if c in("#2b4fd6","#357a70","#6a2fd0") else "black")
def arrow(x1,y1,x2,y2): ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="->",lw=2,color="#222"))
box(2,28,16,14,"Image","#f1e6c8")
box(26,28,20,14,"Image encoder\n(big, run once)","#2b4fd6")
box(2,4,16,14,"Prompt:\npoints, box,\nrough mask","#f1e6c8")
box(26,4,20,14,"Prompt encoder\n(small)","#357a70")
box(58,16,18,14,"Mask decoder\n(light, fast)","#6a2fd0")
box(84,16,14,14,"Masks +\nquality\nscores","#f1e6c8")
arrow(18,35,26,35); arrow(18,11,26,11)
arrow(46,35,58,26); arrow(46,11,58,20); arrow(76,23,84,23)
ax.text(36,46,"embedding is reused for every new prompt",ha="center",fontsize=11)
fig.tight_layout(); fig.savefig("sam_prompt_flow.png",dpi=110)
