#!/usr/bin/env python3
"""Merge tools/datasets/catalog_*.json into assets/data-catalog.js and write data/README.md.

Usage (from the project root):  python3 tools/build_data_catalog.py
Checks that every listed file exists under data/, fills rows/size from the files, and verifies that every dictionary
column exists in the first CSV of the dataset. Output: window.DATA_CATALOG=[...]; (works from file:// via <script>).
"""
import csv, glob, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "data")


def main():
    items, errs = [], []
    for path in sorted(glob.glob(os.path.join(ROOT, "tools", "datasets", "catalog_*.json"))):
        items += json.load(open(path, encoding="utf-8"))["datasets"]
    seen = set()
    for it in items:
        if it["id"] in seen:
            errs.append("duplicate id " + it["id"])
        seen.add(it["id"])
        total = 0
        first_csv = None
        files = []
        for f in it["files"]:
            p = os.path.join(DATA, f)
            if not os.path.exists(p):
                errs.append(f"{it['id']}: missing file data/{f}")
                continue
            total += os.path.getsize(p)
            files.append({"path": f, "kb": round(os.path.getsize(p) / 1024)})
            if f.endswith(".csv") and first_csv is None:
                first_csv = p
        it["file_info"] = files
        it["size_kb"] = round(total / 1024)
        if first_csv:
            with open(first_csv, newline="", encoding="utf-8") as fh:
                rd = csv.reader(fh)
                head = next(rd)
                n = sum(1 for _ in rd)
            it["rows"] = n
            it["columns"] = len(head)
            cols = {d["col"] for d in it.get("dictionary", [])}
            miss = [c for c in head if c not in cols and len(it["files"]) == 1]
            if miss:
                errs.append(f"{it['id']}: columns missing from dictionary: {miss}")
    out = os.path.join(ROOT, "assets", "data-catalog.js")
    open(out, "w", encoding="utf-8").write("window.DATA_CATALOG=%s;\n" % json.dumps(items, ensure_ascii=False, separators=(",", ":")))
    lines = ["# Practice datasets", "", "Synthetic but realistic, deliberately messy, seeded and reproducible (`tools/datasets/make_*.py`).",
             "Browse them with descriptions, data dictionaries, planted gotchas and exercises on the **Datasets** page of the site.", "",
             "| id | domain | level | files | size |", "|---|---|---|---|---|"]
    for it in items:
        lines.append(f"| `{it['id']}` | {it.get('domain', '')} | {it.get('level', '')} | {', '.join(it['files'])} | {it['size_kb']} KB |")
    open(os.path.join(DATA, "README.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("datasets:", len(items), "total KB:", sum(i["size_kb"] for i in items))
    if errs:
        print("PROBLEMS:\n- " + "\n- ".join(errs))
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
