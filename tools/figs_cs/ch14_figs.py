import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
from matplotlib.patches import FancyBboxPatch
def box(ax,x,y,w,h,txt,fc="white",ec="#222",fs=10,tc="#111"):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=1.5))
    ax.text(x+w/2,y+h/2,txt,ha="center",va="center",fontsize=fs,color=tc)
def arrow(ax,p,q,col="#444",style="-|>"):
    ax.annotate("",xy=q,xytext=p,arrowprops=dict(arrowstyle=style,color=col,lw=1.6))
# LRU diagram
fig,ax=plt.subplots(figsize=(9,4.4)); ax.set_xlim(0,10); ax.set_ylim(0,5); ax.axis("off")
ax.text(0.2,4.6,"Hash map: key -> node (O(1) lookup)",fontsize=11,color=BLUE,fontweight="bold")
for i,(k,x) in enumerate([("C",1.5),("A",3.4),("B",5.3)]):
    box(ax,x,3.5,1.2,0.6,f"key {k}",fc="#dfe6fb",ec=BLUE)
ax.text(0.2,0.35,"Doubly linked list: most recent on the left, least recent on the right",fontsize=11,color=ORANGE,fontweight="bold")
nodes=[("head",0.2,"#eee",GREY),("C",2.0,"#f4dccf",ORANGE),("A",3.9,"#f4dccf",ORANGE),("B",5.8,"#f4dccf",ORANGE),("tail",7.7,"#eee",GREY)]
for n,x,fc,ec in nodes: box(ax,x,1.0,1.3,0.7,n if n in("head","tail") else f"{n}: value",fc=fc,ec=ec)
for a,b in zip(nodes,nodes[1:]):
    arrow(ax,(a[1]+1.3,1.45),(b[1],1.45)); arrow(ax,(b[1],1.2),(a[1]+1.3,1.2))
for x,k,tx in [(1.5,"C",2.65),(3.4,"A",4.55),(5.3,"B",6.45)]:
    arrow(ax,(x+0.6,3.5),(tx,1.7),col=BLUE,style="->")
ax.text(6.45,0.75,"evict from here",ha="center",fontsize=10,color=RED)
ax.set_title("LRU cache: a map for speed plus a list for recency order")
plt.tight_layout(); plt.savefig("ch14_lru.png",dpi=110); plt.close()
# pattern chooser
fig,ax=plt.subplots(figsize=(10,5)); ax.set_xlim(0,10); ax.set_ylim(0,6); ax.axis("off")
rows=[("Sorted or can sort? pairs/triples","two pointers, binary search"),
("Contiguous subarray or substring","sliding window, prefix sums, Kadane"),
("Find an item fast / count / group","hash map or set"),
("Next greater / nested / undo","stack, monotonic stack"),
("Top k, running min or max, merge k","heap"),
("Tree, grid or network, reach or shortest","DFS, BFS, Dijkstra, union-find"),
("Count / best over choices, overlapping","DP (state, recurrence, order)"),
("Range query with updates / text search","Fenwick, segment tree, KMP, rolling hash")]
cols=[BLUE,TEAL,ORANGE,PURPLE,RED,BLUE,TEAL,ORANGE]
for i,((q,a),c) in enumerate(zip(rows,cols)):
    y=5.4-i*0.7
    box(ax,0.2,y,4.6,0.55,q,fc="white",ec=c,fs=10)
    arrow(ax,(4.85,y+0.27),(5.35,y+0.27),col=c)
    box(ax,5.4,y,4.4,0.55,a,fc=c,ec=c,fs=10,tc="white")
ax.set_title("First-guess chooser: what the problem says, and the tool to try first")
plt.tight_layout(); plt.savefig("ch14_pattern_chooser.png",dpi=110); plt.close()
