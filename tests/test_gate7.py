import unittest

import numpy as np


class Gate7Tests(unittest.TestCase):
    def test_additive_endpoint_cycle_contrast_cancels(self):
        a = np.asarray([0.7, -1.1, 0.2, 2.0, -0.4, 0.9])
        d12 = a[0] + a[1]
        d23 = a[1] + a[2]
        d34 = a[2] + a[3]
        d45 = a[3] + a[4]
        d56 = a[4] + a[5]
        d16 = a[0] + a[5]
        contrast = d12 - d23 + d34 - d45 + d56 - d16
        self.assertAlmostEqual(float(contrast), 0.0, places=12)

    def test_pure_multiplicative_cycle_product_nonnegative(self):
        a = np.asarray([0.7, -1.1, 0.2, 2.0, -0.4, 0.9])
        product = (
            (a[0] * a[1])
            * (a[1] * a[2])
            * (a[2] * a[3])
            * (a[3] * a[4])
            * (a[4] * a[5])
            * (a[5] * a[0])
        )
        self.assertGreaterEqual(float(product), 0.0)


if __name__ == "__main__":
    unittest.main()
