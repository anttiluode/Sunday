from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sunday.composition import CompositionConfig  # noqa: E402
from sunday.dormant_jacobian import analyze_seed  # noqa: E402


SEED_START = 460000
SEED_COUNT = 4
EPSILON = 0.25
GLOBAL_GAIN = 4.805610803751662

PRIMARY_NMSE_MAX = 0.15
PRIMARY_COSINE_MIN = 0.90
DORMANT_TOP3_ENERGY_MIN = 0.90
MODE_WEAKEST_COSINE_MIN = 0.85
PRIMARY_TO_WRITE_MAX = 0.25
PRIMARY_TO_PERM_MAX = 0.35
MASS_ERROR_MAX = 1e-10


def summarize(rows: list[dict]) -> dict:
    primary_nmse = np.asarray([row["primary_frozen_gain_nmse"] for row in rows])
    primary_cos = np.asarray([row["primary_mean_direction_cosine"] for row in rows])
    top3 = np.asarray([row["dormant_top3_energy_fraction"] for row in rows])
    weak_mode = np.asarray([
        row["dormant_vs_finite_weakest_top3_input_cosine"] for row in rows
    ])
    write_nmse = np.asarray([row["write_only_nmse"] for row in rows])
    perm_nmse = np.asarray([row["permuted_nmse"] for row in rows])

    mean_primary = float(primary_nmse.mean())
    mean_write = float(write_nmse.mean())
    mean_perm = float(perm_nmse.mean())

    metrics = {
        "seed_start": int(rows[0]["seed"]) if rows else None,
        "seed_count": len(rows),
        "epsilon": EPSILON,
        "global_gain": GLOBAL_GAIN,
        "mean_primary_frozen_gain_nmse": mean_primary,
        "mean_primary_direction_cosine": float(primary_cos.mean()),
        "mean_primary_flattened_cosine": float(np.mean([
            row["primary_flattened_cosine"] for row in rows
        ])),
        "mean_diagnostic_optimal_seed_nmse": float(np.mean([
            row["diagnostic_optimal_seed_nmse"] for row in rows
        ])),
        "mean_dormant_top3_energy_fraction": float(top3.mean()),
        "mean_weakest_dormant_vs_finite_top3_input_cosine": float(weak_mode.mean()),
        "mean_write_only_nmse": mean_write,
        "mean_permuted_nmse": mean_perm,
        "primary_to_write_nmse_ratio": float(mean_primary / max(mean_write, 1e-30)),
        "primary_to_permuted_nmse_ratio": float(mean_primary / max(mean_perm, 1e-30)),
        "all_permutations_preserve_write_gram": bool(all(
            row["write_gram_preserved_by_permutation"] for row in rows
        )),
        "max_one_step_write_mass_sum_error": float(max(
            row["max_one_step_write_mass_sum_error"] for row in rows
        )),
        "max_finite_mass_budget_error": float(max(
            row["max_finite_mass_budget_error"] for row in rows
        )),
        "all_finite": bool(all(row["all_finite"] for row in rows)),
    }

    checks = {
        "primary_zero_shot_nmse": metrics["mean_primary_frozen_gain_nmse"] <= PRIMARY_NMSE_MAX,
        "primary_zero_shot_cosine": metrics["mean_primary_direction_cosine"] >= PRIMARY_COSINE_MIN,
        "dormant_top3_energy": metrics["mean_dormant_top3_energy_fraction"] >= DORMANT_TOP3_ENERGY_MIN,
        "dormant_finite_mode_alignment": metrics["mean_weakest_dormant_vs_finite_top3_input_cosine"] >= MODE_WEAKEST_COSINE_MIN,
        "composite_beats_write_only": metrics["primary_to_write_nmse_ratio"] <= PRIMARY_TO_WRITE_MAX,
        "composite_beats_permuted_write": metrics["primary_to_permuted_nmse_ratio"] <= PRIMARY_TO_PERM_MAX,
        "permutation_preserves_write_gram": metrics["all_permutations_preserve_write_gram"],
        "one_step_mass_conserved": metrics["max_one_step_write_mass_sum_error"] < MASS_ERROR_MAX,
        "finite_mass_conserved": metrics["max_finite_mass_budget_error"] < MASS_ERROR_MAX,
        "all_finite": metrics["all_finite"],
    }

    return {
        "metrics": metrics,
        "checks": checks,
        "gate_pass": bool(all(checks.values())),
        "thresholds": {
            "primary_nmse_max": PRIMARY_NMSE_MAX,
            "primary_cosine_min": PRIMARY_COSINE_MIN,
            "dormant_top3_energy_min": DORMANT_TOP3_ENERGY_MIN,
            "mode_weakest_cosine_min": MODE_WEAKEST_COSINE_MIN,
            "primary_to_write_max": PRIMARY_TO_WRITE_MAX,
            "primary_to_permuted_max": PRIMARY_TO_PERM_MAX,
            "mass_error_max": MASS_ERROR_MAX,
        },
        "per_seed": rows,
    }


def run_gate(seed_start: int = SEED_START, seed_count: int = SEED_COUNT) -> dict:
    cfg = CompositionConfig()
    rows = [
        analyze_seed(
            seed_start + i,
            global_gain=GLOBAL_GAIN,
            epsilon=EPSILON,
            permutation_seed=970000 + seed_start + i,
            cfg=cfg,
        )
        for i in range(seed_count)
    ]
    return summarize(rows)


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
        print("Gate 10 — dormant write/read Jacobian")
        print(f"primary NMSE / cosine       {m['mean_primary_frozen_gain_nmse']:.5f} / {m['mean_primary_direction_cosine']:.5f}")
        print(f"dormant top-3 energy       {m['mean_dormant_top3_energy_fraction']:.4f}")
        print(f"weakest mode cosine mean   {m['mean_weakest_dormant_vs_finite_top3_input_cosine']:.4f}")
        print(f"write / perm NMSE          {m['mean_write_only_nmse']:.4f} / {m['mean_permuted_nmse']:.4f}")
        for name, ok in receipt["checks"].items():
            print(f"{'PASS' if ok else 'FAIL'}  {name}")
        print(f"GATE 10: {'PASS' if receipt['gate_pass'] else 'FAIL'}")

    raise SystemExit(0 if receipt["gate_pass"] else 1)


if __name__ == "__main__":
    main()
