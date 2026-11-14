from common import *
import numpy as np
m=["Jan","Feb","Mar"]; d={"North":[120,125,130],"West":[95,97,99],"South":[80,60,55]}
fig,(a,b)=plt.subplots(1,2,figsize=(8,4.2),dpi=110)
cols=[BLUE,ORANGE,TEAL]
for (k,v),c in zip(d.items(),cols): a.plot(m,v,marker="o",color=c,label=k)
a.set_title("Sales",fontsize=10); a.legend(fontsize=7); a.grid(True); a.set_ylim(50,135)
a.text(0.5,0.04,"BEFORE: vague title, legend, grid,\ncolours with no priority",transform=a.transAxes,ha="center",fontsize=8,color=RED)
for k,v in d.items():
    if k=="South":
        b.plot(m,v,marker="o",color=RED,lw=3); b.text(2.05,v[-1],"South 55",color=RED,va="center",fontsize=9,fontweight="bold")
    else:
        b.plot(m,v,marker="o",color=GREY,lw=1.5); b.text(2.05,v[-1],f"{k} {v[-1]}",color="#666",va="center",fontsize=9)
b.annotate("Jan to Mar: -25 lakh",xy=(1,60),xytext=(0.15,88),color=RED,fontsize=9,arrowprops=dict(arrowstyle="->",color=RED))
b.set_xlim(-0.2,2.7); b.set_ylim(0,140); b.set_ylabel("lakh rupees per month",fontsize=8); clean(b)
b.set_title("South sales fell 31% in two months",fontsize=10,fontweight="bold",loc="left")
b.text(0.5,0.04,"AFTER: title is the message, one highlight,\ndirect labels, zero baseline",transform=b.transAxes,ha="center",fontsize=8,color=TEAL)
fig.tight_layout(); fig.savefig("ch05d_before_after.png")
