<p>Three months after the late-delivery model launched, Meera's team notices that the vouchers are going to the wrong orders. The data scientist who built the model has moved to another team. The notebook is on a laptop. Nobody remembers which months were used for training, which library version was used, or what threshold the operations team was told to use. The model is not wrong because the maths was wrong; it is wrong because nobody owns it, nobody watches it and nobody can rebuild it.</p>
<p>This final chapter closes the loop of the whole document. You will package the model with its preprocessing and a record of how it was built, wrap it in a validated prediction function, watch the data change under it (using the <strong>population stability index</strong>, PSI), decide when retraining is justified, write the model card, and finish with the thing the CEO actually asked for in Chapter 1: a short decision memo built from numbers you can reproduce. We then map the whole journey to five career paths and give you a one-page end-to-end checklist. Cloud deployment, containers and orchestration are explained and shown as code but marked <strong>not run here</strong>; everything that can run on your laptop is run.</p>

<h2>8.1 From notebook to product</h2>
<p>A model in a notebook is an experiment. A model in production is a small system with five parts, each with an owner.</p>
@@table
Part | Question it answers | ShopKart example
Artifact | What exactly is deployed? | Fitted pipeline (encoders, scaler, model), file hash, metadata
Interface | How does a caller get a prediction? | Function <code>predict_late(order)</code> or an HTTP endpoint
Validation | What if the input is wrong? | Reject unknown city, negative quantity, missing promise
Monitoring | Is it still right? | PSI on inputs and scores, monthly AUC once labels arrive
Lifecycle | When do we retrain, who approves? | Triggers, review, rollback to previous version
@@
<div class="callout green"><div class="lab">BASIC EXPLANATION</div><div class="txt">Deploying a model means packaging it as a service with data input, model, serving, monitoring and an owner for each. It is used to turn a notebook experiment into a system that others can use.</div></div>
<div class="callout blue"><div class="lab">INTUITION</div><div class="txt">Imagine a vending machine. The recipe (training code) is one thing. The machine (serving), the sensor that notices an empty slot (monitoring), the person who refills it (retraining) and the manual on its side (model card) are the rest. A great recipe in a broken machine sells nothing.</div></div>

<h2>8.2 Package: save the pipeline and its record</h2>
<p>The unit you save must include <em>preprocessing</em>. Saving only the model, and re-creating the encoders by hand in the serving code, is the most common cause of "works in the notebook, wrong in production" (training-serving skew). With scikit-learn the Pipeline object bundles both. Save it with <code>joblib</code> and write a <strong>metadata</strong> file next to it: training window, features, metrics, library versions and a hash of the training data.</p>
<p class="problem"><span class="pl">Problem 8.2.1</span> Train the Chapter 6 pipeline on January to September, save it with metadata, reload it in a fresh object and prove that predictions are identical.</p>
@@steps
Train | Pipeline(one-hot + scale, logistic regression) on orders before 1 October.
Save | <code>joblib.dump</code> the pipeline; write <code>meta.json</code> with window, features, test AUC, versions, data hash.
Reload | <code>joblib.load</code> into a new variable.
Verify | Compare predictions of the original and the reloaded object, bit for bit.
@@
@@py
import sys, os, json, hashlib, tempfile
sys.path.insert(0, DATA)
import prep, mlprep
import numpy as np, sklearn, joblib
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score

o, c, p = prep.load_clean(DATA)
d = mlprep.late_frame(o)
tr, te = d[d.order_date < "2024-10-01"], d[d.order_date >= "2024-10-01"]
F = mlprep.CAT + mlprep.NUM
pre = ColumnTransformer([("c", OneHotEncoder(handle_unknown="ignore"), mlprep.CAT), ("n", StandardScaler(), mlprep.NUM)])
model = make_pipeline(pre, LogisticRegression(max_iter=1000)).fit(tr[F], tr.late)

folder = tempfile.mkdtemp()
joblib.dump(model, os.path.join(folder, "late_model.joblib"))
meta = {"name": "late_delivery", "version": "1.0", "train_window": ["2024-01-01", "2024-09-30"], "features": F,
        "test_auc": round(roc_auc_score(te.late, model.predict_proba(te[F])[:, 1]), 4), "threshold": 0.11,
        "sklearn": sklearn.__version__, "rows": len(tr),
        "data_hash": hashlib.sha256(tr[F].to_csv().encode()).hexdigest()[:12]}
json.dump(meta, open(os.path.join(folder, "meta.json"), "w"), indent=1)

again = joblib.load(os.path.join(folder, "late_model.joblib"))
same = np.array_equal(model.predict_proba(te[F]), again.predict_proba(te[F]))
print("files:", sorted(os.listdir(folder)))
print("identical predictions after reload:", same)
print({k: meta[k] for k in ("version", "train_window", "test_auc", "threshold", "rows")})
@@
<p>The data hash is a short fingerprint: if someone retrains on slightly different data, the hash changes, so you can tell versions apart even when file names lie. A format caution: <code>joblib</code> and <code>pickle</code> files can execute code when loaded, so never load one from a source you do not trust. For sharing between languages, formats such as ONNX or PMML are safer (not run here).</p>
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Saving the model without its preprocessing.</strong> Wrong: saving only the logistic regression and re-implementing the encoding in the app, with categories in a different order. Predictions silently become garbage. Right: save one pipeline object, test the reloaded object against the original, and keep a few "golden" inputs with known outputs in your tests.</div></div>

<h2>8.3 Serve: a validated prediction function</h2>
<p>A prediction function is the simplest serving interface: input dictionary in, decision out. Production adds three things the notebook never had: <strong>input validation</strong>, <strong>explicit handling of unknowns</strong> and <strong>tests</strong>.</p>
@@py
import sys, os, json, tempfile, time
sys.path.insert(0, DATA)
import prep, mlprep
import pandas as pd, joblib
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import make_pipeline

o, c, p = prep.load_clean(DATA)
d = mlprep.late_frame(o)
tr = d[d.order_date < "2024-10-01"]
F = mlprep.CAT + mlprep.NUM
pre = ColumnTransformer([("c", OneHotEncoder(handle_unknown="ignore"), mlprep.CAT), ("n", StandardScaler(), mlprep.NUM)])
MODEL = make_pipeline(pre, LogisticRegression(max_iter=1000)).fit(tr[F], tr.late)
THRESHOLD, CITIES = 0.11, {"Bengaluru", "Mumbai", "Delhi", "Chennai", "Pune"}

def predict_late(order):
    """order: dict with city, channel, category, quantity, discount, order_hour, promised_minutes, weekend."""
    errors = []
    if order.get("city") not in CITIES: errors.append("unknown city")
    if order.get("channel") not in {"App", "Web", "Unknown"}: errors.append("bad channel")
    if not (isinstance(order.get("quantity"), (int, float)) and 1 <= order["quantity"] <= 20): errors.append("quantity out of range")
    if order.get("promised_minutes") not in (45, 60): errors.append("promise must be 45 or 60")
    if not (0 <= order.get("order_hour", -1) <= 23): errors.append("hour out of range")
    if errors:
        return {"ok": False, "errors": errors}
    row = dict(order, evening=int(18 <= order["order_hour"] <= 21))
    prob = float(MODEL.predict_proba(pd.DataFrame([row])[F])[:, 1][0])
    return {"ok": True, "p_late": round(prob, 3), "action": "intervene" if prob >= THRESHOLD else "none"}

good = dict(city="Bengaluru", channel="App", category="Grocery", quantity=2, discount=0.1, order_hour=19, promised_minutes=45, weekend=0)
print(predict_late(good))
print(predict_late(dict(good, order_hour=11, promised_minutes=60, city="Chennai")))
print(predict_late(dict(good, city="Atlantis", quantity=-3)))

# tests: the kind you keep in a repository
assert predict_late(good)["action"] == "intervene"
assert predict_late(dict(good, promised_minutes=60, order_hour=11))["action"] == "none"
assert not predict_late(dict(good, quantity=500))["ok"]
t = time.perf_counter()
for _ in range(200):
    predict_late(good)
ms = (time.perf_counter() - t) / 200 * 1000
print("single-order latency under 50 ms:", ms < 50)
@@
<p>The same function serves a single order (online, in milliseconds) or a whole file (batch): for a nightly batch, pass a DataFrame to <code>MODEL.predict_proba</code> directly, which is far faster than calling the function row by row. Pick online serving only when a decision is needed immediately; a nightly batch is cheaper, simpler and easier to monitor.</p>
@@python-not-run
# serve.py  (needs fastapi and uvicorn; run with: uvicorn serve:app --port 8000)
from fastapi import FastAPI
app = FastAPI()

@app.post("/predict")
def predict(order: dict):
    return predict_late(order)          # the function above, imported from the package
@@
@@table
Delivery style | Latency | Best for | Tools
Batch scoring | Minutes to hours | Nightly churn lists, weekly reports | cron, Airflow, SQL write-back
Online API | Milliseconds | Checkout fraud, delivery promise | FastAPI, Flask, cloud endpoints
Embedded in a report | Refresh time | Scores shown in a dashboard | Power BI Python/R step, dataflow AutoML
Spreadsheet | Manual | One-off analysis | Excel with a pasted score column
@@
<h3>Going deeper: containers and CI (not run here)</h3>
<p>A <strong>container</strong> (Docker) bundles the code, the pinned library versions and the model file into one image that runs the same everywhere, solving "works on my machine". A <strong>CI pipeline</strong> (GitHub Actions or similar) runs the tests on every change: unit tests for the function, a check that the saved model reproduces its golden predictions, and a comparison of the new model's metric against the current one. Only then does the image get deployed. The key idea is that deployment is a routine, repeatable and reversible action, not an event.</p>

<h2>8.4 Monitor: has the world changed?</h2>
<p>A model is a snapshot of the past. Two things go wrong after launch. <strong>Data drift</strong>: the inputs change (more orders in the evening, a new city). <strong>Concept drift</strong>: the relationship between inputs and the outcome changes (a new rider contract changes delivery times). Drift in inputs can be seen immediately, because inputs need no labels; performance can only be measured once outcomes are known.</p>
<p>The standard drift statistic is the <strong>population stability index</strong>. Split a feature into bins using the reference (training) period. For each bin let a be the share of reference data and b the share of new data. Then</p>
<div class="eq">PSI = Σ (b − a) × ln(b / a)</div>
<p>over the bins. Each term is non-negative; zero means identical distributions. A common rule of thumb: below 0.1 stable, 0.1 to 0.25 watch, above 0.25 significant shift. These thresholds are conventions, not laws.</p>
<p class="problem"><span class="pl">Problem 8.4.1</span> A feature has three bins with reference shares 0.50, 0.30, 0.20 and new shares 0.40, 0.30, 0.30. Compute PSI by hand and in code.</p>
@@steps
Term 1 | (0.40 − 0.50) × ln(0.40/0.50) = (−0.10) × (−0.2231) = 0.02231
Term 2 | (0.30 − 0.30) × ln(1) = 0
Term 3 | (0.30 − 0.20) × ln(0.30/0.20) = 0.10 × 0.4055 = 0.04055
PSI | 0.02231 + 0 + 0.04055 = 0.06286, which is stable (below 0.1)
@@
@@py
import sys
sys.path.insert(0, DATA)
import prep, mlprep
import numpy as np, pandas as pd

def psi(ref, new, eps=1e-4):
    ref, new = np.asarray(ref, float), np.asarray(new, float)
    a, b = np.clip(ref / ref.sum(), eps, None), np.clip(new / new.sum(), eps, None)
    return float(np.sum((b - a) * np.log(b / a)))
print("hand example:", round(psi([50, 30, 20], [40, 30, 30]), 5))

o, c, p = prep.load_clean(DATA)
d = mlprep.late_frame(o)
ref, new = d[d.order_date < "2024-07-01"], d[d.order_date >= "2024-10-01"]

def psi_cat(col):
    cats = sorted(d[col].dropna().unique())
    return psi([(ref[col] == k).sum() for k in cats], [(new[col] == k).sum() for k in cats])
def psi_num(col, bins=10):
    edges = np.unique(np.quantile(ref[col].dropna(), np.linspace(0, 1, bins + 1)))
    edges[0], edges[-1] = -np.inf, np.inf
    return psi(np.histogram(ref[col].dropna(), edges)[0], np.histogram(new[col].dropna(), edges)[0])

rows = [(c_, "categorical", psi_cat(c_)) for c_ in ["city", "channel", "category", "promised_minutes"]]
rows += [(c_, "numeric", psi_num(c_)) for c_ in ["order_hour", "quantity", "discount"]]
t = pd.DataFrame(rows, columns=["feature", "type", "psi"])
t["status"] = np.where(t.psi < 0.1, "stable", np.where(t.psi < 0.25, "watch", "shift"))
print(t.round(4).to_string(index=False))
@@
<p>All input PSIs are tiny: in this synthetic world the inputs are stationary, so the model's inputs did not drift. That is itself a finding, and it tells you where to look next: if performance fell while PSI stayed low, the cause is concept drift or a label problem, not a change in the data feeding the model. Let us look at the output side: the churn rate in Chapter 6 rose from 23 to 31 percent between cut-offs, a drift in the <em>label</em>. Here, the performance of a frozen model month by month:</p>
@@py
import sys
sys.path.insert(0, DATA)
import prep, mlprep
import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score

o, c, p = prep.load_clean(DATA)
d = mlprep.late_frame(o)
F = mlprep.CAT + mlprep.NUM
def fit(df):
    pre = ColumnTransformer([("c", OneHotEncoder(handle_unknown="ignore"), mlprep.CAT), ("n", StandardScaler(), mlprep.NUM)])
    return make_pipeline(pre, LogisticRegression(max_iter=1000)).fit(df[F], df.late)

frozen = fit(d[d.order_date < "2024-07-01"])
rows = []
for m in range(7, 13):
    month = d[d.order_date.dt.month == m]
    retrained = fit(d[d.order_date < f"2024-{m:02d}-01"])
    rows.append((f"2024-{m:02d}", len(month), month.late.mean(),
                 roc_auc_score(month.late, frozen.predict_proba(month[F])[:, 1]),
                 roc_auc_score(month.late, retrained.predict_proba(month[F])[:, 1])))
t = pd.DataFrame(rows, columns=["month", "orders", "late_rate", "auc_frozen", "auc_retrained_monthly"])
print(t.round(4).to_string(index=False))
print("mean AUC frozen:", round(t.auc_frozen.mean(), 4), "| retrained monthly:", round(t.auc_retrained_monthly.mean(), 4))
@@
<p>With a stable world the frozen model stays as good as the monthly retrained one; retraining every month would have cost effort and bought nothing. Month-to-month AUC wanders between 0.82 and 0.86 for both versions just from sampling noise (a month has only 1,300 to 1,700 labelled orders), so a one- or two-point dip is noise, not drift, and July's 0.8155 would have been a false alarm. Set alert thresholds with that noise in mind.</p>

<div class="callout green"><div class="lab">BASIC EXPLANATION</div><div class="txt">Monitoring is the regular checking of a deployed model's inputs, predictions and accuracy over time. It is used to detect drift, which means the data has changed and the model may need retraining.</div></div>

@@blue
Monitoring is a smoke detector, not a fire brigade. It tells you when to look. Because every metric has noise, a good alert needs a threshold wider than the noise and a rule such as "two periods in a row" so that you are not woken up by chance.
@@
<h2>8.5 Retrain: triggers and rules</h2>
<p>Retraining on a calendar is easy but may waste effort or arrive too late. Triggers based on evidence are better.</p>
@@table
Trigger | Rule of thumb | Needs labels? | Example action
Input drift | PSI above 0.25 on a key feature or on the score | No | Investigate; retrain if confirmed
Performance drop | Rolling AUC below baseline by more than the noise (for example 0.03) for two periods | Yes, delayed | Retrain, compare, review
Label shift | Event rate moves outside the control band | Yes | Recalibrate threshold or retrain
Business change | New city, new promise policy, new product line | No | Retrain after enough new data
Calendar | Every quarter | No | Safety net
@@
<p>Every retrain follows the same gate: train the candidate on the new window, score both the candidate and the current model on the <em>same</em> recent hold-out, require a meaningful improvement, review fairness checks, record the new version, and keep the previous version one command away (rollback). A model that does not beat its predecessor on a fair test is not deployed, however new it is.</p>
<div class="callout green"><div class="lab">KEY IDEA</div><div class="txt">Labels arrive late. A late delivery is known within the hour, but a churned customer is known only after 90 days. Plan monitoring around the delay: use input drift and score drift for early warning, and performance for confirmation.</div></div>
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Retraining on the model's own decisions.</strong> Wrong: training only on orders that were not flagged (because flagged ones were rescued and their lateness was prevented), so the model learns that flagged-type orders are rarely late and gets worse. Right: keep a small random holdout that receives no intervention, and train on it or reweight; this feedback loop is a classic production failure.</div></div>

<h2>8.6 Document: the model card and the decision memo</h2>
<p>Two documents travel with a model. The <strong>model card</strong> is for colleagues and auditors: what the model is for, how it was built, how it performs, where it should not be used. The <strong>decision memo</strong> is for the person who asked the question in the first place. Both can be generated from the same numbers the analysis produced, which prevents the commonest memo error: a number typed by hand that no longer matches the data.</p>
@@table
Model card section | Content for the late-delivery model
Purpose | Flag orders likely to miss their promise at order time, to trigger rescue actions
Data | Orders Jan to Sep 2024 with promise and delivery times; cleaning rules from Chapter 3
Features | City, channel, category, quantity, discount, hour, weekend, evening, promise
Metrics | ROC-AUC, PR-AUC, precision and recall at the chosen threshold, cost
Limits | Trained on one year, five cities; not for pricing; unreliable in new cities
Fairness | Recall differs across cities at one threshold; see Chapter 6
Monitoring | PSI monthly; AUC when labels arrive; owner and contact
@@
<p>Now the memo itself, produced by code from the cleaned data. The recommendations are the analyst's judgement, but every number is computed.</p>
@@py
import sys
sys.path.insert(0, DATA)
import prep, mlprep
import pandas as pd

o, c, p = prep.load_clean(DATA)
rev = o.revenue.sum()
cat = o.groupby("category").revenue.sum().sort_values(ascending=False)
city = o.groupby("city").revenue.sum().sort_values(ascending=False)
m = o.groupby(o.order_date.dt.month).revenue.sum()
ret = o.groupby("category").apply(lambda d: (d.status == "returned").mean(), include_groups=False).sort_values(ascending=False)
late = o.late.mean()
per = o.groupby("customer_id").size()
memo = f"""MEMO to the CEO: ShopKart 2024 in five lines
1. Size: {len(o):,} orders, rupees {rev/1e6:.1f} million net revenue (delivered orders, after cleaning).
2. Where: {cat.index[0]} ({cat.iloc[0]/rev:.0%}) and {cat.index[1]} ({cat.iloc[1]/rev:.0%}) lead; {city.index[0]} is the top city ({city.iloc[0]/rev:.0%}).
3. Trend: revenue peaked in month {m.idxmax()} and fell in the autumn; a late-November promotion lifted November by {m[11]/m[10]-1:.0%} over October.
4. Service: {late:.1%} of deliveries miss their promise; 45-minute promises are late {o[o.promised_minutes==45].late.mean():.0%} of the time against {o[o.promised_minutes==60].late.mean():.0%} for 60-minute ones.
5. Returns: {(o.status=='returned').mean():.1%} overall; {ret.index[0]} is highest at {ret.iloc[0]:.0%}.
Customers: {(per>=2).mean():.0%} of customers who ordered placed at least two orders; {(~c.customer_id.isin(o.customer_id)).sum():,} registered customers never ordered.
RECOMMENDATIONS
 a. Review the 45-minute promise: it accounts for most late deliveries; test 60 minutes in one city with a randomised experiment (about 19,000 orders per arm needed to see a one-point change).
 b. Use the late-delivery model (AUC about 0.84) to trigger rescue actions at a cost-based threshold; re-check recall by city before rollout.
 c. Reduce Fashion returns before spending on acquisition there.
 d. Win back the never-ordered customers with a first-order offer, measured with a holdout group.
LIMITS: one year of data, five cities, no cost of goods per delivery, discounts not shown to raise basket size."""
print(memo)
@@
<p>Read the memo as a reader would. Every claim is a fact computed from the cleaned table or a recommendation tied to such a fact; each recommendation names how to <em>test</em> it, and the limits are stated. Compare this with the vague email that began Chapter 1: the work between them is the document you have just read.</p>
@@table
Tool | Delivering the same story (not run here)
Excel | One summary sheet with PivotTables and charts; lock formulas; Review, Protect Sheet; share via OneDrive with a refresh note
Power BI | Publish the report to the service; schedule refresh; row-level security by city manager; subscribe stakeholders to a weekly e-mail snapshot
R | R Markdown or Quarto report that re-runs the analysis and regenerates the memo on a schedule
Python | A notebook exported to HTML or PDF, or this memo printed by a scheduled job into e-mail
@@

<h2>8.7 Choose your path by role</h2>
<p>The journey of this document is the shared skeleton. Roles differ in where they spend their time. Pick the path that matches the job you want and read the other study documents on this site for depth (listed as "Next reading").</p>
@@table
Role | Spends most time in stages | Core tools | Read here | Next reading (other documents)
Data analyst | 1, 3, 4, 5, 8 (reports) | SQL, Excel, Power BI, pandas | Ch 1, 3, 4, 5, 8 | Analyst document, SQL document, Statistics document
Data engineer | 2, 3, 8 (pipelines) | SQL, Python, orchestration, warehouses | Ch 2, 3, 8 | SQL document, Data Engineering document, CS document
Data scientist | 3, 5, 6, 8 | pandas, scikit-learn, statistics | Ch 3, 5, 6, 8 | Statistics, Data Science, Machine Learning documents
ML engineer | 6, 8 | scikit-learn, packaging, APIs, monitoring | Ch 6, 8 | Machine Learning, MLOps, Python documents
GenAI engineer | 7, 8 | Embeddings, retrieval, prompts, evaluation | Ch 7, 8 | Deep Learning, NLP and GenAI, MLOps documents
@@
<p>A strong generalist can read all five columns of this table and writes confidently in two. When you interview, tell the story of one project from framing to monitoring: interviewers hire people who understand the whole path.</p>

<h2>8.8 The one-page end-to-end checklist</h2>
@@table
Stage | Checklist (tick each before moving on)
1 Frame | Decision named; ten questions with metric definitions; data dictionary; privacy and ethics noted
2 Engineer | Raw kept untouched; schema with keys; loads idempotent; quality checks run and visible; pipeline scripted
3 Clean | Duplicates, spellings, missing values, outliers, types handled by rules; cleaning log with effect on metrics
4 Analyse | Same answer in two tools; joins checked by row counts; windows ordered explicitly; charts with zero baseline and a stated takeaway
5 Test | Interval with every estimate; sample size planned; confounders considered; forecast scored on hold-out against a naive baseline
6 Model | Prediction time fixed; no leakage; time-based split; baseline beaten; threshold from costs; explained; fairness checked
7 Deep and GenAI | Compared with the simple model; retrieval and generation evaluated separately; guards on generated SQL; privacy of external calls checked
8 Deliver | Pipeline saved with metadata; input validation and tests; PSI and performance monitoring; retraining triggers; model card; decision memo with limits
@@
<div class="callout cream"><div class="lab">REAL JOB</div><div class="txt">Print this checklist and attach it to your next project. Teams that use even a short checklist avoid most of the failures in this document: the doubled revenue from a join, the leaked column, the unmonitored model. Experts are not people who never make these mistakes; they are people who have a habit that catches them.</div></div>

<h2>Chapter recap</h2>
<ul><li>A model in production is a system: artifact, interface, validation, monitoring and lifecycle.</li><li>Save the whole pipeline with metadata and a data hash; test that a reload reproduces predictions.</li><li>Wrap the model in a validated function with tests; choose batch unless you need immediate answers.</li><li>PSI = Σ(b − a) ln(b/a) compares a new distribution with the reference; below 0.1 stable, above 0.25 shift.</li><li>Input drift is visible at once; performance needs labels, which arrive late.</li><li>Retrain on evidence (drift, performance, business change) and gate each new version against the current one.</li><li>Keep a random no-intervention holdout to avoid training on the model's own effects.</li><li>Write a model card and generate the decision memo from code so numbers cannot drift from the data.</li><li>Choose a path by role; the whole journey is the shared skeleton.</li></ul>
@@table
Pattern | Meaning
<code>joblib.dump(pipeline)</code> + <code>meta.json</code> | Reproducible artifact with a record
PSI = Σ (b − a) ln(b / a) | Distribution drift score
Rolling AUC vs baseline | Performance monitoring once labels arrive
Candidate vs current on the same hold-out | Retraining gate
Model card + decision memo | Documentation for colleagues and decision-makers
@@

<h2>Practice set</h2>
@@qa 8.9
Q: Why must the preprocessing be saved together with the model?
A: Predictions depend on the exact encoders and scalers used in training; recreating them by hand risks different category orders and scaling (training-serving skew).
Q: Compute PSI for reference shares 0.6, 0.4 and new shares 0.5, 0.5.
A: (0.5 − 0.6) ln(0.5/0.6) + (0.5 − 0.4) ln(0.5/0.4) = (−0.1)(−0.18232) + (0.1)(0.22314) = 0.018232 + 0.022314 = 0.0405, stable.
Q: A feature has PSI 0.4 but the model's AUC is unchanged. What do you do?
A: Investigate the cause (new city, data bug, upstream change); the model may still be fine, but the shift is a warning and the next performance check should be earlier.
Q: Why is it a mistake to alert on every one-point fall in monthly AUC?
A: Monthly AUC has sampling noise of several points with only 1,300 to 1,700 labelled orders a month (here 0.82 to 0.86); alert on sustained drops larger than the noise.
Q: Give two reasons to prefer batch scoring to an online API.
A: Simpler and cheaper to run and monitor; no latency requirement. Use online only when the decision must happen immediately.
Q: What is the danger of loading a pickle or joblib file from an untrusted source?
A: Loading can execute arbitrary code embedded in the file.
Q: List four fields you would put in the model's metadata file.
A: Version, training window, feature list, library versions, data hash, test metric, threshold (any four).
Q: What is the retraining gate?
A: Train the candidate, evaluate candidate and current model on the same recent hold-out, require a meaningful improvement plus fairness and sanity checks, then deploy with rollback available.
Q: How can a model damage its own training data after deployment?
A: Its actions change outcomes (rescued orders are no longer late), so logged outcomes no longer reflect what would happen without intervention; keep a random holdout.
Q: Name two checks in the CI pipeline for a model.
A: Unit tests of the prediction function with golden inputs; comparison of the candidate metric against the current model; schema checks of input data.
Q: In the memo, why is each recommendation attached to a test?
A: Because the data supports associations, not causes; a randomised test or holdout turns a recommendation into a measured effect.
Q: Interview style: "Walk me through a project from raw data to production in two minutes."
A: Use the eight stages: frame the decision and metrics, ingest into a database with quality checks, clean with logged rules, analyse in SQL and pandas, test with intervals and an experiment plan, model with a time split and cost-based threshold, check against simpler options, deploy as a validated pipeline with monitoring and retraining triggers, and report with a memo that states limits.
@@

<h2>Prompt pack</h2>
@@prompt
You are my patient, practical professor. I am a working professional moving into data roles. Teach me MLOps basics through a late-delivery model: packaging a scikit-learn pipeline with metadata, serving it with input validation, monitoring drift with PSI, and deciding when to retrain. Ask one question at a time and have me compute a PSI by hand.
@@
@@prompt
Act as an ML platform lead reviewing my deployment plan: [paste plan]. Check artifact versioning, preprocessing included, input validation, tests, latency needs, monitoring (inputs, scores, performance with delayed labels), rollback, retraining triggers and feedback loops. Return a prioritised list of gaps and a one-page checklist.
@@
@@prompt
Run a mock end-to-end interview for a data role. Start with: "Tell me about a project from raw data to production." Interrupt with follow-ups on data quality, leakage, validation, drift, and how you would explain the result to a non-technical executive. Grade the answer against the eight stages: frame, engineer, clean, analyse, test, model, deep or GenAI, deliver.
@@
