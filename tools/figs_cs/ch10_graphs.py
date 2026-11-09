import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
import heapq
# ---- Dijkstra steps
pos={"A":(0,1),"B":(1.6,2),"C":(1.6,0),"D":(3.4,1.0),"E":(5,1)}
edges=[("A","B",2),("A","C",7),("B","C",3),("B","D",8),("C","D",1),("D","E",2),("C","E",5)]
adj={}
for u,v,w in edges: adj.setdefault(u,[]).append((v,w))
dist={n:float("inf") for n in pos}; dist["A"]=0; done=[]; snaps=[]; pq=[(0,"A")]; pred={}
while pq:
    d,u=heapq.heappop(pq)
    if u in done: continue
    done.append(u)
    for v,w in adj.get(u,[]):
        if d+w<dist[v]: dist[v]=d+w; pred[v]=u; heapq.heappush(pq,(dist[v],v))
    snaps.append((list(done),dict(dist),dict(pred)))
fig,axs=plt.subplots(2,3,figsize=(11,6))
for ax,(dn,ds,pr),i in zip(axs.flat,snaps[:5],range(5)):
    fill={n:(TEAL) for n in dn}
    lab={n:("inf" if ds[n]==float("inf") else str(ds[n])) for n in pos}
    hl={(pr[v],v) for v in dn if v in pr}
    draw_graph(ax,pos,edges,fill,lab,hl=hl)
    ax.set_title(f"Step {i+1}: finalise {dn[-1]}")
axs.flat[5].axis("off")
axs.flat[5].text(0.02,0.7,"Teal = finalised (shortest known\nfor sure). Red number = best\ndistance found so far.\nOrange edges = best path tree.",fontsize=11,va="top")
plt.tight_layout(); plt.savefig("ch10_dijkstra_steps.png",dpi=110); plt.close()
print(snaps[-1][1])
# ---- BFS layers
pos={0:(0,1),1:(1.5,2),2:(1.5,0),3:(3,2.4),4:(3,1),5:(3,-0.4),6:(4.5,1.2),7:(4.5,-0.2)}
edges=[(0,1),(0,2),(1,3),(1,4),(2,4),(2,5),(4,6),(5,7),(6,7)]
from collections import deque
adjl={n:[] for n in pos}
for u,v in edges: adjl[u].append(v); adjl[v].append(u)
d={0:0}; q=deque([0])
while q:
    u=q.popleft()
    for v in sorted(adjl[u]):
        if v not in d: d[v]=d[u]+1; q.append(v)
cols=[BLUE,TEAL,ORANGE,PURPLE,RED]
fig,ax=plt.subplots(figsize=(8,4.2))
draw_graph(ax,pos,edges,{n:cols[d[n]] for n in pos},{n:f"d={d[n]}" for n in pos},directed=False,ewlabels=False)
ax.set_title("BFS layers from node 0: colour = number of edges from the start")
plt.tight_layout(); plt.savefig("ch10_bfs_layers.png",dpi=110); plt.close()
print(d)
# ---- union-find forest
fig,axs=plt.subplots(1,3,figsize=(11,3.6))
def forest(ax,parent,title):
    # compute depth layout
    kids={}
    for c,p in parent.items():
        if c!=p: kids.setdefault(p,[]).append(c)
    roots=[n for n in parent if parent[n]==n]
    pos={}; x=[0]
    def lay(n,dep):
        ch=kids.get(n,[])
        if not ch: pos[n]=(x[0],-dep); x[0]+=1; return
        for c in ch: lay(c,dep+1)
        pos[n]=(sum(pos[c][0] for c in ch)/len(ch),-dep)
    for r in roots: lay(r,0); x[0]+=0.5
    ed=[(c,p) for c,p in parent.items() if c!=p]
    draw_graph(ax,pos,ed,{r:BLUE for r in roots},directed=True,ewlabels=False,r=0.25)
    ax.set_title(title)
draw=[{i:i for i in range(6)},
 {0:0,1:0,2:1,3:2,4:3,5:5},
 {0:0,1:0,2:0,3:0,4:0,5:5}]
forest(axs[0],draw[0],"Start: 6 separate sets")
forest(axs[1],draw[1],"Chain 0<-1<-2<-3<-4 (bad)")
forest(axs[2],draw[2],"After find(4) with path compression")
plt.tight_layout(); plt.savefig("ch10_uf_forest.png",dpi=110); plt.close()
