from __future__ import annotations

import unittest

import numpy as np

from sunday.nonlinear_overlap import (
    A, B, C, D,
    OverlapConfig,
    PROGRAM_AB,
    PROGRAM_CD,
    pair_interaction,
    route_overlap,
    same_permutation_shuffle,
    terminal_counts,
    train_program,
)


class Gate1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cfg = OverlapConfig(cycles=20)
        cls.hab = train_program(230826, PROGRAM_AB, cls.cfg)
        cls.hcd = train_program(230826, PROGRAM_CD, cls.cfg)

    def test_programs_match_each_terminal_count(self) -> None:
        self.assertEqual(terminal_counts(PROGRAM_AB), terminal_counts(PROGRAM_CD))
        self.assertEqual(terminal_counts(PROGRAM_AB), {A: 1, B: 1, C: 1, D: 1})

    def test_capacity_and_geometry_are_matched(self) -> None:
        np.testing.assert_array_equal(self.hab.positions, self.hcd.positions)
        np.testing.assert_array_equal(self.hab.base, self.hcd.base)
        self.assertAlmostEqual(float(self.hab.mass.sum()), self.cfg.mass_budget, places=10)
        self.assertAlmostEqual(float(self.hcd.mass.sum()), self.cfg.mass_budget, places=10)

    def test_coactivation_history_changes_pair_overlap(self) -> None:
        sep_ab = route_overlap(self.hcd, A, B) - route_overlap(self.hab, A, B)
        sep_cd = route_overlap(self.hab, C, D) - route_overlap(self.hcd, C, D)
        self.assertGreater(sep_ab, 0.0)
        self.assertGreater(sep_cd, 0.0)

    def test_distributed_nonlinearity_reads_structural_difference(self) -> None:
        distributed = (
            pair_interaction(self.hcd, A, B, mode="distributed")
            - pair_interaction(self.hab, A, B, mode="distributed")
        )
        soma_only = abs(
            pair_interaction(self.hcd, A, B, mode="soma_only")
            - pair_interaction(self.hab, A, B, mode="soma_only")
        )
        self.assertGreater(distributed, 20.0 * max(soma_only, 1e-12))

    def test_shuffle_preserves_mass_multisets(self) -> None:
        sa, sb = same_permutation_shuffle(self.hab, self.hcd, seed=1234)
        np.testing.assert_array_equal(np.sort(sa.mass[5:]), np.sort(self.hab.mass[5:]))
        np.testing.assert_array_equal(np.sort(sb.mass[5:]), np.sort(self.hcd.mass[5:]))
        np.testing.assert_array_equal(sa.positions, self.hab.positions)
        np.testing.assert_array_equal(sb.positions, self.hcd.positions)


if __name__ == "__main__":
    unittest.main()
