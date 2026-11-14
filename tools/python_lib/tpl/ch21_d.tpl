
<h2 id="s21-4">21.4 PyTorch Part 3: Datasets, DataLoader, the Training Loop and Saving</h2>
<div class="callout blue"><div class="lab">INTUITION</div><div class="txt">The <code>Dataset</code> answers "give me item number i". The <code>DataLoader</code> is a waiter: it decides the order (shuffling), collects items into trays (batches), and uses a <em>collate function</em> to stack uneven items into one rectangular tensor. The training loop is the kitchen routine: for each tray, predict, measure the error, clear old gradients, backpropagate, step. Once you can write that routine from memory you can debug any framework built on it, including the Hugging Face <code>Trainer</code>.</div></div>
<h3>Reference: data, training and saving</h3>
<div class="tablewrap"><table class="data"><thead><tr><th>Name</th><th>What it does in plain English</th><th>Minimal example (not run here)</th></tr></thead><tbody>
<tr><td><code>Dataset</code></td><td>Your class with <code>__len__</code> and <code>__getitem__</code></td><td><code>def __getitem__(self, i): return self.x[i], self.y[i]</code></td></tr>
<tr><td><code>TensorDataset</code></td><td>Wrap tensors that share the first dimension</td><td><code>TensorDataset(X, y)</code></td></tr>
<tr><td><code>IterableDataset</code></td><td>Stream items without random access (huge files)</td><td><code>class Stream(IterableDataset): def __iter__(self): ...</code></td></tr>
<tr><td><code>DataLoader</code></td><td>Batches, shuffles and (optionally) parallelises loading</td><td><code>DataLoader(ds, batch_size=32, shuffle=True)</code></td></tr>
<tr><td><code>shuffle=True</code></td><td>New random order each epoch (train only)</td><td><code>DataLoader(train, shuffle=True)</code></td></tr>
<tr><td><code>num_workers</code></td><td>Background processes that prepare batches</td><td><code>DataLoader(ds, num_workers=4)</code></td></tr>
<tr><td><code>pin_memory=True</code></td><td>Page-locked host memory for faster GPU copies</td><td><code>DataLoader(ds, pin_memory=True)</code></td></tr>
<tr><td><code>drop_last=True</code></td><td>Discard the final short batch</td><td><code>DataLoader(ds, drop_last=True)</code></td></tr>
<tr><td><code>collate_fn</code></td><td>Your function that merges a list of items into a batch</td><td><code>DataLoader(ds, collate_fn=pad_collate)</code></td></tr>
<tr><td><code>random_split</code></td><td>Split a dataset into train/validation parts</td><td><code>random_split(ds, [0.8, 0.2], generator=g)</code></td></tr>
<tr><td><code>WeightedRandomSampler</code></td><td>Oversample rare classes</td><td><code>DataLoader(ds, sampler=sampler)</code></td></tr>
<tr><td><code>pad_sequence</code></td><td>Pad a list of tensors to equal length</td><td><code>pad_sequence(seqs, batch_first=True)</code></td></tr>
<tr><td><code>model.train() / eval()</code></td><td>Switch layer behaviour</td><td><code>model.eval()</code></td></tr>
<tr><td><code>torch.no_grad() / inference_mode()</code></td><td>Skip graph building in evaluation</td><td><code>with torch.inference_mode(): ...</code></td></tr>
<tr><td><code>loss.backward()</code></td><td>Compute gradients</td><td><code>loss.backward()</code></td></tr>
<tr><td><code>torch.save</code></td><td>Write a checkpoint (use a dict of state_dicts)</td><td><code>torch.save({"model": m.state_dict()}, "ck.pt")</code></td></tr>
<tr><td><code>torch.load(weights_only=True)</code></td><td>Read it back safely (never load untrusted pickles)</td><td><code>torch.load("ck.pt", map_location="cpu", weights_only=True)</code></td></tr>
<tr><td><code>load_state_dict(strict)</code></td><td>Copy tensors into a model; <code>strict=False</code> reports mismatches</td><td><code>model.load_state_dict(sd)</code></td></tr>
<tr><td><code>torch.manual_seed</code></td><td>Reproducible init and shuffling</td><td><code>torch.manual_seed(42)</code></td></tr>
<tr><td><code>worker_init_fn / generator</code></td><td>Seed each loader worker and the shuffle order</td><td><code>DataLoader(ds, generator=g)</code></td></tr>
<tr><td><code>SummaryWriter</code></td><td>Log scalars for TensorBoard</td><td><code>writer.add_scalar("loss", v, step)</code></td></tr>
</tbody></table></div>
<h3>A DataLoader with padding, built by hand</h3>
<p>Sentences have different lengths, but a tensor must be rectangular. The collate function pads short sequences with a pad id (0 here) and builds a <strong>mask</strong> that is 1 for real tokens and 0 for padding, so the model can ignore the padding. This is the single most common reason a hand-written <code>DataLoader</code> breaks ("expected sequence of length 5 at dim 1 (got 3)").</p>
<p class="problem"><span class="pl">Problem 21.4.1</span> Seven tickets are lists of token ids with lengths 3, 5, 2, 4, 6, 2, 3. Batch them in threes without shuffling, then with <code>drop_last</code>, and show the padded matrix and mask for the first batch.</p>
%%PY
import numpy as np

class TicketDataset:
    def __init__(self, seqs, labels):
        self.seqs, self.labels = seqs, labels
    def __len__(self):
        return len(self.seqs)
    def __getitem__(self, i):
        return self.seqs[i], self.labels[i]

def pad_collate(items, pad_id=0):
    seqs, labels = zip(*items)
    longest = max(len(s) for s in seqs)
    ids = np.full((len(seqs), longest), pad_id, dtype=np.int64)
    mask = np.zeros((len(seqs), longest), dtype=np.int64)
    for r, s in enumerate(seqs):
        ids[r, :len(s)] = s
        mask[r, :len(s)] = 1
    return ids, mask, np.array(labels, dtype=np.int64)

class DataLoader:
    def __init__(self, ds, batch_size, shuffle=False, drop_last=False, collate_fn=pad_collate, seed=0):
        self.ds, self.bs, self.shuffle = ds, batch_size, shuffle
        self.drop_last, self.collate, self.rng = drop_last, collate_fn, np.random.default_rng(seed)
    def __len__(self):
        n = len(self.ds)
        return n // self.bs if self.drop_last else -(-n // self.bs)
    def __iter__(self):
        order = self.rng.permutation(len(self.ds)) if self.shuffle else np.arange(len(self.ds))
        for start in range(0, len(order), self.bs):
            idx = order[start:start + self.bs]
            if self.drop_last and len(idx) < self.bs:
                break
            yield self.collate([self.ds[int(i)] for i in idx])

seqs = [[5, 6, 7], [8, 9, 10, 11, 12], [13, 14], [15, 16, 17, 18], [19, 20, 21, 22, 23, 24], [25, 26], [27, 28, 29]]
ds = TicketDataset(seqs, [0, 1, 2, 0, 1, 2, 0])

dl = DataLoader(ds, batch_size=3)
print("batches:", len(dl), "| with drop_last:", len(DataLoader(ds, 3, drop_last=True)))
for ids, mask, y in dl:
    print("ids", ids.shape, "mask", mask.shape, "labels", y)
ids, mask, y = next(iter(dl))
print(ids)
print(mask)
first = [int(y.sum()) for _, _, y in DataLoader(ds, 3, shuffle=True, seed=1)]
print("shuffled label sums per batch:", first)
%%END
<ol><li><code>TicketDataset</code> follows the PyTorch contract: <code>__len__</code> says how many items exist and <code>__getitem__</code> returns one item. Nothing is loaded until asked, which is how a Dataset can wrap a million files.</li><li><code>pad_collate</code> receives a <em>list</em> of items from <code>__getitem__</code>. It finds the longest sequence in <em>this batch only</em>, allocates a rectangle filled with the pad id, copies each sequence into its row, and sets the mask to 1 on real positions. Padding to the batch maximum, not the global maximum, saves compute.</li><li><code>__len__</code> uses ceiling division: 7 items in batches of 3 give 3 batches (3, 3 and 1). With <code>drop_last</code> the short last batch is discarded, giving 2.</li><li>Iterating prints shapes <code>(3, 5)</code>, <code>(3, 6)</code> and <code>(1, 3)</code>: the second dimension changes per batch, because lengths differ. A model must therefore accept any sequence length.</li><li>The matrix shows token ids with zeros on the right and the mask with ones exactly where ids are real.</li><li>With <code>shuffle=True</code> the permutation changes the batch contents. The seed makes the order repeatable; in PyTorch pass <code>generator=torch.Generator().manual_seed(1)</code>.</li></ol>
<p>The PyTorch version (not run here). The real <code>DataLoader</code> adds workers, pinned memory and many more safety checks, but the collate idea is identical:</p>
%%NORUN
import torch
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence

class TicketDataset(Dataset):
    def __init__(self, seqs, labels):
        self.seqs, self.labels = seqs, labels
    def __len__(self):
        return len(self.seqs)
    def __getitem__(self, i):
        return torch.tensor(self.seqs[i]), self.labels[i]

def pad_collate(items):
    seqs, labels = zip(*items)
    ids = pad_sequence(seqs, batch_first=True, padding_value=0)      # (B, T_max)
    mask = (ids != 0).long()
    return ids, mask, torch.tensor(labels)

g = torch.Generator().manual_seed(0)
train_dl = DataLoader(TicketDataset(seqs, labels), batch_size=32, shuffle=True,
                      collate_fn=pad_collate, num_workers=2, pin_memory=True,
                      drop_last=False, generator=g)
%%END
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Wrong:</strong> using <code>shuffle=True</code> on the validation loader and, on the training loader, forgetting it. <strong>Symptom:</strong> training on sorted or grouped data (all class 0 first, then class 1) makes the loss oscillate wildly and the model memorise the last class it saw; a shuffled validation loader is harmless but wasteful and makes batch-by-batch logs impossible to compare. <strong>Fix:</strong> shuffle training only.</div></div>
<h3>The complete training loop</h3>
<p>Now the full routine in a form you can compare line by line with PyTorch: mini-batches, an Adam optimiser, a validation pass without gradient tracking, <strong>early stopping</strong> (stop when validation loss has not improved for 30 epochs), and keeping the best weights. We deliberately use a tiny training set (60 points) and a wide hidden layer so the model overfits and you can watch it happen.</p>
<p class="problem"><span class="pl">Problem 21.4.2</span> Train a 2-64-2 network on 60 noisy "two moons" points, validate on 340 others, stop early, then save and reload the best checkpoint and confirm identical predictions.</p>
%%PY
import numpy as np, tempfile, os
from sklearn.datasets import make_moons

X, y = make_moons(n_samples=400, noise=0.35, random_state=0)
X = (X - X.mean(0)) / X.std(0)
Xtr, ytr, Xva, yva = X[:60], y[:60], X[60:], y[60:]

class MLP:
    def __init__(self, sizes, rng):
        self.W = [rng.normal(scale=np.sqrt(2 / a), size=(a, b)) for a, b in zip(sizes[:-1], sizes[1:])]
        self.b = [np.zeros(b) for b in sizes[1:]]
    def params(self):
        return self.W + self.b
    def forward(self, x):
        self.acts = [x]
        for i, (W, b) in enumerate(zip(self.W, self.b)):
            x = x @ W + b
            if i < len(self.W) - 1:
                x = np.maximum(x, 0)
            self.acts.append(x)
        return x
    def backward(self, g):
        gW, gb = [None] * len(self.W), [None] * len(self.W)
        for i in reversed(range(len(self.W))):
            gW[i] = self.acts[i].T @ g
            gb[i] = g.sum(0)
            if i > 0:
                g = (g @ self.W[i].T) * (self.acts[i] > 0)
        return gW + gb

class Adam:
    def __init__(self, params, lr=0.01, b1=0.9, b2=0.999, eps=1e-8):
        self.p, self.lr, self.b1, self.b2, self.eps, self.t = params, lr, b1, b2, eps, 0
        self.m = [np.zeros_like(q) for q in params]
        self.v = [np.zeros_like(q) for q in params]
    def step(self, grads):
        self.t += 1
        for q, g, m, v in zip(self.p, grads, self.m, self.v):
            m *= self.b1; m += (1 - self.b1) * g
            v *= self.b2; v += (1 - self.b2) * g * g
            q -= self.lr * (m / (1 - self.b1 ** self.t)) / (np.sqrt(v / (1 - self.b2 ** self.t)) + self.eps)

def ce_loss_grad(logits, y):
    z = logits - logits.max(1, keepdims=True)
    p = np.exp(z); p /= p.sum(1, keepdims=True)
    loss = -np.log(p[np.arange(len(y)), y]).mean()
    p[np.arange(len(y)), y] -= 1
    return loss, p / len(y)

def evaluate(model, X, y):                  # like model.eval() + torch.no_grad()
    logits = model.forward(X)
    loss, _ = ce_loss_grad(logits, y)
    return loss, (logits.argmax(1) == y).mean()

rng = np.random.default_rng(0)
model = MLP([2, 64, 2], rng)
opt = Adam(model.params(), lr=0.01)
best_loss, best_state, best_epoch, bad = 1e9, None, -1, 0

for epoch in range(1, 301):
    order = rng.permutation(len(Xtr))
    total = 0.0
    for i in range(0, len(order), 16):
        idx = order[i:i + 16]
        logits = model.forward(Xtr[idx])              # forward
        loss, g = ce_loss_grad(logits, ytr[idx])      # loss
        grads = model.backward(g)                     # backward
        opt.step(grads)                               # optimiser step
        total += loss * len(idx)
    val_loss, val_acc = evaluate(model, Xva, yva)
    if val_loss < best_loss - 1e-4:
        best_loss, best_epoch, bad = val_loss, epoch, 0
        best_state = [q.copy() for q in model.params()]
    else:
        bad += 1
    if epoch % 20 == 0:
        print(f"epoch {epoch:3d} train {total/len(Xtr):.4f} val {val_loss:.4f} acc {val_acc:.3f}")
    if bad >= 30:
        print(f"early stop at epoch {epoch}; best epoch {best_epoch} (val loss {best_loss:.4f})")
        break

path = os.path.join(tempfile.mkdtemp(), "best.npz")
np.savez(path, *best_state)                                   # like torch.save(state_dict)
fresh = MLP([2, 64, 2], np.random.default_rng(99))            # different random init
loaded = np.load(path)
for q, key in zip(fresh.params(), loaded.files):
    q[...] = loaded[key]                                      # like load_state_dict
for q, s in zip(model.params(), best_state):
    q[...] = s
print("reloaded predictions identical:", np.array_equal(fresh.forward(Xva), model.forward(Xva)))
print("final val accuracy of best model:", round(evaluate(fresh, Xva, yva)[1], 3))
%%END
<ol><li>Standardising the features (mean 0, standard deviation 1) is the same preprocessing you would do before any neural network; unscaled inputs make learning slow and unstable.</li><li>The <code>MLP</code> keeps the layer inputs in <code>self.acts</code> during <code>forward</code> because the backward pass needs them. This is the memory PyTorch calls <em>activations</em>, and it is why training uses far more memory than inference (see 21.5).</li><li>Each mini-batch of 16 runs the four-step heartbeat: forward, loss, backward, step. In PyTorch you would also call <code>opt.zero_grad()</code>; here the gradients are fresh arrays each time, so there is nothing to clear.</li><li>The cross-entropy function returns the loss <em>and</em> the gradient <code>(softmax - onehot) / batch</code>, which is what <code>loss.backward()</code> would start the chain with.</li><li><code>evaluate</code> never calls <code>backward</code> or the optimiser, the equivalent of <code>model.eval()</code> plus <code>torch.no_grad()</code>.</li><li>Look at the printed table: training loss keeps falling while validation loss reaches its minimum around epoch 53 and then rises. That divergence is overfitting, and early stopping watches for it. Patience 30 stops the run at epoch 83.</li><li>We keep a copy of the weights at the best epoch (<code>q.copy()</code>; without the copy the saved weights would silently keep changing because they are views of the live parameters).</li><li>Saving writes the arrays to disk, and loading copies them into a model that started from a different random seed. The check prints <code>True</code>: the checkpoint fully determines the model.</li></ol>
<figure><img src="images/lib21_training_curves.png" alt="Training loss falling steadily while validation loss reaches a minimum near epoch 53 then rises, with the early-stopping point marked" loading="lazy"/><figcaption>Figure 21.4. Training and validation loss from the run above. The dashed line marks the best epoch that early stopping restores.</figcaption></figure>
<p><strong>How to read it:</strong> the blue training curve only goes down, because the network can memorise 60 points. The orange validation curve bottoms out and climbs: from that point extra training makes the model worse on new data. The gap between the curves is the generalisation gap.</p>
<p>The same loop in PyTorch (not run here). Compare it line by line with the NumPy version:</p>
%%NORUN
import copy, torch
import torch.nn as nn

device = "cuda" if torch.cuda.is_available() else "cpu"
model = TicketNet(vocab_size=5000).to(device)
loss_fn = nn.CrossEntropyLoss()
opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.01)

@torch.no_grad()
def evaluate(model, loader):
    model.eval()
    total, correct, n = 0.0, 0, 0
    for ids, mask, y in loader:
        ids, mask, y = ids.to(device), mask.to(device), y.to(device)
        logits = model(ids, mask)
        total += loss_fn(logits, y).item() * len(y)
        correct += (logits.argmax(dim=-1) == y).sum().item()
        n += len(y)
    return total / n, correct / n

best_loss, best_state, bad = float("inf"), None, 0
for epoch in range(100):
    model.train()
    for ids, mask, y in train_dl:
        ids, mask, y = ids.to(device), mask.to(device), y.to(device)
        opt.zero_grad(set_to_none=True)
        loss = loss_fn(model(ids, mask), y)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
    val_loss, val_acc = evaluate(model, val_dl)
    if val_loss < best_loss - 1e-4:
        best_loss, bad = val_loss, 0
        best_state = copy.deepcopy(model.state_dict())     # deepcopy, or it keeps changing
    else:
        bad += 1
        if bad >= 5:
            break

model.load_state_dict(best_state)
torch.save({"model": model.state_dict(), "epoch": epoch, "val_loss": best_loss}, "best.pt")

# later, in another process (weights_only=True is the safe default in recent versions):
ckpt = torch.load("best.pt", map_location="cpu", weights_only=True)
new_model = TicketNet(vocab_size=5000)
new_model.load_state_dict(ckpt["model"])
new_model.eval()
%%END
<div class="callout cream"><div class="lab">REAL JOB</div><div class="txt">Save the <strong>state_dict</strong>, not the whole model object. Pickling the object ties the file to your exact class and module path, so it breaks when you refactor, and loading untrusted pickles can run arbitrary code. A state_dict is just named tensors, and the safetensors format used by Hugging Face stores them without pickle at all. Also save the config (layer sizes, vocab) next to the weights, because a state_dict cannot rebuild the architecture.</div></div>
