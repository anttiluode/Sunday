import unittest

from sunday.composition import MATCHING_1, MATCHING_2, M1_SET, M2_SET, terminal_counts


class Gate6Tests(unittest.TestCase):
    def test_matchings_have_equal_terminal_marginals(self):
        self.assertEqual(terminal_counts(MATCHING_1), terminal_counts(MATCHING_2))
        self.assertTrue(all(v == 1 for v in terminal_counts(MATCHING_1).values()))

    def test_matchings_are_disjoint(self):
        self.assertEqual(M1_SET & M2_SET, set())
        self.assertEqual(len(M1_SET), 3)
        self.assertEqual(len(M2_SET), 3)


if __name__ == "__main__":
    unittest.main()
