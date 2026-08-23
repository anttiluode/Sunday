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
from sunday.relation_generality import CODES, design_controls, run_seed  # noqa: E402


SEED_START = 420000
SEED_COUNT = 6

MEAN_SIGN_MIN = 0.80
MEAN_CONTRAST_MIN = 0.00050
MEAN_TRAINED_UNUSED_MIN = 2.0
MEAN_SPECIFICITY_MIN = 1.5
SELF_TOP_FRACTION_MIN = 0.75
POOLED_SHUFFLE_RATIO_MAX = 0.40
MASS_ERROR_MAX = 1e-10


def summarize(rows: list[dict], cfg: CompositionConfig) -> dict:
    design = design_controls()
    flat = [entry for row in rows for entry in row["codes"]]

    per_code = {}
    for code in CODES:
        entries = [entry for entry in flat if entry["code"] == code.name]
        own = np.asarray([entry["own_signed_contrast"] for entry in entries], dtype=np.float64)
        per_code[code.name] = {
            "mean_expected_sign_fraction": float(np.mean([
                entry["expected_sign_fraction"] for entry in entries
            ])),
            "mean_own_signed_contrast": float(own.mean()),
            "mean_trained_unused_ratio": float(np.mean([
                entry["trained_unused_ratio"] for entry in entries
            ])),
            "mean_specificity_ratio": float(np.mean([
                entry["specificity_ratio"] for entry in entries
            ])),
            "self_top_fraction": float(np.mean([
                entry["self_top"] for entry in entries
            ])),
            "mean_shuffle_ratio": float(np.mean([
                entry["shuffle_ratio"] for entry in entries
            ])),
        }

    original_abs = np.asarray([abs(entry["own_signed_contrast"]) for entry in flat])
    shuffled_abs = np.asarray([abs(entry["shuffle_own_signed_contrast"]) for entry in flat])
    pooled_shuffle_ratio = float(shuffled_abs.sum() / max(original_abs.sum(), 1e-15))

    max_mass_error = float(max(
        max(abs(entry["mass_sum_A"] - cfg.mass_budget), abs(entry["mass_sum_B"] - cfg.mass_budget))
        for entry in flat
    ))

    metrics = {
        "seed_start": int(rows[0]["seed"]) if rows else None,
        "seed_count": len(rows),
        "registered_code_rank": int(design["rank"]),
        "registered_dot_matrix": design["dot_matrix"],
        "per_code": per_code,
        "pooled_shuffle_ratio": pooled_shuffle_ratio,
        "max_mass_budget_error": max_mass_error,
        "all_finite": bool(np.all(np.isfinite([
            value
            for entry in flat
            for value in (
                entry["expected_sign_fraction"],
                entry["own_signed_contrast"],
                entry["trained_unused_ratio"],
                entry["specificity_ratio"],
                entry["shuffle_ratio"],
            )
        ]))),
    }

    design_ok = bool(
        design["rank"] == 4
        and all(
            item["terminal_marginals_match"]
            and item["distance_multiset_match"]
            and item["trained_edges_disjoint"]
            for item in design["per_code"].values()
        )
    )

    code_checks = {}
    for name, m in per_code.items():
        code_checks[name] = {
            "sign_fraction": m["mean_expected_sign_fraction"] >= MEAN_SIGN_MIN,
            "own_contrast": m["mean_own_signed_contrast"] >= MEAN_CONTRAST_MIN,
            "trained_edges_stand_out": m["mean_trained_unused_ratio"] >= MEAN_TRAINED_UNUSED_MIN,
            "code_specificity": m["mean_specificity_ratio"] >= MEAN_SPECIFICITY_MIN,
            "self_top": m["self_top_fraction"] >= SELF_TOP_FRACTION_MIN,
        }

    checks = {
        "design_controls": design_ok,
        "mass_budget_exact": max_mass_error < MASS_ERROR_MAX,
        "all_finite": metrics["all_finite"],
        "pooled_shuffle_destroys_contrast": pooled_shuffle_ratio <= POOLED_SHUFFLE_RATIO_MAX,
        "all_codes_robust": bool(all(
            ok
            for code_result in code_checks.values()
            for ok in code_result.values()
        )),
    }

    return {
        "metrics": metrics,
        "code_checks": code_checks,
        "checks": checks,
        "gate_pass": bool(all(checks.values())),
        "thresholds": {
            "mean_sign_fraction_min": MEAN_SIGN_MIN,
            "mean_own_contrast_min": MEAN_CONTRAST_MIN,
            "mean_trained_unused_ratio_min": MEAN_TRAINED_UNUSED_MIN,
            "mean_specificity_ratio_min": MEAN_SPECIFICITY_MIN,
            "self_top_fraction_min": SELF_TOP_FRACTION_MIN,
            "pooled_shuffle_ratio_max": POOLED_SHUFFLE_RATIO_MAX,
            "mass_error_max": MASS_ERROR_MAX,
        },
        "design": design,
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
    m = receipt["metrics"]

    if args.json:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    else:
        print("Gate 8 — independent relation codes")
        print(f"registered code rank          {m['registered_code_rank']}")
        for code in CODES:
            c = m["per_code"][code.name]
            print(
                f"{code.name} sign={c['mean_expected_sign_fraction']:.3f} "
                f"own={c['mean_own_signed_contrast']:.6f} "
                f"T/U={c['mean_trained_unused_ratio']:.2f}x "
                f"spec={c['mean_specificity_ratio']:.2f}x "
                f"top={c['self_top_fraction']:.3f}"
            )
        print(f"pooled shuffle ratio         {m['pooled_shuffle_ratio']:.3f}")
        for name, ok in receipt["checks"].items():
            print(f"{'PASS' if ok else 'FAIL'}  {name}")
        print(f"GATE 8: {'PASS' if receipt['gate_pass'] else 'FAIL'}")

    raise SystemExit(0 if receipt["gate_pass"] else 1)


if __name__ == "__main__":
    main()
