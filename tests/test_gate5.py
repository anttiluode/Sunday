import unittest

import numpy as np

from sunday.boundary_alignment import PAIRINGS, pairing_is_aligned, pairing_is_crossed


class Gate5Tests(unittest.TestCase):
    def test_two_two_partition_has_one_aligned_pairing(self):
        group = np.zeros(8, dtype=np.int8)
        group[1] = 0
        group[2] = 1
        group[3] = 0
        group[4] = 1
        aligned = [pairing_is_aligned(group, p) for p in PAIRINGS]
        crossed = [pairing_is_crossed(group, p) for p in PAIRINGS]
        self.assertEqual(sum(aligned), 1)
        self.assertEqual(sum(crossed), 2)

    def test_pairing_classification_changes_with_boundary_not_graph(self):
        group = np.zeros(8, dtype=np.int8)
        group[[1, 2]] = 0
        group[[3, 4]] = 1
        self.assertTrue(pairing_is_aligned(group, PAIRINGS[0]))
        self.assertTrue(pairing_is_crossed(group, PAIRINGS[1]))
        self.assertTrue(pairing_is_crossed(group, PAIRINGS[2]))


if __name__ == "__main__":
    unittest.main()
