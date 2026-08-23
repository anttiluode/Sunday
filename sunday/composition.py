from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import numpy as np


SOMA = 0
TERMINALS = tuple(range(1, 7))
PORTS = (SOMA,) + TERMINALS
MATCHING_1 = ((1, 2), (3, 4), (5, 6))
MATCHING_2 = ((2, 3), (4, 5), (6, 1))
ALL_PAIRS = tuple(combinations(TERMINALS, 2))
M1_SET = {tuple(sorted(pair)) for pair in MATCHING_1}
M2_SET = {tuple(sorted(pair)) for pair in MATCHING_2}


@dataclass(frozen=True)
class CompositionConfig:
    n_elements: int = 256
    yz_scale: float = 0.75
    terminal_radius: float = 0.55
    overlap_length: float = 0.28
    overlap_cutoff: float = 0.52
    dt: float = 0.035
    leak: float = 0.35
    kappa: float = 0.80
    teacher_steps: int = 80
    teacher_drive_steps: int = 50
    cycles: int = 40
    mass_floor: float = 0.20
    learning_rate: float = 0.08
    response_steps: int = 160
    response_drive_steps: int = 8
    nonlinear_gamma: float = 50.0
    nonlinear_probe_amplitude: float = 10.0

    @property
    def mass_budget(self) -> float:
        return float(self.n_elements)


@dataclass
class CompositionMaterial:
    positions: np.ndarray
    base: np.ndarray
    mass: np.ndarray
    cfg: CompositionConfig

    def copy(self) -> "CompositionMaterial":
        return CompositionMaterial(
            self.positions.copy(), self.base.copy(), self.mass.copy(), self.cfg
        )


def terminal_counts(program: tuple[tuple[int, int], ...]) -> dict[int, int]:
    out = {terminal: 0 for terminal in TERMINALS}
    for left, right in program:
        out[left] += 1
        out[right] += 1
    return out


def make_positions(seed: int, cfg: CompositionConfig) -> np.ndarray:
    rng = np.random.default_rng(seed)
    pos = rng.uniform(-1.0, 1.0, size=(cfg.n_elements, 3))
    pos[:, 1:] *= cfg.yz_scale
    pos[SOMA] = np.array([0.95, 0.0, 0.0])

    for q, terminal in enumerate(TERMINALS):
        angle = 2.0 * np.pi * q / len(TERMINALS)
        pos[terminal] = np.array([
            -0.95,
            cfg.terminal_radius * np.cos(angle),
            cfg.terminal_radius * np.sin(angle),
        ])
    return pos


def make_base(positions: np.ndarray, cfg: CompositionConfig) -> np.ndarray:
    delta = positions[:, None, :] - positions[None, :, :]
    r2 = np.sum(delta * delta, axis=-1)
    r = np.sqrt(r2)
    base = np.exp(-0.5 * r2 / (cfg.overlap_length**2))
    base[r > cfg.overlap_cutoff] = 0.0
    np.fill_diagonal(base, 0.0)
    return base


def initialize(seed: int, cfg: CompositionConfig | None = None) -> CompositionMaterial:
    cfg = cfg or CompositionConfig()
    positions = make_positions(seed, cfg)
    return CompositionMaterial(
        positions=positions,
        base=make_base(positions, cfg),
        mass=np.ones(cfg.n_elements, dtype=np.float64),
        cfg=cfg,
    )


def conductance(material: CompositionMaterial) -> np.ndarray:
    return material.base * np.sqrt(np.outer(material.mass, material.mass))


def teacher_episode(material: CompositionMaterial, sources: tuple[int, int]) -> np.ndarray:
    cfg = material.cfg
    G = conductance(material)
    degree = G.sum(axis=1)
    v = np.zeros(cfg.n_elements, dtype=np.float64)
    eligibility = np.zeros(cfg.n_elements, dtype=np.float64)

    for t in range(cfg.teacher_steps):
        u = np.zeros(cfg.n_elements, dtype=np.float64)
        if t < cfg.teacher_drive_steps:
            for source in sources:
                u[source] += 1.0
            u[SOMA] -= float(len(sources))
        v += cfg.dt * (-cfg.leak * v + cfg.kappa * (G @ v - degree * v) + u)
        eligibility += np.abs(G * (v[:, None] - v[None, :])).sum(axis=1)

    eligibility /= float(cfg.teacher_steps)
    eligibility[list(PORTS)] = 0.0
    return eligibility


def redistribute_mass(material: CompositionMaterial, eligibility: np.ndarray) -> None:
    cfg = material.cfg
    mask = np.ones(cfg.n_elements, dtype=bool)
    mask[list(PORTS)] = False
    e = np.maximum(eligibility[mask], 0.0)
    if float(e.mean()) <= 1e-15:
        return
    e /= float(e.mean())

    free_budget = cfg.mass_budget - float(len(PORTS))
    allocatable = free_budget - cfg.mass_floor * int(mask.sum())
    target = cfg.mass_floor + allocatable * e / (float(e.sum()) + 1e-15)
    material.mass[mask] = (
        (1.0 - cfg.learning_rate) * material.mass[mask]
        + cfg.learning_rate * target
    )
    material.mass[list(PORTS)] = 1.0
    material.mass[mask] += (cfg.mass_budget - float(material.mass.sum())) / int(mask.sum())


def train_program(
    seed: int,
    program: tuple[tuple[int, int], ...],
    cfg: CompositionConfig | None = None,
) -> CompositionMaterial:
    cfg = cfg or CompositionConfig()
    material = initialize(seed, cfg)
    for _ in range(cfg.cycles):
        for pair in program:
            eligibility = teacher_episode(material, pair)
            redistribute_mass(material, eligibility)
    return material


def _stable_soma_auc(
    material: CompositionMaterial,
    sources: tuple[int, ...],
    *,
    substeps: int = 8,
) -> float:
    cfg = material.cfg
    G = conductance(material)
    degree = G.sum(axis=1)
    v = np.zeros(cfg.n_elements, dtype=np.float64)
    h = cfg.dt / float(substeps)
    auc = 0.0

    for t in range(cfg.response_steps):
        for _ in range(substeps):
            u = np.zeros(cfg.n_elements, dtype=np.float64)
            if t < cfg.response_drive_steps:
                for source in sources:
                    u[source] += cfg.nonlinear_probe_amplitude
            v += h * (
                -cfg.leak * v
                + cfg.kappa * (G @ v - degree * v)
                + u
                - cfg.nonlinear_gamma * v**3
            )
            if not np.all(np.isfinite(v)):
                return float("nan")
            auc += max(float(v[SOMA]), 0.0) * h
    return auc


def pair_interaction(material: CompositionMaterial, left: int, right: int) -> float:
    left_auc = _stable_soma_auc(material, (left,))
    right_auc = _stable_soma_auc(material, (right,))
    joint_auc = _stable_soma_auc(material, (left, right))
    separate = left_auc + right_auc
    return float((separate - joint_auc) / max(separate, 1e-15))


def same_permutation_shuffle(
    left: CompositionMaterial,
    right: CompositionMaterial,
    seed: int,
) -> tuple[CompositionMaterial, CompositionMaterial]:
    a = left.copy()
    b = right.copy()
    rng = np.random.default_rng(seed)
    idx = np.arange(len(PORTS), left.cfg.n_elements)
    perm = idx.copy()
    rng.shuffle(perm)
    a.mass[idx] = left.mass[perm]
    b.mass[idx] = right.mass[perm]
    return a, b


def pair_class(pair: tuple[int, int]) -> str:
    key = tuple(sorted(pair))
    if key in M1_SET:
        return "M1"
    if key in M2_SET:
        return "M2"
    return "unused"


def differential_matrix_rows(
    material_1: CompositionMaterial,
    material_2: CompositionMaterial,
) -> list[dict[str, float | int | str | list[int]]]:
    rows: list[dict[str, float | int | str | list[int]]] = []
    for left, right in ALL_PAIRS:
        i1 = pair_interaction(material_1, left, right)
        i2 = pair_interaction(material_2, left, right)
        rows.append({
            "pair": [left, right],
            "class": pair_class((left, right)),
            "interaction_T1": i1,
            "interaction_T2": i2,
            "dI": float(i2 - i1),
        })
    return rows


def summarize_rows(rows: list[dict]) -> dict[str, float]:
    trained = [row for row in rows if row["class"] != "unused"]
    unused = [row for row in rows if row["class"] == "unused"]
    signed = np.asarray([
        float(row["dI"]) if row["class"] == "M1" else -float(row["dI"])
        for row in trained
    ])
    trained_abs = np.asarray([abs(float(row["dI"])) for row in trained])
    unused_abs = np.asarray([abs(float(row["dI"])) for row in unused])
    return {
        "expected_sign_fraction": float(np.mean(signed > 0.0)),
        "mean_signed_contrast": float(signed.mean()),
        "min_signed_edge": float(signed.min()),
        "trained_abs_mean": float(trained_abs.mean()),
        "unused_abs_mean": float(unused_abs.mean()),
        "trained_vs_unused_abs_ratio": float(
            trained_abs.mean() / max(unused_abs.mean(), 1e-15)
        ),
    }


def run_seed(seed: int, cfg: CompositionConfig | None = None) -> dict:
    cfg = cfg or CompositionConfig()
    t1 = train_program(seed, MATCHING_1, cfg)
    t2 = train_program(seed, MATCHING_2, cfg)
    rows = differential_matrix_rows(t1, t2)
    metrics = summarize_rows(rows)

    sh1, sh2 = same_permutation_shuffle(t1, t2, seed=900000 + seed)
    shuffle_rows = differential_matrix_rows(sh1, sh2)
    shuffle_metrics = summarize_rows(shuffle_rows)

    return {
        "seed": int(seed),
        "matching_1_counts": terminal_counts(MATCHING_1),
        "matching_2_counts": terminal_counts(MATCHING_2),
        "mass_sum_T1": float(t1.mass.sum()),
        "mass_sum_T2": float(t2.mass.sum()),
        **metrics,
        "shuffle_signed_contrast": float(shuffle_metrics["mean_signed_contrast"]),
        "shuffle_contrast_ratio": float(
            abs(shuffle_metrics["mean_signed_contrast"])
            / max(abs(metrics["mean_signed_contrast"]), 1e-15)
        ),
        "rows": rows,
    }
