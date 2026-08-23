from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sunday.microarbor import (  # noqa: E402
    MicroarborConfig,
    SOMA,
    TERMINAL_A,
    TERMINAL_B,
    impulse_response,
    initialize,
    observer_snapshot,
    shuffled_mass,
    train_history,
)


SELECTIVITY_MIN = 1.20
UNIFORM_GAIN_MIN = 1.20
SHUFFLE_GAIN_MIN = 1.35
SHUFFLES = 40


def run_gate() -> dict:
    cfg = MicroarborConfig()
    uniform = initialize(cfg)
    trained_a = train_history(TERMINAL_A, cfg)
    trained_b = train_history(TERMINAL_B, cfg)

    u_a = impulse_response(uniform, TERMINAL_A)
    u_b = impulse_response(uniform, TERMINAL_B)
    aa = impulse_response(trained_a, TERMINAL_A)
    ab = impulse_response(trained_a, TERMINAL_B)
    ba = impulse_response(trained_b, TERMINAL_A)
    bb = impulse_response(trained_b, TERMINAL_B)

    shuffle_a = np.array([
        impulse_response(shuffled_mass(trained_a, 1000 + i), TERMINAL_A).peak
        for i in range(SHUFFLES)
    ])
    shuffle_b = np.array([
        impulse_response(shuffled_mass(trained_b, 2000 + i), TERMINAL_B).peak
        for i in range(SHUFFLES)
    ])

    # Explicit observer purity test: this callback copies every visible state at every step.
    aa_observed = impulse_response(trained_a, TERMINAL_A, observer_snapshot)
    observer_identical = bool(np.array_equal(aa.trace, aa_observed.trace))

    metrics = {
        "seed": cfg.seed,
        "n_elements": cfg.n_elements,
        "mass_budget": cfg.mass_budget,
        "mass_sum_A": float(trained_a.mass.sum()),
        "mass_sum_B": float(trained_b.mass.sum()),
        "uniform_peak_A": u_a.peak,
        "uniform_peak_B": u_b.peak,
        "A_trained_peak_A": aa.peak,
        "A_trained_peak_B": ab.peak,
        "B_trained_peak_A": ba.peak,
        "B_trained_peak_B": bb.peak,
        "A_selectivity": aa.peak / max(ab.peak, 1e-15),
        "B_selectivity": bb.peak / max(ba.peak, 1e-15),
        "A_uniform_gain": aa.peak / max(u_a.peak, 1e-15),
        "B_uniform_gain": bb.peak / max(u_b.peak, 1e-15),
        "A_shuffle_median": float(np.median(shuffle_a)),
        "B_shuffle_median": float(np.median(shuffle_b)),
        "A_shuffle_gain": aa.peak / max(float(np.median(shuffle_a)), 1e-15),
        "B_shuffle_gain": bb.peak / max(float(np.median(shuffle_b)), 1e-15),
        "observer_identical": observer_identical,
        "A_mass_min": float(trained_a.mass.min()),
        "A_mass_max": float(trained_a.mass.max()),
        "B_mass_min": float(trained_b.mass.min()),
        "B_mass_max": float(trained_b.mass.max()),
    }

    checks = {
        "A_selective": metrics["A_selectivity"] >= SELECTIVITY_MIN,
        "B_selective": metrics["B_selectivity"] >= SELECTIVITY_MIN,
        "A_beats_uniform": metrics["A_uniform_gain"] >= UNIFORM_GAIN_MIN,
        "B_beats_uniform": metrics["B_uniform_gain"] >= UNIFORM_GAIN_MIN,
        "A_geometry_matters": metrics["A_shuffle_gain"] >= SHUFFLE_GAIN_MIN,
        "B_geometry_matters": metrics["B_shuffle_gain"] >= SHUFFLE_GAIN_MIN,
        "A_budget_exact": abs(metrics["mass_sum_A"] - cfg.mass_budget) < 1e-10,
        "B_budget_exact": abs(metrics["mass_sum_B"] - cfg.mass_budget) < 1e-10,
        "observer_is_read_only": observer_identical,
    }
    return {
        "thresholds": {
            "selectivity_min": SELECTIVITY_MIN,
            "uniform_gain_min": UNIFORM_GAIN_MIN,
            "shuffle_gain_min": SHUFFLE_GAIN_MIN,
            "shuffle_count": SHUFFLES,
        },
        "metrics": metrics,
        "checks": checks,
        "gate_pass": bool(all(checks.values())),
    }


def save_plot(path: Path) -> None:
    import matplotlib.pyplot as plt

    cfg = MicroarborConfig()
    a = train_history(TERMINAL_A, cfg)
    b = train_history(TERMINAL_B, cfg)

    fig = plt.figure(figsize=(11, 5))
    for k, (mat, title) in enumerate(((a, "history A"), (b, "history B")), start=1):
        ax = fig.add_subplot(1, 2, k, projection="3d")
        size = 8.0 + 45.0 * mat.mass / max(float(mat.mass.max()), 1e-9)
        ax.scatter(mat.positions[:, 0], mat.positions[:, 1], mat.positions[:, 2], s=size)
        ax.scatter(
            mat.positions[[SOMA, TERMINAL_A, TERMINAL_B], 0],
            mat.positions[[SOMA, TERMINAL_A, TERMINAL_B], 1],
            mat.positions[[SOMA, TERMINAL_A, TERMINAL_B], 2],
            s=90,
            marker="x",
        )
        ax.set_title(title)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
    fig.suptitle("Gate 0: same 3-D cloud and mass budget, different signal history")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="print machine-readable receipt")
    ap.add_argument("--plot", type=Path, default=None, help="optional 3-D observer snapshot")
    args = ap.parse_args()

    receipt = run_gate()
    if args.json:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    else:
        m = receipt["metrics"]
        print("Gate 0 — signal-carved 3-D microarbor")
        print(f"elements={m['n_elements']} mass_budget={m['mass_budget']:.1f} seed={m['seed']}")
        print(f"uniform peaks     A={m['uniform_peak_A']:.9g} B={m['uniform_peak_B']:.9g}")
        print(f"A-trained peaks   A={m['A_trained_peak_A']:.9g} B={m['A_trained_peak_B']:.9g}")
        print(f"B-trained peaks   A={m['B_trained_peak_A']:.9g} B={m['B_trained_peak_B']:.9g}")
        print(f"selectivity       A={m['A_selectivity']:.3f}x B={m['B_selectivity']:.3f}x")
        print(f"uniform gain      A={m['A_uniform_gain']:.3f}x B={m['B_uniform_gain']:.3f}x")
        print(f"shuffle gain      A={m['A_shuffle_gain']:.3f}x B={m['B_shuffle_gain']:.3f}x")
        print(f"mass sums         A={m['mass_sum_A']:.12f} B={m['mass_sum_B']:.12f}")
        print(f"observer identical={m['observer_identical']}")
        for name, ok in receipt["checks"].items():
            print(f"{'PASS' if ok else 'FAIL'}  {name}")
        print(f"GATE 0: {'PASS' if receipt['gate_pass'] else 'FAIL'}")

    if args.plot is not None:
        save_plot(args.plot)
        print(f"plot -> {args.plot}")

    raise SystemExit(0 if receipt["gate_pass"] else 1)


if __name__ == "__main__":
    main()
