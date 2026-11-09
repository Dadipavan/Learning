// Usage: node tools/test_search.js   (loads assets/search-index.js + ranking block from index.html)
const fs = require("fs"), vm = require("vm"), path = require("path");
const root = path.join(__dirname, "..");
const win = {}; const ctx = vm.createContext({ window: win });
vm.runInContext(fs.readFileSync(path.join(root, "assets/search-index.js"), "utf8"), ctx);
const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
const a = html.indexOf("/*SEARCH-RANK*/"), b = html.indexOf("/*END-SEARCH-RANK*/");
vm.runInContext(html.slice(a, b), ctx);
const docs = {}; win.SEARCH_DOCS.forEach(d => docs[d.k] = d.d);
console.log("records:", win.SEARCH_INDEX.length);
const qs = process.argv.slice(2).length ? process.argv.slice(2) : ["eigenvalues", "window functions", "gradient descent", "STAR", "PCA", "backpropagation", "cross entropy", "negotiation"];
for (const q of qs) {
  const t0 = Date.now();
  const res = vm.runInContext("sqSearch(window.SEARCH_INDEX," + JSON.stringify(q) + ",'all')", ctx);
  console.log("\n> " + q + "  (" + res.length + " hits, " + (Date.now() - t0) + " ms)");
  res.slice(0, 3).forEach(x => console.log("  " + x.s + "  [" + x.r.k + "] " + x.r.h.slice(0, 70) + "  -> " + x.r.u));
}
