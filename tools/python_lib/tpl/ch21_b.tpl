
<h2 id="s21-2">21.2 PyTorch Part 1: Tensors and Autograd</h2>
<div class="callout blue"><div class="lab">INTUITION</div><div class="txt">A PyTorch tensor is a NumPy array with two extra powers: it can live on a GPU, and it can <em>remember the operations that created it</em>. That memory is a recorded recipe (a graph). When you call <code>.backward()</code> PyTorch walks the recipe backwards and fills in the slope of the loss for every number you marked as trainable. Think of a cooking show: the forward pass cooks the dish while writing the recipe, the backward pass reads the recipe in reverse to say how much each ingredient mattered.</div></div>
<h3>Reference: the 24 tensor functions you will use daily</h3>
<div class="tablewrap"><table class="data"><thead><tr><th>Name</th><th>What it does in plain English</th><th>Minimal example (not run here)</th></tr></thead><tbody>
<tr><td><code>torch.tensor</code></td><td>Make a tensor from Python numbers (copies the data)</td><td><code>torch.tensor([[1., 2.], [3., 4.]])</code></td></tr>
<tr><td><code>torch.zeros / ones / full</code></td><td>Filled tensors of a given shape</td><td><code>torch.zeros(2, 3)</code></td></tr>
<tr><td><code>torch.arange / linspace</code></td><td>Evenly spaced values</td><td><code>torch.arange(0, 10, 2)</code></td></tr>
<tr><td><code>torch.manual_seed</code></td><td>Fix the random generator so runs repeat</td><td><code>torch.manual_seed(0)</code></td></tr>
<tr><td><code>torch.randn / rand / randint</code></td><td>Random normal, uniform, integers</td><td><code>torch.randn(4, 3)</code></td></tr>
<tr><td><code>torch.from_numpy / .numpy()</code></td><td>Share memory with a NumPy array (CPU only)</td><td><code>torch.from_numpy(arr)</code></td></tr>
<tr><td><code>x.shape, x.dtype, x.device</code></td><td>The three facts to check first when anything breaks</td><td><code>print(x.shape, x.dtype, x.device)</code></td></tr>
<tr><td><code>x.to(...)</code></td><td>Move to a device and/or change dtype</td><td><code>x.to("cuda")</code>, <code>x.to(torch.float16)</code></td></tr>
<tr><td><code>x.view / x.reshape</code></td><td>Same numbers, new shape (<code>view</code> needs contiguous memory)</td><td><code>x.reshape(-1, 4)</code></td></tr>
<tr><td><code>x.permute / x.transpose</code></td><td>Reorder dimensions (a view, often non-contiguous)</td><td><code>x.permute(0, 2, 1)</code></td></tr>
<tr><td><code>x.unsqueeze / x.squeeze</code></td><td>Add or remove a length-1 dimension</td><td><code>x.unsqueeze(0)</code></td></tr>
<tr><td><code>torch.cat / torch.stack</code></td><td>Join along an existing / a new dimension</td><td><code>torch.stack([a, b])</code></td></tr>
<tr><td><code>@ / torch.matmul</code></td><td>Matrix product, batched when there are leading dimensions</td><td><code>a @ b</code></td></tr>
<tr><td><code>torch.einsum</code></td><td>Any product or reduction written as index letters</td><td><code>torch.einsum("bij,bjk-&gt;bik", a, b)</code></td></tr>
<tr><td><code>x.sum / mean / max (dim, keepdim)</code></td><td>Reduce along a dimension</td><td><code>x.sum(dim=1, keepdim=True)</code></td></tr>
<tr><td><code>x.argmax</code></td><td>Index of the largest value (turn logits into a class)</td><td><code>logits.argmax(dim=-1)</code></td></tr>
<tr><td><code>torch.softmax</code></td><td>Turn scores into probabilities along a dimension</td><td><code>torch.softmax(z, dim=-1)</code></td></tr>
<tr><td><code>torch.where / masked_fill</code></td><td>Choose elementwise / overwrite where a mask is true</td><td><code>x.masked_fill(mask, -1e9)</code></td></tr>
<tr><td><code>x.gather</code></td><td>Pick one entry per row using index tensor</td><td><code>logp.gather(1, y.unsqueeze(1))</code></td></tr>
<tr><td><code>x.item()</code></td><td>One-element tensor to a Python number</td><td><code>loss.item()</code></td></tr>
<tr><td><code>x.requires_grad_()</code></td><td>Start recording operations on this tensor</td><td><code>w = torch.randn(3, requires_grad=True)</code></td></tr>
<tr><td><code>loss.backward()</code></td><td>Fill <code>.grad</code> for every tracked leaf</td><td><code>loss.backward(); w.grad</code></td></tr>
<tr><td><code>torch.no_grad()</code></td><td>Stop recording (evaluation, inference)</td><td><code>with torch.no_grad(): y = model(x)</code></td></tr>
<tr><td><code>x.detach()</code></td><td>Same data, cut from the graph</td><td><code>x.detach().cpu().numpy()</code></td></tr>
<tr><td><code>x.clone()</code></td><td>Real copy (otherwise slices share memory)</td><td><code>y = x.clone()</code></td></tr>
</tbody></table></div>
<p>The names and ideas are the same as in NumPy, so we first practise the mechanics where we can run them. The first example covers shapes, dtypes, and the most important distinction in the whole chapter: a <strong>view</strong> shares memory, a <strong>copy</strong> does not.</p>
<p class="problem"><span class="pl">Problem 21.2.1</span> Build a batch of 2 tickets, each with 3 tokens, each token a 4-number vector. Reshape it, take a slice, and prove whether the slice shares memory with the original.</p>
<table class="steps"><tr><th>Idea</th><td>NumPy plays the part of <code>torch</code>: <code>reshape</code>, slicing and transposing return views; <code>copy()</code> returns new memory. PyTorch behaves the same way.</td></tr><tr><th>Check</th><td><code>np.shares_memory(a, b)</code> answers the question directly. In PyTorch compare <code>a.data_ptr()</code> or <code>a.untyped_storage().data_ptr()</code>.</td></tr></table>
%%PY
import numpy as np

x = np.arange(24, dtype=np.float32).reshape(2, 3, 4)   # (batch, tokens, features)
print("shape", x.shape, "dtype", x.dtype, "bytes", x.nbytes)

flat = x.reshape(6, 4)            # merge batch and tokens
first_ticket = x[0]               # a slice
copy = x[0].copy()
swapped = x.transpose(0, 2, 1)    # (batch, features, tokens)

print("flat shares memory:", np.shares_memory(x, flat))
print("slice shares memory:", np.shares_memory(x, first_ticket))
print("copy shares memory:", np.shares_memory(x, copy))
print("transposed shape:", swapped.shape, "contiguous:", swapped.flags["C_CONTIGUOUS"])

first_ticket[0, 0] = 99.0          # write through the view
print("x[0,0,0] is now", x[0, 0, 0], "and copy[0,0] is still", copy[0, 0])
%%END
<ol><li>Line 3 builds 24 numbers and shapes them as <code>(2, 3, 4)</code>. Read shapes left to right as "2 tickets, 3 tokens, 4 features". <code>float32</code> uses 4 bytes per number, so 24 numbers need 96 bytes.</li><li>Lines 7 to 10 create four relatives of <code>x</code>. <code>reshape</code> and a slice are views. <code>.copy()</code> allocates new memory. <code>transpose</code> only changes how the same memory is walked (the strides), so it is also a view.</li><li>The three <code>shares_memory</code> lines print <code>True</code>, <code>True</code>, <code>False</code>. A view costs nothing but is dangerous if you modify it.</li><li>The transposed array is no longer C-contiguous (<code>False</code>). In PyTorch this is exactly the case where <code>.view()</code> raises an error and <code>.reshape()</code> or <code>.contiguous()</code> is needed.</li><li>The last two lines write 99.0 through the slice. The original changes too, while the copy keeps the old value 0.0.</li></ol>
<p>Now the PyTorch version of the same ideas. This is what you would run on a machine with torch installed (not run here):</p>
%%NORUN
import torch

torch.manual_seed(0)
x = torch.arange(24, dtype=torch.float32).reshape(2, 3, 4)
print(x.shape, x.dtype, x.device, x.element_size() * x.nelement())

flat = x.reshape(6, 4)             # view when possible
copy = x[0].clone()                # real copy
swapped = x.transpose(1, 2)        # (2, 4, 3), non-contiguous
print(swapped.is_contiguous())     # False
try:
    swapped.view(8, 3)             # fails: view needs contiguous memory
except RuntimeError as e:
    print("view failed:", str(e)[:60])
ok = swapped.reshape(8, 3)         # reshape silently copies when it has to
ok2 = swapped.contiguous().view(8, 3)
%%END
<h3>Broadcasting, reductions and a stable softmax</h3>
<p><strong>Broadcasting</strong> is the rule that lets arrays of different shapes combine. Line the shapes up from the <em>right</em>; two dimensions are compatible when they are equal or one of them is 1; a missing dimension counts as 1. It saves memory and loops, and it silently produces nonsense if you get a shape wrong, which is why the shape-debugging guide in 21.6 matters.</p>
<p class="problem"><span class="pl">Problem 21.2.2</span> Scores for 3 tickets over 4 classes are given. Convert them to probabilities with a numerically safe softmax, using keepdims, and show why subtracting the row maximum matters.</p>
<table class="steps"><tr><th>Formula</th><td>softmax(z)<sub>i</sub> = exp(z<sub>i</sub>) / sum<sub>j</sub> exp(z<sub>j</sub>). Subtracting any constant c from every z<sub>i</sub> leaves the answer unchanged.</td></tr><tr><th>Trap</th><td><code>exp(1000)</code> overflows to infinity. Subtract the row maximum first so the largest exponent is <code>exp(0) = 1</code>.</td></tr></table>
%%PY
import numpy as np

z = np.array([[2.0, 1.0, 0.1, -1.0],
              [1000.0, 999.0, 998.0, 0.0],
              [0.0, 0.0, 0.0, 0.0]], dtype=np.float64)

def softmax_naive(z):
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)

def softmax_stable(z):
    z = z - z.max(axis=1, keepdims=True)      # (3,4) - (3,1) broadcasts
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)

with np.errstate(over="ignore", invalid="ignore"):
    print("naive row 1:", softmax_naive(z)[1])
print("stable row 1:", np.round(softmax_stable(z)[1], 4))
p = softmax_stable(z)
print("rows sum to", p.sum(axis=1))
print("argmax per row:", p.argmax(axis=1))
print("uniform row:", p[2])
%%END
<ol><li><code>z.max(axis=1, keepdims=True)</code> has shape <code>(3, 1)</code>. Without <code>keepdims=True</code> it would have shape <code>(3,)</code>, and <code>(3, 4) - (3,)</code> would try to align 3 with 4 and fail (or worse, succeed with the wrong meaning when the sizes happen to match).</li><li>The naive version overflows for 1000: <code>exp(1000)</code> is infinity and infinity divided by infinity is <code>nan</code>. The first printed line shows <code>nan</code> for the three large entries (the last entry, <code>exp(0)/inf</code>, becomes 0).</li><li>The stable version gives the true probabilities, about 0.665, 0.245, 0.09 and 0.0 for row 1, because after subtraction the row becomes <code>[0, -1, -2, -1000]</code>.</li><li>Each row sums to 1, <code>argmax</code> picks class 0 for every row (on the all-zero row it is a tie and the first index wins), and that all-zero row becomes the uniform distribution 0.25 each. <code>torch.softmax</code> and <code>F.cross_entropy</code> do this subtraction for you internally; the lesson is never to write <code>exp(z) / sum(exp(z))</code> yourself.</li></ol>
<h3>Autograd, first by hand</h3>
<p>Before trusting <code>loss.backward()</code>, build a tiny version. We create a scalar class <code>Value</code> that stores its number, its gradient, the values it came from, and a small function that pushes gradient back to those parents using the chain rule. This is a miniature of what PyTorch records in <code>grad_fn</code>.</p>
<p class="problem"><span class="pl">Problem 21.2.3</span> Let z = x*y + x<sup>2</sup> with x = 2 and y = -3. By hand: z = -6 + 4 = -2. dz/dx = y + 2x = -3 + 4 = 1 and dz/dy = x = 2. Verify with a hand-built autograd, then with a finite-difference check.</p>
<table class="steps"><tr><th>Rule 1</th><td>For c = a + b: dc/da = 1 and dc/db = 1, so each parent receives the child's gradient.</td></tr><tr><th>Rule 2</th><td>For c = a * b: dc/da = b and dc/db = a, so a parent receives (child gradient) times (the other parent's value).</td></tr><tr><th>Rule 3</th><td>If a variable is used twice (here x), its gradients from the two paths are <em>added</em>. This is why PyTorch accumulates into <code>.grad</code>.</td></tr></table>
%%PY
class Value:
    def __init__(self, data, parents=()):
        self.data = float(data)
        self.grad = 0.0
        self._parents = parents
        self._backward = lambda: None

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other))
        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other))
        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out

    def __pow__(self, k):
        out = Value(self.data ** k, (self,))
        def _backward():
            self.grad += k * self.data ** (k - 1) * out.grad
        out._backward = _backward
        return out

    def backward(self):
        order, seen = [], set()
        def visit(v):
            if id(v) not in seen:
                seen.add(id(v))
                for p in v._parents:
                    visit(p)
                order.append(v)
        visit(self)
        self.grad = 1.0
        for v in reversed(order):
            v._backward()

def f(xv, yv):
    x, y = Value(xv), Value(yv)
    z = x * y + x ** 2
    return x, y, z

x, y, z = f(2.0, -3.0)
z.backward()
print("z =", z.data, " dz/dx =", x.grad, " dz/dy =", y.grad)

h = 1e-6
num_dx = (f(2.0 + h, -3.0)[2].data - f(2.0 - h, -3.0)[2].data) / (2 * h)
num_dy = (f(2.0, -3.0 + h)[2].data - f(2.0, -3.0 - h)[2].data) / (2 * h)
print("numeric dx, dy:", round(num_dx, 4), round(num_dy, 4))

z.backward()                      # call again without zeroing
print("after second backward, x.grad =", x.grad)
%%END
<ol><li>Each operator (<code>__add__</code>, <code>__mul__</code>, <code>__pow__</code>) computes the forward number and stores a closure <code>_backward</code> that knows the local derivative. This is the recipe the cooking-show analogy described.</li><li>Inside each closure the update uses <code>+=</code>, not <code>=</code>. Because <code>x</code> feeds two operations (the product and the square), it receives two contributions that must be added: y + 2x = -3 + 4 = 1.</li><li><code>backward()</code> first orders the nodes so that every node comes after its parents (a topological order), seeds the output gradient with 1.0 (the slope of z with respect to itself), then calls each closure from the output back to the inputs.</li><li>The first printed line matches the hand calculation: z = -2, dz/dx = 1, dz/dy = 2.</li><li>The finite-difference check nudges the input up and down by <code>h</code> and measures the slope. It agrees to four decimals, which is the standard way to test any gradient code.</li><li>Calling <code>backward()</code> a second time without resetting adds to everything already stored, including the intermediate nodes, so <code>x.grad</code> becomes 3 instead of 1 (it is not even a clean doubling). This is the exact behaviour behind the famous bug "I forgot <code>optimizer.zero_grad()</code>".</li></ol>
<p>In PyTorch the same computation is three lines (not run here), and the two behaviours (accumulation and the graph being freed) are the ones that surprise newcomers:</p>
%%NORUN
import torch

x = torch.tensor(2.0, requires_grad=True)
y = torch.tensor(-3.0, requires_grad=True)
z = x * y + x ** 2
z.backward()
print(z.item(), x.grad.item(), y.grad.item())   # -2.0 1.0 2.0

# calling backward again on the SAME graph raises an error, because buffers were freed:
# RuntimeError: Trying to backward through the graph a second time ...
# Use z.backward(retain_graph=True) only if you truly need it.

# gradients ACCUMULATE across separate backward passes:
x.grad.zero_()                       # reset (optimizer.zero_grad() does this for all parameters)
(x ** 2).backward()
print(x.grad.item())                 # 4.0

with torch.no_grad():                # nothing is recorded inside
    w = x * 3
print(w.requires_grad)               # False
v = (x * 3).detach()                 # cut a tensor out of the graph
%%END
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Wrong:</strong> storing <code>losses.append(loss)</code> in a loop. <strong>Symptom:</strong> memory grows every step, because each stored tensor keeps its entire graph alive. <strong>Fix:</strong> <code>losses.append(loss.item())</code> (a plain Python float) or <code>loss.detach()</code>.</div></div>
<h3>Realistic: gradients for a whole layer, checked numerically</h3>
<p>Real networks use vectors and matrices, so the backward formulas are matrix formulas. For a linear model y&#770; = X w + b with mean squared error L = mean((y&#770; - y)<sup>2</sup>), the gradients are dL/dw = (2/N) X<sup>T</sup> (y&#770; - y) and dL/db = (2/N) sum(y&#770; - y). We implement them, then check against numerical gradients, which is how you validate any custom layer.</p>
%%PY
import numpy as np

rng = np.random.default_rng(0)
N, D = 50, 3
X = rng.normal(size=(N, D))
true_w = np.array([2.0, -1.0, 0.5])
y = X @ true_w + 0.3 + rng.normal(scale=0.1, size=N)

def loss_fn(w, b):
    err = X @ w + b - y
    return np.mean(err ** 2)

def analytic_grads(w, b):
    err = X @ w + b - y
    return 2 / N * X.T @ err, 2 / N * err.sum()

def numeric_grads(w, b, h=1e-6):
    gw = np.zeros_like(w)
    for i in range(len(w)):
        e = np.zeros_like(w); e[i] = h
        gw[i] = (loss_fn(w + e, b) - loss_fn(w - e, b)) / (2 * h)
    gb = (loss_fn(w, b + h) - loss_fn(w, b - h)) / (2 * h)
    return gw, gb

w0, b0 = np.zeros(D), 0.0
gw, gb = analytic_grads(w0, b0)
nw, nb = numeric_grads(w0, b0)
print("analytic dw:", np.round(gw, 4), "db:", round(gb, 4))
print("numeric  dw:", np.round(nw, 4), "db:", round(nb, 4))
print("match:", np.allclose(gw, nw, atol=1e-6) and abs(gb - nb) < 1e-6)
%%END
<ol><li>We simulate data from a known rule (weights 2, -1, 0.5 and offset 0.3) plus small noise, so we know what a good fit looks like.</li><li><code>analytic_grads</code> is the formula you would code in a custom autograd function. Note <code>X.T @ err</code>: <code>(D, N) @ (N,)</code> gives shape <code>(D,)</code>, one gradient per weight.</li><li><code>numeric_grads</code> nudges one weight at a time, which is slow (two forward passes per weight) but needs no calculus. This is the idea behind <code>torch.autograd.gradcheck</code>.</li><li>At <code>w = 0</code> each gradient has the opposite sign to the true weight (negative for 2 and 0.5, positive for -1), so a step <em>against</em> the gradient moves each weight toward its true value. The two printed rows agree and <code>match</code> prints <code>True</code>.</li></ol>
<div class="callout green"><div class="lab">KEY IDEA</div><div class="txt">Autograd is the chain rule applied by a program. It needs three things from you: mark trainable tensors with <code>requires_grad=True</code>, produce one scalar loss, and call <code>backward()</code>. It gives you three things back: <code>.grad</code> on each leaf, accumulation across calls, and a graph that is freed after use.</div></div>
<figure><img src="images/lib21_autograd_graph.png" alt="Computation graph for z = x*y + x squared with forward values in blue and backward gradients in orange" loading="lazy"/><figcaption>Figure 21.2. The graph for z = x*y + x<sup>2</sup> at x = 2, y = -3. Blue numbers go forward, orange numbers are the gradients flowing back; x receives two contributions that are added.</figcaption></figure>
<p><strong>How to read it:</strong> start at the left with the inputs, follow the blue values to z = -2, then read the orange numbers from right to left. At x the two incoming gradients are y = -3 (through the product) and 2x = 4 (through the square); they add to 1.</p>
