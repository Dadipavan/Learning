import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BLUE="#2b4fd6"; ORANGE="#b84a22"; TEAL="#357a70"; RED="#aa2d26"; PURPLE="#6a2fd0"; GREY="#8a8a8a"; LIGHT="#e8ecf8"
plt.rcParams.update({"font.size":11,"axes.titlesize":12,"font.family":"DejaVu Sans"})
def draw_graph(ax, pos, edges, fill=None, labels=None, directed=True, ewlabels=True, hl=None, r=0.28):
    import math
    fill = fill or {}
    labels = labels or {}
    hl = hl or set()
    for e in edges:
        u,v = e[0],e[1]; w = e[2] if len(e)>2 else None
        (x1,y1),(x2,y2)=pos[u],pos[v]
        dx,dy=x2-x1,y2-y1; d=math.hypot(dx,dy); ux,uy=dx/d,dy/d
        sx,sy=x1+ux*r,y1+uy*r; ex,ey=x2-ux*r,y2-uy*r
        col = ORANGE if (u,v) in hl or (v,u) in hl else GREY
        ax.annotate("",xy=(ex,ey),xytext=(sx,sy),arrowprops=dict(arrowstyle="-|>" if directed else "-",color=col,lw=2 if col==ORANGE else 1.4,shrinkA=0,shrinkB=0))
        if w is not None and ewlabels:
            mx,my=(x1+x2)/2-uy*0.17,(y1+y2)/2+ux*0.17
            ax.text(mx,my,str(w),ha="center",va="center",fontsize=10,color="#333",bbox=dict(fc="white",ec="none",pad=0.5))
    for n,(x,y) in pos.items():
        ax.add_patch(plt.Circle((x,y),r,fc=fill.get(n,"white"),ec="#222",lw=1.5,zorder=3))
        ax.text(x,y,str(n),ha="center",va="center",fontsize=12,zorder=4,color="white" if fill.get(n) in (BLUE,TEAL,PURPLE,RED,ORANGE) else "#111")
        if n in labels:
            ax.text(x+0.05,y-r-0.06,labels[n],ha="center",va="top",fontsize=10,color=RED,fontweight="bold",bbox=dict(fc="white",ec="none",pad=0.3))
    xs=[p[0] for p in pos.values()]; ys=[p[1] for p in pos.values()]
    ax.set_xlim(min(xs)-0.7,max(xs)+0.7); ax.set_ylim(min(ys)-0.9,max(ys)+0.7); ax.set_aspect("equal"); ax.axis("off")
