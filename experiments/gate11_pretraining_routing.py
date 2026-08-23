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
from sunday.pretraining_routing import (  # noqa: E402
    CANDIDATES,
    CANDIDATE_BY_VECTOR,
    TARGET_DISTANCES,
    UNIVERSAL_BEST,
    UNIVERSAL_WORST,
    design_controls,
    run_seed,
)


SEED_START = 480000
SEED_COUNT = 6

PEARSON_MIN = 0.70
SPEARMAN_MIN = 0.65
BEST_WORST_FRACTION_MIN = 5.0 / 6.0
BEST_WORST_RATIO_MIN = 2.5
PEARSON_ADVANTAGE_MIN = 0.40
SPEARMAN_ADVANTAGE_MIN = 0.35
MASS_ERROR_MAX = 1e-10


def _pearson(x: np.ndarray, y: np.ndarray) -> float:
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    if float(x.std()) <= 1e-15 or float(y.std()) <= 1e-15:
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])


def _ranks(x: np.ndarray) -> np.ndarray:
    """Average ranks for ties, zero-based scale irrelevant to correlation."""
    x = np.asarray(x, dtype=np.float64)
    order = np.argsort(x, kind="mergesort")
    ranks = np.empty(len(x), dtype=np.float64)
    start = 0
    while start < len(x):
        end = start + 1
        value = x[order[start]]
        while end < len(x) and x[order[end]] == value:
            end += 1
        ranks[order[start:end]] = 0.5 * (start + end - 1)
        start = end
    return ranks


def _spearman(x: np.ndarray, y: np.ndarray) -> float:
    return _pearson(_ranks(x), _ranks(y))


def analyze_seed(raw: dict, cfg: CompositionConfig) -> dict:
    scores = np.asarray(raw["scores"], dtype=np.float64)
    shuffle_scores = np.asarray(raw["shuffle_scores"], dtype=np.float64)
    own = np.asarray([
        entry["own_signed_contrast"] for entry in raw["finite"]
    ], dtype=np.float64)

    best = int(raw["best_index"])
    worst = int(raw["worst_index"])
    universal_best = CANDIDATES.index(CANDIDATE_BY_VECTOR[UNIVERSAL_BEST])
    universal_worst = CANDIDATES.index(CANDIDATE_BY_VECTOR[UNIVERSAL_WORST])

    mass_error = float(max(
        max(abs(entry["mass_sum_A"] - cfg.mass_budget),
            abs(entry["mass_sum_B"] - cfg.mass_budget))
        for entry in raw["finite"]
    ))

    return {
        "seed": int(raw["seed"]),
        "pearson": _pearson(scores, own),
        "spearman": _spearman(scores, own),
        "shuffle_pearson": _pearson(shuffle_scores, own),
        "shuffle_spearman": _spearman(shuffle_scores, own),
        "best_name": CANDIDATES[best].name,
        "worst_name": CANDIDATES[worst].name,
        "best_score": float(scores[best]),
        "worst_score": float(scores[worst]),
        "best_finite_contrast": float(own[best]),
        "worst_finite_contrast": float(own[worst]),
        "best_beats_worst": bool(own[best] > own[worst]),
        "universal_best_finite_contrast": float(own[universal_best]),
        "universal_worst_finite_contrast": float(own[universal_worst]),
        "max_finite_mass_budget_error": mass_error,
        "max_one_step_write_mass_sum_error": float(raw["max_one_step_write_mass_sum_error"]),
        "shuffle_preserves_singular_values": bool(raw["shuffle_preserves_singular_values"]),
        "all_finite": bool(
            np.all(np.isfinite(scores))
            and np.all(np.isfinite(shuffle_scores))
            and np.all(np.isfinite(own))
        ),
        "assignments": [
            {
                "name": CANDIDATES[i].name,
                "score": float(scores[i]),
                "shuffle_score": float(shuffle_scores[i]),
                "finite_own_contrast": float(own[i]),
                "expected_sign_fraction": float(raw["finite"][i]["expected_sign_fraction"]),
                "trained_unused_ratio": float(raw["finite"][i]["trained_unused_ratio"]),
            }
            for i in range(len(CANDIDATES))
        ],
    }


def summarize(raw_rows: list[dict], cfg: CompositionConfig) -> dict:
    design = design_controls()
    rows = [analyze_seed(row, cfg) for row in raw_rows]

    mean_pearson = float(np.mean([row["pearson"] for row in rows]))
    mean_spearman = float(np.mean([row["spearman"] for row in rows]))
    mean_shuffle_pearson = float(np.mean([row["shuffle_pearson"] for row in rows]))
    mean_shuffle_spearman = float(np.mean([row["shuffle_spearman"] for row in rows]))
    mean_best = float(np.mean([row["best_finite_contrast"] for row in rows]))
    mean_abs_worst = float(np.mean([abs(row["worst_finite_contrast"]) for row in rows]))

    controls = list(design["per_candidate"].values())
    metrics = {
        "seed_start": int(rows[0]["seed"]) if rows else None,
        "seed_count": len(rows),
        "candidate_count": design["candidate_count"],
        "mean_pearson": mean_pearson,
        "mean_spearman": mean_spearman,
        "mean_shuffle_pearson": mean_shuffle_pearson,
        "mean_shuffle_spearman": mean_shuffle_spearman,
        "pearson_advantage_over_shuffled": mean_pearson - mean_shuffle_pearson,
        "spearman_advantage_over_shuffled": mean_spearman - mean_shuffle_spearman,
        "fraction_best_beats_worst": float(np.mean([
            row["best_beats_worst"] for row in rows
        ])),
        "mean_best_finite_contrast": mean_best,
        "mean_absolute_worst_finite_contrast": mean_abs_worst,
        "pooled_best_to_abs_worst_ratio": float(mean_best / max(mean_abs_worst, 1e-15)),
        "mean_universal_best_finite_contrast": float(np.mean([
            row["universal_best_finite_contrast"] for row in rows
        ])),
        "mean_universal_worst_finite_contrast": float(np.mean([
            row["universal_worst_finite_contrast"] for row in rows
        ])),
        "max_finite_mass_budget_error": float(max(
            row["max_finite_mass_budget_error"] for row in rows
        )),
        "max_one_step_write_mass_sum_error": float(max(
            row["max_one_step_write_mass_sum_error"] for row in rows
        )),
        "all_shuffle_singular_values_preserved": bool(all(
            row["shuffle_preserves_singular_values"] for row in rows
        )),
        "all_finite": bool(all(row["all_finite"] for row in rows)),
    }

    checks = {
        "candidate_count": design["candidate_count"] == 18,
        "geometry_arm_a_exact": all(tuple(control["arm_a_distances"]) == TARGET_DISTANCES for control in controls),
        "geometry_arm_b_exact": all(tuple(control["arm_b_distances"]) == TARGET_DISTANCES for control in controls),
        "terminal_marginals_match": all(control["terminal_marginals_match"] for control in controls),
        "trained_edges_disjoint": all(control["trained_edges_disjoint"] for control in controls),
        "universal_diagnostics_present": bool(design["universal_best_present"] and design["universal_worst_present"]),
        "mean_pearson": mean_pearson >= PEARSON_MIN,
        "mean_spearman": mean_spearman >= SPEARMAN_MIN,
        "best_beats_worst": metrics["fraction_best_beats_worst"] >= BEST_WORST_FRACTION_MIN,
        "best_worst_effect_ratio": metrics["pooled_best_to_abs_worst_ratio"] >= BEST_WORST_RATIO_MIN,
        "true_beats_shuffled_pearson": metrics["pearson_advantage_over_shuffled"] >= PEARSON_ADVANTAGE_MIN,
        "true_beats_shuffled_spearman": metrics["spearman_advantage_over_shuffled"] >= SPEARMAN_ADVANTAGE_MIN,
        "shuffle_spectrum_preserved": metrics["all_shuffle_singular_values_preserved"],
        "finite_mass_conserved": metrics["max_finite_mass_budget_error"] < MASS_ERROR_MAX,
        "one_step_mass_conserved": metrics["max_one_step_write_mass_sum_error"] < MASS_ERROR_MAX,
        "all_finite": metrics["all_finite"],
    }

    return {
        "metrics": metrics,
        "checks": checks,
        "gate_pass": bool(all(checks.values())),
        "thresholds": {
            "pearson_min": PEARSON_MIN,
            "spearman_min": SPEARMAN_MIN,
            "best_worst_fraction_min": BEST_WORST_FRACTION_MIN,
            "best_worst_ratio_min": BEST_WORST_RATIO_MIN,
            "pearson_advantage_min": PEARSON_ADVANTAGE_MIN,
            "spearman_advantage_min": SPEARMAN_ADVANTAGE_MIN,
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
        print("Gate 11 — pre-training semantic routing")
        print(f"candidate count             {m['candidate_count']}")
        print(f"Pearson / Spearman          {m['mean_pearson']:.4f} / {m['mean_spearman']:.4f}")
        print(f"shuffle Pearson / Spearman  {m['mean_shuffle_pearson']:.4f} / {m['mean_shuffle_spearman']:.4f}")
        print(f"BEST > WORST fraction       {m['fraction_best_beats_worst']:.3f}")
        print(f"pooled BEST/WORST ratio     {m['pooled_best_to_abs_worst_ratio']:.2f}x")
        print(f"universal/local BEST means  {m['mean_universal_best_finite_contrast']:.6f} / {m['mean_best_finite_contrast']:.6f}")
        for name, ok in receipt["checks"].items():
            print(f"{'PASS' if ok else 'FAIL'}  {name}")
        print(f"GATE 11: {'PASS' if receipt['gate_pass'] else 'FAIL'}")

    raise SystemExit(0 if receipt["gate_pass"] else 1)


if __name__ == "__main__":
    main()
