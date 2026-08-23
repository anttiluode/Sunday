from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sunday.low_gap_attacker import PARTITIONS_PER_SEED, run_seed  # noqa: E402

SEED_START = 340000
SEED_COUNT = 5

GEO_INTERACTION_MIN = 0.0015
STRENGTH_REL_MAX = 1e-8
GAP_RATIO_MIN = 0.60
GAP_RATIO_MAX = 1.25
LONG_EDGE_MIN = 0.75
CLUSTER_RATIO_MAX = 0.45
MEAN_RECOVERY_MAX = 0.50
RECOVERY_FRACTION_MIN = 0.70


def summarize(rows: list[dict]) -> dict:
    geo_interaction = np.asarray([row["geo"]["mean_interaction"] for row in rows], dtype=np.float64)
    modular = [m for row in rows for m in row["modular"]]
    recovery = np.asarray([m["recovery"] for m in modular], dtype=np.float64)

    metrics = {
        "seed_start": int(rows[0]["seed"]) if rows else None,
        "seed_count": len(rows),
        "partitions_per_seed": PARTITIONS_PER_SEED,
        "modular_count": len(modular),
        "geo_mean_interaction": float(geo_interaction.mean()),
        "mean_modular_recovery": float(recovery.mean()),
        "median_modular_recovery": float(np.median(recovery)),
        "fraction_recovery_le_0_5": float(np.mean(recovery <= 0.50)),
        "max_modular_recovery": float(recovery.max()),
        "min_gap_ratio": float(min(m["gap_ratio"] for m in modular)),
        "max_gap_ratio": float(max(m["gap_ratio"] for m in modular)),
        "mean_gap_ratio": float(np.mean([m["gap_ratio"] for m in modular])),
        "min_long_edge_fraction": float(min(m["long_edge_fraction"] for m in modular)),
        "mean_long_edge_fraction": float(np.mean([m["long_edge_fraction"] for m in modular])),
        "max_clustering_ratio": float(max(m["clustering_ratio"] for m in modular)),
        "mean_clustering_ratio": float(np.mean([m["clustering_ratio"] for m in modular])),
        "max_strength_rel_error": float(max(m["strength_rel_error"] for m in modular)),
        "all_connected": bool(all(m["connected"] for m in modular)),
        "all_degree_exact": bool(all(m["degree_exact"] for m in modular)),
        "all_finite": bool(np.all(np.isfinite([
            m["mean_interaction"] for m in modular
        ]))),
        "mean_expander_recovery": float(np.mean([
            abs(row["expander"]["mean_interaction"]) / max(abs(row["geo"]["mean_interaction"]), 1e-15)
            for row in rows
        ])),
    }

    checks = {
        "geo_interaction_present": metrics["geo_mean_interaction"] >= GEO_INTERACTION_MIN,
        "all_modular_connected": metrics["all_connected"],
        "all_modular_degree_exact": metrics["all_degree_exact"],
        "all_modular_finite": metrics["all_finite"],
        "modular_strength_matched": metrics["max_strength_rel_error"] < STRENGTH_REL_MAX,
        "modular_gap_matched_low": metrics["min_gap_ratio"] >= GAP_RATIO_MIN,
        "modular_gap_matched_high": metrics["max_gap_ratio"] <= GAP_RATIO_MAX,
        "modular_stays_nongeometric": metrics["min_long_edge_fraction"] >= LONG_EDGE_MIN,
        "modular_stays_less_clustered": metrics["max_clustering_ratio"] <= CLUSTER_RATIO_MAX,
        "slow_mixing_not_sufficient_mean": metrics["mean_modular_recovery"] <= MEAN_RECOVERY_MAX,
        "slow_mixing_not_sufficient_fraction": metrics["fraction_recovery_le_0_5"] >= RECOVERY_FRACTION_MIN,
    }

    return {
        "metrics": metrics,
        "checks": checks,
        "gate_pass": bool(all(checks.values())),
        "thresholds": {
            "geo_interaction_min": GEO_INTERACTION_MIN,
            "strength_rel_error_max": STRENGTH_REL_MAX,
            "gap_ratio_min": GAP_RATIO_MIN,
            "gap_ratio_max": GAP_RATIO_MAX,
            "long_edge_fraction_min": LONG_EDGE_MIN,
            "clustering_ratio_max": CLUSTER_RATIO_MAX,
            "mean_modular_recovery_max": MEAN_RECOVERY_MAX,
            "recovery_fraction_min": RECOVERY_FRACTION_MIN,
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
        print("Gate 4 — low-gap non-geometric attacker")
        print(f"GEO interaction             {m['geo_mean_interaction']:.6f}")
        print(f"EXPANDER recovery           {m['mean_expander_recovery']:.3f}")
        print(f"MODULAR recovery mean/med   {m['mean_modular_recovery']:.3f}/{m['median_modular_recovery']:.3f}")
        print(f"MODULAR recovery <=.5       {m['fraction_recovery_le_0_5']:.2f}")
        print(f"MODULAR gap ratio range     {m['min_gap_ratio']:.3f}..{m['max_gap_ratio']:.3f}")
        print(f"MODULAR long-edge min       {m['min_long_edge_fraction']:.3f}")
        print(f"MODULAR clustering ratio max {m['max_clustering_ratio']:.3f}")
        for name, ok in receipt["checks"].items():
            print(f"{'PASS' if ok else 'FAIL'}  {name}")
        print(f"GATE 4: {'PASS' if receipt['gate_pass'] else 'FAIL'}")

    raise SystemExit(0 if receipt["gate_pass"] else 1)


if __name__ == "__main__":
    main()
