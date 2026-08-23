from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

SOMA = 0
A = 1
B = 2
C = 3
D = 4
PORTS = (SOMA, A, B, C, D)
PROGRAM_AB = ((A, B), (C,), (D,))
PROGRAM_CD = ((C, D), (A,), (B,))


@dataclass(frozen=True)
class OverlapConfig:
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
class OverlapMaterial:
    positions: np.ndarray
    base: np.ndarray
    mass: np.ndarray
    cfg: OverlapConfig

    def copy(self) -> "OverlapMaterial":
        return OverlapMaterial(
            positions=self.positions.copy(),
            base=self.base.copy(),
            mass=self.mass.copy(),
            cfg=self.cfg,
        )


def terminal_counts(program: Iterable[Iterable[int]]) -> dict[int, int]:
    counts = {A: 0, B: 0, C: 0, D: 0}
    for episode in program:
        for terminal in episode:
            counts[terminal] += 1
    return counts


def make_positions(seed: int, cfg: OverlapConfig) -> np.ndarray:
    rng = np.random.default_rng(seed)
    pos = rng.uniform(-1.0, 1.0, size=(cfg.n_elements, 3))
    pos[:, 1:] *= cfg.yz_scale
    pos[SOMA] = np.array([0.95, 0.0, 0.0])

    # Four fixed ports on a circle. This specifies ports, not an internal tree.
    for q, terminal in enumerate((A, B, C, D)):
        angle = 2.0 * np.pi * q / 4.0
        pos[terminal] = np.array([
            -0.95,
            cfg.terminal_radius * np.cos(angle),
            cfg.terminal_radius * np.sin(angle),
        ])
    return pos


def make_base(positions: np.ndarray, cfg: OverlapConfig) -> np.ndarray:
    delta = positions[:, None, :] - positions[None, :, :]
    r2 = np.sum(delta * delta, axis=-1)
    r = np.sqrt(r2)
    base = np.exp(-0.5 * r2 / (cfg.overlap_length**2))
    base[r > cfg.overlap_cutoff] = 0.0
    np.fill_diagonal(base, 0.0)
    return base


def initialize(seed: int, cfg: OverlapConfig | None = None) -> OverlapMaterial:
    cfg = cfg or OverlapConfig()
    positions = make_positions(seed, cfg)
    return OverlapMaterial(
        positions=positions,
        base=make_base(positions, cfg),
        mass=np.ones(cfg.n_elements, dtype=np.float64),
        cfg=cfg,
    )


def conductance(material: OverlapMaterial) -> np.ndarray:
    return material.base * np.sqrt(np.outer(material.mass, material.mass))


def teacher_episode(material: OverlapMaterial, sources: tuple[int, ...]) -> np.ndarray:
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


def redistribute_mass(material: OverlapMaterial, eligibility: np.ndarray) -> None:
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
    program: tuple[tuple[int, ...], ...],
    cfg: OverlapConfig | None = None,
) -> OverlapMaterial:
    cfg = cfg or OverlapConfig()
    material = initialize(seed, cfg)
    for _ in range(cfg.cycles):
        for episode in program:
            eligibility = teacher_episode(material, episode)
            redistribute_mass(material, eligibility)
    return material


def drive_matrix(
    material: OverlapMaterial,
    sources: tuple[int, ...],
    amplitude: float,
) -> np.ndarray:
    cfg = material.cfg
    drive = np.zeros((cfg.response_steps, cfg.n_elements), dtype=np.float64)
    for source in sources:
        drive[: cfg.response_drive_steps, source] += amplitude
    return drive


def simulate(
    material: OverlapMaterial,
    sources: tuple[int, ...],
    *,
    amplitude: float,
    mode: str = "linear",
) -> np.ndarray:
    """Return all compartment states. Nonlinearity is fixed and local; no new learned weights."""
    cfg = material.cfg
    drive = drive_matrix(material, sources, amplitude)
    G = conductance(material)
    degree = G.sum(axis=1)
    v = np.zeros(cfg.n_elements, dtype=np.float64)
    states = np.zeros((cfg.response_steps, cfg.n_elements), dtype=np.float64)

    if mode not in {"linear", "distributed", "soma_only"}:
        raise ValueError("mode must be linear, distributed, or soma_only")

    for t in range(cfg.response_steps):
        nonlinear = np.zeros_like(v)
        if mode == "distributed":
            nonlinear = -cfg.nonlinear_gamma * v**3
        elif mode == "soma_only":
            nonlinear[SOMA] = -cfg.nonlinear_gamma * v[SOMA] ** 3

        v += cfg.dt * (
            -cfg.leak * v
            + cfg.kappa * (G @ v - degree * v)
            + drive[t]
            + nonlinear
        )
        states[t] = v
    return states


def route_signature(material: OverlapMaterial, terminal: int) -> np.ndarray:
    states = simulate(material, (terminal,), amplitude=1.0, mode="linear")
    signature = np.sum(np.abs(states), axis=0)
    signature[list(PORTS)] = 0.0
    return signature / (float(np.linalg.norm(signature)) + 1e-15)


def route_overlap(material: OverlapMaterial, left: int, right: int) -> float:
    return float(route_signature(material, left) @ route_signature(material, right))


def soma_auc(states: np.ndarray, dt: float) -> float:
    return float(np.maximum(states[:, SOMA], 0.0).sum() * dt)


def pair_interaction(
    material: OverlapMaterial,
    left: int,
    right: int,
    *,
    mode: str = "distributed",
) -> float:
    cfg = material.cfg
    amp = cfg.nonlinear_probe_amplitude
    left_states = simulate(material, (left,), amplitude=amp, mode=mode)
    right_states = simulate(material, (right,), amplitude=amp, mode=mode)
    joint_states = simulate(material, (left, right), amplitude=amp, mode=mode)
    separate = soma_auc(left_states, cfg.dt) + soma_auc(right_states, cfg.dt)
    joint = soma_auc(joint_states, cfg.dt)
    return (separate - joint) / max(separate, 1e-15)


def same_permutation_shuffle(
    left: OverlapMaterial,
    right: OverlapMaterial,
    seed: int,
) -> tuple[OverlapMaterial, OverlapMaterial]:
    """Preserve both mass histograms but destroy their relation to 3-D position with one permutation."""
    a = left.copy()
    b = right.copy()
    rng = np.random.default_rng(seed)
    idx = np.arange(len(PORTS), left.cfg.n_elements)
    perm = idx.copy()
    rng.shuffle(perm)
    a.mass[idx] = left.mass[perm]
    b.mass[idx] = right.mass[perm]
    return a, b
