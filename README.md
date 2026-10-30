# CD-QFed — Channel-Decohered Quantum Federated Learning

Simulation study of the proposed **CDQ-lit** aggregation rule for quantum federated
learning over imperfect classical/quantum channels, benchmarked against a plain
federated baseline, JEQFL, and six ablation arms.

Status: **complete grid — 13,950 / 13,950 configurations.**
Run finished 2026-10-29 21:41 UTC, profile `paper`, backend `torch/cuda`.

> **Caveat carried over from the original run notes:** hardware error rates are
> `[PLACEHOLDER]` and the reported accuracies are **proxy** numbers, by design of
> the notebook. Treat accuracy as a relative signal between arms, not as an
> absolute classification result.

---

## Experimental grid

| Factor | Levels |
|---|---|
| Scale (proxy qubits) | `small` (10), `medium` (12), `large` (15) |
| Dirichlet non-IID α | 100, 50, 25 |
| Channel quality | `good` (p=0.82), `moderate` (p=0.63), `poor` (p=0.31) |
| Seeds | 0–9 (10 seeds) |
| Rounds | 60 (eval every 5, weights logged every 5) |
| Clients | 12, K=6 sampled per round, B=16, n_local=240, η₀=2.0 |
| Variants | `base`, `JEQFL`, `M2`, `M3`, `M4a`, `M4ab`, `M5b`, `CDQ`, `CDQ-lit` *(proposed)*, plus 10 innovation-ablation arms (`-noI1 … -noI4`) |

## Headline findings

Paired comparisons of **CDQ-lit** against the matched baseline (24 cells = 3 scales
× 3 alphas × 3 channels, pooled where noted):

| Metric | Significant improvement | Good trend (n.s.) | Bad trend |
|---|---|---|---|
| Accuracy | 14 | 10 | 0 |
| Client drift `E_drift` | 24 | 0 | 0 |
| Drift alignment `S_CDA` | 23 | 0 | 1 |

The consistent effect is on **drift, not accuracy**: CDQ-lit roughly halves client
drift (e.g. small scale 0.0238 → 0.0123; medium 0.0205 → 0.0132; large 0.0207 →
0.0129) and raises alignment `S_CDA` (0.281 → 0.351 at small scale), while accuracy
moves only slightly and never significantly downward. The unregularised `CDQ` arm
*increases* drift, which is what motivates the `-lit` shrinkage.

Full per-scale, per-channel and per-α tables are in
[`reports/experiment_notes.md`](reports/experiment_notes.md) and
[`outputs/tables/`](outputs/tables).

## Validation

All **11 acceptance gates passed** (see `outputs/tables/reproducibility.json`), including:

- **Gate 4** — same seed + same method → bit-identical results.
- **Gate 5** — CD-QFed and baseline share identical channel uniforms and shot draws (common random numbers).
- **Gate 9** — cross-device determinism, so the sharded multi-GPU sweep is sound.
- **Gate 1** — γ′=0 DMapS compile is identical to the `none` compile (circuit hash, cost, `S_local`, `E_link`).

Every random draw is keyed by `rng_for(seed, round, client, purpose)`, so a resumed
run is bit-identical to an uninterrupted one.

## Pipeline

```
data/raw/sweep_cfgs.json          grid definition (13,950 configs)
        │
        ▼
src/sweep_worker.py  ──►  src/cdqfed_sim.py          one worker per GPU
        │                 (λ calibration, channel model, CDQ-lit aggregation)
        ▼
data/processed/shards_paper_torchcuda/shard0{0..3}.csv
        │  concatenated
        ▼
data/processed/results_cdqfed_paper_torchcuda.csv    13,950 rows
        │  sha256 064aef6e…3fea (recorded in reproducibility.json)
        ▼
src/cdqfed_analysis.py  ──►  outputs/metrics/, outputs/tables/, figures/
```

The DMapS circuit-compilation branch (`src/dmaps_worker.py`, `src/patch_dmaps.py`)
runs in a separate Python 3.10 / Qiskit 0.39.2 environment; its results are cached
in `outputs/diagnostics/recorded_dmaps_compiles.json` and
`outputs/diagnostics/dmaps_compile/`, so the sweep can be reproduced without it.

## Environment

Python 3.13.15, numpy 2.1.3, pandas 2.3.3, scipy 1.16.3, matplotlib 3.10.0,
torch 2.11.0+cu128. Hardware: 2× Tesla T4, 4 CPU cores. See `requirements.txt`.

## Directory map

```
data/raw/           fmnist4.npz (dataset), sweep_cfgs.json (grid), refs_torchcuda.json
data/processed/     results_cdqfed_paper_torchcuda.csv + the 4 per-GPU shards
notebooks/          main_analysis.ipynb — end-to-end driver
figures/            78 publication figures, 300 DPI PNG
   pdf_vector/         the same 78 figures as vector PDF
   preview_130dpi/     81 screen-resolution PNGs from the original plots/ folder
   notebook_inline/    109 inline renders captured from the notebook run
outputs/metrics/    comparison, ablation, power and shrinkage tables
   epoch_weights/      81 per-(scale, α, variant) epoch-weight traces
   weight_diagnostics/ w_eff, w_static, κ, ε, σ², innovation and memory-norm traces
outputs/supplementary/  the 94-file supplementary CSV set from the journal pack
outputs/tables/     journal tables 1–13 (.csv + .tex), figure_index, reproducibility.json
outputs/diagnostics/ manifest, device verification, DMapS compile records
outputs/archives/   original packed bundles, plus their expanded contents:
   resume_state/       22 state files + manifest for bit-identical resume
   outputs_plots/      the 81 screen-resolution plots as originally bundled
outputs/logs/       raw per-worker console logs
reports/            experiment_notes.md — the full generated results report
src/                simulation, analysis and worker scripts
```

Note on figures: the original upload shipped two resolutions of the same 78 plots.
`figures/` holds the 300 DPI publication set (e.g. 4289×10043 px for the accuracy
curves); `figures/preview_130dpi/` holds the 130 DPI screen versions. Use the former
for submission.

## Reproducing

```bash
pip install -r requirements.txt
# Replay the analysis from the finished sweep:
python src/cdqfed_analysis.py
# Or re-run the full sweep (≈85 s/run × 13,950 configs across available GPUs):
python src/sweep_worker.py
```

`outputs/archives/cdqfed_resume_state.zip` holds the 22 state files (≈144 MB) that
let a partial sweep resume bit-identically.
