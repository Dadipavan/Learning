
<h2 id="s21-3">21.3 PyTorch Part 2: nn.Module, Losses, Optimisers and Schedulers</h2>
<div class="callout blue"><div class="lab">INTUITION</div><div class="txt">An <code>nn.Module</code> is a labelled toolbox of parameters plus a recipe (<code>forward</code>) that uses them. The label part matters: when you assign a layer or a parameter as an attribute, the module registers it, so <code>model.parameters()</code> can hand every trainable number to the optimiser, <code>state_dict()</code> can save them, and <code>.to("cuda")</code> can move them. A layer stored in a plain Python list is invisible to all of that.</div></div>
<h3>Reference: modules, losses, optimisers and schedulers</h3>
<div class="tablewrap"><table class="data"><thead><tr><th>Name</th><th>What it does in plain English</th><th>Minimal example (not run here)</th></tr></thead><tbody>
<tr><td><code>nn.Module</code></td><td>Base class: registers parameters and sub-modules</td><td><code>class Net(nn.Module): ...</code></td></tr>
<tr><td><code>nn.Linear(i, o)</code></td><td>Fully connected layer, y = xW<sup>T</sup> + b</td><td><code>nn.Linear(10, 4)</code></td></tr>
<tr><td><code>nn.Sequential</code></td><td>Chain layers; output of one feeds the next</td><td><code>nn.Sequential(nn.Linear(4, 8), nn.ReLU())</code></td></tr>
<tr><td><code>nn.ReLU / GELU</code></td><td>Non-linearities; without them stacked layers collapse into one</td><td><code>nn.GELU()</code></td></tr>
<tr><td><code>nn.Dropout(p)</code></td><td>Randomly zero values in training; identity in eval</td><td><code>nn.Dropout(0.1)</code></td></tr>
<tr><td><code>nn.LayerNorm(d)</code></td><td>Normalise each sample's features (used in transformers)</td><td><code>nn.LayerNorm(768)</code></td></tr>
<tr><td><code>nn.BatchNorm1d(d)</code></td><td>Normalise across the batch; has running statistics</td><td><code>nn.BatchNorm1d(64)</code></td></tr>
<tr><td><code>nn.Embedding(n, d)</code></td><td>Lookup table from integer id to vector</td><td><code>nn.Embedding(30000, 128)</code></td></tr>
<tr><td><code>nn.TransformerEncoderLayer</code></td><td>One attention + feed-forward block</td><td><code>nn.TransformerEncoderLayer(d_model=128, nhead=4, batch_first=True)</code></td></tr>
<tr><td><code>model.parameters()</code></td><td>All trainable tensors (what the optimiser needs)</td><td><code>sum(p.numel() for p in model.parameters())</code></td></tr>
<tr><td><code>model.named_parameters()</code></td><td>Same, with names (inspect, freeze, group)</td><td><code>for n, p in model.named_parameters(): ...</code></td></tr>
<tr><td><code>state_dict / load_state_dict</code></td><td>Dictionary of tensors; the portable way to save</td><td><code>model.load_state_dict(sd)</code></td></tr>
<tr><td><code>model.train() / model.eval()</code></td><td>Switch dropout and batch-norm behaviour</td><td><code>model.eval()</code></td></tr>
<tr><td><code>p.requires_grad_(False)</code></td><td>Freeze a parameter (transfer learning)</td><td><code>for p in base.parameters(): p.requires_grad_(False)</code></td></tr>
<tr><td><code>nn.CrossEntropyLoss</code></td><td>Classification loss from raw logits and integer class ids</td><td><code>nn.CrossEntropyLoss()(logits, y)</code></td></tr>
<tr><td><code>nn.BCEWithLogitsLoss</code></td><td>Binary / multi-label loss from raw logits</td><td><code>nn.BCEWithLogitsLoss(pos_weight=w)</code></td></tr>
<tr><td><code>nn.MSELoss</code></td><td>Mean squared error for regression</td><td><code>nn.MSELoss()(pred, y)</code></td></tr>
<tr><td><code>optim.SGD</code></td><td>Plain gradient step, optional momentum</td><td><code>optim.SGD(ps, lr=0.01, momentum=0.9)</code></td></tr>
<tr><td><code>optim.Adam / AdamW</code></td><td>Adaptive step per parameter; AdamW decouples weight decay</td><td><code>optim.AdamW(ps, lr=3e-4, weight_decay=0.01)</code></td></tr>
<tr><td><code>optimizer.zero_grad()</code></td><td>Clear gradients before the next backward</td><td><code>opt.zero_grad(set_to_none=True)</code></td></tr>
<tr><td><code>optimizer.step()</code></td><td>Apply the update using <code>.grad</code></td><td><code>opt.step()</code></td></tr>
<tr><td><code>lr_scheduler.CosineAnnealingLR</code></td><td>Smoothly decay the learning rate</td><td><code>CosineAnnealingLR(opt, T_max=1000)</code></td></tr>
<tr><td><code>lr_scheduler.OneCycleLR / LambdaLR</code></td><td>Warm-up then decay; or any custom rule</td><td><code>LambdaLR(opt, lambda s: min(1, s / 100))</code></td></tr>
<tr><td><code>clip_grad_norm_</code></td><td>Rescale gradients so their total length is at most a limit</td><td><code>nn.utils.clip_grad_norm_(ps, 1.0)</code></td></tr>
<tr><td><code>nn.init.*</code></td><td>Choose starting values for weights</td><td><code>nn.init.kaiming_normal_(w)</code></td></tr>
</tbody></table></div>
<p>First, the PyTorch way (not run here). The class below is a complete, idiomatic classifier. Read it once, then see the same mechanics built by hand.</p>
%%NORUN
import torch
import torch.nn as nn

class TicketNet(nn.Module):
    def __init__(self, vocab_size, emb_dim=64, hidden=128, n_classes=3, p_drop=0.2):
        super().__init__()                       # REQUIRED: sets up the registry
        self.emb = nn.Embedding(vocab_size, emb_dim, padding_idx=0)
        self.body = nn.Sequential(
            nn.Linear(emb_dim, hidden),
            nn.ReLU(),
            nn.Dropout(p_drop),
            nn.Linear(hidden, n_classes),
        )

    def forward(self, ids, mask):
        # ids: (B, T) int64, mask: (B, T) with 1 for real tokens, 0 for padding
        e = self.emb(ids)                                    # (B, T, E)
        m = mask.unsqueeze(-1).to(e.dtype)                   # (B, T, 1)
        pooled = (e * m).sum(dim=1) / m.sum(dim=1).clamp(min=1)   # mean over real tokens: (B, E)
        return self.body(pooled)                             # logits: (B, n_classes)

model = TicketNet(vocab_size=5000)
print(sum(p.numel() for p in model.parameters()))            # 5000*64 + (64*128+128) + (128*3+3) = 328707
for name, p in model.named_parameters():
    print(name, tuple(p.shape))                              # emb.weight (5000, 64), body.0.weight (128, 64), ...

loss_fn = nn.CrossEntropyLoss()                              # takes LOGITS, not probabilities
opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.01)
%%END
<p>The comment on the parameter count is an arithmetic check you can do yourself: embedding 5000 x 64 = 320,000; first linear 64 x 128 + 128 = 8,320; second linear 128 x 3 + 3 = 387; total 328,707. Counting parameters by hand before running is one of the best shape-debugging habits.</p>
<h3>Building the module system from scratch</h3>
<p>The registry trick is simple: intercept attribute assignment and file parameters and sub-modules into dictionaries. Below is a 40-line NumPy version with <code>Linear</code>, <code>ReLU</code>, <code>Dropout</code> and <code>Sequential</code>, including a hand-written backward pass.</p>
<p class="problem"><span class="pl">Problem 21.3.1</span> Build <code>Sequential(Linear(2,16), ReLU(), Linear(16,2))</code>. List the named parameters, count them (by hand: 2*16 + 16 + 16*2 + 2 = 82) and verify one weight gradient numerically.</p>
%%PY
import numpy as np

class Parameter:
    def __init__(self, data):
        self.data = data
        self.grad = np.zeros_like(data)

class Module:
    def __init__(self):
        object.__setattr__(self, "_params", {})
        object.__setattr__(self, "_mods", {})
        object.__setattr__(self, "training", True)
    def __setattr__(self, name, value):
        if isinstance(value, Parameter):
            self._params[name] = value
        elif isinstance(value, Module):
            self._mods[name] = value
        object.__setattr__(self, name, value)
    def named_parameters(self, prefix=""):
        for k, p in self._params.items():
            yield prefix + k, p
        for k, m in self._mods.items():
            yield from m.named_parameters(prefix + k + ".")
    def parameters(self):
        return [p for _, p in self.named_parameters()]
    def zero_grad(self):
        for p in self.parameters():
            p.grad[...] = 0.0
    def train(self, mode=True):
        object.__setattr__(self, "training", mode)
        for m in self._mods.values():
            m.train(mode)
        return self
    def eval(self):
        return self.train(False)

class Linear(Module):
    def __init__(self, n_in, n_out, rng):
        super().__init__()
        self.weight = Parameter(rng.normal(scale=np.sqrt(2 / n_in), size=(n_in, n_out)))
        self.bias = Parameter(np.zeros(n_out))
    def forward(self, x):
        self.x = x
        return x @ self.weight.data + self.bias.data
    def backward(self, g):
        self.weight.grad += self.x.T @ g
        self.bias.grad += g.sum(axis=0)
        return g @ self.weight.data.T

class ReLU(Module):
    def forward(self, x):
        self.mask = x > 0
        return x * self.mask
    def backward(self, g):
        return g * self.mask

class Sequential(Module):
    def __init__(self, *layers):
        super().__init__()
        for i, layer in enumerate(layers):
            setattr(self, str(i), layer)
        self.layers = layers
    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        return x
    def backward(self, g):
        for layer in reversed(self.layers):
            g = layer.backward(g)
        return g

rng = np.random.default_rng(1)
model = Sequential(Linear(2, 16, rng), ReLU(), Linear(16, 2, rng))
for name, p in model.named_parameters():
    print(f"{name:10s} {p.data.shape}")
print("total parameters:", sum(p.data.size for p in model.parameters()))

x = rng.normal(size=(5, 2))
out = model.forward(x)
print("output shape:", out.shape)
model.zero_grad()
model.backward(np.ones_like(out))            # gradient of sum(out) w.r.t. out is 1
analytic = model.layers[0].weight.grad[0, 0]

w = model.layers[0].weight.data
h = 1e-6
w[0, 0] += h; up = model.forward(x).sum()
w[0, 0] -= 2 * h; down = model.forward(x).sum()
w[0, 0] += h
print("analytic vs numeric:", round(analytic, 5), round((up - down) / (2 * h), 5))
%%END
<ol><li><code>Parameter</code> pairs a number array with a same-shaped gradient array. In PyTorch a <code>Parameter</code> is a tensor flagged as trainable.</li><li><code>Module.__setattr__</code> is the whole registry: when you write <code>self.weight = Parameter(...)</code> it files the object into <code>_params</code>; when you assign a sub-module it files it into <code>_mods</code>. <code>named_parameters</code> walks both, producing dotted names like <code>0.weight</code>.</li><li><code>Linear.forward</code> remembers its input because the backward pass needs it: dW = x<sup>T</sup> g. The bias gradient is the column sum of g, and the gradient passed to the previous layer is g W<sup>T</sup>. These are the same formulas as in 21.2.</li><li><code>Sequential</code> registers its layers under the names "0", "1", "2", which is exactly why PyTorch parameter names look like <code>body.0.weight</code>. It then runs forward in order and backward in reverse order.</li><li>The listing prints four parameter tensors (two weights, two biases) and 82 in total, matching the hand count 32 + 16 + 32 + 2.</li><li>Finally one weight gradient from backward is compared with a finite-difference estimate; they agree to 5 decimals. If a custom layer ever disagrees with the numeric check, the bug is in your backward.</li><li><code>train()</code> and <code>eval()</code> only set a flag on every sub-module. They change nothing by themselves; layers like dropout read the flag.</li></ol>
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Wrong:</strong> <code>self.layers = [nn.Linear(4, 4) for _ in range(3)]</code> inside an <code>nn.Module</code>. <strong>Symptom:</strong> <code>model.parameters()</code> is empty (or misses the layers), the optimiser trains nothing, the loss never moves, and <code>.to("cuda")</code> leaves the layers on the CPU. <strong>Fix:</strong> <code>nn.ModuleList([...])</code> or <code>nn.Sequential(...)</code>, which register their contents. The registry above shows why: only attributes that are <code>Module</code> or <code>Parameter</code> objects are filed.</div></div>
<h3>Dropout and the train/eval switch</h3>
<p>Dropout randomly zeroes a fraction p of the values while training and scales the survivors by 1/(1-p) so the average stays the same ("inverted dropout"). At evaluation it must do nothing. Forgetting <code>model.eval()</code> is the single most common reason for predictions that change between two identical calls.</p>
%%PY
import numpy as np

rng = np.random.default_rng(0)

def dropout(x, p, training, rng):
    if not training or p == 0:
        return x
    keep = rng.random(x.shape) >= p
    return x * keep / (1 - p)

x = np.ones((1, 10))
print("train call 1:", dropout(x, 0.5, True, rng))
print("train call 2:", dropout(x, 0.5, True, rng))
print("eval  call 1:", dropout(x, 0.5, False, rng))

big = np.ones((10000, 1))
print("train mean over 10000 values:", round(dropout(big, 0.3, True, rng).mean(), 3))
%%END
<ol><li>The mask <code>rng.random(shape) &gt;= p</code> keeps each value with probability 1-p. Dividing by 1-p keeps survivors at 2.0 when p = 0.5.</li><li>Two training calls on identical input print different patterns of 0.0 and 2.0, which is why a model left in train mode gives different predictions every time.</li><li>The eval call returns the input unchanged.</li><li>With p = 0.3 over 10,000 values the average stays close to 1.0 (printed above), the whole point of the scaling.</li></ol>
<h3>Losses: why they take logits</h3>
<p>Classification losses in PyTorch (<code>CrossEntropyLoss</code>, <code>BCEWithLogitsLoss</code>) expect <strong>raw scores (logits)</strong>, not probabilities, because they fuse the softmax and the logarithm using the log-sum-exp trick: log softmax(z)<sub>y</sub> = z<sub>y</sub> - log sum exp(z). The gradient of the cross-entropy with respect to the logits has a famously simple form: softmax(z) minus the one-hot label.</p>
<p class="problem"><span class="pl">Problem 21.3.2</span> For logits z = [2.0, 0.5, -1.0] and true class 0, compute the cross-entropy by hand: softmax = [0.7856, 0.1753, 0.0391] (approximately), so the loss is -log 0.7856 = 0.2413 and the gradient is [0.7856 - 1, 0.1753, 0.0391] = [-0.2144, 0.1753, 0.0391]. Verify, and show what happens to a naive loss with huge logits.</p>
%%PY
import numpy as np

def cross_entropy_from_logits(z, y):
    z = z - z.max(axis=1, keepdims=True)
    log_probs = z - np.log(np.exp(z).sum(axis=1, keepdims=True))
    return -log_probs[np.arange(len(y)), y].mean()

def naive_cross_entropy(z, y):
    p = np.exp(z) / np.exp(z).sum(axis=1, keepdims=True)
    return -np.log(p[np.arange(len(y)), y]).mean()

z = np.array([[2.0, 0.5, -1.0]])
y = np.array([0])
p = np.exp(z) / np.exp(z).sum()
print("softmax:", np.round(p, 4))
print("loss:", round(cross_entropy_from_logits(z, y), 4))
print("gradient wrt logits:", np.round(p - np.eye(3)[y], 4))

huge = np.array([[1000.0, 0.0, -5.0]])
with np.errstate(all="ignore"):
    print("naive on huge logits:", naive_cross_entropy(huge, y))
print("stable on huge logits:", cross_entropy_from_logits(huge, y) + 0.0)

# binary version with logits: log(1 + exp(-t*z)) written stably
def bce_with_logits(z, t):
    return np.mean(np.maximum(z, 0) - z * t + np.log1p(np.exp(-np.abs(z))))
print("BCE:", round(bce_with_logits(np.array([2.0, -1.0, 0.5]), np.array([1.0, 0.0, 1.0])), 4))
%%END
<ol><li>The stable version subtracts the row maximum, then computes <code>z - log(sum(exp(z)))</code>. This is what <code>F.log_softmax</code> does and is why <code>CrossEntropyLoss</code> accepts logits.</li><li><code>log_probs[np.arange(len(y)), y]</code> picks, for each row, the log-probability of its true class. In PyTorch the same pick is <code>gather</code> or <code>nll_loss</code>.</li><li>The printed loss is 0.2413 and the gradient is <code>p - onehot</code>, matching the hand calculation: the true class is pushed up (negative gradient means increase), the others pushed down.</li><li>With logits of 1000 the naive formula returns <code>nan</code>, while the stable one returns 0.0 (the model is certain and right; we add 0.0 only to avoid printing a negative zero).</li><li><code>bce_with_logits</code> uses the rewrite max(z,0) - z*t + log(1 + exp(-|z|)), which never overflows. That is the formula inside <code>BCEWithLogitsLoss</code>.</li></ol>
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Wrong:</strong> <code>nn.CrossEntropyLoss()(torch.softmax(logits, -1), y)</code>. <strong>Symptom:</strong> training works but plateaus at a poor accuracy and the loss looks oddly small, because softmax is applied twice. <strong>Fix:</strong> pass raw logits. Apply <code>softmax</code> only when you want probabilities to show a user.</div></div>
<h3>Optimisers: SGD, momentum and Adam by hand</h3>
<p>An optimiser takes the gradient and decides the step. <strong>SGD</strong> subtracts lr times the gradient. <strong>Momentum</strong> keeps a running velocity so steps in a consistent direction speed up and zig-zags cancel. <strong>Adam</strong> keeps running averages of the gradient (m) and of its square (v) and divides one by the root of the other, giving every parameter its own step size. With bias correction the update is: m&#770; = m/(1 - &#946;<sub>1</sub><sup>t</sup>), v&#770; = v/(1 - &#946;<sub>2</sub><sup>t</sup>), w -= lr * m&#770; / (&#8730;v&#770; + &#949;).</p>
<p class="problem"><span class="pl">Problem 21.3.3</span> Minimise the stretched bowl f(x, y) = 0.5 * (x<sup>2</sup> + 100 y<sup>2</sup>) starting at (5, 5). The gradient is (x, 100 y). Compare plain SGD, momentum and Adam after 100 steps. SGD needs lr below 2/100 = 0.02 to stay stable in the steep y direction, which makes it crawl along the shallow x direction.</p>
%%PY
import numpy as np

def f(w):
    return 0.5 * (w[0] ** 2 + 100 * w[1] ** 2)

def grad(w):
    return np.array([w[0], 100 * w[1]])

def run(step_fn, steps=100):
    w = np.array([5.0, 5.0])
    state = {}
    for t in range(1, steps + 1):
        w = step_fn(w, grad(w), state, t)
    return f(w)

def sgd(lr):
    def step(w, g, s, t):
        return w - lr * g
    return step

def momentum(lr, beta=0.9):
    def step(w, g, s, t):
        s["v"] = beta * s.get("v", 0) + g
        return w - lr * s["v"]
    return step

def adam(lr, b1=0.9, b2=0.999, eps=1e-8):
    def step(w, g, s, t):
        s["m"] = b1 * s.get("m", 0) + (1 - b1) * g
        s["v"] = b2 * s.get("v", 0) + (1 - b2) * g ** 2
        mh = s["m"] / (1 - b1 ** t)
        vh = s["v"] / (1 - b2 ** t)
        return w - lr * mh / (np.sqrt(vh) + eps)
    return step

print("start loss:", f(np.array([5.0, 5.0])))
print("SGD lr=0.019      :", round(run(sgd(0.019)), 6))
print("SGD lr=0.021 (too big):", f"{run(sgd(0.021)):.3e}")
print("momentum lr=0.01  :", round(run(momentum(0.01)), 6))
print("Adam lr=0.3       :", round(run(adam(0.3)), 6))
%%END
<ol><li>The two directions have very different curvature: the x direction has curvature 1 and the y direction 100. This "ravine" is the classic reason plain SGD is slow.</li><li>SGD with <code>lr = 0.019</code> is just stable for y (the factor 1 - 100*0.019 = -0.9 shrinks it by 0.9 each step with a sign flip) but x only shrinks by 0.981 per step, so after 100 steps x is still about 5 * 0.981<sup>100</sup> = 0.73 and the loss is about 0.27.</li><li>With <code>lr = 0.021</code> the y factor is 1 - 2.1 = -1.1, so |y| grows 10 percent every step and the loss explodes (printed in scientific notation). That is the classic divergence symptom: a loss that goes to <code>inf</code> then <code>nan</code>.</li><li>Momentum accumulates velocity in the consistent x direction. With an even smaller lr of 0.01 it reaches a loss near 0.002, about a hundred times lower than plain SGD. (Its stability limit is higher, so the safe range is wider.)</li><li>Adam divides by the square root of the running squared gradient, so both coordinates move at a similar speed regardless of curvature. With lr 0.3 it reaches about 0.02: far better than SGD, but with a constant step size it keeps overshooting near the minimum, which is the reason schedulers exist. The exact ranking depends on the problem and the learning rates tried; the lesson is the behaviour, not a winner.</li></ol>
<h3>Learning-rate schedules and gradient clipping</h3>
<p>A common recipe for transformers is <strong>warm-up then cosine decay</strong>: increase the rate linearly from zero for the first few percent of steps (the early gradients are noisy and Adam's statistics are still unreliable), then decay smoothly toward a small floor. In PyTorch you express it with <code>LambdaLR</code> or use <code>get_cosine_schedule_with_warmup</code> from <code>transformers</code>. <strong>Gradient clipping</strong> rescales all gradients together if their combined length exceeds a limit, which prevents one bad batch from wrecking the weights.</p>
%%PY
import numpy as np

def lr_at(step, total, warmup, peak, floor=0.0):
    if step < warmup:
        return peak * step / warmup
    prog = (step - warmup) / max(1, total - warmup)
    return floor + 0.5 * (peak - floor) * (1 + np.cos(np.pi * prog))

for s in [0, 50, 100, 300, 550, 1000]:
    print(f"step {s:4d}  lr {lr_at(s, 1000, 100, 3e-4):.2e}")

def clip_grad_norm(grads, max_norm):
    total = np.sqrt(sum((g ** 2).sum() for g in grads))
    scale = min(1.0, max_norm / (total + 1e-6))
    return [g * scale for g in grads], total

grads = [np.array([3.0, 4.0]), np.array([12.0])]      # global norm = sqrt(9+16+144) = 13
clipped, before = clip_grad_norm(grads, 1.0)
after = np.sqrt(sum((g ** 2).sum() for g in clipped))
print("norm before:", round(before, 3), "after:", round(after, 3))
print("direction kept:", np.round(clipped[0] / np.linalg.norm(clipped[0]), 3), "= [0.6, 0.8]")
%%END
<ol><li><code>lr_at</code> has two phases. Before <code>warmup</code> steps the rate is a straight line from 0 to the peak. After that, <code>prog</code> goes from 0 to 1 and the cosine term goes from 1 to -1, so the rate moves from the peak to the floor along a smooth S curve.</li><li>The printout shows 0 at step 0, half of the peak at step 50, the peak 3.00e-04 at step 100, then decay to 0.00e+00 at step 1000. Halfway through the decay (step 550) the rate is exactly half the peak.</li><li><code>clip_grad_norm</code> computes the <em>global</em> norm across all gradient tensors (13 here), then multiplies every gradient by max_norm / total. The relative direction of the update is unchanged; only its length shrinks to 1.</li><li>In PyTorch you call it after <code>backward()</code> and before <code>step()</code>: <code>torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)</code>. It also returns the pre-clip norm, which is a useful number to log.</li></ol>
<figure><img src="images/lib21_lr_schedules.png" alt="Four learning rate curves: constant, step decay, cosine decay and warmup plus cosine over 1000 steps" loading="lazy"/><figcaption>Figure 21.3. Four common learning-rate schedules over 1000 steps with the same peak rate.</figcaption></figure>
<p><strong>How to read it:</strong> the vertical axis is the learning rate and the horizontal axis is the training step. The purple warm-up curve rises for 100 steps and then follows a cosine down to zero; the step schedule drops by a factor of 10 at fixed moments; constant never changes. Large rates early explore quickly, small rates late settle into a minimum.</p>
<p>The PyTorch equivalents (not run here):</p>
%%NORUN
import torch
from torch.optim.lr_scheduler import LambdaLR, CosineAnnealingLR, OneCycleLR

opt = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.01)

# 1) warm-up then cosine using LambdaLR (the lambda returns a MULTIPLIER of the base lr)
import math
total, warm = 1000, 100
def mult(step):
    if step < warm:
        return step / warm
    prog = (step - warm) / (total - warm)
    return 0.5 * (1 + math.cos(math.pi * prog))
sched = LambdaLR(opt, lr_lambda=mult)

# 2) param groups: different learning rates (or no weight decay on biases and norms)
decay = [p for n, p in model.named_parameters() if p.ndim >= 2]
no_decay = [p for n, p in model.named_parameters() if p.ndim < 2]
opt = torch.optim.AdamW([{"params": decay, "weight_decay": 0.01},
                         {"params": no_decay, "weight_decay": 0.0}], lr=3e-4)

# inside the training loop, the ORDER matters:
#   opt.zero_grad(); loss.backward(); clip_grad_norm_(...); opt.step(); sched.step()
print(opt.param_groups[0]["lr"])      # inspect the current learning rate
%%END
