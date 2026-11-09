
<h2 id="s21-5">21.5 Devices, Memory and Mixed Precision</h2>
<div class="callout blue"><div class="lab">INTUITION</div><div class="txt">A GPU is a separate computer with its own small, fast memory. Data and model must be in <em>that</em> memory to be used there, and copying between the two memories is slow compared with computing. Nearly every "device" error is one of two stories: two things that must be in the same place are not, or there is not enough room for everything you asked to keep.</div></div>
<h3>Reference: device and memory tools</h3>
<div class="tablewrap"><table class="data"><thead><tr><th>Name</th><th>What it does in plain English</th><th>Minimal example (not run here)</th></tr></thead><tbody>
<tr><td><code>torch.cuda.is_available()</code></td><td>Is an NVIDIA GPU usable?</td><td><code>torch.cuda.is_available()</code></td></tr>
<tr><td><code>torch.backends.mps.is_available()</code></td><td>Is the Apple-silicon GPU usable?</td><td><code>torch.backends.mps.is_available()</code></td></tr>
<tr><td><code>torch.device</code></td><td>A device handle</td><td><code>torch.device("cuda:0")</code></td></tr>
<tr><td><code>model.to(device)</code></td><td>Move all parameters in place</td><td><code>model.to(device)</code></td></tr>
<tr><td><code>x.to(device, non_blocking=True)</code></td><td>Copy a tensor (returns a new tensor)</td><td><code>x = x.to(device)</code></td></tr>
<tr><td><code>x.cpu() / x.cuda()</code></td><td>Shortcuts for moving</td><td><code>x.cpu().numpy()</code></td></tr>
<tr><td><code>torch.cuda.memory_allocated()</code></td><td>Bytes held by live tensors</td><td><code>torch.cuda.memory_allocated() / 1e9</code></td></tr>
<tr><td><code>torch.cuda.max_memory_allocated()</code></td><td>Peak bytes since last reset</td><td>log it once per epoch</td></tr>
<tr><td><code>torch.cuda.memory_summary()</code></td><td>Readable report for OOM debugging</td><td><code>print(torch.cuda.memory_summary())</code></td></tr>
<tr><td><code>torch.cuda.empty_cache()</code></td><td>Return cached blocks to the driver (rarely helps)</td><td><code>torch.cuda.empty_cache()</code></td></tr>
<tr><td><code>torch.autocast</code></td><td>Run matmuls in lower precision automatically</td><td><code>with torch.autocast("cuda", dtype=torch.bfloat16): ...</code></td></tr>
<tr><td><code>torch.amp.GradScaler</code></td><td>Scale the loss so float16 gradients do not underflow</td><td><code>scaler = torch.amp.GradScaler()</code></td></tr>
<tr><td><code>torch.utils.checkpoint</code></td><td>Trade compute for memory by recomputing activations</td><td><code>checkpoint(block, x, use_reentrant=False)</code></td></tr>
<tr><td><code>torch.inference_mode()</code></td><td>Fastest no-gradient mode for serving</td><td><code>with torch.inference_mode(): ...</code></td></tr>
<tr><td><code>model.half() / .to(torch.bfloat16)</code></td><td>Cast weights to 16 bits</td><td><code>model.to(torch.bfloat16)</code></td></tr>
<tr><td><code>CUDA_VISIBLE_DEVICES</code></td><td>Environment variable that hides other GPUs</td><td><code>CUDA_VISIBLE_DEVICES=1 python train.py</code></td></tr>
</tbody></table></div>
<p>The standard device boilerplate (not run here). Pick the device once, put it in one variable, and move the <em>model once</em> and every <em>batch</em> each step:</p>
%%NORUN
import torch

if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")
print("using", device)

model = model.to(device)                  # for a Module, .to() is in place
x = x.to(device)                          # for a Tensor, .to() RETURNS a new tensor: assign it!
with torch.autocast(device_type=device.type, dtype=torch.bfloat16, enabled=device.type != "mps"):
    logits = model(x)
print(logits.device, logits.dtype)

if device.type == "cuda":
    print(torch.cuda.get_device_name(0))
    print(torch.cuda.memory_allocated() / 1e9, "GB held,", torch.cuda.max_memory_allocated() / 1e9, "GB peak")
%%END
<h3>How much memory does training need? Do the arithmetic first</h3>
<p>Training memory has four parts: <strong>parameters</strong>, <strong>gradients</strong> (one per parameter), <strong>optimiser state</strong> (Adam keeps two extra numbers per parameter) and <strong>activations</strong> (the intermediate results saved for backward, which grow with batch size and sequence length). The first three depend only on the parameter count P and the bytes per number. In plain fp32 with Adam that is 4 + 4 + 8 = 16 bytes per parameter, before any activations.</p>
<p class="problem"><span class="pl">Problem 21.5.1</span> How much memory do the parameters, gradients and optimiser state need for a 7-billion-parameter model? By hand: 7e9 x 16 bytes = 112e9 bytes = 112 GB (decimal gigabytes). Compare with inference in 16-bit (2 bytes per parameter = 14 GB), a 4-bit quantised copy (0.5 bytes = 3.5 GB) and LoRA fine-tuning where the frozen base is in 16-bit and only 0.5 percent of the parameters train in fp32 with Adam.</p>
%%PY
def training_gb(n_params, w_bytes, g_bytes, opt_bytes, trainable_frac=1.0, base_bytes=None):
    """Bytes for weights + grads + optimiser state (activations excluded)."""
    trainable = n_params * trainable_frac
    frozen = n_params - trainable
    base = frozen * (base_bytes if base_bytes is not None else w_bytes)
    total = base + trainable * (w_bytes + g_bytes + opt_bytes)
    return total / 1e9

P = 7e9
rows = {
    "full fine-tune, fp32 + Adam":      training_gb(P, 4, 4, 8),
    "all bf16 (weights, grads, Adam)":   training_gb(P, 2, 2, 4),
    "LoRA 0.5% trainable, bf16 base":    training_gb(P, 4, 4, 8, trainable_frac=0.005, base_bytes=2),
    "inference, bf16":                   P * 2 / 1e9,
    "inference, 4-bit quantised":        P * 0.5 / 1e9,
}
for name, gb in rows.items():
    print(f"{name:34s} {gb:7.1f} GB")

# batch size finder: halve until the estimate fits, like an OOM retry loop
def max_batch(budget_gb, fixed_gb, per_sample_gb, start=256):
    b = start
    while b > 0 and fixed_gb + b * per_sample_gb > budget_gb:
        b //= 2
    return b
print("largest batch that fits 24 GB with 14.5 GB fixed:", max_batch(24, 14.5, 0.35))
%%END
<ol><li>The function multiplies bytes per parameter for the trainable part and uses a smaller footprint for frozen weights. The first row is the hand calculation: 7e9 x 16 = 112 GB.</li><li>Keeping everything in bf16 (2 + 2 + 4 = 8 bytes per parameter) halves it to 56 GB. This is aggressive and can hurt accuracy because tiny weight updates are lost in 16-bit rounding (see the next example).</li><li>LoRA stores the frozen base at 2 bytes per parameter (about 13.9 GB for the 99.5 percent that is frozen) and pays the 16-byte price only on 0.5 percent of the parameters (0.56 GB), so the total is about 14.5 GB. This is why a model that cannot be fully fine-tuned on one 24 GB GPU can be LoRA-tuned on it.</li><li>The two inference rows show the saving from fewer bits: 14 GB and 3.5 GB.</li><li><code>max_batch</code> imitates the standard defence against out-of-memory errors: start big, halve until it fits. With 24 GB, 14.5 GB already used and an assumed 0.35 GB per sample, it settles on a batch of 16 (0.35 x 16 = 5.6 GB, total 20.1 GB; 32 would need 25.7 GB). The 0.35 GB per sample is an invented illustration; measure your own with <code>max_memory_allocated</code>.</li></ol>
<figure><img src="images/lib21_memory_budget.png" alt="Stacked bars of weights, gradients and optimiser state in gigabytes for a 7 billion parameter model under five setups" loading="lazy"/><figcaption>Figure 21.5. Memory for weights, gradients and optimiser state of a 7-billion-parameter model (activations not included). The numbers are arithmetic from bytes per parameter.</figcaption></figure>
<p><strong>How to read it:</strong> each bar is one setup. Blue is the weights, orange the gradients, teal the optimiser state. The full fp32 bar is dominated by the optimiser and gradients; LoRA and inference bars are almost all blue, because nothing but the (frozen) weights needs to be stored.</p>
<h3>Why precision matters: float16, bfloat16 and float32</h3>
<p>float32 has 8 exponent bits and 23 mantissa bits. float16 has 5 exponent bits and 10 mantissa bits: more precise than bfloat16 but its largest number is only 65,504, so large activations overflow to infinity. bfloat16 keeps float32's 8 exponent bits (same range) but only 7 mantissa bits, so it is coarse yet rarely overflows. That is why bfloat16 needs no loss scaling and float16 does.</p>
%%PY
import numpy as np

print("float16 max:", np.finfo(np.float16).max, " eps:", np.finfo(np.float16).eps)
print("float32 max:", f"{np.finfo(np.float32).max:.3e}", " eps:", f"{np.finfo(np.float32).eps:.3e}")
print("bfloat16 max (computed): ", f"{(2 - 2**-7) * 2.0**127:.3e}", " eps:", 2**-7)

big = np.float32(70000.0)
print("70000 in float16:", np.float16(big))

# emulate bfloat16 by keeping only the top 16 bits of a float32
def to_bf16(x):
    u = np.asarray(x, dtype=np.float32).view(np.uint32)
    return (u & np.uint32(0xFFFF0000)).view(np.float32)
print("70000 in bfloat16 (truncated):", to_bf16(70000.0))

# small updates vanish when added to a large weight
w16 = np.float16(1.0)
print("1.0 + 0.0004 in float16:", w16 + np.float16(0.0004))
print("1.0 + 0.0004 in float32:", np.float32(1.0) + np.float32(0.0004))

# accumulating in low precision stalls
s16, s32 = np.float16(0.0), np.float32(0.0)
for _ in range(20000):
    s16 = np.float16(s16 + np.float16(0.0001))
    s32 = np.float32(s32 + np.float32(0.0001))
print("sum of 20000 x 0.0001 -> float16:", s16, " float32:", round(float(s32), 4))
%%END
<ol><li><code>np.finfo</code> reports the limits of a type. float16 tops out at 65504, so a value of 70000 becomes <code>inf</code>, as the next line shows. This is the overflow that makes float16 training unstable without a loss scaler.</li><li>bfloat16 does not exist in NumPy, so <code>to_bf16</code> emulates it: a float32 is 32 bits, and dropping the lowest 16 bits keeps the sign, the full 8-bit exponent and 7 mantissa bits. 70000 survives, as 69632 after the truncation, which shows the price: only about 2 to 3 significant digits.</li><li>Adding 0.0004 to 1.0 in float16 returns exactly 1.0, because the spacing between neighbouring float16 numbers near 1 is about 0.001. Updates smaller than half that spacing vanish. In float32 the addition works (1.0004).</li><li>The loop adds 0.0001 twenty thousand times. The correct total is 2.0. In float16 the running sum stops growing at 0.25, where the spacing between neighbouring numbers is about 0.0002 and adding 0.0001 rounds back to the same value. Even float32 drifts slightly (2.0002) because 0.0001 is not exactly representable; it is just far more accurate. This is why mixed precision keeps master weights, loss and reductions in float32.</li></ol>
<div class="callout green"><div class="lab">KEY IDEA</div><div class="txt">Mixed precision means: do the heavy matrix multiplications in 16 bits, but keep the sensitive things (master weights, optimiser state, loss, sums) in 32 bits. <code>torch.autocast</code> chooses the precision per operation for you. On recent NVIDIA GPUs prefer bfloat16 (no scaler needed); use float16 with <code>GradScaler</code> on older ones.</div></div>
<h3>Gradient accumulation: a big batch from small pieces</h3>
<p>When a batch of 64 does not fit, run 4 micro-batches of 16, divide each loss by 4, call <code>backward()</code> on each (gradients add up in <code>.grad</code>, which is the accumulation behaviour from 21.2) and call <code>step()</code> once. The result equals the big-batch gradient exactly for losses that are averages over examples. Let us prove it.</p>
%%PY
import numpy as np

rng = np.random.default_rng(3)
X = rng.normal(size=(64, 5)); y = rng.normal(size=64)
w = rng.normal(size=5)

def grad(Xb, yb, w):                       # gradient of the MEAN squared error
    return 2 / len(yb) * Xb.T @ (Xb @ w - yb)

full = grad(X, y, w)

acc = np.zeros(5)
for i in range(0, 64, 16):                 # 4 micro-batches of 16
    acc += grad(X[i:i + 16], y[i:i + 16], w) / 4      # divide by the number of micro-batches
print("identical to full batch:", np.allclose(full, acc))

wrong = np.zeros(5)
for i in range(0, 64, 16):
    wrong += grad(X[i:i + 16], y[i:i + 16], w)        # forgot the division
print("without /4 the gradient is", round(float(wrong[0] / full[0]), 3), "times too large")
%%END
<ol><li>The target is the gradient of the mean squared error over all 64 rows.</li><li>The loop visits four slices of 16 rows. Each slice has its own mean, so averaging four slice-means (each divided by 4 before adding) equals the overall mean when the slices are the same size.</li><li><code>np.allclose</code> prints <code>True</code>.</li><li>If you skip the division, the gradient is 4 times too big, which acts like a learning rate four times larger and may diverge. The printed ratio is 4.0.</li><li>In PyTorch: <code>(loss / accum_steps).backward()</code> every micro-batch, then <code>opt.step(); opt.zero_grad()</code> only every <code>accum_steps</code> micro-batches. Batch-norm statistics still see only the micro-batch, so accumulation is not perfectly identical for networks that use it.</li></ol>
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Wrong:</strong> <code>x.to(device)</code> on its own line, or <code>model = model.to(device)</code> but <code>x = x</code> left on the CPU. <strong>Symptom:</strong> <code>RuntimeError: Expected all tensors to be on the same device</code>. <strong>Fix:</strong> tensors are not moved in place, so write <code>x = x.to(device)</code>; modules are moved in place, so either style works for a model. Move every field of a batch, including masks and labels.</div></div>

<h2 id="s21-6">21.6 The Shape-Debugging Guide</h2>
<p>Most deep learning bugs are shape bugs, and the most dangerous shape bugs do not raise errors: broadcasting silently produces an answer of the wrong size or meaning. The cure is a habit: <strong>write the shape of every tensor in a comment, print shapes at the first batch, and assert the ones that matter.</strong></p>
<div class="tablewrap"><table class="data"><thead><tr><th>Data kind</th><th>Usual shape</th><th>Letters</th></tr></thead><tbody>
<tr><td>Tabular batch</td><td>(B, F)</td><td>B batch, F features</td></tr>
<tr><td>Token ids</td><td>(B, T)</td><td>T sequence length</td></tr>
<tr><td>Embedded tokens</td><td>(B, T, E)</td><td>E embedding size</td></tr>
<tr><td>Multi-head attention tensors</td><td>(B, H, T, D)</td><td>H heads, D = E / H</td></tr>
<tr><td>Attention scores</td><td>(B, H, T, T)</td><td>every token against every token</td></tr>
<tr><td>Images</td><td>(B, C, H, W)</td><td>channels first in PyTorch (NumPy and PIL are channels last)</td></tr>
<tr><td>Classifier logits</td><td>(B, K)</td><td>K classes; labels are (B,) integers</td></tr>
<tr><td>Language-model logits</td><td>(B, T, V)</td><td>V vocabulary; cross-entropy wants (B*T, V) and (B*T,)</td></tr>
</tbody></table></div>
<h3>A shape trace through multi-head attention</h3>
<p>Attention is where shapes get hardest. The code below runs a real multi-head self-attention in NumPy, prints the shape after each step, and uses a tiny <code>check</code> helper that fails loudly with a readable message. Every line has the PyTorch equivalent in its comment.</p>
%%PY
import numpy as np

def check(x, spec, **dims):
    """Assert a shape against letters, e.g. check(x, 'B T E', B=2)."""
    names = spec.split()
    assert x.ndim == len(names), f"expected {len(names)} dims ({spec}), got shape {x.shape}"
    for n, s in zip(names, x.shape):
        if n in dims:
            assert dims[n] == s, f"dim {n}: expected {dims[n]}, got {s} (shape {x.shape})"
        dims[n] = s
    return dims

rng = np.random.default_rng(0)
B, T, E, H = 2, 5, 8, 2
D = E // H
x = rng.normal(size=(B, T, E)); check(x, "B T E", B=B, T=T, E=E)
Wq, Wk, Wv, Wo = (rng.normal(scale=0.3, size=(E, E)) for _ in range(4))
mask = np.array([[1, 1, 1, 1, 1], [1, 1, 1, 0, 0]])          # second ticket has 2 pad tokens

q = x @ Wq                                                     # (B, T, E)
k = x @ Wk
v = x @ Wv
def split_heads(t):                                            # t.view(B, T, H, D).transpose(1, 2)
    return t.reshape(B, T, H, D).transpose(0, 2, 1, 3)         # (B, H, T, D)
qh, kh, vh = split_heads(q), split_heads(k), split_heads(v)
print("heads      :", qh.shape)

scores = qh @ kh.transpose(0, 1, 3, 2) / np.sqrt(D)            # (B, H, T, T)
print("scores     :", scores.shape)
scores = np.where(mask[:, None, None, :] == 1, scores, -1e9)   # mask: (B,1,1,T) broadcasts over H and rows
scores = scores - scores.max(-1, keepdims=True)
att = np.exp(scores); att /= att.sum(-1, keepdims=True)        # softmax over the LAST dim (keys)
print("attention  :", att.shape, " rows sum to 1:", np.allclose(att.sum(-1), 1))
print("pad weight in ticket 2:", round(float(att[1, :, :, 3:].sum()), 6))

ctx = att @ vh                                                 # (B, H, T, D)
merged = ctx.transpose(0, 2, 1, 3).reshape(B, T, E)            # back to (B, T, E)
out = merged @ Wo
print("context    :", ctx.shape, " merged:", merged.shape, " out:", out.shape)
print(check(out, "B T E", B=B, T=T, E=E))

try:
    check(out.reshape(B * T, E), "B T E", B=B)
except AssertionError as e:
    print("caught:", e)
%%END
<ol><li><code>check</code> maps letters to sizes the first time it sees them and verifies them afterwards. It turns a mystery crash 30 lines later into an immediate message that names the dimension.</li><li>Queries, keys and values are the same input multiplied by three weight matrices: shape <code>(B, T, E)</code> each. <code>split_heads</code> reshapes the last dimension E into (H, D) and then moves the head dimension forward, giving <code>(B, H, T, D)</code>. In PyTorch: <code>t.view(B, T, H, D).transpose(1, 2)</code>.</li><li>Scores are every query against every key: <code>(B, H, T, D) @ (B, H, D, T)</code> gives <code>(B, H, T, T)</code>. Dividing by the square root of D keeps the numbers in a range where softmax is not saturated.</li><li>The padding mask has shape <code>(B, T)</code>. Inserting two length-1 axes makes it <code>(B, 1, 1, T)</code>, which broadcasts over heads and over query rows. Masked positions get a huge negative score, so softmax gives them weight 0. The printout confirms the second ticket puts exactly zero attention on its padding.</li><li>Softmax runs over the <em>last</em> axis (the keys), so each query row sums to one.</li><li>After attention, <code>transpose(0, 2, 1, 3)</code> followed by <code>reshape</code> puts the heads side by side again. In PyTorch you must call <code>.contiguous()</code> before <code>.view()</code> here, or use <code>.reshape()</code>.</li><li>The last test feeds a deliberately wrong shape and the helper raises a readable assertion (printed after "caught:").</li></ol>
<figure><img src="images/lib21_attention_shapes.png" alt="Flow chart of tensor shapes through multi-head attention: input B T E, projections, split heads B H T D, scores B H T T, softmax, context, merge, output B T E" loading="lazy"/><figcaption>Figure 21.6. The shape of the tensor after each step of multi-head attention. Only the last two or three dimensions change meaning at each step.</figcaption></figure>
<p><strong>How to read it:</strong> follow the boxes from left to right. The batch dimension B never changes. The blue boxes are projections, the orange ones are the head split and merge (pure shape changes with no arithmetic), and the red box is the only place where T appears twice, which is why attention memory grows with the square of the sequence length.</p>
<h3>The silent broadcasting bug</h3>
<p>Not every shape bug crashes. Subtracting a column from a row broadcasts into a full matrix, a classic cause of a loss that "works" but never improves.</p>
%%PY
import numpy as np

pred = np.array([0.9, 0.2, 0.7, 0.4])            # shape (4,)
target = np.array([[1.0], [0.0], [1.0], [0.0]])  # shape (4, 1), e.g. from y.unsqueeze(1)

diff = pred - target                             # (4,) - (4,1) -> (4,4)
print("diff shape:", diff.shape)
print("wrong MSE :", round(float(np.mean(diff ** 2)), 4))

fixed = pred - target.ravel()                    # both (4,)
print("right MSE :", round(float(np.mean(fixed ** 2)), 4))
%%END
<ol><li>A vector of shape <code>(4,)</code> aligned from the right with <code>(4, 1)</code> becomes <code>(1, 4)</code> versus <code>(4, 1)</code>, so both stretch to <code>(4, 4)</code>: every prediction is compared with every target.</li><li>The wrong mean is computed over 16 meaningless pairs and is much larger than the true error; the right one is over 4 matching pairs.</li><li>No exception occurs. PyTorch's <code>nn.MSELoss</code> warns in this case ("Using a target size that is different to the input size"), but your own arithmetic does not.</li><li>Defence: assert <code>pred.shape == target.shape</code> before computing a custom loss.</li></ol>
