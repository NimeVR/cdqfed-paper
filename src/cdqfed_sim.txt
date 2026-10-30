"""
CD-QFed : Compilation-Deconvolved & Dual-Drift-Controlled Quantum Federated Learning
          (simulator, baselines, theory checks, gates)

Physical / experimental set-up is identical to the v2 pipeline (notebookd98a7bfd44):
  * 12 clients; Concept 1 client tiers tau_client = [1]*4 + [3]*4 + [10]*4  (Good / Medium / Bad)
  * Concept 2 chip tiers inside each client: small [1,1,3,10,10], medium [1,1,3,3,10,10], large [1,1,3,10,10]
  * full-width DMapS compile counts (S_local per chip, E_link per chip pair) -> eps_total per client (Step-4 analytic model)
  * proxy QNN  q = 10 / 12 / 15 qubits, L = 3 RY layers + CZ ring, Pauli-Z readout on 4 qubits -> softmax (4 FMNIST classes)
  * Joint-EQFL joint parameter-shift rule (Eq. 15-17 of Chung et al.) over a lossy SIC uplink, p_dec good/moderate/poor = .82/.63/.31
  * keyed RNG rng_for(seed, round, client, purpose) -> common random numbers between every method and its baseline

Methods (VARIANTS):
  base        Joint EQFL joint P-S estimator (M5a two-subset form), uniform weights          [baseline, Chung et al. Eq. 15-17 / 32]
  JEQFL       Joint EQFL + divergence DP clustering (LC/RC) + SIC shift ordering              [baseline, full Chung et al. method]
  M4a/M4ab/M5b/M3/M2                                                                          [v2 mechanisms, kept as baselines]
  CDQ-lit     CD-QFed AS PROPOSED (Eqs. 16-22 literal: Eq.16 control variate + Gauss-Markov orphan shrinkage in Eq.17 and Eq.22)
  CDQ         the same framework WITHOUT the Gauss-Markov orphan shrinkage  [shrinkage ablation]
  CDQ-noI1 / -noI2 / -noI3a / -noI3b / -noI4                                                [ablations: one innovation removed each]
All hardware error rates are [PLACEHOLDER]; accuracies are PROXY numbers.
"""
import os, json, math, time, hashlib, gzip, pickle, glob, urllib.request
import numpy as np
from scipy.optimize import brentq

try:
    import torch
    HAVE_TORCH = True
    torch.backends.cuda.matmul.allow_tf32 = False
    DEV = "cuda" if torch.cuda.is_available() else "cpu"
except Exception:
    HAVE_TORCH, DEV = False, "cpu"
USE_TORCH = HAVE_TORCH and DEV == "cuda"      # GPU -> torch kernels; CPU -> numpy (measured faster than torch-CPU at these shapes)


class SessionTimeUp(Exception):
    """raised inside run_one when the Kaggle session budget is reached; the run's round-level checkpoint has
    already been written, so the next session continues it at exactly that round."""


def backend_report():
    print("torch installed:", HAVE_TORCH, "| cuda available:", HAVE_TORCH and torch.cuda.is_available())
    if USE_TORCH: print("GPU:", torch.cuda.get_device_name(0), "| statevector backend = torch/cuda (float32, TF32 off)")
    else: print("statevector backend = numpy (CPU).  On Kaggle: Settings > Accelerator > GPU, then Run All.")
    return DEV


# ----------------------------------------------------------------------------------------------- constants (same as v2)
P1_BASE, P2_BASE, PR_BASE = 1e-4, 5e-3, 6e-2        # [PLACEHOLDER - needs real device calibration]
M_SHOTS = 1024                                      # [ASSUMED]
TIER_CLIENT = [1.0] * 4 + [3.0] * 4 + [10.0] * 4    # clients 1-4 Good, 5-8 Medium, 9-12 Bad   (Concept 1)
TIER_NAME = ["Good"] * 4 + ["Medium"] * 4 + ["Bad"] * 4
CHANNEL_P = {"good": 0.82, "moderate": 0.63, "poor": 0.31}
PROXY_Q = {"small": 10, "medium": 12, "large": 15}
PROXY_L = 3
N_CLIENTS = 12
KAPPA_MISMATCH = 0.2        # [PLACEHOLDER] rel. std of per-circuit infidelity when the two shifted circuits are mapped independently
LOGIT_SCALE = 3.0           # [ASSUMED]
W_CLAMP = 4.0
SIC_KAPPA = 0.5             # [ASSUMED] SIC priority strength (v2 M4ab and CD-QFed FD-SIC use the same value)
SIC_DELTA = 0.15            # [ASSUMED] first-decoded / second-decoded shift asymmetry under SIC (mean preserved)
RUN_DEFAULTS = dict(rounds=60, K=6, B=16, n_local=240, eta0=2.0, eval_every=5, n_test=600)   # identical to v2

# CD-QFed hyper-parameters - fixed a priori from the theory (NOT tuned on accuracy)
CDQ_HP = dict(tau_reg=1.0,        # Tikhonov constant in Eq. (10)
              lam_mid=0.5,        # Eq. (16) control-variate mixing (unshifted baseline vs EMA of paired midpoints)
              rho_mid=0.5,        # EMA rate of paired midpoints
              rho_mem=0.6,        # Eq. (19) drift-memory rate
              beta_pin=0.5,       # strength of gradient-sensitivity pinning (0 = off, 1 = full chip-tier ratio)  [ASSUMED]
              tau_floor=0.25,     # Eq. (21) variance floor (fraction of the minimum deconvolved variance)
              fsnr_gammas=(0.1, 1.0, 10.0),
              cv="offset",        # midpoint control variate: "y0" = literal Eq.(16) (y0 + own EMA midpoint), "offset" = y0 + cross-client offset
              orph="weight")      # where gamma_orph enters: "shrink" (Eq.17 only), "weight" (Eq.22 only, unbiased), "both" (literal 17+22)


# ----------------------------------------------------------------------------------------------- keyed RNG (common random numbers)
def rng_for(seed, round_idx, client, purpose):
    key = hashlib.blake2b(f"{seed}|{round_idx}|{client}|{purpose}".encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(key, "little"))


# ----------------------------------------------------------------------------------------------- data
def load_fmnist4(cache="fmnist4.npz"):
    """Fashion-MNIST classes 0-3, 28x28 -> 4x4 (7x7 block mean).  Sources tried: cache, torchvision, GitHub raw (zalandoresearch)."""
    if os.path.exists(cache):
        d = np.load(cache); return d["xtr"], d["ytr"], d["xte"], d["yte"], "fashion-mnist"
    def prep(x, y):
        x = x.astype(np.float32) / 255.0; m = y < 4; x, y = x[m], y[m]
        return x.reshape(-1, 4, 7, 4, 7).mean(axis=(2, 4)).reshape(-1, 16), y.astype(np.int64)
    xtr = None
    try:
        import torchvision
        tr = torchvision.datasets.FashionMNIST("/tmp/fmnist", train=True, download=True)
        te = torchvision.datasets.FashionMNIST("/tmp/fmnist", train=False, download=True)
        xtr, ytr = prep(tr.data.numpy(), tr.targets.numpy()); xte, yte = prep(te.data.numpy(), te.targets.numpy())
    except Exception:
        pass
    if xtr is None:
        base = "https://raw.githubusercontent.com/zalandoresearch/fashion-mnist/master/data/fashion/"
        def get(name, off):
            local = "/tmp/fm/" + name
            if not os.path.exists(local):
                os.makedirs("/tmp/fm", exist_ok=True); urllib.request.urlretrieve(base + name, local)
            return np.frombuffer(gzip.open(local).read(), np.uint8, offset=off)
        xtr, ytr = prep(get("train-images-idx3-ubyte.gz", 16).reshape(-1, 28, 28), get("train-labels-idx1-ubyte.gz", 8))
        xte, yte = prep(get("t10k-images-idx3-ubyte.gz", 16).reshape(-1, 28, 28), get("t10k-labels-idx1-ubyte.gz", 8))
    try: np.savez(cache, xtr=xtr, ytr=ytr, xte=xte, yte=yte)
    except Exception: pass
    return xtr, ytr, xte, yte, "fashion-mnist"


def angles(x, q):
    out = np.zeros((x.shape[0], q), np.float32); cnt = np.zeros(q)
    for k in range(16):
        out[:, k % q] += x[:, k]; cnt[k % q] += 1
    return (math.pi * out / cnt).astype(np.float32)


# ----------------------------------------------------------------------------------------------- statevector (RY + CZ ring: real amplitudes)
class Circ:
    """proxy QNN: product-state angle encoding -> L x (RY on every qubit + CZ ring) -> <Z_k>, k = 0..3.
    RY and CZ keep the amplitudes real, so one real float32 array per amplitude is exact.
    State layout is (2^q, B): the batch is the innermost (contiguous) axis, which is 2-3x faster on CPU and
    lets the GPU kernels run as plain strided views.  Identical arithmetic on both backends (GATE 8 checks it)."""

    def __init__(self, q, L=PROXY_L):
        self.q, self.L, self.P = q, L, q * L
        idx = np.arange(2 ** q)
        bits = [((idx >> (q - 1 - j)) & 1) for j in range(q)]
        ph = sum(bits[j] * bits[(j + 1) % q] for j in range(q))
        self.cz = (1 - 2 * (ph % 2)).astype(np.float32)
        self.zmat = np.stack([1 - 2 * bits[k] for k in range(4)], 1).astype(np.float32)
        if HAVE_TORCH and DEV == "cuda":          # built whenever a GPU exists; USE_TORCH decides whether they are used
            self.cz_t = torch.tensor(self.cz, device=DEV).unsqueeze(1)
            self.zmat_t = torch.tensor(self.zmat, device=DEV)

    def encode(self, ang):
        """classical angles (B,q) -> encoded product state, (2^q, B)"""
        B = ang.shape[0]; st = np.ones((B, 1), np.float32)
        c, s = np.cos(ang / 2), np.sin(ang / 2)
        for j in range(self.q):
            a = np.stack([c[:, j], s[:, j]], 1)
            st = (st[:, :, None] * a[:, None, :]).reshape(B, -1)
        return np.ascontiguousarray(st.T)

    def to_backend(self, st0):
        """move an encoded state to the active backend once (avoids host<->device copies inside the round loop)"""
        return torch.as_tensor(np.ascontiguousarray(st0), device=DEV) if USE_TORCH else st0

    def run(self, theta, st0):
        """theta (L,q), encoded state (2^q, B) -> <Z_k> as numpy (B,4)"""
        q = self.q
        if USE_TORCH:
            st = st0 if torch.is_tensor(st0) else torch.as_tensor(np.ascontiguousarray(st0), device=DEV)
            shp = st.shape; st = st.clone()
            for l in range(self.L):
                for j in range(q):
                    c, s = math.cos(float(theta[l, j]) / 2), math.sin(float(theta[l, j]) / 2)
                    v = st.view(2 ** j, 2, -1); a, b = v[:, 0, :], v[:, 1, :]
                    st = torch.stack([c * a - s * b, s * a + c * b], 1).reshape(shp)
                st = st * self.cz_t
            return ((st * st).transpose(0, 1) @ self.zmat_t).cpu().numpy()
        st = np.array(st0, dtype=np.float32, copy=True); buf = np.empty_like(st); cz = self.cz[:, None]
        for l in range(self.L):
            for j in range(q):
                c, s = np.float32(math.cos(theta[l, j] / 2)), np.float32(math.sin(theta[l, j] / 2))
                v = st.reshape(2 ** j, 2, -1); o = buf.reshape(2 ** j, 2, -1); a, b = v[:, 0, :], v[:, 1, :]
                np.multiply(a, c, out=o[:, 0, :]); o[:, 0, :] -= s * b
                np.multiply(a, s, out=o[:, 1, :]); o[:, 1, :] += c * b
                st, buf = buf, st
            st *= cz
        return (self.zmat.T @ (st * st)).T


def selftest_backend(q=8, B=24, tol=2e-4, seed=0):
    """GATE 8: the GPU kernels must reproduce the numpy kernels; on any mismatch or error the numpy backend is used."""
    global USE_TORCH
    if not USE_TORCH: return dict(backend="numpy", checked=False, max_abs_diff=0.0)
    try:
        rng = np.random.default_rng(seed); c = Circ(q); th = rng.uniform(-1, 1, (PROXY_L, q))
        st = c.encode(rng.uniform(0, math.pi, (B, q)).astype(np.float32))
        gpu = c.run(th, c.to_backend(st))
        USE_TORCH = False; cpu = Circ(q).run(th, st); USE_TORCH = True
        d = float(np.max(np.abs(gpu - cpu)))
    except Exception as e:
        USE_TORCH = False; print("!! torch backend failed (%s) -> numpy backend" % e)
        return dict(backend="numpy", checked=True, max_abs_diff=float("nan"))
    if d > tol:
        USE_TORCH = False; print("!! torch/numpy mismatch %.2e > %.1e -> numpy backend" % (d, tol))
    return dict(backend="torch/cuda" if USE_TORCH else "numpy", checked=True, max_abs_diff=d)


def autoselect_backend(qs=(10, 12, 15), B=192, reps=3):
    """Pick the faster statevector backend for THIS machine and keep it for the whole session (one backend per results file:
    float reduction order differs between numpy and cuda, and pooled rows must not mix).  GPU kernel-launch overhead can make
    torch slower than numpy at q = 10-12, so the choice is measured, not assumed."""
    global USE_TORCH
    rep = backend_report()
    if not (HAVE_TORCH and DEV == "cuda"):
        USE_TORCH = False; return dict(backend="numpy", timings={})
    q = max(qs); rng = np.random.default_rng(0)
    ang = rng.uniform(0, math.pi, (B, q)).astype(np.float32); th = rng.uniform(-1, 1, (PROXY_L, q))
    timings = {}
    for name, flag in (("numpy", False), ("torch/cuda", True)):
        USE_TORCH = flag; c = Circ(q); st = c.to_backend(c.encode(ang))
        c.run(th, st)                                                   # warm-up (cuda context / kernel compile)
        if flag: torch.cuda.synchronize()
        t0 = time.time()
        for _ in range(reps): c.run(th, st)
        if flag: torch.cuda.synchronize()
        timings[name] = (time.time() - t0) / reps
    USE_TORCH = timings["torch/cuda"] < timings["numpy"]
    print("backend timing at q=%d, B=%d:  numpy %.1f ms | torch/cuda %.1f ms  ->  using %s"
          % (q, B, 1e3 * timings["numpy"], 1e3 * timings["torch/cuda"], "torch/cuda" if USE_TORCH else "numpy"))
    return dict(backend="torch/cuda" if USE_TORCH else "numpy", timings=timings)


# ----------------------------------------------------------------------------------------------- compile-derived noise (v2 Step-4 model)
def eps_total(counts, tau_client, tau_chip_override=None, lam=0.1):
    tau = {int(k): float(v) for k, v in counts["tau_chip"].items()}
    if tau_chip_override is not None:
        tau = {k: tau_chip_override for k in tau}
    tbar = float(np.mean(list(tau.values())))
    e0 = lam * tau_client * (P1_BASE * counts["n1q"] + P2_BASE * tbar * counts["n2q_logical"])
    es = sum(3.0 * lam * tau_client * tau[int(c)] * P2_BASE * s for c, s in counts["S_local"].items())
    er = 0.0
    for link, e in counts["E_link"].items():
        a, b = [int(v) for v in link.split("-")]
        er += lam * tau_client * 0.5 * (tau[a] + tau[b]) * PR_BASE * e
    return e0 + es + er


def sigma2_of_eps(eps, m2):
    return (1.0 - np.exp(-2.0 * np.asarray(eps, float)) * m2) / M_SHOTS


def psi_nsr(eps, m2):
    """Eq. (5): noise-to-signal variance amplification  M*sigma^2 / exp(-2 eps) = exp(2 eps) - m2  (never saturates)"""
    return np.exp(2.0 * np.asarray(eps, float)) - m2


def _arm_eps_full(counts, arm, lam):
    if arm in ("A1", "A0_A1"):  return np.array([eps_total(counts, t, 1.0, lam) for t in TIER_CLIENT])
    if arm in ("A2", "A0_A2"):  return np.array([eps_total(counts, 1.0, None, lam)] * N_CLIENTS)
    if arm in ("A3", "A3adv", "A0_A3"): return np.array([eps_total(counts, t, None, lam) for t in TIER_CLIENT])
    raise KeyError(arm)


def proxy_ratio(counts, scale):
    return PROXY_L * PROXY_Q[scale] / counts["n2q_logical"]


def fleet_eps(counts, scale, arm, lam, m2, ratio=None):
    """eps_proxy for the 12 clients.  A0_Ax = homogeneous fleet matched on MEAN sigma^2 of arm Ax (v2 FIX 3).
    `ratio` lets a recompiled circuit (DMapS-FSNR) be scaled with the BASELINE proxy ratio, so only the compile changes."""
    ratio = proxy_ratio(counts, scale) if ratio is None else ratio
    if arm == "CLEAN": return np.zeros(N_CLIENTS)
    full = _arm_eps_full(counts, arm.replace("A0_", "") if arm.startswith("A0_") else arm, lam) * ratio
    if arm.startswith("A0_"):
        s_bar = float(np.mean(sigma2_of_eps(full, m2)))
        f = lambda e: float(sigma2_of_eps(e, m2)) - s_bar
        e0 = 0.0 if abs(f(0.0)) < 1e-15 else brentq(f, 0.0, 60.0, xtol=1e-14, rtol=1e-14)
        return np.full(N_CLIENTS, e0)
    return full


def calibrate_lambda(scale, counts, m2, targets=(0.15, 0.40, 0.65), lam_grid=np.logspace(-4, 0, 400)):
    """v2 FIX 2 (strict mode): lambda chosen on sigma^2 only; unreachable targets remapped onto [floor+0.02, 0.80]."""
    e01 = _arm_eps_full(counts, "A3", 0.1) * proxy_ratio(counts, scale)
    tier = np.array([e01[0], e01[4], e01[8]])
    curves = np.array([sigma2_of_eps(tier * (l / 0.1), m2) * M_SHOTS for l in lam_grid])
    floor = 1.0 - m2; tg = np.array(targets, float); bad_max, good_min = 0.80, 0.05
    if tg.min() < floor + 0.005:
        lo, hi = floor + 0.02, bad_max
        if hi <= lo: raise RuntimeError("calibration infeasible (m2 too small)")
        tg = lo + (tg - tg.min()) / (tg.max() - tg.min()) * (hi - lo)
    ok = (curves[:, 2] <= bad_max) & (curves[:, 0] >= good_min)
    obj = np.where(ok, ((curves - tg) ** 2).sum(1), np.inf); i = int(np.argmin(obj))
    return dict(scale=scale, lam=float(lam_grid[i]), m2=float(m2), realised=curves[i].tolist(), floor=float(floor),
                ratio=float(curves[i, 2] / curves[i, 0]), bad_max=bad_max, good_min=good_min,
                tier_eps=(tier * lam_grid[i] / 0.1).tolist(), tier_signal=np.exp(-tier * lam_grid[i] / 0.1).tolist())


# ----------------------------------------------------------------------------------------------- Innovation 1: DMapS-FSNR selection + pinning
def select_fsnr_compile(compile_tbl, scale, arm, lam, m2):
    """Among {baseline (gamma'=0 == none)} U {FSNR compiles gamma' in CDQ_HP['fsnr_gammas']} pick the compile minimising the
    predicted fleet-mean Psi_NSR (Eq. 5).  Uses the analytic noise model only - no accuracy is involved.  Because the baseline
    is a candidate, the selected compile is never worse than the baseline on the selection criterion."""
    base = compile_tbl["%s|none" % scale]; r0 = proxy_ratio(base, scale)
    cands = {"none": base}
    for g in CDQ_HP["fsnr_gammas"]:
        k = "%s|fsnr%s" % (scale, g)
        if k in compile_tbl: cands["fsnr%s" % g] = compile_tbl[k]
    score = {k: float(np.mean(psi_nsr(fleet_eps(c, scale, arm, lam, m2, ratio=r0), m2))) for k, c in cands.items()}
    best = min(score, key=lambda k: (score[k], k != "none"))
    return best, cands[best], score


def pinning_factors(counts, arm, sens, beta_pin):
    """Gradient-sensitivity sub-circuit pinning: parameters ranked by noiseless |dF/dtheta_k|; the top block is placed on the
    lowest-tier chip partition, ...  xi_k = 1 + beta_pin (tau_assigned/tau_bar - 1), renormalised to mean 1 (mean eps invariant).
    A1 (all chips tier 1) -> xi == 1 exactly."""
    P = len(sens)
    if arm in ("A1", "A0_A1", "A0_A2", "A0_A3", "CLEAN") or beta_pin == 0: return np.ones(P)
    used = sorted({int(c) for c in counts["S_local"]} | {int(x) for l in counts["E_link"] for x in l.split("-")})
    taus = np.sort([float(counts["tau_chip"][str(c)]) for c in used])
    groups = np.array_split(np.argsort(-np.asarray(sens)), len(taus))
    xi = np.ones(P)
    for g, t in zip(groups, taus): xi[g] = 1.0 + beta_pin * (t / taus.mean() - 1.0)
    return xi / xi.mean()


# ----------------------------------------------------------------------------------------------- Innovation 2: MMSE/Tikhonov fidelity deconvolution
def deconv_gain(eps, m2, tau_reg=1.0):
    """Eq. (10)  kappa* = m2 e^{-eps} / (m2 e^{-2eps} + tau_reg sigma^2),  sigma^2 = (1 - m2 e^{-2eps})/M"""
    eps = np.asarray(eps, float); s2 = sigma2_of_eps(eps, m2)
    return m2 * np.exp(-eps) / (m2 * np.exp(-2 * eps) + tau_reg * s2)


def inject(f, eps_row, z):
    """<O>_noisy = e^{-eps} F_ideal + N(0, (1 - (e^{-eps}F)^2)/M)"""
    m = np.exp(-eps_row)[:, None] * f
    var = np.clip(1 - m * m, 0, None) / M_SHOTS
    return m + np.sqrt(var) * z, var


# ----------------------------------------------------------------------------------------------- Innovation 4 / JEQFL: divergence DP partition
def dp_partition(d, scale_int=1000):
    """Chung et al. Sec. IV-B: split clients into LC / RC minimising |sum_LC d - sum_RC d| (subset-sum DP)."""
    w = np.maximum(np.round(np.asarray(d) / max(np.max(d), 1e-12) * scale_int).astype(int), 0)
    tot = int(w.sum()); reach = {0: ()}
    for i, wi in enumerate(w):
        new = dict(reach)
        for s, members in reach.items():
            if s + wi not in new: new[s + wi] = members + (i,)
        reach = new
    best = min(reach, key=lambda s: (abs(tot - 2 * s), s))
    LC = np.zeros(len(d), bool); LC[list(reach[best])] = True
    return LC


# ----------------------------------------------------------------------------------------------- method definitions
_B = dict(est="m5a", w="uniform", sic="none", twin=False, crit=None, deconv=False, mem=False, fsnr=False, pin=False, hp={})
def _v(**k): d = dict(_B); d.update(k); return d
VARIANTS = {
    "base":     _v(),
    "JEQFL":    _v(sic="jeqfl"),
    "M4a":      _v(w="ivar"),
    "M4ab":     _v(w="ivar", sic="m4ab"),
    "M5b":      _v(est="m5b"),
    "M3":       _v(twin=True),
    "M2":       _v(crit="m2"),
    "CDQ":      _v(est="drjps", w="fisher", sic="fdsic", twin=True, deconv=True, mem=True, fsnr=True, pin=True),
    # literal reading of the design document: control variate mu = (1-lam) y0 + lam * EMA(midpoint)   [Eq. 16 as written]
    # and gamma_orph applied BOTH inside Eq. (17) and again as the Eq. (22) weight.  Kept as its own method so the two
    # readings can be compared on the same seeds instead of one being chosen silently.
    "CDQ-lit":  _v(est="drjps", w="fisher", sic="fdsic", twin=True, deconv=True, mem=True, fsnr=True, pin=True,
                   hp=dict(cv="y0", orph="both")),
    "CDQ-noI1": _v(est="drjps", w="fisher", sic="fdsic", twin=True, deconv=True, mem=True, fsnr=False, pin=False),
    "CDQ-noI2": _v(est="drjps", w="fisher", sic="fdsic", twin=True, deconv=False, mem=True, fsnr=True, pin=True),
    "CDQ-noI3a": _v(est="m5b", w="fisher", sic="fdsic", twin=True, deconv=True, mem=True, fsnr=True, pin=True),
    "CDQ-noI3b": _v(est="drjps", w="fisher", sic="fdsic", twin=True, deconv=True, mem=False, fsnr=True, pin=True),
    "CDQ-noI4": _v(est="drjps", w="uniform", sic="none", twin=True, deconv=True, mem=True, fsnr=True, pin=True),
}
# ---- ablations anchored on CDQ-lit --------------------------------------------------------------------------------
# CDQ-lit is the PROPOSED algorithm (Eqs. 16-22 exactly as written: control variate mu = (1-lam)y0 + lam*EMA(midpoint),
# Gauss-Markov orphan shrinkage gamma_orph applied in both Eq.(17) and Eq.(22)).  CDQ is the SAME framework with the
# shrinkage removed, i.e. the shrinkage ablation.  The per-innovation ablation must therefore be anchored on CDQ-lit
# as well, so each innovation is removed from the reported method rather than from a variant of it.
_LIT = dict(cv="y0", orph="both")
VARIANTS.update({
    "CDQ-lit-noI1":  _v(est="drjps", w="fisher", sic="fdsic", twin=True, deconv=True,  mem=True,  fsnr=False, pin=False, hp=dict(_LIT)),
    "CDQ-lit-noI2":  _v(est="drjps", w="fisher", sic="fdsic", twin=True, deconv=False, mem=True,  fsnr=True,  pin=True,  hp=dict(_LIT)),
    "CDQ-lit-noI3a": _v(est="m5b",   w="fisher", sic="fdsic", twin=True, deconv=True,  mem=True,  fsnr=True,  pin=True,  hp=dict(_LIT)),
    "CDQ-lit-noI3b": _v(est="drjps", w="fisher", sic="fdsic", twin=True, deconv=True,  mem=False, fsnr=True,  pin=True,  hp=dict(_LIT)),
    "CDQ-lit-noI4":  _v(est="drjps", w="uniform", sic="none", twin=True, deconv=True,  mem=True,  fsnr=True,  pin=True,  hp=dict(_LIT)),
})
BASELINES = ["base", "JEQFL", "M4a", "M4ab", "M5b", "M3", "M2"]
METHODS = ["CDQ-lit", "CDQ"]                       # CDQ-lit first: it is the proposed method, CDQ is the shrinkage ablation
ABLATIONS = ["CDQ-noI1", "CDQ-noI2", "CDQ-noI3a", "CDQ-noI3b", "CDQ-noI4"]
ABLATIONS_LIT = ["CDQ-lit-noI1", "CDQ-lit-noI2", "CDQ-lit-noI3a", "CDQ-lit-noI3b", "CDQ-lit-noI4"]


# ----------------------------------------------------------------------------------------------- one federated run
def run_one(scale, arm, alpha, channel, seed, variant, compile_tbl, data, cal, hp_over=None, **over):
    kw = dict(RUN_DEFAULTS); kw.update(over)
    rounds, K, B, n_local, eta0, eval_every, n_test = (kw[k] for k in ("rounds", "K", "B", "n_local", "eta0", "eval_every", "n_test"))
    v = VARIANTS[variant]; hp = dict(CDQ_HP); hp.update(v.get("hp") or {}); hp.update(hp_over or {}); q = PROXY_Q[scale]; circ = Circ(q); P = circ.P
    xtr, ytr, xte, yte, _ = data
    lam, m2 = cal[scale]["lam"], cal[scale]["m2"]
    base_counts = compile_tbl["%s|none" % scale]; r0 = proxy_ratio(base_counts, scale)
    compile_key, counts = "none", base_counts
    if v["fsnr"] and not arm.startswith("A0_") and arm != "CLEAN":
        compile_key, counts, _ = select_fsnr_compile(compile_tbl, scale, arm, lam, m2)
    eps = fleet_eps(counts, scale, arm, lam, m2, ratio=r0)

    # ---- shards (keyed per client; identical for every variant)
    idx_by_c = [np.where(ytr == c)[0] for c in range(4)]; cl_idx = []
    for n in range(N_CLIENTS):
        g = rng_for(seed, 0, n, "shards"); base = np.ones(4)
        if arm == "A3adv" and n < 8: base[2:] = 0.05          # rare classes 2,3 live on Bad-hardware clients 9-12
        pn = g.dirichlet(alpha / 4.0 * base * 4.0 / base.sum())
        cnt = g.multinomial(n_local, pn)
        cl_idx.append(np.concatenate([g.choice(idx_by_c[c], cnt[c]) for c in range(4)]))
    te_i = rng_for(seed, 0, -1, "testset").choice(len(yte), min(n_test, len(yte)), replace=False)
    Ste = circ.to_backend(circ.encode(angles(xte[te_i], q))); Yte = yte[te_i]
    theta = rng_for(seed, 0, -1, "init").uniform(-0.3, 0.3, (PROXY_L, q))

    # ---- noiseless sensitivity ranking (M2 pre-test batch; also used by CD-QFed pinning)
    crit_mult = np.ones(P)
    if v["crit"] == "m2" or v["pin"]:
        Sb = circ.to_backend(circ.encode(angles(xtr[rng_for(seed, 0, -1, "m2batch").choice(len(xtr), 64)], q))); sens = np.zeros(P)
        for k in range(P):
            a = theta.copy().ravel(); b = a.copy(); a[k] += math.pi / 2; b[k] -= math.pi / 2
            sens[k] = 0.5 * np.abs(circ.run(a.reshape(PROXY_L, q), Sb) - circ.run(b.reshape(PROXY_L, q), Sb)).mean()
        if v["crit"] == "m2":
            top = np.argsort(-sens)[: P // 3]; crit_mult[:] = (P - 0.5 * len(top)) / (P - len(top)); crit_mult[top] = 0.5
        if v["pin"]:
            crit_mult = pinning_factors(counts, arm, sens, hp["beta_pin"])

    # ---- channel / SIC configuration
    p_shift = CHANNEL_P[channel]
    s2n = sigma2_of_eps(eps, m2)
    sig2_dec = sigma2_of_eps(eps, m2) * deconv_gain(eps, m2, hp["tau_reg"]) ** 2 if v["deconv"] else s2n
    if v["w"] == "ivar":
        w = 1.0 / np.maximum(s2n, 1e-12); w /= w.mean(); w = np.minimum(w, W_CLAMP); w /= w.mean()
    elif v["w"] == "fisher":                                         # Eq. (21) precision-clamped weights on deconvolved variance
        wr = 1.0 / (sig2_dec + hp["tau_floor"] * sig2_dec.min()); w = np.minimum(wr / wr.mean(), W_CLAMP); w /= w.mean()
    else:
        w = np.ones(N_CLIENTS)
    pdec = np.full(N_CLIENTS, p_shift)
    if v["sic"] == "m4ab":
        pd_ = np.clip(p_shift * (1 + SIC_KAPPA * (w / w.mean() - 1)), 0.05, 0.98); pdec = np.clip(pd_ * p_shift / pd_.mean(), 0.05, 0.98)

    # ---- state for DR-JPS / Fed-QDrift
    mem = np.zeros((N_CLIENTS, P)); abar = np.full((N_CLIENTS, P), np.nan); dk_ema = np.full(P, np.nan); abar_mid = np.full((N_CLIENTS, P), np.nan)
    vg_ema, vr_ema = None, None
    kap0 = deconv_gain(eps, m2, hp["tau_reg"]) if v["deconv"] else np.ones(N_CLIENTS)

    log = dict(acc=[], rec=[], drift=[], scda=[], skew=[], att=[], active=[], mism=[], gorph=[], m2=[])
    # ---- weight-matrix recording.  Wtrace[t][n] = client n's EFFECTIVE aggregation weight in round t
    # (ideal 1.0 for every client: that is what "no tier skew" means).  PDtrace[t][n] = its mean SIC decode
    # probability that round.  log_weights=True additionally keeps the full matrices for printing.
    log_weights = bool(kw.get("log_weights", False))
    weight_every = int(kw.get("weight_every", 5) or 5)        # snapshot the weight matrix every N rounds ("epochs")
    Wtrace, PDtrace, PItrace = [], [], []
    # The two CRN digests are accumulated as byte buffers and folded into one md5 at the end.  md5(concat) is
    # identical to streaming md5(update, update, ...), so hash_u / hash_z are the SAME numbers as before - but a
    # list of bytes can be pickled, which is what lets an interrupted run be resumed exactly.
    h_u_buf, h_z_buf = [], []
    rep = lambda a: np.repeat(a, B)

    def shot(t, tag):
        z = np.concatenate([rng_for(seed, t, n, "shot|" + tag).standard_normal((B, 4)) for n in range(N_CLIENTS)]).astype(np.float32)
        h_z_buf.append(z.tobytes()[:64]); return z

    # ---------------------------------------------------------------- in-run checkpoint (Kaggle 12 h session limit)
    # Saved: everything the round loop carries forward.  NOT saved, because they are deterministic functions of
    # (scale, arm, alpha, channel, seed, variant) and are rebuilt identically on resume: eps, w, pdec, sig2_dec,
    # kap0, crit_mult, the client shards, the test set and theta_0.  Every random draw goes through
    # rng_for(seed, round, client, purpose), so round t resumed from disk draws EXACTLY the numbers it would have
    # drawn without the interruption -> a resumed run is bit-identical to an uninterrupted one.  No algorithm changes.
    ck_path = kw.get("ckpt_path"); ck_every = int(kw.get("ckpt_every", 0) or 0); ck_deadline = kw.get("deadline")
    ck_sig = (scale, arm, alpha, channel, seed, variant, rounds, K, B, n_local, eta0, eval_every, n_test, weight_every)
    t_start = 0
    if ck_path and os.path.exists(ck_path):
        try:
            with gzip.open(ck_path, "rb") as fh: _ck = pickle.load(fh)
            if tuple(_ck.get("sig", ())) == ck_sig:
                theta, mem, abar, abar_mid = _ck["theta"], _ck["mem"], _ck["abar"], _ck["abar_mid"]
                dk_ema, vg_ema, vr_ema, log = _ck["dk_ema"], _ck["vg_ema"], _ck["vr_ema"], _ck["log"]
                Wtrace, PDtrace, PItrace = _ck["Wtrace"], _ck["PDtrace"], _ck["PItrace"]
                h_u_buf[:], h_z_buf[:] = _ck["h_u_buf"], _ck["h_z_buf"]
                t_start = int(_ck["t_next"])
                print("    [resume] %s|%s|a%s|%s|seed%s|%s  continuing at round %d/%d"
                      % (scale, arm, alpha, channel, seed, variant, t_start, rounds), flush=True)
            else:
                print("    [resume] checkpoint signature differs - restarting this run", flush=True)
        except Exception as _e:
            print("    [resume] checkpoint unreadable (%s) - restarting this run" % _e, flush=True)

    def _save_ckpt(t_next):
        st = dict(sig=ck_sig, t_next=int(t_next), theta=theta, mem=mem, abar=abar, abar_mid=abar_mid,
                  dk_ema=dk_ema, vg_ema=vg_ema, vr_ema=vr_ema, log=log, Wtrace=Wtrace, PDtrace=PDtrace,
                  PItrace=PItrace, h_u_buf=h_u_buf, h_z_buf=h_z_buf)
        tmp = ck_path + ".tmp"
        with gzip.open(tmp, "wb", compresslevel=1) as fh: pickle.dump(st, fh, protocol=4)
        os.replace(tmp, ck_path)                                   # atomic: a killed session never leaves a torn file

    for t in range(t_start, rounds):
        eta = eta0 / (1 + 0.03 * t)
        bi = [rng_for(seed, t, n, "batch").choice(cl_idx[n], B) for n in range(N_CLIENTS)]
        xb = np.concatenate([xtr[i] for i in bi]); yb = np.concatenate([ytr[i] for i in bi])
        S0 = circ.to_backend(circ.encode(angles(xb, q))); Yoh = np.eye(4, dtype=np.float32)[yb]

        f0 = circ.run(theta, S0)
        f0n, _ = inject(f0, rep(eps), shot(t, "base"))
        f0d = f0n * rep(kap0)[:, None]                                 # Eq. (11) deconvolved base observable (kappa=1 if off)
        sm_ = lambda z: np.exp(z - z.max(1, keepdims=True)) / np.exp(z - z.max(1, keepdims=True)).sum(1, keepdims=True)
        wgt = LOGIT_SCALE * (sm_(LOGIT_SCALE * f0d) - Yoh)            # Eq. (12)
        wgt_i = LOGIT_SCALE * (sm_(LOGIT_SCALE * f0) - Yoh)
        y0 = (wgt * f0d).sum(1).reshape(N_CLIENTS, B).mean(1)          # unshifted control-variate baseline (Eq. 16)

        # ---- per-round decode probabilities (JEQFL clustering / FD-SIC) -> LS/RS probabilities per client
        pL, pR = pdec.copy(), pdec.copy()
        if v["sic"] in ("jeqfl", "fdsic"):
            dvg = np.linalg.norm(wgt.reshape(N_CLIENTS, B, 4), axis=2).mean(1)            # Chung Eq. (8)
            if v["sic"] == "fdsic":
                dvg = w * dvg ** 2                                                         # Eq. (23) Fisher-divergence
                pd_ = np.clip(p_shift * (1 + SIC_KAPPA * (dvg / dvg.mean() - 1)), 0.05, 0.98)   # Eq. (24)
                pbase = np.clip(pd_ * p_shift / pd_.mean(), 0.05, 0.98)
            else:
                pbase = pdec.copy()
            LC = dp_partition(dvg)
            hi_, lo_ = np.clip(pbase * (1 + SIC_DELTA), 0.05, 0.98), np.clip(pbase * (1 - SIC_DELTA), 0.05, 0.98)
            pL = np.where(LC, hi_, lo_); pR = np.where(LC, lo_, hi_)

        ks = rng_for(seed, t, -1, "paramsel").choice(P, K, replace=False)
        g_est = np.zeros(K); g_ref = np.zeros(K); G_n = np.zeros((N_CLIENTS, K)); Weff = np.zeros(N_CLIENTS)
        for ii, k in enumerate(ks):
            outs = {}
            for sgn in (+1, -1):
                th = theta.copy().ravel(); th[k] += sgn * math.pi / 2
                f = circ.run(th.reshape(PROXY_L, q), S0)
                em = eps * crit_mult[k]
                xi = rng_for(seed, t, -1, "jitter|%d|%d" % (ii, sgn)).standard_normal(N_CLIENTS)   # drawn always (CRN)
                if not v["twin"]: em = em * np.clip(1 + KAPPA_MISMATCH * xi, 0.0, None)
                fn, _ = inject(f, rep(em), shot(t, "%d|%d" % (ii, sgn)))
                if v["deconv"]: fn = fn * rep(deconv_gain(eps * crit_mult[k], m2, hp["tau_reg"]))[:, None]
                outs[sgn] = (fn, f); log["m2"].append(float((f ** 2).mean()))
            sp = (wgt * outs[1][0]).sum(1).reshape(N_CLIENTS, B).mean(1)
            sm = (wgt * outs[-1][0]).sum(1).reshape(N_CLIENTS, B).mean(1)
            sp_i = (wgt_i * outs[1][1]).sum(1).reshape(N_CLIENTS, B).mean(1)
            sm_i = (wgt_i * outs[-1][1]).sum(1).reshape(N_CLIENTS, B).mean(1)
            gn_star = 0.5 * (sp_i - sm_i); G_n[:, ii] = gn_star; g_ref[ii] = gn_star.mean()
            uLR = np.stack([rng_for(seed, t, n, "channel|%d" % ii).random(2) for n in range(N_CLIENTS)])
            h_u_buf.append(uLR.tobytes())
            Ld, Rd = uLR[:, 0] < pL, uLR[:, 1] < pR
            Pd = Ld & Rd; A = Ld | Rd; OL = Ld & ~Rd; OR = Rd & ~Ld
            weff = np.zeros(N_CLIENTS)
            if v["est"] == "m5b":
                g = 0.5 * np.sum(w[Pd] * (sp[Pd] - sm[Pd])) / w[Pd].sum() if Pd.any() else 0.0
                if Pd.any(): weff[Pd] = w[Pd] / w[Pd].sum()
                g_cl = np.where(Pd, 0.5 * (sp - sm), np.nan); act = Pd
            elif v["est"] == "m5a":
                if Ld.any() and Rd.any():
                    g = 0.5 * (np.sum(w[Ld] * sp[Ld]) / w[Ld].sum() - np.sum(w[Rd] * sm[Rd]) / w[Rd].sum())
                    weff[Ld] += 0.5 * w[Ld] / w[Ld].sum(); weff[Rd] += 0.5 * w[Rd] / w[Rd].sum()
                    fb = 0.5 * (sp_i + sm_i); log["mism"].append(abs(fb[Ld].mean() - fb[Rd].mean()))
                else:
                    g = 0.0
                g_cl = np.where(Pd, 0.5 * (sp - sm), np.where(OL, sp - y0, np.where(OR, y0 - sm, np.nan))); act = A
            else:                                                       # ---- DR-JPS (Eq. 16-18)
                # control variate for the shift midpoint A_{n,k} (Eq. 14-16).  delta_n = A_n - y0_n is the harmonic offset
                # (B cos + C sin) between midpoint and unshifted output; it is estimated from the PAIRED clients of this round
                # (cross-client, same coordinate) mixed with the client's own EMA offset:  mu_n = y0_n + (1-lam) dbar + lam d_n^own
                gpair = 0.5 * (sp - sm); mid = 0.5 * (sp + sm); delta = mid - y0
                if Pd.any():
                    dbar = float(delta[Pd].mean()); dk_ema[k] = dbar if np.isnan(dk_ema[k]) else (1 - hp["rho_mid"]) * dk_ema[k] + hp["rho_mid"] * dbar
                else:
                    dbar = 0.0 if np.isnan(dk_ema[k]) else float(dk_ema[k])
                own = abar[:, k]
                dhat = np.where(np.isnan(own), dbar, (1 - hp["lam_mid"]) * dbar + hp["lam_mid"] * np.nan_to_num(own))
                mu = y0 + dhat
                if hp["cv"] == "y0":                                    # literal Eq. (16): (1-lam) y0 + lam * own EMA midpoint
                    own_mid = abar_mid[:, k]
                    mu = np.where(np.isnan(own_mid), y0, (1 - hp["lam_mid"]) * y0 + hp["lam_mid"] * np.nan_to_num(own_mid))
                if Pd.sum() >= 2:                                       # Eq. (18) moments: signal power + leave-one-out residual
                    npd = Pd.sum(); loo = (delta[Pd].sum() - delta[Pd]) / (npd - 1)
                    vg = float(np.mean(gpair[Pd] ** 2)); vr = float(np.mean((delta[Pd] - loo) ** 2))
                    vg_ema = vg if vg_ema is None else 0.8 * vg_ema + 0.2 * vg
                    vr_ema = vr if vr_ema is None else 0.8 * vr_ema + 0.2 * vr
                s2y = float(np.mean(sig2_dec)) * float(np.mean(wgt ** 2)) * 4 / B
                g_orph = 0.5 if vg_ema is None else vg_ema / (vg_ema + vr_ema + s2y + 1e-12)
                log["gorph"].append(g_orph)
                g_cl = np.full(N_CLIENTS, np.nan)
                # Eq.(17) x Eq.(22) folded: orphan estimate kept UNBIASED (y - mu); gamma_orph is its normalised reliability weight
                # (pi_orph = 0.5 gamma_orph w).  Shrinking inside Eq.17 AND weighting in Eq.22 would pull E[g_hat] below grad G,
                # violating the unbiasedness assumed in the proof of Theorem 1.
                shr = g_orph if hp["orph"] in ("shrink", "both") else 1.0
                g_cl[Pd] = gpair[Pd]; g_cl[OL] = shr * (sp[OL] - mu[OL]); g_cl[OR] = -shr * (sm[OR] - mu[OR])
                upm = Pd & np.isnan(abar_mid[:, k]); abar_mid[upm, k] = mid[upm]
                upm2 = Pd & ~upm; abar_mid[upm2, k] = (1 - hp["rho_mid"]) * abar_mid[upm2, k] + hp["rho_mid"] * mid[upm2]
                upd = Pd & np.isnan(abar[:, k]); abar[upd, k] = delta[upd]          # own offset tracker (EMA of paired offsets)
                upd2 = Pd & ~upd; abar[upd2, k] = (1 - hp["rho_mid"]) * abar[upd2, k] + hp["rho_mid"] * delta[upd2]
                act = A
                wo = g_orph if hp["orph"] in ("weight", "both") else 1.0
                pi = np.where(Pd, w, 0.5 * wo * w) * A
                if not v["mem"]:
                    g = float(np.sum(pi[A] * g_cl[A]) / pi[A].sum()) if A.any() else 0.0
                    if A.any(): weff[A] = pi[A] / pi[A].sum()
            if v["mem"]:                                                # ---- Fed-QDrift (Eq. 19-20)
                pi = (np.where(Pd, w, 0.5 * wo * w) if v["est"] == "drjps" else w) * act
                anchor = mem[:, k].mean()
                if act.any():
                    innov = np.sum(pi[act] * (g_cl[act] - mem[act, k])) / pi[act].sum()
                    weff = 1.0 / N_CLIENTS + np.where(act, pi / pi[act].sum(), 0.0)
                    mem[act, k] = (1 - hp["rho_mem"]) * mem[act, k] + hp["rho_mem"] * g_cl[act]
                else:
                    innov = 0.0; weff = np.full(N_CLIENTS, 1.0 / N_CLIENTS)
                g = anchor + innov
            log["active"].append(int(act.sum()))
            try: PItrace.append(np.asarray(pi, float).copy())        # Eq. (22) precision-clamped innovation weights
            except Exception: PItrace.append(np.asarray(w, float).copy() * act)
            Weff += weff
            g_est[ii] = g
            th = theta.ravel(); th[k] -= eta * g; theta = th.reshape(PROXY_L, q)

        # ---- client-drift metrics (Eq. 1-2): reference = noiseless, lossless full-fleet gradient on the sampled coordinates
        err = g_est - g_ref; gn = np.linalg.norm(g_ref) + 1e-12
        het = np.linalg.norm(G_n - g_ref[None, :], axis=1)
        we = Weff / max(Weff.sum(), 1e-12) * N_CLIENTS
        Wtrace.append(we.copy()); PDtrace.append(0.5 * (pL + pR))
        cov = float(np.mean((we - we.mean()) * (het - het.mean())))
        log["drift"].append(float(err @ err) + cov ** 2)
        cosv = float(g_est @ g_ref / (np.linalg.norm(g_est) * gn + 1e-12))
        log["scda"].append(cosv * math.exp(-np.linalg.norm(err) / gn))
        log["skew"].append(float(we[8:].sum() / N_CLIENTS))            # share of effective weight on Bad-tier clients (ideal 1/3)
        log["att"].append(float(np.linalg.norm(g_est) / gn))
        log["rec"].append(float(np.linalg.norm(err)))
        if (t + 1) % eval_every == 0 or t == rounds - 1:
            log["acc"].append(float((circ.run(theta, Ste).argmax(1) == Yte).mean()))

        # ---- intermediate state to disk, and a clean stop when the session clock runs out
        if ck_path and ck_every and ((t + 1) % ck_every == 0 or t == rounds - 1):
            _save_ckpt(t + 1)
        if ck_path and ck_deadline is not None and time.time() > ck_deadline and t < rounds - 1:
            _save_ckpt(t + 1)
            raise SessionTimeUp("session budget reached inside %s|%s|a%s|%s|seed%s|%s at round %d/%d "
                                "- checkpointed, will continue next session"
                                % (scale, arm, alpha, channel, seed, variant, t + 1, rounds))

    acc = log["acc"]
    if ck_path and os.path.exists(ck_path):
        try: os.remove(ck_path)                                    # the run finished; its checkpoint is dead weight
        except OSError: pass

    # ---------------------------------------------------------------- weight matrices of this training run
    W = np.asarray(Wtrace, float) if Wtrace else np.ones((1, N_CLIENTS))
    PD = np.asarray(PDtrace, float) if PDtrace else np.full((1, N_CLIENTS), float("nan"))
    PI = np.asarray(PItrace, float) if PItrace else np.ones((1, N_CLIENTS))
    r3 = max(1, len(W) // 3)
    jj = lambda a, d=5: json.dumps([round(float(x), d) for x in np.asarray(a, float).ravel()])

    # ---- weight matrix snapshot every `weight_every` rounds: block means, labelled by the last round of the block
    nblk = len(W) // weight_every
    if nblk:
        SNAP = W[:nblk * weight_every].reshape(nblk, weight_every, N_CLIENTS).mean(1)
        SNAP_PD = PD[:nblk * weight_every].reshape(nblk, weight_every, N_CLIENTS).mean(1)
        SNAP_R = [int((i + 1) * weight_every) for i in range(nblk)]
    else:
        SNAP, SNAP_PD, SNAP_R = W.mean(0, keepdims=True), PD.mean(0, keepdims=True), [len(W)]
    wx = dict(
        w_static=jj(w),                                           # Eq. (21) clamped precision weights (constant over the run)
        w_eff_mean=jj(W.mean(0)),                                 # effective aggregation weight, mean over rounds (ideal 1.0)
        w_eff_early=jj(W[:r3].mean(0)),                           #   ... over the first third of the rounds
        w_eff_late=jj(W[-r3:].mean(0)),                           #   ... over the last third  (steady state)
        w_innov_mean=jj(PI.mean(0)),                              # Eq. (22) innovation weights pi_{n,k}
        p_dec_mean=jj(PD.mean(0)),                                # Eq. (24) realised per-client SIC decode probability
        eps_client=jj(eps),                                       # compiled infidelity eps_n (Concept 1 x Concept 2)
        signal_client=jj(np.exp(-np.asarray(eps, float))),        # hardware attenuation e^{-eps_n}
        kappa_client=jj(np.asarray(kap0, float)),                 # Eq. (10) MMSE deconvolution gain kappa*_n
        sig2_dec_client=jj(np.asarray(sig2_dec, float) * M_SHOTS, 6),   # Eq. (13) deconvolved variance x M_shots
        mem_norm=jj(np.linalg.norm(mem, axis=1), 6),              # Eq. (19) drift-memory norm per client
        tier_share_late=jj([W[-r3:].mean(0)[:4].sum() / N_CLIENTS,
                            W[-r3:].mean(0)[4:8].sum() / N_CLIENTS,
                            W[-r3:].mean(0)[8:].sum() / N_CLIENTS]),    # Good / Medium / Bad share, ideal 1/3 each
        weight_every=weight_every,
        w_every_rounds=json.dumps(SNAP_R),                        # the round each snapshot block ends on
        w_every_matrix=json.dumps(np.round(SNAP, 5).tolist()),    # (rounds/weight_every) x 12 effective-weight matrix
        p_dec_every_matrix=json.dumps(np.round(SNAP_PD, 5).tolist()),
        theta_shape=json.dumps([PROXY_L, q]),
        theta_final=jj(theta),                                    # trained QNN parameter matrix (L x q)
        crit_mult=jj(crit_mult),                                  # Innovation-1 chip-pinning factor per parameter
    )
    if log_weights:                                               # full matrices, only for the showcase runs
        wx["w_eff_matrix"] = json.dumps(np.round(W, 5).tolist())              # rounds x 12
        wx["p_dec_matrix"] = json.dumps(np.round(PD, 5).tolist())             # rounds x 12
        wx["w_innov_matrix"] = json.dumps(np.round(PI, 5).tolist())           # (rounds*K) x 12
        wx["mem_matrix"] = json.dumps(np.round(mem, 6).tolist())              # 12 x P drift memory
    return dict(scale=scale, arm=arm, alpha=alpha, channel=channel, seed=seed, variant=variant, compile=compile_key,
                **wx,
                acc_final=acc[-1], acc_tail=float(np.mean(acc[-3:])), acc_curve=json.dumps([round(a, 4) for a in acc]),
                drift=float(np.mean(log["drift"])), drift_tail=float(np.mean(log["drift"][-rounds // 3:])),
                scda=float(np.mean(log["scda"])), bad_share=float(np.mean(log["skew"])), att_ratio=float(np.median(log["att"])),
                rec_err=float(np.mean(log["rec"])), active_mean=float(np.mean(log["active"])),
                mismatch=float(np.mean(log["mism"])) if log["mism"] else float("nan"),
                gamma_orph=float(np.mean(log["gorph"])) if log["gorph"] else float("nan"),
                drift_curve=json.dumps([round(x, 6) for x in log["drift"]]),
                eps_mean=float(np.mean(eps)), eps_bad=float(np.mean(eps[8:])),
                m2_shift=float(np.mean(log["m2"][-max(1, len(log["m2"]) // 6):])),
                hash_u=hashlib.md5(b"".join(h_u_buf)).hexdigest()[:12],
                hash_z=hashlib.md5(b"".join(h_z_buf)).hexdigest()[:12])


# ----------------------------------------------------------------------------------------------- noiseless reference (m2, ceiling)
def noiseless_reference(scale, compile_tbl, data, seeds=(0, 1), **over):
    """CLEAN fleet (eps = 0), exactly as v2: m2 = tail mean of E[F_ideal^2] at the shifted circuits along the noiseless training
    trajectory (needed by the sigma^2 formula) + the accuracy ceiling.  No noisy accuracy is involved in calibrating lambda."""
    cal = {scale: dict(lam=0.0, m2=0.5)}
    rows = [run_one(scale, "CLEAN", 100, "good", s, "base", compile_tbl, data, cal, **over) for s in seeds]
    return dict(m2=float(np.mean([r["m2_shift"] for r in rows])), acc=float(np.mean([r["acc_tail"] for r in rows])),
                curves=[json.loads(r["acc_curve"]) for r in rows])


# ----------------------------------------------------------------------------------------------- theory checks (Lemmas 2-4)
def theory_checks(cal, compile_tbl, scales, n_mc=200000, seed=0):
    rng = np.random.default_rng(seed); out = {}
    # Lemma 2 - residual attenuation of R-FD, per scale / per tier, analytic + Monte-Carlo
    L2 = []
    for s in scales:
        m2 = cal[s]["m2"]; eps = fleet_eps(compile_tbl["%s|none" % s], s, "A3", cal[s]["lam"], m2)
        for tier, e in (("Good", eps[0]), ("Medium", eps[4]), ("Bad", eps[8])):
            F = rng.choice([-1, 1], n_mc) * math.sqrt(m2)                    # E[F^2] = m2
            sig = math.sqrt(sigma2_of_eps(e, m2)); noisy = math.exp(-e) * F + sig * rng.standard_normal(n_mc)
            kap = float(deconv_gain(e, m2)); dlt_an = 1 - kap * math.exp(-e)
            dlt_mc = 1 - float(np.mean(kap * noisy * F) / np.mean(F * F))
            mse_raw = float(np.mean((noisy - F) ** 2)); mse_inv = float(np.mean((noisy * math.exp(e) - F) ** 2))
            mse_rfd = float(np.mean((kap * noisy - F) ** 2))
            L2.append(dict(scale=s, tier=tier, eps=float(e), attenuation=math.exp(-e), kappa=kap, delta_analytic=dlt_an, delta_mc=dlt_mc,
                           drift_removed_pct=100 * (1 - dlt_an / (1 - math.exp(-e))), mse_raw=mse_raw, mse_naive_inv=mse_inv, mse_rfd=mse_rfd))
    out["lemma2"] = L2
    # Lemma 3 - subset mismatch of M5a vs DR-JPS and active-client count (Monte-Carlo over channel draws)
    L3 = []
    for ch, p in CHANNEL_P.items():
        A = rng.normal(0, 1, (4000, N_CLIENTS)); mu = A + 0.35 * rng.normal(0, 1, A.shape)      # rho_corr ~ 0.94
        Ld = rng.random(A.shape) < p; Rd = rng.random(A.shape) < p; ok = Ld.any(1) & Rd.any(1)
        m5a = 0.5 * ((A * Ld).sum(1) / np.maximum(Ld.sum(1), 1) - (A * Rd).sum(1) / np.maximum(Rd.sum(1), 1))
        Pd = Ld & Rd; OL = Ld & ~Rd; OR = Rd & ~Ld; Aact = Ld | Rd
        res = np.where(OL, 0.5 * (A - mu), np.where(OR, -0.5 * (A - mu), 0.0))
        dr = res.sum(1) / np.maximum(Aact.sum(1), 1)
        L3.append(dict(channel=ch, p_dec=p, mism_m5a_mc=float(np.mean(m5a[ok] ** 2)),
                       mism_m5a_formula=float((1 - p) / (2 * N_CLIENTS * p) * np.var(A)),
                       mism_drjps_mc=float(np.mean(dr ** 2)), N_eff_m5b=float(Pd.sum(1).mean()), N_eff_m5b_formula=N_CLIENTS * p * p,
                       N_eff_drjps=float(Aact.sum(1).mean()), N_eff_drjps_formula=N_CLIENTS * p * (2 - p)))
    out["lemma3"] = L3
    # Lemma 4 - partial-participation drift with / without drift memory (heterogeneous clients, slowly moving gradients)
    L4 = []
    for p in (0.82, 0.63, 0.31):
        g_star = rng.normal(0, 1, N_CLIENTS); T = 400; mem = np.zeros(N_CLIENTS); e_ml, e_mem = [], []
        for t in range(T):
            g_t = g_star + 0.02 * t / T + 0.05 * rng.normal(0, 1, N_CLIENTS)
            act = rng.random(N_CLIENTS) < p * (2 - p)
            if not act.any(): continue
            e_ml.append((g_t[act].mean() - g_t.mean()) ** 2)
            est = mem.mean() + (g_t[act] - mem[act]).mean(); e_mem.append((est - g_t.mean()) ** 2)
            mem[act] = 0.4 * mem[act] + 0.6 * g_t[act]
        L4.append(dict(p_dec=p, drift_memoryless=float(np.mean(e_ml[50:])), drift_fedqdrift=float(np.mean(e_mem[50:]))))
    out["lemma4"] = L4
    return out


# ----------------------------------------------------------------------------------------------- acceptance gates
def run_gates(gate1, cal, compile_tbl, data, scales):
    res = []
    add = lambda n, ok, d: res.append((n, bool(ok), d))
    add("GATE 1  gamma'=0 DMapS compile identical to 'none' (S_local, E_link, cost, circuit hash)", all(gate1.values()), gate1)
    for s in scales:
        c = cal[s]; G, M, Bd = c["realised"]
        add("GATE 2  %-6s lambda calibrated on sigma^2 only: Bad<=%.2f, Good>=%.2f" % (s, c["bad_max"], c["good_min"]),
            Bd <= c["bad_max"] + 1e-9 and G >= c["good_min"] - 1e-9, "G/M/B sigma2*M = %.3f/%.3f/%.3f  lambda=%.4g" % (G, M, Bd, c["lam"]))
    d3 = [abs(sigma2_of_eps(fleet_eps(compile_tbl["%s|none" % s], s, "A0_A3", cal[s]["lam"], cal[s]["m2"]), cal[s]["m2"]).mean()
              - sigma2_of_eps(fleet_eps(compile_tbl["%s|none" % s], s, "A3", cal[s]["lam"], cal[s]["m2"]), cal[s]["m2"]).mean()) for s in scales]
    add("GATE 3  A0_A3 mean sigma^2 == A3 mean sigma^2", max(d3) < 1e-9, "max |diff| %.1e" % max(d3))
    s0 = scales[0]; kw = dict(rounds=3, K=2, eval_every=3)
    a = run_one(s0, "A3", 25, "poor", 7, "CDQ", compile_tbl, data, cal, **kw); b = run_one(s0, "A3", 25, "poor", 7, "CDQ", compile_tbl, data, cal, **kw)
    add("GATE 4  same seed + same method -> bit-identical results", a["acc_curve"] == b["acc_curve"] and a["drift"] == b["drift"], "")
    bs = run_one(s0, "A3", 25, "poor", 7, "base", compile_tbl, data, cal, **kw)
    add("GATE 5  CD-QFed vs base: identical channel uniforms and shot draws (CRN)", a["hash_u"] == bs["hash_u"] and a["hash_z"] == bs["hash_z"],
        "u %s/%s  z %s/%s" % (a["hash_u"], bs["hash_u"], a["hash_z"], bs["hash_z"]))
    ok6 = all(np.all((sigma2_of_eps(fleet_eps(compile_tbl["%s|none" % s], s, arm, cal[s]["lam"], cal[s]["m2"]), cal[s]["m2"]) >= 0) &
                     (sigma2_of_eps(fleet_eps(compile_tbl["%s|none" % s], s, arm, cal[s]["lam"], cal[s]["m2"]), cal[s]["m2"]) <= 1 / M_SHOTS))
              for s in scales for arm in ("A1", "A2", "A3", "A3adv", "A0_A3"))
    add("GATE 6  all sigma^2 in [0, 1/M]", ok6, "")
    bt = selftest_backend()
    add("GATE 8  statevector backend self-test (torch/cuda kernels == numpy kernels)", bt["max_abs_diff"] < 2e-4,
        "backend=%s  max|diff|=%.2e%s" % (bt["backend"], bt["max_abs_diff"], "" if bt["checked"] else "  (numpy backend: nothing to compare)"))
    sel = {s: select_fsnr_compile(compile_tbl, s, "A3", cal[s]["lam"], cal[s]["m2"]) for s in scales}
    add("GATE 7  DMapS-FSNR selection never worse than baseline compile (predicted Psi_NSR)",
        all(v[2][v[0]] <= v[2]["none"] + 1e-12 for v in sel.values()), {s: (v[0], {k: round(x, 4) for k, x in v[2].items()}) for s, v in sel.items()})
    print("=" * 110); print("ACCEPTANCE GATES")
    for n, ok, d in res: print("[%s] %s\n       %s" % ("x" if ok else " ", n, d))
    print("=" * 110)
    return res


# ----------------------------------------------------------------------------------------------- resumable sweep
CFG_KEY = ("scale", "arm", "alpha", "channel", "seed", "variant")
cfg_key = lambda c: "__".join(str(x) for x in c)


def read_csv_safe(path, **kw):
    """a results file whose last row was torn by a killed session must not cost us the other 10 000 rows."""
    import pandas as pd
    if not os.path.exists(path) or os.path.getsize(path) == 0: return None
    for attempt in (dict(), dict(on_bad_lines="skip"), dict(on_bad_lines="skip", engine="python")):
        try:
            return pd.read_csv(path, **dict(kw, **attempt))
        except Exception:
            continue
    return None


def load_done(patterns):
    """every config that ALREADY has a result row, across every shard CSV and merged results file of this notebook -
    including the rows restored from a previous Kaggle session.  This is what makes the sweep resumable."""
    done = set()
    for pat in patterns:
        for f in sorted(glob.glob(pat)):
            d = read_csv_safe(f, usecols=list(CFG_KEY))
            if d is None or d.empty: continue
            done |= set(map(tuple, d[list(CFG_KEY)].astype(str).values.tolist()))
    return done


def claim(claims_dir, key):
    """atomic O_EXCL claim.  Exactly one worker can own a config, so every worker may pull from ONE shared pool
    instead of a fixed interleaved shard: the GPUs stay busy even though a `large` config costs ~15x a `small` one."""
    if not claims_dir: return True
    try:
        fd = os.open(os.path.join(claims_dir, key + ".claim"), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, ("%d %s" % (os.getpid(), time.strftime("%Y-%m-%dT%H:%M:%S"))).encode()); os.close(fd)
        return True
    except FileExistsError:
        return False
    except OSError:
        return True


def unclaim(claims_dir, key):
    if not claims_dir: return
    try: os.remove(os.path.join(claims_dir, key + ".claim"))
    except OSError: pass


def sweep(csv_path, compile_tbl, data, cal, cfgs, done=None, claims_dir=None, deadline=None,
          ckpt_dir=None, ckpt_every=0, ckpt_scales=(), tag="", report_every=10, **kw):
    """Run configs and append ONE CSV row per finished run - that row carries the run's learned theta, its weight
    matrices and its metrics, so the CSV IS the intermediate-results store.

      done        configs already finished in this or any previous session -> skipped
      claims_dir  shared claim pool (dynamic scheduling); None -> this worker owns `cfgs` exclusively
      deadline    unix time after which no NEW config is started; a run already in flight with a checkpoint
                  saves its round-level state and stops, to be picked up by the next session
      ckpt_dir / ckpt_every / ckpt_scales   round-level checkpointing for the expensive scales
    """
    import pandas as pd
    done = set(done or ())
    d = read_csv_safe(csv_path, usecols=list(CFG_KEY))
    if d is not None and not d.empty:
        done |= set(map(tuple, d[list(CFG_KEY)].astype(str).values.tolist()))
    todo = [c for c in cfgs if tuple(map(str, c)) not in done]
    t0 = time.time(); n_run = 0; stopped = ""
    print("sweep%s: %d configs in the pool, %d already finished, %d to go"
          % (tag, len(cfgs), len(cfgs) - len(todo), len(todo)), flush=True)
    for c in todo:
        sc, arm, al, ch, sd, var = c
        key = cfg_key(c)
        if deadline is not None and time.time() > deadline:
            stopped = "session budget reached"; break
        if not claim(claims_dir, key):
            continue                                        # another worker already owns this config
        ck = os.path.join(ckpt_dir, key + ".pkl.gz") if (ckpt_dir and ckpt_every and sc in ckpt_scales) else None
        try:
            row = run_one(sc, arm, al, ch, sd, var, compile_tbl, data, cal,
                          ckpt_path=ck, ckpt_every=ckpt_every, deadline=deadline, **kw)
        except SessionTimeUp as e:
            print("  %s" % e, flush=True)
            unclaim(claims_dir, key)                        # its checkpoint stays: next session resumes mid-run
            stopped = "session budget reached mid-run"; break
        except Exception as e:
            print("  !! %s FAILED: %r" % (key, e), flush=True); unclaim(claims_dir, key); continue
        hdr = (not os.path.exists(csv_path)) or os.path.getsize(csv_path) == 0
        txt = pd.DataFrame([row]).to_csv(index=False, header=hdr)
        with open(csv_path, "a", newline="") as fh:     # one write + fsync: a killed session cannot tear a row
            fh.write(txt); fh.flush(); os.fsync(fh.fileno())
        n_run += 1
        if n_run % max(1, report_every) == 0:
            print("  %s: %d runs written, %.0f s elapsed, %.1f s/run" % (tag or "sweep", n_run, time.time() - t0,
                                                                         (time.time() - t0) / n_run), flush=True)
    print("sweep%s finished: %d runs in %.0fs%s" % (tag, n_run, time.time() - t0,
                                                    ("  [%s]" % stopped) if stopped else ""), flush=True)
    return n_run
