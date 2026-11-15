#!/usr/bin/env python3
"""Generator for data/ecom_store/*.csv and data/ecom_store/ecom_store.db  (SPOILERS inside).

A fictional mid-size Indian online store, 2023-01-01 to 2024-12-31. Tables: customers, products, orders, order_items, returns, events.
Planted problems: duplicated customers after an app migration, IST/UTC timestamp switch on 2024-03-01, a Simpson's paradox in the
events table (device vs traffic source), money stored as text and paise-as-rupees, orphan keys, MNAR delivery ratings.
Deterministic: fixed seed, numpy + pandas + sqlite3 only. Run: python3 tools/datasets/make_ecom_store.py [--out DIR]
"""
import argparse
import hashlib
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20241231
N_CUST, N_PROD, N_ORD, N_SESS = 2600, 220, 6000, 3000
D0, D1 = pd.Timestamp("2023-01-01"), pd.Timestamp("2024-12-31")
MIGRATION = pd.Timestamp("2024-03-01")               # from this IST midnight, new orders are written in UTC with a Z suffix
FEST = {"2023-11-12": 1.9, "2024-11-01": 2.0}        # Diwali (verified dates): demand multiplier on the day, ramping up over the week before
SALE_WEEKS = [("2023-10-15", "2023-10-21", 1.7), ("2024-10-04", "2024-10-10", 1.8)]   # invented 'Mega Saver Days'
CATS = {"Electronics": (4200, 0.9, 0.05), "Fashion": (900, 0.6, 0.16), "Home & Kitchen": (1100, 0.7, 0.06), "Beauty": (450, 0.5, 0.04), "Grocery & Staples": (260, 0.4, 0.01)}
CAT_P = [0.22, 0.30, 0.20, 0.16, 0.12]
BRANDS = ["Aarav", "Kisan Fresh", "Urban Loom", "VoltEdge", "Glowvya", "HomeNest", "Zenta", "Desi Pantry", "Pixelon", "Rangoli", "Bharat Basics", "NovaWear"]
CITIES = [("Mumbai", "Maharashtra", "4000"), ("Delhi", "Delhi", "1100"), ("Bengaluru", "Karnataka", "5600"), ("Hyderabad", "Telangana", "5000"),
          ("Chennai", "Tamil Nadu", "6000"), ("Kolkata", "West Bengal", "7000"), ("Pune", "Maharashtra", "4110"), ("Ahmedabad", "Gujarat", "3800"),
          ("Jaipur", "Rajasthan", "3020"), ("Lucknow", "Uttar Pradesh", "2260"), ("Patna", "Bihar", "8000"), ("Indore", "Madhya Pradesh", "4520"),
          ("Kochi", "Kerala", "6820"), ("Nagpur", "Maharashtra", "4400"), ("Guwahati", "Assam", "7810")]
CITY_P = np.array([0.15, 0.14, 0.13, 0.08, 0.08, 0.07, 0.07, 0.05, 0.04, 0.04, 0.03, 0.03, 0.03, 0.03, 0.03])
TIER1 = {"Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Pune"}
PAY = ["UPI", "COD", "Credit Card", "Debit Card", "Net Banking", "Wallet", "EMI"]
PAY_P = [0.38, 0.27, 0.12, 0.08, 0.06, 0.05, 0.04]
SOURCES = ["organic_search", "direct", "email", "paid_social"]
P_SRC = {"mobile": [0.25, 0.12, 0.08, 0.55], "desktop": [0.45, 0.30, 0.17, 0.08]}
CONV = {"organic_search": 0.06, "direct": 0.09, "email": 0.12, "paid_social": 0.015}    # session to purchase, desktop
MOBILE_MULT = 1.25                                                                   # mobile converts BETTER inside every source
SCHEMA = """
CREATE TABLE customers (customer_id TEXT PRIMARY KEY, email_hash TEXT, signup_ts TEXT, city TEXT, state TEXT, pincode TEXT, acquisition_channel TEXT, birth_year INTEGER, gender TEXT, loyalty_tier TEXT);
CREATE TABLE products (product_id INTEGER PRIMARY KEY, sku TEXT, product_name TEXT, category TEXT, brand TEXT, mrp INTEGER, cost_price REAL, gst_rate INTEGER, launch_date TEXT, is_active INTEGER);
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id TEXT REFERENCES customers(customer_id), order_ts TEXT, status TEXT, payment_method TEXT, ship_city TEXT, coupon_code TEXT, order_total TEXT, shipping_fee REAL, delivered_date TEXT, delivery_rating INTEGER);
CREATE TABLE order_items (order_item_id INTEGER PRIMARY KEY, order_id INTEGER REFERENCES orders(order_id), product_id INTEGER REFERENCES products(product_id), quantity INTEGER, unit_price REAL, discount_pct INTEGER, gst_amount REAL, line_total REAL);
CREATE TABLE returns (return_id INTEGER PRIMARY KEY, order_item_id INTEGER REFERENCES order_items(order_item_id), return_ts TEXT, reason TEXT, refund_amount REAL);
CREATE TABLE events (event_id INTEGER PRIMARY KEY, session_id TEXT, customer_id TEXT, event_ts TEXT, event_type TEXT, product_id INTEGER, device TEXT, traffic_source TEXT);
CREATE INDEX ix_orders_cust ON orders(customer_id);
CREATE INDEX ix_items_order ON order_items(order_id);
CREATE INDEX ix_events_session ON events(session_id);
"""


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def ts_ist(t):
    return f"{t.year:04d}-{t.month:02d}-{t.day:02d} {t.hour:02d}:{t.minute:02d}:{t.second:02d}+05:30"


def ts_utc(t):
    u = t - pd.Timedelta(hours=5, minutes=30)
    return f"{u.year:04d}-{u.month:02d}-{u.day:02d}T{u.hour:02d}:{u.minute:02d}:{u.second:02d}Z"


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    # ---------------- products
    cat = rng.choice(list(CATS), size=N_PROD, p=CAT_P)
    mrp = np.array([int(round(np.exp(rng.normal(np.log(CATS[c][0]), CATS[c][1])) / 10) * 10) for c in cat]); mrp = np.maximum(mrp, 49)
    gst = np.array([{"Electronics": 18, "Fashion": 12, "Home & Kitchen": 18, "Beauty": 18, "Grocery & Staples": 5}[c] for c in cat])
    gst = np.where((cat == "Fashion") & (mrp > 1000), 12, gst)
    brand = rng.choice(BRANDS, size=N_PROD).astype(object); brand[rng.random(N_PROD) < 0.04] = ""
    launch = D0 - pd.to_timedelta(rng.integers(0, 700, N_PROD), unit="D")
    products = pd.DataFrame({"product_id": 3001 + np.arange(N_PROD), "sku": [f"SKU-{c[:3].upper()}-{i:04d}" for i, c in enumerate(cat)],
                             "product_name": [f"{b or 'Generic'} {c.split()[0]} item {i}" for i, (b, c) in enumerate(zip(brand, cat))],
                             "category": cat, "brand": brand, "mrp": mrp, "cost_price": np.round(mrp * rng.uniform(0.55, 0.85, N_PROD), 2),
                             "gst_rate": gst, "launch_date": [f"{t.year:04d}-{t.month:02d}-{t.day:02d}" for t in launch],
                             "is_active": (rng.random(N_PROD) < 0.93).astype(int)})
    # ---------------- customers
    sign_day = np.sort(np.minimum((rng.beta(1.3, 1.0, N_CUST) * 760).astype(int), 729))
    signup = D0 + pd.to_timedelta(sign_day, unit="D") + pd.to_timedelta(rng.integers(0, 86400, N_CUST), unit="s")
    ci = rng.choice(len(CITIES), size=N_CUST, p=CITY_P)
    chan = rng.choice(["Organic", "Paid social", "Google ads", "Referral", "Email"], size=N_CUST, p=[0.30, 0.25, 0.22, 0.13, 0.10])
    byear = rng.integers(1965, 2006, N_CUST).astype(float)
    cust_id = np.array([f"C{100000 + 3 * i + int(rng.integers(0, 3))}" for i in range(N_CUST)], dtype=object)
    email_hash = np.array([f"{int(x):012x}" for x in rng.integers(1 << 40, 1 << 47, N_CUST)], dtype=object)
    gender = rng.choice(["Female", "Male"], size=N_CUST, p=[0.46, 0.54]).astype(object)
    # ---------------- orders: date intensity with growth, weekday, festivals, sale weeks
    days = pd.date_range(D0, D1)
    lam = (1 + 0.9 * np.arange(len(days)) / len(days)) * np.array([0.95, 0.93, 0.95, 0.98, 1.05, 1.15, 1.10])[days.dayofweek]
    for d, m in FEST.items():
        i = int((pd.Timestamp(d) - D0).days)
        for k in range(8):
            if i - k >= 0:
                lam[i - k] *= 1 + (m - 1) * (1 - k / 8)
    for a, b, m in SALE_WEEKS:
        lam[(days >= pd.Timestamp(a)) & (days <= pd.Timestamp(b))] *= m
    day_i = rng.choice(len(days), size=N_ORD, p=lam / lam.sum())
    hw = np.array([1, 0.6, 0.4, 0.3, 0.3, 0.5, 1, 2, 3, 4, 4.5, 5, 5.5, 5.5, 5, 5, 5, 5.5, 6, 7, 8, 8.5, 7, 3], dtype=float)
    hour = rng.choice(24, size=N_ORD, p=hw / hw.sum())
    ots = days[day_i] + pd.to_timedelta(hour * 3600 + rng.integers(0, 3600, N_ORD), unit="s")
    ots = ots.sort_values()
    # customer for each order: only customers who already signed up, heavy-tailed activity
    w = rng.gamma(0.6, 2.0, N_CUST)
    cidx = np.empty(N_ORD, dtype=int)
    for j, t in enumerate(ots):
        k = int(np.searchsorted(signup.values, np.datetime64(t), side="right"))
        k = max(k, 5)
        p = w[:k] / w[:k].sum()
        cidx[j] = rng.choice(k, p=p)
    pay = rng.choice(PAY, size=N_ORD, p=PAY_P)
    ship_i = np.where(rng.random(N_ORD) < 0.8, ci[cidx], rng.choice(len(CITIES), size=N_ORD, p=CITY_P))
    cod = pay == "COD"
    r = rng.random(N_ORD)
    status = np.where(r < np.where(cod, 0.11, 0.04), "cancelled", np.where(r < np.where(cod, 0.11, 0.04) + np.where(cod, 0.06, 0.0), "rto", "delivered"))
    coupon = np.where(rng.random(N_ORD) < 0.22, rng.choice(["WELCOME10", "FESTIVE15", "SAVE200", "APPONLY5"], size=N_ORD), "")
    order_id = 700001 + np.arange(N_ORD) * 2
    # ---------------- items
    n_items = np.minimum(1 + rng.poisson(0.75, N_ORD), 5)
    rows = []
    sale = np.zeros(N_ORD, dtype=bool)
    for a, b, m in SALE_WEEKS:
        sale |= (ots >= pd.Timestamp(a)) & (ots < pd.Timestamp(b) + pd.Timedelta(days=1))
    oi_id = 9000001
    for j in range(N_ORD):
        for _ in range(int(n_items[j])):
            pidx = int(rng.integers(0, N_PROD))
            disc = int(rng.choice([0, 10, 15, 20, 30], p=[0.45, 0.2, 0.15, 0.12, 0.08])) + (10 if sale[j] else 0)
            qty = 1 + int(rng.random() < 0.18) + int(rng.random() < 0.05)
            price = round(mrp[pidx] * (1 - disc / 100), 2)
            rows.append([oi_id, order_id[j], int(products.product_id[pidx]), qty, price, disc, j, pidx])
            oi_id += 1
    items = pd.DataFrame(rows, columns=["order_item_id", "order_id", "product_id", "quantity", "unit_price", "discount_pct", "j", "pidx"])
    items["line_total"] = np.round(items.unit_price * items.quantity, 2)
    items["gst_amount"] = np.round(items.line_total * gst[items.pidx] / (100 + gst[items.pidx]), 2)
    sub = items.groupby("j").line_total.sum().reindex(range(N_ORD)).to_numpy()
    ship_fee = np.where(sub >= 499, 0.0, 49.0)
    order_total = np.round(sub + ship_fee, 2)
    # ---------------- returns (delivered orders only): category, discount and a little noise
    ret_rows = []
    rid = 50001
    for x in items.itertuples():
        if status[x.j] != "delivered":
            continue
        base = CATS[cat[x.pidx]][2]
        p = sigmoid(np.log(base / (1 - base)) + 0.01 * x.discount_pct + (0.25 if cod[x.j] else 0.0))
        if rng.random() < p:
            ret_rows.append([rid, x.order_item_id, x.j, str(rng.choice(["Size/fit issue", "Damaged on arrival", "Not as described", "Changed mind", "Wrong item"], p=[0.3, 0.2, 0.2, 0.2, 0.1])), x.line_total])
            rid += 1
    returns = pd.DataFrame(ret_rows, columns=["return_id", "order_item_id", "j", "reason", "refund_amount"])
    returned_order = set(returns.j.tolist())
    status = np.where((status == "delivered") & np.isin(np.arange(N_ORD), list(returned_order)), "returned", status)
    # delivery date and MNAR rating
    tier1 = np.array([CITIES[i][0] in TIER1 for i in ship_i])
    lead = rng.integers(2, 5, N_ORD) + np.where(tier1, 0, rng.integers(1, 4, N_ORD))
    delivered_ok = np.isin(status, ["delivered", "returned"])
    true_rating = np.clip(np.round(rng.normal(4.0 - 0.35 * (lead - 3) - 0.9 * np.isin(status, ["returned"]), 0.9)), 1, 5)
    seen = rng.random(N_ORD) < np.where(np.isin(true_rating, [1, 2, 5]), 0.75, 0.22)
    rating = np.where(delivered_ok & seen, true_rating, np.nan)

    # ---------------- observed tables with messiness
    cust_obs = cust_id.copy()
    # duplicates after migration: 80 people get a second row with a new id format and the same email_hash
    dup_i = rng.choice(N_CUST, size=80, replace=False)
    dup_ids = np.array([f"U-{500000 + 11 * k}" for k in range(80)], dtype=object)
    cust_for_order = cust_obs[cidx].copy()
    moved = 0
    for k, i in enumerate(dup_i):
        m = np.flatnonzero(cidx == i)
        sel = m[rng.random(len(m)) < 0.45]
        cust_for_order[sel] = dup_ids[k]; moved += len(sel)
    order_ts_txt = np.array([ts_ist(t) if t < MIGRATION else ts_utc(t) for t in ots], dtype=object)
    odd = rng.random(N_ORD) < 0.012
    order_ts_txt[odd] = [f"{t.day:02d}/{t.month:02d}/{t.year:04d} {t.hour:02d}:{t.minute:02d}" for t in ots[odd]]   # a few manual entries
    stat_txt = status.astype(object)
    for i in np.flatnonzero(rng.random(N_ORD) < 0.04):
        stat_txt[i] = stat_txt[i].capitalize() if rng.random() < 0.5 else stat_txt[i].upper()
    tot_txt = np.array([f"{v:.2f}" for v in order_total], dtype=object)
    for i in np.flatnonzero(rng.random(N_ORD) < 0.07):
        tot_txt[i] = f"₹{order_total[i]:,.2f}"
    deliv = np.array([("" if not delivered_ok[j] else (ots[j] + pd.Timedelta(days=int(lead[j]))).strftime("%Y-%m-%d")) for j in range(N_ORD)], dtype=object)
    orders = pd.DataFrame({"order_id": order_id, "customer_id": cust_for_order, "order_ts": order_ts_txt, "status": stat_txt, "payment_method": pay,
                           "ship_city": [CITIES[i][0] for i in ship_i], "coupon_code": coupon, "order_total": tot_txt, "shipping_fee": ship_fee,
                           "delivered_date": deliv, "delivery_rating": rating})
    # customers: second rows for duplicates, MAR missing birth_year (more for COD-heavy customers), MCAR gender blanks
    cod_share = pd.Series(cod).groupby(cidx).mean().reindex(range(N_CUST)).fillna(0).to_numpy()
    byear[rng.random(N_CUST) < 0.05 + 0.25 * cod_share] = np.nan
    gender[rng.random(N_CUST) < 0.03] = ""
    st = signup
    sg = np.array([ts_ist(t) if t < MIGRATION else ts_utc(t) for t in st], dtype=object)
    tier = np.where(rng.random(N_CUST) < 0.7, "Basic", np.where(rng.random(N_CUST) < 0.75, "Silver", "Gold"))
    customers = pd.DataFrame({"customer_id": cust_obs, "email_hash": email_hash, "signup_ts": sg, "city": [CITIES[i][0] for i in ci],
                              "state": [CITIES[i][1] for i in ci], "pincode": [CITIES[i][2] + f"{int(rng.integers(0, 100)):02d}" for i in ci],
                              "acquisition_channel": chan, "birth_year": byear, "gender": gender, "loyalty_tier": tier})
    d = customers.iloc[dup_i].copy(); d["customer_id"] = dup_ids
    d["signup_ts"] = [ts_utc(t + pd.Timedelta(days=int(rng.integers(200, 400)))) if True else "" for t in signup[dup_i]]
    customers = pd.concat([customers, d], ignore_index=True)
    # items: legacy paise batch, orphan products, odd quantities
    it = items[["order_item_id", "order_id", "product_id", "quantity", "unit_price", "discount_pct", "gst_amount", "line_total"]].copy()
    paise = rng.random(len(it)) < 0.015
    it.loc[paise, "unit_price"] = it.loc[paise, "unit_price"] * 100
    orphan = rng.choice(len(it), size=25, replace=False)
    it.loc[it.index[orphan], "product_id"] = 9999
    q = rng.choice(np.flatnonzero(it.quantity.to_numpy() >= 1), size=12, replace=False)
    it.loc[it.index[q[:6]], "quantity"] = 0; it.loc[it.index[q[6:]], "quantity"] = -1
    # returns table: timestamp text, a few orphans
    rt = ots[returns.j.to_numpy()] + pd.to_timedelta(rng.integers(3, 20, len(returns)), unit="D")
    ret = pd.DataFrame({"return_id": returns.return_id, "order_item_id": returns.order_item_id,
                        "return_ts": [f"{t.year:04d}-{t.month:02d}-{t.day:02d} {t.hour:02d}:{t.minute:02d}:{t.second:02d}" for t in rt],
                        "reason": returns.reason, "refund_amount": returns.refund_amount})
    ret.loc[ret.index[rng.choice(len(ret), size=8, replace=False)], "order_item_id"] = 99999999
    # events: sampled sessions of visitors who reached a product page. NOT linked to orders on purpose.
    dev = rng.choice(["mobile", "desktop"], size=N_SESS, p=[0.68, 0.32])
    src = np.array([rng.choice(SOURCES, p=P_SRC[d_]) for d_ in dev], dtype=object)
    p_buy = np.array([CONV[s] * (MOBILE_MULT if d_ == "mobile" else 1.0) for s, d_ in zip(src, dev)])
    a_atc = np.clip(p_buy / (0.85 * 0.6 * 0.7), 0, 0.95)
    sday = rng.choice(len(days), size=N_SESS, p=lam / lam.sum())
    sts = days[sday] + pd.to_timedelta(rng.integers(0, 86400, N_SESS), unit="s")
    sess_cust = np.where(rng.random(N_SESS) < 0.55, cust_obs[rng.choice(N_CUST, size=N_SESS)], "")
    ev = []
    eid = 1
    for s in range(N_SESS):
        t = sts[s]; steps = ["page_view"]
        steps += ["page_view"] * int(rng.poisson(1.2))
        if rng.random() < 0.85:
            steps.append("product_view")
            if rng.random() < a_atc[s]:
                steps.append("add_to_cart")
                if rng.random() < 0.6:
                    steps.append("begin_checkout")
                    if rng.random() < 0.7:
                        steps.append("purchase")
        for k, e in enumerate(steps):
            tt = t + pd.Timedelta(seconds=45 * k)
            ev.append([eid, f"S{800000 + s}", sess_cust[s], ts_ist(tt) if tt < MIGRATION else ts_utc(tt), e,
                       int(products.product_id[int(rng.integers(0, N_PROD))]) if e != "page_view" else None, dev[s], src[s]])
            eid += 1
    events = pd.DataFrame(ev, columns=["event_id", "session_id", "customer_id", "event_ts", "event_type", "product_id", "device", "traffic_source"])
    truth = {"n_dup_customers": 80, "dup_idx": dup_i.copy(), "moved_orders": moved, "migration": str(MIGRATION.date()),
             "customers_base": customers.iloc[:N_CUST].copy(), "dev": dev, "src": src, "conv": CONV, "mobile_mult": MOBILE_MULT,
             "n_paise_items": int(paise.sum()), "n_orphan_items": 25, "n_orphan_returns": 8, "n_zero_or_neg_qty": 12, "fest": FEST, "sale_weeks": SALE_WEEKS,
             "status_true": status.copy(), "true_rating": true_rating.copy(), "rating_seen": seen & delivered_ok, "cod": cod.copy(), "ots": ots}
    return {"orders": orders, "customers": customers, "products": products, "order_items": it, "returns": ret, "events": events}, truth


def write_db(tables, path):
    if path.exists():
        path.unlink()
    con = sqlite3.connect(path)
    con.executescript(SCHEMA)
    for name, df in tables.items():
        cols = list(df.columns)
        recs = []
        for row in df.itertuples(index=False):
            recs.append(tuple(None if (v is None or (isinstance(v, float) and np.isnan(v))) else (v.item() if hasattr(v, "item") else v) for v in row))
        con.executemany(f"INSERT INTO {name} ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})", recs)
    con.commit(); con.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[2]
    out_dir = (Path(args.out) if args.out else root / "data") / "ecom_store"
    out_dir.mkdir(parents=True, exist_ok=True)
    tables, truth = generate()
    tot = 0
    for name, df in tables.items():
        o = df.copy()
        for c in ("birth_year", "delivery_rating", "product_id"):
            if c in o:
                o[c] = o[c].map(lambda v: "" if pd.isna(v) else f"{v:.0f}")
        o.to_csv(out_dir / f"{name}.csv", index=False, lineterminator="\n")
        sz = (out_dir / f"{name}.csv").stat().st_size; tot += sz
        print(f"{name}.csv: {len(df)} rows, {df.shape[1]} columns, {sz:,} bytes")
    write_db(tables, out_dir / "ecom_store.db")
    raw = (out_dir / "ecom_store.db").read_bytes()
    print(f"ecom_store.db: {len(raw):,} bytes, sha256 {hashlib.sha256(raw).hexdigest()[:12]}; CSV total {tot:,}")


if __name__ == "__main__":
    main()
