from __future__ import annotations

import unittest

from experiments.audit_reservoir_null import analyze_seed as analyze_reservoir
from experiments.audit_ring_symmetry import symmetry_objects


class AuditRegressionTests(unittest.TestCase):
    def test_dormant_reservoir_preserves_registered_relation_rank(self):
        row = analyze_reservoir(520000)
        self.assertEqual(row["registered_rank"], 7)
        self.assertEqual(row["dormant_feature_rank"], 7)
        self.assertEqual(row["minimum_loo_feature_rank"], 7)
        self.assertLess(row["loo_q_reconstruction_nmse"], 1e-20)
        self.assertGreater(row["loo_q_reconstruction_cosine"], 1.0 - 1e-12)

    def test_ring_relation_span_decomposition(self):
        obj = symmetry_objects()
        self.assertEqual(obj["Q"].shape, (16, 15))
        self.assertEqual(obj["sector_dimensions"], {"1": 2, "2": 4, "3": 1})
        self.assertEqual(obj["candidate"].shape, (15, 3))
        self.assertEqual(obj["broad"].shape, (15, 5))


if __name__ == "__main__":
    unittest.main()
