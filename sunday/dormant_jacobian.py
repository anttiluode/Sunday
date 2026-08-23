from __future__ import annotations

import numpy as np

from sunday.composition import (
    ALL_PAIRS,
    PORTS,
    CompositionConfig,
    initialize,
    redistribute_mass,
    teacher_episode,
)
from sunday.relation_generality import interaction_vector
from sunday.relation_tomography import code_matrix, principal_cosines, run_seed as run_finite_seed


DEFAULT_EPSILON = 0.25


def one_step_write_matrix(seed: int, cfg: CompositionConfig | None = None) -> np.ndarray:
    """15 pair-specific mass displacements from one dormant write update."""
    cfg = cfg or CompositionConfig()
    rows = []
    for pair in ALL_PAIRS:
        material = initialize(seed, cfg)
        before = material.mass.copy()
        eligibility = teacher_episode(material, pair)
        redistribute_mass(material, eligibility)
        rows.append(material.mass - before)
    return np.asarray(rows, dtype=np.float64)


def _material_with_mass(seed: int, mass: np.ndarray, cfg: CompositionConfig):
    material = initialize(seed, cfg)
    material.mass = np.asarray(mass, dtype=np.float64).copy()
    return material


def read_directional_matrix(
    seed: int,
    write_matrix: np.ndarray,
    *,
    epsilon: float = DEFAULT_EPSILON,
    cfg: CompositionConfig | None = None,
) -> np.ndarray:
    """Central directional derivative of all 15 readouts along each write row."""
    cfg = cfg or CompositionConfig()
    base = np.ones(cfg.n_elements, dtype=np.float64)
    rows = []
    for direction in np.asarray(write_matrix, dtype=np.float64):
        plus = _material_with_mass(seed, base + epsilon * direction, cfg)
        minus = _material_with_mass(seed, base - epsilon * direction, cfg)
        rows.append(
            (interaction_vector(plus) - interaction_vector(minus))
            / (2.0 * epsilon)
        )
    return np.asarray(rows, dtype=np.float64)


def permute_write_locations(
    write_matrix: np.ndarray,
    seed: int,
    cfg: CompositionConfig | None = None,
) -> np.ndarray:
    """Same internal-node permutation for every write row; ports remain fixed."""
    cfg = cfg or CompositionConfig()
    out = np.asarray(write_matrix, dtype=np.float64).copy()
    idx = np.arange(len(PORTS), cfg.n_elements)
    perm = idx.copy()
    rng = np.random.default_rng(seed)
    rng.shuffle(perm)
    out[:, idx] = write_matrix[:, perm]
    return out


def dormant_operator(
    seed: int,
    *,
    epsilon: float = DEFAULT_EPSILON,
    cfg: CompositionConfig | None = None,
) -> dict:
    cfg = cfg or CompositionConfig()
    W = one_step_write_matrix(seed, cfg)
    D = read_directional_matrix(seed, W, epsilon=epsilon, cfg=cfg)
    # q = +arm_A -arm_B, while finite target is F(B)-F(A).
    B0 = -D
    return {"W": W, "D": D, "B0": B0}


def finite_target(seed: int, cfg: CompositionConfig | None = None) -> tuple[np.ndarray, dict]:
    cfg = cfg or CompositionConfig()
    raw = run_finite_seed(seed, cfg)
    Y = np.asarray([entry["y"] for entry in raw["codes"]], dtype=np.float64)
    return Y, raw


def _nmse(pred: np.ndarray, truth: np.ndarray) -> float:
    return float(
        np.sum((pred - truth) ** 2)
        / max(float(np.sum(truth ** 2)), 1e-30)
    )


def _cosine(left: np.ndarray, right: np.ndarray) -> float:
    return float(
        np.dot(left.ravel(), right.ravel())
        / (np.linalg.norm(left) * np.linalg.norm(right) + 1e-30)
    )


def optimal_scalar(pred: np.ndarray, truth: np.ndarray) -> float:
    denom = float(np.sum(pred * pred))
    if denom <= 1e-30:
        return 0.0
    return float(np.sum(pred * truth) / denom)


def analyze_seed(
    seed: int,
    *,
    global_gain: float,
    epsilon: float = DEFAULT_EPSILON,
    permutation_seed: int | None = None,
    cfg: CompositionConfig | None = None,
) -> dict:
    cfg = cfg or CompositionConfig()
    Q = code_matrix()

    finite_Y, finite_raw = finite_target(seed, cfg)
    write = one_step_write_matrix(seed, cfg)
    read_D = read_directional_matrix(seed, write, epsilon=epsilon, cfg=cfg)
    B0 = -read_D
    dormant_Y = Q @ B0
    primary = global_gain * dormant_Y

    per_direction_cosines = [
        _cosine(primary[i], finite_Y[i]) for i in range(len(Q))
    ]

    per_seed_gain = optimal_scalar(dormant_Y, finite_Y)
    per_seed_best = per_seed_gain * dormant_Y

    # Finite operator only for mode analysis; it never modifies B0.
    finite_B = np.linalg.lstsq(Q, finite_Y, rcond=None)[0]
    input_projector = np.linalg.pinv(Q) @ Q
    dormant_B_projected = input_projector @ B0

    U0, s0, _ = np.linalg.svd(dormant_B_projected, full_matrices=False)
    Uf, sf, _ = np.linalg.svd(finite_B, full_matrices=False)
    mode_cosines = principal_cosines(U0[:, :3], Uf[:, :3])
    dormant_energy = s0 * s0
    dormant_top3 = float(
        dormant_energy[:3].sum() / max(float(dormant_energy.sum()), 1e-30)
    )

    # Write-only attacker: overlap of pair-specific mass-write directions.
    write_B = -(write @ write.T)
    write_Y = Q @ write_B
    write_gain = optimal_scalar(write_Y, finite_Y)
    write_pred = write_gain * write_Y

    # Strong surgery: same permutation preserves W W^T exactly.
    pseed = permutation_seed if permutation_seed is not None else 970000 + seed
    write_perm = permute_write_locations(write, pseed, cfg)
    perm_D = read_directional_matrix(seed, write_perm, epsilon=epsilon, cfg=cfg)
    perm_B = -perm_D
    perm_Y = Q @ perm_B
    perm_gain = optimal_scalar(perm_Y, finite_Y)
    perm_pred = perm_gain * perm_Y

    finite_mass_error = float(max(
        max(abs(entry["mass_sum_A"] - cfg.mass_budget),
            abs(entry["mass_sum_B"] - cfg.mass_budget))
        for entry in finite_raw["codes"]
    ))
    write_mass_error = float(np.max(np.abs(write.sum(axis=1))))

    return {
        "seed": int(seed),
        "epsilon": float(epsilon),
        "global_gain": float(global_gain),
        "primary_frozen_gain_nmse": _nmse(primary, finite_Y),
        "primary_mean_direction_cosine": float(np.mean(per_direction_cosines)),
        "primary_flattened_cosine": _cosine(dormant_Y, finite_Y),
        "diagnostic_optimal_seed_gain": per_seed_gain,
        "diagnostic_optimal_seed_nmse": _nmse(per_seed_best, finite_Y),
        "dormant_top3_energy_fraction": dormant_top3,
        "dormant_vs_finite_top3_input_principal_cosines": mode_cosines.tolist(),
        "dormant_vs_finite_weakest_top3_input_cosine": float(mode_cosines.min()),
        "write_only_optimal_gain": write_gain,
        "write_only_nmse": _nmse(write_pred, finite_Y),
        "write_only_mean_direction_cosine": float(np.mean([
            _cosine(write_pred[i], finite_Y[i]) for i in range(len(Q))
        ])),
        "permuted_optimal_gain": perm_gain,
        "permuted_nmse": _nmse(perm_pred, finite_Y),
        "permuted_mean_direction_cosine": float(np.mean([
            _cosine(perm_pred[i], finite_Y[i]) for i in range(len(Q))
        ])),
        "write_gram_preserved_by_permutation": bool(np.allclose(
            write @ write.T, write_perm @ write_perm.T, rtol=0.0, atol=1e-12
        )),
        "max_one_step_write_mass_sum_error": write_mass_error,
        "max_finite_mass_budget_error": finite_mass_error,
        "all_finite": bool(np.all(np.isfinite([
            primary, finite_Y, dormant_B_projected, write_pred, perm_pred
        ]))),
    }
