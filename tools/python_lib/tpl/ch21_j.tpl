
<h2 id="s21-11">21.11 Recipes: How Do I ...?</h2>
<p>Each recipe is a small, real task. Torch snippets are marked not run here; the ones with output are runnable stand-ins you can execute.</p>
<h3>Recipe 1: How do I freeze the pretrained body and train only a new head?</h3>
<p>Set <code>requires_grad_(False)</code> on the body and give the optimiser only the parameters that still require gradients (not run here):</p>
%%NORUN
for p in model.body.parameters():
    p.requires_grad_(False)
trainable = [p for p in model.parameters() if p.requires_grad]
print(sum(p.numel() for p in trainable), "trainable of", sum(p.numel() for p in model.parameters()))
opt = torch.optim.AdamW(trainable, lr=1e-3)
model.body.eval()          # also stop dropout / batch-norm updates inside the frozen part
%%END
<h3>Recipe 2: How do I use a smaller learning rate for the pretrained body than for the new head?</h3>
<p>Pass parameter groups (not run here). Typical: 10 to 100 times smaller for pretrained layers.</p>
%%NORUN
opt = torch.optim.AdamW([
    {"params": model.encoder.parameters(), "lr": 2e-5},
    {"params": model.classifier.parameters(), "lr": 1e-3},
], weight_decay=0.01)
%%END
<h3>Recipe 3: How do I resume training after a crash?</h3>
<p>Save the model, the optimiser <em>and</em> the scheduler plus the epoch; restore all of them (not run here):</p>
%%NORUN
torch.save({"model": model.state_dict(), "opt": opt.state_dict(),
            "sched": sched.state_dict(), "epoch": epoch}, "last.pt")

ck = torch.load("last.pt", map_location=device, weights_only=True)
model.load_state_dict(ck["model"]); opt.load_state_dict(ck["opt"]); sched.load_state_dict(ck["sched"])
start_epoch = ck["epoch"] + 1
%%END
<h3>Recipe 4: How do I handle imbalanced classes?</h3>
<p>Weight the loss by inverse class frequency (or oversample). The weights below follow the common rule weight = N / (K x count).</p>
%%PY
import numpy as np

y = np.array([0] * 90 + [1] * 8 + [2] * 2)           # 90 billing, 8 bug, 2 outage
counts = np.bincount(y)
weights = len(y) / (len(counts) * counts)
print("counts :", counts)
print("weights:", np.round(weights, 3))

def weighted_ce(logits, y, w):
    z = logits - logits.max(1, keepdims=True)
    logp = z - np.log(np.exp(z).sum(1, keepdims=True))
    per = -logp[np.arange(len(y)), y]
    return (w[y] * per).sum() / w[y].sum()           # PyTorch normalises by the sum of weights too

logits = np.zeros((len(y), 3))                       # an uninformed model
print("plain loss   :", round(float(-np.log(1 / 3)), 4))
print("weighted loss:", round(float(weighted_ce(logits, y, weights)), 4))
logits[:, 0] = 3.0                                   # a model that always says class 0
print("always-0 plain accuracy:", (logits.argmax(1) == y).mean(), "| weighted loss:", round(float(weighted_ce(logits, y, weights)), 3))
%%END
<ol><li>Class 2 appears only twice in 100 rows, so its weight is 100 / (3 x 2) = 16.667, while class 0 gets 0.370.</li><li>With zero logits every class has probability 1/3, so the plain loss is log 3 = 1.0986; the weighted loss is the same because the model is uniform.</li><li>A model that always predicts the majority class gets 90 percent accuracy, which looks good but is useless. The weighted loss (about 2.1) exposes it because the rare examples are expensive. In PyTorch: <code>nn.CrossEntropyLoss(weight=torch.tensor(weights, dtype=torch.float32))</code>. Judge with per-class recall, not accuracy.</li></ol>
<h3>Recipe 5: How do I run inference on 100,000 texts without running out of memory?</h3>
<p>Sort by length so batches have little padding, use no-grad mode, move results to the CPU as you go (not run here), and restore the original order at the end. The runnable part below shows the ordering logic.</p>
%%PY
import numpy as np

lengths = np.array([5, 40, 7, 38, 6, 41, 9, 37, 8, 39])
order = np.argsort(lengths)                          # short with short, long with long
batches = [order[i:i + 5] for i in range(0, len(order), 5)]
padded_sorted = sum(lengths[b].max() * len(b) for b in batches)
unsorted = [np.arange(10)[i:i + 5] for i in range(0, 10, 5)]
padded_unsorted = sum(lengths[b].max() * len(b) for b in unsorted)
print("padded cells, unsorted batches:", padded_unsorted, "| sorted batches:", padded_sorted)

preds_sorted = lengths[order] * 2                    # pretend model output, in sorted order
restored = np.empty_like(preds_sorted)
restored[order] = preds_sorted                       # undo the sort
print("original order restored:", np.array_equal(restored, lengths * 2))
%%END
<ol><li>Padding cost is batch size times the longest item in the batch. Unsorted, each batch of five contains a 40-ish token text, so the batches pad to 40 and 41 and cost 200 + 205 = 405 cells. Sorted, one batch pads to 9 and the other to 41: 45 + 205 = 250 cells.</li><li><code>restored[order] = preds_sorted</code> is the standard inverse permutation. Skipping it returns predictions in the wrong order: a silent, serious bug.</li></ol>
%%NORUN
@torch.inference_mode()
def predict(texts, batch_size=64):
    order = sorted(range(len(texts)), key=lambda i: len(texts[i]))
    out = [None] * len(texts)
    model.eval()
    for s in range(0, len(order), batch_size):
        idx = order[s:s + batch_size]
        enc = tok([texts[i] for i in idx], padding=True, truncation=True, max_length=256, return_tensors="pt").to(device)
        probs = torch.softmax(model(**enc).logits, dim=-1).cpu().numpy()      # move off the GPU each batch
        for j, i in enumerate(idx):
            out[i] = probs[j]
    return out
%%END
<h3>Recipe 6: How do I chunk long documents for retrieval?</h3>
<p>Cut into windows of roughly fixed size with overlap so that a sentence cut at one boundary appears whole in the neighbour. Here words stand in for tokens.</p>
%%PY
def chunk(words, size, overlap):
    assert 0 <= overlap < size
    step = size - overlap
    return [words[i:i + size] for i in range(0, max(1, len(words) - overlap), step)]

text = "one two three four five six seven eight nine ten eleven twelve".split()
for c in chunk(text, size=5, overlap=2):
    print(c)
print("chunks for 1000 words, size 200, overlap 50:", len(chunk(list(range(1000)), 200, 50)))
%%END
<ol><li>The step between window starts is <code>size - overlap</code> = 3, so windows start at words 0, 3, 6 and 9, and consecutive chunks share two words.</li><li>For 1000 words with step 150 the starts are 0, 150, ..., 900 (7 windows; the last one is shorter). Store the start offset in the metadata so you can cite where an answer came from.</li><li>Chunk by tokens (or sentences) in real systems, not characters, because the embedding model limit is in tokens.</li></ol>
<h3>Recipe 7: How do I find near-duplicate tickets?</h3>
<p>Embed, normalise, compute the similarity matrix, and keep pairs above a threshold. For large sets use an ANN index instead of the full matrix.</p>
%%PY
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

tickets = ["charged twice this month", "I was charged twice this month", "app crashes on login",
           "the app crashes on login screen", "how do I export data"]
M = TfidfVectorizer(ngram_range=(1, 2)).fit_transform(tickets)
S = (M @ M.T).toarray()                       # TF-IDF rows are unit length, so this is cosine
np.fill_diagonal(S, 0)
i, j = np.where(np.triu(S) > 0.5)
for a, b in zip(i, j):
    print(f"{a} ~ {b}  cosine {S[a, b]:.2f}  {tickets[a]!r} / {tickets[b]!r}")
%%END
<ol><li><code>M @ M.T</code> gives every pairwise cosine at once. The diagonal (each text with itself) is zeroed so it does not match.</li><li><code>np.triu</code> keeps each pair once. Only the two paraphrase pairs should pass the 0.5 threshold; pick the threshold by inspecting pairs near it.</li><li>For 1 million tickets the matrix would have 10<sup>12</sup> cells, so use FAISS range search or nearest neighbours per item.</li></ol>
<h3>Recipe 8: How do I cache LLM answers so repeated prompts are free?</h3>
%%PY
import hashlib, json

class CachedClient:
    def __init__(self, llm):
        self.llm, self.cache, self.hits = llm, {}, 0
    def complete(self, model, prompt, temperature=0):
        key = hashlib.sha256(json.dumps([model, prompt, temperature], sort_keys=True).encode()).hexdigest()
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        self.cache[key] = self.llm(prompt)
        return self.cache[key]

calls = []
def llm(prompt):
    calls.append(prompt)
    return prompt.upper()

c = CachedClient(llm)
for p in ["hello", "hello", "bye", "hello"]:
    c.complete("m1", p)
print("real calls:", len(calls), "| cache hits:", c.hits)
c.complete("m2", "hello")
print("different model -> new call, total real calls:", len(calls))
%%END
<ol><li>The key hashes everything that changes the answer: model name, prompt and temperature. Leaving one out returns stale answers.</li><li>Four requests make two real calls and two hits; asking the same prompt of a different model is a miss.</li><li>Cache only when output is meant to be repeatable (temperature 0). Caching a creative sampling call makes every user see one answer. Providers also offer prompt caching on the server side for long repeated prefixes; that is separate.</li></ol>
<h3>Recipe 9: How do I call an LLM for 1,000 rows concurrently without flooding the API?</h3>
<p>Use <code>asyncio</code> with a semaphore that caps in-flight calls. The fake client sleeps briefly to imitate latency.</p>
%%PY
import asyncio

active, peak = 0, 0

async def fake_call(i):
    global active, peak
    active += 1
    peak = max(peak, active)
    await asyncio.sleep(0.001)
    active -= 1
    return i * 2

async def run_all(n, limit):
    sem = asyncio.Semaphore(limit)
    async def guarded(i):
        async with sem:
            return await fake_call(i)
    return await asyncio.gather(*(guarded(i) for i in range(n)))

results = asyncio.run(run_all(200, limit=8))
print("results in input order:", results[:5], "... count", len(results))
print("peak concurrent calls:", peak)
%%END
<ol><li>All 200 tasks are created at once, but the semaphore lets only 8 run the call at a time; the peak counter confirms 8.</li><li><code>asyncio.gather</code> returns results in the order the tasks were given, not the order they finished, so rows stay aligned with inputs.</li><li>With real async clients (<code>AsyncAnthropic</code>, <code>AsyncOpenAI</code>) the structure is the same; combine it with the retry helper from 21.9 inside <code>guarded</code>, and keep the limit under your rate limit.</li></ol>
<h3>Recipe 10: How do I make a run reproducible?</h3>
<p>Seed every generator you use, and know the limits. In PyTorch: <code>random.seed</code>, <code>np.random.seed</code>, <code>torch.manual_seed</code> (this also seeds CUDA), a seeded <code>torch.Generator</code> for the DataLoader, and optionally <code>torch.use_deterministic_algorithms(True)</code> (slower, and some operations then raise errors). The NumPy side of the idea:</p>
%%PY
import numpy as np

def noisy_mean(seed):
    rng = np.random.default_rng(seed)
    return float(rng.normal(size=1000).mean())

print(noisy_mean(7) == noisy_mean(7), noisy_mean(7) == noisy_mean(8))
child1, child2 = np.random.default_rng(1), np.random.default_rng(2)
print("independent streams differ:", child1.random() != child2.random())
%%END
<ol><li>The same seed reproduces the same number exactly; a different seed does not.</li><li>Prefer one explicit <code>Generator</code> object per component over the global state, so adding a random call in one place does not shift the numbers somewhere else.</li><li>Exact reproducibility across different GPUs or library versions is not guaranteed; report mean and spread over several seeds when the result matters.</li></ol>
<h3>Recipe 11: How do I keep a chat history inside the model's token limit?</h3>
<p>Keep the system message, then the newest turns that fit the budget. Count with the provider's token counter (<code>count_tokens</code>, or the model's tokenizer); words are used below only to keep the example runnable.</p>
%%PY
def fit_history(system, turns, budget, count=lambda s: len(s.split())):
    used = count(system)
    kept = []
    for role, text in reversed(turns):            # walk from the newest turn backwards
        c = count(text)
        if used + c > budget:
            break
        kept.append((role, text)); used += c
    return list(reversed(kept)), used

turns = [("user", "hello there"), ("assistant", "hi how can I help you today"),
         ("user", "my invoice is wrong"), ("assistant", "which month is it from"), ("user", "last month")]
kept, used = fit_history("You are a billing assistant", turns, budget=16)
print([t[1] for t in kept], "| used:", used)
%%END
<ol><li>The system message costs 5 words and is always kept.</li><li>Walking backwards keeps the three newest turns (2 + 5 + 4 = 11 more words, total 16, exactly the budget). The next older turn ("hi how can I help you today", 7 words) would exceed it, so the loop stops.</li><li>Dropping old turns blindly can lose facts; summarising old turns into one short message is the usual refinement.</li></ol>
<h3>Recipe 12: How do I turn logits into top-k labels with probabilities?</h3>
%%PY
import numpy as np

labels = np.array(["billing", "bug", "how-to", "other"])
logits = np.array([[2.0, 0.5, -1.0, 0.0], [0.1, 0.2, 3.0, 0.0]])
z = logits - logits.max(1, keepdims=True)
probs = np.exp(z) / np.exp(z).sum(1, keepdims=True)
top2 = np.argsort(-probs, axis=1)[:, :2]                    # torch.topk(probs, 2)
for row, idx in enumerate(top2):
    print([(str(labels[i]), round(float(probs[row, i]), 3)) for i in idx])
%%END
<ol><li>Softmax turns each row of scores into probabilities that sum to 1.</li><li><code>argsort(-probs)</code> sorts descending; the first two columns are the top two classes per row. <code>torch.topk</code> returns values and indices together.</li><li>Show users the probability, but remember softmax probabilities of an uncalibrated network are often over-confident.</li></ol>

<h2 id="s21-12">21.12 Performance and Pitfalls</h2>
<p>Twelve traps, each with the wrong code, the symptom and the fix. The numbers in this section are timings measured on the machine that produced this book; they vary on yours, so measure your own.</p>
<div class="callout red"><div class="lab">COMMON MISTAKE 1: forgot to clear gradients</div><div class="txt"><strong>Wrong:</strong> a loop with <code>loss.backward(); opt.step()</code> and no <code>opt.zero_grad()</code>. <strong>Symptom:</strong> the loss behaves erratically or diverges, because every step uses the sum of all gradients so far (we saw accumulation in 21.2). <strong>Fix:</strong> call <code>opt.zero_grad(set_to_none=True)</code> once per optimiser step, before <code>backward()</code>.</div></div>
<div class="callout red"><div class="lab">COMMON MISTAKE 2: evaluating in train mode</div><div class="txt"><strong>Wrong:</strong> <code>preds = model(x)</code> after training without <code>model.eval()</code> or <code>no_grad</code>. <strong>Symptom:</strong> predictions change each call (dropout), batch-norm statistics drift, and memory climbs because a graph is built. <strong>Fix:</strong> <code>model.eval()</code> plus <code>with torch.inference_mode():</code>, and switch back with <code>model.train()</code> before training again.</div></div>
<div class="callout red"><div class="lab">COMMON MISTAKE 3: row-by-row instead of batched</div><div class="txt"><strong>Wrong:</strong> <code>[model(x) for x in rows]</code> or <code>for row in df.itertuples()</code> around a model. <strong>Symptom:</strong> inference is many times slower than needed. <strong>Fix:</strong> stack rows into a batch and call once. The timing below shows the same effect in NumPy.</div></div>
%%PY
import time
import numpy as np

rng = np.random.default_rng(0)
X = rng.normal(size=(2000, 64)).astype(np.float32)
W = rng.normal(size=(64, 32)).astype(np.float32)

t0 = time.perf_counter(); slow = np.stack([x @ W for x in X]); t_loop = time.perf_counter() - t0
t0 = time.perf_counter(); fast = X @ W; t_batch = time.perf_counter() - t0
print("same result:", np.allclose(slow, fast, atol=1e-4))
print("batched is more than 2x faster:", t_loop / t_batch > 2)
%%END
<p>On the machine used here the loop took about 2 ms and the batch about 0.4 ms, a ratio around 6 (it varies from run to run). With a real model on a GPU the gap is much larger, because each call has a fixed launch overhead.</p>
<div class="callout red"><div class="lab">COMMON MISTAKE 4: a starving GPU</div><div class="txt"><strong>Wrong:</strong> <code>DataLoader(ds, batch_size=64)</code> with heavy preprocessing in <code>__getitem__</code> and the default <code>num_workers=0</code>. <strong>Symptom:</strong> the GPU shows low utilisation and each epoch is slow even though the model is small. <strong>Fix:</strong> <code>num_workers=2</code> or more, <code>pin_memory=True</code>, do the tokenisation once in a <code>map</code> step instead of per item, and time data loading separately from the model step.</div></div>
<div class="callout red"><div class="lab">COMMON MISTAKE 5: leakage through preprocessing</div><div class="txt"><strong>Wrong:</strong> <code>scaler.fit(X_all)</code> or learning a vocabulary on all text before splitting, or duplicates of one ticket on both sides of the split. <strong>Symptom:</strong> validation scores far better than production. <strong>Fix:</strong> split first, fit every learned transform on the training part only, deduplicate (recipe 7) before splitting, and split by customer or time when rows are related.</div></div>
<div class="callout red"><div class="lab">COMMON MISTAKE 6: loading untrusted pickles</div><div class="txt"><strong>Wrong:</strong> <code>torch.load("model_from_the_internet.pt")</code> with old defaults, or <code>pickle.load</code>. <strong>Symptom:</strong> none until a malicious file runs code on your machine. <strong>Fix:</strong> <code>weights_only=True</code>, or the safetensors format, and download models only from sources you trust.</div></div>
<div class="callout red"><div class="lab">COMMON MISTAKE 7: learning rate too high and no clipping</div><div class="txt"><strong>Wrong:</strong> <code>lr=0.1</code> with Adam on a transformer. <strong>Symptom:</strong> the loss jumps to <code>nan</code> within a few steps (we saw divergence in 21.3). <strong>Fix:</strong> start near 1e-5 to 3e-4 for Adam-type optimisers on transformers, add warm-up, clip the gradient norm to 1.0, and log the pre-clip norm to see spikes.</div></div>
<div class="callout red"><div class="lab">COMMON MISTAKE 8: wrong dimension for sequence logits</div><div class="txt"><strong>Wrong:</strong> <code>F.cross_entropy(logits, targets)</code> with logits of shape (B, T, V) and targets (B, T). <strong>Symptom:</strong> a shape error, or (worse, if sizes line up) a loss computed over the wrong axis. <strong>Fix:</strong> <code>F.cross_entropy(logits.reshape(-1, V), targets.reshape(-1))</code>, or <code>logits.transpose(1, 2)</code> to (B, V, T), and set <code>ignore_index=-100</code> for padded positions.</div></div>
<div class="callout red"><div class="lab">COMMON MISTAKE 9: an in-place operation on a tracked tensor</div><div class="txt"><strong>Wrong:</strong> <code>h = layer(x); h += 1; h.relu_()</code> where autograd still needs the old values. <strong>Symptom:</strong> <code>RuntimeError: one of the variables needed for gradient computation has been modified by an inplace operation</code>. <strong>Fix:</strong> use the out-of-place form (<code>h = h + 1</code>). Reserve in-place updates for code under <code>torch.no_grad()</code>, such as manual weight updates.</div></div>
<div class="callout red"><div class="lab">COMMON MISTAKE 10: silent prompt truncation</div><div class="txt"><strong>Wrong:</strong> stuffing all retrieved text into one prompt without counting tokens, or embedding long documents with a model that has a 256-token limit. <strong>Symptom:</strong> answers ignore the end of the document, or the API returns a context-length error. <strong>Fix:</strong> count tokens before sending, chunk (recipe 6), limit retrieved chunks, and check the embedding model's <code>max_seq_length</code>.</div></div>
<div class="callout red"><div class="lab">COMMON MISTAKE 11: retrying actions that are not safe to repeat</div><div class="txt"><strong>Wrong:</strong> wrapping a tool call that sends an email or issues a refund inside the same retry loop as the model call. <strong>Symptom:</strong> after a timeout the action runs twice. <strong>Fix:</strong> retry only the read-only model request; make side-effect tools idempotent with an idempotency key, and record completed actions.</div></div>
<div class="callout red"><div class="lab">COMMON MISTAKE 12: secrets in code</div><div class="txt"><strong>Wrong:</strong> <code>client = OpenAI(api_key="sk-...")</code> committed to a repository or notebook. <strong>Symptom:</strong> leaked key, unexpected bills, a forced key rotation. <strong>Fix:</strong> read keys from environment variables or a secret manager (the SDKs do this by default), keep <code>.env</code> in <code>.gitignore</code>, and never print request headers in logs.</div></div>
<div class="callout green"><div class="lab">KEY IDEA</div><div class="txt">Speed order of attack: first make it correct, then <em>measure</em>, then fix the biggest cost. In training the usual order is data loading, batch size and padding, mixed precision (bfloat16), and only then compile or kernel-level work. In LLM apps it is fewer and shorter calls, caching, concurrency within rate limits, and a smaller model for easy cases.</div></div>

<h2 id="s21-13">21.13 Common Error Messages and Their Fixes</h2>
<p>Exact wording differs between library versions, so search for the distinctive phrase. The table lists the situation, the cause and the fix.</p>
<div class="tablewrap"><table class="data"><thead><tr><th>Message (abridged)</th><th>Cause</th><th>Fix</th></tr></thead><tbody>
<tr><td><code>RuntimeError: mat1 and mat2 shapes cannot be multiplied (32x10 and 20x5)</code></td><td>Layer expects 20 inputs, got 10 features</td><td>Print <code>x.shape</code>; fix <code>in_features</code> or the flatten step</td></tr>
<tr><td><code>RuntimeError: Expected all tensors to be on the same device, but found at least two devices, cuda:0 and cpu</code></td><td>Model on GPU, a tensor on CPU</td><td><code>x = x.to(device)</code> for every batch field</td></tr>
<tr><td><code>torch.OutOfMemoryError: CUDA out of memory. Tried to allocate ...</code></td><td>Batch, sequence or model too big for the GPU</td><td>Smaller batch, gradient accumulation, bfloat16, checkpointing, shorter sequences, LoRA (21.5)</td></tr>
<tr><td><code>RuntimeError: element 0 of tensors does not require grad and does not have a grad_fn</code></td><td>Loss detached from the graph (<code>no_grad</code>, <code>.detach()</code>, frozen everything, or <code>.item()</code> used in the loss)</td><td>Keep the loss as a tensor built from model outputs; check <code>requires_grad</code></td></tr>
<tr><td><code>RuntimeError: Trying to backward through the graph a second time</code></td><td>Reusing a graph, often hidden state carried across batches</td><td><code>.detach()</code> the carried state; avoid <code>retain_graph</code></td></tr>
<tr><td><code>one of the variables needed for gradient computation has been modified by an inplace operation</code></td><td>In-place op on a needed tensor</td><td>Use the out-of-place version</td></tr>
<tr><td><code>Can't call numpy() on Tensor that requires grad. Use tensor.detach().numpy()</code></td><td>Converting a tracked tensor</td><td><code>t.detach().cpu().numpy()</code></td></tr>
<tr><td><code>expected scalar type Long but found Float</code> (or the reverse)</td><td>Class ids must be integer, inputs float</td><td><code>y.long()</code> for CrossEntropy class ids; <code>x.float()</code></td></tr>
<tr><td><code>IndexError: Target 5 is out of bounds</code> / <code>CUDA error: device-side assert triggered</code></td><td>Label outside 0..K-1, or token id beyond the embedding size</td><td>Check <code>y.min(), y.max()</code> and <code>num_labels</code>; rerun on CPU for a clear message</td></tr>
<tr><td><code>view size is not compatible with input tensor's size and stride</code></td><td><code>.view</code> on non-contiguous memory</td><td><code>.reshape(...)</code> or <code>.contiguous().view(...)</code></td></tr>
<tr><td><code>ValueError: expected sequence of length 5 at dim 1 (got 3)</code></td><td>Building a tensor from ragged lists</td><td>Pad in a collate function (21.4)</td></tr>
<tr><td><code>Input type (torch.cuda.FloatTensor) and weight type (torch.FloatTensor) should be the same</code></td><td>Data on GPU, model on CPU</td><td><code>model.to(device)</code></td></tr>
<tr><td><code>ValueError: Asking to pad but the tokenizer does not have a padding token</code></td><td>Decoder-only tokenisers often lack one</td><td><code>tok.pad_token = tok.eos_token</code></td></tr>
<tr><td><code>Token indices sequence length is longer than the specified maximum sequence length</code></td><td>Text exceeds the model limit</td><td><code>truncation=True, max_length=...</code> or chunk the text</td></tr>
<tr><td><code>OSError: ... is not a local folder and is not a valid model identifier</code></td><td>Typo in the model id, no network, or a private model without a token</td><td>Check the id; log in; pass a local path</td></tr>
<tr><td><code>Error(s) in loading state_dict ... Missing key(s) / size mismatch</code></td><td>Architecture differs from the checkpoint</td><td>Rebuild with the saved config; <code>strict=False</code> only to inspect</td></tr>
<tr><td><code>AssertionError: ... d == self.d</code> (FAISS) or dtype errors</td><td>Wrong vector size or float64</td><td><code>x.astype("float32")</code>, same dimension as the index</td></tr>
<tr><td><code>openai.RateLimitError</code> / <code>anthropic.RateLimitError</code> (429)</td><td>Too many requests or tokens per minute</td><td>Backoff, <code>retry-after</code>, lower concurrency (21.9)</td></tr>
<tr><td><code>BadRequestError</code> (400) mentioning context length or max tokens</td><td>Prompt plus output exceeds the window, or invalid parameters</td><td>Count and trim tokens; do not retry unchanged</td></tr>
<tr><td><code>AuthenticationError</code> (401)</td><td>Missing or wrong key</td><td>Set the environment variable; check the organisation</td></tr>
<tr><td><code>json.JSONDecodeError</code> on a model reply</td><td>Fence, trailing text, truncation</td><td>Structured output feature, validator, repair loop (21.9)</td></tr>
</tbody></table></div>
<p>The NumPy equivalents of the first and last of these are real errors you can see right now:</p>
%%PY
import numpy as np

x = np.ones((32, 10)); W = np.ones((20, 5))
try:
    x @ W
except ValueError as e:
    print("numpy:", str(e).splitlines()[0][:70])
try:
    np.array([[1, 2, 3, 4, 5], [1, 2, 3]], dtype=float)
except ValueError as e:
    print("ragged:", str(e)[:80])
t = np.arange(12).reshape(3, 4).T
try:
    t.view().shape = (12,)
except AttributeError as e:
    print("reshape in place:", str(e)[:70])
%%END
<ol><li>The first error is NumPy's version of the PyTorch matrix shape message. Both name the offending sizes; read them as (rows, columns) pairs and check the inner numbers (10 versus 20).</li><li>Building an array from ragged lists fails for the same reason a tensor does: a rectangle needs equal lengths.</li><li>Assigning a new shape to a transposed array in place fails because the memory is not contiguous; <code>reshape</code> copies where necessary, exactly as <code>tensor.reshape</code> does.</li></ol>
