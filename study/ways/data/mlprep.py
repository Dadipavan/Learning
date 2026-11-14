"""Feature builders shared by Chapters 6 to 8."""
import pandas as pd

CAT = ["city", "category", "channel"]
NUM = ["order_hour", "quantity", "discount", "promised_minutes", "evening", "weekend"]


def late_frame(o):
    """Orders that have a promise and a delivery time, with simple features known at order time."""
    d = o.dropna(subset=["late"]).copy()
    d["evening"] = d.order_hour.between(18, 21).astype(int)
    d["weekend"] = (d.order_date.dt.dayofweek >= 5).astype(int)
    return d


def build_churn(o, c, cut):
    """One row per customer active in the 90 days before `cut`; label = no order in the next 90 days."""
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
