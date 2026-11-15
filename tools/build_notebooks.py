#!/usr/bin/env python3
"""Build one Jupyter/Colab notebook per chapter from the chapter pages.

Usage (project root):  python3 tools/build_notebooks.py [key ...]
Writes study/<key>/notebooks/chNN.ipynb and assets/notebooks.js (window.NOTEBOOKS manifest, rebuilt from disk).
Each Python block becomes a code cell with the expected output stored; `norun` blocks keep a "needs" comment."""
import glob, html, json, os, re, sys
import nbformat
from bs4 import BeautifulSoup
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook, new_output

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = "https://dadipavan.github.io/Learning/"
SETUP = '''# Setup: practice datasets live on the site. This helper loads one into a DataFrame.
import warnings; warnings.filterwarnings("ignore")
DATA_URL = "https://dadipavan.github.io/Learning/data/"
def load_dataset(name, table=None):
    import pandas as pd
    path = f"{name}.csv" if table is None else f"{name}/{table}.csv"
    return pd.read_csv(DATA_URL + path)
'''
WAYS_SETUP = '''# Setup: the files used in this chapter are downloaded next to the notebook.
import os, urllib.request
os.makedirs("data", exist_ok=True)
for f in ["customers.csv", "orders.csv", "products.csv", "shopkart.db"]:
    if not os.path.exists("data/" + f):
        urllib.request.urlretrieve("https://dadipavan.github.io/Learning/study/ways/data/" + f, "data/" + f)
'''
IMPORT_RE = re.compile(r"^\s*(?:from|import)\s+([A-Za-z_][\w]*)", re.M)


def md(el):
    """Very small HTML -> markdown for inline text."""
    out = []
    for c in el.children:
        if getattr(c, "name", None) is None:
            out.append(str(c))
        elif c.name == "code":
            out.append("`" + c.get_text() + "`")
        elif c.name in ("strong", "b"):
            out.append("**" + c.get_text() + "**")
        elif c.name in ("em", "i"):
            out.append("*" + c.get_text() + "*")
        elif c.name == "br":
            out.append("\n")
        else:
            out.append(c.get_text())
    return re.sub(r"[ \t]+", " ", "".join(out)).strip()


def build(key, page):
    soup = BeautifulSoup(open(page, encoding="utf-8").read(), "html.parser")
    title = soup.find("h1").get_text(strip=True)
    num = int(os.path.basename(page)[2:4])
    body = soup.find("div", class_="page")
    cells, ncode = [], 0
    cells.append(new_markdown_cell(f"# {title}\n\nNotebook for **Chapter {num}** of the *{key}* study document. "
                                   f"Run the cells top to bottom. Read the full explanation on the site: {SITE}study/{key}/ch{num:02d}.html\n\n"
                                   f"Tip: change a number, predict the output, then run the cell again."))
    pres = [p for p in body.find_all("pre", class_="code") if "lang-python" in p.get("class", [])]
    allcode = "\n".join(p.get_text() for p in pres)
    if key == "ways" and "data/" in allcode:
        cells.append(new_code_cell(WAYS_SETUP))
    elif "load_dataset(" in allcode and key != "python":
        cells.append(new_code_cell(SETUP))
    current_h2 = False
    for el in body.find_all(["h2", "pre"]):
        if el.name == "h2":
            nxt = el.find_next_sibling()
            text = f"## {el.get_text(strip=True)}"
            if nxt is not None and nxt.name == "p":
                text += "\n\n" + md(nxt)
            cells.append(new_markdown_cell(text))
            continue
        cls = el.get("class", [])
        if "lang-python" not in cls:
            continue
        code = html.unescape(el.get_text()).rstrip("\n")
        if "norun" in cls:
            mods = sorted({m for m in IMPORT_RE.findall(code)} - {"os", "sys", "re", "json", "math", "time", "random", "typing", "collections", "itertools", "functools", "pathlib", "datetime"})
            code = f"# needs a full environment: pip install {' '.join(mods[:6]) or 'the libraries used below'}\n" + code
        outputs = []
        nxt = el.find_next_sibling()
        if "norun" not in cls and nxt is not None and nxt.name == "pre" and "lang-text" in nxt.get("class", []):
            outputs = [new_output("stream", name="stdout", text=html.unescape(nxt.get_text()).rstrip("\n") + "\n")]
        cell = new_code_cell(code, outputs=outputs)
        if outputs and re.search(r"^\w*(Error|Exception)\b", outputs[0]["text"], re.M):
            cell.source = "# This cell is meant to fail: read the error message, that is the lesson.\n" + cell.source
            cell.metadata["tags"] = ["raises-exception"]
        cells.append(cell)
        ncode += 1
    cells.append(new_markdown_cell(f"---\nDone? Do the **Practice set** at the end of the chapter, then clear your Review cards on the site.\n\n{SITE}study/{key}/ch{num:02d}.html"))
    nb = new_notebook(cells=cells, metadata={"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                              "language_info": {"name": "python"}, "colab": {"provenance": []}})
    nbformat.validate(nb)
    return nb, len(cells), ncode


def main(keys):
    manifest = {}
    docs = sorted(d for d in os.listdir(os.path.join(ROOT, "study")) if os.path.isdir(os.path.join(ROOT, "study", d)))
    for key in docs:
        for page in sorted(glob.glob(os.path.join(ROOT, "study", key, "ch[0-9][0-9].html"))):
            name = os.path.basename(page)[:-5]
            out = os.path.join(ROOT, "study", key, "notebooks", name + ".ipynb")
            if not keys or key in keys:
                nb, cells, code = build(key, page)
                if code == 0:
                    if os.path.exists(out):
                        os.remove(out)
                    continue
                os.makedirs(os.path.dirname(out), exist_ok=True)
                nbformat.write(nb, out)
            if os.path.exists(out):
                nb = nbformat.read(out, as_version=4)
                manifest.setdefault(key, {})[name] = {"cells": len(nb.cells), "code": sum(1 for c in nb.cells if c.cell_type == "code")}
    open(os.path.join(ROOT, "assets", "notebooks.js"), "w").write("window.NOTEBOOKS=%s;\n" % json.dumps(manifest, separators=(",", ":")))
    print("notebooks:", sum(len(v) for v in manifest.values()), "docs:", len(manifest))


if __name__ == "__main__":
    main(sys.argv[1:])
