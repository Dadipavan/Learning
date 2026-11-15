#!/usr/bin/env python3
"""movie_ratings: ratings from a fictional streaming app with Indian and international films (all titles invented).

Model: rating = 3.45 + user bias + item bias + 1.1 * (user taste . item taste, rank 5) + language bonus + N(0, 0.65), then rounded.
Exposure is MNAR: users pick films with probability proportional to popularity (Zipf, rank^-0.85) * exp(0.9 * taste), so people rate what
they expected to like. Ratings are whole stars before 2023-06-01 and half stars after.
Planted problems: popularity bias, cold-start users (<=3 ratings) and late new films, scale change + mixed second/millisecond timestamps,
3 bot accounts (all 5.0 within seconds) and a review bomb (150 ratings of 0.5 on one film in an hour), duplicate re-ratings,
impossible/text ratings, user ids with a 'u' prefix, spelling variants in users.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ID = "movie_ratings"
SEED = 20250105
U, M, K = 1300, 950, 5
END_DAY = 1095           # days since 2022-01-01 -> 2024-12-31
SCALE_DAY = 516          # 2023-06-01
EPOCH0 = 1640995200      # 2022-01-01 00:00:00 UTC
LANGS = ["Hindi", "English", "Tamil", "Telugu", "Malayalam", "Bengali", "Kannada", "Marathi", "Punjabi"]
GEN = ["Drama", "Comedy", "Romance", "Action", "Thriller", "Family", "Crime", "Musical", "Horror", "Sci-Fi", "Biography", "Documentary"]
A = ["Raat", "Dil", "Safar", "Sapna", "Shehar", "Aakhri", "Pehla", "Chandni", "Toofan", "Sheesha", "Mausam", "Khwab", "Zindagi", "Rang",
     "Baazi", "Jungle", "Mohabbat", "Sunehri", "Kaali", "Meri", "Naya", "Dhoop", "Barish", "Rajdhani", "Gali", "Midnight", "Silent", "Last", "Paper", "Glass"]
B = ["Ka Raja", "Ki Kahani", "Express", "Junction", "Diaries", "Returns", "Nagar", "Wala", "Ke Baad", "Se Pehle", "Story", "Gang", "Mela", "Road",
     "Hotel", "Secret", "Code", "Files", "Garden", "Train", "Season", "Letter"]


def generate():
    rng = np.random.default_rng(SEED)
    lang = rng.choice(LANGS, M, p=[.34, .20, .10, .10, .06, .05, .05, .05, .05])
    rel_year = np.clip(2024 - rng.gamma(1.4, 6.5, M), 1990, 2024).astype(int)
    rel_day = np.where(rel_year >= 2022, (rel_year - 2022) * 365 + rng.integers(0, 365, M), -1)
    new = rng.choice(M, 60, replace=False)
    rel_day[new] = rng.integers(1000, 1085, 60); rel_year[new] = 2024
    rel_day = np.minimum(rel_day, END_DAY - 5)
    cnt, titles = {}, []
    for i in range(M):
        t = f"{A[rng.integers(len(A))]} {B[rng.integers(len(B))]}"
        cnt[t] = cnt.get(t, 0) + 1
        if cnt[t] > 1:
            t = f"{t} {cnt[t]}"
        titles.append(f"{t} ({rel_year[i]})")
    gens = ["|".join(sorted(rng.choice(GEN, rng.integers(1, 4), replace=False))) for _ in range(M)]
    movies = pd.DataFrame({"movie_id": np.arange(1, M + 1), "title": titles, "genres": gens, "language": lang, "release_year": rel_year})
    P = rng.normal(0, 0.55, (U, K)); Q = rng.normal(0, 0.55, (M, K))
    pref = rng.choice(LANGS, U, p=[.40, .15, .09, .09, .05, .06, .05, .06, .05])
    bu = rng.normal(0, 0.4, U); bi = rng.normal(0, 0.45, M)
    langb = 0.45 * (lang[None, :] == pref[:, None]) + 0.15 * (lang[None, :] == "English")
    taste = 1.1 * (P @ Q.T) + langb
    aff = 3.45 + bu[:, None] + bi[None, :] + taste
    w = (rng.permutation(M) + 1.0) ** -0.85
    cold = rng.random(U) < 0.12
    newu = (rng.random(U) < 0.08) & ~cold
    nu = np.clip(np.exp(rng.normal(np.log(24), 0.9, U)), 4, 350).astype(int)
    nu[cold] = rng.integers(1, 4, cold.sum()); nu[newu] = rng.integers(1, 8, newu.sum())
    signup = np.where(newu, rng.integers(1060, 1090, U), rng.integers(0, 1060, U))
    rows = []
    for u in range(U):
        start = np.maximum(signup[u], rel_day)
        wt = w * np.exp(0.9 * taste[u]) * (start < END_DAY - 2)
        k = int(min(nu[u], np.count_nonzero(wt)))
        it = rng.choice(M, k, replace=False, p=wt / wt.sum())
        day = start[it] + (END_DAY - start[it]) * rng.random(k) ** 1.4
        r = aff[u, it] + rng.normal(0, 0.65, k)
        rows.append(np.column_stack([np.full(k, u + 1), it + 1, r, day]))
    R = np.vstack(rows)
    uid, mid, raw, day = R[:, 0].astype(int), R[:, 1].astype(int), R[:, 2], R[:, 3]
    rating = np.where(day >= SCALE_DAY, np.round(np.clip(raw, 0.5, 5) * 2) / 2, np.clip(np.round(raw), 1, 5))
    ts = EPOCH0 + (day * 86400).astype(np.int64)
    df = pd.DataFrame({"user_id": uid, "movie_id": mid, "rating": rating, "timestamp": ts})
    # bots and a review bomb
    bots = []
    for b in range(3):
        bid = U + 1 + b
        ms = rng.choice(M, 130, replace=False)
        t0 = EPOCH0 + int((700 + 120 * b) * 86400 + 40000)
        bots.append(pd.DataFrame({"user_id": bid, "movie_id": ms + 1, "rating": 5.0, "timestamp": t0 + np.cumsum(rng.integers(1, 3, 130))}))
    bomb_movie = int(new[0]) + 1
    bu_ids = rng.choice(U, 150, replace=False) + 1
    t0 = EPOCH0 + 1090 * 86400 + 19 * 3600
    bomb = pd.DataFrame({"user_id": bu_ids, "movie_id": bomb_movie, "rating": 0.5, "timestamp": t0 + np.sort(rng.integers(0, 3600, 150))})
    bomb = bomb.merge(df[["user_id", "movie_id"]].assign(x=1), how="left", on=["user_id", "movie_id"])
    bomb = bomb[bomb.x.isna()].drop(columns="x")
    df = pd.concat([df] + bots + [bomb], ignore_index=True)
    dup = df.sample(frac=0.016, random_state=3).copy()
    dup["rating"] = np.clip(dup["rating"] + rng.choice([-0.5, 0, 0.5], len(dup)), 0.5, 5)
    dup["timestamp"] = dup["timestamp"] + rng.integers(86400, 40 * 86400, len(dup))
    df = pd.concat([df, dup], ignore_index=True).sort_values(["user_id", "timestamp"], kind="stable").reset_index(drop=True)
    N = len(df)
    bad = rng.random(N) < 0.005
    df["rating"] = df["rating"].astype(object)
    df.loc[bad, "rating"] = rng.choice([0, 6, -1, 10], int(bad.sum()))
    txt = (rng.random(N) < 0.001) & ~bad
    df.loc[txt, "rating"] = rng.choice(["five", "4/5", "N/A"], int(txt.sum()))
    ms_rows = rng.random(N) < 0.06
    df["timestamp"] = np.where(ms_rows, df["timestamp"] * 1000, df["timestamp"])
    uidtxt = df["user_id"].astype(object)
    pre = rng.random(N) < 0.02
    uidtxt[pre] = ["u%04d" % v for v in df.loc[pre, "user_id"]]
    df["user_id"] = uidtxt
    gender = rng.choice(["M", "F", "Male", "female", "male", "Other", "Non-binary", ""], U + 3, p=[.28, .24, .14, .12, .08, .04, .03, .07])
    age = rng.choice(["18-24", "25-34", "35-44", "45-54", "55+", "18 - 24", "25to34", "under 18", ""], U + 3, p=[.2, .3, .17, .09, .05, .06, .05, .03, .05])
    city = rng.choice(["Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Kochi", "Lucknow", "bangalore", "Bombay"], U + 3)
    users = pd.DataFrame({"user_id": np.arange(1, U + 4), "age_band": age, "gender": gender, "city": city,
                          "signup_date": (pd.Timestamp("2022-01-01") + pd.to_timedelta(np.concatenate([signup, [690, 810, 930]]), unit="D")).strftime("%Y-%m-%d"),
                          "preferred_language": np.concatenate([pref, ["Hindi", "English", "Hindi"]])})
    truth = dict(U=U, M=M, n_bots=3, bot_user_ids=[U + 1, U + 2, U + 3], bomb_movie_id=bomb_movie, bomb_day="2024-12-26", n_bomb=int(len(bomb)),
                 scale_change_date="2023-06-01", n_new_movies=60, new_movie_ids=[int(i) + 1 for i in new], cold_share=float(cold.mean()),
                 n_dup_rows=int(len(dup)), n_bad_rating=int(bad.sum()), n_text_rating=int(txt.sum()), n_ms_timestamps=int(ms_rows.sum()),
                 n_u_prefixed=int(pre.sum()), true_mean_all_pairs=float(np.clip(aff, 0.5, 5).mean()), exposure_gamma=0.9, zipf_exponent=0.85)
    return {"ratings": df, "movies": movies, "users": users}, truth


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
    for k, v in tables.items():
        print(f"{k}: {len(v)} rows x {len(v.columns)} cols")
    print("bytes:", sizes)


if __name__ == "__main__":
    main()
