from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sunday.composition import CompositionConfig  # noqa: E402
from sunday.relation_tomography import (  # noqa: E402
    analyze_seed,
    design_controls,
    principal_cosines,
    run_seed,
)


SEED_START = 440000
SEED_COUNT = 4

FULL_NMSE_MAX = 0.020
FULL_COSINE_MIN = 0.980
FULL_TO_SCALAR_MAX = 0.10
FULL_TO_DIAGONAL_MAX = 0.10
TOP3_ENERGY_MIN = 0.90
RANK3_NMSE_MAX = 0.10
RANK3_COSINE_MIN = 0.90
INPUT_MODE_MIN_COSINE_MIN = 0.75
MASS_ERROR_MAX = 1e-10


def summarize(raw_rows: list[dict], cfg: CompositionConfig) -> dict:
    design = design_controls()
    rows = [analyze_seed(row, rank_k=3) for row in raw_rows]

    full_nmse = np.asarray([row["full_loo_nmse"] for row in rows])
    full_cos = np.asarray([row["full_loo_mean_cosine"] for row in rows])
    scalar_nmse = np.asarray([row["scalar_loo_nmse"] for row in rows])
    diagonal_nmse = np.asarray([row["diagonal_loo_nmse"] for row in rows])
    rank3_nmse = np.asarray([row["rankk_loo_nmse"] for row in rows])
    rank3_cos = np.asarray([row["rankk_loo_mean_cosine"] for row in rows])
    top3_energy = np.asarray([row["topk_energy_fraction"] for row in rows])

    pair_cosines = []
    for left, right in combinations(rows, 2):
        a = np.asarray(left["input_modes_topk"], dtype=np.float64)
        b = np.asarray(right["input_modes_topk"], dtype=np.float64)
        cs = principal_cosines(a, b)
        pair_cosines.append({
            "seed_a": left["seed"],
            "seed_b": right["seed"],
            "cosines": cs.tolist(),
            "minimum": float(cs.min()),
        })

    mean_full = float(full_nmse.mean())
    mean_scalar = float(scalar_nmse.mean())
    mean_diagonal = float(diagonal_nmse.mean())
    mean_min_principal = float(np.mean([pair["minimum"] for pair in pair_cosines]))

    metrics = {
        "seed_start": int(rows[0]["seed"]) if rows else None,
        "seed_count": len(rows),
        "code_count": design["code_count"],
        "registered_input_rank": design["rank"],
        "minimum_loo_training_rank": design["all_loo_rank"],
        "mean_full_loo_nmse": mean_full,
        "mean_full_loo_cosine": float(full_cos.mean()),
        "mean_scalar_loo_nmse": mean_scalar,
        "mean_diagonal_loo_nmse": mean_diagonal,
        "full_to_scalar_nmse_ratio": float(mean_full / max(mean_scalar, 1e-30)),
        "full_to_diagonal_nmse_ratio": float(mean_full / max(mean_diagonal, 1e-30)),
        "mean_top3_energy_fraction": float(top3_energy.mean()),
        "mean_rank3_loo_nmse": float(rank3_nmse.mean()),
        "mean_rank3_loo_cosine": float(rank3_cos.mean()),
        "mean_pairwise_minimum_top3_input_principal_cosine": mean_min_principal,
        "max_mass_budget_error": float(max(row["max_mass_budget_error"] for row in rows)),
        "all_finite": bool(all(row["all_finite"] for row in rows)),
        "pairwise_input_mode_cosines": pair_cosines,
    }

    checks = {
        "design_code_count": design["code_count"] == 16,
        "design_rank": design["rank"] == 7,
        "loo_training_rank": design["all_loo_rank"] == 7,
        "mass_budget_exact": metrics["max_mass_budget_error"] < MASS_ERROR_MAX,
        "all_finite": metrics["all_finite"],
        "full_linear_loo_nmse": metrics["mean_full_loo_nmse"] <= FULL_NMSE_MAX,
        "full_linear_loo_cosine": metrics["mean_full_loo_cosine"] >= FULL_COSINE_MIN,
        "full_beats_scalar": metrics["full_to_scalar_nmse_ratio"] <= FULL_TO_SCALAR_MAX,
        "full_beats_diagonal": metrics["full_to_diagonal_nmse_ratio"] <= FULL_TO_DIAGONAL_MAX,
        "top3_energy": metrics["mean_top3_energy_fraction"] >= TOP3_ENERGY_MIN,
        "rank3_loo_nmse": metrics["mean_rank3_loo_nmse"] <= RANK3_NMSE_MAX,
        "rank3_loo_cosine": metrics["mean_rank3_loo_cosine"] >= RANK3_COSINE_MIN,
        "input_mode_stability": metrics["mean_pairwise_minimum_top3_input_principal_cosine"] >= INPUT_MODE_MIN_COSINE_MIN,
    }

    return {
        "metrics": metrics,
        "checks": checks,
        "gate_pass": bool(all(checks.values())),
        "thresholds": {
            "full_nmse_max": FULL_NMSE_MAX,
            "full_cosine_min": FULL_COSINE_MIN,
            "full_to_scalar_max": FULL_TO_SCALAR_MAX,
            "full_to_diagonal_max": FULL_TO_DIAGONAL_MAX,
            "top3_energy_min": TOP3_ENERGY_MIN,
            "rank3_nmse_max": RANK3_NMSE_MAX,
            "rank3_cosine_min": RANK3_COSINE_MIN,
            "input_mode_min_cosine_min": INPUT_MODE_MIN_COSINE_MIN,
            "mass_error_max": MASS_ERROR_MAX,
        },
        "design": design,
        "per_seed": rows,
    }


def run_gate(seed_start: int = SEED_START, seed_count: int = SEED_COUNT) -> dict:
    cfg = CompositionConfig()
    raw = [run_seed(seed_start + i, cfg) for i in range(seed_count)]
    return summarize(raw, cfg)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed-start", type=int, default=SEED_START)
    ap.add_argument("--seeds", type=int, default=SEED_COUNT)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    receipt = run_gate(args.seed_start, args.seeds)
    if args.json:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    else:
        m = receipt["metrics"]
        print("Gate 9 — writable-subspace tomography")
        print(f"codes / input rank          {m['code_count']} / {m['registered_input_rank']}")
        print(f"full LOO NMSE / cosine      {m['mean_full_loo_nmse']:.6f} / {m['mean_full_loo_cosine']:.5f}")
        print(f"scalar / diagonal NMSE      {m['mean_scalar_loo_nmse']:.4f} / {m['mean_diagonal_loo_nmse']:.4f}")
        print(f"top-3 operator energy       {m['mean_top3_energy_fraction']:.4f}")
        print(f"rank-3 LOO NMSE / cosine    {m['mean_rank3_loo_nmse']:.5f} / {m['mean_rank3_loo_cosine']:.5f}")
        print(f"input-mode min cosine mean  {m['mean_pairwise_minimum_top3_input_principal_cosine']:.4f}")
        for name, ok in receipt["checks"].items():
            print(f"{'PASS' if ok else 'FAIL'}  {name}")
        print(f"GATE 9: {'PASS' if receipt['gate_pass'] else 'FAIL'}")

    raise SystemExit(0 if receipt["gate_pass"] else 1)


if __name__ == "__main__":
    main()
