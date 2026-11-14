
<h2 id="s21-7">21.7 Hugging Face: transformers, tokenizers, datasets and peft</h2>
<div class="callout blue"><div class="lab">INTUITION</div><div class="txt">Hugging Face is a library of <em>parts that fit together by convention</em>. A checkpoint name such as a model id on the Hub points to three things: a tokeniser (text to ids), a config (the architecture) and weights. The <code>Auto*</code> classes read the config and build the right architecture for you. The <code>datasets</code> library holds your examples in a fast disk-backed table. The <code>Trainer</code> is a ready-made training loop like the one you wrote in 21.4. <code>peft</code> freezes the big model and trains tiny add-on matrices.</div></div>
<h3>Reference: the most important Hugging Face names</h3>
<div class="tablewrap"><table class="data"><thead><tr><th>Name</th><th>What it does in plain English</th><th>Minimal example (not run here)</th></tr></thead><tbody>
<tr><td><code>AutoTokenizer.from_pretrained</code></td><td>Load the tokeniser that matches a model</td><td><code>tok = AutoTokenizer.from_pretrained(name)</code></td></tr>
<tr><td><code>tok(text, ...)</code></td><td>Text to <code>input_ids</code> and <code>attention_mask</code></td><td><code>tok(["a", "bb"], padding=True, return_tensors="pt")</code></td></tr>
<tr><td><code>padding / truncation / max_length</code></td><td>Make a batch rectangular and bounded</td><td><code>tok(x, truncation=True, max_length=128)</code></td></tr>
<tr><td><code>tok.tokenize / convert_ids_to_tokens</code></td><td>See the pieces</td><td><code>tok.tokenize("unbelievable")</code></td></tr>
<tr><td><code>tok.decode</code></td><td>Ids back to text</td><td><code>tok.decode(ids, skip_special_tokens=True)</code></td></tr>
<tr><td><code>tok.pad_token / eos_token</code></td><td>Special tokens; set pad if missing</td><td><code>tok.pad_token = tok.eos_token</code></td></tr>
<tr><td><code>AutoModel</code></td><td>Bare encoder: hidden states only</td><td><code>AutoModel.from_pretrained(name)</code></td></tr>
<tr><td><code>AutoModelForSequenceClassification</code></td><td>Encoder plus a classification head</td><td><code>...from_pretrained(name, num_labels=3)</code></td></tr>
<tr><td><code>AutoModelForCausalLM</code></td><td>A text-continuing language model</td><td><code>AutoModelForCausalLM.from_pretrained(name)</code></td></tr>
<tr><td><code>from_pretrained(dtype, device_map)</code></td><td>Load in 16-bit and spread across devices (older releases call the first argument <code>torch_dtype</code>)</td><td><code>..., dtype=torch.bfloat16, device_map="auto"</code></td></tr>
<tr><td><code>model.generate</code></td><td>Produce new tokens</td><td><code>model.generate(**batch, max_new_tokens=50)</code></td></tr>
<tr><td><code>pipeline(task)</code></td><td>One-line tokenise, model, decode</td><td><code>pipeline("text-classification", model=name)</code></td></tr>
<tr><td><code>TrainingArguments</code></td><td>All training settings in one object</td><td><code>TrainingArguments(output_dir="out", learning_rate=2e-5)</code></td></tr>
<tr><td><code>Trainer</code></td><td>Ready-made loop with eval, saving, logging</td><td><code>Trainer(model=m, args=a, train_dataset=tr)</code></td></tr>
<tr><td><code>DataCollatorWithPadding</code></td><td>Dynamic padding per batch</td><td><code>DataCollatorWithPadding(tok)</code></td></tr>
<tr><td><code>model.save_pretrained / from_pretrained</code></td><td>Save and reload weights plus config</td><td><code>model.save_pretrained("dir")</code></td></tr>
<tr><td><code>load_dataset</code></td><td>Load from the Hub, files or scripts</td><td><code>load_dataset("csv", data_files="t.csv")</code></td></tr>
<tr><td><code>ds.map(fn, batched=True)</code></td><td>Apply a function to many rows at a time</td><td><code>ds.map(tokenize, batched=True)</code></td></tr>
<tr><td><code>ds.filter / select / shuffle</code></td><td>Subset and reorder rows</td><td><code>ds.filter(lambda r: r["n"] &gt; 3)</code></td></tr>
<tr><td><code>ds.train_test_split</code></td><td>Make train and test splits</td><td><code>ds.train_test_split(test_size=0.2, seed=0)</code></td></tr>
<tr><td><code>ds.set_format("torch")</code></td><td>Return tensors instead of lists</td><td><code>ds.set_format("torch", columns=["input_ids"])</code></td></tr>
<tr><td><code>ds.to_pandas / Dataset.from_pandas</code></td><td>Convert to and from a DataFrame</td><td><code>Dataset.from_pandas(df)</code></td></tr>
<tr><td><code>load_dataset(..., streaming=True)</code></td><td>Iterate without downloading everything</td><td><code>for row in ds: ...</code></td></tr>
<tr><td><code>LoraConfig</code></td><td>Choose rank r, scaling alpha, target layers</td><td><code>LoraConfig(r=8, lora_alpha=16, target_modules=["q_proj", "v_proj"])</code></td></tr>
<tr><td><code>get_peft_model</code></td><td>Wrap a model with trainable adapters</td><td><code>model = get_peft_model(base, cfg)</code></td></tr>
<tr><td><code>print_trainable_parameters</code></td><td>Show the small trainable share</td><td><code>model.print_trainable_parameters()</code></td></tr>
<tr><td><code>merge_and_unload</code></td><td>Fold adapters into the base weights</td><td><code>merged = model.merge_and_unload()</code></td></tr>
</tbody></table></div>
<h3>Tokenisers: from text to ids</h3>
<p>Models cannot read letters; they read integer ids. A tokeniser splits text into pieces from a fixed vocabulary of <strong>subwords</strong>. Common words are one piece; rare words are cut into smaller known pieces; nothing is ever completely unknown. The most common method, <strong>byte-pair encoding (BPE)</strong>, builds the vocabulary by repeatedly merging the most frequent adjacent pair of symbols. The tokeniser also adds an <code>attention_mask</code> telling the model which positions are real.</p>
<p>Idiomatic use (not run here):</p>
%%NORUN
from transformers import AutoTokenizer

name = "your-model-id"                       # any Hub id, e.g. a BERT-style or small encoder model
tok = AutoTokenizer.from_pretrained(name)

batch = tok(["reset password", "refund the billing charge twice"],
            padding=True, truncation=True, max_length=128, return_tensors="pt")
print(batch.keys())                           # input_ids, attention_mask (and sometimes token_type_ids)
print(batch["input_ids"].shape)               # (2, T) where T = longest in this batch
print(tok.convert_ids_to_tokens(batch["input_ids"][0]))
print(tok.decode(batch["input_ids"][0], skip_special_tokens=True))

# decoder-only models often have no pad token: set one before padding a batch
if tok.pad_token is None:
    tok.pad_token = tok.eos_token
tok.padding_side = "left"                     # for generation with decoder-only models
%%END
<p>Now a working miniature. This BPE tokeniser trains on a small corpus, splits unseen words into known pieces and returns the same dictionary keys as the Hugging Face call.</p>
<p class="problem"><span class="pl">Problem 21.7.1</span> Train 50 merges on eight support sentences. Show the first merges, split an unseen word, and encode a padded batch.</p>
%%PY
from collections import Counter

corpus = ["refund the billing charge", "billing charge refunded twice", "cannot reset password",
          "password reset link broken", "charge appears twice on billing page", "reset the password link",
          "refund requested for twice charged order", "how to reset billing password"]

def train_bpe(texts, n_merges):
    words = Counter()
    for t in texts:
        for w in t.lower().split():
            words[tuple(w) + ("</w>",)] += 1
    merges = []
    for _ in range(n_merges):
        pairs = Counter()
        for w, c in words.items():
            for a, b in zip(w, w[1:]):
                pairs[(a, b)] += c
        if not pairs:
            break
        best = max(pairs, key=lambda p: (pairs[p], p))      # most frequent pair, ties by name
        merges.append(best)
        new = Counter()
        for w, c in words.items():
            out, i = [], 0
            while i < len(w):
                if i < len(w) - 1 and (w[i], w[i + 1]) == best:
                    out.append(w[i] + w[i + 1]); i += 2
                else:
                    out.append(w[i]); i += 1
            new[tuple(out)] += c
        words = new
    return merges

class BPETokenizer:
    def __init__(self, merges, corpus):
        self.rank = {m: i for i, m in enumerate(merges)}
        chars = sorted({ch for t in corpus for ch in t.lower() if ch != " "})
        toks = ["<pad>", "<unk>"] + chars + ["</w>"] + ["".join(m) for m in merges]
        self.vocab = {t: i for i, t in enumerate(dict.fromkeys(toks))}
        self.inv = {i: t for t, i in self.vocab.items()}
    def tokenize(self, text):
        out = []
        for w in text.lower().split():
            syms = list(w) + ["</w>"]
            while len(syms) > 1:
                cand = [(self.rank[p], i) for i, p in enumerate(zip(syms, syms[1:])) if p in self.rank]
                if not cand:
                    break
                _, i = min(cand)                              # apply the earliest-learned merge first
                syms[i:i + 2] = [syms[i] + syms[i + 1]]
            out.extend(syms)
        return out
    def __call__(self, texts, padding=False, truncation=False, max_length=None):
        ids = [[self.vocab.get(t, 1) for t in self.tokenize(x)] for x in texts]
        if truncation and max_length:
            ids = [s[:max_length] for s in ids]
        longest = max(len(s) for s in ids) if padding else 0
        mask = [[1] * len(s) + [0] * (longest - len(s)) for s in ids]
        ids = [s + [0] * (longest - len(s)) for s in ids]
        return {"input_ids": ids, "attention_mask": mask}
    def decode(self, ids):
        return "".join(self.inv[i] for i in ids if i != 0).replace("</w>", " ").strip()

merges = train_bpe(corpus, 50)
tok = BPETokenizer(merges, corpus)
print("first merges:", merges[:5])
print("vocab size:", len(tok.vocab))
print("seen    :", tok.tokenize("refund the billing"))
print("unseen  :", tok.tokenize("refunding passwords"))
print("unknown :", tok.tokenize("xyz"))
batch = tok(["reset password", "refund the billing charge twice"], padding=True)
print("shape   :", len(batch["input_ids"]), "x", len(batch["input_ids"][0]))
print("mask    :", batch["attention_mask"])
print("decoded :", tok.decode(batch["input_ids"][0]))
print("truncated:", tok(["refund the billing charge twice"], truncation=True, max_length=4)["input_ids"])
%%END
<ol><li><code>train_bpe</code> starts with each word as a tuple of characters plus an end-of-word marker. Each round it counts all adjacent pairs (weighted by word frequency), merges the most frequent pair everywhere, and records the merge. Fifty rounds leave an ordered list of merge rules.</li><li>The <code>BPETokenizer</code> vocabulary contains special tokens first (<code>&lt;pad&gt;</code> id 0, <code>&lt;unk&gt;</code> id 1), then single characters, then one entry per merge. A real tokeniser works the same way with a vocabulary of tens of thousands.</li><li><code>tokenize</code> applies the earliest-learned merge first, repeatedly. A word seen in training collapses into few pieces. The unseen word "refunding" still works because it breaks into known smaller pieces (see the printed lists).</li><li>A word made of letters outside the training alphabet falls back to the <code>&lt;unk&gt;</code> id when mapped to ids. Real byte-level tokenisers avoid <code>&lt;unk&gt;</code> entirely by starting from the 256 bytes.</li><li>The call returns the same two keys as Hugging Face. The shorter sequence is padded with zeros and its mask has zeros in those places.</li><li><code>decode</code> reverses the mapping. <code>truncation=True, max_length=4</code> simply cuts the id list. In real models truncation also reserves room for special tokens; keep an eye on this when comparing lengths.</li></ol>
<div class="callout green"><div class="lab">KEY IDEA</div><div class="txt">Always use the tokeniser that was trained with the model. A different vocabulary maps the same id to a different piece, and the model produces garbage without raising any error. Token counts, not characters or words, decide cost, speed and the context limit of an LLM call.</div></div>
<h3>datasets: a table that does not live in RAM</h3>
<p>A Hugging Face <code>Dataset</code> is a typed table stored on disk (Apache Arrow) and memory-mapped, with results of <code>map</code> cached. Two ideas matter most. <strong>Batched map</strong>: your function receives a dictionary of lists and returns a dictionary of lists, which is much faster than one row at a time. <strong>Immutability</strong>: every operation returns a <em>new</em> dataset; writing <code>ds.map(f)</code> and ignoring the result does nothing (the same trap as DataFrame methods).</p>
%%NORUN
from datasets import load_dataset, Dataset

ds = load_dataset("csv", data_files={"train": "tickets_train.csv", "test": "tickets_test.csv"})
print(ds)                                    # DatasetDict with 'train' and 'test'
print(ds["train"].features)                  # column types

label2id = {"billing": 0, "bug": 1, "how-to": 2}

def prepare(batch):                          # batched=True: batch is a dict of lists
    enc = tok(batch["text"], truncation=True, max_length=128)
    enc["labels"] = [label2id[x] for x in batch["label"]]
    return enc

ds = ds.map(prepare, batched=True, remove_columns=["text", "label"])
ds = ds.filter(lambda row: len(row["input_ids"]) > 2)
split = ds["train"].train_test_split(test_size=0.1, seed=0)
ds.set_format("torch")                       # rows now come back as tensors
small = ds["train"].shuffle(seed=0).select(range(1000))      # quick debugging subset
df = ds["train"].to_pandas()
streamed = load_dataset("csv", data_files="huge.csv", split="train", streaming=True)
for row in streamed.take(2):
    print(row)
%%END
<p>The pandas stand-in below uses the same moves: a batched <code>map</code>, <code>filter</code>, a seeded <code>train_test_split</code> and a streaming read. It also shows the pandas 3 string dtype.</p>
<p class="problem"><span class="pl">Problem 21.7.2</span> Prepare ten tickets: add a token count, keep tickets with at least 3 tokens, split 80/20 with a seed, and stream the CSV in chunks of 4 rows.</p>
%%PY
import io
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.DataFrame({
    "text": ["refund the charge", "app crashes on login", "how to export data", "charged twice", "button does nothing",
             "reset my password please", "invoice missing", "error 500 on save", "where is the api key", "ok"],
    "label": ["billing", "bug", "how-to", "billing", "bug", "how-to", "billing", "bug", "how-to", "bug"],
})
print("text dtype:", df["text"].dtype)

def add_tokens(batch):                       # batched map: dict of lists in, dict of lists out
    return {"n_tokens": [len(t.split()) for t in batch["text"]]}

new_cols = add_tokens({"text": df["text"].tolist()})
df = df.assign(**new_cols)                   # returns a NEW frame, like Dataset.map
df = df[df["n_tokens"] >= 3].reset_index(drop=True)      # like Dataset.filter
print("rows kept:", len(df))

train, test = train_test_split(df, test_size=0.2, random_state=0, stratify=None)
print("train/test:", len(train), len(test), "| test rows:", list(test["text"]))

csv_text = df.to_csv(index=False)
seen = 0
for chunk in pd.read_csv(io.StringIO(csv_text), chunksize=4):     # like streaming=True
    seen += len(chunk)
    print("chunk of", len(chunk), "rows; first label:", chunk["label"].iloc[0])
print("streamed rows:", seen)
%%END
<ol><li>In pandas 3 a text column has the dedicated string dtype (printed as <code>str</code>), not <code>object</code>. Hugging Face stores strings in Arrow, which has the same idea.</li><li><code>add_tokens</code> has the batched-map shape: it receives a dictionary of columns (lists) and returns a dictionary of new columns. Writing the function this way means the same function works unchanged in <code>Dataset.map(add_tokens, batched=True)</code>.</li><li><code>df.assign</code> and boolean filtering return new objects. We reassign to <code>df</code>; forgetting that is the same bug as ignoring the result of <code>ds.map</code>.</li><li>The filter removes the three tickets with fewer than 3 words ("charged twice", "invoice missing" and "ok"), leaving 7 rows. A 20 percent test share of 7 rows rounds up to 2 test rows and 5 train rows, and the seed makes the chosen test rows repeatable.</li><li><code>chunksize=4</code> reads the file in pieces without loading it all, the idea behind <code>streaming=True</code>. With 7 rows we see a chunk of 4 and a chunk of 3.</li></ol>
<h3>Fine-tuning with Trainer (not run here)</h3>
<p>This is the complete recipe for fine-tuning a pretrained encoder as a ticket classifier. Compare it with the loop you wrote in 21.4: <code>Trainer</code> does the same forward, loss, backward, step, evaluate, save, early stop and logging, configured by <code>TrainingArguments</code>.</p>
%%NORUN
import numpy as np
from transformers import (AutoTokenizer, AutoModelForSequenceClassification,
                          DataCollatorWithPadding, TrainingArguments, Trainer)

name = "your-model-id"
tok = AutoTokenizer.from_pretrained(name)
model = AutoModelForSequenceClassification.from_pretrained(
    name, num_labels=3, id2label={0: "billing", 1: "bug", 2: "how-to"},
    label2id={"billing": 0, "bug": 1, "how-to": 2})

def compute_metrics(eval_pred):
    logits, labels = eval_pred                      # numpy arrays
    pred = logits.argmax(axis=-1)
    return {"accuracy": float((pred == labels).mean())}

args = TrainingArguments(
    output_dir="out", num_train_epochs=3, learning_rate=2e-5, weight_decay=0.01,
    per_device_train_batch_size=16, per_device_eval_batch_size=64,
    eval_strategy="epoch", save_strategy="epoch",   # called evaluation_strategy in older releases
    load_best_model_at_end=True, metric_for_best_model="accuracy",
    logging_steps=50, seed=42, report_to="none",
    bf16=False,                                     # set True on a GPU that supports bfloat16
)
trainer = Trainer(
    model=model, args=args,
    train_dataset=ds["train"], eval_dataset=ds["test"],
    data_collator=DataCollatorWithPadding(tok),     # pads each batch to its longest
    compute_metrics=compute_metrics,
    processing_class=tok,                           # called tokenizer= in older releases
)
trainer.train()
print(trainer.evaluate())
trainer.save_model("ticket-classifier")
tok.save_pretrained("ticket-classifier")

# inference
from transformers import pipeline
clf = pipeline("text-classification", model="ticket-classifier")
print(clf(["I was charged twice this month"]))
%%END
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Wrong:</strong> padding every example to <code>max_length=512</code> in the <code>map</code> step "to be safe". <strong>Symptom:</strong> training is several times slower and uses far more memory, because most positions are padding. <strong>Fix:</strong> tokenise without padding and use <code>DataCollatorWithPadding</code>, which pads each batch to its own longest example.</div></div>
<h3>peft and LoRA: train a small update instead of the whole matrix</h3>
<p>A weight matrix W of shape (d<sub>out</sub>, d<sub>in</sub>) normally changes by a full matrix of updates during fine-tuning. <strong>LoRA</strong> (low-rank adaptation) freezes W and learns the update as a product of two thin matrices: ΔW = (alpha / r) B A, where A has shape (r, d<sub>in</sub>), B has shape (d<sub>out</sub>, r) and r is small (4 to 64). B starts at zero so the model starts exactly equal to the base model. For d = 4096 and r = 8, the update has 2 x 4096 x 8 = 65,536 numbers instead of 16.8 million.</p>
%%NORUN
from peft import LoraConfig, get_peft_model, TaskType, PeftModel

base = AutoModelForCausalLM.from_pretrained("your-model-id", dtype=torch.bfloat16, device_map="auto")
cfg = LoraConfig(task_type=TaskType.CAUSAL_LM, r=8, lora_alpha=16, lora_dropout=0.05,
                 target_modules=["q_proj", "v_proj"])         # names depend on the architecture
model = get_peft_model(base, cfg)
model.print_trainable_parameters()          # prints trainable params, total params and the percentage
# ... train with Trainer or your own loop; only adapter weights have requires_grad=True ...
model.save_pretrained("ticket-lora")        # saves just the small adapter (megabytes)

# serving: reload base + adapter, optionally fold the adapter in for speed
base = AutoModelForCausalLM.from_pretrained("your-model-id", dtype=torch.bfloat16)
model = PeftModel.from_pretrained(base, "ticket-lora")
merged = model.merge_and_unload()           # plain model again, no adapter overhead
%%END
<p>Now the same mechanics in NumPy. A frozen weight matrix W0 is shifted by a hidden rank-4 change. We learn the change with only A and B, then merge.</p>
<p class="problem"><span class="pl">Problem 21.7.3</span> Let W0 be a 64 x 64 frozen matrix and the target be W0 plus a hidden rank-4 matrix. Train a LoRA update with r = 4 and alpha = 8 (scale s = alpha / r = 2) using gradients computed by hand, then verify that merging gives the same outputs.</p>
<table class="steps"><tr><th>Model</th><td>output = x (W0 + s B A)<sup>T</sup>. Parameters: A is 4 x 64 and B is 64 x 4, so 512 numbers instead of 4,096.</td></tr><tr><th>Gradient</th><td>With G = dL/dW (a 64 x 64 matrix from the usual layer formula), the chain rule gives dL/dB = s G A<sup>T</sup> and dL/dA = s B<sup>T</sup> G.</td></tr><tr><th>Start</th><td>B = 0 and A small random, so the first prediction equals the base model.</td></tr></table>
%%PY
import numpy as np

rng = np.random.default_rng(0)
d, r, N = 64, 4, 512
W0 = rng.normal(size=(d, d)) / np.sqrt(d)                       # frozen base weight
delta = rng.normal(size=(d, r)) @ rng.normal(size=(r, d)) / np.sqrt(d * r)   # hidden rank-4 change
X = rng.normal(size=(N, d))
Y = X @ (W0 + delta).T                                          # targets from the "true" fine-tuned layer

alpha = 8
s = alpha / r
A = rng.normal(scale=0.01, size=(r, d))
B = np.zeros((d, r))

def forward_loss():
    E = X @ (W0 + s * B @ A).T - Y
    return (E ** 2).mean(), E

print("loss at start (base model):", round(forward_loss()[0], 4))
mA, vA, mB, vB = np.zeros_like(A), np.zeros_like(A), np.zeros_like(B), np.zeros_like(B)
for t in range(1, 501):
    loss, E = forward_loss()
    G = 2 / (N * d) * E.T @ X                                   # dL/d(effective weight), shape (d, d)
    gB, gA = s * G @ A.T, s * B.T @ G
    for p, g, m, v in ((A, gA, mA, vA), (B, gB, mB, vB)):       # Adam, lr 0.02
        m *= 0.9; m += 0.1 * g
        v *= 0.999; v += 0.001 * g * g
        p -= 0.02 * (m / (1 - 0.9 ** t)) / (np.sqrt(v / (1 - 0.999 ** t)) + 1e-8)

print("loss after 500 steps:", f"{forward_loss()[0]:.2e}")
print("trainable:", A.size + B.size, "of", W0.size, f"= {100 * (A.size + B.size) / W0.size:.1f}%")
W_merged = W0 + s * B @ A                                       # merge_and_unload
unmerged = X @ W0.T + s * (X @ A.T) @ B.T                       # adapter applied on the side
print("merged equals unmerged:", np.allclose(X @ W_merged.T, unmerged))
print("rank of learned update:", np.linalg.matrix_rank(s * B @ A))
print("max error vs true weights:", f"{np.abs(W_merged - (W0 + delta)).max():.1e}")
%%END
<ol><li>We build the situation LoRA is designed for: the "true" fine-tuned layer differs from the base by a low-rank matrix. Real fine-tuning updates are not exactly low-rank, but they are often well approximated by low rank, which is the empirical bet behind LoRA.</li><li>The effective weight is <code>W0 + s * B @ A</code>. The loss at the start equals the base-model loss because B is zero. This is why LoRA adapters begin as an exact no-op.</li><li><code>G</code> is the gradient with respect to the full 64 x 64 weight, computed with the normal layer formula. The two adapter gradients follow from the chain rule for a product of matrices. Only A and B are updated; W0 never changes.</li><li>The loss drops from about 1.06 to about 1e-10 (printed in scientific notation), and the learned update has rank 4 and recovers the hidden change to within about 1e-5.</li><li>Trainable numbers are 512 out of 4096, 12.5 percent here. For a real 4096 x 4096 layer at r = 8 the share is 65,536 / 16,777,216 = 0.39 percent.</li><li>Merging folds the product into the weight; the merged and unmerged outputs agree, which is why <code>merge_and_unload()</code> costs nothing at serving time.</li></ol>
<div class="callout cream"><div class="lab">REAL JOB</div><div class="txt">When fine-tuning with LoRA you manage three choices: <strong>rank r</strong> (capacity; start at 8 or 16), <strong>which layers</strong> to adapt (attention projections first, then add more if underfitting), and <strong>learning rate</strong> (LoRA typically tolerates a higher rate than full fine-tuning). Evaluate on held-out data against the untouched base model with a prompt-only baseline: if prompting is good enough, you do not need to fine-tune.</div></div>
