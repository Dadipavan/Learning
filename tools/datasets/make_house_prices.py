#!/usr/bin/env python3
"""house_prices: asking-price listings from a fictional property portal in 8 Indian cities (2023-2024).

Generative model (log of the true market price, INR):
  ln P = ln(base_psf[city] * tier_mult[tier]) + locality_effect + ln(800) + 0.86*ln(carpet/800)
         - 0.05*(bhk-2)                      (fixed area: more rooms means smaller rooms, so the BHK sign flips)
         + type + age + floor + metro + RERA + furnishing + parking + amenities + lift + facing + under-construction
         + city trend * years + eps,  eps ~ N(0, sd) with sd larger in expensive tiers/cities, plus 3% luxury uplift.
  Asking price = P * (1 + premium) where premium depends on who posts (owner about 10%, broker about 7%, builder about 2.5%),
  then rounded to attractive numbers (digit heaping).
Planted problems: price stored as mixed lakh/crore text, 'Price on request' (MNAR: pricier homes hide the price), wrong-magnitude
prices, three area concepts (carpet/built-up/super built-up) in three units (sq ft / sq yd / sq m), impossible values,
near-duplicate listings by several brokers, exact duplicate rows, inconsistent spellings, mixed date formats, missing values
(age MNAR: old homes hide it; floors structurally missing for houses/villas; furnishing missing for builders; bathrooms MCAR).
Locality names are real places; every number, distance and price is synthetic.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ID = "house_prices"
SEED = 20240915
N_BASE = 4200

CITY_BASE = {"Mumbai": 26000, "Delhi NCR": 12500, "Bengaluru": 10500, "Hyderabad": 9300, "Pune": 9800,
             "Chennai": 9000, "Kolkata": 7200, "Ahmedabad": 6300}
CITY_W = {"Mumbai": 0.13, "Delhi NCR": 0.17, "Bengaluru": 0.18, "Hyderabad": 0.14, "Pune": 0.12,
          "Chennai": 0.10, "Kolkata": 0.08, "Ahmedabad": 0.08}
CITY_TREND = {"Mumbai": 0.05, "Delhi NCR": 0.09, "Bengaluru": 0.08, "Hyderabad": 0.09, "Pune": 0.08,
              "Chennai": 0.06, "Kolkata": 0.05, "Ahmedabad": 0.07}
TIER_MULT = {"A": 1.55, "B": 1.0, "C": 0.76, "D": 0.58}
TIER_W = {"A": 0.14, "B": 0.38, "C": 0.34, "D": 0.14}
LOCS = {
    "Mumbai": "Bandra West:A:9 Powai:A:20 Andheri West:A:17 Chembur:B:14 Mulund West:B:28 Goregaon East:B:24 Malad West:B:26 Thane West:C:30 Borivali East:C:32 Kharghar:C:36 Vikhroli:B:21 Dombivli:D:48",
    "Delhi NCR": "Saket:A:14 Vasant Kunj:A:17 Golf Course Road Gurugram:A:25 Mayur Vihar:B:10 Sector 56 Gurugram:B:27 Sector 62 Noida:B:22 Dwarka:C:22 Rohini:C:20 Sohna Road Gurugram:C:30 Sector 137 Noida:C:30 Indirapuram:C:20 Greater Noida West:D:38",
    "Bengaluru": "Indiranagar:A:5 Koramangala:A:7 HSR Layout:B:10 Whitefield:B:18 Marathahalli:B:14 Sarjapur Road:B:20 Hebbal:B:10 JP Nagar:B:11 Electronic City:C:22 Yelahanka:C:18 Bannerghatta Road:C:14 KR Puram:C:15",
    "Hyderabad": "Banjara Hills:A:6 Jubilee Hills:A:8 Gachibowli:B:15 Madhapur:B:12 Kondapur:B:16 Kukatpally:C:14 Miyapur:C:20 Uppal:C:13 Narsingi:C:20 LB Nagar:D:15 Bachupally:D:22 Kompally:D:20",
    "Pune": "Koregaon Park:A:3 Baner:B:9 Aundh:B:8 Kothrud:B:6 Kharadi:B:9 Viman Nagar:B:7 Hinjewadi:C:18 Wakad:C:16 Hadapsar:C:10 Pimple Saudagar:C:17 Undri:D:12 Wagholi:D:15",
    "Chennai": "Adyar:A:8 Anna Nagar:A:10 Thiruvanmiyur:B:12 Velachery:B:14 Guindy:B:9 Porur:C:16 Perungudi:C:15 Sholinganallur:C:20 Medavakkam:D:20 Tambaram:D:26 Ambattur:C:18 T Nagar:A:6",
    "Kolkata": "Ballygunge:A:5 Salt Lake:A:10 Tollygunge:B:9 Jadavpur:B:9 New Town:B:14 Rajarhat:C:17 Behala:C:12 Garia:C:13 Dum Dum:C:12 Baranagar:D:10 Howrah:D:8 Kasba:B:8",
    "Ahmedabad": "Satellite:A:8 Vastrapur:A:9 Prahlad Nagar:A:10 Thaltej:B:11 Bopal:B:16 Naranpura:B:7 Gota:C:15 Maninagar:C:9 Chandkheda:C:14 Shela:C:18 Naroda:D:16 SG Highway:B:12",
}
CITY_ALIASES = {"Mumbai": ["Mumbai", "Mumbai", "Mumbai", "Bombay", "mumbai", "Mumbai "],
                "Delhi NCR": ["Delhi NCR", "Delhi NCR", "Delhi-NCR", "New Delhi", "delhi ncr", "NCR"],
                "Bengaluru": ["Bengaluru", "Bengaluru", "Bangalore", "bangalore", "Bengaluru ", "BLR"],
                "Hyderabad": ["Hyderabad", "Hyderabad", "Hyderabad", "hyderabad", "Hyd", "Hyderabad "],
                "Pune": ["Pune", "Pune", "Pune", "pune", "Pune ", "PUNE"],
                "Chennai": ["Chennai", "Chennai", "Chennai", "Madras", "chennai", "Chennai "],
                "Kolkata": ["Kolkata", "Kolkata", "Calcutta", "kolkata", "Kolkata ", "Kolkatta"],
                "Ahmedabad": ["Ahmedabad", "Ahmedabad", "Ahmedabad", "Ahmadabad", "ahmedabad", "Amdavad"]}
TYPES = ["Apartment", "Builder Floor", "Independent House", "Villa", "Studio"]
TYPE_ALIASES = {"Apartment": ["Apartment", "Apartment", "Apartment", "Flat", "apartment", "Apt"],
                "Builder Floor": ["Builder Floor", "Builder Floor", "Builder floor", "builder floor"],
                "Independent House": ["Independent House", "Independent House", "House", "independent house"],
                "Villa": ["Villa", "Villa", "villa", "Villa/Bungalow"],
                "Studio": ["Studio", "Studio", "Studio Apartment", "studio"]}
BHK_P = {"Apartment": [.14, .42, .32, .10, .02], "Builder Floor": [.02, .35, .50, .12, .01],
         "Independent House": [.02, .18, .40, .28, .12], "Villa": [0, .05, .30, .40, .25]}
CARPET_MEAN = {1: 470, 2: 760, 3: 1130, 4: 1750, 5: 2600}
TRUE = {"elasticity_carpet": 0.86, "bhk_at_fixed_area": -0.05, "age_per_year_to_25": -0.011, "age_per_year_after_25": -0.004,
        "metro_per_km": -0.022, "rera": 0.04, "semi_furnished": 0.03, "furnished": 0.075, "parking_per_slot": 0.035,
        "amenity_each": 0.006, "lift": 0.02, "east_or_ne_facing": 0.02, "under_construction": -0.05,
        "type_effect": {"Apartment": 0.0, "Builder Floor": 0.02, "Independent House": 0.06, "Villa": 0.18, "Studio": -0.05},
        "asking_premium_mean": {"Owner": 0.10, "Broker": 0.07, "Builder": 0.025},
        "area_ratio_built_up_to_carpet": 1.12, "area_ratio_super_to_carpet": 1.35, "sqft_per_sqyd": 9.0, "sqft_per_sqm": 10.7639,
        "city_trend_per_year": CITY_TREND, "luxury_uplift_share": 0.03}


def _round_price(p, rng):
    if p < 1e7:
        step = 5e5 if rng.random() < 0.55 else 1e5
    elif p < 5e7:
        step = 5e5 if rng.random() < 0.6 else 1e5
    else:
        step = 5e6 if rng.random() < 0.6 else 1e6
    return max(step, round(p / step) * step)


def _price_text(p, rng):
    r = rng.random()
    if p >= 1e7:
        cr = p / 1e7
        if r < 0.38:
            return f"{cr:.2f} Cr"
        if r < 0.48:
            return f"{cr:.2f} Crore"
        if r < 0.58:
            return f"₹{cr:.2f} Cr"
        if r < 0.63:
            return f"{cr:.1f}cr"
        if r < 0.80:
            return "Rs " + _indian(p)
        return str(int(p))
    lac = p / 1e5
    if r < 0.32:
        return f"{lac:.0f} Lac" if lac == int(lac) else f"{lac:.1f} Lac"
    if r < 0.42:
        return f"{lac:.0f} Lakh"
    if r < 0.52:
        return f"{lac:.0f}L"
    if r < 0.57:
        return f"₹{lac:.0f} L"
    if r < 0.78:
        return "Rs " + _indian(p)
    return str(int(p))


def _indian(v):
    s = str(int(v))
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:]); head = head[:-2]
    if head:
        parts.insert(0, head)
    return ",".join(parts + [tail])


def _vary(rng, alts_by_value, values):
    out = []
    for v in values:
        a = alts_by_value[v]
        out.append(a[rng.integers(len(a))])
    return np.array(out, dtype=object)


def generate():
    rng = np.random.default_rng(SEED)
    loc = []
    for city, s in LOCS.items():
        cur = []
        for t in s.split():
            if t.count(":") == 2:
                nm, tier, km = t.split(":")
                cur.append(nm)
                loc.append((city, " ".join(cur), tier, float(km)))
                cur = []
            else:
                cur.append(t)
    loc = pd.DataFrame(loc, columns=["city", "locality", "tier", "km_to_cbd"])
    loc["loc_eff"] = rng.normal(0, 0.08, len(loc))
    w = np.array([CITY_W[c] * TIER_W[t] for c, t in zip(loc.city, loc.tier)])
    for c in CITY_W:                                 # normalise inside each city so city weights hold
        m = (loc.city == c).values
        w[m] = w[m] / w[m].sum() * CITY_W[c]
    li = rng.choice(len(loc), N_BASE, p=w / w.sum())
    d = loc.iloc[li].reset_index(drop=True)
    n = len(d)
    ptype = rng.choice(TYPES, n, p=[.66, .12, .09, .06, .07])
    bhk = np.ones(n, dtype=int)
    for t, p in BHK_P.items():
        m = ptype == t
        bhk[m] = rng.choice([1, 2, 3, 4, 5], m.sum(), p=p)
    base = np.array([CARPET_MEAN[b] for b in bhk], dtype=float)
    base[ptype == "Studio"] = 330
    carpet = base * np.exp(rng.normal(0, 0.17, n)) * np.where(np.isin(ptype, ["Independent House", "Villa"]), 1.3, 1.0)
    carpet = np.clip(carpet, 180, None).round(0)
    bath = np.clip(bhk + rng.choice([-1, 0, 0, 1], n), 1, 6)
    bath[ptype == "Studio"] = 1
    tier_uc = np.array([{"A": .06, "B": .13, "C": .22, "D": .35}[t] for t in d.tier])      # new projects sit on the outskirts
    uc = (rng.random(n) < np.where(np.isin(ptype, ["Apartment", "Studio"]), tier_uc, 0.04))
    age = np.clip(rng.gamma(1.6, np.array([{"A": 9.0, "B": 6.5, "C": 5.0, "D": 3.5}[t] for t in d.tier])), 0, 40).round(0)   # older stock in prime tiers
    age[uc] = np.nan
    house = np.isin(ptype, ["Independent House", "Villa"])
    total = np.clip(rng.lognormal(2.15, 0.55, n), 3, 45).round(0)
    total[ptype == "Builder Floor"] = rng.integers(3, 5, (ptype == "Builder Floor").sum())
    floor = np.floor(rng.random(n) * (total + 1))
    floor[ptype == "Builder Floor"] = np.minimum(floor[ptype == "Builder Floor"], 3)
    total[house] = np.nan; floor[house] = np.nan
    new = uc | (np.nan_to_num(age, nan=0) <= 5)
    parking = np.array([rng.choice([0, 1, 2], p={"A": [.1, .5, .4], "B": [.2, .55, .25], "C": [.35, .55, .10], "D": [.5, .45, .05]}[t]) for t in d.tier])
    lift = np.where(np.nan_to_num(total, nan=1) >= 5, 1, 0) * (rng.random(n) < 0.93)
    amen = np.clip(rng.poisson(2.5 + 5.5 * new + 1.5 * (d.tier == "A").values + 1.0 * (d.tier == "B").values), 0, 20)
    amen[house] = np.minimum(amen[house], 4)
    facing = rng.choice(["East", "West", "North", "South", "North-East", "North-West", "South-East", "South-West"], n,
                        p=[.2, .13, .16, .12, .12, .09, .1, .08])
    rera = np.where(new, rng.random(n) < 0.85, rng.random(n) < 0.12)
    furn = rng.choice([0, 1, 2], n, p=[.45, .38, .17])
    posted = np.where(uc, np.where(rng.random(n) < 0.7, "Builder", "Broker"),
                      rng.choice(["Owner", "Broker", "Builder"], n, p=[.45, .50, .05]))
    metro = np.clip(d.km_to_cbd.values * 0.25 * np.exp(rng.normal(0, 0.5, n)), 0.2, 25).round(1)
    day = rng.integers(0, 731, n)
    t_years = day / 365.0
    # ---- true log price
    ages = np.nan_to_num(age, nan=0.0)
    ln = (np.log(np.array([CITY_BASE[c] * TIER_MULT[t] for c, t in zip(d.city, d.tier)])) + d.loc_eff.values + np.log(800)
          + TRUE["elasticity_carpet"] * np.log(carpet / 800) + TRUE["bhk_at_fixed_area"] * (bhk - 2)
          + np.array([TRUE["type_effect"][t] for t in ptype])
          + TRUE["age_per_year_to_25"] * np.minimum(ages, 25) + TRUE["age_per_year_after_25"] * np.maximum(ages - 25, 0)
          + TRUE["under_construction"] * uc
          + np.where(house, 0, 0.012 * np.minimum(np.nan_to_num(floor), 10) - 0.03 * ((floor == total) & (total >= 8)) - 0.04 * (floor == 0))
          + TRUE["metro_per_km"] * np.minimum(metro, 10) + TRUE["rera"] * rera
          + np.array([0, TRUE["semi_furnished"], TRUE["furnished"]])[furn] + TRUE["parking_per_slot"] * parking
          + TRUE["amenity_each"] * amen + TRUE["lift"] * lift
          + TRUE["east_or_ne_facing"] * np.isin(facing, ["East", "North-East"])
          + np.array([CITY_TREND[c] for c in d.city]) * t_years)
    sd = 0.10 + 0.05 * (d.tier.values == "A") + 0.03 * (d.city.values == "Mumbai") + 0.02 * (d.tier.values == "D")
    lux = rng.random(n) < TRUE["luxury_uplift_share"]
    ln = ln + rng.normal(0, sd) + lux * rng.uniform(0.3, 0.8, n)
    market = np.exp(ln)
    prem = np.array([max(0.0, rng.normal(TRUE["asking_premium_mean"][p], 0.04 if p != "Builder" else 0.015)) for p in posted])
    ask = np.array([_round_price(m * (1 + q), rng) for m, q in zip(market, prem)])

    # ---- area concepts and units
    atype = np.where(house, rng.choice(["Built-up Area", "Carpet Area"], n, p=[.7, .3]),
                     rng.choice(["Carpet Area", "Built-up Area", "Super built-up Area"], n, p=[.30, .30, .40]))
    ratio = np.where(atype == "Carpet Area", 1.0, np.where(atype == "Built-up Area", rng.uniform(1.08, 1.16, n), rng.uniform(1.25, 1.45, n)))
    stated_sqft = carpet * ratio
    yd_city = np.isin(d.city.values, ["Hyderabad", "Delhi NCR", "Ahmedabad"])
    u = rng.random(n)
    unit = np.where(house & yd_city & (u < 0.5), "sqyd", np.where(u > 0.955, "sqm", "sqft"))
    area = np.where(unit == "sqyd", stated_sqft / TRUE["sqft_per_sqyd"], np.where(unit == "sqm", stated_sqft / TRUE["sqft_per_sqm"], stated_sqft))
    area = np.where(unit == "sqft", area.round(0), area.round(1))
    psf = np.round(ask / stated_sqft)
    wrong = rng.random(n) < 0.15
    psf = np.where(wrong, np.round(ask / carpet * rng.choice([0.8, 1.0, 1.25], n)), psf)
    psf = np.where(rng.random(n) < 0.10, np.nan, psf)

    df = pd.DataFrame({"city": d.city.values, "locality": d.locality.values, "ptype": ptype, "bhk": bhk, "bath": bath.astype(float),
                       "area": area, "unit": unit, "atype": atype, "ask": ask.astype(float), "psf": psf, "floor": floor, "total": total,
                       "age": age, "uc": uc, "furn": furn, "parking": parking, "lift": lift, "amen": amen,
                       "facing": facing, "rera": rera, "posted": posted, "metro": metro, "day": day, "carpet": carpet, "market": market,
                       "lux": lux})
    # ---- near duplicates: the same flat posted by other brokers
    base_idx = rng.choice(n, int(0.12 * n), replace=False)
    dups, groups = [], []
    for gi, i in enumerate(base_idx):
        for _ in range(1 + (rng.random() < 0.45)):
            r = df.iloc[i].copy()
            r["posted"] = "Broker"
            r["ask"] = _round_price(r["ask"] * (1 + rng.normal(0, 0.02)), rng)
            r["area"] = round(r["area"] * (1 + rng.normal(0, 0.01)), 1 if r["unit"] != "sqft" else 0)
            r["day"] = int(min(730, r["day"] + rng.integers(1, 40)))
            r["psf"] = np.nan if rng.random() < 0.3 else round(r["ask"] / (r["carpet"] * 1.0))
            dups.append(r); groups.append((gi, i))
    dup_df = pd.DataFrame(dups).reset_index(drop=True)
    df["grp"] = -1
    df.loc[base_idx, "grp"] = np.arange(len(base_idx))
    dup_df["grp"] = [g for g, _ in groups]
    df = pd.concat([df, dup_df], ignore_index=True)
    df = df.sort_values("day", kind="stable").reset_index(drop=True)
    N = len(df)
    df["listing_id"] = ["HP-%06d" % v for v in (100000 + np.cumsum(rng.integers(1, 9, N)))]

    # ---- messy measurements
    outlier_area = rng.random(N) < 0.003
    area_out = np.where(outlier_area, rng.choice([5.0, 99999.0, 0.0], N), df["area"].values)
    mag = rng.random(N) < 0.005
    mag_fac = np.where(rng.random(N) < 0.5, 10.0, 0.1)
    price_val = np.where(mag, df["ask"].values * mag_fac, df["ask"].values)
    hide = rng.random(N) < 1 / (1 + np.exp(-(np.log(df["market"].values / 1.2e7) * 1.6 - 3.3)))   # MNAR: pricey homes hide price
    ptxt = np.array([_price_text(p, rng) for p in price_val], dtype=object)
    ptxt = np.where(hide, np.where(rng.random(N) < 0.7, "Price on request", "Contact for price"), ptxt)
    age_v = df["age"].values.copy()
    age_hide = rng.random(N) < 1 / (1 + np.exp(-(-4.0 + 0.15 * np.nan_to_num(age_v, nan=0))))   # MNAR: old homes hide age
    age_v = np.where(age_hide, np.nan, age_v)
    odd = rng.random(N)
    age_v = np.where(odd < 0.002, -2.0, np.where(odd < 0.004, 150.0, age_v))
    floor_v = df["floor"].values.copy(); total_v = df["total"].values.copy()
    mcar = rng.random(N) < 0.04
    floor_v = np.where(mcar, np.nan, floor_v)
    bad = (rng.random(N) < 0.02) & ~np.isnan(total_v)
    floor_v = np.where(bad, total_v + rng.integers(1, 6, N), floor_v)
    bath_v = np.where(rng.random(N) < 0.03, np.nan, df["bath"].values)
    bath_v = np.where(rng.random(N) < 0.002, 9.0, bath_v)
    FURN = [["Unfurnished", "Un-furnished", "unfurnished", "Not furnished"], ["Semi-Furnished", "Semi Furnished", "semi-furnished", "Semi"],
            ["Furnished", "Fully Furnished", "furnished", "Fully-Furnished"]]
    furn_txt = np.array([FURN[f][rng.integers(4)] for f in df["furn"].values], dtype=object)
    furn_txt = np.where((df["posted"].values == "Builder") & (rng.random(N) < 0.35), None, furn_txt)
    bhk_txt = []
    for b, t in zip(df["bhk"].values, df["ptype"].values):
        if t == "Studio":
            bhk_txt.append(["1 RK", "Studio", "1RK", "1 RK"][rng.integers(4)])
        else:
            bhk_txt.append([f"{b} BHK", f"{b} BHK", f"{b}BHK", f"{b}", f"{b} bhk", f"{b}.0"][rng.integers(6)] if rng.random() < 0.97 else f"{b} BHK")
    dts = pd.Timestamp("2023-01-01") + pd.to_timedelta(df["day"].values, unit="D")
    dstr = []
    for ts in dts:
        r = rng.random()
        dstr.append(ts.strftime("%Y-%m-%d") if r < 0.7 else ts.strftime("%d/%m/%Y") if r < 0.9 else ts.strftime("%d %b %Y"))
    loc_txt = []
    for c, l in zip(df["city"].values, df["locality"].values):
        r = rng.random()
        loc_txt.append(l if r < 0.82 else l.upper() if r < 0.89 else l + " " if r < 0.93 else l.replace(" ", "") if r < 0.96 else f"{l}, {c}")
    out = pd.DataFrame({
        "listing_id": df["listing_id"].values, "listing_date": dstr,
        "city": _vary(rng, CITY_ALIASES, df["city"].values), "locality": loc_txt,
        "property_type": _vary(rng, TYPE_ALIASES, df["ptype"].values), "bhk": bhk_txt, "bathrooms": bath_v,
        "area": area_out, "area_unit": df["unit"].values, "area_type": df["atype"].values, "price": ptxt,
        "price_per_sqft": df["psf"].values, "floor": floor_v, "total_floors": total_v, "age_years": age_v,
        "possession_status": np.where(df["uc"].values, "Under construction", "Ready to move"),
        "furnishing": furn_txt, "parking": df["parking"].values,
        "lift": np.where(df["lift"].values == 1, np.where(rng.random(N) < 0.7, "Yes", "1"), np.where(rng.random(N) < 0.7, "No", "0")),
        "amenities_count": df["amen"].values, "facing": df["facing"].values,
        "rera_registered": np.where(rng.random(N) < 0.08, None, np.where(df["rera"].values, "Yes", "No")),
        "posted_by": df["posted"].values, "metro_km": np.where(rng.random(N) < 0.06, np.nan, df["metro"].values)})
    # exact duplicate rows (portal re-post), inserted right after the original
    ex = np.sort(rng.choice(N, int(0.008 * N), replace=False))
    parts, last = [], 0
    for i in ex:
        parts.append(out.iloc[last:i + 1]); parts.append(out.iloc[[i]]); last = i + 1
    parts.append(out.iloc[last:])
    out = pd.concat(parts, ignore_index=True)
    loc_out = loc[["city", "locality", "tier", "km_to_cbd"]].copy()
    # facts for the answer key / verify script
    ids = df["listing_id"].values
    dup_groups = [[str(x) for x in ids[(df["grp"].values == g)]] for g in range(len(base_idx))]
    tm = df["market"].values
    q = np.quantile(tm, [1 / 3, 2 / 3])
    ta = df["age"].values
    rd = ~np.isnan(ta)
    ask_ratio = {k: float(np.mean((df["ask"].values / tm)[(df["posted"].values == k)])) for k in ["Owner", "Broker", "Builder"]}
    truth = dict(price_hidden_rate_by_true_price_tercile=[float(hide[tm <= q[0]].mean()), float(hide[(tm > q[0]) & (tm <= q[1])].mean()), float(hide[tm > q[1]].mean())],
                 age_hidden_rate_by_true_age={"0-5": float(age_hide[rd & (ta <= 5)].mean()), "6-15": float(age_hide[rd & (ta > 5) & (ta <= 15)].mean()),
                                              "16+": float(age_hide[rd & (ta > 15)].mean())},
                 asking_over_market_mean=ask_ratio, TRUE=TRUE, seed=SEED, n_rows=len(out), n_unique_listing_ids=int(out.listing_id.nunique()),
                 n_exact_duplicate_rows=int(len(ex)), n_near_duplicate_groups=len(base_idx), dup_groups=dup_groups,
                 n_price_hidden=int(hide.sum()), n_price_wrong_magnitude=int(mag.sum()), n_area_outliers=int(outlier_area.sum()),
                 n_age_missing_mnar=int(age_hide.sum()), n_floor_above_total=int(bad.sum()),
                 market_price=dict(zip(ids.tolist(), np.round(df["market"].values).tolist())), true_log_sd=float(np.mean(sd)))
    return {"listings": out, "localities": loc_out}, truth


def write(outdir):
    tables, _ = generate()
    outdir = Path(outdir)
    (outdir / ID).mkdir(parents=True, exist_ok=True)
    sizes = {}
    for name, df in tables.items():
        p = outdir / ID / f"{name}.csv"
        df.to_csv(p, index=False, lineterminator="\n", encoding="utf-8")
        sizes[f"{ID}/{name}.csv"] = p.stat().st_size
    return sizes


def main():
    root = Path(__file__).resolve().parents[2]
    tables, truth = generate()
    sizes = write(root / "data")
    for name, df in tables.items():
        print(f"{name}: {len(df)} rows x {len(df.columns)} cols")
    print("bytes:", sizes)
    print("near-duplicate groups:", truth["n_near_duplicate_groups"], "exact dup rows:", truth["n_exact_duplicate_rows"],
          "price hidden:", truth["n_price_hidden"], "wrong magnitude:", truth["n_price_wrong_magnitude"])


if __name__ == "__main__":
    main()
