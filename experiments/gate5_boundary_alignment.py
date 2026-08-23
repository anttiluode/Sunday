from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sunday.boundary_alignment import run_seed  # noqa: E402


SEED_START = 360000
SEED_COUNT = 8

GEO_VALID_STRENGTH_REL_MAX = 1e-8
GAP_RATIO_MIN = 0.60
GAP_RATIO_MAX = 1.25
LONG_EDGE_MIN = 0.75
CLUSTER_RATIO_MAX = 0.45

MEAN_ALIGNED_INTERACTION_MIN = 0.0015
ALIGNED_OVER_CROSS_FRACTION_MIN = 0.75
ALIGNED_OVER_BOTH_FRACTION_MIN = 0.75
MEAN_ALIGNMENT_RATIO_MIN = 1.50


def summarize(rows: list[dict]) -> dict:
    aligned = np.asarray([row["aligned_interaction"] for row in rows], dtype=np.float64)
    crossed = np.asarray([row["cross_mean_interaction"] for row in rows], dtype=np.float64)
    aligned_overlap = np.asarray([row["aligned_overlap"] for row in rows], dtype=np.float64)
    crossed_overlap = np.asarray([row["cross_mean_overlap"] for row in rows], dtype=np.float64)

    mean_aligned = float(aligned.mean())
    mean_crossed = float(crossed.mean())
    ratio = mean_aligned / max(mean_crossed, 1e-15)

    metrics = {
        "seed_start": int(rows[0]["seed"]) if rows else None,
        "seed_count": len(rows),
        "mean_aligned_interaction": mean_aligned,
        "mean_cross_interaction": mean_crossed,
        "mean_alignment_ratio": float(ratio),
        "fraction_aligned_over_cross_mean": float(np.mean(aligned > crossed)),
        "fraction_aligned_over_both_crosses": float(np.mean([
            row["aligned_beats_both_crosses"] for row in rows
        ])),
        "mean_aligned_overlap": float(aligned_overlap.mean()),
        "mean_cross_overlap": float(crossed_overlap.mean()),
        "mean_overlap_alignment_ratio": float(
            aligned_overlap.mean() / max(crossed_overlap.mean(), 1e-15)
        ),
        "min_gap_ratio": float(min(row["graph"]["gap_ratio"] for row in rows)),
        "max_gap_ratio": float(max(row["graph"]["gap_ratio"] for row in rows)),
        "min_long_edge_fraction": float(min(row["graph"]["long_edge_fraction"] for row in rows)),
        "max_clustering_ratio": float(max(row["graph"]["clustering_ratio"] for row in rows)),
        "max_strength_rel_error": float(max(row["graph"]["strength_rel_error"] for row in rows)),
        "all_connected": bool(all(row["graph"]["connected"] for row in rows)),
        "all_degree_exact": bool(all(row["graph"]["degree_exact"] for row in rows)),
        "all_finite": bool(np.all(np.isfinite(np.concatenate([aligned, crossed])))),
    }

    checks = {
        "all_connected": metrics["all_connected"],
        "all_degree_exact": metrics["all_degree_exact"],
        "all_finite": metrics["all_finite"],
        "strength_matched": metrics["max_strength_rel_error"] < GEO_VALID_STRENGTH_REL_MAX,
        "gap_matched_low": metrics["min_gap_ratio"] >= GAP_RATIO_MIN,
        "gap_matched_high": metrics["max_gap_ratio"] <= GAP_RATIO_MAX,
        "stays_nongeometric": metrics["min_long_edge_fraction"] >= LONG_EDGE_MIN,
        "stays_less_clustered": metrics["max_clustering_ratio"] <= CLUSTER_RATIO_MAX,
        "aligned_effect_present": mean_aligned >= MEAN_ALIGNED_INTERACTION_MIN,
        "aligned_beats_cross_fraction": metrics["fraction_aligned_over_cross_mean"] >= ALIGNED_OVER_CROSS_FRACTION_MIN,
        "aligned_beats_both_fraction": metrics["fraction_aligned_over_both_crosses"] >= ALIGNED_OVER_BOTH_FRACTION_MIN,
        "alignment_ratio_large_enough": ratio >= MEAN_ALIGNMENT_RATIO_MIN,
    }

    return {
        "metrics": metrics,
        "checks": checks,
        "gate_pass": bool(all(checks.values())),
        "thresholds": {
            "strength_rel_error_max": GEO_VALID_STRENGTH_REL_MAX,
            "gap_ratio_min": GAP_RATIO_MIN,
            "gap_ratio_max": GAP_RATIO_MAX,
            "long_edge_fraction_min": LONG_EDGE_MIN,
            "clustering_ratio_max": CLUSTER_RATIO_MAX,
            "mean_aligned_interaction_min": MEAN_ALIGNED_INTERACTION_MIN,
            "aligned_over_cross_fraction_min": ALIGNED_OVER_CROSS_FRACTION_MIN,
            "aligned_over_both_fraction_min": ALIGNED_OVER_BOTH_FRACTION_MIN,
            "mean_alignment_ratio_min": MEAN_ALIGNMENT_RATIO_MIN,
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
        print("Gate 5 — boundary-condition alignment")
        print(f"aligned interaction mean     {m['mean_aligned_interaction']:.6f}")
        print(f"crossed interaction mean     {m['mean_cross_interaction']:.6f}")
        print(f"alignment ratio              {m['mean_alignment_ratio']:.3f}x")
        print(f"aligned > cross mean         {m['fraction_aligned_over_cross_mean']:.2f}")
        print(f"aligned > both crosses       {m['fraction_aligned_over_both_crosses']:.2f}")
        print(f"route alignment ratio        {m['mean_overlap_alignment_ratio']:.3f}x")
        for name, ok in receipt["checks"].items():
            print(f"{'PASS' if ok else 'FAIL'}  {name}")
        print(f"GATE 5: {'PASS' if receipt['gate_pass'] else 'FAIL'}")

    raise SystemExit(0 if receipt["gate_pass"] else 1)


if __name__ == "__main__":
    main()
