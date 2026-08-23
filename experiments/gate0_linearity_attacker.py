from __future__ import annotations

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
    conductance,
    train_history,
)


def simulate(material, drive: np.ndarray) -> np.ndarray:
    cfg = material.cfg
    if drive.shape != (cfg.impulse_steps, cfg.n_elements):
        raise ValueError("drive shape mismatch")
    G = conductance(material)
    degree = G.sum(axis=1)
    v = np.zeros(cfg.n_elements, dtype=np.float64)
    states = np.zeros((cfg.impulse_steps, cfg.n_elements), dtype=np.float64)
    for t in range(cfg.impulse_steps):
        dv = -cfg.leak * v + cfg.kappa * (G @ v - degree * v) + drive[t]
        v = v + cfg.dt * dv
        states[t] = v
    return states


def pulse(cfg: MicroarborConfig, terminal: int, amplitude: float = 1.0) -> np.ndarray:
    drive = np.zeros((cfg.impulse_steps, cfg.n_elements), dtype=np.float64)
    drive[: cfg.impulse_drive_steps, terminal] = amplitude
    return drive


def attack(material) -> dict[str, float]:
    cfg = material.cfg
    a = pulse(cfg, TERMINAL_A)
    b = pulse(cfg, TERMINAL_B)
    ra = simulate(material, a)
    rb = simulate(material, b)
    rab = simulate(material, a + b)
    r2a = simulate(material, 2.0 * a)

    superposition_abs = float(np.max(np.abs(rab - (ra + rb))))
    scaling_abs = float(np.max(np.abs(r2a - 2.0 * ra)))
    scale = max(float(np.max(np.abs(rab))), 1e-30)
    return {
        "superposition_max_abs_error": superposition_abs,
        "superposition_relative_error": superposition_abs / scale,
        "scaling_max_abs_error": scaling_abs,
        "soma_superposition_max_abs_error": float(
            np.max(np.abs(rab[:, SOMA] - (ra[:, SOMA] + rb[:, SOMA])))
        ),
    }


def main() -> None:
    cfg = MicroarborConfig()
    for name, material in (
        ("A-trained", train_history(TERMINAL_A, cfg)),
        ("B-trained", train_history(TERMINAL_B, cfg)),
    ):
        result = attack(material)
        print(name)
        for key, value in result.items():
            print(f"  {key}: {value:.12e}")

    print()
    print("Interpretation: the frozen Gate 0 material is a linear transfer operator.")
    print("It has learned spatial routing, but it does not yet create nonlinear input interactions.")


if __name__ == "__main__":
    main()
