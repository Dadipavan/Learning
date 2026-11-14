import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
from matplotlib.patches import FancyBboxPatch
def box(ax,x,y,w,h,txt,fc="white",ec="#222",fs=10,tc="#111",lw=1.5):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw))
    ax.text(x+w/2,y+h/2,txt,ha="center",va="center",fontsize=fs,color=tc)
fig,ax=plt.subplots(figsize=(9,4.8)); ax.set_xlim(0,10); ax.set_ylim(0,5.4); ax.axis("off")
box(ax,0.2,0.2,9.6,0.9,"One Linux kernel (shared by every container)\nscheduler, memory manager, network stack",fc="#eceff9",ec=BLUE,fs=11)
for x,name,lim in [(0.4,"Container A","limit: 512 MiB, 1 CPU"),(5.2,"Container B","limit: 2 GiB, 4 CPUs")]:
    box(ax,x,1.5,4.4,3.2,"",fc="white",ec=ORANGE,lw=2)
    ax.text(x+2.2,4.4,name,ha="center",fontsize=12,fontweight="bold",color=ORANGE)
    box(ax,x+0.2,3.1,4.0,0.9,"namespaces: its own process IDs,\nhostname, network, mounts",fc="#f4dccf",ec=ORANGE,fs=9.5)
    box(ax,x+0.2,2.0,4.0,0.8,f"cgroup  ({lim})",fc="#d7ebe7",ec=TEAL,fs=10)
ax.text(5,5.1,"Namespaces decide what a process can SEE. cgroups decide how much it can USE.",ha="center",fontsize=11)
plt.tight_layout(); plt.savefig("ch05_containers.png",dpi=110); plt.close()
# GIL timeline
fig,axs=plt.subplots(3,1,figsize=(9,4.6),sharex=True)
def bar(ax,row,s,e,c): ax.barh(row,e-s,left=s,color=c,edgecolor="#222",height=0.6)
ax=axs[0]; ax.set_title("A: one thread, four tasks in a row (time 4 units)",loc="left",fontsize=10)
for i in range(4): bar(ax,0,i,i+1,[BLUE,TEAL,ORANGE,PURPLE][i])
ax=axs[1]; ax.set_title("B: four threads, CPU-bound work: the GIL lets one run at a time (still about 4 units)",loc="left",fontsize=10)
for k in range(16):
    t=k*0.25; bar(ax,k%4,t,t+0.25,[BLUE,TEAL,ORANGE,PURPLE][k%4])
ax=axs[2]; ax.set_title("C: four processes on four cores: truly parallel (about 1 unit plus start-up cost)",loc="left",fontsize=10)
for k in range(4): bar(ax,k,0,1,[BLUE,TEAL,ORANGE,PURPLE][k])
for a in axs: a.set_yticks([]); a.set_xlim(0,4.2)
axs[2].set_xlabel("time (arbitrary units)")
plt.tight_layout(); plt.savefig("ch05_gil.png",dpi=110); plt.close()
