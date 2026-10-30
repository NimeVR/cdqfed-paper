"""One CD-QFed sweep worker.

Stage 5 launches WORKERS_PER_GPU of these per GPU (Kaggle `GPU T4 x2` -> 2 GPUs x 2 = 4 processes), each with
CUDA_VISIBLE_DEVICES already set so torch sees exactly ONE device, and with the BLAS thread count pinned to 1 so
the four processes do not fight over the four vCPUs.

Scheduling.  With --claims the workers pull from ONE shared pool of configs, claiming each one atomically
(O_EXCL): the two GPUs stay saturated even though a `large` config costs ~15x a `small` one, and a worker that is
killed leaves no hole in the grid.  Without --claims the old fixed interleaved shard (cfgs[shard::nshards]) is used.

Resumability.  --done-glob tells the worker which CSVs already hold finished runs (this session's shards plus
everything restored from previous Kaggle sessions); those configs are skipped.  --deadline is the unix time after
which no NEW config is started, and --ckpt-dir/--ckpt-every let a long `large` run save its round-level state and
stop cleanly, so the next session continues that very run instead of redoing it.

The worker rebuilds COMPILE_TBL / CAL from the files Stage 2-3 wrote to disk, so its numbers are bit-identical to
the in-notebook path (same compile counts, same calibrated lambda, same keyed RNG).
"""
import os, sys, json, glob, argparse, time

os.environ.setdefault("PYTHONHASHSEED", "0")
for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, os.environ.get("CDQ_THREADS", "1"))      # set BEFORE numpy/torch are imported

ap = argparse.ArgumentParser()
ap.add_argument("--shard", type=int, default=0)
ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--cfgs", default="sweep_cfgs.json")
ap.add_argument("--csv", default="shard.csv")
ap.add_argument("--refs", default="")
ap.add_argument("--rounds", type=int, default=0)
ap.add_argument("--backend", default="auto")       # "numpy" | "torch/cuda" | "auto"
ap.add_argument("--weight-every", dest="weight_every", type=int, default=5)   # weight-matrix snapshot interval
ap.add_argument("--verify", default="")            # write a determinism probe to this json and exit
ap.add_argument("--claims", default="")            # shared claim directory -> dynamic scheduling
ap.add_argument("--deadline", type=float, default=0.0)        # unix time: start no new config after this
ap.add_argument("--ckpt-dir", dest="ckpt_dir", default="")    # round-level checkpoints for long runs
ap.add_argument("--ckpt-every", dest="ckpt_every", type=int, default=0)
ap.add_argument("--ckpt-scales", dest="ckpt_scales", default="large")
ap.add_argument("--done-glob", dest="done_glob", default="")  # comma-separated globs of CSVs holding finished runs
AR = ap.parse_args()

import numpy as np
import cdqfed_sim as Q

try:
    import torch; torch.set_num_threads(int(os.environ.get("CDQ_THREADS", "1")))
except Exception:
    pass

# ---- fix the backend explicitly: one results file must never mix numpy and cuda float-reduction orders
if AR.backend == "numpy":
    Q.USE_TORCH = False
elif AR.backend.startswith("torch"):
    Q.USE_TORCH = bool(Q.HAVE_TORCH and Q.DEV == "cuda")
st = Q.selftest_backend()                           # GATE 8 inside every worker
BACKEND = st["backend"]

# ---- rebuild the compile table exactly as Stage 2 did
COMPILE_TBL = {}
for f in sorted(glob.glob("compile/*.json")):
    sc, mode, g = os.path.basename(f)[:-5].split("_")
    d = json.load(open(f))
    if mode == "m1" and g == "none": COMPILE_TBL[f"{sc}|none"] = d
    if mode == "fsnr": COMPILE_TBL[f"{sc}|fsnr{float(g)}"] = d

data = Q.load_fmnist4()
refs_file = AR.refs or ("refs_%s.json" % BACKEND.replace("/", ""))
REFS = json.load(open(refs_file))
CAL = {s: Q.calibrate_lambda(s, COMPILE_TBL[f"{s}|none"], REFS[s]["m2"])
       for s in REFS if f"{s}|none" in COMPILE_TBL}
KW = dict(weight_every=AR.weight_every)
if AR.rounds: KW["rounds"] = AR.rounds

# ---- determinism probe: the same configs are run on every device and compared by the parent
if AR.verify:
    probe = [("small", "A3", 25, "poor", 0, "base"),
             ("small", "A3", 25, "poor", 0, "CDQ-lit"),
             ("small", "A3", 25, "poor", 0, "CDQ")]
    out = {}
    for cfg in probe:
        if cfg[0] not in {k.split("|")[0] for k in COMPILE_TBL}: continue
        r = Q.run_one(*cfg, COMPILE_TBL, data, CAL, rounds=12, eval_every=4, weight_every=AR.weight_every)
        out["|".join(map(str, cfg))] = {k: r[k] for k in
                                        ("acc_final", "acc_tail", "drift", "scda", "att_ratio", "hash_u", "hash_z")}
    out["_backend"] = BACKEND
    out["_device"] = os.environ.get("CUDA_VISIBLE_DEVICES", "")
    json.dump(out, open(AR.verify, "w"), indent=1)
    print("verify written ->", AR.verify, flush=True)
    sys.exit(0)

# ---- the pool this worker draws from
cfgs = [tuple(c) for c in json.load(open(AR.cfgs))]
if AR.claims:
    os.makedirs(AR.claims, exist_ok=True)
    mine, mode = cfgs, "dynamic pool"                 # everyone sees the whole list; claims decide who runs what
else:
    mine, mode = cfgs[AR.shard::AR.nshards], "static shard"

DONE = Q.load_done([p for p in AR.done_glob.split(",") if p.strip()]) if AR.done_glob else set()
if AR.ckpt_dir: os.makedirs(AR.ckpt_dir, exist_ok=True)

print(f"[worker {AR.shard}/{AR.nshards}] device={os.environ.get('CUDA_VISIBLE_DEVICES', 'cpu')} "
      f"backend={BACKEND} threads={os.environ.get('CDQ_THREADS', '1')} {mode}={len(mine)} "
      f"already-done={len(DONE)} -> {AR.csv}", flush=True)
t0 = time.time()
n = Q.sweep(AR.csv, COMPILE_TBL, data, CAL, mine,
            done=DONE, claims_dir=AR.claims or None,
            deadline=AR.deadline or None,
            ckpt_dir=AR.ckpt_dir or None, ckpt_every=AR.ckpt_every,
            ckpt_scales=tuple(s for s in AR.ckpt_scales.split(",") if s),
            tag=" [w%d]" % AR.shard, **KW)
print(f"[worker {AR.shard}] finished: {n} new rows in {time.time() - t0:.0f}s", flush=True)
