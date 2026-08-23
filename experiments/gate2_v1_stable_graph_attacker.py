from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sunday.graph_attacker import run_seed  # noqa: E402

SEED_START = 300000
SEED_COUNT = 12

GEO_POSITIVE_MIN = 0.90
GEO_OVERLAP_MIN = 0.04
GEO_INTERACTION_MIN = 0.0015
GRAPH_SAME_MAX = 1e-12
STRENGTH_REL_MAX = 1e-8
LONG_EDGE_MIN = 0.50
OVERLAP_RATIO_MIN = 3.0
INTERACTION_RATIO_MIN = 2.0


def summarize(rows: list[dict]) -> dict:
    def arr(arm: str, key: str) -> np.ndarray:
        return np.asarray([row[arm][key] for row in rows], dtype=np.float64)

    geo_oa = arr("geo", "overlap_AB")
    geo_oc = arr("geo", "overlap_CD")
    geo_ia = arr("geo", "interaction_AB")
    geo_ic = arr("geo", "interaction_CD")
    rw_oa = arr("rewired", "overlap_AB")
    rw_oc = arr("rewired", "overlap_CD")
    rw_ia = arr("rewired", "interaction_AB")
    rw_ic = arr("rewired", "interaction_CD")

    geo_overlap = float((geo_oa.mean() + geo_oc.mean()) / 2.0)
    geo_interaction = float((geo_ia.mean() + geo_ic.mean()) / 2.0)
    rw_overlap = float((np.abs(rw_oa).mean() + np.abs(rw_oc).mean()) / 2.0)
    rw_interaction = float((np.abs(rw_ia).mean() + np.abs(rw_ic).mean()) / 2.0)

    metrics = {
        "seed_start": int(rows[0]["seed"]) if rows else None,
        "seed_count": len(rows),
        "geo_AB_overlap_positive_fraction": float(np.mean(geo_oa > 0.0)),
        "geo_CD_overlap_positive_fraction": float(np.mean(geo_oc > 0.0)),
        "geo_AB_interaction_positive_fraction": float(np.mean(geo_ia > 0.0)),
        "geo_CD_interaction_positive_fraction": float(np.mean(geo_ic > 0.0)),
        "geo_mean_overlap_separation": geo_overlap,
        "geo_mean_interaction_separation": geo_interaction,
        "rewire_mean_abs_overlap_separation": rw_overlap,
        "rewire_mean_abs_interaction_separation": rw_interaction,
        "geo_to_rewire_overlap_ratio": geo_overlap / max(rw_overlap, 1e-15),
        "geo_to_rewire_interaction_ratio": geo_interaction / max(rw_interaction, 1e-15),
        "rewire_AB_overlap_positive_fraction": float(np.mean(rw_oa > 0.0)),
        "rewire_CD_overlap_positive_fraction": float(np.mean(rw_oc > 0.0)),
        "rewire_AB_interaction_positive_fraction": float(np.mean(rw_ia > 0.0)),
        "rewire_CD_interaction_positive_fraction": float(np.mean(rw_ic > 0.0)),
        "max_graph_same_difference": float(max(row["graph_same_max_diff"] for row in rows)),
        "all_degree_sequences_exact": bool(all(row["degree_exact"] for row in rows)),
        "all_rewires_connected": bool(all(row["rewire_connected"] for row in rows)),
        "all_values_finite": bool(all(row["all_finite"] for row in rows)),
        "max_strength_relative_error": float(max(row["strength_rel_error"] for row in rows)),
        "min_long_edge_fraction": float(min(row["long_edge_fraction"] for row in rows)),
        "mean_long_edge_fraction": float(np.mean([row["long_edge_fraction"] for row in rows])),
        "mean_edge_count": float(np.mean([row["edge_count"] for row in rows])),
    }

    checks = {
        "all_nonlinear_values_finite": metrics["all_values_finite"],
        "geo_AB_overlap_replicates": metrics["geo_AB_overlap_positive_fraction"] >= GEO_POSITIVE_MIN,
        "geo_CD_overlap_replicates": metrics["geo_CD_overlap_positive_fraction"] >= GEO_POSITIVE_MIN,
        "geo_AB_interaction_replicates": metrics["geo_AB_interaction_positive_fraction"] >= GEO_POSITIVE_MIN,
        "geo_CD_interaction_replicates": metrics["geo_CD_interaction_positive_fraction"] >= GEO_POSITIVE_MIN,
        "geo_overlap_effect_present": geo_overlap >= GEO_OVERLAP_MIN,
        "geo_interaction_effect_present": geo_interaction >= GEO_INTERACTION_MIN,
        "same_graph_erased_coordinates_equivalent": metrics["max_graph_same_difference"] < GRAPH_SAME_MAX,
        "rewire_degree_sequence_exact": metrics["all_degree_sequences_exact"],
        "rewire_connected": metrics["all_rewires_connected"],
        "rewire_strength_matched": metrics["max_strength_relative_error"] < STRENGTH_REL_MAX,
        "rewire_destroys_locality": metrics["min_long_edge_fraction"] >= LONG_EDGE_MIN,
        "geometry_amplifies_overlap": metrics["geo_to_rewire_overlap_ratio"] >= OVERLAP_RATIO_MIN,
        "geometry_amplifies_interaction": metrics["geo_to_rewire_interaction_ratio"] >= INTERACTION_RATIO_MIN,
    }

    return {
        "metrics": metrics,
        "checks": checks,
        "gate_pass": bool(all(checks.values())),
        "thresholds": {
            "geo_positive_fraction_min": GEO_POSITIVE_MIN,
            "geo_mean_overlap_min": GEO_OVERLAP_MIN,
            "geo_mean_interaction_min": GEO_INTERACTION_MIN,
            "graph_same_max_difference": GRAPH_SAME_MAX,
            "rewire_strength_relative_error_max": STRENGTH_REL_MAX,
            "rewire_long_edge_fraction_min": LONG_EDGE_MIN,
            "geo_to_rewire_overlap_ratio_min": OVERLAP_RATIO_MIN,
            "geo_to_rewire_interaction_ratio_min": INTERACTION_RATIO_MIN,
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
        print("Gate 2 v1 — stable abstract graph attacker")
        print(f"GEO overlap / interaction         {m['geo_mean_overlap_separation']:.6f} / {m['geo_mean_interaction_separation']:.6f}")
        print(f"REWIRE |overlap| / |interaction| {m['rewire_mean_abs_overlap_separation']:.6f} / {m['rewire_mean_abs_interaction_separation']:.6f}")
        print(f"GEO / REWIRE ratios               {m['geo_to_rewire_overlap_ratio']:.2f}x / {m['geo_to_rewire_interaction_ratio']:.2f}x")
        print(f"coordinate erase max difference   {m['max_graph_same_difference']:.3e}")
        print(f"rewire strength error             {m['max_strength_relative_error']:.3e}")
        print(f"rewire long-edge fraction         min={m['min_long_edge_fraction']:.3f} mean={m['mean_long_edge_fraction']:.3f}")
        print(f"all finite                        {m['all_values_finite']}")
        for name, ok in receipt["checks"].items():
            print(f"{'PASS' if ok else 'FAIL'}  {name}")
        print(f"GATE 2 v1: {'PASS' if receipt['gate_pass'] else 'FAIL'}")

    raise SystemExit(0 if receipt["gate_pass"] else 1)


if __name__ == "__main__":
    main()
