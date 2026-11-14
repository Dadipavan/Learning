<p>The marketing director has just come back from a conference. "Everyone is talking about deep learning and chatbots," she says. "Can we use a neural network for the late-delivery model? And could customers just ask the dashboard questions in plain English?" These are two fair questions with two honest answers, and the wrong response to either is a shrug or a sales pitch. The right response is an experiment on your own data, run in an hour.</p>
<p>This chapter does that. We test whether a neural network beats the models of Chapter 6 on ShopKart's table (we write one from scratch with NumPy, so you see the mechanics, and compare it with scikit-learn's version). Then we turn to text: product descriptions become numbers (TF-IDF and a low-dimensional embedding), we build a search and question-answering retriever you can actually run, we assemble the prompt that a language model (LLM) would receive in a retrieval-augmented generation (RAG) system, and we write a safe guard for a text-to-SQL assistant. Anything that needs a trained transformer or an external model is shown as code and marked <strong>not run here</strong>: no GPU, no deep learning framework and no network call is needed for the runnable parts.</p>
<p>After this chapter you will know when deep learning and GenAI add value on business data, how to build their classical and runnable cousins, and how to spot the cases where a SQL query or a logistic regression is the right answer.</p>

<h2>7.1 When does deep learning help on a table?</h2>
<p>A neural network is a stack of simple functions: a weighted sum, a bend (a non-linear activation such as tanh), another weighted sum, a final sigmoid for a probability. Training adjusts the weights to reduce a loss by gradient descent. Neural networks shine when the input is images, audio, text or very large data, where they learn their own features. On <em>small tables</em>, carefully engineered features and tree or linear models usually match them. We test that claim instead of repeating it.</p>
@@table
Data type | Typical winner | Why
Tabular, thousands of rows | Logistic regression, boosting | Features already meaningful, little data for a network to exploit
Tabular, millions of rows, many categories | Boosting, sometimes networks with embeddings | Scale lets networks learn category representations
Images, audio | Deep networks | Raw pixels have no usable hand features
Text | Transformers | Meaning depends on word order and context
@@
<p class="problem"><span class="pl">Problem 7.1.1</span> Train a one-hidden-layer network from scratch with NumPy on the late-delivery features and compare its test AUC with scikit-learn's <code>MLPClassifier</code> and with the logistic regression of Chapter 6.</p>
@@steps
Architecture | Inputs (one-hot city, channel, category plus scaled numbers) → 16 hidden tanh units → 1 sigmoid output.
Forward | A = tanh(XW<sub>1</sub> + b<sub>1</sub>); P = σ(A·W<sub>2</sub> + b<sub>2</sub>).
Loss | Mean log loss: −mean(y log P + (1 − y) log(1 − P)).
Backward | dz = (P − y)/n; gW<sub>2</sub> = Aᵀdz; dA = dz·W<sub>2</sub> ⊙ (1 − A²); gW<sub>1</sub> = Xᵀ dA.
Update | Each weight minus learning rate × its gradient; repeat 400 times.
@@
@@py
import sys
sys.path.insert(0, DATA)
import prep, mlprep
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import roc_auc_score
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression

o, c, p = prep.load_clean(DATA)
d = mlprep.late_frame(o)
tr, te = d[d.order_date < "2024-10-01"], d[d.order_date >= "2024-10-01"]
F = mlprep.CAT + mlprep.NUM
pre = ColumnTransformer([("c", OneHotEncoder(handle_unknown="ignore", sparse_output=False), mlprep.CAT), ("n", StandardScaler(), mlprep.NUM)])
Xtr, Xte = pre.fit_transform(tr[F]), pre.transform(te[F])
ytr, yte = tr.late.values, te.late.values

rng = np.random.default_rng(0)
H = 16
W1, b1 = rng.normal(0, 0.3, (Xtr.shape[1], H)), np.zeros(H)
W2, b2 = rng.normal(0, 0.3, H), -1.8
sigmoid = lambda z: 1 / (1 + np.exp(-z))
lr, losses = 0.5, []
for epoch in range(400):
    A = np.tanh(Xtr @ W1 + b1)
    P = sigmoid(A @ W2 + b2)
    losses.append(-np.mean(ytr * np.log(P + 1e-9) + (1 - ytr) * np.log(1 - P + 1e-9)))
    dz = (P - ytr) / len(ytr)
    gW2, gb2 = A.T @ dz, dz.sum()
    dA = np.outer(dz, W2) * (1 - A ** 2)
    gW1, gb1 = Xtr.T @ dA, dA.sum(0)
    W1 -= lr * gW1; b1 -= lr * gb1; W2 -= lr * gW2; b2 -= lr * gb2
print("loss at epochs 0, 100, 399:", [round(float(losses[i]), 4) for i in (0, 100, 399)])

P_np = sigmoid(np.tanh(Xte @ W1 + b1) @ W2 + b2)
mlp = MLPClassifier((16,), max_iter=500, random_state=0).fit(Xtr, ytr)
lr_model = LogisticRegression(max_iter=1000).fit(Xtr, ytr)
print("numpy network AUC   :", round(roc_auc_score(yte, P_np), 4))
print("sklearn MLP AUC     :", round(roc_auc_score(yte, mlp.predict_proba(Xte)[:, 1]), 4))
print("logistic regression :", round(roc_auc_score(yte, lr_model.predict_proba(Xte)[:, 1]), 4))
@@
<figure><img src="images/ch07_nn_embed.png" alt="Left: training loss curve of the numpy network falling from 0.41 to 0.30. Right: two-dimensional map of product descriptions coloured by category" loading="lazy"/><figcaption>Left: the loss of our hand-written network falls quickly and flattens. Right: product descriptions mapped to two dimensions with TF-IDF and SVD (Section 7.3).</figcaption></figure>
<p>How to read the left panel: the loss drops fast in the first 100 epochs (the network learns the big effects such as the promise) and then flattens, because nothing more can be learned from these seven fields. The three AUCs are within about 0.01 of one another. The neural network does not beat logistic regression here: the relationship is simple and the data small. A fair summary for the director: "A network costs more to train, explain and maintain and gave no gain on this table; boosting and logistic regression stay."</p>
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Reaching for deep learning because it sounds modern.</strong> Wrong: replacing a working logistic regression with a network and calling the 0.002 AUC difference an improvement. Right: define the gain that would justify extra cost (say +0.02 AUC or a measurable saving), compare on the same time-based split, and keep the simpler model if it does not clear the bar.</div></div>
<div class="callout green"><div class="lab">BASIC EXPLANATION</div><div class="txt">Deep learning uses neural networks with many layers to learn patterns from data. On tabular data it is used when there is enough data and non-linear structure, and it is compared with simpler models.</div></div>

@@blue
A neural network is a very flexible curve-fitter. Flexibility helps when the true pattern is complicated and you have lots of data to pin it down. When the true pattern is simple, flexibility has nothing to add and only costs you training time and clarity.
@@
<h3>Going deeper: why the loss curve flattens</h3>
<p>The loss of a perfectly specified model on noisy labels cannot reach zero: late delivery here depends on rain and random gamma-distributed delays that no feature records. A flat curve at 0.30 is the <em>noise floor</em> for these features. More layers cannot lower it; only new information (weather, rider location, traffic) can. When a more powerful model does not help, ask what information is missing, not what architecture is next.</p>

<h2>7.2 Text as numbers: TF-IDF by hand and in scikit-learn</h2>
<p>A model cannot read words. The oldest useful trick turns a document into a vector of word counts, then reweights so that common words matter less. <strong>TF-IDF</strong> (term frequency times inverse document frequency) gives a word a high weight if it appears often in <em>this</em> document and in few others. With N documents and a word appearing in df of them: tf-idf = tf × (ln((1 + N)/(1 + df)) + 1) in scikit-learn's smoothed version, then each document vector is scaled to length 1.</p>
<p class="problem"><span class="pl">Problem 7.2.1</span> Compute TF-IDF by hand for three mini descriptions and check it with scikit-learn.</p>
@@steps
Documents | d1 "fresh rice rice", d2 "fresh tea", d3 "premium tea" (N = 3).
Counts | d1: fresh 1, rice 2. d2: fresh 1, tea 1. d3: premium 1, tea 1.
Document frequency | fresh 2, rice 1, tea 2, premium 1.
IDF | ln(4/3) + 1 = 1.2877 for df = 2; ln(4/2) + 1 = 1.6931 for df = 1.
d1 raw | fresh 1.2877; rice 2 × 1.6931 = 3.3863; length √(1.658 + 11.466) = 3.6227; scaled: fresh 0.3555, rice 0.9347.
@@
@@py
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

docs = ["fresh rice rice", "fresh tea", "premium tea"]
v = TfidfVectorizer()
X = v.fit_transform(docs).toarray()
print(v.get_feature_names_out())
print(np.round(X, 4))

idf = lambda df: np.log((1 + 3) / (1 + df)) + 1
raw = np.array([1 * idf(2), 2 * idf(1)])
print("by hand d1:", np.round(raw / np.linalg.norm(raw), 4))
@@
<p>The hand calculation (0.3555 for "fresh", 0.9347 for "rice") matches the first row of scikit-learn's matrix: the rare word "rice" gets the larger weight inside d1. Once documents are vectors, similarity is the angle between them: the <strong>cosine similarity</strong> is the dot product of two unit vectors, from 0 (no shared words) to 1 (same direction).</p>
<h3>Similar products and a low-dimensional embedding</h3>
<p>Apply it to the 32 catalogue descriptions. First find which products are textually closest to "Earbuds". Then compress the 40-odd word dimensions into 2 with a truncated SVD (the same decomposition behind PCA); the resulting coordinates are a crude <strong>embedding</strong>, a short dense vector in which similar texts sit nearby.</p>
@@py
import pandas as pd, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

p = pd.read_csv(DATA + "products.csv")
V = TfidfVectorizer()
T = V.fit_transform(p.description)
print("vocabulary size:", len(V.vocabulary_), "| matrix shape:", T.shape)
i = p.index[p["product"] == "Earbuds"][0]
print("description:", p.description[i])
sim = cosine_similarity(T[i], T).ravel()
for j in np.argsort(-sim)[1:4]:
    print(f"  {sim[j]:.3f}  {p['product'][j]:14s} {p.description[j]}")

svd = TruncatedSVD(5, random_state=0).fit(T)
print("variance explained by 5 SVD dimensions:", round(svd.explained_variance_ratio_.sum(), 3))
@@
<p>Two of the three nearest descriptions are other electronics (they share "electronics shoppers"), but the third, a bedsheet, is there only because it shares "everyday" and "classic": the generated descriptions reuse a small vocabulary. That is the nature of bag-of-words: it measures word overlap, not meaning. Two products can be conceptually close and share no word ("headphones" and "earbuds"), or share words and mean different things. The right-hand panel of the figure shows a weak category structure for the same reason, and five SVD dimensions explain only a small share of the variance: with 32 short texts there is little to compress.</p>
<p><strong>Transformer embeddings</strong> (sentence-transformers, OpenAI or Cohere embedding models) fix the synonym problem by mapping text into a few hundred dimensions where meaning, not spelling, determines distance. They need a pretrained model, so this is shown as code (not run here):</p>
@@python-not-run
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")        # downloads a pretrained model
E = model.encode(products.description.tolist(), normalize_embeddings=True)
sim = E @ E[i]                                          # cosine similarity, same idea as above
@@
@@table
Approach | Needs | Strength | Weakness
TF-IDF | scikit-learn | Fast, transparent, no training data | Word overlap only
SVD / LSA on TF-IDF | scikit-learn | Dense short vectors, finds co-occurring words | Weak with tiny corpora
Pretrained sentence embeddings | Model download or API | Meaning, synonyms, multilingual | Cost, opaque, drift between model versions
Fine-tuned transformer | GPU, labelled data | Best task accuracy | Heavy to build and maintain
@@
<div class="callout green"><div class="lab">KEY IDEA</div><div class="txt">An embedding is a number-vector whose geometry reflects similarity. Everything downstream (search, clustering, recommendation, classification) is vector arithmetic on those numbers. Better embeddings give better downstream results with the same simple arithmetic.</div></div>

<h2>7.3 A question-answering search you can run: retrieval first</h2>
<p>A RAG system answers a question in two steps: <strong>retrieve</strong> the most relevant passages from your own documents, then <strong>generate</strong> an answer with an LLM that is told to use only those passages. The retrieval half is classical information retrieval and runs here. Its quality caps the quality of the whole system: if the right passage is not retrieved, no LLM can answer from it.</p>
@@py
import pandas as pd, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

p = pd.read_csv(DATA + "products.csv")
V = TfidfVectorizer(ngram_range=(1, 2))
T = V.fit_transform(p["product"].str.lower() + " " + p.description)

def search(q, k=3):
    s = cosine_similarity(V.transform([q]), T).ravel()
    idx = np.argsort(-s)[:k]
    return [(p["product"][i], p.category[i], round(float(s[i]), 3)) for i in idx]

for q in ["something to keep my phone charged", "olive oil for cooking", "durable sneakers", "gentle face wash"]:
    print(q, "->", search(q))

# evaluation: query = product name; is the right product ranked first?
hit1 = np.mean([search(name.lower(), 1)[0][0] == name for name in p["product"]])
# vaguer query: only category words; is a product of that category in the top 3?
cat_hit = np.mean([any(c == cat for _, c, _ in search(f"{cat.lower()} shoppers everyday", 3)) for cat in p.category.unique()])
print("top-1 accuracy for exact product-name queries:", round(hit1, 3))
print("top-3 category hit rate for vague category queries:", round(cat_hit, 3))
@@
<p>Look at the first query: "something to keep my phone charged" shares no word with "Power Bank", so lexical retrieval fails. Exact names and strong keywords work (top-1 accuracy 1.0 above, and the vague category queries also hit because the category word appears in every description), while meaning-based queries without shared words return nothing useful (all scores 0.0). That is the case for embeddings or a hybrid (keyword plus embedding) search, and it shows why measuring retrieval with a small labelled query set is the first thing to do before connecting an LLM.</p>
<p>The generation step takes the retrieved passages and builds a prompt. We assemble it here; sending it to a model is the part marked not run here.</p>
@@py
import pandas as pd, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

p = pd.read_csv(DATA + "products.csv")
V = TfidfVectorizer()
T = V.fit_transform(p["product"].str.lower() + " " + p.description)
question = "Which product is good for cooking and what does it cost?"
s = cosine_similarity(V.transform([question]), T).ravel()
top = np.argsort(-s)[:2]
context = "\n".join(f"[{i + 1}] {p['product'][j]} (category {p.category[j]}, list price {p.list_price[j]:.0f}): {p.description[j]}" for i, j in enumerate(top))
prompt = ("Answer using ONLY the passages. If the answer is not in them, say 'I do not know'. Cite passage numbers.\n\n"
          f"Passages:\n{context}\n\nQuestion: {question}\nAnswer:")
print(prompt)
@@
<p>Look at what retrieval returned: the question asks about cooking, but no description mentions cooking, so the retriever matched filler words ("good", "for", "which") and returned two Fashion items. This is the case the 'I do not know' instruction exists for, and a reminder to remove stop words or require a minimum similarity before passing passages on. Three safeguards in that prompt carry the engineering: restricting the answer to the passages, allowing "I do not know", and requiring citations so a human can check. The call itself looks like this (not run here; any chat-model API has the same shape):</p>
@@python-not-run
import anthropic                                   # or openai, google-genai, a local model
client = anthropic.Anthropic()                      # reads the API key from the environment
reply = client.messages.create(model="<model-name>", max_tokens=300,
                               messages=[{"role": "user", "content": prompt}])
print(reply.content[0].text)
@@
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Evaluating the LLM answer while ignoring retrieval.</strong> Wrong: reading a few fluent answers and deciding the system works. Right: build a small test set of questions with known source passages, measure retrieval hit rate (is the right passage in the top k?) separately from answer faithfulness (does the answer follow the passages?), and rerun both after every change.</div></div>

<h2>7.4 Text-to-SQL: letting people ask the database</h2>
<p>An LLM can translate "How many orders were returned in Mumbai?" into SQL, given the table schema. The danger is not that the SQL is wrong sometimes (you can review that), but that it is <em>executed</em> automatically: a wrong, slow or destructive query on a production database. The engineering pattern is therefore: schema in the prompt, query out, then a <strong>guard</strong> that allows only read-only statements on approved tables, executed on a read-only connection with a row limit.</p>
<p>We cannot call an LLM here, so we <em>pretend</em> its output with a fixed list of candidate queries, which is exactly how you would unit-test the guard.</p>
@@py
import sqlite3, re

SCHEMA = "orders(order_id, customer_id, order_date, city, channel, category, product, quantity, unit_price, discount, status, delivery_minutes)"
PROMPT = f"You write SQLite. Tables: {SCHEMA}. Return one SELECT statement only. Question: {{q}}"

ALLOWED_TABLES = {"orders", "customers", "products"}
def guard(sql):
    s = sql.strip().rstrip(";")
    if ";" in s:
        return False, "multiple statements"
    if not re.match(r"(?is)^(select|with)\b", s):
        return False, "only SELECT/WITH allowed"
    if re.search(r"(?i)\b(insert|update|delete|drop|alter|create|attach|pragma|replace)\b", s):
        return False, "write keyword found"
    tables = set(re.findall(r"(?i)\b(?:from|join)\s+([a-z_][a-z0-9_]*)", s))
    if not tables <= ALLOWED_TABLES:
        return False, f"table not allowed: {tables - ALLOWED_TABLES}"
    return True, "ok"

con = sqlite3.connect("file:" + DATA + "shopkart.db?mode=ro", uri=True)       # read-only connection
pretend_llm_outputs = {
    "How many orders were returned?": "SELECT COUNT(*) FROM orders WHERE status = 'returned'",
    "Delete all cancelled orders": "DELETE FROM orders WHERE status = 'cancelled'",
    "Show me the employees table": "SELECT * FROM employees",
    "Two things at once": "SELECT 1; DROP TABLE orders",
}
for q, sql in pretend_llm_outputs.items():
    ok, why = guard(sql)
    result = con.execute(sql + " LIMIT 5").fetchall() if ok else None
    print(f"{q!r:36} -> {why:28} {result if ok else ''}")
print(PROMPT.format(q="How many orders were returned?")[:100] + "...")
@@
<p>The count (2,976) comes from the <em>raw</em> table, which includes duplicates, a subtle point: an assistant querying raw tables will give different answers from your dashboard. Point it at the cleaned views and at a semantic layer where metrics like "revenue" and "late" are defined once. Otherwise you will have rebuilt the Chapter 1 argument about definitions, with a faster and more confident speaker.</p>
<div class="callout cream"><div class="lab">REAL JOB</div><div class="txt">Companies that ship text-to-SQL assistants invest more in the boring parts than in the model: a curated semantic layer, a read-only account with row and time limits, logging of every question and query, a test set of 100 or more questions with known answers, and a button "this answer is wrong" feeding back to the test set. Power BI's Copilot and Q&amp;A features follow the same logic over a governed model.</div></div>

@@green
Retrieval, generation and the guard are separate parts with separate tests. A failure in a RAG or text-to-SQL system is almost never "the model is bad"; it is usually bad retrieval, a missing definition, or a missing guard.
@@
<h2>7.5 Recommending products: co-purchase similarity</h2>
<p>Before language models, recommenders used behaviour. Build a customer-by-product matrix of purchase counts; two products are similar when the same customers buy both; similarity is the cosine of their columns. No text is needed.</p>
@@py
import sys
sys.path.insert(0, DATA)
import prep
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

o, c, p = prep.load_clean(DATA)
M = o.pivot_table(index="customer_id", columns="product", values="order_id", aggfunc="count", fill_value=0)
S = cosine_similarity(M.T.values)
names = list(M.columns)
i = names.index("Earbuds")
order = np.argsort(-S[i])[1:4]
print("matrix:", M.shape, "| Earbuds co-purchase neighbours:", [(names[j], round(float(S[i, j]), 3)) for j in order])
print("spread of similarities between all product pairs:", round(float(np.min(S[np.triu_indices(len(S), 1)])), 3), "to", round(float(np.max(S[np.triu_indices(len(S), 1)])), 3))
@@
<p>All similarities lie in a narrow band (0.16 to 0.39) because in this synthetic data customers pick products independently of each other (the generator draws the product at random within category), so heavy buyers buy everything and activity dominates the cosine. Real baskets contain structure (cameras with memory cards), and the same code then finds it. If your neighbours are all just "popular items", normalise for popularity before trusting a recommender.</p>

<div class="callout green"><div class="lab">BASIC EXPLANATION</div><div class="txt">Co-purchase similarity measures how often two products are bought by the same customers. It is used to recommend products that are similar to what a customer has already bought.</div></div>

@@blue
Think of retrieval as a librarian and the LLM as a writer. A brilliant writer with the wrong books on the desk writes confident nonsense; a mediocre writer with the right books is useful. Spend your effort on getting the right books to the desk.
@@
<h2>7.6 What LLMs add, and when not to use them</h2>
@@table
Task | Classical (runs here) | LLM / deep learning | Honest verdict for ShopKart
Predict late delivery | Logistic regression, boosting | Tabular network | Classical wins on cost and clarity
Answer "how many returns in Mumbai?" | SQL, dashboard | Text-to-SQL assistant | Dashboard first; assistant helps casual users, with guardrails
Find a product from a vague phrase | TF-IDF search | Embedding search | Embeddings clearly better on synonyms
Summarise 5,000 customer comments | Keyword counts, topic models | LLM summary | LLM adds real value; verify on a sample
Classify complaint emails | TF-IDF + logistic regression | Fine-tuned model or LLM prompt | Start classical, compare on 200 labelled emails
Write product descriptions | Templates | LLM | LLM, with human review
@@
<p>Four tests before using an LLM. (1) <strong>Is language the input or output?</strong> If not, probably no. (2) <strong>Is a wrong answer costly?</strong> If yes, add retrieval, citations, a human check. (3) <strong>Can a simpler method reach the target quality?</strong> Measure on labelled examples. (4) <strong>What does a call cost, how slow is it, where does the data go?</strong> Customer data sent to an external API may breach privacy policy (Chapter 1, Section 1.7).</p>
@@table
Tool | GenAI-related features (not run here)
Excel | Copilot suggests formulas and summaries; <code>=COPILOT()</code> style functions where available; Python in Excel for scikit-learn code
Power BI | Copilot to draft measures and report pages; Q&amp;A visual; AI visuals "Key influencers" and "Decomposition tree"; text analytics (sentiment, key phrases) in Power Query via Azure AI
R | Packages for embeddings and API calls (<code>httr2</code>, <code>ellmer</code>); tidytext for TF-IDF
SQL | Warehouse built-ins that call models (for example sentiment and summarise functions), vector indexes for embedding search
@@
<h3>Going deeper: how evaluation changes for generative systems</h3>
<p>A classifier has one right answer per row; a generator has many acceptable answers. Evaluate with (a) a fixed question set where facts can be checked, (b) metrics for retrieval (recall at k), (c) faithfulness checks (does every claim appear in a passage?), (d) side-by-side human preference on a sample, and (e) cost and latency budgets. Track all five over time: model updates change behaviour without notice, and so do changes in your documents.</p>

<h2>Chapter recap</h2>
<ul><li>On small tables a neural network matched but did not beat logistic regression (AUC within about 0.01).</li><li>A network is weighted sums, bends and gradient descent; backpropagation is the chain rule.</li><li>A flat loss means the information in the features is exhausted; more layers cannot help.</li><li>TF-IDF turns text into vectors; cosine similarity measures overlap; SVD gives short dense vectors.</li><li>Lexical retrieval fails on synonyms; embeddings address that and need a pretrained model.</li><li>RAG: retrieve, then generate from the retrieved passages, with citations and an "I do not know" option.</li><li>Measure retrieval separately from generation.</li><li>Text-to-SQL needs a guard, a read-only connection and a governed semantic layer.</li><li>Choose GenAI when language is the input or output and a simpler method cannot reach the quality.</li></ul>
@@table
Pattern | Meaning
tanh, sigmoid | Common activation functions; sigmoid maps to (0, 1)
tf-idf = tf × (ln((1+N)/(1+df)) + 1) | Word weight in a document (smoothed)
cos(a, b) = a·b / (‖a‖‖b‖) | Similarity of two vectors
RAG = retrieve + prompt + generate | Answers grounded in your own text
Guard + read-only + limit | Minimum safety for generated SQL
@@

<h2>Practice set</h2>
@@qa 7.7
Q: Name the four steps of one training iteration of a neural network.
A: Forward pass (predictions), loss computation, backward pass (gradients by the chain rule), weight update (weights minus learning rate times gradient).
Q: Why did the loss of the NumPy network flatten at about 0.30?
A: The features cannot explain the rest: rain and random delays are not recorded, so the label has irreducible noise.
Q: A network gets AUC 0.845 and logistic regression 0.844 on the same split. What do you recommend?
A: Keep logistic regression: the gain is far below the fold-to-fold noise and the simpler model is cheaper to run and explain.
Q: Compute the smoothed idf for a word in 1 of 9 documents.
A: ln((1 + 9)/(1 + 1)) + 1 = ln(5) + 1 = 2.609.
Q: Two unit vectors have dot product 0.6. What is their cosine similarity and angle?
A: Cosine 0.6; angle = arccos(0.6) ≈ 53.1 degrees.
Q: Why does "something to keep my phone charged" fail to retrieve "Power Bank" with TF-IDF?
A: They share no words; TF-IDF only measures word overlap. Embeddings would map both near each other.
Q: What three instructions in a RAG prompt reduce hallucination?
A: Answer only from the passages, say "I do not know" if absent, cite passage numbers.
Q: How would you measure retrieval quality before connecting an LLM?
A: Build 50 to 200 questions with known source passages and compute the share where the correct passage is in the top k (recall at k).
Q: List three guards for a text-to-SQL assistant.
A: Allow only SELECT on approved tables; run on a read-only connection with row and time limits; log and review queries (plus a test set of questions).
Q: The assistant says there were 2,976 returns while the dashboard says fewer. Give two causes.
A: It queried raw tables (duplicates, absurd values) instead of cleaned views, and its definition of "return" or the date filter differs from the dashboard's.
Q: Find the bug: embeddings from model A were used to index documents, then queries were embedded with model B.
A: The vector spaces differ; similarity between them is meaningless. Use the same model (and version) for both documents and queries.
Q: Interview style: "A VP wants an AI chatbot for sales data. How do you respond?"
A: Ask what decisions and which users; show that a governed dashboard answers common questions; if a chatbot still helps, propose a pilot: semantic layer, read-only access, guard, a test set with measured accuracy, logging, and a feedback loop, before a wider rollout.
@@

<h2>Prompt pack</h2>
@@prompt
You are my patient, practical professor. I am a working professional moving into data roles. Teach me how a small neural network learns, using a late-delivery prediction example: forward pass, loss, backpropagation, learning rate. Make me compute one gradient step by hand, then explain why a network did not beat logistic regression on a small table. One question at a time.
@@
@@prompt
Act as a GenAI engineer reviewing my plan for a question-answering assistant over product documentation: [paste design]. Check retrieval design, chunking, evaluation set, prompt constraints, citation, hallucination handling, privacy of data sent to an external API, cost and latency. Give a prioritised list of risks and a minimal evaluation plan.
@@
@@prompt
Run a mock interview for a GenAI or ML engineer role. Ask me one at a time: TF-IDF versus embeddings, RAG architecture, how to evaluate retrieval and generation separately, how to secure text-to-SQL, and when not to use an LLM. Grade each answer and give me a final score with next steps.
@@
