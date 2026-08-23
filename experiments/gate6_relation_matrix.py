from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sunday.composition import (  # noqa: E402
    CompositionConfig,
    MATCHING_1,
    MATCHING_2,
    run_seed,
    terminal_counts,
)


SEED_START = 380000
SEED_COUNT = 10

POOLED_SIGN_FRACTION_MIN = 0.90
MEAN_SIGNED_CONTRAST_MIN = 0.00070
TRAINED_UNUSED_RATIO_MIN = 5.0
SHUFFLE_RATIO_MAX = 0.35
MASS_ERROR_MAX = 1e-10


def summarize(rows: list[dict], cfg: CompositionConfig) -> dict:
    sign_fraction = float(np.mean([
        row_entry["dI"] > 0.0 if row_entry["class"] == "M1" else row_entry["dI"] < 0.0
        for row in rows
        for row_entry in row["rows"]
        if row_entry["class"] != "unused"
    ]))

    signed_contrast = np.asarray([row["mean_signed_contrast"] for row in rows], dtype=np.float64)
    trained_abs = np.asarray([row["trained_abs_mean"] for row in rows], dtype=np.float64)
    unused_abs = np.asarray([row["unused_abs_mean"] for row in rows], dtype=np.float64)
    shuffle_signed = np.asarray([row["shuffle_signed_contrast"] for row in rows], dtype=np.float64)

    mean_signed = float(signed_contrast.mean())
    trained_unused_ratio = float(trained_abs.mean() / max(unused_abs.mean(), 1e-15))
    shuffle_ratio = float(abs(shuffle_signed.mean()) / max(abs(mean_signed), 1e-15))

    metrics = {
        "seed_start": int(rows[0]["seed"]) if rows else None,
        "seed_count": len(rows),
        "matching_1_counts": terminal_counts(MATCHING_1),
        "matching_2_counts": terminal_counts(MATCHING_2),
        "pooled_expected_sign_fraction": sign_fraction,
        "fraction_seeds_all_6_signs": float(np.mean([
            row["expected_sign_fraction"] == 1.0 for row in rows
        ])),
        "mean_signed_contrast": mean_signed,
        "mean_trained_abs_differential": float(trained_abs.mean()),
        "mean_unused_abs_differential": float(unused_abs.mean()),
        "trained_vs_unused_abs_ratio": trained_unused_ratio,
        "mean_shuffle_signed_contrast": float(shuffle_signed.mean()),
        "shuffle_signed_contrast_ratio": shuffle_ratio,
        "max_per_seed_shuffle_ratio": float(max(row["shuffle_contrast_ratio"] for row in rows)),
        "min_signed_edge_overall": float(min(row["min_signed_edge"] for row in rows)),
        "max_mass_budget_error": float(max(
            max(abs(row["mass_sum_T1"] - cfg.mass_budget), abs(row["mass_sum_T2"] - cfg.mass_budget))
            for row in rows
        )),
        "all_finite": bool(np.all(np.isfinite([
            value
            for row in rows
            for pair in row["rows"]
            for value in (pair["interaction_T1"], pair["interaction_T2"], pair["dI"])
        ]))),
    }

    checks = {
        "programs_match_terminal_marginals": metrics["matching_1_counts"] == metrics["matching_2_counts"],
        "all_finite": metrics["all_finite"],
        "mass_budget_exact": metrics["max_mass_budget_error"] < MASS_ERROR_MAX,
        "pooled_sign_fraction": sign_fraction >= POOLED_SIGN_FRACTION_MIN,
        "mean_signed_contrast": mean_signed >= MEAN_SIGNED_CONTRAST_MIN,
        "trained_edges_stand_out": trained_unused_ratio >= TRAINED_UNUSED_RATIO_MIN,
        "mass_shuffle_destroys_contrast": shuffle_ratio <= SHUFFLE_RATIO_MAX,
    }

    return {
        "metrics": metrics,
        "checks": checks,
        "gate_pass": bool(all(checks.values())),
        "thresholds": {
            "pooled_expected_sign_fraction_min": POOLED_SIGN_FRACTION_MIN,
            "mean_signed_contrast_min": MEAN_SIGNED_CONTRAST_MIN,
            "trained_vs_unused_abs_ratio_min": TRAINED_UNUSED_RATIO_MIN,
            "shuffle_signed_contrast_ratio_max": SHUFFLE_RATIO_MAX,
            "mass_budget_error_max": MASS_ERROR_MAX,
        },
        "per_seed": rows,
    }


def run_gate(seed_start: int = SEED_START, seed_count: int = SEED_COUNT) -> dict:
    cfg = CompositionConfig()
    rows = [run_seed(seed_start + i, cfg) for i in range(seed_count)]
    return summarize(rows, cfg)


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
        print("Gate 6 — relation-matrix composition")
        print(f"pooled trained-edge sign     {m['pooled_expected_sign_fraction']:.3f}")
        print(f"all-6 seed fraction          {m['fraction_seeds_all_6_signs']:.3f}")
        print(f"mean signed contrast         {m['mean_signed_contrast']:.6f}")
        print(f"trained/unused |dI|          {m['trained_vs_unused_abs_ratio']:.2f}x")
        print(f"shuffle contrast ratio       {m['shuffle_signed_contrast_ratio']:.3f}")
        for name, ok in receipt["checks"].items():
            print(f"{'PASS' if ok else 'FAIL'}  {name}")
        print(f"GATE 6: {'PASS' if receipt['gate_pass'] else 'FAIL'}")

    raise SystemExit(0 if receipt["gate_pass"] else 1)


if __name__ == "__main__":
    main()
