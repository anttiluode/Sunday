from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sunday.composition import CompositionConfig, PORTS  # noqa: E402
from sunday.dormant_jacobian import one_step_write_matrix  # noqa: E402
from sunday.relation_tomography import code_matrix  # noqa: E402


SEED_START = 520000
SEED_COUNT = 6


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(
        np.dot(a.ravel(), b.ravel())
        / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-30)
    )


def analyze_seed(seed: int, cfg: CompositionConfig | None = None) -> dict:
    cfg = cfg or CompositionConfig()
    Q = code_matrix()
    W = one_step_write_matrix(seed, cfg)
    X = Q @ W

    # Orthonormal basis of the registered rank-7 input span.
    _, _, vt_q = np.linalg.svd(Q, full_matrices=False)
    rank_q = int(np.linalg.matrix_rank(Q))
    basis = vt_q[:rank_q].T
    restricted_write = basis.T @ W
    singular = np.linalg.svd(restricted_write, compute_uv=False)

    pred = np.empty_like(Q)
    loo_ranks = []
    for held_out in range(len(Q)):
        keep = np.ones(len(Q), dtype=bool)
        keep[held_out] = False
        loo_ranks.append(int(np.linalg.matrix_rank(X[keep])))
        readout = np.linalg.lstsq(X[keep], Q[keep], rcond=None)[0]
        pred[held_out] = X[held_out] @ readout

    nmse = float(
        np.sum((pred - Q) ** 2)
        / max(float(np.sum(Q ** 2)), 1e-30)
    )
    mean_cosine = float(np.mean([
        _cosine(pred[i], Q[i]) for i in range(len(Q))
    ]))

    return {
        "seed": int(seed),
        "registered_rank": rank_q,
        "dormant_feature_rank": int(np.linalg.matrix_rank(X)),
        "minimum_loo_feature_rank": int(min(loo_ranks)),
        "loo_q_reconstruction_nmse": nmse,
        "loo_q_reconstruction_cosine": mean_cosine,
        "restricted_smallest_to_largest_singular_ratio": float(
            singular[-1] / max(singular[0], 1e-30)
        ),
        "restricted_top3_write_energy_fraction": float(
            np.sum(singular[:3] ** 2) / max(float(np.sum(singular ** 2)), 1e-30)
        ),
        "mutable_mass_scalars": int(cfg.n_elements - len(PORTS)),
    }


def summarize(rows: list[dict]) -> dict:
    return {
        "audit": "fixed dormant reservoir plus trained linear readout",
        "seed_start": int(rows[0]["seed"]) if rows else None,
        "seed_count": len(rows),
        "metrics": {
            "all_registered_rank": sorted({r["registered_rank"] for r in rows}),
            "all_dormant_feature_rank": sorted({r["dormant_feature_rank"] for r in rows}),
            "minimum_loo_feature_rank": int(min(r["minimum_loo_feature_rank"] for r in rows)),
            "mean_loo_q_reconstruction_nmse": float(np.mean([
                r["loo_q_reconstruction_nmse"] for r in rows
            ])),
            "mean_loo_q_reconstruction_cosine": float(np.mean([
                r["loo_q_reconstruction_cosine"] for r in rows
            ])),
            "minimum_restricted_singular_ratio": float(min(
                r["restricted_smallest_to_largest_singular_ratio"] for r in rows
            )),
            "mean_restricted_top3_write_energy_fraction": float(np.mean([
                r["restricted_top3_write_energy_fraction"] for r in rows
            ])),
            "mutable_mass_scalars": int(rows[0]["mutable_mass_scalars"]),
        },
        "per_seed": rows,
    }


def run_audit(seed_start: int = SEED_START, seed_count: int = SEED_COUNT) -> dict:
    cfg = CompositionConfig()
    return summarize([analyze_seed(seed_start + i, cfg) for i in range(seed_count)])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed-start", type=int, default=SEED_START)
    ap.add_argument("--seeds", type=int, default=SEED_COUNT)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    out = run_audit(args.seed_start, args.seeds)
    if args.json:
        print(json.dumps(out, indent=2, sort_keys=True))
        return

    m = out["metrics"]
    print("Sunday audit A — fixed reservoir + trained readout")
    print(f"registered / dormant ranks      {m['all_registered_rank']} / {m['all_dormant_feature_rank']}")
    print(f"minimum LOO dormant rank        {m['minimum_loo_feature_rank']}")
    print(f"LOO q reconstruction NMSE       {m['mean_loo_q_reconstruction_nmse']:.3e}")
    print(f"LOO q reconstruction cosine     {m['mean_loo_q_reconstruction_cosine']:.12f}")
    print(f"minimum singular ratio          {m['minimum_restricted_singular_ratio']:.4f}")
    print(f"mutable Sunday mass scalars     {m['mutable_mass_scalars']}")


if __name__ == "__main__":
    main()
