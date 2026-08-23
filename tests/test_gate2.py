from __future__ import annotations

import unittest

import numpy as np

from sunday.graph_attacker import (
    make_degree_strength_rewire,
    stable_pair_interaction,
    train_on_base,
)
from sunday.nonlinear_overlap import (
    A,
    B,
    PROGRAM_AB,
    OverlapConfig,
    make_base,
    make_positions,
)


class Gate2Tests(unittest.TestCase):
    def small_cfg(self) -> OverlapConfig:
        return OverlapConfig(
            n_elements=96,
            teacher_steps=12,
            teacher_drive_steps=8,
            cycles=2,
            response_steps=20,
            response_drive_steps=4,
        )

    def test_same_graph_does_not_use_coordinates(self) -> None:
        cfg = self.small_cfg()
        positions = make_positions(12345, cfg)
        base = make_base(positions, cfg)
        left = train_on_base(positions, base, PROGRAM_AB, cfg)
        right = train_on_base(np.zeros_like(positions), base, PROGRAM_AB, cfg)
        self.assertTrue(np.array_equal(left.mass, right.mass))

    def test_degree_strength_rewire_matches_registered_resources(self) -> None:
        cfg = self.small_cfg()
        positions = make_positions(12345, cfg)
        base = make_base(positions, cfg)
        receipt = make_degree_strength_rewire(
            positions,
            base,
            cfg,
            seed=512345,
        )
        self.assertTrue(receipt.degree_exact)
        self.assertTrue(receipt.connected)
        self.assertLess(receipt.strength_rel_error, 1e-8)
        self.assertGreater(receipt.long_edge_fraction, 0.5)

    def test_stable_probe_is_finite(self) -> None:
        cfg = self.small_cfg()
        positions = make_positions(12345, cfg)
        base = make_base(positions, cfg)
        material = train_on_base(positions, base, PROGRAM_AB, cfg)
        value = stable_pair_interaction(material, A, B)
        self.assertTrue(np.isfinite(value))


if __name__ == "__main__":
    unittest.main()
