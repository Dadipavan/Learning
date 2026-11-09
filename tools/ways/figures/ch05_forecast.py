import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
sys.path.insert(0,'/Users/c2487352/Personal/Career/final/study/ways/data'); import prep, numpy as np, pandas as pd
o,c,p=prep.load_clean('/Users/c2487352/Personal/Career/final/study/ways/data/')
y=o.groupby('order_date').size().astype(float)
H=28; tr,te=y.iloc[:-H],y.iloc[-H:]
f={}
f['naive']=np.repeat(tr.iloc[-1],H)
f['seasonal naive (7)']=np.tile(tr.iloc[-7:].values,4)
f['moving average 7']=np.repeat(tr.iloc[-7:].mean(),H)
def ses(x,a):
    l=x[0]
    for v in x[1:]: l=a*v+(1-a)*l
    return l
def sse(a):
    l=tr.iloc[0]; e=0
    for v in tr.iloc[1:]:
        e+=(v-l)**2; l=a*v+(1-a)*l
    return e
alphas=np.linspace(.05,.95,19); a=alphas[np.argmin([sse(x) for x in alphas])]
f['exp. smoothing']=np.repeat(ses(tr.values,a),H)
def design(idx,t0):
    t=np.arange(len(idx))+t0
    X=np.column_stack([np.ones(len(idx)),t]+[(idx.dayofweek==d).astype(float) for d in range(1,7)])
    return X
X=design(tr.index,0); b=np.linalg.lstsq(X,tr.values,rcond=None)[0]
f['linear trend + weekday']=design(te.index,len(tr))@b
t90=tr.iloc[-90:]; X9=design(t90.index,0); b9=np.linalg.lstsq(X9,t90.values,rcond=None)[0]
f['same, last 90 days']=design(te.index,90)@b9

def design2(idx,t0):
    X=design(idx,t0); promo=((idx.month==11)&(idx.day>=20)&(idx.day<=30)).astype(float)
    return np.column_stack([X,promo])
fig,ax=plt.subplots(figsize=(9,4.4))
ax.plot(y.index[-70:],y.values[-70:],color="#12182b",lw=1.6,label="actual daily orders")
cols={"naive":"#aa2d26","moving average 7":"#b84a22","exp. smoothing":"#6a2fd0","linear trend + weekday":"#357a70","seasonal naive (7)":"#2b4fd6"}
for k,cc in cols.items(): ax.plot(te.index,f[k],color=cc,lw=1.3,ls="--",label=k)
ax.axvline(te.index[0],color="grey",lw=1); ax.text(te.index[0],ax.get_ylim()[1]*0.95," hold-out starts",fontsize=8,va="top")
ax.set_ylabel("orders per day"); ax.legend(fontsize=7,ncol=2,frameon=False); ax.set_title("Five forecasts against the same 28-day hold-out")
ax.spines[["top","right"]].set_visible(False); fig.tight_layout(); fig.savefig("ch05_forecast.png",dpi=110)
