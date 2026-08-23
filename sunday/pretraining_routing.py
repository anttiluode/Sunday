from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations

import numpy as np

from sunday.composition import ALL_PAIRS, CompositionConfig, terminal_counts, train_program
from sunday.dormant_jacobian import one_step_write_matrix
from sunday.relation_generality import distance_multiset, interaction_vector


TARGET_DISTANCES = (1, 2, 2)
SEMANTIC_ARM_A = ((1, 3), (2, 5), (4, 6))
SEMANTIC_ARM_B = ((1, 4), (2, 6), (3, 5))
EDGE_INDEX = {pair: i for i, pair in enumerate(ALL_PAIRS)}

UNIVERSAL_WORST = (0, -1, 0, 1, 0, 1, -1, 0, 0, 0, 0, 0, 0, 1, -1)
UNIVERSAL_BEST = (-1, 1, 0, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0, -1, 1)


@dataclass(frozen=True)
class RoutingCandidate:
    name: str
    permutation: tuple[int, ...]
    arm_a: tuple[tuple[int, int], ...]
    arm_b: tuple[tuple[int, int], ...]
    vector: tuple[int, ...]


def _map_program(
    program: tuple[tuple[int, int], ...],
    permutation: tuple[int, ...],
) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(
        tuple(sorted((permutation[left - 1], permutation[right - 1])))
        for left, right in program
    ))


def _vector(
    arm_a: tuple[tuple[int, int], ...],
    arm_b: tuple[tuple[int, int], ...],
) -> tuple[int, ...]:
    q = np.zeros(len(ALL_PAIRS), dtype=np.int8)
    for pair in arm_a:
        q[EDGE_INDEX[tuple(sorted(pair))]] = +1
    for pair in arm_b:
        q[EDGE_INDEX[tuple(sorted(pair))]] = -1
    return tuple(int(value) for value in q)


def enumerate_candidates() -> tuple[RoutingCandidate, ...]:
    """The fixed 18-member geometry-equivalent routing class."""
    unique: dict[tuple[int, ...], tuple] = {}
    for permutation in permutations(range(1, 7)):
        arm_a = _map_program(SEMANTIC_ARM_A, permutation)
        arm_b = _map_program(SEMANTIC_ARM_B, permutation)
        if distance_multiset(arm_a) != TARGET_DISTANCES:
            continue
        if distance_multiset(arm_b) != TARGET_DISTANCES:
            continue
        q = _vector(arm_a, arm_b)
        if q not in unique:
            unique[q] = (permutation, arm_a, arm_b)

    records = sorted(unique.items())
    return tuple(
        RoutingCandidate(
            name=f"R{index:02d}",
            permutation=permutation,
            arm_a=arm_a,
            arm_b=arm_b,
            vector=q,
        )
        for index, (q, (permutation, arm_a, arm_b)) in enumerate(records)
    )


CANDIDATES = enumerate_candidates()
CANDIDATE_BY_VECTOR = {candidate.vector: candidate for candidate in CANDIDATES}


def design_controls() -> dict:
    return {
        "candidate_count": len(CANDIDATES),
        "target_distances": list(TARGET_DISTANCES),
        "universal_best_present": UNIVERSAL_BEST in CANDIDATE_BY_VECTOR,
        "universal_worst_present": UNIVERSAL_WORST in CANDIDATE_BY_VECTOR,
        "per_candidate": {
            candidate.name: {
                "arm_a": [list(pair) for pair in candidate.arm_a],
                "arm_b": [list(pair) for pair in candidate.arm_b],
                "arm_a_distances": list(distance_multiset(candidate.arm_a)),
                "arm_b_distances": list(distance_multiset(candidate.arm_b)),
                "terminal_marginals_match": terminal_counts(candidate.arm_a) == terminal_counts(candidate.arm_b),
                "trained_edges_disjoint": set(candidate.arm_a).isdisjoint(set(candidate.arm_b)),
            }
            for candidate in CANDIDATES
        },
    }


def score_candidates(write_matrix: np.ndarray) -> np.ndarray:
    W = np.asarray(write_matrix, dtype=np.float64)
    return np.asarray([
        np.linalg.norm(np.asarray(candidate.vector, dtype=np.float64) @ W)
        for candidate in CANDIDATES
    ], dtype=np.float64)


def shuffled_write_rows(write_matrix: np.ndarray, seed: int) -> np.ndarray:
    W = np.asarray(write_matrix, dtype=np.float64)
    rng = np.random.default_rng(seed)
    return W[rng.permutation(len(W))].copy()


def finite_candidate(
    seed: int,
    candidate: RoutingCandidate,
    cfg: CompositionConfig | None = None,
) -> dict:
    cfg = cfg or CompositionConfig()
    material_a = train_program(seed, candidate.arm_a, cfg)
    material_b = train_program(seed, candidate.arm_b, cfg)
    y = interaction_vector(material_b) - interaction_vector(material_a)
    q = np.asarray(candidate.vector, dtype=np.float64)
    trained = q != 0.0
    unused = ~trained

    trained_abs = float(np.mean(np.abs(y[trained])))
    unused_abs = float(np.mean(np.abs(y[unused])))
    return {
        "name": candidate.name,
        "vector": list(candidate.vector),
        "mass_sum_A": float(material_a.mass.sum()),
        "mass_sum_B": float(material_b.mass.sum()),
        "own_signed_contrast": float(q @ y / 6.0),
        "expected_sign_fraction": float(np.mean(np.sign(y[trained]) == np.sign(q[trained]))),
        "trained_unused_ratio": float(trained_abs / max(unused_abs, 1e-15)),
        "differential": y.tolist(),
    }


def run_seed(seed: int, cfg: CompositionConfig | None = None) -> dict:
    cfg = cfg or CompositionConfig()
    W = one_step_write_matrix(seed, cfg)
    scores = score_candidates(W)
    W_shuffle = shuffled_write_rows(W, 990000 + seed)
    shuffle_scores = score_candidates(W_shuffle)

    best = int(np.argmax(scores))
    worst = int(np.argmin(scores))
    finite = [finite_candidate(seed, candidate, cfg) for candidate in CANDIDATES]

    return {
        "seed": int(seed),
        "scores": scores.tolist(),
        "shuffle_scores": shuffle_scores.tolist(),
        "best_index": best,
        "worst_index": worst,
        "best_name": CANDIDATES[best].name,
        "worst_name": CANDIDATES[worst].name,
        "finite": finite,
        "write_row_norms": np.linalg.norm(W, axis=1).tolist(),
        "shuffle_preserves_singular_values": bool(np.allclose(
            np.linalg.svd(W, compute_uv=False),
            np.linalg.svd(W_shuffle, compute_uv=False),
            rtol=0.0,
            atol=1e-12,
        )),
        "max_one_step_write_mass_sum_error": float(np.max(np.abs(W.sum(axis=1)))),
    }
