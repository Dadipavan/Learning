import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
BL,OR,TE,RE,PU,CR="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0","#f1e6c8"
plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
def box(ax,x,y,w,h,t,c,fs=9.5,tc=None):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.25",fc=c,ec="#222",lw=1.2))
    ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=fs,color=tc or ("black" if c==CR else "white"))
def arrow(ax,x1,y1,x2,y2,col="#222"): ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="->",lw=1.6,color=col))

fig,ax=plt.subplots(figsize=(8,4.2)); ax.set_xlim(0,100); ax.set_ylim(-4,50); ax.axis("off")
box(ax,38,42,24,5,"What does the question ask for?",CR,9.5)
cols=[(1,"A number","count params, memory,\noutput of a forward pass",BL,["P1 count params","P2 trace shapes","P3 forward pass"]),
(26,"Can it be done?","can this model represent\nthis pattern, and why not",TE,["P4 separable? build it","P5 perceptron trace"]),
(51,"Which choice?","activation, output layer,\nloss pairing",OR,["P6 pick activation","P7 stable softmax"]),
(76,"It is broken","not learning, NaN, flat\nloss, wrong accuracy",PU,["P8 gradient-flow diagnosis"])]
for x,h,sub,c,pats in cols:
    box(ax,x,28,21,8,f"{h}\n{sub}",c,8.5); arrow(ax,50,41,x+10.5,37.5)
    arrow(ax,x+10.5,27.2,x+10.5,25.6)
    for i,p in enumerate(pats):
        box(ax,x,20-i*8,21,4,p,CR,7.5)
        if i<len(pats)-1: arrow(ax,x+10.5,19.4-i*8,x+10.5,16.8-i*8)
ax.text(50,-2.5,"After any answer: check shapes, check a tiny case by hand, check with code",ha="center",fontsize=9.5,color=RE)
fig.tight_layout(); fig.savefig("ch01d_playbook.png",dpi=110)
