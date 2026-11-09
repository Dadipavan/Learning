#!/usr/bin/env python3
"""Build one study document (chapter pages, index, appendix, full.html, .docx, .pdf)
from HTML fragments, in the same layout as the other study/<key>/ documents.

Usage:  python3 -I tools/build_doc.py tools/math/doc.json [--no-pdf]

Source layout (next to doc.json):
  src/index_body.html   front matter shown under the tiles on the index page (h2 sections)
  src/chNN.html         chapter body: intro paragraphs, then <h2> sections (no banner/TOC/pager)
  src/appendix.html     appendix body (h2 sections)
  figures/*.py          optional matplotlib scripts, run with cwd = study/<key>/images
"""
import json, os, re, sys, html, zipfile, subprocess, shutil, tempfile
from xml.sax.saxutils import escape as xesc

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
COLORS = ["#2b4fd6", "#6a2fd0", "#357a70", "#b84a22", "#aa2d26", "#b02d5e"]
APPX_COLOR = "#12182b"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def slug(t):
    t = re.sub(r"<[^>]+>", "", html.unescape(t)).lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:70]


def words(h):
    return len(re.sub(r"<[^>]+>", " ", h).split())


def add_ids(body):
    """Give every <h2> an id (sN-slug) and return (body, [(id, text)])."""
    toc, n = [], [0]

    def rep(m):
        n[0] += 1
        text = re.sub(r"<[^>]+>", "", m.group(2))
        i = f"s{n[0]}-{slug(text)}"
        toc.append((i, m.group(2)))
        return f'<h2 id="{i}">{m.group(2)}</h2>'

    return re.sub(r"<h2([^>]*)>(.*?)</h2>", rep, body, flags=re.S), toc


def head(title, depth="../../"):
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{title}</title><link rel="stylesheet" href="{depth}assets/study.css"></head>')


def topbar(label):
    return (f'<div class="topbar"><div class="in"><a href="../../index.html#/study">← Study library</a><a href="index.html">Contents</a>'
            f'<span class="doc">{label}</span><span class="sp"></span><a href="../../index.html#/home">Tracker</a></div></div>')


def tiles(cfg, chapters):
    out = []
    for c in chapters:
        out.append(f'<a href="{c["page"]}" data-tile="{c["readid"]}" style="background:{c["color"]}"><b>{c["label"]}<i></i></b>{c["title"]}</a>')
    return '<div class="tiles">' + "".join(out) + "</div>"


def build(cfg_path, make_pdf=True):
    cfg = json.load(open(cfg_path))
    base = os.path.dirname(os.path.abspath(cfg_path))
    key = cfg["key"]
    out = os.path.join(ROOT, "study", key)
    os.makedirs(os.path.join(out, "images"), exist_ok=True)

    # 1. figures
    fig_dir = os.path.join(base, "figures")
    if os.path.isdir(fig_dir):
        for f in sorted(os.listdir(fig_dir)):
            if f.endswith(".py"):
                r = subprocess.run([sys.executable, os.path.join(fig_dir, f)], cwd=os.path.join(out, "images"),
                                   capture_output=True, text=True)
                if r.returncode:
                    print("FIGURE FAIL", f, r.stderr[-500:])

    # 2. chapters
    chapters = []
    for i, ch in enumerate(cfg["chapters"], 1):
        num = ch["num"]
        src = open(os.path.join(base, "src", f"ch{num:02d}.html")).read()
        body, toc = add_ids(src)
        chapters.append(dict(num=num, title=ch["title"], sub=ch["sub"], label=f"CHAPTER {num}",
                             page=f"ch{num:02d}.html", color=COLORS[(num - 1) % 6], readid=f"study:{key}:ch{num:02d}",
                             body=body, toc=toc, words=words(src)))
    app = None
    ap = os.path.join(base, "src", "appendix.html")
    if os.path.exists(ap):
        src = open(ap).read()
        body, toc = add_ids(src)
        app = dict(num=99, title=cfg["appendix_title"], sub=cfg["appendix_sub"], label="APPENDIX", page="appendix.html",
                   color=APPX_COLOR, readid=f"study:{key}:appendix", body=body, toc=toc, words=words(src))
    allp = chapters + ([app] if app else [])

    for i, c in enumerate(allp):
        prev = allp[i - 1] if i else None
        nxt = allp[i + 1] if i + 1 < len(allp) else None
        tocs = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in c["toc"])
        pager = ('<div class="pager">' +
                 (f'<a class="btn ghost" href="{prev["page"]}">← {prev["label"].title() if prev["label"]!="APPENDIX" else "Appendix"}: {prev["title"]}</a>' if prev else
                  '<a class="btn ghost" href="index.html">← Contents</a>') +
                 (f'<a class="btn" href="{nxt["page"]}">{nxt["label"].title()}: {nxt["title"]} →</a>' if nxt else '<span></span>') + "</div>")
        c["html"] = (head(f'{c["label"].title()}: {c["title"]}') + f'<body style="--accent:{c["color"]}">' + topbar(cfg["label"]) +
                     f'<div class="page"><div class="banner"><div class="eyebrow">{c["label"]}</div><h1>{c["title"]}</h1><p>{c["sub"]}</p></div>'
                     f'<details class="toc" open><summary>In this chapter</summary><ol>{tocs}</ol></details>'
                     f'{c["body"]}<div class="readbtn"><button class="btn" data-read="{c["readid"]}">Mark this chapter as read</button></div>'
                     f'{pager}</div><script src="../../assets/study.js"></script></body></html>')
        open(os.path.join(out, c["page"]), "w").write(c["html"])

    # 3. index
    ib = open(os.path.join(base, "src", "index_body.html")).read()
    ib, _ = add_ids(ib)
    cover = (f'<div class="cover"><div class="eyebrow">Study guide</div><h1>{cfg["title"]}</h1><hr/><p class="sub">{cfg["subtitle"]}</p>'
             f'<p class="tag">{cfg["tagline"]}</p></div>')
    ids = json.dumps([c["readid"] for c in allp])
    actions = (f'<div class="actions"><a class="btn" href="ch01.html">Start Chapter 1 →</a>'
               f'<a class="btn ghost" href="full.html">Read everything on one page (print or Save as PDF)</a>'
               f'<a class="btn ghost" href="{key}.docx" download>Download .docx</a>'
               f'<a class="btn ghost" href="{key}.pdf" download>Download .pdf</a>'
               f'<span style="align-self:center;color:#5a6580" id="readprog" data-ids=\'{ids}\'></span></div>')
    index_html = (head(cfg["title"]) + f'<body style="--accent:{COLORS[0]}">' + topbar(cfg["label"]) + '<div class="page">' + cover +
                  tiles(cfg, allp) + actions + ib + '</div><script src="../../assets/study.js"></script></body></html>')
    open(os.path.join(out, "index.html"), "w").write(index_html)

    # 4. full
    parts = [head(cfg["title"] + " (full)") + f'<body style="--accent:{COLORS[0]}">' + topbar(cfg["label"]) +
             '<div class="page"><div class="actions"><button class="btn" onclick="window.print()">Print or Save as PDF</button></div>' + cover + tiles(cfg, allp) + ib]
    for c in allp:
        parts.append(f'<section class="chapter" style="--accent:{c["color"]}"><div class="banner"><div class="eyebrow">{c["label"]}</div><h1>{c["title"]}</h1><p>{c["sub"]}</p></div>{c["body"]}</section>')
    parts.append('</div><script src="../../assets/study.js"></script></body></html>')
    full = "".join(parts)
    open(os.path.join(out, "full.html"), "w").write(full)

    # 5. docx + pdf
    to_docx(full, out, os.path.join(out, f"{key}.docx"), cfg)
    if make_pdf:
        to_pdf(os.path.join(out, "full.html"), os.path.join(out, f"{key}.pdf"))

    # 6. registry in index.html
    register(cfg, allp)
    tot = sum(c["words"] for c in allp)
    print(f"built {key}: {len(chapters)} chapters, appendix={bool(app)}, ~{tot} words")


def to_pdf(src, dst):
    if not os.path.exists(CHROME):
        print("Chrome not found; skipping PDF")
        return
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={dst}",
                        "file://" + src], capture_output=True, text=True, timeout=600)
    print("pdf:", "ok" if os.path.exists(dst) else "FAILED " + r.stderr[-300:])


def register(cfg, allp):
    p = os.path.join(ROOT, "index.html")
    h = open(p).read()
    chs = [dict(num=c["num"], title=c["title"], label=c["label"], page=c["page"], color=c["color"], words=c["words"], readid=c["readid"]) for c in allp]
    entry = dict(key=cfg["key"], label=cfg["label"], icon=cfg["icon"], areas=cfg["areas"], blurb=cfg["blurb"], status="ready",
                 chapters=chs, words=sum(c["words"] for c in allp), docx=f'study/{cfg["key"]}/{cfg["key"]}.docx',
                 pdf=f'study/{cfg["key"]}/{cfg["key"]}.pdf', title=cfg["title"], subtitle=cfg["subtitle"])
    js = json.dumps(entry, ensure_ascii=False)
    m = re.search(r'\{"key": "%s", "label"' % re.escape(cfg["key"]), h)
    if m:  # replace existing entry (find its end by brace matching)
        i, depth, j = m.start(), 0, m.start()
        instr = False
        while True:
            ch = h[j]
            if instr:
                if ch == "\\": j += 1
                elif ch == '"': instr = False
            else:
                if ch == '"': instr = True
                elif ch == "{": depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0: break
            j += 1
        h = h[:i] + js + h[j + 1:]
    else:
        i = h.find('"study": [') + len('"study": [')
        h = h[:i] + js + ", " + h[i:]
    if cfg.get("mathPdf"):
        h = re.sub(r'"mathPdf": "[^"]*"', '"mathPdf": "%s"' % cfg["mathPdf"], h)
    open(p, "w").write(h)


# ---------------------------------------------------------------- docx
def to_docx(full_html, out_dir, dst, cfg):
    from bs4 import BeautifulSoup, NavigableString
    try:
        from PIL import Image
    except Exception:
        Image = None
    soup = BeautifulSoup(full_html, "html.parser")
    page = soup.find("div", class_="page")
    body, rels, media = [], [], []

    def run(text, b=False, i=False, code=False, sup=False, sub=False, color=None):
        if not text:
            return ""
        pr = ""
        if b: pr += "<w:b/>"
        if i: pr += "<w:i/>"
        if code: pr += '<w:rFonts w:ascii="Menlo" w:hAnsi="Menlo" w:cs="Menlo"/><w:sz w:val="19"/>'
        if color: pr += f'<w:color w:val="{color}"/>'
        if sup: pr += '<w:vertAlign w:val="superscript"/>'
        if sub: pr += '<w:vertAlign w:val="subscript"/>'
        return f'<w:r><w:rPr>{pr}</w:rPr><w:t xml:space="preserve">{xesc(text)}</w:t></w:r>'

    def inline(node, st=None):
        st = dict(st or {})
        out = ""
        for ch in node.children:
            if isinstance(ch, NavigableString):
                out += run(str(ch).replace("\n", " "), **st)
            elif ch.name in ("strong", "b"):
                out += inline(ch, {**st, "b": True})
            elif ch.name in ("em", "i"):
                out += inline(ch, {**st, "i": True})
            elif ch.name == "code":
                out += inline(ch, {**st, "code": True})
            elif ch.name == "sup":
                out += inline(ch, {**st, "sup": True})
            elif ch.name == "sub":
                out += inline(ch, {**st, "sub": True})
            elif ch.name == "br":
                out += "<w:r><w:br/></w:r>"
            elif ch.name in ("button",):
                pass
            else:
                out += inline(ch, st)
        return out

    def para(runs, style=None, shade=None, ind=None, keep=False):
        pp = ""
        if style: pp += f'<w:pStyle w:val="{style}"/>'
        if keep: pp += "<w:keepNext/>"
        if shade: pp += f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>'
        if ind: pp += f'<w:ind w:left="{ind}"/>'
        return f"<w:p><w:pPr>{pp}</w:pPr>{runs}</w:p>"

    def image(img):
        src = img.get("src", "")
        path = os.path.join(out_dir, src)
        if not (Image and os.path.exists(path) and src.lower().endswith((".png", ".jpg", ".jpeg"))):
            return ""
        w, h = Image.open(path).size
        cx = 5800000
        cy = int(cx * h / w)
        n = len(media) + 1
        media.append((f"image{n}.png", path))
        rid = f"rIdImg{n}"
        rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image{n}.png"/>')
        return (f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
                f'<wp:docPr id="{n}" name="Picture {n}"/><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
                f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="{n}" name="image{n}.png"/><pic:cNvPicPr/></pic:nvPicPr>'
                f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
                f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')

    def table(t):
        rows = ""
        for tr in t.find_all("tr"):
            cells = ""
            for td in tr.find_all(["td", "th"]):
                hd = td.name == "th"
                cells += (f'<w:tc><w:tcPr><w:tcW w:w="0" w:type="auto"/>' + ('<w:shd w:val="clear" w:color="auto" w:fill="E8ECF8"/>' if hd else "") +
                          f'</w:tcPr>{para(inline(td, {"b": hd}))}</w:tc>')
            rows += f"<w:tr>{cells}</w:tr>"
        b = '<w:tblBorders>' + "".join(f'<w:{s} w:val="single" w:sz="4" w:space="0" w:color="B8C0D8"/>' for s in ("top", "left", "bottom", "right", "insideH", "insideV")) + "</w:tblBorders>"
        return f'<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/>{b}</w:tblPr>{rows}</w:tbl>' + para("")

    def walk(el):
        for ch in el.children:
            if isinstance(ch, NavigableString):
                continue
            n, cl = ch.name, ch.get("class", [])
            if n in ("script", "button", "details") or "actions" in cl or "readbtn" in cl or "pager" in cl or "tiles" in cl:
                continue
            if n == "div" and "banner" in cl:
                body.append(para(run(ch.find("div", class_="eyebrow").get_text(), b=True, color="6A7390"), keep=True))
                body.append(para(run(ch.find("h1").get_text()), "Heading1"))
                continue
            if n == "div" and "cover" in cl:
                body.append(para(run(ch.find("h1").get_text()), "Title"))
                for p in ch.find_all("p"):
                    body.append(para(run(p.get_text(), i=True)))
                continue
            if n in ("h1", "h2", "h3"):
                body.append(para(run(ch.get_text()), {"h1": "Heading1", "h2": "Heading2", "h3": "Heading3"}[n], keep=True))
            elif n == "p":
                if "problem" in cl:
                    body.append(para(inline(ch, {"b": False}), shade="FFF4D6"))
                else:
                    body.append(para(inline(ch)))
            elif n in ("ul", "ol"):
                for k, li in enumerate(ch.find_all("li", recursive=False), 1):
                    mark = "• " if n == "ul" else f"{k}. "
                    body.append(para(run(mark) + inline(li), ind=500))
            elif n == "pre":
                for line in ch.get_text().split("\n"):
                    body.append(para(run(line, code=True), shade="F2F4F9"))
                body.append(para(""))
            elif n == "table":
                body.append(table(ch))
            elif n == "figure":
                im = ch.find("img")
                if im: body.append(image(im))
                cap = ch.find("figcaption")
                if cap: body.append(para(run(cap.get_text(), i=True, color="5A6580")))
            elif n == "div" and "callout" in cl:
                lab = ch.find("div", class_="lab"); txt = ch.find("div", class_="txt")
                col = {"blue": "E6EEFB", "red": "FBE8E6", "green": "E4F4EA", "cream": "F7F1DF"}.get(next((c for c in cl if c != "callout"), ""), "EEEEEE")
                body.append(para((run((lab.get_text() + ": ") if lab else "", b=True) + inline(txt or ch)), shade=col))
            elif n == "div" and "prompt" in cl:
                pre = ch.find("pre")
                body.append(para(run("AI prompt: ", b=True) + run(pre.get_text() if pre else ""), shade="EDE9FB"))
            elif n == "div" and "eq" in cl:
                body.append(para(inline(ch), ind=700))
            elif n in ("div", "section"):
                walk(ch)
            else:
                t = ch.get_text(" ", strip=True)
                if t:
                    body.append(para(run(t)))

    walk(page)
    NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
          'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"')
    doc = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {NS}><w:body>' + "".join(body) +
           '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="567" w:footer="567" w:gutter="0"/></w:sectPr></w:body></w:document>')

    def sty(i, name, sz, bold=True, color="1F2A5C", before=240, after=80):
        return (f'<w:style w:type="paragraph" w:styleId="{i}"><w:name w:val="{name}"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>'
                f'<w:pPr><w:spacing w:before="{before}" w:after="{after}"/></w:pPr><w:rPr>{"<w:b/>" if bold else ""}<w:color w:val="{color}"/><w:sz w:val="{sz}"/></w:rPr></w:style>')
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
              '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:sz w:val="22"/></w:rPr></w:rPrDefault>'
              '<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
              '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>' +
              sty("Title", "Title", 52, before=0, after=200) + sty("Heading1", "heading 1", 40, before=480) +
              sty("Heading2", "heading 2", 30, color="2B4FD6") + sty("Heading3", "heading 3", 25, color="3A4668") + "</w:styles>")
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
          '<Default Extension="png" ContentType="image/png"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
          '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>')
    rels_root = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
    rels_doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rIdSty" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>' + "".join(rels) + "</Relationships>")
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels_root)
        z.writestr("word/document.xml", doc)
        z.writestr("word/styles.xml", styles)
        z.writestr("word/_rels/document.xml.rels", rels_doc)
        for name, path in media:
            z.write(path, "word/media/" + name)


if __name__ == "__main__":
    build(sys.argv[1], make_pdf="--no-pdf" not in sys.argv)
