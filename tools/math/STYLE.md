# Style guide for the Math document (read fully before writing)

You are writing ONE chapter of "Mathematics for Data Science and AI: From Zero to Expert", a mini-textbook inside the
static site in `/Users/c2487352/Personal/Career/final/`. The reader is a working professional moving into data roles
(strong curiosity, school-level math only, wants to become truly proficient). The goal: someone who reads your chapter and
does the exercises can go from **beginner to expert on this topic**, and can explain it, compute it by hand, and code it.

## Output
Write ONLY the chapter body fragment to `tools/math/src/chNN.html` (NN = two digits). Do NOT include `<html>`, banner, table
of contents, pager or "mark as read" button: the builder adds them. Do NOT run `tools/build_doc.py` and do NOT edit any
file other than your own `src/chNN.html` and your own `figures/chNN_*.py` (other chapters are being written at the same
time, and the build script edits shared files). Figures: write self-contained matplotlib scripts
`tools/math/figures/chNN_<name>.py` that save `chNN_<name>.png` into the CURRENT directory, then generate them by running
`cd /Users/c2487352/Personal/Career/final/study/math/images && python3 -I ../../../tools/math/figures/chNN_<name>.py`
(create the images dir if needed). Use `matplotlib.use("Agg")`, dpi 110, figsize about (8,4.2), clear labels, readable fonts,
colour-blind-safe colours (#2b4fd6 blue, #b84a22 orange, #357a70 teal, #aa2d26 red, #6a2fd0 purple). 3 to 5 figures per chapter.
Reference them as `<figure><img src="images/chNN_name.png" alt="..." loading="lazy"/><figcaption>...</figcaption></figure>`
followed by a paragraph "How to read it: ...".

Validate with: `python3 -I tools/check_fragment.py tools/math/src/chNN.html --run` (from the `final/` folder). It checks tag
balance, required sections, counts, that every Python block runs, and that its printed output equals the output block shown
under it. Fix everything it reports.

## Length and depth
- 7,000 to 10,000 words of prose and code (check_fragment prints the count). Do not pad; every paragraph must teach.
- Structure: a story-style opening (2 to 3 paragraphs with a concrete real-life/data scenario that makes the reader NEED this math,
  then what they will be able to do after the chapter), then 5 to 8 numbered `<h2>` sections like `3.1 Title`, then these three
  final sections, exactly named: `<h2>Chapter recap</h2>`, `<h2>Practice set</h2>`, `<h2>Prompt pack</h2>`.
- Inside each concept section climb the ladder **Beginner → Intermediate → Expert**:
  1. Beginner: plain-English intuition (analogy), the smallest numeric example, by hand.
  2. Intermediate: the formal definition/formula, 3 or more worked examples of increasing difficulty with full steps and real numbers.
  3. Expert: the deeper idea (why it works, derivation or proof sketch, geometry, edge cases, numerical issues, how it appears in
     machine learning / deep learning / statistics / data engineering, what interviewers ask).
  Label expert material with `<h3>Going deeper</h3>` so a beginner knows it can be returned to.
- Every concept needs at least 3 different worked examples (different flavours: pure numbers, a data/ML story, a geometric or
  graphical picture, a "what if it goes wrong" case). Show every arithmetic step; do not skip lines.
- Always connect math to data work: where does this appear in pandas/NumPy, regression, PCA, neural nets, recommender systems, A/B tests...
- Verify with code: after the hand calculation, a Python/NumPy/SymPy-free (SymPy is NOT installed; use numpy, scipy, matplotlib, pandas only)
  snippet that reproduces the number. Plain names, comments, short.
- Teach the traps: at least 5 `callout red` "Common mistake" boxes in the chapter, with the wrong calculation and the right one.
- Be exact. Every number, derivation and code output must be correct. Recompute by hand AND by code. If unsure, do not state it.
- Plain, warm, direct voice ("you"), short sentences, define every symbol on first use, no jargon without a definition,
  no hand-waving ("it is easy to show"). Do not use em dashes; use commas, colons or full stops. No emojis in text.
- Do not repeat material from other documents; link to it instead, in plain text: "see the Statistics document, Chapter 3".
  Existing documents (folders in `study/`): python, sql, cs, analyst, stats, ds, ml, dl, genai, de, mlops, career.
  Statistics (hypothesis tests, regression inference, Bayesian, time series) is covered in `stats`; here only the math underneath.
- Make it correct for the intended audience: school algebra is the only assumed knowledge before Chapter 1, and each chapter may use
  only earlier chapters of THIS document (Chapter N may refer back to earlier chapters, and may point forward with "you will meet this in Chapter M").

## Chapter list (for cross references)
1 Numbers, Algebra and Equations; 2 Functions, Graphs and Modelling; 3 Exponents, Logarithms and Growth; 4 Sums, Sequences, Sets and
Counting; 5 Vectors and Geometry; 6 Matrices and Linear Transformations; 7 Linear Systems and Vector Spaces; 8 Eigenvalues,
Eigenvectors and Special Matrices; 9 SVD, PCA and Matrix Decompositions; 10 Limits and Derivatives; 11 Using Derivatives, Integrals
and Taylor Series; 12 Multivariable Calculus and Matrix Calculus; 13 The Chain Rule and Backpropagation; 14 Optimization: From Gradient
Descent to Adam; 15 Probability Mathematics and Information Theory; 16 Math Interview Bank, Pitfalls and a Study Plan; 17 Project Lab.

## HTML components (use exactly these class names; the CSS already exists)
Section: `<h2>3.2 Title</h2>`, sub-heading `<h3>Title</h3>`. Paragraphs `<p>`, lists `<ul><li>`, `<ol><li>`, inline `<code>`, `<strong>`, `<em>`,
`<sup>`, `<sub>`. ESCAPE `<`, `>` and `&` in text and code as `&lt;`, `&gt;`, `&amp;`.

Callouts (about 8 to 14 per chapter). Labels are short uppercase words:
```
<div class="callout blue"><div class="lab">INTUITION</div><div class="txt">...</div></div>
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt">...</div></div>
<div class="callout green"><div class="lab">KEY IDEA</div><div class="txt">...</div></div>
<div class="callout cream"><div class="lab">REAL JOB</div><div class="txt">...</div></div>
```
(other labels used: DEFINITION, REMEMBER, TRY IT, WHY IT MATTERS, INTERVIEW.)

Worked problem with steps table (the signature pattern of this site):
```
<p class="problem"><span class="pl">Problem 3.2.1</span> Statement with real numbers...</p>
<table class="steps"><tr><th>Formula</th><td>...</td></tr><tr><th>Plug in</th><td>...</td></tr><tr><th>Compute</th><td>...</td></tr><tr><th>Check</th><td>...</td></tr></table>
```
Number problems `Problem C.S.k` (chapter.section.index). Row headers can vary (Idea, Setup, Step 1, Step 2, Answer, Meaning).

Tables: `<div class="tablewrap"><table class="data"><thead><tr><th>..</th></tr></thead><tbody><tr><td>..</td></tr></tbody></table></div>`

Code (Python) then its real, pasted output:
```
<pre class="code lang-python"><code>import numpy as np
print(np.round(2/3, 4))</code></pre>
<pre class="code lang-text"><code>0.6667</code></pre>
```
Each Python block must be standalone (own imports) and deterministic (set seeds). Print only what you show.

Display equations and notation (use Unicode first: ×, ÷, ≤, ≥, ≠, ≈, ∞, ∑, ∏, √, ∫, ∂, ∇, ∈, ⊂, ∪, ∩, π, θ, λ, μ, σ, α, β, ε, ⁻¹, ᵀ, →, ⇒, ∀, ∃, ·):
```
<div class="eq">f(x) = x<sup>2</sup> + 3x − 5</div>
<div class="eq">slope = <span class="frac"><span>y<sub>2</sub> − y<sub>1</sub></span><span>x<sub>2</sub> − x<sub>1</sub></span></span></div>
<div class="eq">√ with overline: <span class="rad">x<sup>2</sup> + 1</span> (prefix with √)</div>
<div class="eq">A = <table class="mat"><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></table></div>
```
Use `.frac` for real fractions in display equations, `table.mat` for matrices/column vectors (a column vector is a mat with one column).
Inline simple fractions as a/b. Keep each `.eq` to one line of reasoning; use several for derivations, one step per line.

Practice set: at least 14 problems `<p class="problem"><span class="pl">Problem C.N.k</span> ...</p>` each followed directly by
`<p><strong>Answer:</strong> full worked answer with numbers</p>`; graded from easy (recall/by hand) to hard (expert, derive, code, find the bug),
mixing: arithmetic, conceptual "why", find-the-bug, what-does-this-code-print, and an interview-style question.
Chapter recap: `<ul>` of 8 to 12 bullets plus one `tablewrap/data` table "Formula / pattern | Meaning".
Prompt pack: exactly 3 of these (learn-with-quiz, review-my-work, mock interview), customised to the chapter topics:
```
<div class="prompt"><div class="ph"><span>✨ AI prompt: copy and paste into any AI</span><button type="button" class="copy">Copy</button></div><pre>You are my patient, practical professor. I am a working professional moving into data roles. ...</pre></div>
```

## Quality bar (self-check before finishing)
- Open `study/stats/ch03.html` and `study/stats/ch06.html` first to absorb the tone and layout, then exceed their explanatory clarity for beginners.
- Could a motivated beginner follow every step without outside help? Could an expert find real new insight in "Going deeper"?
- Each section answers: What is it? Why does it exist? How do I compute it by hand? How do I code it? Where does it show up in data/AI? What goes wrong?
- Final check: `check_fragment.py --run` prints OK; figures exist; no placeholder text; no unverified claims.
Reply with a 3-line summary (word count, sections, anything the editor should double-check).
