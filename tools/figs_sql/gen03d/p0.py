import sys; sys.path.insert(0,"/Users/c2487352/Personal/Career/final/tools/figs_sql")
from _kit import *
db=shop()
X=lambda c: exec_sql(db,c)
def ERR(code):
    """show sql that fails and the real error message"""
    try:
        db.execute(code); msg="(no error)"
    except Exception as ex: msg="Error: "+str(ex)
    return sql(code)+"\n"+text(msg)
def insert_before(anchor_re, key, body):
    path=ROOT+"ch03.html"; s=open(path).read()
    a,b="<!-- gen:%s -->"%key,"<!-- /gen:%s -->"%key
    blk=a+"\n"+body.strip()+"\n"+b+"\n"
    if a in s: s=re.sub(re.escape(a)+".*?"+re.escape(b)+"\n",lambda m:blk,s,flags=re.S)
    else:
        m=list(re.finditer(anchor_re,s)); assert len(m)==1,(key,len(m)); s=s[:m[0].start()]+blk+s[m[0].start():]
    open(path,"w").write(s); print("inserted",key,len(re.sub(r"<[^>]+>"," ",body).split()),"words")
RECAP=r'<h2 id="s\d+-chapter-recap">'
PROMPT=r'<h2 id="s\d+-prompt-pack">'
def ins(key,body): insert_before(RECAP,key,body)
