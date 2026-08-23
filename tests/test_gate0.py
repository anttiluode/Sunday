from __future__ import annotations

import unittest

import numpy as np

from sunday.microarbor import (
    MicroarborConfig,
    TERMINAL_A,
    TERMINAL_B,
    impulse_response,
    initialize,
    observer_snapshot,
    shuffled_mass,
    train_history,
)


class Gate0Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cfg = MicroarborConfig()
        cls.uniform = initialize(cls.cfg)
        cls.a = train_history(TERMINAL_A, cls.cfg)
        cls.b = train_history(TERMINAL_B, cls.cfg)

    def test_fixed_capacity_and_ports(self) -> None:
        self.assertEqual(len(self.a.mass), self.cfg.n_elements)
        self.assertAlmostEqual(float(self.a.mass.sum()), self.cfg.mass_budget, places=10)
        self.assertAlmostEqual(float(self.b.mass.sum()), self.cfg.mass_budget, places=10)
        np.testing.assert_array_equal(self.a.positions, self.b.positions)
        np.testing.assert_array_equal(self.a.base, self.b.base)
        np.testing.assert_array_equal(self.a.mass[:3], np.ones(3))
        np.testing.assert_array_equal(self.b.mass[:3], np.ones(3))

    def test_histories_create_terminal_specific_transfer(self) -> None:
        aa = impulse_response(self.a, TERMINAL_A).peak
        ab = impulse_response(self.a, TERMINAL_B).peak
        ba = impulse_response(self.b, TERMINAL_A).peak
        bb = impulse_response(self.b, TERMINAL_B).peak
        self.assertGreater(aa / ab, 1.20)
        self.assertGreater(bb / ba, 1.20)

    def test_geometry_shuffle_preserves_values_but_damages_transfer(self) -> None:
        learned = impulse_response(self.a, TERMINAL_A).peak
        sh = shuffled_mass(self.a, 1234)
        self.assertAlmostEqual(float(sh.mass.sum()), float(self.a.mass.sum()), places=12)
        np.testing.assert_array_equal(np.sort(sh.mass[3:]), np.sort(self.a.mass[3:]))
        np.testing.assert_array_equal(sh.positions, self.a.positions)
        shuffled_peak = impulse_response(sh, TERMINAL_A).peak
        self.assertGreater(learned, 1.25 * shuffled_peak)

    def test_observer_cannot_feed_back(self) -> None:
        plain = impulse_response(self.a, TERMINAL_A)
        observed = impulse_response(self.a, TERMINAL_A, observer_snapshot)
        np.testing.assert_array_equal(plain.trace, observed.trace)


if __name__ == "__main__":
    unittest.main()
