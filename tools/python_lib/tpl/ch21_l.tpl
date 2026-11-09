
<h2 id="s21-recap">Chapter recap</h2>
<ul>
<li>Every deep learning program is one loop: batch, forward, loss, backward, optimiser step. If you can write it from memory (21.4), you can debug any framework built on it, including <code>Trainer</code>.</li>
<li>A tensor is an array that remembers its history. <code>requires_grad</code> marks what to train, <code>backward()</code> fills <code>.grad</code>, gradients accumulate until cleared, and the graph is freed after use.</li>
<li><code>nn.Module</code> registers parameters through attributes. Use <code>ModuleList</code> or <code>Sequential</code>, never a plain list. <code>train()</code> and <code>eval()</code> switch dropout and batch-norm behaviour.</li>
<li>Classification losses take logits. Compute log-softmax stably; the gradient with respect to logits is softmax minus one-hot.</li>
<li>Shapes, dtypes and devices explain most errors. Write shapes in comments, print them for the first batch and assert the important ones.</li>
<li>Training memory is roughly parameters x (weights + gradients + optimiser state) plus activations: 16 bytes per parameter for fp32 with Adam. Mixed precision, accumulation, checkpointing and LoRA are the standard levers.</li>
<li>Hugging Face is a set of conventions: tokeniser, config, weights, <code>datasets</code> tables, <code>Trainer</code>. Always use the tokeniser that matches the model and pad dynamically.</li>
<li>LoRA trains W + (alpha / r) B A with W frozen: tiny trainable share, exact no-op at the start, and mergeable at serving time.</li>
<li>Vector search is nearest-neighbour lookup on embeddings. Normalise for cosine, use float32, measure recall of approximate indexes against exact search, and filter metadata before ranking.</li>
<li>LLM calls fail, stream and return unchecked text: set client retries and timeouts, back off with jitter, never retry 4xx errors, validate every reply and cap tool loops.</li>
<li>Evaluation is a fixed golden set, a metric that fits the task, a baseline, a paired comparison with uncertainty, and a held-out test set you touch once.</li>
</ul>
<div class="tablewrap"><table class="data"><thead><tr><th>Formula / pattern</th><th>Meaning</th></tr></thead><tbody>
<tr><td>loss.backward(); opt.step(); opt.zero_grad()</td><td>Backpropagate, update, clear: one training step</td></tr>
<tr><td>dL/dz = softmax(z) - onehot(y)</td><td>Gradient of cross-entropy with respect to logits</td></tr>
<tr><td>log softmax(z)<sub>y</sub> = z<sub>y</sub> - max(z) - log sum exp(z - max(z))</td><td>Stable cross-entropy ingredient</td></tr>
<tr><td>Adam: w -= lr m&#770; / (&#8730;v&#770; + &#949;)</td><td>Per-parameter adaptive step with bias correction</td></tr>
<tr><td>bytes = P x (w + g + opt), fp32 + Adam = 16 P</td><td>Training memory before activations</td></tr>
<tr><td>W<sub>eff</sub> = W + (alpha / r) B A</td><td>LoRA update; B starts at zero</td></tr>
<tr><td>mean of k micro-batch grads = big-batch grad</td><td>Gradient accumulation (divide loss by k)</td></tr>
<tr><td>||a - b||<sup>2</sup> = 2 - 2 cos(a, b) for unit vectors</td><td>L2 ranking equals cosine ranking</td></tr>
<tr><td>wait = uniform(0, min(cap, base x 2<sup>attempt</sup>))</td><td>Full-jitter exponential backoff</td></tr>
<tr><td>recall@k, MRR, nDCG@k</td><td>Retrieval quality metrics</td></tr>
<tr><td>paired bootstrap on per-item correctness</td><td>Uncertainty of a difference between two systems</td></tr>
<tr><td>overfit one batch</td><td>The first test for any training pipeline</td></tr>
</tbody></table></div>

<h2 id="s21-practice">Practice set</h2>
<p>Graded from easy to expert. Code shown in a problem is not run by the book; answers were checked by running equivalent code.</p>
<p class="problem"><span class="pl">Problem 21.P.1</span> (easy) What are logits, and why do <code>CrossEntropyLoss</code> and <code>BCEWithLogitsLoss</code> want them instead of probabilities?</p>
<p><strong>Answer:</strong> Logits are the raw scores a model outputs before softmax or sigmoid. The loss functions fuse the squashing with the logarithm using the log-sum-exp trick, which avoids overflow and taking log of values that underflow to 0. Passing probabilities means softmax is applied twice and stability is lost.</p>
<p class="problem"><span class="pl">Problem 21.P.2</span> (easy) How many trainable parameters does <code>nn.Linear(10, 4)</code> have?</p>
<p><strong>Answer:</strong> The weight matrix has 4 x 10 = 40 numbers and the bias has 4: total 44.</p>
<p class="problem"><span class="pl">Problem 21.P.3</span> (easy) A batch holds 32 colour images of 224 x 224 pixels. Give its PyTorch shape, and the shape after <code>x.flatten(1)</code>.</p>
<p><strong>Answer:</strong> (32, 3, 224, 224), channels first. Flattening from dimension 1 keeps the batch: (32, 3 x 224 x 224) = (32, 150528).</p>
<p class="problem"><span class="pl">Problem 21.P.4</span> (easy, what does this print?)</p>
<pre class="code lang-torch"><code>import numpy as np
a = np.arange(6)
b = a[:3]
b[0] = 9
c = a[:3].copy()
c[1] = 7
print(a[0], a[1])</code></pre>
<p><strong>Answer:</strong> <code>9 1</code>. The slice <code>b</code> is a view, so writing 9 changes <code>a[0]</code>. The copy <code>c</code> is independent, so <code>a[1]</code> stays 1. (Torch behaves the same way for slices and <code>.clone()</code>.)</p>
<p class="problem"><span class="pl">Problem 21.P.5</span> (easy) What is the broadcast result shape of <code>(8, 1, 5)</code> plus <code>(3, 1)</code>?</p>
<p><strong>Answer:</strong> Align from the right: (8, 1, 5) with (1, 3, 1). Each pair is equal or has a 1, giving (8, 3, 5).</p>
<p class="problem"><span class="pl">Problem 21.P.6</span> (easy) Which of these HTTP errors should a retry loop retry: 400, 401, 429, 503, 404?</p>
<p><strong>Answer:</strong> Only 429 (rate limit, honour <code>retry-after</code>) and 503 (temporary overload), together with timeouts and connection errors. 400, 401 and 404 describe a problem with the request, key or address; repeating the same request fails the same way.</p>
<p class="problem"><span class="pl">Problem 21.P.7</span> (easy) How much memory do the weights alone need for a 1-billion-parameter model in float32, bfloat16 and 4-bit?</p>
<p><strong>Answer:</strong> 1e9 x 4 bytes = 4 GB, 1e9 x 2 = 2 GB, and 1e9 x 0.5 = 0.5 GB (decimal gigabytes). Full fine-tuning in fp32 with Adam needs 16 GB for weights, gradients and optimiser state before activations.</p>
<p class="problem"><span class="pl">Problem 21.P.8</span> (medium, find the bug) The loss wanders and sometimes explodes. What is wrong?</p>
<pre class="code lang-torch"><code>for x, y in loader:
    loss = loss_fn(model(x), y)
    loss.backward()
    opt.step()</code></pre>
<p><strong>Answer:</strong> <code>opt.zero_grad()</code> is missing, so gradients from all previous batches keep adding up and every step uses a growing sum. Add <code>opt.zero_grad()</code> before <code>loss.backward()</code> (or right after <code>opt.step()</code>).</p>
<p class="problem"><span class="pl">Problem 21.P.9</span> (medium, find the bug) After training, <code>model.parameters()</code> seems to contain only the output layer. Why?</p>
<pre class="code lang-torch"><code>class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden = [nn.Linear(8, 8) for _ in range(3)]
        self.out = nn.Linear(8, 2)</code></pre>
<p><strong>Answer:</strong> A plain Python list is not registered by <code>nn.Module</code>, so the three hidden layers are invisible to <code>parameters()</code>, <code>state_dict()</code> and <code>.to(device)</code>; the optimiser never trains them. Use <code>nn.ModuleList([...])</code>.</p>
<p class="problem"><span class="pl">Problem 21.P.10</span> (medium, find the bug) Training accuracy plateaus low although the code runs. Find the issue.</p>
<pre class="code lang-torch"><code>logits = model(x)
probs = torch.softmax(logits, dim=-1)
loss = nn.CrossEntropyLoss()(probs, y)</code></pre>
<p><strong>Answer:</strong> The loss applies log-softmax internally, so the model's softmax is applied twice. The squashed probabilities flatten gradients and the loss cannot go to zero. Pass <code>logits</code> directly.</p>
<p class="problem"><span class="pl">Problem 21.P.11</span> (medium, find the bug) Predictions on 10,000 texts come back misaligned with the input rows.</p>
<pre class="code lang-torch"><code>order = sorted(range(len(texts)), key=lambda i: len(texts[i]))
preds = []
for s in range(0, len(order), 64):
    batch = [texts[i] for i in order[s:s + 64]]
    preds.extend(predict_batch(batch))
return preds</code></pre>
<p><strong>Answer:</strong> The predictions are in length-sorted order but returned as if they were in input order. Write each result back to its original index: <code>out[order[s + j]] = pred_j</code>, or invert the permutation at the end as in recipe 5.</p>
<p class="problem"><span class="pl">Problem 21.P.12</span> (medium, find the bug) A FAISS search sometimes returns the wrong document text for tiny corpora.</p>
<pre class="code lang-torch"><code>D, I = index.search(q, 5)
answers = [docs[i] for i in I[0]]</code></pre>
<p><strong>Answer:</strong> When fewer than 5 vectors are stored, FAISS fills the missing slots with <code>-1</code>, and <code>docs[-1]</code> in Python is the last document, which silently appears as a fake hit. Filter first: <code>[docs[i] for i in I[0] if i != -1]</code>.</p>
<p class="problem"><span class="pl">Problem 21.P.13</span> (medium) Compute the cross-entropy loss and the gradient with respect to the logits for logits z = [1, 0, 0] and true class 0.</p>
<p><strong>Answer:</strong> exp(1) = 2.718, exp(0) = 1, so the sum is 4.718 and the probabilities are [0.576, 0.212, 0.212]. Loss = -ln 0.576 = 0.551. Gradient = p - onehot = [-0.424, 0.212, 0.212]. The three gradient entries sum to 0, as they always do for softmax cross-entropy.</p>
<p class="problem"><span class="pl">Problem 21.P.14</span> (medium) Adam, first step: gradient g = 0.5, lr = 0.1, beta1 = 0.9, beta2 = 0.999, epsilon negligible. By how much does the parameter move?</p>
<p><strong>Answer:</strong> m = 0.1 x 0.5 = 0.05 and v = 0.001 x 0.25 = 0.00025. Bias correction at t = 1 divides by 0.1 and 0.001, giving m&#770; = 0.5 and v&#770; = 0.25, so &#8730;v&#770; = 0.5. The step is 0.1 x 0.5 / 0.5 = 0.1. Early Adam steps have size close to lr whatever the scale of the gradient.</p>
<p class="problem"><span class="pl">Problem 21.P.15</span> (medium) You want an effective batch of 64 but only 8 examples fit in memory. What do you change, and what must you remember about the loss?</p>
<p><strong>Answer:</strong> Accumulate over 8 micro-batches: call <code>backward()</code> on each and <code>opt.step(); opt.zero_grad()</code> every 8th one. Divide each micro-batch loss by 8 (for mean losses) so the summed gradient equals the mean over 64. The scheduler should count optimiser steps, not micro-batches. Batch-norm statistics still see only 8 examples.</p>
<p class="problem"><span class="pl">Problem 21.P.16</span> (medium) A transformer with d = 4096 adapts the query and value projections (each 4096 x 4096) in all 32 layers with LoRA rank r = 8. How many trainable parameters is that?</p>
<p><strong>Answer:</strong> One adapted matrix has A (8 x 4096) and B (4096 x 8): 2 x 4096 x 8 = 65,536. Two matrices per layer give 131,072; times 32 layers gives 4,194,304 trainable parameters, about 4.2 million, versus 16.8 million per full matrix.</p>
<p class="problem"><span class="pl">Problem 21.P.17</span> (medium) A system returns [1, 5, 2, 9] and the relevant documents are {1, 2}. Compute recall@2, MRR and nDCG@4.</p>
<p><strong>Answer:</strong> Top 2 are [1, 5]: one of two relevant found, recall@2 = 0.5. The first relevant item is at rank 1, so MRR = 1. DCG = 1/log<sub>2</sub>2 + 1/log<sub>2</sub>4 = 1 + 0.5 = 1.5 (relevant items at ranks 1 and 3). IDCG = 1 + 1/log<sub>2</sub>3 = 1.6309. nDCG = 1.5 / 1.6309 = 0.920.</p>
<p class="problem"><span class="pl">Problem 21.P.18</span> (medium) With base 0.5 s, cap 8 s and full jitter, give the maximum wait for attempts 0 to 5 and their sum.</p>
<p><strong>Answer:</strong> min(8, 0.5 x 2<sup>n</sup>): 0.5, 1, 2, 4, 8, 8 (attempt 5 would be 16, capped). The sum is 23.5 s, the worst-case total waiting time; the expected total with jitter is about half of that.</p>
<p class="problem"><span class="pl">Problem 21.P.19</span> (medium) A job makes 2,000 LLM calls a day, each with 1,500 input and 300 output tokens, at 2 dollars per million input tokens and 10 dollars per million output tokens (invented prices). Cost per day and per 30 days?</p>
<p><strong>Answer:</strong> Per call: 1,500 x 2 / 1e6 = 0.003 and 300 x 10 / 1e6 = 0.003, total 0.006 dollars. Per day: 2,000 x 0.006 = 12 dollars. Per 30 days: 360 dollars. Output tokens cost five times as much per token here, so cutting answer length is as valuable as cutting the prompt.</p>
<p class="problem"><span class="pl">Problem 21.P.20</span> (medium, what does this print?)</p>
<pre class="code lang-torch"><code>attempts = 0
def flaky():
    global attempts
    attempts += 1
    if attempts &lt; 3:
        raise TimeoutError
    return "ok"

for i in range(5):
    try:
        print(flaky())
        break
    except TimeoutError:
        print("retry", i)</code></pre>
<p><strong>Answer:</strong> <code>retry 0</code>, <code>retry 1</code>, then <code>ok</code>. The first two calls raise, the third succeeds and <code>break</code> ends the loop, so the remaining iterations never run.</p>
<p class="problem"><span class="pl">Problem 21.P.21</span> (expert) Derive the gradient of the cross-entropy L = -z<sub>y</sub> + log sum<sub>j</sub> exp(z<sub>j</sub>) with respect to z<sub>k</sub>.</p>
<p><strong>Answer:</strong> The first term gives -1 when k = y and 0 otherwise. The derivative of log sum exp(z<sub>j</sub>) with respect to z<sub>k</sub> is exp(z<sub>k</sub>) / sum<sub>j</sub> exp(z<sub>j</sub>) = softmax(z)<sub>k</sub>. Adding: dL/dz<sub>k</sub> = softmax(z)<sub>k</sub> - 1[k = y], that is p minus the one-hot vector. This is why backward from the logits needs no extra work, and why the gradient entries sum to 0.</p>
<p class="problem"><span class="pl">Problem 21.P.22</span> (expert) Show that merging a LoRA adapter does not change the layer's outputs, and explain why merging helps at serving time.</p>
<p><strong>Answer:</strong> With scale s = alpha / r, the adapted layer computes y = x W<sup>T</sup> + s (x A<sup>T</sup>) B<sup>T</sup> = x (W + s B A)<sup>T</sup>, because (B A)<sup>T</sup> = A<sup>T</sup> B<sup>T</sup> and matrix multiplication is associative. So replacing W by W + s B A gives identical outputs. Merging removes the two extra small matrix products per layer (less latency, simpler deployment). The cost is that the adapter can no longer be swapped without keeping the original W, and merging into a quantised base needs care for rounding.</p>
<p class="problem"><span class="pl">Problem 21.P.23</span> (expert) Self-attention scores are materialised in float16 with shape (B, H, T, T) for B = 8, H = 16, T = 4096. How large is that tensor for one layer, and what happens when T doubles?</p>
<p><strong>Answer:</strong> Elements: 8 x 16 x 4096 x 4096 = 2,147,483,648. At 2 bytes each that is 4,294,967,296 bytes, about 4.3 GB for one layer's score matrix (more for the softmax output and for backward). Doubling T quadruples it to about 17 GB. This quadratic growth is why fused attention kernels that never write the full matrix, and shorter or chunked contexts, matter.</p>
<p class="problem"><span class="pl">Problem 21.P.24</span> (expert, design) You must show that a new prompt for a ticket classifier is better than the current one before shipping. Describe the evaluation.</p>
<p><strong>Answer:</strong> (1) Build a golden set of real tickets labelled by people, split into a development set for prompt iteration and a test set touched once; deduplicate before splitting. (2) Choose metrics that match the business: per-class precision and recall (and a cost-weighted error if mistakes differ in cost), valid-output rate, latency and cost per call. (3) Run both prompts at the same settings, with temperature 0 or several samples. (4) Compare per item (paired): count items where only the new prompt is right versus only the old one, and bootstrap a confidence interval of the accuracy difference. (5) Read the errors, not only the number. (6) Ship behind a monitored rollout and keep sampling real traffic into the golden set. If the interval includes zero, say that the evidence is inconclusive and collect more labels.</p>
<p class="problem"><span class="pl">Problem 21.P.25</span> (expert, interview) Explain the difference between <code>view</code> and <code>reshape</code>, and between <code>detach()</code> and <code>torch.no_grad()</code>.</p>
<p><strong>Answer:</strong> <code>view</code> never copies and requires compatible strides (contiguous memory); it errors otherwise. <code>reshape</code> returns a view when possible and silently copies when not. <code>detach()</code> returns a tensor that shares data but is cut from the graph, for a single tensor. <code>torch.no_grad()</code> is a context in which no operation is recorded at all, so no graph is built and memory is saved; it does not change <code>requires_grad</code> of existing parameters. Use <code>no_grad</code> or <code>inference_mode</code> for evaluation and <code>detach</code> to stop gradients through one value (for example a target or a stored state).</p>
<p class="problem"><span class="pl">Problem 21.P.26</span> (expert, what does this print?)</p>
<pre class="code lang-torch"><code>import numpy as np
x = np.arange(12.0).reshape(3, 4)
print(x.sum(0).shape, x.sum(1, keepdims=True).shape)
print((x - x.mean(1, keepdims=True)).mean(1))</code></pre>
<p><strong>Answer:</strong> The first line prints <code>(4,) (3, 1)</code>: summing over axis 0 removes it, while <code>keepdims=True</code> keeps a length-1 axis. The second line subtracts each row's mean from the row, so every row now has mean zero: it prints <code>[0. 0. 0.]</code> (possibly tiny floating-point values such as <code>-0.</code>). Without <code>keepdims=True</code> the mean has shape (3,), which cannot broadcast against (3, 4) and raises an error (or worse, mis-aligns when the sizes happen to match).</p>

<h2 id="s21-prompts">Prompt pack</h2>
<div class="prompt"><div class="ph"><span>AI prompt: copy and paste into any AI</span><button type="button" class="copy">Copy</button></div><pre>You are my patient, practical professor of deep learning engineering. I am a working professional moving into data roles and I know basic Python, NumPy and pandas. Teach me PyTorch and the LLM toolchain one idea at a time: tensors and autograd, nn.Module, optimisers, DataLoader, the training loop, device and memory, Hugging Face, embeddings with vector search, and LLM API calls with retries and structured output. For each idea: (1) explain it in plain English with an analogy, (2) show a minimal example and tell me the output before I run it, (3) ask me one prediction question and wait for my answer, (4) correct me kindly and ask a harder follow-up. After five ideas, give me a 10-question quiz mixing what-does-this-print, find-the-bug and shape questions, and grade it. Do not move on until I say I understand.</pre></div>
<div class="prompt"><div class="ph"><span>AI prompt: copy and paste into any AI</span><button type="button" class="copy">Copy</button></div><pre>Act as a senior ML engineer doing a code review. I will paste a PyTorch or LLM-API script. Review it in this order: (1) correctness: shapes, dtypes, devices, missing zero_grad, eval and no_grad, loss inputs (logits versus probabilities), data leakage; (2) memory and speed: batch size, padding, num_workers, mixed precision, storing tensors with graphs; (3) LLM calls: retries only for 429, 5xx and timeouts, timeouts set, streaming, reply validation, secrets in code, cost per call; (4) evaluation: is there a held-out set, a baseline and a confidence interval? For every problem give the exact line, why it matters, the symptom I would see, and a fixed version. End with the three most important changes. Ask me for the missing information (library versions, hardware, data size) before guessing.</pre></div>
<div class="prompt"><div class="ph"><span>AI prompt: copy and paste into any AI</span><button type="button" class="copy">Copy</button></div><pre>Run a mock interview for a machine learning engineer role focused on deep learning and GenAI libraries. Ask me one question at a time and wait for my answer. Mix: explain autograd and why gradients accumulate; estimate the memory to fine-tune a 7B-parameter model and name ways to reduce it; explain LoRA with parameter counts; debug a shape error from an error message I will paste; design a retrieval-augmented generation system with chunking, embeddings, an index, metrics and failure modes; make an LLM call reliable and cheap at one million requests a day; show that a new prompt beats the old one. After each answer, score me from 1 to 5, point out what I missed, and give a model answer in under 120 words. After eight questions, summarise my strengths and the three topics I should revise, and propose a one-week study plan.</pre></div>
