from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sunday.topology_dial import LEVELS, run_seed  # noqa: E402

SEED_START = 320000
SEED_COUNT = 6

STRENGTH_REL_MAX = 1e-8
GEO_OVERLAP_MIN = 0.04
GEO_INTERACTION_MIN = 0.0015
HALF_CLUSTER_RATIO_MAX = 0.60
HALF_INTERACTION_RATIO_MAX = 0.65
SATURATED_INTERACTION_RATIO_MAX = 0.50
CLUSTER_INTERACTION_RHO_MIN = 0.60
GAP_INTERACTION_RHO_MAX = -0.60


def _rankdata(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(len(values), dtype=np.float64)
    i = 0
    while i < len(values):
        j = i + 1
        while j < len(values) and values[order[j]] == values[order[i]]:
            j += 1
        rank = (i + j - 1) / 2.0
        ranks[order[i:j]] = rank
        i = j
    return ranks


def _spearman(left: np.ndarray, right: np.ndarray) -> float:
    a = _rankdata(np.asarray(left, dtype=np.float64))
    b = _rankdata(np.asarray(right, dtype=np.float64))
    if float(a.std()) <= 1e-15 or float(b.std()) <= 1e-15:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def summarize(rows: list[dict]) -> dict:
    by_level = {float(level): [r for r in rows if float(r["swaps_per_edge"]) == float(level)] for level in LEVELS}

    level_metrics: dict[str, dict[str, float]] = {}
    for level in LEVELS:
        group = by_level[float(level)]
        level_metrics[str(level)] = {
            "mean_clustering": float(np.mean([r["clustering"] for r in group])),
            "mean_transitivity": float(np.mean([r["transitivity"] for r in group])),
            "mean_shortest_path": float(np.mean([r["mean_shortest_path"] for r in group])),
            "mean_normalized_laplacian_gap": float(np.mean([r["normalized_laplacian_gap"] for r in group])),
            "mean_long_edge_fraction": float(np.mean([r["long_edge_fraction"] for r in group])),
            "mean_overlap": float(np.mean([r["mean_overlap"] for r in group])),
            "mean_abs_overlap": float(np.mean([abs(r["mean_overlap"]) for r in group])),
            "mean_interaction": float(np.mean([r["mean_interaction"] for r in group])),
            "mean_abs_interaction": float(np.mean([abs(r["mean_interaction"]) for r in group])),
        }

    geo = level_metrics["0.0"]
    half = level_metrics["0.5"]
    sat_abs_interaction = float(np.mean([
        level_metrics["2.0"]["mean_abs_interaction"],
        level_metrics["5.0"]["mean_abs_interaction"],
    ]))

    clustering = np.asarray([r["clustering"] for r in rows], dtype=np.float64)
    gap = np.asarray([r["normalized_laplacian_gap"] for r in rows], dtype=np.float64)
    abs_interaction = np.asarray([abs(r["mean_interaction"]) for r in rows], dtype=np.float64)
    abs_overlap = np.asarray([abs(r["mean_overlap"]) for r in rows], dtype=np.float64)

    metrics = {
        "seed_start": int(min(r["seed"] for r in rows)),
        "seed_count": len(set(int(r["seed"]) for r in rows)),
        "points": len(rows),
        "all_connected": bool(all(r["connected"] for r in rows)),
        "all_degree_exact": bool(all(r["degree_exact"] for r in rows)),
        "all_finite": bool(np.all(np.isfinite([
            r["mean_interaction"] for r in rows
        ]))),
        "max_strength_rel_error": float(max(r["strength_rel_error"] for r in rows)),
        "geo_mean_overlap": geo["mean_overlap"],
        "geo_mean_interaction": geo["mean_interaction"],
        "half_clustering_ratio": half["mean_clustering"] / max(geo["mean_clustering"], 1e-15),
        "half_abs_interaction_ratio": half["mean_abs_interaction"] / max(geo["mean_abs_interaction"], 1e-15),
        "saturated_abs_interaction_ratio": sat_abs_interaction / max(geo["mean_abs_interaction"], 1e-15),
        "spearman_clustering_abs_interaction": _spearman(clustering, abs_interaction),
        "spearman_gap_abs_interaction": _spearman(gap, abs_interaction),
        "spearman_clustering_abs_overlap": _spearman(clustering, abs_overlap),
        "spearman_gap_abs_overlap": _spearman(gap, abs_overlap),
    }

    checks = {
        "all_snapshots_connected": metrics["all_connected"],
        "all_degree_sequences_exact": metrics["all_degree_exact"],
        "all_nonlinear_values_finite": metrics["all_finite"],
        "strength_matched": metrics["max_strength_rel_error"] < STRENGTH_REL_MAX,
        "geo_overlap_present": metrics["geo_mean_overlap"] >= GEO_OVERLAP_MIN,
        "geo_interaction_present": metrics["geo_mean_interaction"] >= GEO_INTERACTION_MIN,
        "half_rewire_destroys_clustering": metrics["half_clustering_ratio"] <= HALF_CLUSTER_RATIO_MAX,
        "half_rewire_reduces_interaction": metrics["half_abs_interaction_ratio"] <= HALF_INTERACTION_RATIO_MAX,
        "saturated_rewire_near_generic_floor": metrics["saturated_abs_interaction_ratio"] <= SATURATED_INTERACTION_RATIO_MAX,
        "clustering_tracks_interaction": metrics["spearman_clustering_abs_interaction"] >= CLUSTER_INTERACTION_RHO_MIN,
        "spectral_gap_anti_tracks_interaction": metrics["spearman_gap_abs_interaction"] <= GAP_INTERACTION_RHO_MAX,
    }

    return {
        "metrics": metrics,
        "level_metrics": level_metrics,
        "checks": checks,
        "gate_pass": bool(all(checks.values())),
        "thresholds": {
            "strength_rel_error_max": STRENGTH_REL_MAX,
            "geo_overlap_min": GEO_OVERLAP_MIN,
            "geo_interaction_min": GEO_INTERACTION_MIN,
            "half_clustering_ratio_max": HALF_CLUSTER_RATIO_MAX,
            "half_interaction_ratio_max": HALF_INTERACTION_RATIO_MAX,
            "saturated_interaction_ratio_max": SATURATED_INTERACTION_RATIO_MAX,
            "clustering_interaction_rho_min": CLUSTER_INTERACTION_RHO_MIN,
            "gap_interaction_rho_max": GAP_INTERACTION_RHO_MAX,
        },
        "per_point": rows,
    }


def run_gate(seed_start: int = SEED_START, seed_count: int = SEED_COUNT) -> dict:
    rows: list[dict] = []
    for seed in range(seed_start, seed_start + seed_count):
        rows.extend(run_seed(seed))
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
        print("Gate 3 — topology/locality dial")
        for level in LEVELS:
            q = receipt["level_metrics"][str(level)]
            print(
                f"{level:>3.1f}E  clustering={q['mean_clustering']:.3f} "
                f"long={q['mean_long_edge_fraction']:.3f} gap={q['mean_normalized_laplacian_gap']:.3f} "
                f"overlap={q['mean_overlap']:.5f} interaction={q['mean_interaction']:.5f}"
            )
        print(f"rho clustering/|interaction| {m['spearman_clustering_abs_interaction']:.3f}")
        print(f"rho gap/|interaction|        {m['spearman_gap_abs_interaction']:.3f}")
        for name, ok in receipt["checks"].items():
            print(f"{'PASS' if ok else 'FAIL'}  {name}")
        print(f"GATE 3: {'PASS' if receipt['gate_pass'] else 'FAIL'}")

    raise SystemExit(0 if receipt["gate_pass"] else 1)


if __name__ == "__main__":
    main()
