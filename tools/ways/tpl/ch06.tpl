<p>Meera's next question is the one every operations lead asks: "Can we know before the customer does that an order will be late?" If the app could warn a rider, add a courier, or send an apology voucher at the moment of ordering, the lateness that costs ShopKart reviews and returns could be reduced. This is a prediction task, and it is the doorway into machine learning (ML). The ML model is not magic: it is a function learned from past rows that turns known facts (hour, city, basket size, promised time) into a number between 0 and 1.</p>
<p>The path from data to a trustworthy model is longer than fitting a library function. In this chapter you will frame the problem (what exactly are we predicting, and <em>when</em>?), engineer features that exist at prediction time, avoid <strong>leakage</strong> (information from the future sneaking into the training data), validate on a later period like production will, compare a rule-based baseline with logistic regression, a random forest and gradient boosting, choose a threshold with money rather than habit, explain the model, and check it for fairness. We then repeat the key ideas on a second target, customer churn. Excel, Power BI and R versions are shown (not run here) so you can see which tool can do what.</p>
<p>Blocks use <code>scikit-learn</code>, which is installed here. Every score printed is real and reproducible: models use fixed seeds.</p>

<h2>6.1 Frame the prediction problem</h2>
<p>Five questions define any ML problem. Answer them in writing before touching a model.</p>
@@table
Question | ShopKart late delivery
What is the unit? | One delivery order
What is the target? | <code>late</code> = delivery minutes &gt; promised minutes (1 or 0)
When do we predict? | At the moment the order is placed
What do we know then? | City, hour, channel, category, quantity, discount, promised time, date
What decision follows? | If P(late) is high: reassign rider, warn customer, add voucher
@@
<p>The last two rows decide everything. If you predict at order time, you cannot use the delivery minutes, the status, or anything about what happens afterwards. Missing this is the single most common reason a model looks wonderful in a notebook and fails in production.</p>
<p>Next, know your baseline and your base rate. About 14 percent of orders with both times are late. A model that always says "on time" is right 86 percent of the time and useless. This is why <strong>accuracy</strong> is a poor metric for rare events; we use ranking and precision-recall measures instead.</p>
@@py
import sys
sys.path.insert(0, DATA)
import prep, mlprep

o, c, p = prep.load_clean(DATA)
d = mlprep.late_frame(o)
train = d[d.order_date < "2024-10-01"]
test = d[d.order_date >= "2024-10-01"]
print("orders with a target:", len(d), "| late share:", round(d.late.mean(), 4))
print("train (Jan-Sep):", len(train), round(train.late.mean(), 4), "| test (Oct-Dec):", len(test), round(test.late.mean(), 4))
print("accuracy of always saying on time:", round(1 - test.late.mean(), 4))
print(d.groupby("promised_minutes").late.mean().round(4).to_dict())
@@
<p>Notice the strongest single fact: orders promised in 45 minutes are late far more often than those promised in 60. The promise itself is a feature (it is known at order time), and the lateness target is partly a function of it. That is acceptable: we are predicting whether the service will meet its own promise.</p>
<div class="callout green"><div class="lab">KEY IDEA</div><div class="txt">Write the prediction time down. For every candidate column ask: "would I know this at that moment in production?" If the answer is no, the column cannot be a feature, however predictive it is.</div></div>

<h2>6.2 Features and leakage</h2>
<p><strong>Feature engineering</strong> turns raw columns into inputs a model can use: category columns become one-hot columns (one 0/1 column per value), numbers are scaled for models that care (logistic regression), and we add knowledge-based features such as <code>evening</code> (hours 18 to 21) and <code>weekend</code>. Tree models can find such thresholds themselves; linear models cannot, so a feature you add by hand is a gift to them.</p>
@@table
Column | Known at order time? | Use as feature?
city, channel, category, quantity, discount, hour, date | Yes | Yes
promised_minutes | Yes (set at order) | Yes
delivery_minutes | No: result of the delivery | Never; it defines the target
status (returned, cancelled) | No: happens after delivery | Never
revenue, net | Derived from status | Never
customer's average past lateness | Yes if computed from earlier orders only | Yes, with care
@@
<p>Watch what leakage does. We add <code>delivery_minutes</code> as a feature, a mistake a hurried person could easily make because the column is "right there".</p>
@@py
import sys
sys.path.insert(0, DATA)
import prep, mlprep
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score

o, c, p = prep.load_clean(DATA)
d = mlprep.late_frame(o)
train, test = d[d.order_date < "2024-10-01"], d[d.order_date >= "2024-10-01"]

def fit_auc(num):
    pre = ColumnTransformer([("c", OneHotEncoder(handle_unknown="ignore"), mlprep.CAT), ("n", StandardScaler(), num)])
    m = make_pipeline(pre, HistGradientBoostingClassifier(random_state=0)).fit(train[mlprep.CAT + num], train.late)
    return roc_auc_score(test.late, m.predict_proba(test[mlprep.CAT + num])[:, 1])

print("honest features      AUC:", round(fit_auc(mlprep.NUM), 4))
print("with delivery_minutes AUC:", round(fit_auc(mlprep.NUM + ["delivery_minutes"]), 4))
@@
<p>An AUC of 1.0 means perfect ranking, which no real problem allows. The target is literally "delivery minutes greater than the promise", so a model that sees delivery minutes just recomputes the target. If a result looks too good, assume leakage until proven otherwise. AUC (area under the ROC curve) is the probability that a randomly chosen late order gets a higher score than a randomly chosen on-time one: 0.5 is a coin flip and 1.0 is perfect.</p>
<p>Leakage has quieter forms. <strong>Target leakage</strong> (above), <strong>preprocessing leakage</strong> (fitting a scaler or imputer on all data before splitting, so test statistics leak into training), <strong>temporal leakage</strong> (random splitting so the model sees the future), and <strong>group leakage</strong> (the same customer in both train and test). Here is the fourth in miniature: a "customer lateness rate" feature computed from <em>all</em> data, including the very order being predicted.</p>
@@py
import sys
sys.path.insert(0, DATA)
import prep, mlprep
from sklearn.metrics import roc_auc_score

o, c, p = prep.load_clean(DATA)
d = mlprep.late_frame(o)
train, test = d[d.order_date < "2024-10-01"], d[d.order_date >= "2024-10-01"]

# leaky: customer's mean lateness over ALL their orders, including the test order itself
leaky = d.groupby("customer_id").late.transform("mean")[test.index]
print("leaky customer-rate feature AUC on test:", round(roc_auc_score(test.late, leaky), 4))

# honest: only orders before October
hist = train.groupby("customer_id").late.mean()
honest = test.customer_id.map(hist).fillna(train.late.mean())
print("honest customer-rate feature AUC on test:", round(roc_auc_score(test.late, honest), 4))
@@
<p>The leaky feature scores about 0.86, as good as the whole model, simply because the answer for the row itself is inside the average. The honest version scores about 0.50, a coin flip: a customer's past lateness tells us nothing about the next order in this data (lateness depends on the promise, city and hour, not on who the customer is). The leaky feature would have convinced us otherwise. Always build history features from rows strictly before the prediction time.</p>
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Celebrating a model that is too good.</strong> Wrong: "AUC 0.99, ship it!" Right: look at the top feature importances and ask whether each is known at prediction time; rerun with a time-based split; if the score collapses, you found leakage, not a model.</div></div>

<h2>6.3 Validation done right</h2>
<p>A model must be judged on data it has not seen, and in a way that mimics its future use. The usual recipe is a split: <strong>train</strong> to fit, <strong>validation</strong> to choose settings, <strong>test</strong> touched once at the end. Three styles exist.</p>
@@table
Split style | How | Use when | Risk
Random split | Shuffle rows, hold out 25% | Rows independent, no time effect | Leaks the future in time-ordered data
Time split | Train on earlier, test on later | Anything that evolves (almost everything here) | Fewer test rows; ranks may shift if the world changed
Group split | Keep each customer in one side | Many rows per person | Smaller effective sample
Cross-validation | Several splits, average | Small data, tuning | Costly; must respect time/groups
@@
<p>Compare a random split with the time split on the same model; the time split is the honest one.</p>
@@py
import sys
sys.path.insert(0, DATA)
import prep, mlprep
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.metrics import roc_auc_score

o, c, p = prep.load_clean(DATA)
d = mlprep.late_frame(o).sort_values("order_date").reset_index(drop=True)
X, y = d[mlprep.CAT + mlprep.NUM], d.late
pre = ColumnTransformer([("c", OneHotEncoder(handle_unknown="ignore"), mlprep.CAT), ("n", StandardScaler(), mlprep.NUM)])
model = make_pipeline(pre, LogisticRegression(max_iter=1000))

Xa, Xb, ya, yb = train_test_split(X, y, test_size=0.25, random_state=0)
print("random split AUC :", round(roc_auc_score(yb, model.fit(Xa, ya).predict_proba(Xb)[:, 1]), 4))

cut = int(len(d) * 0.75)
model.fit(X.iloc[:cut], y.iloc[:cut])
print("time split AUC   :", round(roc_auc_score(y.iloc[cut:], model.predict_proba(X.iloc[cut:])[:, 1]), 4))

scores = []
for tr, te in TimeSeriesSplit(n_splits=5).split(X):
    model.fit(X.iloc[tr], y.iloc[tr])
    scores.append(roc_auc_score(y.iloc[te], model.predict_proba(X.iloc[te])[:, 1]))
print("5 forward-chaining folds:", np.round(scores, 4), "mean", round(np.mean(scores), 4))
@@
<p>Here the three numbers are close (the random split even scores slightly lower, which is chance) because this synthetic world is stable. In real data with trends and promotions the random split is usually optimistic. Notice also the spread across folds (the third decimal moves): a single score is a point estimate, not a fact. Putting the scaler and encoder <strong>inside the pipeline</strong> guarantees they are fitted only on each training fold; that is how preprocessing leakage is prevented.</p>

<h2>6.4 Baseline, logistic regression, random forest, gradient boosting</h2>
<p>Four contenders, from simplest to most complex.</p>
@@table
Model | Idea | Strength | Weakness
Rule baseline | "Late if promised 45 minutes" | Zero training, explainable | Ignores everything else
Logistic regression | Weighted sum of features turned into a probability by the S-shaped function 1/(1+e<sup>−z</sup>) | Fast, interpretable, hard to overfit | Needs hand-made interactions
Random forest | Many decision trees on random subsets, averaged | Handles interactions, little tuning | Larger, slower, less smooth probabilities
Gradient boosting | Trees added one by one, each fixing the previous errors | Often the top on tables | More knobs; can overfit
@@
@@py
import sys
sys.path.insert(0, DATA)
import prep, mlprep
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score, average_precision_score

o, c, p = prep.load_clean(DATA)
d = mlprep.late_frame(o)
train, test = d[d.order_date < "2024-10-01"], d[d.order_date >= "2024-10-01"]
F = mlprep.CAT + mlprep.NUM
pre = ColumnTransformer([("c", OneHotEncoder(handle_unknown="ignore"), mlprep.CAT), ("n", StandardScaler(), mlprep.NUM)])
models = {
    "logistic regression": make_pipeline(pre, LogisticRegression(max_iter=1000)),
    "random forest": make_pipeline(pre, RandomForestClassifier(200, min_samples_leaf=20, random_state=0, n_jobs=-1)),
    "gradient boosting": make_pipeline(pre, HistGradientBoostingClassifier(random_state=0)),
}
rows = [("rule: promised 45", roc_auc_score(test.late, test.promised_minutes == 45), average_precision_score(test.late, (test.promised_minutes == 45).astype(float)))]
for name, m in models.items():
    s = m.fit(train[F], train.late).predict_proba(test[F])[:, 1]
    rows.append((name, roc_auc_score(test.late, s), average_precision_score(test.late, s)))
print("base rate (PR-AUC of a random model):", round(test.late.mean(), 3))
print(pd.DataFrame(rows, columns=["model", "ROC-AUC", "PR-AUC"]).round(4).to_string(index=False))
@@
<p>The result teaches three lessons. First, the rule already captures much of the signal (AUC about 0.74), which is a bar any model must clear. Second, all three learned models land close together near 0.84, with logistic regression marginally ahead: the true relationship here is an additive one (hour, city, promise) and a simple model captures it; extra flexibility adds no value. Third, PR-AUC (average precision) is about 0.45 against a base rate of 0.14, a threefold lift, a more honest summary for a rare event than ROC-AUC alone. In your own work, boosting often wins on messy tables with many interactions; this dataset is not one of them, and reporting that honestly is part of the job.</p>
<div class="callout blue"><div class="lab">INTUITION</div><div class="txt">Model complexity is a dial between underfitting (too simple to see the pattern) and overfitting (memorising noise). Compare training and test score: a large gap means overfitting. A good habit is to start at the simplest model that could work and move up only while the validation score improves meaningfully.</div></div>

<h2>6.5 Metrics, thresholds and money</h2>
<p>A model outputs probabilities; a decision needs a yes or no. Choosing the <strong>threshold</strong> is a business decision. At any threshold, count four outcomes: true positives (flagged and late), false positives (flagged, not late), false negatives (missed late orders), true negatives. <strong>Precision</strong> = TP ÷ (TP + FP) tells how many flags are right; <strong>recall</strong> = TP ÷ (TP + FN) tells how many late orders we catch.</p>
<p class="problem"><span class="pl">Problem 6.5.1</span> A proactive action (calling the rider, a 5-rupee message) costs 5 rupees per flagged order. A late order that we did not act on costs 60 rupees (voucher, lost goodwill). A late order we acted on costs 20 rupees. Choose the threshold that minimises total cost, using validation data, and report the result on the test set.</p>
@@steps
Setup | Train on Jan to Jun, choose the threshold on Jul to Sep (validation), report on Oct to Dec (test).
Cost per order | flagged: 5 (+ 20 if late); not flagged: 60 if late, else 0.
Search | Try thresholds from 0.05 to 0.60; pick the minimum validation cost.
Compare | Cost of acting on nobody, on everybody, and at the chosen threshold, on the test set.
@@
@@py
import sys
sys.path.insert(0, DATA)
import prep, mlprep
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import make_pipeline

o, c, p = prep.load_clean(DATA)
d = mlprep.late_frame(o)
tr = d[d.order_date < "2024-07-01"]
va = d[(d.order_date >= "2024-07-01") & (d.order_date < "2024-10-01")]
te = d[d.order_date >= "2024-10-01"]
F = mlprep.CAT + mlprep.NUM
pre = ColumnTransformer([("c", OneHotEncoder(handle_unknown="ignore"), mlprep.CAT), ("n", StandardScaler(), mlprep.NUM)])
m = make_pipeline(pre, LogisticRegression(max_iter=1000)).fit(tr[F], tr.late)

def cost(y, flag):
    y, flag = np.asarray(y), np.asarray(flag)
    return np.where(flag, 5 + 20 * y, 60 * y).sum()

pv, pt = m.predict_proba(va[F])[:, 1], m.predict_proba(te[F])[:, 1]
ths = np.round(np.arange(0.05, 0.61, 0.01), 2)
best = ths[np.argmin([cost(va.late, pv >= t) for t in ths])]
print("best threshold on validation:", best)
for label, flag in [("flag nobody", np.zeros(len(te), bool)), ("flag everybody", np.ones(len(te), bool)), (f"model at {best}", pt >= best)]:
    tp = (flag & (te.late.values == 1)).sum()
    print(f"{label:18s} cost {cost(te.late, flag):9,.0f}  flagged {flag.sum():5d}  recall {tp / te.late.sum():.3f}  precision {tp / max(flag.sum(), 1):.3f}")
@@
<p>The best threshold on validation is low (about 0.11): because a miss costs 60 and a flag costs 5, it is worth acting even when the chance of lateness is modest. Acting on nobody is the most expensive; acting on everyone wastes money on the 86 percent who would be on time; the model flags about 40 percent of orders, catches most late ones and is clearly the cheapest of the three. A general rule: act when P(late) × (cost saved by acting) &gt; cost of acting, here P × 40 &gt; 5, so P &gt; 0.125 on paper; the empirical optimum (0.11) is close to the theory, which is a sign that the probabilities are reasonably calibrated.</p>
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Using the default threshold 0.5.</strong> Wrong: predicting "late" only when P &gt; 0.5. With a 14 percent base rate almost no order reaches 0.5, so recall is close to zero and the model "never warns". Right: choose the threshold from costs on validation data, and report precision and recall at that point.</div></div>
<h3>Going deeper: calibration</h3>
<p>If a model says 0.2, are 20 percent of such orders actually late? That is <strong>calibration</strong>. Cost-based thresholds assume it. Logistic regression is usually well calibrated; random forests tend to be less so. Check by binning scores into deciles and comparing the average predicted score with the observed rate; fix with <code>CalibratedClassifierCV</code>.</p>

<h2>6.6 Explaining the model</h2>
<p>Stakeholders will not act on a black box. Three tools of increasing power.</p>
<ol><li><strong>Coefficients</strong> of logistic regression. A coefficient is the change in the log-odds per unit of the (scaled) feature; exp(coefficient) is an odds ratio.</li><li><strong>Permutation importance</strong>: shuffle one feature in the test set and see how much the score drops. Works for any model.</li><li><strong>Partial dependence</strong>: average prediction as one feature moves across its range, others fixed.</li></ol>
@@py
import sys
sys.path.insert(0, DATA)
import prep, mlprep
import numpy as np, pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.pipeline import make_pipeline
from sklearn.inspection import permutation_importance

o, c, p = prep.load_clean(DATA)
d = mlprep.late_frame(o)
train, test = d[d.order_date < "2024-10-01"], d[d.order_date >= "2024-10-01"]
F = mlprep.CAT + mlprep.NUM
pre = ColumnTransformer([("c", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), mlprep.CAT)], remainder="passthrough")
m = make_pipeline(pre, HistGradientBoostingClassifier(random_state=0)).fit(train[F], train.late)
r = permutation_importance(m, test[F], test.late, scoring="roc_auc", n_repeats=5, random_state=0)
imp = pd.Series(r.importances_mean, index=F).sort_values(ascending=False)
print("drop in test AUC when a feature is shuffled:")
print(imp.round(4).to_string())

# partial dependence by hand for the hour
base = test[F].copy()
curve = {}
for h in [8, 12, 15, 18, 20, 23]:
    x = base.copy(); x["order_hour"] = h; x["evening"] = int(18 <= h <= 21)
    curve[h] = round(float(m.predict_proba(x)[:, 1].mean()), 3)
print("average predicted P(late) if every order were placed at hour h:", curve)
@@
<p>The promised time dominates, then city, the evening flag and the basket size. Features near zero (or slightly negative, which is noise) add nothing. The partial dependence shows the evening bump: orders placed from 18 to 21 are predicted noticeably more likely to be late. This agrees with how the data was made and with what an operations lead would guess, which is the best sanity check an explanation can give. If an explanation says something absurd (a customer id matters most), look for leakage.</p>
<div class="callout green"><div class="lab">KEY IDEA</div><div class="txt">Importance says <em>what the model uses</em>, not what causes the outcome. "Hour matters to the model" does not prove that moving orders to another hour would reduce lateness. For causal claims go back to Chapter 5.</div></div>
<h3>Fairness check</h3>
<p>Compare error rates across groups the business cares about. Here, if the model systematically misses late orders in one city, that city's customers get worse service.</p>
@@py
import sys
sys.path.insert(0, DATA)
import prep, mlprep
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import make_pipeline

o, c, p = prep.load_clean(DATA)
d = mlprep.late_frame(o).dropna(subset=["city"])
train, test = d[d.order_date < "2024-10-01"], d[d.order_date >= "2024-10-01"].copy()
F = mlprep.CAT + mlprep.NUM
pre = ColumnTransformer([("c", OneHotEncoder(handle_unknown="ignore"), mlprep.CAT), ("n", StandardScaler(), mlprep.NUM)])
m = make_pipeline(pre, LogisticRegression(max_iter=1000)).fit(train[F], train.late)
test["flag"] = m.predict_proba(test[F])[:, 1] >= 0.11
g = test.groupby("city").apply(lambda x: pd.Series({"orders": len(x), "late_rate": x.late.mean(),
        "flagged": x.flag.mean(), "recall": (x.flag & (x.late == 1)).sum() / x.late.sum()}), include_groups=False)
g["orders"] = g.orders.astype(int)
print(g.round(3).to_string())
@@
<p>This table is a warning. At one pooled threshold the model catches about 90 percent of late orders in Bengaluru, Delhi and Mumbai but only about 17 percent in Pune. The reason is not malice: Pune has a lower base rate of lateness, so its late orders rarely reach a score of 0.11, and customers there get fewer rescue actions. Options: a city-specific threshold, a city-specific cost, or accepting the gap knowingly. Equal recall across groups and equal flag rates cannot generally be had at the same time; which definition of fairness matters is a policy decision to take with the business, but the check must be run before deployment, not after the complaints.</p>

<h2>6.7 An AutoML-style comparison table</h2>
<p>AutoML tools (Power BI's automated ML in dataflows, cloud services, <code>auto-sklearn</code>) try many models and settings and rank them on cross-validation. You can reproduce the idea in twenty lines: a loop over candidates with small parameter grids, scored by forward-chaining cross-validation on the training period, then one final score on the untouched test period. The important discipline: <strong>the test set picks nothing</strong>.</p>
@@py
import sys, time
sys.path.insert(0, DATA)
import prep, mlprep
import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.metrics import roc_auc_score

o, c, p = prep.load_clean(DATA)
d = mlprep.late_frame(o).sort_values("order_date")
train, test = d[d.order_date < "2024-10-01"], d[d.order_date >= "2024-10-01"]
F = mlprep.CAT + mlprep.NUM
pre = ColumnTransformer([("c", OneHotEncoder(handle_unknown="ignore"), mlprep.CAT), ("n", StandardScaler(), mlprep.NUM)])
cands = {
    "logreg C=0.1": LogisticRegression(C=0.1, max_iter=1000),
    "logreg C=1": LogisticRegression(C=1, max_iter=1000),
    "logreg C=10": LogisticRegression(C=10, max_iter=1000),
    "forest depth 6": RandomForestClassifier(200, max_depth=6, random_state=0, n_jobs=-1),
    "forest leaf 20": RandomForestClassifier(200, min_samples_leaf=20, random_state=0, n_jobs=-1),
    "boosting lr 0.05": HistGradientBoostingClassifier(learning_rate=0.05, max_iter=150, random_state=0),
    "boosting lr 0.1": HistGradientBoostingClassifier(learning_rate=0.1, max_iter=100, random_state=0),
}
rows = []
for name, est in cands.items():
    pipe = make_pipeline(pre, est)
    t = time.perf_counter()
    cv = cross_val_score(pipe, train[F], train.late, cv=TimeSeriesSplit(4), scoring="roc_auc")
    pipe.fit(train[F], train.late)
    rows.append((name, cv.mean(), cv.std(), roc_auc_score(test.late, pipe.predict_proba(test[F])[:, 1])))
tab = pd.DataFrame(rows, columns=["candidate", "cv_auc", "cv_std", "test_auc"]).sort_values("cv_auc", ascending=False)
print(tab.round(4).to_string(index=False))
print("best by CV:", tab.iloc[0].candidate)
@@
<p>Rank by <code>cv_auc</code>, never by <code>test_auc</code>. The differences among the top candidates are smaller than the fold-to-fold standard deviation, so the honest conclusion is "these models are tied; choose the simplest and fastest". An AutoML leaderboard always has a first place, but whether first is meaningfully better than fifth is something only the spread can tell you.</p>
@@table
Tool | How you would do this (not run here)
Excel | No native classifier. Logistic regression is possible with Solver (maximise the log-likelihood over coefficients) or the Analysis ToolPak for linear regression; for real ML export to Python or R
Power BI | Dataflows, AI insights, Automated ML (binary prediction) on a dataflow entity in Premium or Fabric workspaces; or the Python visual with scikit-learn
R | <code>glm(late ~ ., family = binomial)</code>; tidymodels or caret for forests and boosting (<code>ranger</code>, <code>xgboost</code>)
Cloud AutoML | Upload the table, pick the target, read the leaderboard; same discipline about splits applies
@@

<h2>6.8 Second target: predicting churn</h2>
<p>The same ideas apply when the unit is a customer. Define <strong>churn</strong> precisely (an experienced analyst spends half the project here): "Among customers who ordered in the 90 days before the cut-off date, those with no order in the 90 days after it." Features come from the past only: <em>recency</em> (days since last order), <em>frequency</em>, <em>monetary</em> value, average delivery time, return rate, segment and age. Train at one cut-off date and test at a later one, which is the production situation.</p>
@@py
import sys
sys.path.insert(0, DATA)
import prep
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score

o, c, p = prep.load_clean(DATA)

def build(cut):
    cut = pd.Timestamp(cut)
    past = o[o.order_date < cut]
    fut = o[(o.order_date >= cut) & (o.order_date < cut + pd.Timedelta(days=90))]
    g = past.groupby("customer_id")
    f = pd.DataFrame({"recency": (cut - g.order_date.max()).dt.days, "frequency": g.size(), "monetary": g.revenue.sum(),
                      "avg_delay": g.delivery_minutes.mean(),
                      "ret_rate": g.apply(lambda d: (d.status == "returned").mean(), include_groups=False),
                      "n90": past[past.order_date >= cut - pd.Timedelta(days=90)].groupby("customer_id").size()})
    f["n90"] = f.n90.fillna(0)
    f = f[f.n90 > 0].join(c.set_index("customer_id")[["segment", "age"]])
    f["avg_delay"] = f.avg_delay.fillna(f.avg_delay.median())
    f["age"] = f.age.fillna(f.age.median())
    f["premium"] = (f.segment == "Premium").astype(int)
    f["student"] = (f.segment == "Student").astype(int)
    f["churn"] = (~f.index.isin(fut.customer_id)).astype(int)
    return f.drop(columns="segment")

tr, te = build("2024-06-30"), build("2024-09-30")
X = [col for col in tr.columns if col != "churn"]
print("customers:", len(tr), "train churn rate:", round(tr.churn.mean(), 3), "| test:", len(te), round(te.churn.mean(), 3))
print("baseline rule (longer since last order = more churn) AUC:", round(roc_auc_score(te.churn, te.recency), 4))
for name, m in [("logistic regression", make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))),
                ("gradient boosting", HistGradientBoostingClassifier(random_state=0))]:
    m.fit(tr[X], tr.churn)
    print(f"{name:20s} test AUC:", round(roc_auc_score(te.churn, m.predict_proba(te[X])[:, 1]), 4))
@@
<p>Churn is harder: AUC is around 0.7 for the best model and only 0.58 for the recency rule. The signal is modest because in this synthetic world customers return largely at random, with higher activity customers more likely to return; real subscription data usually has stronger signals (usage drops, support tickets). Two further observations. The churn rate rose from about 23 percent at the first cut-off to 31 percent at the second, so the world drifted between training and test; this is exactly what Chapter 8 monitors. Before telling any story about which features matter, run the permutation importance of Section 6.6 on this model too.</p>
<div class="callout cream"><div class="lab">REAL JOB</div><div class="txt">In practice a churn model is judged by a campaign: score customers, offer a voucher to the top 10 percent, hold out a random group that gets nothing, and measure the difference. The holdout turns a prediction into a causal measurement, linking back to Chapter 5's experiments.</div></div>

<h2>6.9 Process, tools and what to hand over</h2>
<ol><li>Frame: unit, target, prediction time, decision, cost of errors.</li><li>Split by time before you look at the test data.</li><li>Build features known at prediction time; check each for leakage.</li><li>Fit a rule baseline, a simple model, then a flexible model.</li><li>Tune with cross-validation inside the training period.</li><li>Choose a threshold from costs on validation data.</li><li>Report once on the test period: ranking metric, precision and recall at the threshold, calibration, group checks.</li><li>Explain and document; save the model and the code (Chapter 8).</li></ol>
@@table
Task | pandas + scikit-learn | R | Power BI | Excel
Feature building | Full control | Full control | Power Query / DAX columns | Formulas
Fit and tune | Excellent | Excellent | Automated ML (limited) | Not suitable
Explain | Permutation, partial dependence, SHAP (if installed) | DALEX, iml | AI insights visuals | Not suitable
Deploy | Chapter 8 | plumber, vetiver | Score in dataflow | Not suitable
@@

<h2>Chapter recap</h2>
<ul><li>Frame the problem: unit, target, prediction time, decision, error costs.</li><li>Features must be known at prediction time; delivery minutes and status are leaks.</li><li>A too-good score (AUC 1.0) is a leakage alarm.</li><li>Validate on a later period; keep preprocessing inside the pipeline.</li><li>Beat a rule baseline first; here logistic regression, forest and boosting tie near AUC 0.84.</li><li>For rare events use PR-AUC, precision and recall; accuracy misleads.</li><li>Pick the threshold from costs on validation data, not 0.5.</li><li>Explain with coefficients, permutation importance and partial dependence; importance is not causation.</li><li>Check errors across groups before deployment.</li><li>Churn needs a precise definition and features from the past only; the world drifts.</li></ul>
@@table
Pattern | Meaning
ROC-AUC | Chance a random late order outranks a random on-time one
Precision = TP/(TP+FP); recall = TP/(TP+FN) | Right flags; caught share of events
Cost(t) = 5·flagged + 20·TP + 60·FN | Business cost at threshold t
Pipeline(preprocess, model) | Prevents preprocessing leakage
TimeSeriesSplit | Forward-chaining cross-validation
@@

<h2>Practice set</h2>
@@qa 6.10
Q: Why can you not use delivery_minutes to predict lateness at order time?
A: It is only known after the delivery and it defines the target; using it is target leakage (AUC becomes 1.0).
Q: Always predicting "on time" gets how much accuracy on the test period, and why is that useless?
A: About 86 percent (1 − 0.142), but it catches none of the late orders, which are the only thing we care about.
Q: Define precision and recall with the numbers TP = 30, FP = 70, FN = 20.
A: Precision = 30 ÷ 100 = 0.30; recall = 30 ÷ 50 = 0.60.
Q: With flag cost 5, late-and-acted cost 25 (5 + 20), late-and-missed cost 60, and P(late) = 0.12 for an order, should you act (assume calibrated)?
A: Expected cost if acting = 5 + 20 × 0.12 = 7.4. If not = 60 × 0.12 = 7.2. Slightly better not to act; break-even P = 5 ÷ 40 = 0.125.
Q: Why use a time split instead of a random split here?
A: In production the model predicts the future from the past; a random split lets it train on later rows, often giving optimistic scores.
Q: What does it mean that ROC-AUC is 0.84?
A: A random late order gets a higher score than a random on-time one 84 percent of the time.
Q: Why put the scaler inside the pipeline?
A: So it is fitted on training folds only; fitting on all data lets test statistics leak into training.
Q: Name three leakage types and give an example of each from this dataset.
A: Target leakage (delivery_minutes), temporal leakage (random split of time-ordered orders), group/history leakage (customer lateness averaged over all orders including the one being predicted).
Q: The best CV candidate is "logreg C=1" with cv_auc 0.842 and a standard deviation 0.01; the forest has 0.838. Which do you pick?
A: They are tied within noise; pick the simpler, faster, more interpretable logistic regression.
Q: Permutation importance says customer_id is the most important feature. What do you suspect?
A: Leakage or overfitting: an id is not causally meaningful; check how the model could memorise customers and whether history is computed using future rows.
Q: Why is churn defined with a window after a cut-off date rather than "customers who did not order recently"?
A: The label must be measured after the features' time; otherwise the same behaviour defines both, and there is no prediction.
Q: Interview style: "Your model has AUC 0.82 in validation and 0.71 in production. List five causes."
A: Leakage in validation; random instead of time split; data drift; different data pipeline in production (training-serving skew); label definition differs; feedback loop (the action changed the outcome).
@@

<h2>Prompt pack</h2>
@@prompt
You are my patient, practical professor. I am a working professional moving into data roles. Teach me to build a binary classifier for late deliveries: framing, features known at prediction time, leakage, time-based validation, logistic regression versus random forest versus gradient boosting, precision, recall and cost-based thresholds. Ask one question at a time and make me explain every choice.
@@
@@prompt
Act as a senior ML reviewer. I will paste my feature list, target definition, split strategy and metrics: [paste]. Look for target leakage, temporal leakage, group leakage, preprocessing leakage, inappropriate metrics for rare events and missing baselines. Rank problems by severity and tell me exactly how to fix each.
@@
@@prompt
Run a mock interview for a data scientist role. Ask me, one at a time, about class imbalance, ROC-AUC versus PR-AUC, how to choose a threshold, how to detect leakage, calibration and how to explain a gradient boosting model to a manager. Score my answers and end with a study list.
@@
