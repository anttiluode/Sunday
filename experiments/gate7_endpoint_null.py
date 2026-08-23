from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sunday.endpoint_null import run_seed  # noqa: E402


SEED_START = 400000
SEED_COUNT = 10

OBSERVED_SIGN_FRACTION_MIN = 0.90
MEAN_CYCLE_CONTRAST_MIN = 0.0042
MEAN_ADDITIVE_R2_MAX = 0.30
ADDITIVE_IN_SAMPLE_SIGN_MAX = 0.75
ADDITIVE_LOO_SIGN_MAX = 0.35
NEGATIVE_PRODUCT_FRACTION_MIN = 0.80
MASS_ERROR_MAX = 1e-10


def summarize(rows: list[dict]) -> dict:
    observed_sign = np.asarray([row["observed_trained_sign_fraction"] for row in rows])
    additive_r2 = np.asarray([row["additive_r2"] for row in rows])
    in_sample = np.asarray([row["additive_in_sample_trained_sign_accuracy"] for row in rows])
    loo = np.asarray([row["additive_loo_trained_sign_accuracy"] for row in rows])
    cycle = np.asarray([row["cycle_contrast"] for row in rows])

    metrics = {
        "seed_start": int(rows[0]["seed"]) if rows else None,
        "seed_count": len(rows),
        "pooled_observed_trained_sign_fraction": float(observed_sign.mean()),
        "mean_cycle_contrast": float(cycle.mean()),
        "min_cycle_contrast": float(cycle.min()),
        "mean_additive_r2": float(additive_r2.mean()),
        "max_additive_r2": float(additive_r2.max()),
        "pooled_additive_in_sample_trained_sign_accuracy": float(in_sample.mean()),
        "pooled_additive_loo_trained_sign_accuracy": float(loo.mean()),
        "negative_trained_cycle_product_fraction": float(np.mean([
            row["trained_cycle_product_negative"] for row in rows
        ])),
        "max_mass_budget_error": float(max(
            max(abs(row["mass_sum_T1"] - 256.0), abs(row["mass_sum_T2"] - 256.0))
            for row in rows
        )),
        "all_finite": bool(np.all(np.isfinite([
            value
            for row in rows
            for value in (
                row["additive_r2"],
                row["cycle_contrast"],
                row["trained_cycle_product"],
            )
        ]))),
    }

    checks = {
        "underlying_relation_code_present": metrics["pooled_observed_trained_sign_fraction"] >= OBSERVED_SIGN_FRACTION_MIN,
        "additive_cycle_invariant_violated": metrics["mean_cycle_contrast"] >= MEAN_CYCLE_CONTRAST_MIN,
        "additive_variance_explained_low": metrics["mean_additive_r2"] <= MEAN_ADDITIVE_R2_MAX,
        "additive_in_sample_sign_weak": metrics["pooled_additive_in_sample_trained_sign_accuracy"] <= ADDITIVE_IN_SAMPLE_SIGN_MAX,
        "additive_loo_sign_weak": metrics["pooled_additive_loo_trained_sign_accuracy"] <= ADDITIVE_LOO_SIGN_MAX,
        "multiplicative_sign_factor_frustrated": metrics["negative_trained_cycle_product_fraction"] >= NEGATIVE_PRODUCT_FRACTION_MIN,
        "mass_budget_exact": metrics["max_mass_budget_error"] < MASS_ERROR_MAX,
        "all_finite": metrics["all_finite"],
    }

    return {
        "metrics": metrics,
        "checks": checks,
        "gate_pass": bool(all(checks.values())),
        "thresholds": {
            "observed_sign_fraction_min": OBSERVED_SIGN_FRACTION_MIN,
            "mean_cycle_contrast_min": MEAN_CYCLE_CONTRAST_MIN,
            "mean_additive_r2_max": MEAN_ADDITIVE_R2_MAX,
            "additive_in_sample_sign_max": ADDITIVE_IN_SAMPLE_SIGN_MAX,
            "additive_loo_sign_max": ADDITIVE_LOO_SIGN_MAX,
            "negative_product_fraction_min": NEGATIVE_PRODUCT_FRACTION_MIN,
            "mass_error_max": MASS_ERROR_MAX,
        },
        "per_seed": rows,
    }


def run_gate(seed_start: int = SEED_START, seed_count: int = SEED_COUNT) -> dict:
    return summarize([run_seed(seed_start + i) for i in range(seed_count)])


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
        print("Gate 7 — endpoint-factor null attack")
        print(f"observed trained signs        {m['pooled_observed_trained_sign_fraction']:.3f}")
        print(f"cycle contrast mean           {m['mean_cycle_contrast']:.6f}")
        print(f"additive R2 mean/max          {m['mean_additive_r2']:.3f}/{m['max_additive_r2']:.3f}")
        print(f"additive sign in/LOO          {m['pooled_additive_in_sample_trained_sign_accuracy']:.3f}/{m['pooled_additive_loo_trained_sign_accuracy']:.3f}")
        print(f"negative cycle product        {m['negative_trained_cycle_product_fraction']:.3f}")
        for name, ok in receipt["checks"].items():
            print(f"{'PASS' if ok else 'FAIL'}  {name}")
        print(f"GATE 7: {'PASS' if receipt['gate_pass'] else 'FAIL'}")

    raise SystemExit(0 if receipt["gate_pass"] else 1)


if __name__ == "__main__":
    main()
