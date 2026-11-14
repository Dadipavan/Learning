
<h2 id="s21-10">21.10 Orchestration Awareness and Evaluation Harnesses</h2>
<div class="callout blue"><div class="lab">INTUITION</div><div class="txt">An LLM application is rarely one call. It is a pipeline: build a prompt from a template, maybe retrieve documents, call a model, parse the reply, maybe call a tool, check the result. Orchestration libraries such as LangChain give these steps a common interface (every step has <code>invoke</code>) and a pipe operator so they snap together like Unix commands. They save glue code when you have many steps or many providers; they add a layer you must learn and debug when you have one. Evaluation is the other half: without a test set and a metric, you cannot tell whether a change made things better.</div></div>
<h3>Reference: LangChain-style building blocks</h3>
<p>This library changes quickly: package names (<code>langchain-core</code>, <code>langchain-community</code>, provider packages, <code>langgraph</code> for agents) and import paths have moved between releases. Treat the table as a map of <em>ideas</em> and check the current documentation for exact imports.</p>
<div class="tablewrap"><table class="data"><thead><tr><th>Idea / name</th><th>What it does in plain English</th><th>Minimal example (not run here)</th></tr></thead><tbody>
<tr><td><code>ChatPromptTemplate</code></td><td>A prompt with named holes</td><td><code>ChatPromptTemplate.from_template("Label: {text}")</code></td></tr>
<tr><td>Runnable</td><td>Anything with <code>invoke</code>, <code>batch</code>, <code>stream</code></td><td><code>chain.invoke({"text": "..."})</code></td></tr>
<tr><td>pipe operator <code>|</code></td><td>Output of the left step feeds the right step</td><td><code>prompt | model | parser</code></td></tr>
<tr><td>chat model wrapper</td><td>One interface over many providers</td><td><code>init_chat_model("provider:model-id")</code></td></tr>
<tr><td><code>StrOutputParser</code></td><td>Reply object to plain string</td><td><code>... | StrOutputParser()</code></td></tr>
<tr><td><code>with_structured_output</code></td><td>Model returns a validated object</td><td><code>model.with_structured_output(Schema)</code></td></tr>
<tr><td><code>RunnableLambda</code></td><td>Wrap any Python function as a step</td><td><code>RunnableLambda(clean_text)</code></td></tr>
<tr><td><code>RunnablePassthrough</code></td><td>Carry the input along unchanged</td><td><code>{"context": retriever, "question": RunnablePassthrough()}</code></td></tr>
<tr><td><code>RunnableParallel</code> (dict syntax)</td><td>Run several steps on the same input</td><td>a dict of runnables</td></tr>
<tr><td>text splitter</td><td>Cut documents into overlapping chunks</td><td><code>RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)</code></td></tr>
<tr><td>vector store / retriever</td><td>Search wrapper over FAISS, Chroma and others</td><td><code>store.as_retriever(search_kwargs={"k": 4})</code></td></tr>
<tr><td><code>@tool</code></td><td>Turn a function into a tool the model can call</td><td><code>@tool def lookup(id: int): ...</code></td></tr>
<tr><td>agent graph (LangGraph)</td><td>Loops and branches with explicit state</td><td>nodes, edges, conditional edges</td></tr>
<tr><td>tracing</td><td>Record every step's input and output</td><td>an environment variable plus a tracing service</td></tr>
</tbody></table></div>
<p>The classic RAG chain looks like this (not run here; import paths follow recent <code>langchain-core</code> but check your version):</p>
%%NORUN
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.chat_models import init_chat_model

model = init_chat_model("provider:your-model-id", temperature=0)
retriever = store.as_retriever(search_kwargs={"k": 3})           # store: Chroma or FAISS wrapper

prompt = ChatPromptTemplate.from_template(
    "Answer using only the context. If the answer is not there, say 'unknown'.\n"
    "Context:\n{context}\n\nQuestion: {question}")

def join_docs(docs):
    return "\n---\n".join(d.page_content for d in docs)

chain = ({"context": retriever | join_docs, "question": RunnablePassthrough()}
         | prompt | model | StrOutputParser())

print(chain.invoke("How do I reset my password?"))
for piece in chain.stream("How do I reset my password?"):       # streaming comes for free
    print(piece, end="")
answers = chain.batch(["question one", "question two"])         # concurrency for free
%%END
<p>Understanding the idea beats memorising the API. Below is a 30-line pipe framework with the same shape, followed by a RAG chain built from our earlier retriever. The "model" is a scripted function so the output is real and repeatable.</p>
<p class="problem"><span class="pl">Problem 21.10.1</span> Build <code>Runnable</code> with <code>invoke</code>, <code>batch</code> and the <code>|</code> operator, then compose retrieve, prompt, model and parse into a chain and run it on two questions.</p>
%%PY
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline

class Runnable:
    def __init__(self, fn, name="step"):
        self.fn, self.name = fn, name
    def invoke(self, x):
        return self.fn(x)
    def batch(self, xs):
        return [self.invoke(x) for x in xs]
    def __or__(self, other):                       # a | b means: run a, then feed its output to b
        return Runnable(lambda x: other.invoke(self.invoke(x)), f"{self.name} | {other.name}")

docs = ["To reset your password open settings and click reset link",
        "Refunds are issued to the original card within five days",
        "Export your data from the dashboard menu as a csv file",
        "The mobile app crash was fixed in the latest update"]
embedder = make_pipeline(TfidfVectorizer(), TruncatedSVD(n_components=3, random_state=0), Normalizer()).fit(docs)
E = embedder.transform(docs)

def retrieve(question, k=2):
    scores = E @ embedder.transform([question])[0]
    return {"question": question, "docs": [docs[i] for i in np.argsort(-scores)[:k]]}

def build_prompt(d):
    context = "\n".join(f"- {t}" for t in d["docs"])
    return f"Answer from the context only.\nContext:\n{context}\nQuestion: {d['question']}"

def fake_model(prompt):
    lines = [l[2:] for l in prompt.splitlines() if l.startswith("- ")]
    return {"content": lines[0] if lines else "unknown", "prompt_chars": len(prompt)}   # echoes the best chunk

parse = Runnable(lambda msg: msg["content"].strip(), "parse")
chain = Runnable(retrieve, "retrieve") | Runnable(build_prompt, "prompt") | Runnable(fake_model, "model") | parse

print("chain:", chain.name)
print(chain.invoke("how do I reset my password"))
print(chain.batch(["where do refunds go", "export csv data"]))

prompt_text = (Runnable(retrieve) | Runnable(build_prompt)).invoke("where do refunds go")
print(prompt_text)
%%END
<ol><li>A <code>Runnable</code> wraps one function. <code>__or__</code> is the special method Python calls for <code>a | b</code>; it returns a new Runnable that calls <code>a</code> and passes its result to <code>b</code>. That is the whole trick behind <code>prompt | model | parser</code>.</li><li><code>retrieve</code> returns a dictionary because the next step needs both the question and the documents. In LangChain that is what the dict-of-runnables syntax produces.</li><li><code>build_prompt</code> turns the dictionary into the text a model would receive. <code>fake_model</code> stands in for a real model: it returns an object with a <code>content</code> field, as chat model replies do.</li><li>The chain output for the password question is the password document, the refund question returns the refund sentence, and the export question returns the export sentence: the retriever put the matching document first, and the scripted model repeats the first context line.</li><li>The last print shows the intermediate prompt. Being able to print the prompt that was actually sent is the most useful debugging move in any LLM pipeline: most "the model is wrong" bugs are "the model was given the wrong context".</li></ol>
<div class="callout cream"><div class="lab">REAL JOB</div><div class="txt">Use a framework when it removes code you would otherwise write (provider switching, tracing, retries, vector store adapters). Skip it when it hides what is sent to the model. A good rule: you must be able to print the final prompt and the raw response at any step. If a framework makes that hard, wrap the SDK directly; the patterns in 21.9 are only a few dozen lines.</div></div>
<h3>Evaluation: the harness that tells you if you improved</h3>
<p>An <strong>evaluation harness</strong> is a script that runs your system on a fixed set of examples with known good answers and reports numbers. The ingredients are always the same: (1) a <strong>golden set</strong> of inputs with expected outputs, held out from any prompt tuning; (2) a <strong>metric</strong> that fits the task; (3) a <strong>baseline</strong> to beat; (4) <strong>uncertainty</strong>, because a difference of three points on 100 examples may be noise.</p>
<div class="tablewrap"><table class="data"><thead><tr><th>Task</th><th>Metrics to use</th><th>Watch out for</th></tr></thead><tbody>
<tr><td>Classification / extraction</td><td>Accuracy, per-class precision and recall, exact match on fields, JSON validity rate</td><td>Class imbalance hides failures behind a high accuracy</td></tr>
<tr><td>Retrieval</td><td>recall@k, MRR, nDCG@k</td><td>Labelling only one relevant document when several are valid</td></tr>
<tr><td>Short-answer QA</td><td>Exact match, token F1</td><td>Correct answers phrased differently score zero on exact match</td></tr>
<tr><td>Free-text generation</td><td>Rubric scoring by humans or an LLM judge, groundedness (is each claim supported by the context?)</td><td>Judges favour long answers; check judge agreement with humans</td></tr>
<tr><td>Operations</td><td>Latency percentiles (p50, p95), cost per request, refusal rate</td><td>Averages hide the slow tail</td></tr>
</tbody></table></div>
<p>First the retrieval metrics, small enough to check by hand. Suppose the relevant documents for a query are {2, 5} and the system returns [7, 2, 9, 5, 1]. <strong>recall@3</strong> = relevant found in the top 3 divided by relevant total = 1/2. <strong>MRR</strong> (mean reciprocal rank) uses 1 divided by the rank of the first relevant hit = 1/2. <strong>nDCG@5</strong> rewards early hits: DCG = 1/log<sub>2</sub>(3) + 1/log<sub>2</sub>(5) = 0.6309 + 0.4307 = 1.0616; the ideal ranking would put both at ranks 1 and 2, IDCG = 1 + 0.6309 = 1.6309; nDCG = 0.651.</p>
%%PY
import numpy as np

def recall_at_k(ranked, relevant, k):
    return len(set(ranked[:k]) & set(relevant)) / len(relevant)

def precision_at_k(ranked, relevant, k):
    return len(set(ranked[:k]) & set(relevant)) / k

def mrr(ranked, relevant):
    for rank, item in enumerate(ranked, start=1):
        if item in relevant:
            return 1 / rank
    return 0.0

def ndcg_at_k(ranked, relevant, k):
    dcg = sum(1 / np.log2(r + 1) for r, item in enumerate(ranked[:k], start=1) if item in relevant)
    ideal = sum(1 / np.log2(r + 1) for r in range(1, min(len(relevant), k) + 1))
    return dcg / ideal

ranked, relevant = [7, 2, 9, 5, 1], {2, 5}
print("recall@3   :", recall_at_k(ranked, relevant, 3))
print("recall@5   :", recall_at_k(ranked, relevant, 5))
print("precision@3:", round(precision_at_k(ranked, relevant, 3), 4))
print("MRR        :", mrr(ranked, relevant))
print("nDCG@5     :", round(ndcg_at_k(ranked, relevant, 5), 4))

def token_f1(pred, gold):
    p, g = pred.lower().split(), gold.lower().split()
    common = sum(min(p.count(w), g.count(w)) for w in set(p))
    if common == 0:
        return 0.0
    prec, rec = common / len(p), common / len(g)
    return 2 * prec * rec / (prec + rec)
print("exact match:", "reset link" == "reset the link", "| token F1:", round(token_f1("reset link", "reset the link"), 3))
%%END
<ol><li>The functions mirror the hand calculations: recall@3 is 0.5 because only document 2 is among the top three; recall@5 is 1.0.</li><li><code>precision@3</code> is 1/3 because one of three returned documents is relevant.</li><li>MRR is 0.5 (first relevant at rank 2). nDCG@5 prints 0.6509, the 0.651 computed by hand above; <code>ideal</code> assumes the relevant documents sit at the very top.</li><li>Token F1 gives partial credit: "reset link" versus "reset the link" has two shared words, precision 1.0, recall 2/3, F1 = 0.8, while exact match says False. That is why QA evaluation uses both.</li></ol>
<p>Now a whole harness on a realistic comparison: a keyword-rule baseline versus a TF-IDF plus logistic regression classifier on a held-out set of synthetic tickets (generated with overlapping vocabulary so the task is not trivial). We report accuracy, a confusion matrix, and a <strong>paired bootstrap</strong> confidence interval for the accuracy difference: resample test examples with replacement many times, recompute the difference each time, and read off the middle 95 percent.</p>
%%PY
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix

rng = random.Random(0)
pools = {
    "billing": ["refund", "charged", "invoice", "payment", "card", "receipt", "subscription", "price", "billing", "discount"],
    "bug": ["crash", "error", "broken", "freezes", "fails", "slow", "bug", "blank", "timeout", "stuck"],
    "how-to": ["how", "export", "reset", "change", "find", "invite", "connect", "setup", "where", "enable"],
}
filler = ["the", "my", "app", "page", "account", "please", "when", "on", "I", "can", "with", "after", "today", "again", "dashboard"]
labels = list(pools)

def make(n):
    X, y = [], []
    for i in range(n):
        lab = labels[i % 3]
        words = rng.sample(pools[lab], rng.choice([1, 2]))
        if rng.random() < 0.6:                                    # confusing words from another class
            other = rng.choice([l for l in labels if l != lab])
            words += rng.sample(pools[other], rng.choice([1, 2]))
        words += rng.sample(filler, 3)
        rng.shuffle(words)
        X.append(" ".join(words)); y.append(lab)
    return X, np.array(y)

Xtr, ytr = make(300)
Xte, yte = make(150)

model = make_pipeline(TfidfVectorizer(), LogisticRegression(max_iter=1000)).fit(Xtr, ytr)
pred_model = model.predict(Xte)

def rule(text):                                                   # the baseline to beat
    w = set(text.split())
    if w & {"refund", "charged", "invoice", "payment"}: return "billing"
    if w & {"crash", "error", "broken", "freezes"}: return "bug"
    return "how-to"
pred_rule = np.array([rule(t) for t in Xte])

ok_model, ok_rule = (pred_model == yte).astype(int), (pred_rule == yte).astype(int)
print("accuracy model:", round(ok_model.mean(), 3), " rule baseline:", round(ok_rule.mean(), 3))
print("model wins / baseline wins:", int(((ok_model == 1) & (ok_rule == 0)).sum()), "/", int(((ok_model == 0) & (ok_rule == 1)).sum()))

boot = np.random.default_rng(0)
diffs = []
for _ in range(2000):
    idx = boot.integers(0, len(yte), len(yte))
    diffs.append(ok_model[idx].mean() - ok_rule[idx].mean())
lo, hi = np.percentile(diffs, [2.5, 97.5])
print(f"accuracy gain 95% CI: [{lo:.3f}, {hi:.3f}]")
print("confusion matrix (rows true, columns predicted), order", labels)
print(confusion_matrix(yte, pred_model, labels=labels))
%%END
<ol><li>The generator mixes in words from other classes on purpose. Real data is ambiguous; a test set where everything is easy tells you nothing. (An earlier version of this script scored 100 percent, which was a warning sign that the task was too easy, not a success.)</li><li>Training and test sets are different draws. The model never sees the test tickets, and any prompt or threshold tuning must also use a separate validation set, never the test set.</li><li>The model scores 0.68 and the baseline 0.56. The win/loss count is a paired view: on 37 examples only the model was right, on 19 only the baseline was right. Paired comparison is more informative than two separate accuracies.</li><li>The bootstrap resamples the 150 test items 2,000 times. The interval for the gain is about 0.03 to 0.21: it excludes zero but is wide, so we can say the model is probably better, but the size of the gain is uncertain. With 150 examples you cannot detect small improvements; collect more labels or accept the uncertainty.</li><li>The confusion matrix shows where errors go. Each row is a true class; the diagonal is correct. Read the off-diagonal cells to decide what to fix: for example whether billing tickets are mistaken for bugs.</li><li>Replace the two classifiers with "prompt version 1" and "prompt version 2" calling an LLM and the harness is unchanged. That is the point: keep the harness fixed and change only the system under test.</li></ol>
<h3>LLM-as-judge, carefully</h3>
<p>For free text there is no single correct string, so teams ask a second model to grade replies against a rubric. It is useful but biased, so calibrate it: label 50 or more examples by hand, run the judge on the same examples, and measure agreement. Cohen's kappa corrects raw agreement for chance. Randomise the order when comparing two answers (judges often favour the first), and keep the rubric specific (for example "is every claim supported by the context?" rather than "is it good?").</p>
%%PY
import numpy as np
from sklearn.metrics import cohen_kappa_score

human = np.array([1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1])
judge = np.array([1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1])

agree = (human == judge).mean()
print("raw agreement:", agree)
print("kappa:", round(cohen_kappa_score(human, judge), 3))
print("judge says 'good' on", int(judge.sum()), "of", len(judge), "| humans say 'good' on", int(human.sum()))
fp = int(((judge == 1) & (human == 0)).sum())
print("judge approves", fp, "replies that humans rejected")

always_yes = np.ones_like(human)
print("an always-yes judge: agreement", (human == always_yes).mean(), "kappa", round(cohen_kappa_score(human, always_yes), 3))
%%END
<ol><li>The two arrays are the grades (1 = acceptable) from a person and from a judge for the same 20 replies. They disagree on exactly two replies, so raw agreement is 0.9.</li><li>Kappa is lower than 0.9 because some agreement would occur by chance, especially when most replies are good. Here kappa is 0.765. A kappa above about 0.6 is usually read as substantial agreement (a rule of thumb, not a law).</li><li>The judge is more lenient than the humans: it approves two replies that humans rejected. A lenient judge inflates every system's score, which matters if you compare against old numbers.</li><li>An always-yes judge reaches 0.65 raw agreement (13 of 20 replies are good) yet kappa 0.0. This is the reason to look at kappa and not only agreement.</li></ol>
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Wrong:</strong> editing the prompt until the score on the test set goes up, then reporting that score. <strong>Symptom:</strong> an impressive offline number that collapses in production, because the prompt now fits the test examples. <strong>Fix:</strong> tune on a validation set, touch the test set once at the end, and keep a few fresh real examples for a final check.</div></div>
