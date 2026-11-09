<p>Imagine you join a software company's support team as the first data person. There are 40,000 old tickets in a spreadsheet and 300 new ones arrive every day. Your manager wants three things: (1) label each new ticket as <em>billing</em>, <em>bug</em> or <em>how-to</em> automatically, (2) show the agent the five most similar old tickets, and (3) draft a first reply with a large language model (LLM) and refuse to send it if it is not valid JSON. Each of those three wishes is a different library family. The labeller is a neural network trained with <strong>PyTorch</strong>, or a pretrained model fine-tuned with <strong>Hugging Face</strong>. The "similar tickets" feature is <strong>embeddings plus vector search</strong> (sentence-transformers, FAISS or Chroma). The reply drafter is an <strong>LLM SDK call</strong> wrapped in retries, streaming and output checks. Glue and measurement come from orchestration code and an <strong>evaluation harness</strong>.</p>
<p>This chapter is a handbook, not a theory course. For each library you get a reference table of the functions you will actually use, worked examples that climb from trivial to realistic, a list of traps, and a playbook for solving problems you have not seen. One practical difficulty shapes the whole chapter: <code>torch</code>, <code>transformers</code>, <code>faiss</code> and the vendor SDKs are <strong>not installed</strong> on the machine that produced this book, and some need a GPU or a network key anyway. So every library appears twice. First you see idiomatic code labelled <strong>not run here</strong> (it is the code you would paste into a real project, written from the documented APIs). Then you see a <strong>runnable equivalent</strong> built from NumPy, scikit-learn and the standard library that demonstrates the same mechanics, with real printed output. When a mechanism is understood by hand (autograd, an optimiser step, a retry loop, a nearest-neighbour search), the library call stops being magic.</p>
<p>By the end you will be able to: read and write a PyTorch training loop and know what every line does; debug shape, device and memory errors in a systematic way; tokenise text and explain what a Hugging Face <code>Trainer</code> does; build and evaluate a retrieval system; call an LLM API with retries, streaming and structured output; and judge whether your GenAI feature actually works with a small evaluation harness. For the maths behind gradients see the Maths document, Chapter 13 (backpropagation) and Chapter 14 (optimisation). For concepts such as attention and fine-tuning in depth, see the Deep Learning and GenAI documents. Here we focus on the <em>libraries and the code</em>.</p>
<p><em>Words you need.</em> A <strong>tensor</strong> is an n-dimensional array that can also remember how it was computed. A <strong>gradient</strong> is the slope of the loss with respect to a number, telling you which way to nudge it. A <strong>token</strong> is a small piece of text (a word or part of a word) mapped to an integer id. An <strong>embedding</strong> is a list of numbers that places a piece of text (or an image) at a point in space so that similar things sit close together. An <strong>LLM</strong> is a very large model that continues text. <strong>Inference</strong> means using a trained model, <strong>training</strong> means changing it.</p>

<h2 id="s21-1">21.1 What These Libraries Are, When to Use Them, and the Mental Model</h2>
<h3>The libraries in one table</h3>
<div class="tablewrap"><table class="data"><thead><tr><th>Library</th><th>What it is</th><th>Use it when</th><th>Do NOT use it when</th></tr></thead><tbody>
<tr><td>PyTorch (<code>torch</code>)</td><td>Tensors with automatic differentiation, neural network building blocks, optimisers, GPU support</td><td>You train or fine-tune neural networks, or need custom losses and architectures</td><td>Tabular data with a few thousand rows: gradient boosting or logistic regression is usually faster, simpler and as accurate</td></tr>
<tr><td><code>transformers</code></td><td>Pretrained models, tokenisers and a <code>Trainer</code> for text, vision and audio</td><td>You want a pretrained model for classification, extraction, generation or embeddings</td><td>A regex or a TF-IDF plus logistic regression already solves the task at the needed accuracy</td></tr>
<tr><td><code>datasets</code></td><td>Memory-mapped, cached tables with fast <code>map</code>, <code>filter</code> and streaming</td><td>Data is too big for pandas RAM or you feed a Hugging Face model</td><td>The data fits in a pandas DataFrame and you only do analysis</td></tr>
<tr><td><code>tokenizers</code></td><td>Fast tokeniser engine (Rust) behind <code>transformers</code></td><td>You train your own vocabulary or need exact offsets</td><td>You use a standard pretrained model: load its own tokeniser instead</td></tr>
<tr><td><code>peft</code></td><td>Parameter-efficient fine-tuning (LoRA and relatives)</td><td>The base model is too big to fine-tune fully on your hardware</td><td>The model is small enough to fine-tune fully, or prompting already works</td></tr>
<tr><td><code>sentence-transformers</code></td><td>Models that turn sentences into embedding vectors</td><td>Semantic search, clustering, deduplication, retrieval for RAG</td><td>Exact keyword matches matter most (use BM25 or a database <code>LIKE</code>)</td></tr>
<tr><td>FAISS</td><td>Fast nearest-neighbour search over millions of vectors</td><td>Vectors live in memory and you need speed</td><td>Under about 100,000 vectors: a NumPy matrix product is enough</td></tr>
<tr><td>Chroma</td><td>A small vector database with metadata filters and persistence</td><td>Prototypes and small apps that need filtering plus storage</td><td>Large multi-user production search (use a managed vector store or pgvector)</td></tr>
<tr><td>OpenAI / Anthropic SDKs</td><td>Typed clients for hosted LLM APIs</td><td>You want a strong model without hosting it</td><td>Data may not leave your network, or the cost per call is too high at your volume</td></tr>
<tr><td>LangChain-style orchestration</td><td>Composable prompt, model, parser chains and agent loops</td><td>Many steps, several providers, tool calls</td><td>One prompt and one call: plain SDK code is clearer</td></tr>
</tbody></table></div>
<div class="callout green"><div class="lab">KEY IDEA</div><div class="txt">The right first question is not "which deep learning library?" but "do I need a neural network at all?". A model you do not train, a rule, or a linear model are all valid answers. Reach for these libraries when the input is text, images, audio or sequences, or when you need to adapt a pretrained model.</div></div>

<h3>Install, version check and import conventions</h3>
<p>Install in a virtual environment (see Chapter 9). PyTorch has a choice of builds (CPU only, or a specific CUDA version), so copy the exact command from the selector on pytorch.org rather than guessing. Not run here:</p>
%%NORUN
# create and activate an environment first (Chapter 9)
python3 -m venv .venv && source .venv/bin/activate
pip install torch                       # use the command from pytorch.org for your CUDA/CPU build
pip install transformers datasets tokenizers peft accelerate
pip install sentence-transformers faiss-cpu chromadb
pip install openai anthropic langchain-core
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
%%END
<p>The conventional imports are below. Learn them: every tutorial and every colleague uses exactly these names.</p>
%%NORUN
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from datasets import load_dataset
from peft import LoraConfig, get_peft_model
from sentence_transformers import SentenceTransformer
import faiss
import chromadb
from openai import OpenAI
import anthropic
%%END
<p>A version check that works whether or not a library exists is a handy first line in any bug report. This one runs here and reports honestly what the machine has:</p>
%%PY
import importlib.util
import importlib.metadata as md

def report(pairs):
    for import_name, pip_name in pairs:
        if importlib.util.find_spec(import_name) is None:
            print(f"{import_name:14s} not installed")
        else:
            try:
                print(f"{import_name:14s} {md.version(pip_name)}")
            except md.PackageNotFoundError:
                print(f"{import_name:14s} installed (no metadata)")

report([("torch", "torch"), ("transformers", "transformers"), ("faiss", "faiss-cpu"),
        ("openai", "openai"), ("anthropic", "anthropic"),
        ("numpy", "numpy"), ("sklearn", "scikit-learn")])
%%END
<ol><li><code>find_spec</code> asks Python whether an import would succeed without actually importing the (possibly slow) package. It returns <code>None</code> when the package is missing.</li><li><code>md.version</code> reads the version from the installed package metadata. This is the same number <code>pip list</code> shows.</li><li>The <em>import name</em> and the <em>pip name</em> can differ: you <code>pip install scikit-learn</code> but <code>import sklearn</code>, and <code>faiss-cpu</code> imports as <code>faiss</code>. So each pair holds both names, and we catch <code>PackageNotFoundError</code> in case the metadata is stored under another name.</li><li>The output shows the first five are absent on this machine, while NumPy and scikit-learn are present. That is the reason every library below comes with a runnable stand-in. Your versions will differ; always print them in a bug report.</li></ol>

<h3>The mental model</h3>
<p>Every deep learning library is a variation on one loop. You hold <strong>parameters</strong> (numbers), you run <strong>data</strong> forward through a function to get a <strong>prediction</strong>, you compare it with the truth to get a single number called the <strong>loss</strong>, you compute the <strong>gradient</strong> of the loss with respect to each parameter (the backward pass), and an <strong>optimiser</strong> nudges the parameters. Repeat. The GenAI libraries add two more pictures: text becomes <strong>token ids</strong> then <strong>embeddings</strong>, and calling a hosted model is a network request that can fail, stream and return text that you must <strong>validate</strong>.</p>
<figure><img src="images/lib21_mental_model.png" alt="Pipeline diagram: data and DataLoader, model with parameters, loss, backward pass producing gradients, optimiser step, with a second row for tokenise, embed, search and LLM call" loading="lazy"/><figcaption>Figure 21.1. The training loop (top row) and the GenAI request path (bottom row) are the two shapes every program in this chapter fits into.</figcaption></figure>
<p><strong>How to read it:</strong> follow the top row left to right for one training step; the arrow from the optimiser back to the model is the only place the model changes. In the bottom row nothing is trained: text is turned into numbers, the closest stored items are retrieved, and a hosted model writes the answer. Whenever you get lost in a library, ask "which box am I in?".</p>
<div class="callout cream"><div class="lab">REAL JOB</div><div class="txt">Most production time goes to the boxes that are not glamorous: getting batches to the model with the right shape and dtype, keeping memory under the limit, retrying failed API calls and measuring whether answers are good. This chapter spends most of its pages there on purpose.</div></div>
