"""CD-QFed analysis.

Reported method  : METHOD   = "CDQ-lit"  -> CD-QFed exactly as proposed (Eqs. 16-22, Gauss-Markov orphan shrinkage ON)
Shrinkage ablation: SHRINK  = "CDQ"      -> identical framework with the Gauss-Markov orphan shrinkage REMOVED

Everything reported is a PAIRED statistic over common random numbers (same seed, same cell), with paired t-tests,
Wilcoxon, Benjamini-Hochberg FDR across each metric family, n reported per row, and a power statement
(observed effect, observed paired sd, n required for 80% power).  Every printed table has a matching figure.
"""
import os, json, math, itertools
import numpy as np, pandas as pd
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt

PLOT_DIR = "plots"
METHOD = "CDQ-lit"          # proposed algorithm
SHRINK = "CDQ"              # same framework, orphan shrinkage removed
BASELINE_ORDER = ["base", "JEQFL", "M4a", "M4ab", "M5b", "M3", "M2", "CDQ", "CDQ-lit"]
MAIN_V = ["base", "JEQFL", "M4a", "M4ab", "M5b", "M3", "M2", "CDQ", "CDQ-lit"]

C = dict(blue="#0072B2", orange="#E69F00", green="#009E73", verm="#D55E00", sky="#56B4E9", purple="#CC79A7",
         grey="#6b6b6b", yellow="#F0E442", black="#000000")
VCOL = {"base": C["grey"], "JEQFL": C["sky"], "M4a": C["yellow"], "M4ab": C["orange"], "M5b": C["purple"],
        "M3": "#8c6d31", "M2": "#9edae5", "CDQ": C["verm"], "CDQ-lit": "#7b3294",
        "CDQ-noI1": "#f4a582", "CDQ-noI2": "#92c5de", "CDQ-noI3a": "#b2abd2", "CDQ-noI3b": "#a6dba0", "CDQ-noI4": "#fddbc7",
        "CDQ-lit-noI1": "#d6604d", "CDQ-lit-noI2": "#4393c3", "CDQ-lit-noI3a": "#8073ac", "CDQ-lit-noI3b": "#5aae61",
        "CDQ-lit-noI4": "#f6e8c3"}
TCOL = {"Good": C["green"], "Medium": C["orange"], "Bad": C["verm"]}
plt.rcParams.update({"figure.dpi": 105, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
                     "grid.color": "#e5e5e5", "axes.axisbelow": True, "axes.titlesize": 10, "axes.titleweight": "bold",
                     "axes.labelsize": 9, "legend.frameon": False, "legend.fontsize": 8, "xtick.labelsize": 8,
                     "ytick.labelsize": 8, "figure.max_open_warning": 0})
CELL = ["scale", "arm", "alpha", "channel"]
SCORD = ["small", "medium", "large"]

# every numeric column the sweep records -> label and polarity (True = higher is better)
NUMCOLS = [
    ("acc_tail",    True,  "final accuracy (mean of last 3 evals)"),
    ("acc_final",   True,  "accuracy at the last round"),
    ("drift",       False, "client drift E_drift (Eq. 1)"),
    ("drift_tail",  False, "client drift E_drift, last third of rounds"),
    ("scda",        True,  "drift alignment S_CDA (Eq. 2)"),
    ("rec_err",     False, "gradient reconstruction error |g_hat - g*|"),
    ("att_ratio",   None,  "|g_hat| / |g*|   (ideal 1.0)"),
    ("bad_share",   None,  "Bad-tier share of effective weight (ideal 1/3)"),
    ("active_mean", True,  "active clients per round (participation)"),
    ("mismatch",    False, "Eq. (42) subset-mismatch magnitude"),
    ("gamma_orph",  None,  "realised Gauss-Markov orphan shrinkage gamma_orph"),
    ("eps_mean",    False, "fleet-mean compiled infidelity eps"),
    ("eps_bad",     False, "Bad-tier compiled infidelity eps"),
]
LAB = {c: l for c, _, l in NUMCOLS}
HB = {c: h for c, h, _ in NUMCOLS}


def col(v):
    return VCOL.get(v, "#999999")


def _order(xs):
    return sorted(xs, key=lambda s: SCORD.index(s) if s in SCORD else 99)


def _save(fig, name):
    os.makedirs(PLOT_DIR, exist_ok=True)
    p = os.path.join(PLOT_DIR, name)
    fig.savefig(p, bbox_inches="tight", dpi=130)
    plt.show()
    plt.close(fig)
    return p


# ================================================================================================ statistics
def bh(p):
    p = np.asarray(p, float); n = len(p)
    if n == 0: return p
    o = np.argsort(p); q = np.empty(n)
    q[o] = np.minimum.accumulate((p[o] * n / (np.arange(n) + 1))[::-1])[::-1]
    return np.clip(q, 0, 1)


def ttest(d):
    d = np.asarray(d, float); n = len(d)
    m = float(d.mean()) if n else float("nan")
    sd = float(d.std(ddof=1)) if n > 1 else float("nan")
    if n < 3 or not np.isfinite(sd): return n, m, sd, float("nan"), float("nan"), float("nan")
    if sd == 0: return n, m, sd, float("inf") if m else 0.0, 0.0 if m else 1.0, float("nan")
    t = m / (sd / math.sqrt(n)); p = float(2 * stats.t.sf(abs(t), n - 1))
    try: pw = float(stats.wilcoxon(d).pvalue) if n >= 6 and np.any(d != 0) else float("nan")
    except Exception: pw = float("nan")
    return n, m, sd, t, p, pw


def n_for_power(gap, sd, power=0.80, alpha=0.05):
    """paired-design n for the OBSERVED effect size and paired sd (normal approximation, two-sided)."""
    if not np.isfinite(gap) or not np.isfinite(sd) or gap == 0: return float("nan")
    z = stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(power)
    return float(math.ceil((z * sd / abs(gap)) ** 2))


def paired(df, a, b, metric):
    """one row per (cell, seed): metric(a) - metric(b) on the SAME seed and cell -> common random numbers."""
    x = df[df.variant == a].set_index(CELL + ["seed"])[metric]
    y = df[df.variant == b].set_index(CELL + ["seed"])[metric]
    j = x.to_frame("a").join(y.to_frame("b"), how="inner")
    j["d"] = j["a"] - j["b"]
    return j.reset_index()


def verdict(gap, q, higher_better=True):
    if higher_better is None: return "n/a (diagnostic)"
    if not np.isfinite(gap): return "n/a"
    good = gap > 0 if higher_better else gap < 0
    if np.isfinite(q) and q < 0.05: return "GOOD (significant)" if good else "BAD (significant)"
    return "good trend (n.s.)" if good else ("bad trend (n.s.)" if gap != 0 else "no change")


METRICS = [("acc_tail", True, "accuracy"), ("drift", False, "client-drift E_drift"), ("scda", True, "drift alignment S_CDA")]
METRICS_EXT = METRICS + [("rec_err", False, "reconstruction error"), ("active_mean", True, "active clients"),
                         ("att_ratio", None, "|g_hat|/|g*|"), ("bad_share", None, "Bad-tier weight share")]


def comparison_table(df, method=None, baselines=None, by=("scale",), metrics=None):
    method = method or METHOD
    baselines = baselines or BASELINE_ORDER
    metrics = metrics or METRICS
    rows = []
    for b in [x for x in baselines if x != method]:
        if b not in set(df.variant): continue
        for met, hb, lab in metrics:
            if met not in df.columns: continue
            j = paired(df, method, b, met)
            if j.empty: continue
            for key, g in j.groupby(list(by)):
                key = key if isinstance(key, tuple) else (key,)
                n, m, sd, t, p, pw = ttest(g["d"].values)
                rel = float(100 * g["d"].sum() / (abs(g["b"]).sum() + 1e-12))
                rows.append(dict(zip(by, key), baseline=b, metric=lab, n_pairs=n, mean_method=float(g["a"].mean()),
                                 mean_baseline=float(g["b"].mean()), gap=m, rel_change_pct=rel, sd=sd, t=t, p=p,
                                 p_wilcoxon=pw, n_80pow=n_for_power(m, sd), hb=hb))
    T = pd.DataFrame(rows)
    if T.empty: return T
    T["q_BH"] = np.nan
    for met in T.metric.unique():
        mk = T.metric == met; ok = mk & T.p.notna()
        T.loc[ok, "q_BH"] = bh(T.loc[ok, "p"].values)
    T["verdict"] = [verdict(g, q, hb) for g, q, hb in zip(T.gap, T.q_BH, T.hb)]
    return T.drop(columns="hb")


def ablation_table(df, method=None):
    """contribution of each innovation: method minus (method with that innovation removed)."""
    method = method or METHOD
    pre = method + "-no"
    rows = []
    for ab in [v for v in sorted(set(df.variant)) if v.startswith(pre)]:
        for met, hb, lab in METRICS:
            j = paired(df, method, ab, met)
            if j.empty: continue
            for sc, g in j.groupby("scale"):
                n, m, sd, t, p, pw = ttest(g["d"].values)
                rows.append(dict(scale=sc, removed=ab.replace(pre, ""), metric=lab, n_pairs=n,
                                 full=float(g["a"].mean()), ablated=float(g["b"].mean()), contribution=m,
                                 sd=sd, t=t, p=p, hb=hb))
    T = pd.DataFrame(rows)
    if T.empty: return T
    T["q_BH"] = bh(T.p.fillna(1).values)
    T["innovation_helps"] = [verdict(c, q, hb) for c, q, hb in zip(T.contribution, T.q_BH, T.hb)]
    return T.drop(columns="hb")


def shrinkage_table(df, method=None, shrink=None, by=("scale",)):
    """the single-scalar ablation: CDQ-lit (gamma_orph ON) vs CDQ (gamma_orph removed), on every metric."""
    return comparison_table(df, method=method or METHOD, baselines=[shrink or SHRINK], by=by, metrics=METRICS_EXT)


def power_table(T):
    d = T[T.metric.isin([m[2] for m in METRICS])].copy()
    return d[["scale", "baseline", "metric", "n_pairs", "gap", "sd", "n_80pow", "p", "q_BH", "verdict"]]


# ================================================================================================ plots
def plot_compile(compile_tbl, sel, scales):
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.4))
    keys = ["none"]
    for i, s in enumerate(scales):
        keys = ["none"] + [k for k in sorted(sel[s][2]) if k != "none"]
        loc = [sum(compile_tbl["%s|%s" % (s, k)]["S_local"].values()) for k in keys]
        epr = [sum(compile_tbl["%s|%s" % (s, k)]["E_link"].values()) for k in keys]
        x = np.arange(len(keys)); ax[0].plot(x, loc, "o-", label=s); ax[1].plot(x, epr, "o-", label=s)
        sc = [sel[s][2][k] for k in keys]; ax[2].plot(x, np.array(sc) / sc[0], "o-", label=s)
        b = keys.index(sel[s][0]); ax[2].plot(b, sc[b] / sc[0], "*", ms=14, color="k")
    for a, t in zip(ax, ["local SWAPs (DMapS-R)", "EPR pairs (remote CX=1, remote SWAP=2)",
                         "predicted fleet Psi_NSR / baseline  (* = selected)"]):
        a.set_title(t); a.set_xticks(range(len(keys))); a.set_xticklabels(keys, rotation=20); a.legend()
    fig.suptitle("Innovation 1 - DMapS-FSNR compiles (gamma'=0 == 'none') and Psi_NSR-based selection",
                 fontsize=10.5, fontweight="bold")
    return _save(fig, "01_dmaps_fsnr_compile.png")


def plot_calibration(cal, scales):
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.3)); w = 0.25
    for i, s in enumerate(scales):
        for j, (tn, cc) in enumerate(TCOL.items()):
            ax[0].bar(i + (j - 1) * w, cal[s]["realised"][j], w, color=cc, label=tn if i == 0 else None)
            ax[1].bar(i + (j - 1) * w, cal[s]["tier_signal"][j], w, color=cc, label=tn if i == 0 else None)
    ax[0].axhline(1 - np.mean([cal[s]["m2"] for s in scales]), ls="--", c="k", lw=0.8)
    ax[0].set_title("sigma^2 * M per tier (floor 1-m2 dashed)")
    ax[1].set_title("signal e^{-eps} per tier  -> 1:3:10 attenuation")
    for a in ax: a.set_xticks(range(len(scales))); a.set_xticklabels(scales); a.legend()
    return _save(fig, "02_calibration_tiers.png")


def plot_theory(th):
    L2 = pd.DataFrame(th["lemma2"]); L3 = pd.DataFrame(th["lemma3"]); L4 = pd.DataFrame(th["lemma4"])
    fig, ax = plt.subplots(1, 4, figsize=(16, 3.4))
    x = np.arange(len(L2)); lab = [f"{a[0]}-{b[0]}" for a, b in zip(L2.scale, L2.tier)]
    ax[0].bar(x - 0.2, 1 - L2.attenuation, 0.4, color=C["grey"], label="baseline bias 1-e^{-eps}")
    ax[0].bar(x + 0.2, L2.delta_analytic, 0.4, color=C["verm"], label="R-FD residual delta (Lemma 2)")
    ax[0].plot(x + 0.2, L2.delta_mc, "k.", label="Monte-Carlo")
    ax[0].set_xticks(x); ax[0].set_xticklabels(lab, rotation=60); ax[0].set_title("Lemma 2: attenuation drift"); ax[0].legend()
    ax[1].bar(x - 0.27, L2.mse_raw, 0.27, color=C["grey"], label="raw")
    ax[1].bar(x, L2.mse_naive_inv, 0.27, color=C["sky"], label="naive e^{eps}")
    ax[1].bar(x + 0.27, L2.mse_rfd, 0.27, color=C["verm"], label="MMSE R-FD")
    ax[1].set_yscale("log"); ax[1].set_xticks(x); ax[1].set_xticklabels(lab, rotation=60)
    ax[1].set_title("Lemma 2: reconstruction MSE"); ax[1].legend()
    xc = np.arange(len(L3))
    ax[2].bar(xc - 0.2, L3.mism_m5a_mc, 0.4, color=C["grey"], label="M5a (Joint EQFL) MC")
    ax[2].plot(xc - 0.2, L3.mism_m5a_formula, "k_", ms=18, label="Eq.(27) formula")
    ax[2].bar(xc + 0.2, L3.mism_drjps_mc, 0.4, color=C["verm"], label="DR-JPS MC")
    ax[2].set_xticks(xc); ax[2].set_xticklabels(L3.channel)
    a2 = ax[2].twinx(); a2.plot(xc, L3.N_eff_m5b, "s--", c=C["purple"], label="N_eff M5b")
    a2.plot(xc, L3.N_eff_drjps, "o--", c=C["verm"], label="N_eff DR-JPS")
    a2.set_ylabel("active clients"); a2.legend(loc="upper right"); ax[2].legend(loc="upper left")
    ax[2].set_title("Lemma 3: subset mismatch & participation")
    ax[3].bar(np.arange(len(L4)) - 0.2, L4.drift_memoryless, 0.4, color=C["grey"], label="memoryless")
    ax[3].bar(np.arange(len(L4)) + 0.2, L4.drift_fedqdrift, 0.4, color=C["verm"], label="Fed-QDrift")
    ax[3].set_xticks(range(len(L4))); ax[3].set_xticklabels(["p=%.2f" % p for p in L4.p_dec])
    ax[3].set_yscale("log"); ax[3].set_title("Lemma 4: partial-participation drift"); ax[3].legend()
    fig.tight_layout(); return _save(fig, "03_theory_checks.png")


def plot_gates(gates, fname="00_acceptance_gates.png"):
    if not gates: return
    fig, ax = plt.subplots(figsize=(11, 0.42 * len(gates) + 0.9)); ax.axis("off"); ax.grid(False)
    for i, (name, ok, detail) in enumerate(gates[::-1]):
        y = i / max(len(gates), 1)
        ax.text(0.0, y, "PASS" if ok else "FAIL", color=C["green"] if ok else C["verm"], fontweight="bold", fontsize=9)
        ax.text(0.08, y, name, fontsize=8.5)
        ax.text(0.08, y - 0.028, str(detail)[:150], fontsize=6.6, color="#555")
    ax.set_title("Acceptance gates (evaluated before any accuracy was inspected)", loc="left")
    ax.set_ylim(-0.06, 1.04); return _save(fig, fname)


def plot_curves(df, variants=None, alpha=25, fname="04_accuracy_curves.png"):
    variants = variants or [v for v in ["base", "JEQFL", "M5b", "M4ab", "CDQ", "CDQ-lit"] if v in set(df.variant)]
    cells = df[df.alpha == alpha][["scale", "arm", "channel"]].drop_duplicates().sort_values(["scale", "arm", "channel"]).values.tolist()
    if not cells: return
    nc = min(4, len(cells)); nr = int(math.ceil(len(cells) / nc))
    fig, ax = plt.subplots(nr, nc, figsize=(3.6 * nc, 2.8 * nr), squeeze=False)
    for i, (s, a, ch) in enumerate(cells):
        A = ax[i // nc][i % nc]
        for v in variants:
            d = df[(df.scale == s) & (df.arm == a) & (df.channel == ch) & (df.alpha == alpha) & (df.variant == v)]
            if d.empty: continue
            cur = np.array([json.loads(c) for c in d.acc_curve]); x = 5 * (np.arange(cur.shape[1]) + 1)
            A.plot(x, cur.mean(0), color=col(v), lw=2.2 if v == METHOD else 1.2, label=v)
            if v in (METHOD, "base"):
                A.fill_between(x, cur.mean(0) - cur.std(0), cur.mean(0) + cur.std(0), color=col(v), alpha=0.12)
        A.set_title(f"{s} | {a} | {ch} | a={alpha}"); A.set_xlabel("round"); A.set_ylabel("test acc")
    for j in range(len(cells), nr * nc): ax[j // nc][j % nc].axis("off")
    ax[0][0].legend(); fig.tight_layout(); return _save(fig, fname)


def plot_drift_curves(df, alpha=25, fname="04b_drift_curves.png", variants=None):
    variants = variants or [v for v in ["base", "JEQFL", "M5b", "M4ab", "CDQ", "CDQ-lit"] if v in set(df.variant)]
    cells = df[df.alpha == alpha][["scale", "channel"]].drop_duplicates().sort_values(["scale", "channel"]).values.tolist()
    if not cells: return
    nc = min(3, len(cells)); nr = int(math.ceil(len(cells) / nc))
    fig, ax = plt.subplots(nr, nc, figsize=(4.2 * nc, 2.9 * nr), squeeze=False)
    for i, (s, ch) in enumerate(cells):
        A = ax[i // nc][i % nc]
        for v in variants:
            d = df[(df.scale == s) & (df.channel == ch) & (df.alpha == alpha) & (df.variant == v)]
            if d.empty: continue
            cur = np.array([json.loads(c) for c in d.drift_curve]); k = 5
            sm = np.convolve(cur.mean(0), np.ones(k) / k, mode="valid")
            A.plot(sm, color=col(v), lw=2.2 if v == METHOD else 1.1, label=v)
        A.set_yscale("log"); A.set_title(f"E_drift | {s} | {ch} | a={alpha}"); A.set_xlabel("round")
    for j in range(len(cells), nr * nc): ax[j // nc][j % nc].axis("off")
    ax[0][0].legend(); fig.tight_layout(); return _save(fig, fname)


def plot_bars(df, metric="acc_tail", ylabel=None, fname=None, variants=None):
    if metric not in df.columns or df[metric].notna().sum() == 0: return
    ylabel = ylabel or LAB.get(metric, metric)
    fname = fname or f"05_bars_{metric}.png"
    variants = variants or [v for v in MAIN_V if v in set(df.variant)]
    g = df[df.variant.isin(variants)].groupby(["scale", "arm", "variant"])[metric].agg(["mean", "std", "count"]).reset_index()
    if g.empty: return
    combos = sorted(g[["scale", "arm"]].drop_duplicates().values.tolist(),
                    key=lambda r: (SCORD.index(r[0]) if r[0] in SCORD else 9, r[1]))
    fig, ax = plt.subplots(1, 1, figsize=(max(9, 1.1 * len(combos) * len(variants) / 3), 3.8))
    w = 0.8 / len(variants)
    for j, v in enumerate(variants):
        y, e = [], []
        for s, a in combos:
            t = g[(g.scale == s) & (g.arm == a) & (g.variant == v)]
            y.append(float(t["mean"].values[0]) if len(t) else np.nan)
            e.append(float(t["std"].values[0]) if len(t) else 0.0)
        ax.bar(np.arange(len(combos)) + (j - len(variants) / 2 + 0.5) * w, y, w, yerr=e, color=col(v), label=v,
               capsize=1.5, error_kw=dict(lw=0.6))
    ax.set_xticks(range(len(combos))); ax.set_xticklabels([f"{s}\n{a}" for s, a in combos]); ax.set_ylabel(ylabel)
    lo = np.nanmin(g["mean"]); hi = np.nanmax(g["mean"]); pad = 0.15 * (hi - lo + 1e-9)
    if metric.startswith("acc"): ax.set_ylim(max(0, lo - 3 * pad), hi + 2 * pad)
    if metric == "bad_share": ax.axhline(1 / 3, c="k", ls="--", lw=0.8)
    if metric == "att_ratio": ax.axhline(1.0, c="k", ls="--", lw=0.8)
    hb = HB.get(metric)
    tag = "" if hb is None else ("  (higher = better)" if hb else "  (lower = better)")
    ax.set_title(ylabel + tag)
    ax.legend(ncol=min(len(variants), 9), loc="upper center", bbox_to_anchor=(0.5, 1.17))
    return _save(fig, fname)


def plot_all_metrics(df, variants=None):
    """one grouped-bar figure per numeric column the sweep records."""
    out = []
    for i, (c, hb, lab) in enumerate(NUMCOLS):
        if c not in df.columns or df[c].notna().sum() == 0: continue
        out.append(plot_bars(df, metric=c, ylabel=lab, fname=f"20_{i:02d}_metric_{c}.png", variants=variants))
    return out


def plot_forest(T, metric="accuracy", fname=None):
    if T is None or T.empty: return
    d = T[T.metric == metric].copy()
    if d.empty: return
    fname = fname or f"06_forest_{metric.split()[0]}.png"
    has_arm = "arm" in d.columns; has_ch = "channel" in d.columns
    d["lab"] = d.apply(lambda r: f"{METHOD} - {r.baseline} | {r.scale}"
                                 + (f" | {r.arm}" if has_arm else "")
                                 + (f" | {r.channel}" if has_ch else ""), axis=1)
    d = d.iloc[::-1]
    fig, ax = plt.subplots(figsize=(8.2, 0.26 * len(d) + 1.4))
    ci = 1.96 * d.sd / np.sqrt(d.n_pairs.clip(lower=1))
    cl = [C["green"] if str(v).startswith("GOOD") else (C["verm"] if str(v).startswith("BAD") else C["grey"]) for v in d.verdict]
    ax.errorbar(d.gap, np.arange(len(d)), xerr=ci, fmt="none", ecolor="#999", lw=0.8)
    ax.scatter(d.gap, np.arange(len(d)), c=cl, zorder=3, s=22)
    ax.axvline(0, c="k", lw=0.8); ax.set_yticks(range(len(d))); ax.set_yticklabels(d.lab, fontsize=7)
    ax.set_xlabel(f"paired gap in {metric}  (green = significant improvement, red = significant degradation, BH q<0.05)")
    ax.set_title(f"Paired {metric} gaps, 95% CI  -  method = {METHOD}")
    return _save(fig, fname)


def plot_drift_panel(df, fname="07_client_drift.png", variants=None):
    variants = variants or [v for v in ["base", "JEQFL", "M4ab", "M5b", "CDQ", "CDQ-lit"] if v in set(df.variant)]
    scales = _order(df.scale.unique())
    fig, ax = plt.subplots(1, 4, figsize=(17, 3.4))
    for i, (met, lab, lg) in enumerate([("drift", "E_drift (lower=better)", True),
                                        ("scda", "S_CDA (higher=better)", False),
                                        ("bad_share", "Bad-tier share of effective weight (ideal 1/3)", False)]):
        for j, s in enumerate(scales):
            for k, v in enumerate(variants):
                d = df[(df.scale == s) & (df.variant == v)][met]
                if d.empty: continue
                ax[i].bar(j + (k - len(variants) / 2 + 0.5) * 0.8 / len(variants), d.mean(), 0.8 / len(variants),
                          yerr=d.std(), color=col(v), label=v if j == 0 else None, error_kw=dict(lw=0.6))
        ax[i].set_xticks(range(len(scales))); ax[i].set_xticklabels(scales); ax[i].set_title(lab)
        if lg: ax[i].set_yscale("log")
        if met == "bad_share": ax[i].axhline(1 / 3, c="k", ls="--", lw=0.8)
    ax[0].legend()
    for v in variants:
        d = df[(df.variant == v) & (df.channel == "poor")]
        if d.empty: continue
        cur = np.array([json.loads(c) for c in d.drift_curve]); k = 5
        sm = np.convolve(cur.mean(0), np.ones(k) / k, mode="valid")
        ax[3].plot(sm, color=col(v), lw=2.2 if v == METHOD else 1, label=v)
    ax[3].set_yscale("log"); ax[3].set_title("E_drift over rounds (poor channel, all scales)")
    ax[3].set_xlabel("round"); ax[3].legend()
    fig.tight_layout(); return _save(fig, fname)


def plot_ablation(A, fname="08_ablation.png", title=None):
    if A is None or A.empty: return
    fig, ax = plt.subplots(1, 3, figsize=(14, 3.4))
    scales = _order(A.scale.unique())
    for i, met in enumerate(["accuracy", "client-drift E_drift", "drift alignment S_CDA"]):
        d = A[A.metric == met]
        if d.empty: continue
        rem = sorted(d.removed.unique())
        for j, s in enumerate(scales):
            e = d[d.scale == s].set_index("removed").reindex(rem)
            ax[i].bar(np.arange(len(rem)) + (j - 0.5 * (len(scales) - 1)) * 0.28, e.contribution.values, 0.28, label=s)
        ax[i].set_xticks(range(len(rem))); ax[i].set_xticklabels(["-" + r for r in rem])
        ax[i].axhline(0, c="k", lw=0.8)
        ax[i].set_title(f"{met}: {METHOD} - {METHOD}(without innovation)"); ax[i].legend()
    fig.suptitle(title or ("Ablation (I1 DMapS-FSNR+pinning, I2 R-FD, I3a DR-JPS, I3b Fed-QDrift, I4 FD-SIC).  "
                           "accuracy/S_CDA: >0 means the innovation helps;  E_drift: <0 means it helps"),
                 fontsize=9.5, fontweight="bold")
    fig.tight_layout(); return _save(fig, fname)


def plot_shrinkage(df, fname="11_shrinkage_ablation.png"):
    """the decisive single-scalar ablation: gamma_orph ON (CDQ-lit) vs OFF (CDQ), against base."""
    if SHRINK not in set(df.variant) or METHOD not in set(df.variant): return
    scales = _order(df.scale.unique())
    mets = [("acc_tail", "accuracy (higher=better)"), ("drift", "E_drift (lower=better)"),
            ("scda", "S_CDA (higher=better)"), ("att_ratio", "|g_hat|/|g*| (ideal 1.0)")]
    fig, ax = plt.subplots(1, 4, figsize=(17, 3.5))
    vs = [v for v in ["base", SHRINK, METHOD] if v in set(df.variant)]
    for i, (m, lab) in enumerate(mets):
        if m not in df.columns: continue
        for k, v in enumerate(vs):
            y = [df[(df.scale == s) & (df.variant == v)][m].mean() for s in scales]
            e = [df[(df.scale == s) & (df.variant == v)][m].std() for s in scales]
            ax[i].bar(np.arange(len(scales)) + (k - len(vs) / 2 + 0.5) * 0.8 / len(vs), y, 0.8 / len(vs),
                      yerr=e, color=col(v), label=v if i == 0 else None, error_kw=dict(lw=0.6))
        ax[i].set_xticks(range(len(scales))); ax[i].set_xticklabels(scales); ax[i].set_title(lab)
        if m == "drift": ax[i].set_yscale("log")
        if m == "att_ratio": ax[i].axhline(1.0, c="k", ls="--", lw=0.8)
    ax[0].legend()
    fig.suptitle("Gauss-Markov orphan shrinkage ablation:  CDQ-lit (gamma_orph in Eq.17 and Eq.22)  vs  CDQ (removed)",
                 fontsize=10, fontweight="bold")
    fig.tight_layout(); return _save(fig, fname)


def plot_heatmap(df, base="base", method=None, metric="acc_tail", fname=None):
    method = method or METHOD
    if base not in set(df.variant) or method not in set(df.variant): return
    j = paired(df, method, base, metric)
    if j.empty: return
    fname = fname or f"09_heatmap_{metric}_vs_{base}.png"
    piv = j.groupby(["scale", "arm", "alpha", "channel"])["d"].mean().unstack(["alpha", "channel"])
    piv = piv.reindex(sorted(piv.index, key=lambda r: (SCORD.index(r[0]) if r[0] in SCORD else 9, r[1])))
    fig, ax = plt.subplots(figsize=(1.25 * piv.shape[1] + 2.8, 0.42 * piv.shape[0] + 1.4))
    m = np.nanmax(np.abs(piv.values)) or 1
    cmap = "RdYlGn" if HB.get(metric, True) else "RdYlGn_r"
    im = ax.imshow(piv.values, cmap=cmap, vmin=-m, vmax=m, aspect="auto")
    for (a, b), v in np.ndenumerate(piv.values):
        if np.isfinite(v): ax.text(b, a, "%+.3f" % v, ha="center", va="center", fontsize=7.2)
    ax.set_xticks(range(piv.shape[1])); ax.set_xticklabels([f"a={a}\n{c}" for a, c in piv.columns])
    ax.set_yticks(range(piv.shape[0])); ax.set_yticklabels([f"{s} | {a}" for s, a in piv.index])
    ax.grid(False); plt.colorbar(im, ax=ax, shrink=0.8)
    ax.set_title(f"mean paired gap in {LAB.get(metric, metric)}:  {method} - {base}  per cell")
    return _save(fig, fname)


def plot_trend(df, by="alpha", metric="drift", fname=None, variants=None):
    """metric vs alpha (data heterogeneity) or vs channel (decode probability), per scale."""
    if by not in df.columns or metric not in df.columns: return
    fname = fname or f"12_trend_{metric}_by_{by}.png"
    variants = variants or [v for v in ["base", "JEQFL", "M5b", "CDQ", "CDQ-lit"] if v in set(df.variant)]
    scales = _order(df.scale.unique())
    xs = sorted(df[by].unique(), key=lambda v: {"good": 0, "moderate": 1, "poor": 2}.get(v, v))
    fig, ax = plt.subplots(1, len(scales), figsize=(4.2 * len(scales), 3.1), squeeze=False)
    for i, s in enumerate(scales):
        A = ax[0][i]
        for v in variants:
            y = [df[(df.scale == s) & (df.variant == v) & (df[by] == x)][metric].mean() for x in xs]
            e = [df[(df.scale == s) & (df.variant == v) & (df[by] == x)][metric].sem() for x in xs]
            A.errorbar(range(len(xs)), y, yerr=e, marker="o", color=col(v), lw=2.0 if v == METHOD else 1.1, label=v)
        A.set_xticks(range(len(xs))); A.set_xticklabels([str(x) for x in xs])
        A.set_xlabel(by); A.set_title(f"{s}: {LAB.get(metric, metric)}")
        if metric == "drift": A.set_yscale("log")
    ax[0][0].set_ylabel(LAB.get(metric, metric)); ax[0][0].legend()
    fig.tight_layout(); return _save(fig, fname)


def plot_power(T, fname="13_power.png"):
    d = T[T.metric.isin([m[2] for m in METRICS])].copy()
    d = d[np.isfinite(d.n_80pow)]
    if d.empty: return
    fig, ax = plt.subplots(1, 2, figsize=(13, 3.6))
    d = d.sort_values("n_80pow")
    lab = [f"{r.scale}|{r.baseline}|{r.metric.split()[0]}" for _, r in d.iterrows()]
    cl = [C["green"] if r.n_pairs >= r.n_80pow else C["verm"] for _, r in d.iterrows()]
    ax[0].barh(np.arange(len(d)), d.n_80pow, color=cl, alpha=0.75, label="n required for 80% power")
    ax[0].plot(d.n_pairs, np.arange(len(d)), "k|", ms=10, label="n actually run")
    ax[0].set_yticks(range(len(d))); ax[0].set_yticklabels(lab, fontsize=6.2); ax[0].set_xscale("log")
    ax[0].set_xlabel("paired n"); ax[0].set_title("Power check (green = adequately powered)"); ax[0].legend()
    ax[1].scatter(np.abs(d.gap), d.sd, c=cl, s=22)
    lim = [min(np.abs(d.gap).min(), d.sd.min()) * 0.5 + 1e-6, max(np.abs(d.gap).max(), d.sd.max()) * 2]
    ax[1].plot(lim, lim, "k--", lw=0.8, label="|gap| = paired sd")
    ax[1].set_xscale("log"); ax[1].set_yscale("log"); ax[1].set_xlabel("|observed paired gap|")
    ax[1].set_ylabel("observed paired sd"); ax[1].set_title("Effect size vs paired noise"); ax[1].legend()
    fig.tight_layout(); return _save(fig, fname)


def plot_scatter(df, fname="14_drift_vs_accuracy.png"):
    if "drift" not in df.columns: return
    g = df.groupby(["scale", "arm", "variant"])[["drift", "acc_tail", "scda"]].mean().reset_index()
    fig, ax = plt.subplots(1, 2, figsize=(12, 3.8))
    for v in sorted(g.variant.unique()):
        d = g[g.variant == v]
        ax[0].scatter(d.drift, d.acc_tail, color=col(v), s=26, label=v)
        ax[1].scatter(d.drift, d.scda, color=col(v), s=26)
    ax[0].set_xscale("log"); ax[1].set_xscale("log")
    ax[0].set_xlabel("E_drift"); ax[0].set_ylabel("final accuracy"); ax[0].set_title("drift vs accuracy (cell means)")
    ax[1].set_xlabel("E_drift"); ax[1].set_ylabel("S_CDA"); ax[1].set_title("drift vs alignment (cell means)")
    ax[0].legend(ncol=3, fontsize=6.5); fig.tight_layout(); return _save(fig, fname)


def plot_seed_spread(df, metric="acc_tail", fname="15_seed_spread.png", variants=None):
    variants = variants or [v for v in ["base", "JEQFL", "M5b", "CDQ", "CDQ-lit"] if v in set(df.variant)]
    scales = _order(df.scale.unique())
    fig, ax = plt.subplots(1, len(scales), figsize=(4.0 * len(scales), 3.2), squeeze=False)
    for i, s in enumerate(scales):
        A = ax[0][i]
        data = [df[(df.scale == s) & (df.variant == v)][metric].dropna().values for v in variants]
        bp = A.boxplot([d for d in data if len(d)], labels=[v for v, d in zip(variants, data) if len(d)],
                       patch_artist=True, widths=0.6)
        for patch, v in zip(bp["boxes"], [v for v, d in zip(variants, data) if len(d)]):
            patch.set_facecolor(col(v)); patch.set_alpha(0.55)
        A.set_title(f"{s}: {LAB.get(metric, metric)}"); A.tick_params(axis="x", rotation=35)
    fig.tight_layout(); return _save(fig, fname)


def plot_paired_hist(df, baseline="base", metric="acc_tail", fname="16_paired_differences.png"):
    j = paired(df, METHOD, baseline, metric)
    if j.empty: return
    scales = _order(j.scale.unique())
    fig, ax = plt.subplots(1, len(scales), figsize=(4.0 * len(scales), 3.0), squeeze=False)
    for i, s in enumerate(scales):
        d = j[j.scale == s]["d"].values
        A = ax[0][i]
        A.hist(d, bins=max(8, int(math.sqrt(len(d)))), color=col(METHOD), alpha=0.75)
        A.axvline(0, c="k", lw=1.0); A.axvline(d.mean(), c=C["verm"], lw=1.6, label="mean %+.4f" % d.mean())
        A.set_title(f"{s}: paired {metric} ({METHOD} - {baseline}), n={len(d)}"); A.legend()
    fig.tight_layout(); return _save(fig, fname)


# ================================================================================================ report
def _pr(title, obj, float_fmt="%.4g"):
    print("\n" + title)
    if isinstance(obj, pd.DataFrame):
        if obj.empty: print("  (empty)"); return
        print(obj.to_string(index=False, float_format=lambda x: float_fmt % x))
    else:
        print(obj)


def full_report(df, gates=None):
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 800)
    print("=" * 120)
    print(f"REPORTED METHOD = {METHOD}  (CD-QFed exactly as proposed)   |   SHRINKAGE ABLATION = {SHRINK} "
          f"(same framework, Gauss-Markov orphan shrinkage removed)")
    print("=" * 120)
    print("runs:", len(df), "| scales:", _order(df.scale.unique()), "| arms:", sorted(df.arm.unique()),
          "| alphas:", sorted(df.alpha.unique()), "| channels:", sorted(df.channel.unique()),
          "| seeds:", df.seed.nunique(), "| variants:", sorted(df.variant.unique()))
    print("\nruns per variant:", dict(df.variant.value_counts().sort_index()))

    for i, (c, hb, lab) in enumerate(NUMCOLS):
        if c not in df.columns or df[c].notna().sum() == 0: continue
        pol = "" if hb is None else ("  (higher = better)" if hb else "  (lower = better)")
        print(f"\n[T{i + 1}] MEAN {lab}{pol}  per scale x arm x variant")
        piv = df.pivot_table(index=["scale", "arm"], columns="variant", values=c, aggfunc="mean")
        piv = piv.reindex(sorted(piv.index, key=lambda r: (SCORD.index(r[0]) if r[0] in SCORD else 9, r[1])))
        print(piv.to_string(float_format=lambda x: "%.4g" % x))

    T = comparison_table(df, by=("scale",))
    Ta = comparison_table(df, by=("scale", "arm"), baselines=["base", "JEQFL", SHRINK])
    Tc = comparison_table(df, by=("scale", "channel"), baselines=["base", "JEQFL", SHRINK])
    Tal = comparison_table(df, by=("scale", "alpha"), baselines=["base", "JEQFL"])
    Tall = comparison_table(df, by=("scale",), metrics=METRICS_EXT)
    Tshr = shrinkage_table(df)
    Tcdq = comparison_table(df, method=SHRINK, baselines=["base", "JEQFL"], by=("scale",))
    Abl = ablation_table(df, method=METHOD)
    AblC = ablation_table(df, method=SHRINK)
    cols = ["scale", "arm", "channel", "alpha", "baseline", "metric", "n_pairs", "mean_method", "mean_baseline",
            "gap", "rel_change_pct", "sd", "t", "p", "p_wilcoxon", "q_BH", "n_80pow", "verdict"]

    def sub(t): return t[[c for c in cols if c in t.columns]] if t is not None and not t.empty else t

    _pr(f"[C1] PAIRED COMPARISON  {METHOD} vs every baseline, pooled per scale (pairs = cells x seeds, common random numbers)", sub(T))
    _pr(f"[C2] PAIRED COMPARISON per scale x arm", sub(Ta))
    _pr(f"[C3] PAIRED COMPARISON per scale x channel  (tests the Lemma-3 (1-p)/p channel scaling)", sub(Tc))
    _pr(f"[C4] PAIRED COMPARISON per scale x alpha  (tests whether the effect is data-heterogeneity driven)", sub(Tal))
    _pr(f"[C5] PAIRED COMPARISON on the diagnostic metrics (reconstruction error, participation, |g|/|g*|, Bad-tier share)", sub(Tall))
    _pr(f"[C6] SHRINKAGE ABLATION  {METHOD} (gamma_orph ON) vs {SHRINK} (gamma_orph REMOVED)", sub(Tshr))
    _pr(f"[C7] {SHRINK} vs base/JEQFL  -  the un-shrunk variant evaluated on its own", sub(Tcdq))
    _pr(f"[C8] PER-INNOVATION ABLATION anchored on {METHOD}  (contribution = {METHOD} minus {METHOD}-without-it)", Abl)
    _pr(f"[C9] PER-INNOVATION ABLATION anchored on {SHRINK}", AblC)

    P = power_table(T)
    _pr("[C10] POWER: observed paired effect, observed paired sd, and n required for 80% power (alpha=0.05, two-sided)", P)
    print("\n[C11] DIAGNOSTICS per scale x channel x variant")
    dcols = [c for c in ["active_mean", "bad_share", "att_ratio", "rec_err", "mismatch", "gamma_orph", "eps_mean", "eps_bad"] if c in df.columns]
    print(df.groupby(["scale", "channel", "variant"])[dcols].mean().round(4).to_string())

    for f, t in (("cdqfed_comparison.csv", T), ("cdqfed_comparison_arm.csv", Ta), ("cdqfed_comparison_channel.csv", Tc),
                 ("cdqfed_comparison_alpha.csv", Tal), ("cdqfed_comparison_diagnostics.csv", Tall),
                 ("cdqfed_shrinkage_ablation.csv", Tshr), ("cdqfed_cdq_vs_base.csv", Tcdq),
                 ("cdqfed_ablation_lit.csv", Abl), ("cdqfed_ablation_cdq.csv", AblC), ("cdqfed_power.csv", P)):
        if t is not None and not t.empty: t.to_csv(f, index=False)

    # ---------------------------------------------------------------------------------------- figures
    print("\n" + "=" * 120); print("FIGURES"); print("=" * 120)
    if gates: plot_gates(gates)
    for al in sorted(df.alpha.unique()):
        plot_curves(df, alpha=al, fname=f"04_accuracy_curves_alpha{al}.png")
        plot_drift_curves(df, alpha=al, fname=f"04b_drift_curves_alpha{al}.png")
    plot_all_metrics(df)
    plot_drift_panel(df)
    for met in ["accuracy", "client-drift E_drift", "drift alignment S_CDA"]:
        plot_forest(T, metric=met, fname=f"06_forest_{met.split()[0].lower()}.png")
        plot_forest(Ta, metric=met, fname=f"06b_forest_arm_{met.split()[0].lower()}.png")
        plot_forest(Tc, metric=met, fname=f"06c_forest_channel_{met.split()[0].lower()}.png")
    plot_ablation(Abl, fname="08_ablation_lit.png")
    plot_ablation(AblC, fname="08b_ablation_cdq.png",
                  title=f"Ablation anchored on {SHRINK} (shrinkage removed) - shown for completeness")
    plot_shrinkage(df)
    for met in ["acc_tail", "drift", "scda"]:
        plot_heatmap(df, base="base", metric=met, fname=f"09_heatmap_{met}_vs_base.png")
        plot_heatmap(df, base="JEQFL", metric=met, fname=f"09b_heatmap_{met}_vs_JEQFL.png")
    for met in ["acc_tail", "drift", "scda", "active_mean", "rec_err"]:
        plot_trend(df, by="channel", metric=met, fname=f"12_trend_{met}_by_channel.png")
        if df.alpha.nunique() > 1:
            plot_trend(df, by="alpha", metric=met, fname=f"12b_trend_{met}_by_alpha.png")
    plot_power(T)
    plot_scatter(df)
    for met in ["acc_tail", "drift", "scda"]:
        plot_seed_spread(df, metric=met, fname=f"15_seed_spread_{met}.png")
        plot_paired_hist(df, metric=met, fname=f"16_paired_diff_{met}.png")
    return dict(T=T, Ta=Ta, Tc=Tc, Tal=Tal, Tall=Tall, Tshr=Tshr, Tcdq=Tcdq, A=Abl, Acdq=AblC, P=P)


def final_summary(R):
    T = R["T"]
    print("=" * 120)
    print(f"FINAL VERDICT   method = {METHOD}  (CD-QFed as proposed).  GOOD = significant improvement at BH q<0.05; "
          f"'trend' = right sign but not significant")
    print("=" * 120)
    for met in ["accuracy", "client-drift E_drift", "drift alignment S_CDA"]:
        d = T[T.metric == met]
        if d.empty: continue
        print(f"\n-- {met} --")
        for _, r in d.sort_values(["baseline", "scale"]).iterrows():
            print(f"  {r.scale:6s} vs {r.baseline:8s}: method {r.mean_method:.4g}  baseline {r.mean_baseline:.4g}  "
                  f"gap {r.gap:+.4g} ({r.rel_change_pct:+.1f}%)  n={r.n_pairs}  p={r.p:.3g}  q={r.q_BH:.3g}  -> {r.verdict}")
    Tshr = R.get("Tshr")
    if Tshr is not None and not Tshr.empty:
        print("\n" + "=" * 120)
        print(f"SHRINKAGE ABLATION   {METHOD} (gamma_orph in Eq.17 + Eq.22)  vs  {SHRINK} (shrinkage removed)")
        print("=" * 120)
        for _, r in Tshr.sort_values(["metric", "scale"]).iterrows():
            print(f"  {r.scale:6s} {r.metric:22s}: {SHRINK} {r.mean_baseline:.4g} -> {METHOD} {r.mean_method:.4g}  "
                  f"({r.rel_change_pct:+.1f}%)  n={r.n_pairs}  q={r.q_BH:.3g}  -> {r.verdict}")
    A = R.get("A")
    if A is not None and not A.empty:
        print("\n" + "=" * 120)
        print(f"PER-INNOVATION ABLATION anchored on {METHOD}  (positive = innovation helps for accuracy/S_CDA, "
              f"negative = helps for E_drift)")
        print("=" * 120)
        for _, r in A.sort_values(["metric", "scale", "removed"]).iterrows():
            print(f"  {r.scale:6s} remove {r.removed:5s} {r.metric:22s}: {r.ablated:.4g} -> {r.full:.4g}  "
                  f"contribution {r.contribution:+.4g}  n={r.n_pairs}  q={r.q_BH:.3g}  {r.innovation_helps}")
    P = R.get("P")
    if P is not None and not P.empty:
        under = P[(P.n_pairs < P.n_80pow) & np.isfinite(P.n_80pow)]
        print("\n" + "=" * 120)
        print("POWER STATEMENT")
        print("=" * 120)
        print(f"  comparisons run: {len(P)} | adequately powered at 80%: {len(P) - len(under)} | underpowered: {len(under)}")
        for _, r in under.sort_values("n_80pow", ascending=False).head(12).iterrows():
            print(f"  underpowered: {r.scale:6s} vs {r.baseline:8s} {r.metric:22s}  gap {r.gap:+.4g}  sd {r.sd:.4g}  "
                  f"n={r.n_pairs}  needs n>={int(r.n_80pow)}")
    print("=" * 120)


# ================================================================================================ weight matrices
N_CLIENTS = 12
TIERN = ["Good"] * 4 + ["Medium"] * 4 + ["Bad"] * 4
CLAB = [f"c{n + 1:02d}{TIERN[n][0]}" for n in range(N_CLIENTS)]
VEC_COLS = [
    ("w_static",        "W1  static precision weight w_n            (Eq. 21, mean-normalised, clamp 4x)"),
    ("w_eff_mean",      "W2  EFFECTIVE aggregation weight           (mean over rounds; IDEAL = 1.000 for every client)"),
    ("w_eff_early",     "W3  effective aggregation weight           (first third of the rounds)"),
    ("w_eff_late",      "W4  effective aggregation weight           (last third = steady state)"),
    ("w_innov_mean",    "W5  innovation weight pi_{n,k}             (Eq. 22, applied to the zero-mean innovation only)"),
    ("p_dec_mean",      "W6  realised SIC decode probability p_dec  (Eq. 24; fleet mean is held at the channel value)"),
    ("eps_client",      "W7  compiled infidelity eps_n              (Concept 1 tier x Concept 2 chips x DMapS counts)"),
    ("signal_client",   "W8  hardware attenuation e^{-eps_n}        (what R-FD has to undo)"),
    ("kappa_client",    "W9  MMSE deconvolution gain kappa*_n       (Eq. 10; 1.0 when R-FD is off)"),
    ("sig2_dec_client", "W10 deconvolved variance sigma~^2_n * M    (Eq. 13; the spread the weights can finally see)"),
    ("mem_norm",        "W11 drift-memory norm ||m_n||              (Eq. 19; 0 when Fed-QDrift is off)"),
]


def _vec(x, n=None):
    if not isinstance(x, str): return None
    try: v = np.asarray(json.loads(x), float)
    except Exception: return None
    if n is not None and len(v) != n: return None
    return v


def weight_matrix(df, quantity, by=("scale", "variant"), n=N_CLIENTS):
    """mean per-client vector for every (scale, variant) -> a printable matrix."""
    if quantity not in df.columns: return pd.DataFrame()
    out = {}
    for key, g in df.groupby(list(by), dropna=False):
        key = key if isinstance(key, tuple) else (key,)
        vs = [v for v in (_vec(x, n) for x in g[quantity]) if v is not None]
        if vs: out["|".join(map(str, key))] = np.mean(vs, axis=0)
    if not out: return pd.DataFrame()
    M = pd.DataFrame(out, index=CLAB[:n] if n == N_CLIENTS else list(range(n))).T
    return M.reindex(sorted(M.index, key=lambda r: (SCORD.index(r.split("|")[0]) if r.split("|")[0] in SCORD else 9,
                                                    r.split("|")[-1])))


def print_weight_tables(df, variants=None):
    variants = variants or [v for v in MAIN_V if v in set(df.variant)]
    d = df[df.variant.isin(variants)]
    print("=" * 130)
    print("WEIGHT MATRICES OF THE TRAINING  -  one row per (scale | variant), one column per client "
          "(c01-c04 Good, c05-c08 Medium, c09-c12 Bad)")
    print("=" * 130)
    for q, lab in VEC_COLS:
        M = weight_matrix(d, q)
        if M.empty: continue
        print(f"\n{lab}")
        print(M.to_string(float_format=lambda x: "%8.4f" % x))
        if q.startswith("w_eff") or q == "w_static":      # these are mean-normalised, so tier shares are meaningful
            T = pd.DataFrame({"Good": M.iloc[:, :4].sum(1) / N_CLIENTS,
                              "Medium": M.iloc[:, 4:8].sum(1) / N_CLIENTS,
                              "Bad": M.iloc[:, 8:].sum(1) / N_CLIENTS})
            T["max|share-1/3|"] = (T - 1 / 3).abs().max(1)
            print("   tier shares (ideal 0.3333 each):")
            print(T.to_string(float_format=lambda x: "%8.4f" % x))
            if q == "w_eff_mean":
                print("   NOTE on reading W2-W4.  For the anchored estimator (Eq. 20) the effective weight is")
                print("        [1/N full-fleet anchor, exactly 1/3 per tier by construction, no client deletable]")
                print("        + [precision-weighted ZERO-MEAN innovation g_hat - m].  A tier tilt in this table")
                print("        therefore sits on a zero-mean term and does NOT move the stationary objective.")
                print("        In M4a the same tilt sits on the gradient itself, which is what deletes rare classes.")
                print("        Compare W1 (M4a: tilt on the objective) with W5 (CD-QFed: tilt on the innovation only).")
    # trained QNN parameter matrix
    if "theta_final" in df.columns:
        print("\nW12 TRAINED QNN PARAMETER MATRIX theta (L x q), mean over seeds/cells")
        for (sc, v), g in d.groupby(["scale", "variant"]):
            sh = _vec(g.theta_shape.iloc[0]) if "theta_shape" in g.columns else None
            vs = [_vec(x) for x in g.theta_final]
            vs = [x for x in vs if x is not None]
            if not vs or sh is None: continue
            L, qq = int(sh[0]), int(sh[1])
            th = np.mean(vs, axis=0).reshape(L, qq)
            print(f"\n  {sc} | {v}   theta shape = {L} x {qq}   |theta|_F = {np.linalg.norm(th):.4f}")
            print(pd.DataFrame(th, index=[f"layer{i + 1}" for i in range(L)],
                               columns=[f"q{j + 1:02d}" for j in range(qq)]).to_string(float_format=lambda x: "%7.4f" % x))
    for q, _ in VEC_COLS:
        M = weight_matrix(d, q)
        if not M.empty: M.to_csv(f"cdqfed_weights_{q}.csv")
    print("\n(weight matrices also written to cdqfed_weights_*.csv)")


def plot_weight_heatmaps(df, variants=None):
    variants = variants or [v for v in MAIN_V if v in set(df.variant)]
    d = df[df.variant.isin(variants)]
    outs = []
    for i, (q, lab) in enumerate(VEC_COLS):
        M = weight_matrix(d, q)
        if M.empty: continue
        fig, ax = plt.subplots(figsize=(0.62 * M.shape[1] + 4.2, 0.30 * M.shape[0] + 1.6))
        centred = q.startswith("w_eff") or q in ("w_static", "w_innov_mean")
        if centred:
            m = np.nanmax(np.abs(M.values - 1.0)) or 1
            im = ax.imshow(M.values, cmap="RdBu_r", vmin=1 - m, vmax=1 + m, aspect="auto")
        else:
            im = ax.imshow(M.values, cmap="viridis", aspect="auto")
        for (a, b), vv in np.ndenumerate(M.values):
            if np.isfinite(vv):
                ax.text(b, a, ("%.2f" % vv) if abs(vv) >= 0.01 else "%.0e" % vv, ha="center", va="center", fontsize=6)
        ax.set_xticks(range(M.shape[1])); ax.set_xticklabels(M.columns, rotation=90, fontsize=6.5)
        ax.set_yticks(range(M.shape[0])); ax.set_yticklabels(M.index, fontsize=6.5)
        for x in (3.5, 7.5): ax.axvline(x, color="k", lw=0.8)
        ax.grid(False); plt.colorbar(im, ax=ax, shrink=0.75)
        ax.set_title(lab, fontsize=8.5)
        outs.append(_save(fig, f"30_{i:02d}_weights_{q}.png"))
    # tier-share summary
    M = weight_matrix(d, "w_eff_late")
    if not M.empty:
        fig, ax = plt.subplots(figsize=(max(8, 0.42 * len(M)), 3.6))
        bot = np.zeros(len(M))
        for j, (tn, cc) in enumerate(TCOL.items()):
            sl = slice(0, 4) if j == 0 else (slice(4, 8) if j == 1 else slice(8, 12))
            y = M.iloc[:, sl].sum(1).values / N_CLIENTS
            ax.bar(np.arange(len(M)), y, 0.75, bottom=bot, color=cc, label=tn); bot += y
        ax.axhline(1 / 3, c="k", ls="--", lw=0.9); ax.axhline(2 / 3, c="k", ls="--", lw=0.9)
        ax.set_xticks(range(len(M))); ax.set_xticklabels(M.index, rotation=90, fontsize=6.5)
        ax.set_ylabel("share of effective aggregation weight")
        ax.set_title("Steady-state tier share of the aggregation weight (dashed = the 1/3 : 1/3 : 1/3 ideal)")
        ax.legend(ncol=3); outs.append(_save(fig, "31_weight_tier_share.png"))
    return outs


def plot_theta(df, variants=None):
    if "theta_final" not in df.columns: return
    variants = variants or [v for v in ["base", SHRINK, METHOD] if v in set(df.variant)]
    scales = _order(df.scale.unique())
    fig, ax = plt.subplots(len(scales), len(variants), figsize=(4.4 * len(variants), 1.9 * len(scales)), squeeze=False)
    for i, s in enumerate(scales):
        for j, v in enumerate(variants):
            g = df[(df.scale == s) & (df.variant == v)]
            A_ = ax[i][j]; A_.grid(False)
            sh = _vec(g.theta_shape.iloc[0]) if len(g) and "theta_shape" in g.columns else None
            vs = [x for x in (_vec(y) for y in g.theta_final) if x is not None] if len(g) else []
            if not vs or sh is None: A_.axis("off"); continue
            th = np.mean(vs, axis=0).reshape(int(sh[0]), int(sh[1]))
            m = np.nanmax(np.abs(th)) or 1
            im = A_.imshow(th, cmap="RdBu_r", vmin=-m, vmax=m, aspect="auto")
            A_.set_title(f"{s} | {v} | |theta|={np.linalg.norm(th):.3f}", fontsize=8)
            A_.set_xlabel("qubit"); A_.set_ylabel("layer"); plt.colorbar(im, ax=A_, shrink=0.8)
    fig.suptitle("W12  trained QNN parameter matrix theta (L x q), averaged over seeds and cells",
                 fontsize=10, fontweight="bold")
    fig.tight_layout(); return _save(fig, "32_theta_matrix.png")


def print_full_weights(row, max_rounds=60):
    """full per-round weight matrix of ONE training run (needs log_weights=True)."""
    tag = f"{row['scale']} | {row['arm']} | a={row['alpha']} | {row['channel']} | seed {row['seed']} | {row['variant']}"
    print("\n" + "=" * 130)
    print("FULL WEIGHT MATRIX OF ONE TRAINING RUN:  " + tag)
    print("=" * 130)
    W = np.asarray(json.loads(row["w_eff_matrix"]), float)
    PD = np.asarray(json.loads(row["p_dec_matrix"]), float)
    print(f"\nW_eff  (rounds x clients, ideal 1.0 everywhere)   shape = {W.shape}")
    T = pd.DataFrame(W, index=[f"r{t + 1:03d}" for t in range(len(W))], columns=CLAB)
    T["Good"] = T.iloc[:, :4].sum(1) / N_CLIENTS
    T["Med"] = T.iloc[:, 4:8].sum(1) / N_CLIENTS
    T["Bad"] = T.iloc[:, 8:12].sum(1) / N_CLIENTS
    print(T.to_string(float_format=lambda x: "%7.4f" % x) if len(T) <= max_rounds
          else pd.concat([T.head(10), T.tail(10)]).to_string(float_format=lambda x: "%7.4f" % x))
    print("\n  column mean   :", np.round(W.mean(0), 4).tolist())
    print("  column sd     :", np.round(W.std(0), 4).tolist())
    print("  max |w-1|     : %.4f   tier shares (G/M/B): %s" %
          (np.abs(W.mean(0) - 1).max(), np.round([W.mean(0)[:4].sum() / 12, W.mean(0)[4:8].sum() / 12,
                                                  W.mean(0)[8:].sum() / 12], 4).tolist()))
    print(f"\np_dec  (rounds x clients, Eq. 24)   mean per client: {np.round(PD.mean(0), 4).tolist()}")
    print(f"       fleet mean = {PD.mean():.4f}  (must equal the channel budget)")
    if "mem_matrix" in row and isinstance(row["mem_matrix"], str):
        M = np.asarray(json.loads(row["mem_matrix"]), float)
        print(f"\nFed-QDrift memory m_n  (12 x P = {M.shape}), per-client norm:")
        print(pd.DataFrame({"||m_n||": np.linalg.norm(M, axis=1)}, index=CLAB).T.to_string(float_format=lambda x: "%8.5f" % x))
    sh = _vec(row.get("theta_shape")) if isinstance(row.get("theta_shape"), str) else None
    th = _vec(row.get("theta_final"))
    if sh is not None and th is not None:
        th = th.reshape(int(sh[0]), int(sh[1]))
        print(f"\ntrained theta ({int(sh[0])} x {int(sh[1])}), |theta|_F = {np.linalg.norm(th):.4f}")
        print(pd.DataFrame(th, index=[f"layer{i + 1}" for i in range(th.shape[0])],
                           columns=[f"q{j + 1:02d}" for j in range(th.shape[1])]).to_string(float_format=lambda x: "%7.4f" % x))


def plot_weight_matrix_runs(rows, fname="33_weight_matrix_runs.png"):
    rows = [r for r in rows if isinstance(r.get("w_eff_matrix"), str)]
    if not rows: return
    fig, ax = plt.subplots(len(rows), 3, figsize=(15, 2.5 * len(rows)), squeeze=False)
    for i, r in enumerate(rows):
        W = np.asarray(json.loads(r["w_eff_matrix"]), float)
        PD = np.asarray(json.loads(r["p_dec_matrix"]), float)
        tag = f"{r['scale']} | {r['variant']} | {r['arm']} | {r['channel']}"
        m = np.nanmax(np.abs(W - 1)) or 1
        im = ax[i][0].imshow(W.T, cmap="RdBu_r", vmin=1 - m, vmax=1 + m, aspect="auto")
        ax[i][0].set_yticks(range(N_CLIENTS)); ax[i][0].set_yticklabels(CLAB, fontsize=5.5)
        ax[i][0].set_xlabel("round"); ax[i][0].grid(False)
        ax[i][0].set_title(f"W_eff  {tag}", fontsize=8); plt.colorbar(im, ax=ax[i][0], shrink=0.8)
        for j, (sl, tn) in enumerate([(slice(0, 4), "Good"), (slice(4, 8), "Medium"), (slice(8, 12), "Bad")]):
            ax[i][1].plot(W[:, sl].sum(1) / N_CLIENTS, color=TCOL[tn], label=tn)
        ax[i][1].axhline(1 / 3, c="k", ls="--", lw=0.8); ax[i][1].set_xlabel("round")
        ax[i][1].set_ylabel("tier share"); ax[i][1].set_title(f"tier share of weight  {tag}", fontsize=8)
        if i == 0: ax[i][1].legend()
        im2 = ax[i][2].imshow(PD.T, cmap="viridis", aspect="auto")
        ax[i][2].set_yticks(range(N_CLIENTS)); ax[i][2].set_yticklabels(CLAB, fontsize=5.5)
        ax[i][2].set_xlabel("round"); ax[i][2].grid(False)
        ax[i][2].set_title(f"p_dec (Eq. 24)  {tag}", fontsize=8); plt.colorbar(im2, ax=ax[i][2], shrink=0.8)
    fig.tight_layout(); return _save(fig, fname)


def plot_mem_matrix(rows, fname="34_drift_memory_matrix.png"):
    rows = [r for r in rows if isinstance(r.get("mem_matrix"), str)]
    if not rows: return
    fig, ax = plt.subplots(1, len(rows), figsize=(4.0 * len(rows), 3.2), squeeze=False)
    for i, r in enumerate(rows):
        M = np.asarray(json.loads(r["mem_matrix"]), float)
        m = np.nanmax(np.abs(M)) or 1
        im = ax[0][i].imshow(M, cmap="RdBu_r", vmin=-m, vmax=m, aspect="auto")
        ax[0][i].set_yticks(range(M.shape[0])); ax[0][i].set_yticklabels(CLAB, fontsize=5.5)
        ax[0][i].set_xlabel("parameter k"); ax[0][i].grid(False)
        ax[0][i].set_title(f"m_n  {r['scale']} | {r['variant']}", fontsize=8)
        plt.colorbar(im, ax=ax[0][i], shrink=0.8)
    fig.suptitle("Eq. (19) Fed-QDrift per-client gradient memory matrix (12 x P)", fontsize=10, fontweight="bold")
    fig.tight_layout(); return _save(fig, fname)


def weight_report(df, showcase_rows=None, variants=None):
    print_weight_tables(df, variants=variants)
    plot_weight_heatmaps(df, variants=variants)
    plot_theta(df, variants=variants)
    if showcase_rows:
        for r in showcase_rows: print_full_weights(r)
        plot_weight_matrix_runs(showcase_rows)
        plot_mem_matrix([r for r in showcase_rows if r.get("variant") in (METHOD, SHRINK)])


# ================================================================================================ per-epoch weight matrices
def epoch_weight_matrix(df, scale, variant, alpha=None, channel=None, arm=None, quantity="w_every_matrix"):
    """mean weight matrix (snapshot rounds x 12 clients) for one (scale, variant[, alpha, channel, arm]) cell."""
    if quantity not in df.columns: return pd.DataFrame()
    g = df[(df.scale == scale) & (df.variant == variant)]
    if alpha is not None: g = g[g.alpha == alpha]
    if channel is not None: g = g[g.channel == channel]
    if arm is not None: g = g[g.arm == arm]
    mats, rnds = [], None
    for _, r in g.iterrows():
        if not isinstance(r[quantity], str): continue
        try: M = np.asarray(json.loads(r[quantity]), float)
        except Exception: continue
        if M.ndim != 2 or M.shape[1] != N_CLIENTS: continue
        mats.append(M)
        if rnds is None and isinstance(r.get("w_every_rounds"), str):
            try: rnds = json.loads(r["w_every_rounds"])
            except Exception: pass
    if not mats: return pd.DataFrame()
    L = min(len(m) for m in mats)
    M = np.mean([m[:L] for m in mats], axis=0)
    idx = [f"r{int(x):03d}" for x in (rnds[:L] if rnds else range(1, L + 1))]
    T = pd.DataFrame(M, index=idx, columns=CLAB)
    T["Good"] = T.iloc[:, :4].sum(1) / N_CLIENTS
    T["Med"] = T.iloc[:, 4:8].sum(1) / N_CLIENTS
    T["Bad"] = T.iloc[:, 8:12].sum(1) / N_CLIENTS
    return T


def print_epoch_weight_tables(df, variants=None, alphas=None, every_label=5):
    """THE per-5-epoch weight matrix of all 12 clients, for every scale x alpha x variant."""
    if "w_every_matrix" not in df.columns:
        print("(no per-epoch weight snapshots in this results file - re-run the sweep with the patched simulator)"); return
    variants = variants or [v for v in MAIN_V if v in set(df.variant)]
    alphas = alphas if alphas is not None else sorted(df.alpha.unique())
    ev = int(df.weight_every.dropna().iloc[0]) if "weight_every" in df.columns and df.weight_every.notna().any() else every_label
    print("=" * 140)
    print(f"PER-EPOCH WEIGHT MATRIX  -  effective aggregation weight of all {N_CLIENTS} clients, snapshotted every {ev} rounds")
    print(f"rows = round block (mean over the {ev} rounds ending there) | columns = clients "
          f"(c01-c04 Good, c05-c08 Medium, c09-c12 Bad) | IDEAL = 1.0000 everywhere, tier shares 0.3333 each")
    print("=" * 140)
    n = 0
    for s in _order(df.scale.unique()):
        for al in alphas:
            for v in variants:
                T = epoch_weight_matrix(df, s, v, alpha=al)
                if T.empty: continue
                n += 1
                print(f"\n--- scale={s} | alpha={al} | variant={v}  (mean over arms, channels and seeds) ---")
                print(T.to_string(float_format=lambda x: "%8.4f" % x))
                w = T[CLAB].values
                print("    mean |w-1| over the run = %.4f  |  steady-state tier share G/M/B = %.4f / %.4f / %.4f"
                      % (np.abs(w - 1).mean(), T["Good"].iloc[-1], T["Med"].iloc[-1], T["Bad"].iloc[-1]))
                T.to_csv(f"cdqfed_epoch_weights_{s}_a{al}_{v}.csv")
    print(f"\n({n} per-epoch weight matrices printed and written to cdqfed_epoch_weights_*.csv)")


def plot_epoch_weights(df, variants=None, alphas=None):
    """one heatmap grid per scale: snapshot rounds x 12 clients, for each alpha and variant."""
    if "w_every_matrix" not in df.columns: return
    variants = variants or [v for v in ["base", "JEQFL", "M4ab", "M5b", SHRINK, METHOD] if v in set(df.variant)]
    alphas = alphas if alphas is not None else sorted(df.alpha.unique())
    outs = []
    for s in _order(df.scale.unique()):
        cells = [(al, v) for al in alphas for v in variants if not epoch_weight_matrix(df, s, v, alpha=al).empty]
        if not cells: continue
        nc = len(variants); nr = int(math.ceil(len(cells) / nc))
        fig, ax = plt.subplots(nr, nc, figsize=(3.1 * nc, 2.5 * nr), squeeze=False)
        for i, (al, v) in enumerate(cells):
            T = epoch_weight_matrix(df, s, v, alpha=al)
            A_ = ax[i // nc][i % nc]; A_.grid(False)
            M = T[CLAB].values
            m = np.nanmax(np.abs(M - 1)) or 1
            im = A_.imshow(M.T, cmap="RdBu_r", vmin=1 - m, vmax=1 + m, aspect="auto")
            A_.set_yticks(range(N_CLIENTS)); A_.set_yticklabels(CLAB, fontsize=5)
            A_.set_xticks(range(len(T))); A_.set_xticklabels([x[1:] for x in T.index], fontsize=5, rotation=90)
            A_.set_xlabel("round"); A_.set_title(f"{s} | a={al} | {v}", fontsize=7.5)
            plt.colorbar(im, ax=A_, shrink=0.8)
        for j in range(len(cells), nr * nc): ax[j // nc][j % nc].axis("off")
        fig.suptitle(f"Per-epoch effective aggregation weight, {s} scale  (blue = under-weighted, red = over-weighted, "
                     f"white = the ideal 1.0)", fontsize=10, fontweight="bold")
        fig.tight_layout(); outs.append(_save(fig, f"35_epoch_weights_{s}.png"))

        # tier share over rounds, per alpha
        fig, ax = plt.subplots(1, len(alphas), figsize=(4.2 * len(alphas), 3.1), squeeze=False)
        for i, al in enumerate(alphas):
            A_ = ax[0][i]
            for v in variants:
                T = epoch_weight_matrix(df, s, v, alpha=al)
                if T.empty: continue
                A_.plot(T["Bad"].values, color=col(v), lw=2.0 if v == METHOD else 1.1, label=v)
            A_.axhline(1 / 3, c="k", ls="--", lw=0.9)
            A_.set_xlabel(f"snapshot block"); A_.set_ylabel("Bad-tier share of weight")
            A_.set_title(f"{s} | alpha={al}", fontsize=8.5)
        ax[0][0].legend(fontsize=6.5)
        fig.suptitle(f"Bad-tier share of the aggregation weight over training, {s} scale (dashed = ideal 1/3)",
                     fontsize=10, fontweight="bold")
        fig.tight_layout(); outs.append(_save(fig, f"36_epoch_tier_share_{s}.png"))
    return outs


def print_epoch_weights_run(row):
    """the per-epoch weight matrix of ONE training run, printed in full."""
    try:
        M = np.asarray(json.loads(row["w_every_matrix"]), float)
        rn = json.loads(row["w_every_rounds"])
    except Exception:
        return
    tag = f"{row['scale']} | {row['arm']} | a={row['alpha']} | {row['channel']} | seed {row['seed']} | {row['variant']}"
    print(f"\n  per-epoch weight matrix (every {row.get('weight_every', 5)} rounds): {tag}")
    T = pd.DataFrame(M, index=[f"r{int(x):03d}" for x in rn[:len(M)]], columns=CLAB)
    T["Good"] = T.iloc[:, :4].sum(1) / N_CLIENTS
    T["Med"] = T.iloc[:, 4:8].sum(1) / N_CLIENTS
    T["Bad"] = T.iloc[:, 8:12].sum(1) / N_CLIENTS
    print(T.to_string(float_format=lambda x: "%8.4f" % x))
