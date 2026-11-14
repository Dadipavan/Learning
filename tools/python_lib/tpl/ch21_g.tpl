
<h2 id="s21-8">21.8 Embeddings and Vector Search: sentence-transformers, FAISS and Chroma</h2>
<div class="callout blue"><div class="lab">INTUITION</div><div class="txt">An embedding model turns a sentence into a point in space, say 384 numbers, so that sentences with similar meaning land near each other. "Charged twice" and "double payment" share no words, yet their points are close. Vector search then answers "which stored points are nearest to this query point?". FAISS is a very fast calculator for that question. Chroma wraps the calculator in a small database that also stores the original text and labels (metadata) and can filter on them.</div></div>
<h3>Reference: embedding and search tools</h3>
<div class="tablewrap"><table class="data"><thead><tr><th>Name</th><th>What it does in plain English</th><th>Minimal example (not run here)</th></tr></thead><tbody>
<tr><td><code>SentenceTransformer(name)</code></td><td>Load an embedding model</td><td><code>m = SentenceTransformer(name)</code></td></tr>
<tr><td><code>m.encode(texts)</code></td><td>Texts to a NumPy matrix (N, dim)</td><td><code>m.encode(docs, batch_size=64)</code></td></tr>
<tr><td><code>normalize_embeddings=True</code></td><td>Unit length vectors: inner product equals cosine</td><td><code>m.encode(docs, normalize_embeddings=True)</code></td></tr>
<tr><td><code>m.get_sentence_embedding_dimension()</code></td><td>The vector size</td><td>use it to build the index</td></tr>
<tr><td><code>m.max_seq_length</code></td><td>Tokens beyond this are silently cut</td><td><code>m.max_seq_length = 256</code></td></tr>
<tr><td><code>util.cos_sim</code></td><td>Cosine similarity matrix of two sets</td><td><code>util.cos_sim(q, docs)</code></td></tr>
<tr><td><code>util.semantic_search</code></td><td>Top-k hits per query (small corpora)</td><td><code>util.semantic_search(q, docs, top_k=5)</code></td></tr>
<tr><td><code>faiss.IndexFlatL2(d)</code></td><td>Exact search by squared Euclidean distance</td><td><code>index = faiss.IndexFlatL2(384)</code></td></tr>
<tr><td><code>faiss.IndexFlatIP(d)</code></td><td>Exact search by inner product</td><td><code>faiss.IndexFlatIP(384)</code></td></tr>
<tr><td><code>faiss.normalize_L2(x)</code></td><td>Normalise rows in place (cosine via IP)</td><td><code>faiss.normalize_L2(x)</code></td></tr>
<tr><td><code>index.add(x)</code></td><td>Store vectors (float32, C-contiguous)</td><td><code>index.add(x.astype("float32"))</code></td></tr>
<tr><td><code>index.search(q, k)</code></td><td>Returns scores <code>D</code> and positions <code>I</code></td><td><code>D, I = index.search(q, 5)</code></td></tr>
<tr><td><code>index.ntotal</code></td><td>Number of stored vectors</td><td><code>assert index.ntotal == len(docs)</code></td></tr>
<tr><td><code>faiss.IndexIVFFlat</code></td><td>Cluster first, search only nearby clusters</td><td><code>IndexIVFFlat(quant, d, nlist)</code></td></tr>
<tr><td><code>index.train(x)</code></td><td>Learn the clusters (IVF and PQ need it)</td><td><code>index.train(x)</code></td></tr>
<tr><td><code>index.nprobe</code></td><td>How many clusters to visit per query</td><td><code>index.nprobe = 8</code></td></tr>
<tr><td><code>faiss.IndexHNSWFlat</code></td><td>Graph index: fast and accurate, more memory</td><td><code>IndexHNSWFlat(d, 32)</code></td></tr>
<tr><td><code>faiss.IndexIDMap</code></td><td>Attach your own integer ids</td><td><code>IndexIDMap(IndexFlatIP(d))</code></td></tr>
<tr><td><code>faiss.write_index / read_index</code></td><td>Save and load an index file</td><td><code>faiss.write_index(index, "t.faiss")</code></td></tr>
<tr><td><code>chromadb.PersistentClient</code></td><td>A Chroma database on disk</td><td><code>PersistentClient(path="chroma_db")</code></td></tr>
<tr><td><code>client.get_or_create_collection</code></td><td>A named table of documents</td><td><code>..., metadata={"hnsw:space": "cosine"}</code></td></tr>
<tr><td><code>collection.add / upsert</code></td><td>Store ids, documents, metadata, embeddings</td><td><code>col.upsert(ids=ids, documents=docs, metadatas=meta)</code></td></tr>
<tr><td><code>collection.query</code></td><td>Nearest documents with optional filters</td><td><code>col.query(query_texts=["..."], n_results=3, where={"product": "mobile"})</code></td></tr>
<tr><td><code>collection.get / delete / count</code></td><td>Fetch by id or filter, remove, size</td><td><code>col.get(where={"label": "bug"})</code></td></tr>
</tbody></table></div>
<p>Typical idiomatic use of the real libraries together (not run here):</p>
%%NORUN
import numpy as np
from sentence_transformers import SentenceTransformer, util
import faiss, chromadb

docs = ["I was charged twice for my subscription", "app crashes on the settings page", "how do I reset my password"]
model = SentenceTransformer("your-embedding-model-id")
emb = model.encode(docs, normalize_embeddings=True).astype("float32")      # (3, dim)

# exact search with FAISS: with unit vectors, inner product == cosine similarity
index = faiss.IndexFlatIP(emb.shape[1])
index.add(emb)
q = model.encode(["double payment on my card"], normalize_embeddings=True).astype("float32")
D, I = index.search(q, 2)                      # D: (1, 2) scores, I: (1, 2) row positions
print([docs[i] for i in I[0]], D[0])

# approximate search for big corpora
nlist = 1024
quantizer = faiss.IndexFlatIP(emb.shape[1])
ivf = faiss.IndexIVFFlat(quantizer, emb.shape[1], nlist, faiss.METRIC_INNER_PRODUCT)
ivf.train(big_matrix)                           # needs at least ~39 x nlist training vectors
ivf.add(big_matrix)
ivf.nprobe = 16
faiss.write_index(ivf, "tickets.faiss")

# Chroma: embeddings + text + metadata + filtering
client = chromadb.PersistentClient(path="chroma_db")
col = client.get_or_create_collection("tickets", metadata={"hnsw:space": "cosine"})
col.upsert(ids=["t1", "t2", "t3"], documents=docs, embeddings=emb.tolist(),
           metadatas=[{"label": "billing"}, {"label": "bug"}, {"label": "how-to"}])
res = col.query(query_embeddings=q.tolist(), n_results=2, where={"label": "billing"})
print(res["documents"][0], res["distances"][0])      # distance = 1 - cosine for the cosine space
%%END
<h3>Worked example: semantic search with a stand-in embedder</h3>
<p>A real sentence-transformer needs a model download. The stand-in below uses TF-IDF (weights each word by how rare it is across documents) followed by a truncated SVD (compresses to a few dimensions that capture words that appear together, called latent semantic analysis). The result has the same shape and use as real embeddings: a dense matrix (N, dim) of unit-length rows. It matches vocabulary and co-occurrence, not true paraphrase, which is the main thing a real model adds.</p>
<p class="problem"><span class="pl">Problem 21.8.1</span> Embed 24 support tickets into 8 dimensions, normalise, and retrieve the 3 nearest tickets to three queries by cosine similarity. Then show that for unit vectors the inner product ranking equals the Euclidean ranking.</p>
%%PY
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline

docs = [
 "I was charged twice for my monthly subscription", "please refund the duplicate payment on my invoice",
 "my invoice shows the wrong billing amount", "how do I update the credit card used for payment",
 "the discount code was not applied to my invoice", "I want a refund for the annual plan I never used",
 "payment failed but my card was charged", "need a receipt for last month payment",
 "the app crashes when I open the settings page", "login button does nothing on the mobile app",
 "error 500 appears when I save my profile", "the export freezes and the page never loads",
 "dark mode breaks the layout of the dashboard", "the mobile app crashes after the latest update",
 "search returns an error instead of results", "upload stops at ninety percent and shows an error",
 "how do I reset my password", "where can I find my api key in the dashboard",
 "how to export my data as a csv file", "how can I invite a teammate to my workspace",
 "how do I change the language of the app", "how do I enable two factor login",
 "how to connect the dashboard to my database", "how can I delete my account and data",
]
topic = ["billing"] * 8 + ["bug"] * 8 + ["how-to"] * 8

embedder = make_pipeline(TfidfVectorizer(sublinear_tf=True),
                         TruncatedSVD(n_components=8, random_state=0),
                         Normalizer())
E = embedder.fit_transform(docs).astype("float32")
print("embedding matrix:", E.shape, E.dtype, "row norms ~1:", np.allclose(np.linalg.norm(E, axis=1), 1, atol=1e-5))

def search(query, k=3):
    q = embedder.transform([query]).astype("float32")
    scores = (E @ q.T).ravel()                    # cosine, because rows are unit length
    top = np.argsort(-scores)[:k]
    return [(int(i), topic[i], round(float(scores[i]), 3)) for i in top]

for query in ["refund my payment", "the app crashes", "how can I export data"]:
    print(f"{query!r:26s}", search(query))

q = embedder.transform(["refund my payment"]).astype("float32")[0]
by_ip = np.argsort(-(E @ q))
by_l2 = np.argsort(((E - q) ** 2).sum(1))
print("same ranking by inner product and by L2:", np.array_equal(by_ip, by_l2))
%%END
<ol><li>The pipeline chains three steps, exactly as you would chain tokeniser, model and normalisation. <code>fit_transform</code> learns the vocabulary and the 8 directions from the 24 tickets.</li><li>The <code>Normalizer</code> makes every row length 1. The printed check confirms the norms are close to 1. This is what <code>normalize_embeddings=True</code> does in sentence-transformers.</li><li><code>search</code> embeds the query with the <em>same fitted pipeline</em> (never refit on the query) and multiplies the matrix by the query vector. For unit vectors, the dot product is the cosine similarity. <code>argsort(-scores)</code> ranks highest first.</li><li>Each query returns tuples of (document position, true topic, score). In this run all three hits of each query come from the expected topic: billing, bug and how-to. A score near 1 means almost the same direction. We left <code>stop_words</code> off on purpose: with only 24 tiny documents, removing common words such as "app" and "how" changed the neighbours for the worse in our trials, a reminder that every preprocessing choice must be checked on your own data.</li><li>The last check explains why <code>IndexFlatL2</code> and <code>IndexFlatIP</code> give the same ranking on normalised vectors: ||a - b||<sup>2</sup> = 2 - 2 (a . b), so a smaller distance means a bigger inner product.</li></ol>
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Wrong:</strong> embedding documents with one model and queries with another, or refitting the vectoriser on the query. <strong>Symptom:</strong> results look random, scores are tiny, or you get a shape error. <strong>Fix:</strong> one model and one normalisation for both sides; store the model name next to the index. Some retrieval models also want a prefix such as "query:" or "passage:", so read the model card.</div></div>
<h3>A FAISS-style index, built to learn the API</h3>
<p>FAISS has a small API: <code>add</code> to store, <code>search</code> to query, results as two matrices <code>(D, I)</code> of scores and positions. When fewer than <code>k</code> vectors exist, the missing slots are filled with <code>-1</code>. This class mimics that contract in NumPy so you can see exactly what you get back.</p>
%%PY
import numpy as np

class FlatIndex:
    """NumPy imitation of faiss.IndexFlatIP / IndexFlatL2."""
    def __init__(self, d, metric="ip"):
        self.d, self.metric = d, metric
        self.x = np.zeros((0, d), dtype=np.float32)
    @property
    def ntotal(self):
        return len(self.x)
    def add(self, x):
        assert x.dtype == np.float32 and x.ndim == 2 and x.shape[1] == self.d, "need float32 (n, d)"
        self.x = np.vstack([self.x, x])
    def search(self, q, k):
        assert q.dtype == np.float32 and q.shape[1] == self.d
        if self.metric == "ip":
            scores = q @ self.x.T
            order = np.argsort(-scores, axis=1)[:, :k]
        else:
            scores = (q ** 2).sum(1)[:, None] - 2 * q @ self.x.T + (self.x ** 2).sum(1)[None, :]
            order = np.argsort(scores, axis=1)[:, :k]
        D = np.take_along_axis(scores, order, 1)
        I = order.copy()
        if k > self.ntotal:                                   # FAISS pads with -1
            pad = k - self.ntotal
            D = np.hstack([D, np.full((len(q), pad), np.nan, dtype=np.float32)])
            I = np.hstack([I, np.full((len(q), pad), -1)])
        return D.astype(np.float32), I

rng = np.random.default_rng(0)
x = rng.normal(size=(100, 16)).astype(np.float32)
x /= np.linalg.norm(x, axis=1, keepdims=True)
q = x[:2] + 0.05 * rng.normal(size=(2, 16)).astype(np.float32)
q /= np.linalg.norm(q, axis=1, keepdims=True)

ip, l2 = FlatIndex(16, "ip"), FlatIndex(16, "l2")
ip.add(x); l2.add(x)
D, I = ip.search(q, 3)
print("positions:", I.tolist())
print("scores   :", np.round(D.astype(float), 3).tolist())
print("L2 gives the same positions:", np.array_equal(I, l2.search(q, 3)[1]))

small = FlatIndex(16); small.add(x[:2])
print("k larger than ntotal:", small.search(q[:1], 4)[1].tolist())

try:
    ip.add(x.astype(np.float64))
except AssertionError as e:
    print("dtype guard:", e)
%%END
<ol><li>The two internal formulas are the whole difference between metrics. Inner product ranks by largest score; squared L2 expands (q - x)<sup>2</sup> into <code>q.q - 2 q.x + x.x</code> and ranks by smallest.</li><li>Queries are slightly noisy copies of the first two stored vectors, so the nearest position for query 0 is 0 and for query 1 is 1. The first column of the printed positions shows exactly that.</li><li>The scores are cosine values close to 1 for the true neighbour and much smaller for the rest.</li><li>The L2 index returns the same positions, as the algebra from the previous example predicts for unit vectors.</li><li>When only two vectors exist, asking for four gives two real hits and two <code>-1</code> placeholders. Code that does <code>docs[i]</code> with <code>i = -1</code> silently picks the <em>last</em> document in Python, a nasty bug. Always filter <code>I &gt;= 0</code>.</li><li>FAISS requires <code>float32</code>. NumPy defaults to <code>float64</code>, so <code>x.astype("float32")</code> is the line you will write most often; the guard here shows the kind of error you get without it.</li></ol>
<h3>Approximate search: IVF and the recall/speed trade-off</h3>
<p>Exact search compares the query with every vector, costing time proportional to N. An <strong>IVF</strong> (inverted file) index first clusters the vectors into <code>nlist</code> groups with k-means. At query time it ranks the cluster centres, visits only the <code>nprobe</code> closest groups and compares with the vectors inside. This trades a little accuracy for a lot of speed. The accuracy is measured as <strong>recall@k</strong>: of the true k nearest neighbours, how many did we find?</p>
<p class="problem"><span class="pl">Problem 21.8.2</span> Build an IVF index with 64 lists over 20,000 vectors in 32 dimensions. Measure recall@10 and the share of vectors scanned for different <code>nprobe</code> values on two data sets: strongly clustered data (like real embeddings, which have topics) and structureless Gaussian noise (the hard case).</p>
%%PY
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

def exact_topk(base, Q, k):
    d = (Q ** 2).sum(1)[:, None] - 2 * Q @ base.T + (base ** 2).sum(1)[None, :]
    idx = np.argpartition(d, k, axis=1)[:, :k]
    order = np.take_along_axis(d, idx, 1).argsort(1)
    return np.take_along_axis(idx, order, 1)

def ivf_curve(X, nlist=64, k=10, probes=(1, 2, 4, 8, 16, 32, 64)):
    base, Q = X[:20000], X[20000:20200]
    truth = exact_topk(base, Q, k)
    km = KMeans(n_clusters=nlist, n_init=1, random_state=0).fit(base)       # index.train
    lists = [np.where(km.labels_ == c)[0] for c in range(nlist)]               # index.add
    cent = km.cluster_centers_.astype(np.float32)
    out = []
    for nprobe in probes:
        rec, scanned = 0.0, 0
        for q, t in zip(Q, truth):
            probe = np.argsort(((cent - q) ** 2).sum(1))[:nprobe]
            cand = np.concatenate([lists[c] for c in probe])
            best = cand[np.argsort(((base[cand] - q) ** 2).sum(1))[:k]]
            rec += len(set(best) & set(t)) / k
            scanned += len(cand)
        out.append((nprobe, rec / len(Q), scanned / len(Q) / len(base)))
    return out

blobs, _ = make_blobs(n_samples=20200, n_features=32, centers=40, cluster_std=6.0, random_state=0)
noise = np.random.default_rng(0).normal(size=(20200, 32))
print("nprobe | clustered recall, scanned | gaussian recall, scanned")
for (p, r1, s1), (_, r2, s2) in zip(ivf_curve(blobs.astype(np.float32)), ivf_curve(noise.astype(np.float32))):
    print(f"{p:6d} | {r1:15.3f} {s1:9.3f} | {r2:15.3f} {s2:9.3f}")
%%END
<ol><li><code>exact_topk</code> is the ground truth (what <code>IndexFlat</code> would return). We need it to <em>measure</em> the approximation; never trust an approximate index without comparing with exact search on a sample.</li><li><code>ivf_curve</code> performs the three real stages: training (k-means on the vectors), adding (store the member list of each cluster), and searching (rank centres, concatenate the chosen lists, rank the candidates).</li><li>On the clustered data, visiting only 4 lists (about 6.5 percent of vectors) already recovers about 99 percent of the true neighbours; this is the situation FAISS is designed for.</li><li>On pure noise there is no cluster structure to exploit: with 8 probes (12.5 percent scanned) recall is only about 0.6, and you need to scan roughly half the data to get above 0.9. The lesson is that the benefit of IVF depends on data structure, so tune <code>nprobe</code> on your own embeddings.</li><li>The last row (<code>nprobe</code> = <code>nlist</code>) scans everything and has recall 1.0 by construction: it is exact search plus overhead.</li></ol>
<figure><img src="images/lib21_ivf_recall.png" alt="Recall at 10 against share of vectors scanned for IVF on clustered data and on Gaussian noise" loading="lazy"/><figcaption>Figure 21.7. Recall at 10 versus the share of vectors scanned. Clustered data reaches high recall after scanning a few percent; structureless noise needs far more.</figcaption></figure>
<p><strong>How to read it:</strong> the horizontal axis is the work done (share of the data compared), the vertical axis is the quality (recall). A curve that rises steeply and early is a good fit for an IVF index. The dashed diagonal is a baseline for a random sample: scanning a fraction f of the data at random finds a fraction f of the neighbours.</p>
<h3>A Chroma-style collection: documents, metadata and filters</h3>
<p>Chroma stores the vector, the original text and a metadata dictionary under a string id. Its two special features are <code>where</code> filters on metadata and persistence. The class below imitates the interface, built on our embedder, so you can see how filtering and the result layout work. (Chroma returns <em>lists of lists</em>, one inner list per query.)</p>
%%PY
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline

class Collection:
    def __init__(self, embedder):
        self.embedder, self.ids, self.docs, self.meta, self.E = embedder, [], [], [], None
    def add(self, ids, documents, metadatas):
        dup = set(ids) & set(self.ids)
        if dup:
            raise ValueError(f"duplicate ids: {sorted(dup)}")       # Chroma add() rejects existing ids
        self.ids += ids; self.docs += documents; self.meta += metadatas
        self.E = self.embedder.transform(self.docs)
    def query(self, query_texts, n_results=3, where=None):
        q = self.embedder.transform(query_texts)
        keep = [i for i, m in enumerate(self.meta) if not where or all(m.get(k) == v for k, v in where.items())]
        out = {"ids": [], "documents": [], "distances": []}
        for row in q:
            dist = 1 - self.E[keep] @ row                           # cosine distance, smaller is closer
            top = np.argsort(dist)[:n_results]
            out["ids"].append([self.ids[keep[j]] for j in top])
            out["documents"].append([self.docs[keep[j]] for j in top])
            out["distances"].append([round(float(dist[j]), 3) for j in top])
        return out
    def count(self):
        return len(self.ids)

docs = ["refund the duplicate payment", "charged twice this month", "app crashes on the settings page",
        "mobile login button does nothing", "how do I reset my password", "where is my api key",
        "mobile app crashes after update", "web dashboard layout is broken"]
meta = [{"label": "billing", "platform": "web"}, {"label": "billing", "platform": "web"},
        {"label": "bug", "platform": "mobile"}, {"label": "bug", "platform": "mobile"},
        {"label": "how-to", "platform": "web"}, {"label": "how-to", "platform": "web"},
        {"label": "bug", "platform": "mobile"}, {"label": "bug", "platform": "web"}]
embedder = make_pipeline(TfidfVectorizer(stop_words="english"), TruncatedSVD(n_components=5, random_state=0), Normalizer())
embedder.fit(docs)

col = Collection(embedder)
col.add([f"t{i}" for i in range(8)], docs, meta)
print("count:", col.count())
res = col.query(["the app keeps crashing"], n_results=2)
print(res["ids"], res["distances"])
res = col.query(["the app keeps crashing"], n_results=2, where={"platform": "web"})
print("filtered to web:", res["ids"], res["documents"])
try:
    col.add(["t0"], ["again"], [{"label": "bug", "platform": "web"}])
except ValueError as e:
    print("add twice:", e)
%%END
<ol><li><code>Collection.add</code> rejects ids that already exist, as Chroma's <code>add</code> does. The fix in real code is <code>upsert</code>, which inserts new ids and replaces existing ones, making re-runs of an ingestion job safe.</li><li><code>query</code> first builds <code>keep</code>, the list of rows whose metadata matches <code>where</code>, then ranks only those. This is <em>pre-filtering</em>. Retrieving the top k and filtering afterwards (post-filtering) can return fewer than k results, or none, if the filter is selective.</li><li>The distance is <code>1 - cosine</code>, the convention of Chroma's cosine space: 0 is identical, 1 is unrelated (orthogonal).</li><li>Results are lists of lists: <code>res["ids"][0]</code> belongs to the first query. Forgetting the <code>[0]</code> is the most common beginner bug with Chroma.</li><li>The unfiltered crash query returns mobile bug tickets; with <code>where={"platform": "web"}</code> the answer switches to the best <em>web</em> ticket, even though it is a weaker match. A filter changes the answer, not just the speed.</li></ol>
<div class="callout cream"><div class="lab">REAL JOB</div><div class="txt">For a retrieval-augmented generation (RAG) system, quality problems are usually in <strong>chunking</strong> (documents cut into pieces of a few hundred tokens, usually with a little overlap), not in the index. Store the source id and chunk position in the metadata, so you can show citations and so re-ingesting a changed file replaces its old chunks. Measure with a small labelled set (see 21.10).</div></div>
