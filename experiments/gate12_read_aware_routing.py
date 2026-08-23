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
from sunday.pretraining_routing import CANDIDATES, TARGET_DISTANCES, design_controls  # noqa: E402
from sunday.read_aware_routing import run_seed  # noqa: E402


SEED_START = 500000
SEED_COUNT = 6

UTILITY_PEARSON_MIN = 0.85
UTILITY_SPEARMAN_MIN = 0.75
READ_BEATS_WRITE_FRACTION_MIN = 5.0 / 6.0
READ_TO_WRITE_UTILITY_RATIO_MIN = 1.08
READ_TO_CONTRAST_UTILITY_RATIO_MIN = 1.04
READ_TO_WRITE_SELECTIVITY_RATIO_MIN = 1.05
READ_TO_WRITE_CONTRAST_RETENTION_MIN = 0.85
READ_BEST_SIGN_FRACTION_MIN = 0.90
MASS_ERROR_MAX = 1e-10


def _pearson(x: np.ndarray, y: np.ndarray) -> float:
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    if float(x.std()) <= 1e-15 or float(y.std()) <= 1e-15:
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])


def _ranks(x: np.ndarray) -> np.ndarray:
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
    predicted_utility = np.asarray([
        entry["clean_utility"] for entry in raw["predictions"]
    ], dtype=np.float64)
    finite_utility = np.asarray([
        entry["clean_utility"] for entry in raw["finite"]
    ], dtype=np.float64)

    r = int(raw["read_best_index"])
    c = int(raw["contrast_best_index"])
    w = int(raw["write_best_index"])

    mass_error = float(max(
        max(abs(entry["mass_sum_A"] - cfg.mass_budget),
            abs(entry["mass_sum_B"] - cfg.mass_budget))
        for entry in raw["finite"]
    ))

    return {
        "seed": int(raw["seed"]),
        "utility_pearson": _pearson(predicted_utility, finite_utility),
        "utility_spearman": _spearman(predicted_utility, finite_utility),
        "read_best_name": CANDIDATES[r].name,
        "contrast_best_name": CANDIDATES[c].name,
        "write_best_name": CANDIDATES[w].name,
        "read_best_finite_utility": float(finite_utility[r]),
        "contrast_best_finite_utility": float(finite_utility[c]),
        "write_best_finite_utility": float(finite_utility[w]),
        "read_beats_write": bool(finite_utility[r] >= finite_utility[w]),
        "read_best_finite_contrast": float(raw["finite"][r]["own_signed_contrast"]),
        "write_best_finite_contrast": float(raw["finite"][w]["own_signed_contrast"]),
        "read_best_finite_selectivity": float(raw["finite"][r]["trained_unused_ratio"]),
        "write_best_finite_selectivity": float(raw["finite"][w]["trained_unused_ratio"]),
        "read_best_sign_fraction": float(raw["finite"][r]["expected_sign_fraction"]),
        "max_finite_mass_budget_error": mass_error,
        "max_one_step_write_mass_sum_error": float(raw["max_one_step_write_mass_sum_error"]),
        "all_finite": bool(
            np.all(np.isfinite(predicted_utility))
            and np.all(np.isfinite(finite_utility))
        ),
        "assignments": [
            {
                "name": CANDIDATES[i].name,
                "predicted_clean_utility": float(predicted_utility[i]),
                "predicted_contrast": float(raw["predictions"][i]["own_signed_contrast"]),
                "predicted_cosine": float(raw["predictions"][i]["direction_cosine"]),
                "write_score": float(raw["write_scores"][i]),
                "finite_clean_utility": float(finite_utility[i]),
                "finite_contrast": float(raw["finite"][i]["own_signed_contrast"]),
                "finite_cosine": float(raw["finite"][i]["direction_cosine"]),
                "finite_trained_unused": float(raw["finite"][i]["trained_unused_ratio"]),
            }
            for i in range(len(CANDIDATES))
        ],
    }


def summarize(raw_rows: list[dict], cfg: CompositionConfig) -> dict:
    design = design_controls()
    rows = [analyze_seed(row, cfg) for row in raw_rows]

    mean_read_utility = float(np.mean([row["read_best_finite_utility"] for row in rows]))
    mean_write_utility = float(np.mean([row["write_best_finite_utility"] for row in rows]))
    mean_contrast_utility = float(np.mean([row["contrast_best_finite_utility"] for row in rows]))
    mean_read_selectivity = float(np.mean([row["read_best_finite_selectivity"] for row in rows]))
    mean_write_selectivity = float(np.mean([row["write_best_finite_selectivity"] for row in rows]))
    mean_read_contrast = float(np.mean([row["read_best_finite_contrast"] for row in rows]))
    mean_write_contrast = float(np.mean([row["write_best_finite_contrast"] for row in rows]))

    controls = list(design["per_candidate"].values())
    metrics = {
        "seed_start": int(rows[0]["seed"]) if rows else None,
        "seed_count": len(rows),
        "candidate_count": design["candidate_count"],
        "mean_utility_pearson": float(np.mean([row["utility_pearson"] for row in rows])),
        "mean_utility_spearman": float(np.mean([row["utility_spearman"] for row in rows])),
        "fraction_read_best_beats_write_best": float(np.mean([
            row["read_beats_write"] for row in rows
        ])),
        "mean_read_best_finite_utility": mean_read_utility,
        "mean_write_best_finite_utility": mean_write_utility,
        "mean_contrast_best_finite_utility": mean_contrast_utility,
        "read_to_write_utility_ratio": float(
            mean_read_utility / max(mean_write_utility, 1e-15)
        ),
        "read_to_contrast_utility_ratio": float(
            mean_read_utility / max(mean_contrast_utility, 1e-15)
        ),
        "mean_read_best_selectivity": mean_read_selectivity,
        "mean_write_best_selectivity": mean_write_selectivity,
        "read_to_write_selectivity_ratio": float(
            mean_read_selectivity / max(mean_write_selectivity, 1e-15)
        ),
        "mean_read_best_contrast": mean_read_contrast,
        "mean_write_best_contrast": mean_write_contrast,
        "read_to_write_contrast_ratio": float(
            mean_read_contrast / max(mean_write_contrast, 1e-15)
        ),
        "mean_read_best_sign_fraction": float(np.mean([
            row["read_best_sign_fraction"] for row in rows
        ])),
        "max_finite_mass_budget_error": float(max(
            row["max_finite_mass_budget_error"] for row in rows
        )),
        "max_one_step_write_mass_sum_error": float(max(
            row["max_one_step_write_mass_sum_error"] for row in rows
        )),
        "all_finite": bool(all(row["all_finite"] for row in rows)),
    }

    checks = {
        "candidate_count": design["candidate_count"] == 18,
        "geometry_arm_a_exact": all(tuple(control["arm_a_distances"]) == TARGET_DISTANCES for control in controls),
        "geometry_arm_b_exact": all(tuple(control["arm_b_distances"]) == TARGET_DISTANCES for control in controls),
        "terminal_marginals_match": all(control["terminal_marginals_match"] for control in controls),
        "trained_edges_disjoint": all(control["trained_edges_disjoint"] for control in controls),
        "utility_pearson": metrics["mean_utility_pearson"] >= UTILITY_PEARSON_MIN,
        "utility_spearman": metrics["mean_utility_spearman"] >= UTILITY_SPEARMAN_MIN,
        "read_best_beats_write_best": metrics["fraction_read_best_beats_write_best"] >= READ_BEATS_WRITE_FRACTION_MIN,
        "read_beats_write_utility": metrics["read_to_write_utility_ratio"] >= READ_TO_WRITE_UTILITY_RATIO_MIN,
        "read_beats_contrast_only_utility": metrics["read_to_contrast_utility_ratio"] >= READ_TO_CONTRAST_UTILITY_RATIO_MIN,
        "read_improves_selectivity": metrics["read_to_write_selectivity_ratio"] >= READ_TO_WRITE_SELECTIVITY_RATIO_MIN,
        "read_retains_contrast": metrics["read_to_write_contrast_ratio"] >= READ_TO_WRITE_CONTRAST_RETENTION_MIN,
        "read_best_signs": metrics["mean_read_best_sign_fraction"] >= READ_BEST_SIGN_FRACTION_MIN,
        "finite_mass_conserved": metrics["max_finite_mass_budget_error"] < MASS_ERROR_MAX,
        "one_step_mass_conserved": metrics["max_one_step_write_mass_sum_error"] < MASS_ERROR_MAX,
        "all_finite": metrics["all_finite"],
    }

    return {
        "metrics": metrics,
        "checks": checks,
        "gate_pass": bool(all(checks.values())),
        "thresholds": {
            "utility_pearson_min": UTILITY_PEARSON_MIN,
            "utility_spearman_min": UTILITY_SPEARMAN_MIN,
            "read_beats_write_fraction_min": READ_BEATS_WRITE_FRACTION_MIN,
            "read_to_write_utility_ratio_min": READ_TO_WRITE_UTILITY_RATIO_MIN,
            "read_to_contrast_utility_ratio_min": READ_TO_CONTRAST_UTILITY_RATIO_MIN,
            "read_to_write_selectivity_ratio_min": READ_TO_WRITE_SELECTIVITY_RATIO_MIN,
            "read_to_write_contrast_retention_min": READ_TO_WRITE_CONTRAST_RETENTION_MIN,
            "read_best_sign_fraction_min": READ_BEST_SIGN_FRACTION_MIN,
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
        print("Gate 12 — read-aware pre-training routing")
        print(f"utility Pearson / Spearman       {m['mean_utility_pearson']:.4f} / {m['mean_utility_spearman']:.4f}")
        print(f"READ >= WRITE fraction           {m['fraction_read_best_beats_write_best']:.3f}")
        print(f"READ/WRITE clean utility          {m['read_to_write_utility_ratio']:.3f}x")
        print(f"READ/contrast-only clean utility  {m['read_to_contrast_utility_ratio']:.3f}x")
        print(f"READ/WRITE selectivity            {m['read_to_write_selectivity_ratio']:.3f}x")
        print(f"READ/WRITE contrast               {m['read_to_write_contrast_ratio']:.3f}x")
        for name, ok in receipt["checks"].items():
            print(f"{'PASS' if ok else 'FAIL'}  {name}")
        print(f"GATE 12: {'PASS' if receipt['gate_pass'] else 'FAIL'}")

    raise SystemExit(0 if receipt["gate_pass"] else 1)


if __name__ == "__main__":
    main()
