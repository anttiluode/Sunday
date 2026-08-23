from __future__ import annotations

import argparse
from dataclasses import replace
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sunday.nonlinear_overlap import (  # noqa: E402
    A, B, C, D,
    OverlapConfig,
    OverlapMaterial,
    PROGRAM_AB,
    PROGRAM_CD,
    pair_interaction,
    train_program,
)

GAMMAS = (5.0, 10.0, 20.0, 50.0, 100.0)
AMPLITUDES = (2.0, 5.0, 10.0)
CONFIRM_START = 260000
CONFIRM_SEEDS = 2


def retune(material: OverlapMaterial, gamma: float, amplitude: float) -> OverlapMaterial:
    out = material.copy()
    out.cfg = replace(
        material.cfg,
        nonlinear_gamma=gamma,
        nonlinear_probe_amplitude=amplitude,
    )
    return out


def run(seed_start: int, seed_count: int) -> dict:
    base_cfg = OverlapConfig()
    rows = []

    for seed in range(seed_start, seed_start + seed_count):
        hab0 = train_program(seed, PROGRAM_AB, base_cfg)
        hcd0 = train_program(seed, PROGRAM_CD, base_cfg)
        for amplitude in AMPLITUDES:
            for gamma in GAMMAS:
                hab = retune(hab0, gamma, amplitude)
                hcd = retune(hcd0, gamma, amplitude)
                sep_ab = (
                    pair_interaction(hcd, A, B, mode="distributed")
                    - pair_interaction(hab, A, B, mode="distributed")
                )
                sep_cd = (
                    pair_interaction(hab, C, D, mode="distributed")
                    - pair_interaction(hcd, C, D, mode="distributed")
                )
                rows.append({
                    "seed": seed,
                    "amplitude": amplitude,
                    "gamma": gamma,
                    "sep_AB": sep_ab,
                    "sep_CD": sep_cd,
                })

    all_values = np.asarray([[row["sep_AB"], row["sep_CD"]] for row in rows]).reshape(-1)
    cells = []
    for amplitude in AMPLITUDES:
        for gamma in GAMMAS:
            values = []
            for row in rows:
                if row["amplitude"] == amplitude and row["gamma"] == gamma:
                    values.extend((row["sep_AB"], row["sep_CD"]))
            arr = np.asarray(values)
            cells.append({
                "amplitude": amplitude,
                "gamma": gamma,
                "positive_fraction": float(np.mean(arr > 0.0)),
                "mean_separation": float(arr.mean()),
                "min_separation": float(arr.min()),
            })

    metrics = {
        "seed_start": seed_start,
        "seed_count": seed_count,
        "total_pair_effects": int(all_values.size),
        "overall_positive_fraction": float(np.mean(all_values > 0.0)),
        "minimum_cell_positive_fraction": float(min(cell["positive_fraction"] for cell in cells)),
        "weakest_cell_mean_separation": float(min(cell["mean_separation"] for cell in cells)),
        "minimum_observed_separation": float(all_values.min()),
        "overall_mean_separation": float(all_values.mean()),
    }

    checks = {
        "overall_sign_consistent": metrics["overall_positive_fraction"] >= 0.95,
        "every_cell_mostly_consistent": metrics["minimum_cell_positive_fraction"] >= 0.80,
        "weakest_cell_mean_positive": metrics["weakest_cell_mean_separation"] > 0.0,
    }
    return {"metrics": metrics, "cells": cells, "checks": checks, "pass": bool(all(checks.values()))}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed-start", type=int, default=CONFIRM_START)
    ap.add_argument("--seeds", type=int, default=CONFIRM_SEEDS, help="use 6 to reproduce the stored confirmation")
    args = ap.parse_args()
    out = run(args.seed_start, args.seeds)
    m = out["metrics"]
    print("Gate 1 robustness sweep")
    print(f"seeds={m['seed_count']} pair-effects={m['total_pair_effects']}")
    print(f"overall positive fraction      {m['overall_positive_fraction']:.3f}")
    print(f"minimum cell positive fraction {m['minimum_cell_positive_fraction']:.3f}")
    print(f"weakest cell mean separation   {m['weakest_cell_mean_separation']:.9g}")
    print(f"minimum observed separation    {m['minimum_observed_separation']:.9g}")
    for cell in out["cells"]:
        print(
            f"amp={cell['amplitude']:>4g} gamma={cell['gamma']:>5g} "
            f"positive={cell['positive_fraction']:.2f} mean={cell['mean_separation']:.9g}"
        )
    for name, ok in out["checks"].items():
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
    raise SystemExit(0 if out["pass"] else 1)


if __name__ == "__main__":
    main()
