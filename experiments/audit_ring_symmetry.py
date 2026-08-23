from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sunday.composition import ALL_PAIRS, CompositionConfig, TERMINALS  # noqa: E402
from sunday.relation_generality import circular_distance  # noqa: E402
from sunday.relation_tomography import code_matrix, run_seed  # noqa: E402


SEED_START = 522000
SEED_COUNT = 4


def _edge_permutation(function) -> np.ndarray:
    edge_index = {pair: i for i, pair in enumerate(ALL_PAIRS)}
    P = np.zeros((len(ALL_PAIRS), len(ALL_PAIRS)), dtype=np.float64)
    for old, pair in enumerate(ALL_PAIRS):
        mapped = tuple(sorted((function(pair[0]), function(pair[1]))))
        P[edge_index[mapped], old] = 1.0
    return P


def _harmonic_projector(rotation: np.ndarray, k: int) -> np.ndarray:
    n = len(TERMINALS)
    factor = 1.0 if k in (0, n // 2) else 2.0
    out = np.zeros_like(rotation)
    power = np.eye(len(rotation))
    for r in range(n):
        out += np.cos(2.0 * np.pi * k * r / n) * power
        power = power @ rotation
    return factor * out / float(n)


def _basis(matrix: np.ndarray, tol: float = 1e-9) -> np.ndarray:
    U, singular, _ = np.linalg.svd(matrix, full_matrices=False)
    return U[:, singular > tol]


def _principal_cosines(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.linalg.svd(a.T @ b, compute_uv=False)


def symmetry_objects() -> dict:
    Q = code_matrix()
    rank = int(np.linalg.matrix_rank(Q))
    _, _, vt = np.linalg.svd(Q, full_matrices=False)
    span_basis = vt[:rank].T
    span_projector = span_basis @ span_basis.T

    rotation = _edge_permutation(lambda i: ((i - 1 + 1) % len(TERMINALS)) + 1)
    harmonic = {
        k: _harmonic_projector(rotation, k)
        for k in (1, 2, 3)
    }

    sector_basis = {
        k: _basis(span_projector @ harmonic[k] @ span_projector)
        for k in (1, 2, 3)
    }

    # Geometry-only 3-D candidate frozen before the fresh full-training range:
    # the k=2 harmonic carried by nearest-neighbour relation edges, plus the
    # one-dimensional k=3 parity sector.
    near_mask = np.diag([
        1.0 if circular_distance(pair) == 1 else 0.0
        for pair in ALL_PAIRS
    ])
    near_k2 = _basis(
        span_projector @ near_mask @ harmonic[2] @ span_projector
    )
    candidate, _ = np.linalg.qr(np.column_stack([near_k2, sector_basis[3]]))
    candidate = candidate[:, :3]

    broad = _basis(
        span_projector @ (harmonic[2] + harmonic[3]) @ span_projector
    )

    return {
        "Q": Q,
        "span_projector": span_projector,
        "sector_basis": sector_basis,
        "candidate": candidate,
        "broad": broad,
        "sector_dimensions": {
            str(k): int(sector_basis[k].shape[1]) for k in (1, 2, 3)
        },
    }


def analyze_seed(seed: int, objects: dict, cfg: CompositionConfig | None = None) -> dict:
    cfg = cfg or CompositionConfig()
    raw = run_seed(seed, cfg)
    Q = objects["Q"]
    Y = np.asarray([entry["y"] for entry in raw["codes"]], dtype=np.float64)
    B = np.linalg.lstsq(Q, Y, rcond=None)[0]
    U, singular, _ = np.linalg.svd(B, full_matrices=False)
    U3 = U[:, :3]

    candidate_cos = _principal_cosines(U3, objects["candidate"])
    broad_cos = _principal_cosines(U3, objects["broad"])

    sector_fraction = {}
    for k, basis in objects["sector_basis"].items():
        sector_fraction[str(k)] = float(
            np.linalg.norm(basis.T @ U3, ord="fro") ** 2 / 3.0
        )

    return {
        "seed": int(seed),
        "finite_top3_energy_fraction": float(
            np.sum(singular[:3] ** 2) / max(float(np.sum(singular ** 2)), 1e-30)
        ),
        "geometry_only_3d_principal_cosines": candidate_cos.tolist(),
        "geometry_only_3d_capture": float(np.mean(candidate_cos ** 2)),
        "broad_k2_plus_k3_principal_cosines": broad_cos.tolist(),
        "broad_k2_plus_k3_capture": float(np.mean(broad_cos ** 2)),
        "harmonic_top3_fraction": sector_fraction,
    }


def summarize(rows: list[dict], objects: dict) -> dict:
    return {
        "audit": "six-terminal ring symmetry / spectral null",
        "seed_start": int(rows[0]["seed"]) if rows else None,
        "seed_count": len(rows),
        "relation_span_rank": int(np.linalg.matrix_rank(objects["Q"])),
        "harmonic_sector_dimensions": objects["sector_dimensions"],
        "metrics": {
            "mean_finite_top3_energy_fraction": float(np.mean([
                r["finite_top3_energy_fraction"] for r in rows
            ])),
            "mean_geometry_only_3d_weakest_principal_cosine": float(np.mean([
                min(r["geometry_only_3d_principal_cosines"]) for r in rows
            ])),
            "mean_geometry_only_3d_capture": float(np.mean([
                r["geometry_only_3d_capture"] for r in rows
            ])),
            "mean_broad_k2_plus_k3_weakest_principal_cosine": float(np.mean([
                min(r["broad_k2_plus_k3_principal_cosines"]) for r in rows
            ])),
            "mean_broad_k2_plus_k3_capture": float(np.mean([
                r["broad_k2_plus_k3_capture"] for r in rows
            ])),
            "mean_harmonic_top3_fraction": {
                str(k): float(np.mean([
                    r["harmonic_top3_fraction"][str(k)] for r in rows
                ]))
                for k in (1, 2, 3)
            },
        },
        "per_seed": rows,
    }


def run_audit(seed_start: int = SEED_START, seed_count: int = SEED_COUNT) -> dict:
    cfg = CompositionConfig()
    objects = symmetry_objects()
    rows = [analyze_seed(seed_start + i, objects, cfg) for i in range(seed_count)]
    return summarize(rows, objects)


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
    print("Sunday audit B — six-terminal ring symmetry")
    print(f"relation rank / harmonic dims  {out['relation_span_rank']} / {out['harmonic_sector_dimensions']}")
    print(f"finite top-3 energy            {m['mean_finite_top3_energy_fraction']:.4f}")
    print(f"fixed 3-D symmetry min cosine  {m['mean_geometry_only_3d_weakest_principal_cosine']:.4f}")
    print(f"fixed 3-D subspace capture     {m['mean_geometry_only_3d_capture']:.4f}")
    print(f"broad k2+k3 min cosine         {m['mean_broad_k2_plus_k3_weakest_principal_cosine']:.4f}")
    print(f"broad k2+k3 capture            {m['mean_broad_k2_plus_k3_capture']:.4f}")
    print(f"top-3 harmonic fractions       {m['mean_harmonic_top3_fraction']}")


if __name__ == "__main__":
    main()
