
<h2 id="s21-14">21.14 Cross-Library Integration</h2>
<p>Real projects pass data between libraries. Most integration bugs are one of three kinds: <strong>dtype</strong> (float64 versus float32, int32 versus int64), <strong>memory sharing</strong> (a view changes the original), and <strong>location</strong> (CPU versus GPU, or a tracked tensor versus plain NumPy). The table is the handoff cheat sheet.</p>
<div class="tablewrap"><table class="data"><thead><tr><th>From to</th><th>How</th><th>Watch out for</th></tr></thead><tbody>
<tr><td>pandas to PyTorch</td><td><code>torch.tensor(df[cols].to_numpy(dtype="float32"))</code></td><td>Mixed or string columns give object arrays; encode first. Missing values become NaN and poison the loss</td></tr>
<tr><td>NumPy to PyTorch</td><td><code>torch.from_numpy(arr)</code> (shares memory) or <code>torch.tensor(arr)</code> (copies)</td><td>float64 stays float64; the model's weights are float32, so cast with <code>.float()</code></td></tr>
<tr><td>PyTorch to NumPy</td><td><code>t.detach().cpu().numpy()</code></td><td>The result shares memory with the tensor on the CPU</td></tr>
<tr><td>PyTorch to scikit-learn metrics</td><td>Convert predictions and labels to NumPy first</td><td>Pass class ids (argmax), not logits, to accuracy</td></tr>
<tr><td>scikit-learn to PyTorch</td><td>Fit scalers and encoders on train; save them with <code>joblib</code>; apply at inference</td><td>Training-time and serving-time preprocessing must match exactly</td></tr>
<tr><td>Hugging Face dataset to pandas</td><td><code>ds.to_pandas()</code>, back with <code>Dataset.from_pandas(df)</code></td><td>Index columns, categorical dtypes, and the new pandas string dtype</td></tr>
<tr><td>Embeddings to FAISS</td><td><code>np.ascontiguousarray(E, dtype="float32")</code></td><td>Dimension fixed at index creation; normalise if you use inner product</td></tr>
<tr><td>Embeddings to Chroma</td><td><code>E.tolist()</code> or let Chroma embed</td><td>Different embedding function at query time than at ingest time</td></tr>
<tr><td>SDK reply to pandas</td><td>Validate to a dict or dataclass, then <code>pd.DataFrame(records)</code></td><td>Store the raw reply and the parsed fields so you can audit later</td></tr>
<tr><td>Config and secrets</td><td><code>yaml.safe_load</code> for settings, environment variables for keys</td><td>Never log keys; record the config with every run</td></tr>
</tbody></table></div>
<p class="problem"><span class="pl">Problem 21.14.1</span> Take a small DataFrame, build float32 features and integer labels ready for a PyTorch model, check memory sharing, evaluate with scikit-learn, and put the results back into pandas. (The model is a logistic regression, standing in for the network.)</p>
%%PY
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

df = pd.DataFrame({
    "text": ["refund my charge", "charged twice", "invoice is wrong", "refund the payment",
             "app crashes", "error on save", "page is broken", "login fails with error"],
    "label": ["billing", "billing", "billing", "billing", "bug", "bug", "bug", "bug"],
})
print("text dtype:", df["text"].dtype, "| label dtype:", df["label"].dtype)

cat = pd.Categorical(df["label"])
y = cat.codes.astype(np.int64)                        # class ids: int64 is what PyTorch's CrossEntropy wants
X = TfidfVectorizer().fit_transform(df["text"]).toarray().astype(np.float32)
X = np.ascontiguousarray(X)
print("X:", X.shape, X.dtype, "| y:", y.dtype, "| classes:", list(cat.categories))

view = X[:2]
print("slice shares memory (torch.from_numpy would too):", np.shares_memory(X, view))

clf = LogisticRegression(max_iter=200).fit(X, y)
pred = clf.predict(X)
print("accuracy:", accuracy_score(y, pred))

out = df.assign(pred=cat.categories[pred], correct=(pred == y))     # a NEW frame (pandas 3 copy-on-write)
subset = out[out["label"] == "bug"]
subset.loc[subset.index[0], "pred"] = "changed"                      # touches only the subset
print("original untouched:", out.loc[4, "pred"] != "changed", "| rows:", len(out), "columns:", list(out.columns))
%%END
<ol><li>In pandas 3 the text column has the string dtype (printed <code>str</code>); the label column too. The model needs numbers, so labels become integer category codes and text becomes a float matrix.</li><li>The label ids are <code>int64</code> because PyTorch's cross-entropy needs <code>long</code> class ids. Features are cast to <code>float32</code>, the dtype of model weights: <code>float64</code> input to a <code>float32</code> layer raises a dtype error.</li><li><code>np.ascontiguousarray</code> guarantees a plain C-ordered block, which <code>torch.from_numpy</code> and FAISS both prefer.</li><li>Slicing shares memory (<code>True</code>), as with <code>from_numpy</code>: changing the tensor changes the array. Use <code>.copy()</code> or <code>torch.tensor</code> if you need independence.</li><li>The scikit-learn metric takes plain integer arrays. With a PyTorch model you would first call <code>logits.argmax(-1).cpu().numpy()</code>.</li><li><code>df.assign</code> returns a new frame. Under pandas 3 copy-on-write, writing into <code>subset</code> never changes <code>out</code>; the final check prints <code>True</code>. The old chained-assignment bugs ("SettingWithCopy") are gone.</li></ol>
<h3>Talking to a model server over HTTP with httpx</h3>
<p>Underneath every SDK is an HTTP call. Knowing the raw form helps when you debug, use a self-hosted model server, or need to see headers. Here a local server plays a rate-limited LLM endpoint: the first request gets a 429 with <code>Retry-After</code>, the second succeeds. The client obeys the header. (Local only; no external network.)</p>
%%PY
import json, threading, time
import httpx
from http.server import BaseHTTPRequestHandler, HTTPServer

state = {"calls": 0}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        state["calls"] += 1
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        if state["calls"] == 1:
            self.send_response(429); self.send_header("Retry-After", "0.05"); self.end_headers(); return
        reply = json.dumps({"text": body["prompt"].upper(), "usage": {"input_tokens": 3, "output_tokens": 3}}).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(reply))); self.end_headers(); self.wfile.write(reply)
    def log_message(self, *a): pass

srv = HTTPServer(("127.0.0.1", 0), Handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{srv.server_address[1]}/v1/complete"

def post_with_retry(client, url, payload, max_retries=3):
    for attempt in range(max_retries + 1):
        r = client.post(url, json=payload, headers={"Authorization": "Bearer demo-key"})
        if r.status_code == 429 and attempt < max_retries:
            time.sleep(float(r.headers.get("Retry-After", 1)))
            continue
        r.raise_for_status()                      # 4xx/5xx other than a retried 429 raise here
        return r.json()

with httpx.Client(timeout=5.0) as client:
    data = post_with_retry(client, url, {"prompt": "hello llm"})
print(data["text"], "| usage:", data["usage"], "| server saw", state["calls"], "requests")
srv.shutdown()
%%END
<ol><li>The server handler counts requests: the first answer is <code>429</code> with a <code>Retry-After</code> header, later ones are JSON. The server is started in a thread on port 0 so the operating system picks a free port.</li><li><code>post_with_retry</code> sends the JSON body and an <code>Authorization</code> header. If the status is 429 and retries remain, it sleeps for the number of seconds in <code>Retry-After</code> and loops.</li><li><code>raise_for_status()</code> turns any other error status into an exception, so a 400 is never mistaken for data (httpx, like requests, does not raise by itself).</li><li>The output shows the uppercased text, the usage numbers and that the server saw two requests: one refused, one served. This is exactly what an SDK's built-in retry does for you.</li></ol>

<h2 id="s21-15">21.15 How to Solve Any Deep Learning and GenAI Libraries Problem</h2>
<h3>The decision flow</h3>
<ol><li><strong>Name the symptom exactly</strong>: error text, wrong number, slow, too big, or unreliable output. Copy the last line of the error, not the whole traceback.</li><li><strong>Shrink the problem</strong>: one batch, ten rows, one prompt, CPU only, a fixed seed. Most bugs reproduce on tiny input, and tiny input runs in seconds.</li><li><strong>Print the facts</strong>: shapes, dtypes, devices, min/max/NaN counts, the actual prompt sent, the raw reply received.</li><li><strong>Test the pipeline in pieces</strong>: data to batch, batch to loss, loss to gradient, gradient to update. Find the first stage whose output is wrong.</li><li><strong>Compare against a trivial baseline</strong> (majority class, keyword rule, random). If the fancy model barely beats it, suspect the data or the labels before the architecture.</li><li><strong>Change one thing at a time</strong> and record the result.</li></ol>
<div class="tablewrap"><table class="data"><thead><tr><th>Symptom</th><th>First check</th><th>Usual cause</th><th>Fix</th></tr></thead><tbody>
<tr><td>Loss does not go down</td><td>Overfit 8 examples</td><td>No step, wrong labels, lr too small, frozen layers, gradients not zeroed</td><td>Pattern 1</td></tr>
<tr><td>Loss is NaN or inf</td><td>First step it appears; input NaNs</td><td>lr too high, log of zero, bad data, float16 overflow</td><td>Pattern 2</td></tr>
<tr><td>Shape or device error</td><td>Print shapes and devices</td><td>Wrong flatten, batch-first mix-up, tensor left on CPU</td><td>21.6, 21.13</td></tr>
<tr><td>Out of memory</td><td>Do the arithmetic (21.5)</td><td>Batch, sequence length, no <code>no_grad</code>, stored graphs</td><td>Pattern 4</td></tr>
<tr><td>Search results are poor</td><td>Print top-5 for 10 queries and read them</td><td>Bad chunks, mismatched embedder, no normalisation</td><td>Pattern 5</td></tr>
<tr><td>LLM output unreliable</td><td>Print the exact prompt and raw reply</td><td>Vague instruction, no schema, no validation</td><td>Pattern 6</td></tr>
<tr><td>Too slow</td><td>Time data versus compute</td><td>Loading, padding, tiny batches, many calls</td><td>Pattern 7</td></tr>
<tr><td>Results differ between runs</td><td>Fix all seeds</td><td>Unseeded shuffle, dropout in eval, nondeterministic kernels</td><td>Recipe 10</td></tr>
</tbody></table></div>
<h3>Pattern 1: the loss does not decrease. Overfit one small batch.</h3>
<p>A correct training pipeline can memorise 8 examples. If it cannot, the bug is in the code, not in the data size or the architecture. Below, the correct loop reaches almost zero loss, and a loop with one wrong sign (updating <em>up</em> the gradient) does not.</p>
%%PY
import numpy as np

def make_data():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(8, 4))
    y = np.array([0, 1, 0, 1, 1, 0, 1, 0])
    return X, y, rng

def train(sign, steps=300, lr=0.5):
    X, y, rng = make_data()
    W1, b1 = rng.normal(scale=0.5, size=(4, 16)), np.zeros(16)
    W2, b2 = rng.normal(scale=0.5, size=(16, 2)), np.zeros(2)
    losses = []
    for _ in range(steps):
        h = np.maximum(X @ W1 + b1, 0)
        z = h @ W2 + b2
        z -= z.max(1, keepdims=True)
        p = np.exp(z); p /= p.sum(1, keepdims=True)
        losses.append(-np.log(p[np.arange(8), y]).mean())
        g = p.copy(); g[np.arange(8), y] -= 1; g /= 8
        gW2, gb2 = h.T @ g, g.sum(0)
        gh = (g @ W2.T) * (h > 0)
        gW1, gb1 = X.T @ gh, gh.sum(0)
        W1 -= sign * lr * gW1; b1 -= sign * lr * gb1
        W2 -= sign * lr * gW2; b2 -= sign * lr * gb2
    return losses

good, bad = train(+1), train(-1)
print("correct update: loss", round(good[0], 3), "->", f"{good[-1]:.4f}")
print("sign bug      : loss", round(bad[0], 3), "->", round(bad[-1], 3))
%%END
<ol><li>Eight points with random labels cannot be fitted by a straight line, but a 16-unit hidden layer has enough capacity to memorise them.</li><li>The correct run starts near log 2 = 0.69 (chance for two classes) and falls close to zero. The buggy run climbs the loss surface instead: the loss grows until it overflows to <code>inf</code>.</li><li>This test costs seconds and splits the world in two: if the tiny batch cannot be fitted, look at the loop (step, zero_grad, labels, learning rate, frozen parameters); if it can, look at data quality, capacity, regularisation and learning-rate schedule.</li><li>In PyTorch the same test is: take one batch, <code>for _ in range(200): train_step(batch)</code>, and expect the loss near zero.</li></ol>
<h3>Pattern 2: NaN or infinite loss. Find the first bad step.</h3>
<p>Do not stare at the final NaN; find the step where the loss first stops being finite, and the quantity that exploded just before it. Then test the two classic fixes: a lower learning rate and gradient clipping.</p>
%%PY
import numpy as np

def run(lr, clip=None, steps=400):
    x = 3.0                                              # minimise 50 * x^2, gradient 100 * x
    for step in range(1, steps + 1):
        g = 100 * x
        if clip is not None and abs(g) > clip:
            g = clip * np.sign(g)                        # clip the gradient
        x = x - lr * g
        if not np.isfinite(50 * x * x):
            return f"loss not finite at step {step}"
    return f"finished, x = {x:.4f}"

with np.errstate(all="ignore"):
    print("lr 0.05           :", run(0.05))
    print("lr 0.05 + clip 5  :", run(0.05, clip=5.0))
    print("lr 0.005          :", run(0.005))
%%END
<ol><li>The curvature is 100, so the stable range is lr below 2/100 = 0.02. At 0.05 each step multiplies x by 1 - 0.05 x 100 = -4, so x grows fourfold per step until the number overflows; the function reports the step.</li><li>With clipping the step length is capped (here to 0.05 x 5 = 0.25), so x walks in at a bounded speed and settles at zero.</li><li>Lowering the learning rate to 0.005 gives a contraction factor 0.5 per step: smooth convergence.</li><li>In real training add the same detective work with <code>torch.isfinite(loss)</code> checks, <code>torch.autograd.set_detect_anomaly(True)</code> (slow, for debugging only), and logging of the gradient norm.</li></ol>
<h3>Pattern 3: shape and device errors</h3>
<p>Solved example: the matmul error <code>mat1 and mat2 shapes cannot be multiplied (32x10 and 20x5)</code>. Read it as batch 32, 10 features coming in, a layer that expects 20. The fix is either the layer (<code>nn.Linear(10, 5)</code>) or the data pipeline that should produce 20 features. Use the <code>check</code> helper of 21.6 at the top of <code>forward</code>.</p>
<h3>Pattern 4: out of memory</h3>
<p>Solved example: a 1.3-billion-parameter model fully fine-tuned in fp32 with Adam needs 1.3e9 x 16 = 20.8 GB before activations, so it cannot fit a 16 GB card at any batch size. The ladder of fixes, cheapest first: <code>inference_mode</code> for evaluation; halve the batch and use gradient accumulation; bfloat16 autocast; gradient checkpointing; shorter sequences; 8-bit or paged optimisers; LoRA (21.7); a smaller model.</p>
<h3>Pattern 5: poor retrieval. Measure, do not guess.</h3>
<p>Write 10 to 30 real queries with the topic they should hit, then compute hit rates for each variant. Below, three embedding variants are compared on the 24-ticket corpus by <em>precision@3</em>: the share of the top-3 results coming from the expected topic.</p>
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
topic = np.array(["billing"] * 8 + ["bug"] * 8 + ["how-to"] * 8)
queries = [("my card was billed two times", "billing"), ("give me my money back", "billing"),
           ("receipt for payment", "billing"), ("the mobile app keeps crashing", "bug"),
           ("error when saving", "bug"), ("page freezes", "bug"),
           ("how can I export my data", "how-to"), ("where is the api key", "how-to"),
           ("how do I invite someone", "how-to")]

def precision_at_3(embed):
    E = embed.fit_transform(docs)
    hits = 0
    for q, t in queries:
        s = E @ embed.transform([q])[0] if not hasattr(E, "toarray") else (E @ embed.transform([q]).T).toarray().ravel()
        top = np.argsort(-s)[:3]
        hits += (topic[top] == t).sum()
    return hits / (3 * len(queries))

variants = {
    "tf-idf words only": make_pipeline(TfidfVectorizer(), Normalizer()),
    "tf-idf + SVD 2 dims": make_pipeline(TfidfVectorizer(), TruncatedSVD(2, random_state=0), Normalizer()),
    "tf-idf + SVD 8 dims": make_pipeline(TfidfVectorizer(), TruncatedSVD(8, random_state=0), Normalizer()),
}
for name, v in variants.items():
    print(f"{name:22s} precision@3 = {precision_at_3(v):.3f}")
%%END
<ol><li>The nine queries use different words from the documents on purpose ("billed two times" versus "charged twice", "money back" versus "refund"), which is where lexical matching struggles and real embedding models help.</li><li>Precision@3 counts how many of the three results come from the expected topic, averaged over queries. It is crude but it turns an argument ("it feels worse") into a number.</li><li>The three rows compare variants under the same test. In this run plain words and the 2-dimension compression both score 0.741, while 8 dimensions reach 0.889: enough dimensions let the SVD merge words that co-occur (billed, charged, payment) without discarding too much. With only 9 queries a difference of one or two hits is noise, so treat the numbers as a demonstration of the method, not a verdict.</li><li>The same loop is how you will choose between embedding models, chunk sizes and values of k in a real system.</li></ol>
<h3>Pattern 6: unreliable LLM output</h3>
<p>Solved example: the model sometimes replies with prose before the JSON. Fixes in order: state the exact schema and one example in the prompt; use the provider's structured output feature; set temperature low for extraction; validate every reply (21.9); retry with the error message at most twice; log failures and add them to the evaluation set. Measure the <em>valid-JSON rate</em> and <em>field accuracy</em> before and after each change.</p>
<h3>Pattern 7: too slow. Time each stage.</h3>
%%PY
import time
import numpy as np

class Timer:
    def __init__(self): self.t = {}
    def stage(self, name):
        timer = self
        class Ctx:
            def __enter__(s): s.t0 = time.perf_counter()
            def __exit__(s, *a): timer.t[name] = timer.t.get(name, 0) + time.perf_counter() - s.t0
        return Ctx()

texts = ["support ticket number %d about billing and refunds" % i for i in range(3000)]
W = np.random.default_rng(0).normal(size=(64, 64)).astype(np.float32)
tm = Timer()
for start in range(0, 3000, 100):
    with tm.stage("data"):                         # python-level tokenising and hashing per item
        batch = np.array([[hash((w, j)) % 97 for j, w in enumerate(t.split())] + [0] * 56 for t in texts[start:start + 100]],
                         dtype=np.float32)[:, :64]
    with tm.stage("compute"):
        out = batch @ W
slowest = max(tm.t, key=tm.t.get)
print("stages measured:", sorted(tm.t))
print("the slower stage in this run is:", slowest)
%%END
<ol><li>A tiny <code>Timer</code> accumulates the time spent in named stages using <code>perf_counter</code>.</li><li>The data stage builds each batch with Python loops and the compute stage is one matrix product, so the data stage dominates here. That mirrors a common real situation: the model is fast, the pipeline around it is slow.</li><li>Only after you know which stage dominates should you optimise (more workers and pre-tokenised data when data dominates; mixed precision and bigger batches when compute dominates). For GPU code remember that kernels run asynchronously: call <code>torch.cuda.synchronize()</code> before reading the clock, or use the built-in profiler.</li></ol>
<h3>How to verify and how to debug</h3>
<ul><li><strong>Verify numerically</strong>: finite-difference gradient checks for custom layers, tiny known inputs with hand-computed outputs, and shape assertions.</li><li><strong>Verify behaviourally</strong>: overfit one batch; compare with a trivial baseline; check that train loss falls, validation loss behaves, and the confusion matrix makes sense.</li><li><strong>Verify the data</strong>: print ten random examples with labels and read them; check class counts, duplicates between splits, and the longest items.</li><li><strong>Debug by bisection</strong>: halve the pipeline until you find the first stage with a wrong output. Print the real prompt and reply for any LLM step.</li><li><strong>Keep a log</strong> of config, seed, library versions and metrics for every run; a result you cannot reproduce is an anecdote.</li></ul>

<h2 id="s21-16">21.16 Going Deeper: Internals, Memory, Speed and What Interviewers Probe</h2>
<h3>Autograd internals</h3>
<p>Every tensor produced by a tracked operation carries a <code>grad_fn</code> pointing to a node that knows how to compute the vector-Jacobian product for that operation, and to the nodes of its inputs. Nodes save whatever the backward formula needs (for a product, the other factor). Each tensor has a version counter; an in-place edit bumps it, and backward compares the saved version to the current one, which is where the "modified by an inplace operation" error comes from. <code>backward()</code> frees the saved buffers unless <code>retain_graph=True</code>. The reason for reverse mode is cost: for one scalar loss and millions of parameters, reverse mode computes all gradients in a few times the cost of one forward pass; forward mode would need one pass per parameter.</p>
<h3>Where the memory goes</h3>
<p>Activations saved for backward scale with batch x sequence length x width x depth, and attention scores add batch x heads x T x T per layer unless a fused attention kernel is used. Gradient checkpointing stores only some activations and recomputes the rest, trading roughly one extra forward pass for a large memory saving. The CUDA caching allocator keeps freed blocks for reuse, so <code>nvidia-smi</code> shows more than <code>memory_allocated()</code>; fragmentation can cause an out-of-memory error even when total free memory looks sufficient. Text generation adds the <strong>KV cache</strong>: keys and values of all past tokens per layer, so its size grows linearly with context length and batch size.</p>
<h3>Where the time goes</h3>
<p>Large matrix multiplications are efficient on GPUs; many small operations are not, because each launch has overhead. Hence larger batches, fused operations, <code>torch.compile</code>, fused attention kernels, and bfloat16 (half the memory traffic). Padding wastes compute (recipe 5). In data loading, avoid doing string work per item inside the training loop. For LLM APIs the cost is tokens: shorten prompts, cache stable prefixes, batch offline jobs, and use a smaller model for easy cases.</p>
<h3>How generation samples a token</h3>
<p>A language model outputs a logit for every vocabulary entry. <strong>Temperature</strong> divides logits (lower means sharper, higher means flatter); <strong>top-k</strong> keeps only the k largest; <strong>top-p</strong> keeps the smallest set of tokens whose probability sums to at least p. Then one token is sampled, appended, and the model runs again.</p>
%%PY
import numpy as np

def probs_from_logits(logits, temperature=1.0, top_k=None, top_p=None):
    z = np.asarray(logits, dtype=float) / temperature
    p = np.exp(z - z.max()); p /= p.sum()
    if top_k is not None:
        cutoff = np.sort(p)[-top_k]
        p = np.where(p >= cutoff, p, 0.0)
    if top_p is not None:
        order = np.argsort(-p)
        cum = np.cumsum(p[order])
        keep = order[: np.searchsorted(cum, top_p) + 1]      # smallest prefix reaching top_p
        mask = np.zeros_like(p); mask[keep] = 1
        p = p * mask
    return p / p.sum()

logits = [4.0, 3.0, 2.0, 1.0, 0.0]
for name, kw in [("T=1", {}), ("T=0.5 (sharper)", {"temperature": 0.5}), ("T=2 (flatter)", {"temperature": 2.0}),
                 ("top_k=2", {"top_k": 2}), ("top_p=0.9", {"top_p": 0.9})]:
    print(f"{name:16s}", np.round(probs_from_logits(logits, **kw), 3))

rng = np.random.default_rng(0)
draws = rng.choice(5, size=1000, p=probs_from_logits(logits, top_k=2))
print("top_k=2 draws only use tokens:", sorted(set(draws.tolist())))
%%END
<ol><li>At T = 1 the probabilities are the plain softmax: the top token gets about 0.64. Halving the temperature sharpens the distribution (top token about 0.87); doubling it flattens it.</li><li>Top-k 2 zeroes everything but the two largest tokens and renormalises them to roughly 0.73 and 0.27.</li><li>Top-p 0.9 keeps the smallest prefix of tokens (sorted by probability) whose cumulative probability reaches 0.9, here the top three tokens, then renormalises.</li><li>Sampling 1000 tokens with top-k 2 only ever produces tokens 0 and 1. Temperature 0 (greedy) is the limit of ever lower temperatures: always the argmax. Greedy is deterministic, but it is not a guarantee of identical output across hardware or service versions.</li></ol>
<h3>Vector search internals</h3>
<p>Flat search costs N x d multiplications per query. IVF reduces the number of vectors compared (21.8). HNSW builds a layered neighbour graph and walks it greedily; it is accurate and fast but memory-heavy. Product quantisation (PQ) compresses each vector into a few bytes by coding sub-vectors with small codebooks: for 1 million vectors of 768 float32 numbers the raw size is 1e6 x 768 x 4 = 3.07 GB, while with 96 one-byte codes per vector it is 96 MB. Compression loses accuracy, so measure recall.</p>
<h3>What interviewers probe</h3>
<ul><li>Explain backpropagation on a two-layer network and why gradients accumulate in <code>.grad</code>.</li><li>What do <code>model.eval()</code> and <code>torch.no_grad()</code> each do? Why do you usually need both?</li><li>Estimate the memory to fine-tune a 7B model with Adam and name three ways to reduce it.</li><li>Why does cross-entropy take logits? Write the stable log-softmax.</li><li>What is the difference between <code>view</code> and <code>reshape</code>; <code>detach</code> and <code>no_grad</code>?</li><li>Why bfloat16 over float16? What is a GradScaler for?</li><li>How does LoRA work and what do <code>r</code> and <code>alpha</code> control?</li><li>Design a RAG system: chunking, embedding, index, retrieval metrics, failure modes, evaluation.</li><li>How would you make an LLM call reliable and cheap at 1 million requests a day?</li><li>How do you know your prompt change helped? (Golden set, baseline, paired comparison, confidence interval, leakage.)</li></ul>
