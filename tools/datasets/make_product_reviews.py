#!/usr/bin/env python3
"""product_reviews: reviews of a fictional Indian online marketplace, 2023-01 to 2025-03 (120 fictional products).

Text is built from templates + vocabulary + noise: English, Hinglish (Roman-script Hindi mixed with English), a little Devanagari Hindi,
SMS-speak, typos, emojis (some contradict the words), sarcasm, HTML entities, zero-width characters and mojibake.
Truth model: product quality q ~ N(0, 0.6) sets P(negative) = sigmoid(-1.55 - 1.1 q) (about 16 percent), P(neutral) = 11 percent, rest positive.
Stars given the sentiment: positive 5/4/3 = 68/27/5 percent, neutral 3/2/4 = 55/15/30, negative 1/2/3 = 58/30/12.
Planted problems: mis-clicked stars (4 percent), sarcasm (4 percent of reviews: positive words, negative meaning), fake-review bursts (6 percent, 25 reviewer
ids, 8 products, 5 stars, unverified), exact and cross-product duplicates, mojibake and HTML noise, stars stored as text for some rows, leakage-ish
columns (seller_replied, helpful_votes), quality drop on 6 products from 2024-06-01 (drift), noisy human sentiment labels on a subset.
"""
import csv
from pathlib import Path
import numpy as np
import pandas as pd

ID = "product_reviews"
SEED = 20250310
CATS = {"Mobiles & Audio": ["earphones", "phone", "power bank", "speaker", "charger"], "Appliances": ["mixer grinder", "iron", "kettle", "air fryer"],
        "Fashion": ["kurta", "jeans", "sneakers", "saree"], "Grocery": ["masala", "tea", "dal", "atta"], "Books": ["book", "notebook"],
        "Beauty": ["face wash", "serum", "shampoo"]}
BR = ["Boltix", "Zenova", "Kaveri Home", "Annapurna Fresh", "Urban Loom", "Pixelio", "Veda Care", "Chaiwala", "Nimbus", "Tarang"]
POS_EN = ["Excellent {n}, totally worth the price.", "Very good quality {n}. Delivery was on time and packaging was nice.", "Loved it! The {n} works perfectly. Highly recommended.",
          "Good {n} for the price, quality is great."]
POS_HI = ["Bahut accha {n}, paisa vasool!", "{n} ki quality zabardast hai, delivery bhi time pe aayi.", "Mast product hai, sab ko recommend karunga.", "Ekdum badhiya {n}, value for money."]
NEU_EN = ["Average {n}, nothing special. Does the job.", "{n} is okay for the price, but packaging could be better."]
NEU_HI = ["Theek-thaak {n} hai, na accha na bura.", "{n} chalega, par quality aur achhi ho sakti thi."]
NEG_EN = ["Worst {n}. Stopped working after two days. Waste of money.", "Very poor quality {n}, do not buy.", "Received a damaged {n} and the refund process is a headache."]
NEG_HI = ["Bekar {n}, paisa barbaad. Mat kharido.", "Quality ghatiya hai, 2 din me kharab ho gaya.", "{n} toota hua mila, return bhi nahi ho raha."]
SARC_EN = ["Wow, great {n}. Stopped working in 2 days. Thanks a lot!", "Amazing quality, it broke on day one. Just what I wanted.", "Superb delivery, only took 3 weeks. Great job."]
SARC_HI = ["Waah, kya {n} hai, 2 din me kharab. Bahut badhiya!", "Zabardast quality, pehle hi din toot gaya. Shukriya."]
DEV = {"pos": "बहुत बढ़िया प्रोडक्ट, पैसा वसूल!", "neu": "ठीक-ठाक है, कुछ खास नहीं।", "neg": "बेकार प्रोडक्ट, पैसे बर्बाद हो गए। मत खरीदो।"}
FAKE = ["Nice product good quality", "Very good product, must buy", "Super product awesome quality", "Best product ever, value for money", "Good quality fast delivery",
        "Excellent product, highly recommended", "Superb quality nice packing", "Amazing product, worth every rupee"]
EXTRA = ["Delivery was late due to the rain.", "Bought during the Diwali sale.", "Packaging was damaged.", "Courier partner DelhiGo was prompt.", "Size is a bit tight."]
EMO = {"pos": ["\U0001F44D", "\U0001F60D", "\U0001F525", "\U0001F64F"], "neg": ["\U0001F621", "\U0001F44E", "\U0001F624"], "neu": ["\U0001F610", "\U0001F642"]}
SMSW = [("good", "gud"), ("awesome", "awsm"), ("nice", "nyc"), ("great", "gr8"), ("very", "vry"), ("quality", "qlty")]


def sig(x):
    return 1 / (1 + np.exp(-x))


def _text(s, n, style, sarcasm, rng):
    if style == "dev":
        t = DEV[s]
    elif sarcasm:
        t = (SARC_HI if style == "hi" else SARC_EN)[rng.integers(2 if style == "hi" else 3)]
    else:
        t = {"pos": (POS_HI if style == "hi" else POS_EN), "neu": (NEU_HI if style == "hi" else NEU_EN), "neg": (NEG_HI if style == "hi" else NEG_EN)}[s]
        t = t[rng.integers(len(t))]
    t = t.format(n=n)
    if style == "sms":
        for a, b in SMSW:
            t = t.replace(a, b).replace(a.capitalize(), b)
    if style != "dev" and rng.random() < 0.25:
        t += " " + EXTRA[rng.integers(len(EXTRA))]
    if rng.random() < 0.12 and style != "dev":
        w = t.split(" ")
        i = rng.integers(len(w))
        if len(w[i]) > 3:
            j = rng.integers(len(w[i]) - 1); w[i] = w[i][:j] + w[i][j + 1] + w[i][j] + w[i][j + 2:]
        t = " ".join(w)
    if rng.random() < 0.18:
        e = EMO["neg" if sarcasm else s]
        t += " " + e[rng.integers(len(e))]
    if sarcasm and rng.random() < 0.3:
        t += " \U0001F602\U0001F44D"
    if rng.random() < 0.03:
        t = t.replace("&", "&amp;").replace("'", "&#39;") + " &amp;"
    if rng.random() < 0.03:
        t = t.replace(". ", ".\n", 1)
    if rng.random() < 0.01:
        t = t[: len(t) // 2] + "​" + t[len(t) // 2:]
    return t


def generate():
    rng = np.random.default_rng(SEED)
    P = 120
    pcat = rng.choice(list(CATS), P)
    pq = rng.normal(0, 0.6, P)
    prod = pd.DataFrame({"product_id": ["PR-%04d" % (1000 + i) for i in range(P)],
                         "name": [f"{BR[rng.integers(len(BR))]} {CATS[c][rng.integers(len(CATS[c]))].title()}" for c in pcat], "category": pcat,
                         "price_inr": np.round(np.exp(rng.normal(6.6, 1.0, P)), -1).astype(int), "launch_date": (pd.Timestamp("2022-06-01") + pd.to_timedelta(rng.integers(0, 600, P), unit="D")).strftime("%Y-%m-%d"),
                         "seller_id": ["S-%03d" % rng.integers(1, 40) for _ in range(P)]})
    drop_p = set(rng.choice(P, 6, replace=False).tolist())
    fake_p = set(rng.choice(P, 8, replace=False).tolist())
    N0 = 4300
    start = pd.Timestamp("2023-01-01"); span = (pd.Timestamp("2025-03-31") - start).days
    pw = np.exp(rng.normal(0, 0.8, P)); pw /= pw.sum()
    pi = rng.choice(P, N0, p=pw)
    day = rng.integers(0, span + 1, N0)
    q = pq[pi] - 1.0 * (np.isin(pi, list(drop_p)) & (day >= 517 + 0))
    pneg = sig(-1.55 - 1.1 * q)
    u = rng.random(N0)
    s = np.where(u < pneg, "neg", np.where(u < pneg + 0.11, "neu", "pos")).astype(object)
    sarc = (rng.random(N0) < 0.04) & (s == "pos")
    s = np.where(sarc, "neg", s)
    st = np.zeros(N0, dtype=int)
    for k, (lbl, vals, pr) in enumerate([("pos", [5, 4, 3], [.68, .27, .05]), ("neu", [3, 2, 4], [.55, .15, .30]), ("neg", [1, 2, 3], [.58, .30, .12])]):
        m = s == lbl
        st[m] = rng.choice(vals, m.sum(), p=pr)
    mis = (rng.random(N0) < 0.04) & ~sarc
    st = np.where(mis & (s == "neg"), 5, np.where(mis & (s == "pos"), 1, st))
    style = rng.choice(["en", "hi", "dev", "sms"], N0, p=[.56, .28, .04, .12])
    txt = [_text(s[i], CATS[pcat[pi[i]]][rng.integers(len(CATS[pcat[pi[i]]]))], style[i], bool(sarc[i]), rng) for i in range(N0)]
    ttl = [t.split(".")[0].split("!")[0][:40] for t in txt]
    rev = rng.integers(0, 3200, N0)
    ver = rng.random(N0) < 0.78
    dev = rng.choice(["app", "web"], N0, p=[.7, .3])
    d_order = np.clip(rng.gamma(2.0, 4.0, N0), 1, 60).round().astype(int)
    hv = np.where(s == "neg", rng.poisson(3.0, N0), rng.poisson(1.0, N0))
    sr = rng.random(N0) < np.where(s == "neg", 0.55, 0.03)
    rows = dict(pi=pi.tolist(), day=day.tolist(), st=st.tolist(), txt=txt, ttl=ttl, rev=rev.tolist(), ver=ver.tolist(), dev=dev.tolist(), do=d_order.tolist(),
                hv=hv.tolist(), sr=sr.tolist(), s=s.tolist(), sarc=sarc.tolist(), mis=mis.tolist(), fake=[False] * N0)
    # fake bursts
    nf = int(0.06 * N0); fp = sorted(fake_p); fr = rng.integers(5000, 5025, nf); bursts = rng.choice(span - 3, 3, replace=False)
    for j in range(nf):
        b = int(bursts[j % 3] + rng.integers(0, 3))
        t = FAKE[rng.integers(8)] + ("!" if rng.random() < 0.3 else "")
        for k, v in dict(pi=fp[rng.integers(len(fp))], day=b, st=5, txt=t, ttl=t[:30], rev=int(fr[j]), ver=False, dev="app", do=int(rng.integers(1, 3)), hv=0, sr=False, s="pos",
                         sarc=False, mis=False, fake=True).items():
            rows[k].append(v)
    N = len(rows["pi"])
    df = pd.DataFrame(rows)
    # duplicates: exact repeats and pasted-across-products
    ex = df.sample(frac=0.015, random_state=5)
    pas = df[~df.fake].sample(frac=0.01, random_state=6).copy()
    pas["pi"] = rng.integers(0, P, len(pas)); pas["rev"] = rng.integers(0, 3200, len(pas)); pas["day"] = np.minimum(pas["day"] + rng.integers(1, 60, len(pas)), span)
    pas["ver"] = False
    df = pd.concat([df, ex, pas], ignore_index=True).sort_values("day", kind="stable").reset_index(drop=True)
    N = len(df)
    # presentation mess
    dt = pd.Timestamp("2023-01-01") + pd.to_timedelta(df["day"].values, unit="D")
    f = rng.choice(4, N, p=[.55, .20, .15, .10])
    dstr = [t.strftime("%Y-%m-%d") if k == 0 else t.strftime("%d/%m/%Y") if k == 1 else t.strftime("%b %d, %Y") if k == 2 else t.strftime("%d-%m-%y") for t, k in zip(dt, f)]
    txt2 = df["txt"].tolist()
    for i in np.where(rng.random(N) < 0.015)[0]:
        if any(ord(ch) > 127 for ch in txt2[i]):
            txt2[i] = txt2[i].encode("utf-8").decode("latin-1")
    stars = df["st"].astype(object).tolist()
    for i in np.where(rng.random(N) < 0.02)[0]:
        stars[i] = f"{stars[i]} stars"
    hvt = [f"{h} people found this helpful" if rng.random() < 0.25 else h for h in df["hv"]]
    vp = np.where(rng.random(N) < 0.5, np.where(df["ver"].values, "Y", "N"), np.where(df["ver"].values, "True", "False"))
    lab_idx = rng.random(N) < 0.30
    true_lab = df["s"].values.astype(object)
    flip = rng.random(N) < 0.06
    other = {"pos": "neu", "neu": "neg", "neg": "pos"}
    lab = np.array([other[x] if fl else x for x, fl in zip(true_lab, flip)], dtype=object)
    lab = np.where(lab_idx, lab, None)
    rv = pd.DataFrame({"review_id": ["R-%06d" % (200000 + 3 * i + rng.integers(0, 3)) for i in range(N)], "product_id": prod["product_id"].values[df["pi"].values],
                       "reviewer_id": ["U-%05d" % (10000 + r) for r in df["rev"]], "review_date": dstr, "rating": stars, "title": df["ttl"].values, "review_text": txt2,
                       "verified_purchase": vp, "helpful_votes": hvt, "device": df["dev"].values, "seller_replied": np.where(df["sr"].values, "Y", "N"),
                       "order_to_review_days": df["do"].values, "sentiment_label": lab})
    ids = rv["review_id"].tolist()
    truth = dict(n=N, mis_click_rate=0.04, sarcasm_rate=0.04, fake_rate=0.06, n_fake=int(df["fake"].sum()), fake_reviewer_ids=["U-%05d" % (10000 + r) for r in range(5000, 5025)],
                 fake_products=[prod["product_id"][i] for i in sorted(fake_p)], drop_products=[prod["product_id"][i] for i in sorted(drop_p)], drop_date="2024-06-01",
                 n_exact_repeats=int(len(ex)), n_pasted_across_products=int(len(pas)), annotator_noise=0.06, label_share=0.30, mojibake_rate=0.015,
                 true_sentiment=dict(zip(ids, true_lab.tolist())), is_fake=dict(zip(ids, df["fake"].tolist())), is_sarcasm=dict(zip(ids, df["sarc"].tolist())),
                 is_misclick=dict(zip(ids, df["mis"].tolist())), style=dict(zip(ids, [None] * 0)))
    return {"reviews": rv, "products": prod}, truth


def write(outdir):
    tables, _ = generate()
    outdir = Path(outdir)
    (outdir / ID).mkdir(parents=True, exist_ok=True)
    sizes = {}
    for name, df in tables.items():
        p = outdir / ID / f"{name}.csv"
        df.to_csv(p, index=False, lineterminator="\n", encoding="utf-8", quoting=csv.QUOTE_NONNUMERIC)
        sizes[f"{ID}/{name}.csv"] = p.stat().st_size
    return sizes


def main():
    root = Path(__file__).resolve().parents[2]
    tables, truth = generate()
    sizes = write(root / "data")
    for k, v in tables.items():
        print(f"{k}: {len(v)} rows x {len(v.columns)} cols")
    print("bytes:", sizes, {k: truth[k] for k in ["n_fake", "n_exact_repeats", "n_pasted_across_products"]})


if __name__ == "__main__":
    main()
