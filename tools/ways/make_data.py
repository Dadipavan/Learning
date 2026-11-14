"""Generate the ShopKart dataset (deterministic). Writes CSVs and shopkart.db into study/ways/data/."""
import numpy as np, pandas as pd, sqlite3, os
OUT = "/Users/c2487352/Personal/Career/final/study/ways/data"
rng = np.random.default_rng(2024)
os.makedirs(OUT, exist_ok=True)

# products
cats = {"Grocery": ["Rice 5kg", "Atta 5kg", "Milk 1L", "Eggs 12", "Tea 500g", "Olive Oil 1L", "Biscuits", "Noodles"],
        "Electronics": ["Earbuds", "Power Bank", "USB Cable", "Smart Watch", "Mouse", "Keyboard"],
        "Fashion": ["T-Shirt", "Jeans", "Sneakers", "Jacket", "Socks 3-pack", "Cap"],
        "Home": ["Desk Lamp", "Bedsheet", "Water Bottle", "Cookware Set", "Storage Box", "Wall Clock"],
        "Beauty": ["Face Wash", "Shampoo", "Sunscreen", "Lip Balm", "Perfume", "Hair Oil"]}
price_rng = {"Grocery": (40, 900), "Electronics": (250, 4500), "Fashion": (300, 3500), "Home": (200, 3000), "Beauty": (90, 1800)}
adj = ["fresh", "durable", "premium", "light", "everyday", "compact", "organic", "classic", "smart", "gentle"]
rows = []
for c, names in cats.items():
    for n in names:
        lo, hi = price_rng[c]
        p = round(float(np.exp(rng.uniform(np.log(lo), np.log(hi)))) / 5) * 5
        cost = round(p * rng.uniform(0.55, 0.8), 2)
        desc = f"{rng.choice(adj)} {n.lower()} for {c.lower()} shoppers, {rng.choice(adj)} and {rng.choice(adj)}, good value"
        rows.append((n, c, p, cost, desc))
products = pd.DataFrame(rows, columns=["product", "category", "list_price", "unit_cost", "description"])
products.insert(0, "product_id", range(1, len(products) + 1))

# customers
N_C = 4000
signup = pd.to_datetime("2023-06-01") + pd.to_timedelta(rng.integers(0, 548, N_C), unit="D")
seg = rng.choice(["Regular", "Premium", "Student"], N_C, p=[0.65, 0.2, 0.15])
age = np.clip(rng.normal(34, 11, N_C).round(), 18, 75).astype(float)
age[seg == "Student"] = np.clip(rng.normal(22, 2.5, (seg == "Student").sum()).round(), 18, 30)
age[rng.random(N_C) < 0.04] = np.nan
cust = pd.DataFrame({"customer_id": np.arange(1001, 1001 + N_C), "signup_date": signup.strftime("%Y-%m-%d"), "segment": seg, "age": age})
order_c = np.argsort(signup.values, kind="stable")
act = rng.gamma(1.2, 1.0, N_C) * np.where(seg == "Premium", 1.8, 1.0)

# orders
N = 20000
days = np.arange(366)
dates0 = pd.to_datetime("2024-01-01") + pd.to_timedelta(days, unit="D")
w = (1 + 0.6 * days / 365) * (1 + 0.25 * np.sin(2 * np.pi * (days - 60) / 365)) * np.where(dates0.dayofweek >= 5, 1.25, 1.0)
w[(dates0.month == 11) & (dates0.day >= 20) & (dates0.day <= 30)] *= 1.8
d_idx = rng.choice(days, N, p=w / w.sum()); d_idx.sort()
od = dates0[d_idx]
sorted_sign = signup.values[order_c]; cw = np.cumsum(act[order_c])
cid = np.empty(N, int)
for i, d in enumerate(od.values):
    k = np.searchsorted(sorted_sign, d, side="right")
    k = max(k, 1)
    cid[i] = order_c[np.searchsorted(cw[:k], rng.random() * cw[k - 1])]
city_p = {"Bengaluru": .28, "Mumbai": .24, "Delhi": .22, "Chennai": .13, "Pune": .13}
city = rng.choice(list(city_p), N, p=list(city_p.values()))
channel = rng.choice(["App", "Web", "Store pickup"], N, p=[.55, .35, .10])
cat_p = {"Grocery": .38, "Electronics": .14, "Fashion": .2, "Home": .14, "Beauty": .14}
cat = rng.choice(list(cat_p), N, p=list(cat_p.values()))
prod = np.empty(N, object); price = np.empty(N)
for c in cats:
    m = cat == c
    sub = products[products.category == c]
    j = rng.integers(0, len(sub), m.sum())
    prod[m] = sub["product"].values[j]; price[m] = sub["list_price"].values[j]
qty = np.where(cat == "Grocery", rng.integers(1, 5, N), rng.choice([1, 1, 1, 2, 3], N))
disc = rng.choice([0, 0, 0, 0.05, 0.1, 0.15, 0.2], N)
hour = np.clip(rng.normal(15, 5, N).round(), 0, 23).astype(int)
promised = np.where(channel == "Store pickup", 0, np.where(rng.random(N) < .5, 45, 60))
rain = rng.random(N) < 0.18
cityfx = pd.Series(city).map({"Bengaluru": 8, "Mumbai": 6, "Delhi": 3, "Chennai": 0, "Pune": -2}).values
dm = 28 + cityfx + 6 * ((hour >= 18) & (hour <= 21)) + 9 * rain + 4 * (qty >= 3) + rng.gamma(3, 4, N) - 8
dm = np.round(np.clip(dm, 8, None))
status = rng.choice(["delivered", "returned", "cancelled"], N, p=[.86, .08, .06])
pr = pd.Series(cat).map({"Fashion": .17, "Electronics": .10, "Grocery": .02, "Home": .07, "Beauty": .06}).values
status = np.where(rng.random(N) < pr * (1 + 0.8 * (dm > 55)), "returned", status)
status = np.where((status == "returned") & (rng.random(N) < 0.0), "x", status)
canc = (status != "returned") & (rng.random(N) < 0.05)
status = np.where(canc, "cancelled", np.where(status == "cancelled", "delivered", status))
dmv = dm.astype(float); dmv[status == "cancelled"] = np.nan; dmv[channel == "Store pickup"] = np.nan
promised = promised.astype(float); promised[channel == "Store pickup"] = np.nan
orders = pd.DataFrame({"order_id": 500000 + np.arange(N), "customer_id": cust.customer_id.values[cid], "order_date": od.strftime("%Y-%m-%d"),
    "order_hour": hour, "city": city, "channel": channel, "category": cat, "product": prod, "quantity": qty,
    "unit_price": price, "discount": disc, "status": status, "promised_minutes": promised, "delivery_minutes": dmv})
# quirks
spell = {"Bengaluru": ["bangalore", "Bangalore ", "BENGALURU", "Bengaluru"], "Mumbai": ["mumbai", "Bombay", "MUMBAI"], "Delhi": ["delhi", "New Delhi", "DELHI "], "Chennai": ["chennai", "Madras"], "Pune": ["pune", "PUNE"]}
for k, v in spell.items():
    idx = orders.index[(orders.city == k) & (rng.random(N) < 0.10)]
    orders.loc[idx, "city"] = rng.choice(v, len(idx))
orders["city"] = orders["city"].astype(object)
orders.loc[rng.choice(N, 120, replace=False), "city"] = np.nan
orders.loc[rng.choice(N, 90, replace=False), "unit_price"] = np.nan
orders.loc[rng.choice(N, 60, replace=False), "channel"] = np.nan
orders.loc[rng.choice(N, 12, replace=False), "delivery_minutes"] = rng.choice([480, 960, 1440, 2900], 12)
orders.loc[rng.choice(N, 5, replace=False), "quantity"] = rng.choice([40, 60, 99], 5)
orders.loc[rng.choice(N, 8, replace=False), "delivery_minutes"] = -rng.integers(1, 30, 8)
dups = orders.sample(150, random_state=1)
orders = pd.concat([orders, dups]).sample(frac=1, random_state=3).sort_values(["order_date", "order_id"], kind="stable").reset_index(drop=True)
products.to_csv(f"{OUT}/products.csv", index=False)
cust.to_csv(f"{OUT}/customers.csv", index=False)
orders.to_csv(f"{OUT}/orders.csv", index=False)
db = f"{OUT}/shopkart.db"
if os.path.exists(db): os.remove(db)
con = sqlite3.connect(db)
orders.to_sql("orders", con, index=False); cust.to_sql("customers", con, index=False); products.to_sql("products", con, index=False)
con.commit(); con.close()
print(len(orders), len(cust), len(products))
