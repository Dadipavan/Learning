import numpy as np
from common import *
crit=["Headline and summary","Bullets with numbers","Keyword match","Layout and ATS","Honest scope"]
before=[2,1,2,2,3]; after=[4,4,4,5,5]
print(sum(before),sum(after),sum(after)-sum(before))
fig,ax=plt.subplots(figsize=(8,4),dpi=110)
y=np.arange(len(crit)); h=0.38
ax.barh(y+h/2,before,h,color=GREY,label=f"Before (total {sum(before)}/25)")
ax.barh(y-h/2,after,h,color=BLUE,label=f"After (total {sum(after)}/25)")
ax.set_yticks(y); ax.set_yticklabels(crit); ax.invert_yaxis(); ax.set_xlim(0,5.5); ax.set_xlabel("score (1 to 5)"); clean(ax)
ax.legend(frameon=False,loc="lower right")
fig.tight_layout(); fig.savefig("ch16_resume_scores.png")
