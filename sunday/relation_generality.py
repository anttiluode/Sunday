from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from sunday.composition import (
    ALL_PAIRS,
    PORTS,
    TERMINALS,
    CompositionConfig,
    _stable_soma_auc,
    same_permutation_shuffle,
    terminal_counts,
    train_program,
)


@dataclass(frozen=True)
class RelationCode:
    name: str
    arm_a: tuple[tuple[int, int], ...]
    arm_b: tuple[tuple[int, int], ...]


CODES: tuple[RelationCode, ...] = (
    RelationCode(
        "C0",
        ((1, 2), (3, 4), (5, 6)),
        ((1, 6), (2, 3), (4, 5)),
    ),
    RelationCode(
        "C1",
        ((1, 2), (3, 5), (4, 6)),
        ((1, 3), (2, 4), (5, 6)),
    ),
    RelationCode(
        "C2",
        ((1, 2), (3, 6), (4, 5)),
        ((1, 6), (2, 5), (3, 4)),
    ),
    RelationCode(
        "C3",
        ((1, 3), (2, 5), (4, 6)),
        ((1, 4), (2, 6), (3, 5)),
    ),
)

CODE_BY_NAME = {code.name: code for code in CODES}
EDGE_INDEX = {pair: i for i, pair in enumerate(ALL_PAIRS)}


def circular_distance(pair: tuple[int, int]) -> int:
    left, right = pair
    delta = abs(left - right)
    return min(delta, len(TERMINALS) - delta)


def distance_multiset(program: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    return tuple(sorted(circular_distance(tuple(sorted(pair))) for pair in program))


def code_vector(code: RelationCode) -> np.ndarray:
    q = np.zeros(len(ALL_PAIRS), dtype=np.float64)
    for pair in code.arm_a:
        q[EDGE_INDEX[tuple(sorted(pair))]] = +1.0
    for pair in code.arm_b:
        q[EDGE_INDEX[tuple(sorted(pair))]] = -1.0
    return q


def code_matrix() -> np.ndarray:
    return np.stack([code_vector(code) for code in CODES], axis=0)


def design_controls() -> dict:
    Q = code_matrix()
    dots = Q @ Q.T
    per_code = {}
    for code in CODES:
        per_code[code.name] = {
            "arm_a_counts": terminal_counts(code.arm_a),
            "arm_b_counts": terminal_counts(code.arm_b),
            "terminal_marginals_match": terminal_counts(code.arm_a) == terminal_counts(code.arm_b),
            "distance_a": distance_multiset(code.arm_a),
            "distance_b": distance_multiset(code.arm_b),
            "distance_multiset_match": distance_multiset(code.arm_a) == distance_multiset(code.arm_b),
            "trained_edges_disjoint": set(code.arm_a).isdisjoint(set(code.arm_b)),
        }
    return {
        "rank": int(np.linalg.matrix_rank(Q)),
        "dot_matrix": dots.astype(int).tolist(),
        "per_code": per_code,
    }


def interaction_vector(material) -> np.ndarray:
    """All 15 pair interactions with single-terminal AUCs cached once."""
    single = {
        terminal: _stable_soma_auc(material, (terminal,))
        for terminal in TERMINALS
    }
    out = np.empty(len(ALL_PAIRS), dtype=np.float64)
    for row, (left, right) in enumerate(ALL_PAIRS):
        separate = single[left] + single[right]
        joint = _stable_soma_auc(material, (left, right))
        out[row] = (separate - joint) / max(separate, 1e-15)
    return out


def analyze_vector(differential: np.ndarray, code_name: str) -> dict:
    y = np.asarray(differential, dtype=np.float64)
    q = code_vector(CODE_BY_NAME[code_name])
    trained = q != 0.0
    unused = ~trained

    expected = np.sign(q[trained])
    observed = np.sign(y[trained])
    sign_fraction = float(np.mean(observed == expected))

    own = float((q @ y) / np.count_nonzero(trained))
    scores = {
        code.name: float((code_vector(code) @ y) / np.count_nonzero(code_vector(code)))
        for code in CODES
    }
    other_max = max(abs(value) for name, value in scores.items() if name != code_name)

    trained_abs = float(np.mean(np.abs(y[trained])))
    unused_abs = float(np.mean(np.abs(y[unused])))

    return {
        "expected_sign_fraction": sign_fraction,
        "own_signed_contrast": own,
        "trained_abs_mean": trained_abs,
        "unused_abs_mean": unused_abs,
        "trained_unused_ratio": float(trained_abs / max(unused_abs, 1e-15)),
        "cross_scores": scores,
        "other_max_abs_score": float(other_max),
        "specificity_ratio": float(own / max(other_max, 1e-15)),
        "self_top": bool(own > other_max),
        "differential": y.tolist(),
    }


def run_code(seed: int, code_name: str, cfg: CompositionConfig | None = None) -> dict:
    cfg = cfg or CompositionConfig()
    code = CODE_BY_NAME[code_name]

    material_a = train_program(seed, code.arm_a, cfg)
    material_b = train_program(seed, code.arm_b, cfg)
    differential = interaction_vector(material_b) - interaction_vector(material_a)
    analysis = analyze_vector(differential, code_name)

    code_index = [code.name for code in CODES].index(code_name)
    shuffled_a, shuffled_b = same_permutation_shuffle(
        material_a,
        material_b,
        seed=950000 + 10 * seed + code_index,
    )
    shuffled_differential = interaction_vector(shuffled_b) - interaction_vector(shuffled_a)
    shuffled_analysis = analyze_vector(shuffled_differential, code_name)

    own = float(analysis["own_signed_contrast"])
    shuffled_own = float(shuffled_analysis["own_signed_contrast"])

    return {
        "seed": int(seed),
        "code": code_name,
        "mass_sum_A": float(material_a.mass.sum()),
        "mass_sum_B": float(material_b.mass.sum()),
        **analysis,
        "shuffle_own_signed_contrast": shuffled_own,
        "shuffle_ratio": float(abs(shuffled_own) / max(abs(own), 1e-15)),
    }


def run_seed(seed: int, cfg: CompositionConfig | None = None) -> dict:
    cfg = cfg or CompositionConfig()
    return {
        "seed": int(seed),
        "codes": [run_code(seed, code.name, cfg) for code in CODES],
    }
