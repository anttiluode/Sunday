from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import numpy as np

from sunday.composition import ALL_PAIRS, CompositionConfig, terminal_counts, train_program
from sunday.relation_generality import distance_multiset, interaction_vector


TERMINALS = tuple(range(1, 7))
EDGE_INDEX = {pair: i for i, pair in enumerate(ALL_PAIRS)}


@dataclass(frozen=True)
class TomographyCode:
    name: str
    arm_a: tuple[tuple[int, int], ...]
    arm_b: tuple[tuple[int, int], ...]
    distances: tuple[int, ...]
    vector: tuple[int, ...]


def _perfect_matchings(items: tuple[int, ...]) -> list[tuple[tuple[int, int], ...]]:
    if not items:
        return [tuple()]
    first = items[0]
    out: list[tuple[tuple[int, int], ...]] = []
    for i, other in enumerate(items[1:]):
        rest = items[1:i + 1] + items[i + 2:]
        for tail in _perfect_matchings(rest):
            matching = tuple(sorted(((first, other),) + tail))
            out.append(matching)
    return out


def _raw_vector(
    arm_a: tuple[tuple[int, int], ...],
    arm_b: tuple[tuple[int, int], ...],
) -> np.ndarray:
    q = np.zeros(len(ALL_PAIRS), dtype=np.int8)
    for pair in arm_a:
        q[EDGE_INDEX[tuple(sorted(pair))]] = +1
    for pair in arm_b:
        q[EDGE_INDEX[tuple(sorted(pair))]] = -1
    return q


def enumerate_codes() -> tuple[TomographyCode, ...]:
    """All unique controlled perfect-matching contrasts, modulo sign."""
    matchings = sorted(set(_perfect_matchings(TERMINALS)))
    unique: dict[tuple[int, ...], tuple] = {}

    for arm_a, arm_b in combinations(matchings, 2):
        if not set(arm_a).isdisjoint(set(arm_b)):
            continue
        da = distance_multiset(arm_a)
        db = distance_multiset(arm_b)
        if da != db:
            continue

        q = _raw_vector(arm_a, arm_b)
        first = int(np.flatnonzero(q)[0])
        if q[first] < 0:
            arm_a, arm_b = arm_b, arm_a
            q = -q

        unique[tuple(int(x) for x in q)] = (arm_a, arm_b, da)

    records = sorted(
        unique.items(),
        key=lambda item: (item[1][2], item[1][0], item[1][1]),
    )
    return tuple(
        TomographyCode(
            name=f"T{index:02d}",
            arm_a=arm_a,
            arm_b=arm_b,
            distances=distances,
            vector=vector,
        )
        for index, (vector, (arm_a, arm_b, distances)) in enumerate(records)
    )


CODES = enumerate_codes()


def code_matrix() -> np.ndarray:
    return np.asarray([code.vector for code in CODES], dtype=np.float64)


def design_controls() -> dict:
    Q = code_matrix()
    loo_ranks = [
        int(np.linalg.matrix_rank(np.delete(Q, i, axis=0)))
        for i in range(len(Q))
    ]
    per_code = {}
    for code in CODES:
        per_code[code.name] = {
            "arm_a": [list(pair) for pair in code.arm_a],
            "arm_b": [list(pair) for pair in code.arm_b],
            "distances": list(code.distances),
            "terminal_marginals_match": terminal_counts(code.arm_a) == terminal_counts(code.arm_b),
            "distance_multiset_match": distance_multiset(code.arm_a) == distance_multiset(code.arm_b),
            "trained_edges_disjoint": set(code.arm_a).isdisjoint(set(code.arm_b)),
        }
    return {
        "code_count": len(CODES),
        "rank": int(np.linalg.matrix_rank(Q)),
        "loo_ranks": loo_ranks,
        "all_loo_rank": int(min(loo_ranks)),
        "per_code": per_code,
    }


def run_code(seed: int, code: TomographyCode, cfg: CompositionConfig) -> dict:
    material_a = train_program(seed, code.arm_a, cfg)
    material_b = train_program(seed, code.arm_b, cfg)
    y = interaction_vector(material_b) - interaction_vector(material_a)
    return {
        "code": code.name,
        "mass_sum_A": float(material_a.mass.sum()),
        "mass_sum_B": float(material_b.mass.sum()),
        "y": y.tolist(),
    }


def run_seed(seed: int, cfg: CompositionConfig | None = None) -> dict:
    cfg = cfg or CompositionConfig()
    return {
        "seed": int(seed),
        "codes": [run_code(seed, code, cfg) for code in CODES],
    }


def _cosine(left: np.ndarray, right: np.ndarray) -> float:
    return float(
        np.dot(left, right)
        / (np.linalg.norm(left) * np.linalg.norm(right) + 1e-15)
    )


def _nmse(pred: np.ndarray, truth: np.ndarray) -> float:
    return float(
        np.sum((pred - truth) ** 2)
        / max(float(np.sum(truth ** 2)), 1e-30)
    )


def analyze_seed(row: dict, rank_k: int = 3) -> dict:
    Q = code_matrix()
    Y = np.asarray([entry["y"] for entry in row["codes"]], dtype=np.float64)
    n = len(Q)

    full_pred = np.empty_like(Y)
    scalar_pred = np.empty_like(Y)
    diagonal_pred = np.empty_like(Y)
    rankk_pred = np.empty_like(Y)

    for held_out in range(n):
        keep = np.ones(n, dtype=bool)
        keep[held_out] = False

        B = np.linalg.lstsq(Q[keep], Y[keep], rcond=None)[0]
        full_pred[held_out] = Q[held_out] @ B

        gain = float(np.sum(Q[keep] * Y[keep]) / np.sum(Q[keep] ** 2))
        scalar_pred[held_out] = gain * Q[held_out]

        denom = np.sum(Q[keep] ** 2, axis=0)
        edge_gain = np.sum(Q[keep] * Y[keep], axis=0) / (denom + 1e-15)
        diagonal_pred[held_out] = Q[held_out] * edge_gain

        U, s, Vt = np.linalg.svd(B, full_matrices=False)
        Bk = (U[:, :rank_k] * s[:rank_k]) @ Vt[:rank_k, :]
        rankk_pred[held_out] = Q[held_out] @ Bk

    B_all = np.linalg.lstsq(Q, Y, rcond=None)[0]
    U, s, Vt = np.linalg.svd(B_all, full_matrices=False)
    energy = s * s
    topk_energy = float(energy[:rank_k].sum() / max(float(energy.sum()), 1e-30))

    return {
        "seed": int(row["seed"]),
        "full_loo_nmse": _nmse(full_pred, Y),
        "full_loo_mean_cosine": float(np.mean([
            _cosine(full_pred[i], Y[i]) for i in range(n)
        ])),
        "scalar_loo_nmse": _nmse(scalar_pred, Y),
        "diagonal_loo_nmse": _nmse(diagonal_pred, Y),
        "rankk_loo_nmse": _nmse(rankk_pred, Y),
        "rankk_loo_mean_cosine": float(np.mean([
            _cosine(rankk_pred[i], Y[i]) for i in range(n)
        ])),
        "topk_energy_fraction": topk_energy,
        "singular_values": s.tolist(),
        "input_modes_topk": U[:, :rank_k].tolist(),
        "output_modes_topk": Vt[:rank_k, :].T.tolist(),
        "max_mass_budget_error": float(max(
            max(abs(entry["mass_sum_A"] - 256.0), abs(entry["mass_sum_B"] - 256.0))
            for entry in row["codes"]
        )),
        "all_finite": bool(np.all(np.isfinite(Y))),
    }


def principal_cosines(input_modes_a: np.ndarray, input_modes_b: np.ndarray) -> np.ndarray:
    return np.linalg.svd(input_modes_a.T @ input_modes_b, compute_uv=False)
