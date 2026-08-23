from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sunday.nonlinear_overlap import (  # noqa: E402
    A, B, C, D,
    OverlapConfig,
    PROGRAM_AB,
    PROGRAM_CD,
    pair_interaction,
    route_overlap,
    same_permutation_shuffle,
    terminal_counts,
    train_program,
)

POSITIVE_FRACTION_MIN = 0.80
MEAN_OVERLAP_SEPARATION_MIN = 0.04
MEAN_INTERACTION_SEPARATION_MIN = 0.0015
DISTRIBUTED_TO_SOMA_MIN = 20.0
SHUFFLE_SIGNED_RATIO_MAX = 0.25
CONFIRM_START = 240000
CONFIRM_SEEDS = 8


def per_seed(seed: int, cfg: OverlapConfig) -> dict[str, float]:
    hab = train_program(seed, PROGRAM_AB, cfg)
    hcd = train_program(seed, PROGRAM_CD, cfg)

    # Positive means: the pair that was coactive during training became less overlapping.
    overlap_ab = route_overlap(hcd, A, B) - route_overlap(hab, A, B)
    overlap_cd = route_overlap(hab, C, D) - route_overlap(hcd, C, D)

    interaction_ab = (
        pair_interaction(hcd, A, B, mode="distributed")
        - pair_interaction(hab, A, B, mode="distributed")
    )
    interaction_cd = (
        pair_interaction(hab, C, D, mode="distributed")
        - pair_interaction(hcd, C, D, mode="distributed")
    )

    soma_ab = (
        pair_interaction(hcd, A, B, mode="soma_only")
        - pair_interaction(hab, A, B, mode="soma_only")
    )
    soma_cd = (
        pair_interaction(hab, C, D, mode="soma_only")
        - pair_interaction(hcd, C, D, mode="soma_only")
    )

    sh_ab, sh_cd = same_permutation_shuffle(hab, hcd, seed=900000 + seed)
    shuffle_overlap_ab = route_overlap(sh_cd, A, B) - route_overlap(sh_ab, A, B)
    shuffle_overlap_cd = route_overlap(sh_ab, C, D) - route_overlap(sh_cd, C, D)
    shuffle_interaction_ab = (
        pair_interaction(sh_cd, A, B, mode="distributed")
        - pair_interaction(sh_ab, A, B, mode="distributed")
    )
    shuffle_interaction_cd = (
        pair_interaction(sh_ab, C, D, mode="distributed")
        - pair_interaction(sh_cd, C, D, mode="distributed")
    )

    return {
        "overlap_sep_AB": overlap_ab,
        "overlap_sep_CD": overlap_cd,
        "interaction_sep_AB": interaction_ab,
        "interaction_sep_CD": interaction_cd,
        "soma_only_sep_AB": soma_ab,
        "soma_only_sep_CD": soma_cd,
        "shuffle_overlap_sep_AB": shuffle_overlap_ab,
        "shuffle_overlap_sep_CD": shuffle_overlap_cd,
        "shuffle_interaction_sep_AB": shuffle_interaction_ab,
        "shuffle_interaction_sep_CD": shuffle_interaction_cd,
        "mass_sum_HAB": float(hab.mass.sum()),
        "mass_sum_HCD": float(hcd.mass.sum()),
    }


def summarize(rows: list[dict[str, float]], cfg: OverlapConfig) -> dict:
    def arr(key: str) -> np.ndarray:
        return np.asarray([row[key] for row in rows], dtype=np.float64)

    ov_ab, ov_cd = arr("overlap_sep_AB"), arr("overlap_sep_CD")
    in_ab, in_cd = arr("interaction_sep_AB"), arr("interaction_sep_CD")
    so_ab, so_cd = arr("soma_only_sep_AB"), arr("soma_only_sep_CD")
    sh_ov_ab, sh_ov_cd = arr("shuffle_overlap_sep_AB"), arr("shuffle_overlap_sep_CD")
    sh_in_ab, sh_in_cd = arr("shuffle_interaction_sep_AB"), arr("shuffle_interaction_sep_CD")

    mean_overlap = float((ov_ab.mean() + ov_cd.mean()) / 2.0)
    mean_interaction = float((in_ab.mean() + in_cd.mean()) / 2.0)
    soma_abs = float((np.abs(so_ab).mean() + np.abs(so_cd).mean()) / 2.0)
    shuffle_overlap_signed = float((abs(sh_ov_ab.mean()) + abs(sh_ov_cd.mean())) / 2.0)
    shuffle_interaction_signed = float((abs(sh_in_ab.mean()) + abs(sh_in_cd.mean())) / 2.0)

    metrics = {
        "confirmation_seed_start": rows and int(CONFIRM_START) or None,
        "confirmation_seed_count": len(rows),
        "program_AB_counts": terminal_counts(PROGRAM_AB),
        "program_CD_counts": terminal_counts(PROGRAM_CD),
        "AB_overlap_positive_fraction": float(np.mean(ov_ab > 0.0)),
        "CD_overlap_positive_fraction": float(np.mean(ov_cd > 0.0)),
        "AB_interaction_positive_fraction": float(np.mean(in_ab > 0.0)),
        "CD_interaction_positive_fraction": float(np.mean(in_cd > 0.0)),
        "mean_overlap_separation": mean_overlap,
        "mean_AB_overlap_separation": float(ov_ab.mean()),
        "mean_CD_overlap_separation": float(ov_cd.mean()),
        "mean_interaction_separation": mean_interaction,
        "mean_AB_interaction_separation": float(in_ab.mean()),
        "mean_CD_interaction_separation": float(in_cd.mean()),
        "mean_abs_soma_only_separation": soma_abs,
        "distributed_to_soma_ratio": mean_interaction / max(soma_abs, 1e-15),
        "shuffle_overlap_signed_mean": shuffle_overlap_signed,
        "shuffle_interaction_signed_mean": shuffle_interaction_signed,
        "shuffle_overlap_signed_ratio": shuffle_overlap_signed / max(mean_overlap, 1e-15),
        "shuffle_interaction_signed_ratio": shuffle_interaction_signed / max(mean_interaction, 1e-15),
        "max_mass_budget_error": float(max(
            max(abs(row["mass_sum_HAB"] - cfg.mass_budget), abs(row["mass_sum_HCD"] - cfg.mass_budget))
            for row in rows
        )),
    }

    checks = {
        "programs_match_terminal_counts": metrics["program_AB_counts"] == metrics["program_CD_counts"],
        "AB_overlap_replication": metrics["AB_overlap_positive_fraction"] >= POSITIVE_FRACTION_MIN,
        "CD_overlap_replication": metrics["CD_overlap_positive_fraction"] >= POSITIVE_FRACTION_MIN,
        "AB_interaction_replication": metrics["AB_interaction_positive_fraction"] >= POSITIVE_FRACTION_MIN,
        "CD_interaction_replication": metrics["CD_interaction_positive_fraction"] >= POSITIVE_FRACTION_MIN,
        "overlap_effect_large_enough": mean_overlap >= MEAN_OVERLAP_SEPARATION_MIN,
        "interaction_effect_large_enough": mean_interaction >= MEAN_INTERACTION_SEPARATION_MIN,
        "distributed_beats_soma_only": metrics["distributed_to_soma_ratio"] >= DISTRIBUTED_TO_SOMA_MIN,
        "overlap_effect_is_spatial": metrics["shuffle_overlap_signed_ratio"] <= SHUFFLE_SIGNED_RATIO_MAX,
        "interaction_effect_is_spatial": metrics["shuffle_interaction_signed_ratio"] <= SHUFFLE_SIGNED_RATIO_MAX,
        "mass_budget_exact": metrics["max_mass_budget_error"] < 1e-10,
    }
    return {"metrics": metrics, "checks": checks, "gate_pass": bool(all(checks.values()))}


def run_gate(seed_start: int = CONFIRM_START, seed_count: int = CONFIRM_SEEDS) -> dict:
    cfg = OverlapConfig()
    rows = [per_seed(seed_start + i, cfg) for i in range(seed_count)]
    out = summarize(rows, cfg)
    out["metrics"]["confirmation_seed_start"] = seed_start
    out["thresholds"] = {
        "positive_fraction_min": POSITIVE_FRACTION_MIN,
        "mean_overlap_separation_min": MEAN_OVERLAP_SEPARATION_MIN,
        "mean_interaction_separation_min": MEAN_INTERACTION_SEPARATION_MIN,
        "distributed_to_soma_min": DISTRIBUTED_TO_SOMA_MIN,
        "shuffle_signed_ratio_max": SHUFFLE_SIGNED_RATIO_MAX,
    }
    out["per_seed"] = rows
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--seed-start", type=int, default=CONFIRM_START)
    ap.add_argument("--seeds", type=int, default=CONFIRM_SEEDS, help="8 is a quick confirmation; use 20 for the stored full receipt")
    args = ap.parse_args()
    receipt = run_gate(seed_start=args.seed_start, seed_count=args.seeds)
    if args.json:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    else:
        m = receipt["metrics"]
        print("Gate 1 — local nonlinear overlap")
        print(f"matched terminal counts: {m['program_AB_counts']} vs {m['program_CD_counts']}")
        print(f"overlap separation mean   {m['mean_overlap_separation']:.6f}")
        print(f"interaction separation    {m['mean_interaction_separation']:.6f}")
        print(f"positive fractions AB/CD  overlap={m['AB_overlap_positive_fraction']:.2f}/{m['CD_overlap_positive_fraction']:.2f} interaction={m['AB_interaction_positive_fraction']:.2f}/{m['CD_interaction_positive_fraction']:.2f}")
        print(f"distributed/soma-only     {m['distributed_to_soma_ratio']:.1f}x")
        print(f"shuffle signed ratios     overlap={m['shuffle_overlap_signed_ratio']:.3f} interaction={m['shuffle_interaction_signed_ratio']:.3f}")
        for name, ok in receipt["checks"].items():
            print(f"{'PASS' if ok else 'FAIL'}  {name}")
        print(f"GATE 1: {'PASS' if receipt['gate_pass'] else 'FAIL'}")
    raise SystemExit(0 if receipt["gate_pass"] else 1)


if __name__ == "__main__":
    main()
