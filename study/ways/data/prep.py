"""Shared cleaning for the ShopKart dataset (Chapter 3 explains every step)."""
import sqlite3
import pandas as pd

CITY = {"bangalore": "Bengaluru", "bengaluru": "Bengaluru", "mumbai": "Mumbai", "bombay": "Mumbai",
        "delhi": "Delhi", "new delhi": "Delhi", "chennai": "Chennai", "madras": "Chennai", "pune": "Pune"}


def load_raw(data):
    o = pd.read_csv(data + "orders.csv", parse_dates=["order_date"])
    c = pd.read_csv(data + "customers.csv", parse_dates=["signup_date"])
    p = pd.read_csv(data + "products.csv")
    return o, c, p


def load_clean(data):
    """Return (orders, customers, products) cleaned, with revenue columns."""
    o, c, p = load_raw(data)
    o = o.drop_duplicates().copy()
    o["city"] = o["city"].str.strip().str.lower().map(CITY)
    o["channel"] = o["channel"].fillna("Unknown")
    o = o[o["quantity"] <= 20].copy()
    o["unit_price"] = o["unit_price"].fillna(o["product"].map(p.set_index("product")["list_price"]))
    bad = (o["delivery_minutes"] < 5) | (o["delivery_minutes"] > 300)
    o.loc[bad, "delivery_minutes"] = float("nan")
    o["gross"] = o["quantity"] * o["unit_price"]
    o["net"] = o["gross"] * (1 - o["discount"])
    o["revenue"] = o["net"].where(o["status"] == "delivered", 0.0)
    o["late"] = (o["delivery_minutes"] > o["promised_minutes"]).astype(float)
    o.loc[o["delivery_minutes"].isna() | o["promised_minutes"].isna(), "late"] = float("nan")
    return o.reset_index(drop=True), c, p


def clean_db(data):
    """In-memory SQLite with orders (cleaned), customers, products."""
    o, c, p = load_clean(data)
    con = sqlite3.connect(":memory:")
    for name, df in (("orders", o), ("customers", c), ("products", p)):
        d = df.copy()
        for col in d.columns:
            if str(d[col].dtype).startswith("datetime"):
                d[col] = d[col].dt.strftime("%Y-%m-%d")
        d.to_sql(name, con, index=False)
    return con
