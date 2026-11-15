#!/usr/bin/env python3
"""support_tickets: customer-support tickets of a fictional UPI / wallet / cards app ('PayNest'), Jan 2024 - Jun 2025.

Text is built from templates + vocabulary + noise (English, Hinglish in Roman script, a little Devanagari Hindi, terse chat, a few Tamil/
Telugu/Bengali/Marathi closing words, typos, SMS-speak, caps, emojis, signatures, quoted replies, HTML entities).
Truth model: true category drives the text; the observed category is wrong for 12 percent of tickets (agent label noise, fixed confusion pairs).
Escalation to L2 depends on fraud, KYC, high amounts and Premium tier. Priority depends mostly on tier and category, only weakly on the text.
Planted problems: leakage (resolution_code, closing_note, csat, resolved_at, reopened exist only after resolution), near-duplicates (same
customer re-sends within 48 h) and an outage-day cluster (2024-11-22), label noise, code-mixed text, concept drift (AutoPay mandate category
exists only from 2025-03-01), MNAR csat and open (censored) tickets, mixed date formats/timezones.
"""
import csv
from pathlib import Path
import numpy as np
import pandas as pd

ID = "support_tickets"
SEED = 20250120
CATS = ["payment_failed", "refund_status", "kyc_verification", "login_locked", "app_bug", "fraud_report", "charges_dispute", "autopay_mandate"]
CONF = {"payment_failed": "refund_status", "refund_status": "payment_failed", "charges_dispute": "fraud_report", "fraud_report": "charges_dispute",
        "login_locked": "kyc_verification", "kyc_verification": "login_locked", "app_bug": "login_locked", "autopay_mandate": "charges_dispute"}
LAUNCH = pd.Timestamp("2025-03-01")
OUTAGE = ("2024-11-22 09:30", "2024-11-22 12:30")
EN = {
 "payment_failed": ["My payment of {amt} to {m} failed but the money was deducted from my account. Transaction ref {utr}. Please check.",
                    "Payment failed at {m} for {amt}, amount debited, order not confirmed. Ref no {utr}.",
                    "UPI payment stuck on processing for {amt}. Money deducted, merchant says not received. Please resolve urgently."],
 "refund_status": ["I cancelled my order at {m} {d} but the refund of {amt} has not arrived yet. Ref {utr}.",
                   "Refund of {amt} still pending after 7 days. Please update me on the status.",
                   "Merchant confirmed refund of {amt} but I have not received it in my wallet."],
 "kyc_verification": ["My KYC is stuck in verification for 5 days. I uploaded my PAN and Aadhaar photo twice.",
                      "KYC rejected saying document not clear. Please tell me which document is needed.",
                      "Video KYC link is not working, cannot complete verification. Account limit is blocking my payments."],
 "login_locked": ["My account got locked after wrong PIN attempts. Please unlock it.", "Not able to login, OTP is not coming on my registered mobile number.",
                  "Account blocked for security reasons, I did not do anything suspicious. Please restore access."],
 "app_bug": ["The app crashes every time I open the payments tab since the last update (version {ver}).",
             "App is very slow and the balance shows wrong after update {ver}. Please fix.", "Cannot scan QR code, camera screen goes black on my phone ({ver})."],
 "fraud_report": ["I received a call asking for my OTP and {amt} was debited without my consent. Ref {utr}. Please block my account.",
                  "Unauthorized transaction of {amt} on my account. I did not make this payment. Need immediate action.",
                  "Someone sent a collect request and money was taken, I think this is a scam. Please freeze my account."],
 "charges_dispute": ["I was charged a convenience fee of {amt} which was not shown earlier. Please explain or reverse.",
                     "Double charge of {amt} on my card statement for the same transaction. Ref {utr}.", "Why was a late fee of {amt} added to my bill? I paid on time."],
 "autopay_mandate": ["My AutoPay mandate for {m} was debited twice this month. Please cancel the mandate.",
                     "Unable to set up AutoPay mandate for {m}, it keeps showing e-NACH failed.", "AutoPay deducted {amt} even after I paused the mandate."]}
HI = {
 "payment_failed": ["Mera payment {amt} ka fail ho gaya lekin paisa kat gaya. Ref {utr}. Please check karo.",
                    "{m} pe payment fail dikha raha hai par account se {amt} debit ho gaye. Kab tak wapas aayenge?",
                    "UPI payment processing me atka hua hai, {amt} kat gaye hain. Jaldi solve kijiye."],
 "refund_status": ["Maine {m} ka order cancel kiya tha, {amt} ka refund abhi tak nahi aaya. Ref {utr}.", "Refund kab milega? {amt} 7 din se pending hai.",
                   "Merchant ne bola refund bhej diya hai lekin mere wallet me {amt} nahi aaya."],
 "kyc_verification": ["Mera KYC 5 din se verification me atka hai. PAN aur Aadhaar dono upload kar diye.",
                      "KYC reject ho gaya, bol raha hai document clear nahi hai. Kaunsa document chahiye batao.", "Video KYC ka link nahi khul raha, verification complete nahi ho pa raha."],
 "login_locked": ["Galat PIN daalne ke baad mera account lock ho gaya hai. Please unlock karo.", "Login nahi ho raha, OTP aa hi nahi raha registered number pe.",
                  "Security reason bata ke account block kar diya, maine kuch galat nahi kiya. Access wapas do."],
 "app_bug": ["App update ke baad (version {ver}) payments tab kholte hi crash ho jata hai.", "App bahut slow hai aur balance galat dikha raha hai, update {ver} ke baad se.",
             "QR scan nahi ho raha, camera black ho jata hai."],
 "fraud_report": ["Kisi ne call karke OTP maanga aur mere account se {amt} nikal gaye. Ref {utr}. Account block karo.",
                  "Mere account se {amt} ka unauthorized transaction hua, maine nahi kiya. Turant action lo.", "Kisi ne collect request bheji aur paisa kat gaya, ye fraud lag raha hai."],
 "charges_dispute": ["Mujhse {amt} ka convenience fee kata gaya jo pehle nahi bataya tha. Reverse karo.", "Ek hi transaction ka {amt} do baar kat gaya hai. Ref {utr}.",
                     "Late fee {amt} kyu laga? Maine time pe pay kiya tha."],
 "autopay_mandate": ["Is mahine {m} ka AutoPay mandate do baar debit ho gaya. Mandate cancel karo.", "AutoPay mandate set nahi ho raha, e-NACH failed dikha raha hai.",
                     "Mandate pause karne ke baad bhi AutoPay se {amt} kat gaye."]}
DEV = {"payment_failed": "मेरा भुगतान फेल हो गया लेकिन पैसे कट गए, कृपया जल्दी बताएं", "refund_status": "मेरा रिफंड अभी तक नहीं आया, कृपया जल्दी बताएं",
       "login_locked": "मेरा अकाउंट लॉक हो गया है, लॉगिन नहीं हो रहा", "app_bug": "ऐप खुल नहीं रहा है, बार-बार क्रैश हो रहा है"}
TERSE = {"payment_failed": ["payment failed money cut", "paisa kat gya order nhi hua", "txn failed amt debited"], "refund_status": ["refund??", "refund kab aayega", "refund not received yet"],
         "kyc_verification": ["kyc pending since days", "kyc kab hoga", "kyc rejected why"], "login_locked": ["cant login", "account locked pls help", "otp nhi aa raha"],
         "app_bug": ["app crash", "app not opening", "qr not scanning"], "fraud_report": ["fraud!! money gone", "unauthorised txn", "someone took my money"],
         "charges_dispute": ["extra charge why", "double charged", "fee kyu kata"], "autopay_mandate": ["autopay double debit", "mandate cancel karo", "autopay not working"]}
SUBJ = {"payment_failed": ["Payment failed", "Money deducted, payment failed", "Transaction failed"], "refund_status": ["Refund not received", "Refund status", "Where is my refund"],
        "kyc_verification": ["KYC pending", "KYC verification issue", "KYC rejected"], "login_locked": ["Account locked", "Unable to login", "OTP not received"],
        "app_bug": ["App crashing", "App issue after update", "QR scan not working"], "fraud_report": ["Unauthorized transaction", "Fraud complaint", "Money debited without consent"],
        "charges_dispute": ["Wrong charge", "Double charge", "Fee dispute"], "autopay_mandate": ["AutoPay problem", "Mandate issue", "AutoPay double debit"]}
MERCH = ["FreshKart", "CabGo", "StreamBox", "MobiRecharge", "ElectraBill", "BookNest", "FoodDash"]
SMS = [("please", "pls"), ("transaction", "txn"), ("account", "acct"), ("urgent", "urgnt"), ("money", "mony"), ("immediately", "immdtly")]
EMO = ["\U0001F621", "\U0001F64F", "\U0001F624", "\U0001F44D", "\U0001F62D"]
REG = [" Seekiram pannunga.", " Tvaraga cheyandi.", " Taratari korun.", " Lavkar kara."]
CODE = {"payment_failed": "REFUND_INITIATED", "refund_status": "REFUND_INITIATED", "kyc_verification": "KYC_DOCS_REQUESTED", "login_locked": "ACCOUNT_UNLOCKED",
        "app_bug": "APP_FIX_PENDING", "fraud_report": "FRAUD_CARD_BLOCKED", "charges_dispute": "CHARGE_REVERSED", "autopay_mandate": "MANDATE_CANCELLED"}
TEAM = {"payment_failed": "Payments", "refund_status": "Payments", "kyc_verification": "KYC", "login_locked": "Accounts", "app_bug": "Tech",
        "fraud_report": "Risk", "charges_dispute": "Billing", "autopay_mandate": "Billing"}


def sig(x):
    return 1 / (1 + np.exp(-x))


def _typo(s, rng):
    w = s.split(" ")
    for _ in range(rng.integers(1, 3)):
        i = rng.integers(len(w))
        if len(w[i]) > 3:
            j = rng.integers(len(w[i]) - 1)
            w[i] = w[i][:j] + w[i][j + 1] + w[i][j] + w[i][j + 2:]
    return " ".join(w)


def _fill(t, rng):
    amt = int(np.exp(rng.normal(6.6, 1.1)))
    a = [f"Rs {amt:,}", f"Rs.{amt}", f"₹{amt}", f"{amt} rs"][rng.integers(4)]
    return t.format(amt=a, m=MERCH[rng.integers(len(MERCH))], utr="".join(str(rng.integers(10)) for _ in range(12)),
                    d=["yesterday", "last week", "on Monday", "kal"][rng.integers(4)], ver=f"{rng.integers(5, 9)}.{rng.integers(0, 9)}.{rng.integers(0, 9)}"), amt


def _body(cat, ch, rng):
    r = rng.random()
    if r < 0.50:
        lang, t = "en", EN[cat][rng.integers(3)]
    elif r < 0.78:
        lang, t = "hinglish", HI[cat][rng.integers(3)]
    elif r < 0.83 and cat in DEV:
        lang, t = "devanagari", DEV[cat]
    elif r < 0.91:
        lang, t = "terse", TERSE[cat][rng.integers(3)]
    else:
        lang, t = "hinglish", HI[cat][rng.integers(3)]
    t, amt = _fill(t, rng)
    if lang != "devanagari" and rng.random() < 0.22:
        t = _typo(t, rng)
    if lang in ("en", "hinglish") and rng.random() < 0.15:
        for a, b in SMS:
            t = t.replace(a, b)
    if lang == "hinglish" and rng.random() < 0.05:
        t += REG[rng.integers(4)]
    if rng.random() < 0.06:
        t = t.upper()
    if rng.random() < 0.10:
        t += " " + EMO[rng.integers(len(EMO))]
    if ch == "email" and lang != "terse":
        t = "Hello PayNest team,\n" + t + "\n\nRegards,\n" + ["Rahul", "Priya", "Arjun", "Sneha", "Vikram", "Anita"][rng.integers(6)] + "\n" + ["Sent from my iPhone", "Get Outlook for Android", ""][rng.integers(3)]
        if rng.random() < 0.08:
            t += "\n\n> On Mon, PayNest Support wrote:\n> Thank you for contacting us. Please share the transaction reference."
    if ch == "phone" and lang != "devanagari":
        t = t.lower().replace(".", "").replace(",", "")
    if rng.random() < 0.02:
        t = t.replace("&", "&amp;").replace("'", "&#39;") + " &amp;"
    return t, lang, amt


def generate():
    rng = np.random.default_rng(SEED)
    base_n = 3000
    start = pd.Timestamp("2024-01-01")
    day = rng.integers(0, 546, base_n)
    hr = np.where(rng.random(base_n) < 0.55, rng.normal(11.5, 2.0, base_n), rng.normal(20.5, 1.8, base_n)) % 24
    created = start + pd.to_timedelta(day, unit="D") + pd.to_timedelta((hr * 3600).astype(int), unit="s")
    cust_w = np.exp(rng.normal(0, 1.0, 1900)); cust_w /= cust_w.sum()
    cust = rng.choice(1900, base_n, p=cust_w)
    tier_c = rng.choice(["Basic", "Plus", "Premium"], 1900, p=[.62, .28, .10])
    rows = []
    post = created >= LAUNCH
    for i in range(base_n):
        p = np.array([.24, .17, .12, .13, .14, .07, .13, 0.0]) if not post[i] else np.array([.20, .15, .10, .11, .12, .06, .17, .09])
        cat = CATS[rng.choice(8, p=p / p.sum())]
        rows.append((created[i], cust[i], cat))
    # outage-day cluster: different customers, same problem
    out_start = pd.Timestamp(OUTAGE[0]); out_n = 110
    for j in range(out_n):
        rows.append((out_start + pd.Timedelta(seconds=int(rng.integers(0, 3 * 3600))), int(rng.integers(0, 1900)), "payment_failed"))
    rows.sort(key=lambda r: r[0])
    n0 = len(rows)
    ch_all = rng.choice(["email", "chat", "whatsapp", "phone"], n0, p=[.30, .40, .18, .12])
    recs = []
    for i, (ts, c, cat) in enumerate(rows):
        body, lang, amt = _body(cat, ch_all[i], rng)
        recs.append(dict(ts=ts, cust=c, cat=cat, ch=ch_all[i], body=body, lang=lang, amt=amt, dup_of=-1, outage=bool(out_start <= ts <= out_start + pd.Timedelta(hours=3))))
    # near-duplicates: same customer re-sends
    ndup = int(0.07 * n0)
    for src in rng.choice(n0, ndup, replace=False):
        o = recs[src]
        pre = ["Re: ", "Reminder: ", "Third time writing. ", "PLEASE REPLY. ", "Any update? "][rng.integers(5)]
        recs.append(dict(o, ts=min(o["ts"] + pd.Timedelta(seconds=int(rng.integers(2 * 3600, 48 * 3600))), pd.Timestamp("2025-06-30 22:00")), body=pre + o["body"], dup_of=src, outage=False))
    recs.sort(key=lambda r: r["ts"])
    N = len(recs)
    ids = ["T-%06d" % (100000 + k * 2 + int(rng.integers(0, 2))) for k in range(N)]
    return _finish(rng, recs, ids, tier_c, N)


def _finish(rng, recs, ids, tier_c, N):
    cat_true = np.array([r["cat"] for r in recs], dtype=object)
    ch = np.array([r["ch"] for r in recs], dtype=object)
    cust = np.array([r["cust"] for r in recs])
    tier = tier_c[cust]
    amt = np.array([r["amt"] for r in recs], dtype=float)
    created = pd.DatetimeIndex([r["ts"] for r in recs])
    is_dup = np.array([r["dup_of"] >= 0 for r in recs])
    is_out = np.array([r["outage"] for r in recs])
    # label noise
    noisy = rng.random(N) < 0.12
    cat_obs = np.where(noisy, [CONF[c] for c in cat_true], cat_true).astype(object)
    # priority (mostly tier + category)
    score = (0.9 * (cat_true == "fraud_report") + 0.4 * (cat_true == "payment_failed") + 0.5 * (amt > 8000) + 0.7 * (tier == "Premium") + 0.3 * (tier == "Plus")
             - 0.2 * (cat_true == "app_bug") + rng.normal(0, 0.55, N))
    prio = np.where(score > 1.3, "P1", np.where(score > 0.7, "P2", np.where(score > 0.1, "P3", "P4")))
    lp = (-2.4 + 1.7 * (cat_true == "fraud_report") + 0.8 * (cat_true == "kyc_verification") + 0.9 * (amt > 10000) + 0.7 * (tier == "Premium")
          + 0.4 * (cat_true == "charges_dispute") - 1.0 * is_out + rng.normal(0, 0.4, N))
    esc = rng.random(N) < sig(lp)
    med = np.array([{"P1": 12, "P2": 35, "P3": 120, "P4": 300}[p] for p in prio], dtype=float) * np.where(ch == "chat", 0.5, np.where(ch == "email", 1.5, 1.0))
    frt = np.round(np.exp(rng.normal(np.log(med), 0.7)), 0).astype(int)
    res_h = np.exp(rng.normal(np.log(20), 0.9)) * np.where(esc, 2.5, 1.0) * np.where(cat_true == "fraud_report", 1.5, 1.0) * np.where(prio == "P1", 0.6, 1.0)
    cutoff = pd.Timestamp("2025-06-30 23:59")
    resolved = created + pd.to_timedelta((res_h * 3600).astype(int), unit="s")
    is_open = (resolved > cutoff) | (rng.random(N) < 0.03)
    slow = res_h > 72
    reopened = rng.random(N) < (0.05 + 0.12 * slow)
    answer = rng.random(N) < sig(-1.5 + 1.0 * (slow | reopened) + 0.5 * (res_h < 4))
    csat = np.where(slow | reopened, rng.choice([1, 2, 3], N, p=[.5, .3, .2]), rng.choice([3, 4, 5], N, p=[.1, .35, .55])).astype(float)
    csat = np.where(answer & ~is_open, csat, np.nan)
    code = np.array([CODE[c] for c in cat_true], dtype=object)
    code = np.where(esc & np.isin(cat_true, ["payment_failed", "refund_status", "charges_dispute"]), "ESCALATED_TO_BANK", code)
    code = np.where(rng.random(N) < 0.08, "NO_ISSUE_FOUND", code)
    code = np.where(is_dup, "DUPLICATE_TICKET", code)
    note = np.array([{"ESCALATED_TO_BANK": "Raised with partner bank, awaiting reply.", "REFUND_INITIATED": "Refund initiated, will reflect in 3 to 5 working days.",
                      "KYC_DOCS_REQUESTED": "Asked customer to re-upload documents.", "ACCOUNT_UNLOCKED": "Account unlocked after identity check.",
                      "APP_FIX_PENDING": "Logged with tech team, fix in next release.", "FRAUD_CARD_BLOCKED": "Account frozen and fraud case opened.",
                      "CHARGE_REVERSED": "Charge reversed to source account.", "MANDATE_CANCELLED": "Mandate cancelled as requested.",
                      "NO_ISSUE_FOUND": "No issue found on our side.", "DUPLICATE_TICKET": "Merged with earlier ticket."}[c] for c in code], dtype=object)
    merged = np.array([None] * N, dtype=object)
    first_out = int(np.where(is_out)[0][0]) if is_out.any() else -1
    for k in range(N):
        r = recs[k]
        if r["dup_of"] >= 0 and rng.random() < 0.45:
            merged[k] = "dup"          # replaced below with the original's id
        if is_out[k] and k != first_out and rng.random() < 0.30:
            merged[k] = ids[first_out]
    # resolve duplicate originals: nearest earlier record with identical customer and same true category
    for k in np.where(merged == "dup")[0]:
        cand = [j for j in range(k - 1, max(-1, k - 400), -1) if cust[j] == cust[k] and cat_true[j] == cat_true[k] and not is_dup[j]]
        merged[k] = ids[cand[0]] if cand else None
    # timestamps in mixed formats
    fmts = rng.choice(5, N, p=[.45, .25, .10, .10, .10])
    ts_txt = []
    for t, f in zip(created, fmts):
        if f == 0:
            ts_txt.append(t.strftime("%Y-%m-%dT%H:%M:%S") + "+05:30")
        elif f == 1:
            ts_txt.append(t.strftime("%d/%m/%Y %H:%M"))
        elif f == 2:
            ts_txt.append(str(int((t - pd.Timestamp("1970-01-01") - pd.Timedelta(hours=5, minutes=30)).total_seconds())))
        elif f == 3:
            ts_txt.append(f"{t.strftime('%b')} {t.day}, {t.year} {t.hour % 12 or 12}:{t.minute:02d} {'AM' if t.hour < 12 else 'PM'}")
        else:
            ts_txt.append((t - pd.Timedelta(hours=5, minutes=30)).strftime("%Y-%m-%dT%H:%M:%S") + "Z")
    subj = np.array([SUBJ[c][rng.integers(3)] for c in cat_true], dtype=object)
    subj = np.where(ch == "chat", "", subj)
    subj = np.where(is_dup, np.char.add("Re: ", subj.astype(str)), subj)
    out = pd.DataFrame({
        "ticket_id": ids, "created_at": ts_txt, "customer_id": ["C-%05d" % (10000 + c) for c in cust], "channel": ch, "tier": tier,
        "subject": subj, "body": [r["body"] for r in recs], "category": cat_obs, "priority": prio,
        "assigned_team": [TEAM[c] for c in cat_obs], "escalated_to_l2": esc.astype(int), "first_response_min": frt,
        "resolved_at": np.where(is_open, None, resolved.strftime("%Y-%m-%d %H:%M")), "resolution_hours": np.where(is_open, np.nan, np.round(res_h, 1)),
        "csat": csat, "reopened": np.where(is_open, None, np.where(reopened, "Y", "N")), "resolution_code": np.where(is_open, None, code),
        "closing_note": np.where(is_open, None, note), "merged_into": merged})
    lang = np.array([r["lang"] for r in recs])
    truth = dict(n=N, n_near_dup=int(is_dup.sum()), n_outage=int(is_out.sum()), outage_window=OUTAGE, launch_date="2025-03-01",
                 label_noise_rate=float(noisy.mean()), confusion_pairs=CONF, n_open=int(is_open.sum()), csat_response_rate=float(np.isfinite(csat).mean()),
                 language_share={k: float((lang == k).mean()) for k in ["en", "hinglish", "devanagari", "terse"]}, esc_rate=float(esc.mean()),
                 true_category=dict(zip(ids, cat_true.tolist())), dup_ids=[ids[k] for k in np.where(is_dup)[0]], outage_ids=[ids[k] for k in np.where(is_out)[0]],
                 language=dict(zip(ids, lang.tolist())))
    return {ID: out}, truth


def write(outdir):
    tables, _ = generate()
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    p = outdir / f"{ID}.csv"
    tables[ID].to_csv(p, index=False, lineterminator="\n", encoding="utf-8", quoting=csv.QUOTE_NONNUMERIC)
    return {f"{ID}.csv": p.stat().st_size}


def main():
    root = Path(__file__).resolve().parents[2]
    tables, truth = generate()
    sizes = write(root / "data")
    print(f"{ID}: {len(tables[ID])} rows x {len(tables[ID].columns)} cols", sizes)
    print({k: truth[k] for k in ["n_near_dup", "n_outage", "label_noise_rate", "n_open", "csat_response_rate", "esc_rate", "language_share"]})


if __name__ == "__main__":
    main()
