from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np


SOMA = 0
TERMINAL_A = 1
TERMINAL_B = 2
PROTECTED = (SOMA, TERMINAL_A, TERMINAL_B)


@dataclass(frozen=True)
class MicroarborConfig:
    n_elements: int = 256
    seed: int = 230826
    yz_scale: float = 0.75
    overlap_length: float = 0.28
    overlap_cutoff: float = 0.52
    dt: float = 0.035
    leak: float = 0.35
    kappa: float = 0.80
    teacher_steps: int = 80
    teacher_drive_steps: int = 50
    impulse_steps: int = 120
    impulse_drive_steps: int = 4
    mass_floor: float = 0.20
    learning_rate: float = 0.08
    train_epochs: int = 80

    @property
    def mass_budget(self) -> float:
        return float(self.n_elements)


@dataclass
class FrozenMaterial:
    positions: np.ndarray
    base: np.ndarray
    mass: np.ndarray
    cfg: MicroarborConfig

    def copy(self) -> "FrozenMaterial":
        return FrozenMaterial(
            positions=self.positions.copy(),
            base=self.base.copy(),
            mass=self.mass.copy(),
            cfg=self.cfg,
        )


@dataclass(frozen=True)
class ImpulseReceipt:
    peak: float
    auc: float
    trace: np.ndarray


def make_positions(cfg: MicroarborConfig) -> np.ndarray:
    """Seeded unstructured 3-D cloud; no tree or preferred route is planted."""
    if cfg.n_elements < 4:
        raise ValueError("n_elements must be >= 4")
    rng = np.random.default_rng(cfg.seed)
    pos = rng.uniform(-1.0, 1.0, size=(cfg.n_elements, 3))
    pos[:, 1:] *= cfg.yz_scale

    # Fixed read/write ports. Their structural masses are protected from learning.
    pos[SOMA] = np.array([0.95, 0.0, 0.0])
    pos[TERMINAL_A] = np.array([-0.95, -0.48, 0.0])
    pos[TERMINAL_B] = np.array([-0.95, +0.48, 0.0])
    return pos


def make_base_coupling(positions: np.ndarray, cfg: MicroarborConfig) -> np.ndarray:
    """Geometry-only overlap graph. Nothing in this matrix is learned."""
    delta = positions[:, None, :] - positions[None, :, :]
    r2 = np.sum(delta * delta, axis=-1)
    r = np.sqrt(r2)
    base = np.exp(-0.5 * r2 / (cfg.overlap_length**2))
    base[r > cfg.overlap_cutoff] = 0.0
    np.fill_diagonal(base, 0.0)
    return base


def initialize(cfg: MicroarborConfig | None = None) -> FrozenMaterial:
    cfg = cfg or MicroarborConfig()
    positions = make_positions(cfg)
    base = make_base_coupling(positions, cfg)
    mass = np.ones(cfg.n_elements, dtype=np.float64)
    return FrozenMaterial(positions=positions, base=base, mass=mass, cfg=cfg)


def conductance(material: FrozenMaterial) -> np.ndarray:
    """Current transfer graph induced by fixed geometry and slow structural mass."""
    m = material.mass
    return material.base * np.sqrt(np.outer(m, m))


def _fast_step(
    v: np.ndarray,
    G: np.ndarray,
    degree: np.ndarray,
    u: np.ndarray,
    cfg: MicroarborConfig,
) -> np.ndarray:
    # Diffusion on the geometry-induced conductance graph plus leak and drive.
    dv = -cfg.leak * v + cfg.kappa * (G @ v - degree * v) + u
    return v + cfg.dt * dv


def teacher_episode(material: FrozenMaterial, source: int) -> np.ndarray:
    """Drive current between one terminal and soma; return local current eligibility."""
    if source not in (TERMINAL_A, TERMINAL_B):
        raise ValueError("source must be TERMINAL_A or TERMINAL_B")
    cfg = material.cfg
    G = conductance(material)
    degree = G.sum(axis=1)
    v = np.zeros(cfg.n_elements, dtype=np.float64)
    eligibility = np.zeros(cfg.n_elements, dtype=np.float64)

    for t in range(cfg.teacher_steps):
        u = np.zeros(cfg.n_elements, dtype=np.float64)
        if t < cfg.teacher_drive_steps:
            u[source] += 1.0
            u[SOMA] -= 1.0
        v = _fast_step(v, G, degree, u, cfg)

        # Incident current is local to the current material graph.
        edge_current = np.abs(G * (v[:, None] - v[None, :]))
        eligibility += edge_current.sum(axis=1)

    eligibility /= float(cfg.teacher_steps)
    eligibility[list(PROTECTED)] = 0.0
    return eligibility


def redistribute_mass(material: FrozenMaterial, eligibility: np.ndarray) -> None:
    """Move slow mass toward used regions while preserving capacity and fixed ports."""
    cfg = material.cfg
    if eligibility.shape != material.mass.shape:
        raise ValueError("eligibility shape mismatch")

    mask = np.ones(cfg.n_elements, dtype=bool)
    mask[list(PROTECTED)] = False
    e = np.maximum(eligibility[mask], 0.0)
    mean_e = float(e.mean())
    if mean_e <= 1e-15:
        return
    e = e / mean_e

    protected_mass = float(len(PROTECTED))  # protected ports stay exactly at 1.
    free_budget = cfg.mass_budget - protected_mass
    n_free = int(mask.sum())
    allocatable = free_budget - cfg.mass_floor * n_free
    if allocatable <= 0:
        raise ValueError("mass_floor leaves no allocatable mass")

    target = cfg.mass_floor + allocatable * e / (float(e.sum()) + 1e-15)
    material.mass[mask] = (
        (1.0 - cfg.learning_rate) * material.mass[mask]
        + cfg.learning_rate * target
    )
    material.mass[list(PROTECTED)] = 1.0

    # Remove tiny floating drift without changing the learning rule.
    delta = cfg.mass_budget - float(material.mass.sum())
    material.mass[mask] += delta / n_free


def train_history(
    source: int,
    cfg: MicroarborConfig | None = None,
) -> FrozenMaterial:
    material = initialize(cfg)
    for _ in range(material.cfg.train_epochs):
        eligibility = teacher_episode(material, source)
        redistribute_mass(material, eligibility)
    return material


def impulse_response(
    material: FrozenMaterial,
    source: int,
    observer: Callable[[FrozenMaterial, np.ndarray, int], object] | None = None,
) -> ImpulseReceipt:
    """Freeze morphology, pulse one terminal, and read the soma time course."""
    if source not in (TERMINAL_A, TERMINAL_B):
        raise ValueError("source must be TERMINAL_A or TERMINAL_B")
    cfg = material.cfg
    G = conductance(material)
    degree = G.sum(axis=1)
    v = np.zeros(cfg.n_elements, dtype=np.float64)
    soma_trace = np.zeros(cfg.impulse_steps, dtype=np.float64)

    for t in range(cfg.impulse_steps):
        u = np.zeros(cfg.n_elements, dtype=np.float64)
        if t < cfg.impulse_drive_steps:
            u[source] = 1.0
        v = _fast_step(v, G, degree, u, cfg)
        soma_trace[t] = v[SOMA]
        if observer is not None:
            observer(material, v, t)

    positive = np.maximum(soma_trace, 0.0)
    return ImpulseReceipt(
        peak=float(positive.max()),
        auc=float(positive.sum() * cfg.dt),
        trace=soma_trace,
    )


def shuffled_mass(material: FrozenMaterial, seed: int) -> FrozenMaterial:
    """Preserve exact non-port mass multiset, budget, positions, and graph; permute geometry."""
    out = material.copy()
    rng = np.random.default_rng(seed)
    mask = np.ones(material.cfg.n_elements, dtype=bool)
    mask[list(PROTECTED)] = False
    values = out.mass[mask].copy()
    rng.shuffle(values)
    out.mass[mask] = values
    return out


def observer_snapshot(material: FrozenMaterial, v: np.ndarray, step: int) -> tuple[np.ndarray, ...]:
    """Pure read-only observer payload. Rendering code may consume this; dynamics may not."""
    return (
        material.positions.copy(),
        material.mass.copy(),
        v.copy(),
        np.asarray(step, dtype=np.int64),
    )
