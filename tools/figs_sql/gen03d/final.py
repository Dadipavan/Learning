import re,html
p="/Users/c2487352/Personal/Career/final/study/sql/ch03.html"
s=open(p).read()
# intro pointer (once)
tag="<!-- gen:intro -->"
if tag not in s:
    anchor='<code>order_items</code> (with <code>qty</code> and <code>unit_price</code>).</p>'
    assert anchor in s
    add=anchor+tag+'<div class="callout green"><div class="lab">HOW TO USE THIS CHAPTER</div><div class="txt">Sections 3.1 to 3.4 teach the four ideas once. Sections 3.5 to 3.9 deepen each idea with a glossary, more worked examples, figures and traps. Section 3.10 is a problem-solving playbook you can apply to any new question. Section 3.11 is the expert layer. Sections 3.12 and 3.13 are a drill and a self-test with a scoring guide. If aggregation feels fuzzy, read Section 3.5 first.</div></div><!-- /gen:intro -->'
    s=s.replace(anchor,add,1)
# renumber ids
heads=list(re.finditer(r'<h2 id="[^"]*">(.*?)</h2>',s))
out=[];last=0
for i,m in enumerate(heads,1):
    title=html.unescape(re.sub(r"<[^>]+>","",m.group(1)))
    slug=re.sub(r"[^a-z0-9]+","-",title.lower()).strip("-")
    out.append(s[last:m.start()]+'<h2 id="s%d-%s">%s</h2>'%(i,slug,m.group(1))); last=m.end()
out.append(s[last:]); s="".join(out)
# toc
heads=list(re.finditer(r'<h2 id="([^"]*)">(.*?)</h2>',s))
toc="".join('<li><a href="#%s">%s</a></li>'%(m.group(1),m.group(2)) for m in heads)
s=re.sub(r'(<details class="toc" open><summary>In this chapter</summary><ol>).*?(</ol></details>)',lambda m:m.group(1)+toc+m.group(2),s,count=1,flags=re.S)
open(p,"w").write(s)
print(len(heads),"h2")
