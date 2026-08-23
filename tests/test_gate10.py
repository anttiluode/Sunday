import numpy as np

from sunday.composition import CompositionConfig, PORTS
from sunday.dormant_jacobian import optimal_scalar, permute_write_locations


def test_same_permutation_preserves_write_gram_and_ports():
    cfg = CompositionConfig()
    rng = np.random.default_rng(7)
    W = rng.standard_normal((15, cfg.n_elements))
    W[:, :len(PORTS)] = 0.0
    P = permute_write_locations(W, seed=1234, cfg=cfg)

    assert np.array_equal(P[:, :len(PORTS)], W[:, :len(PORTS)])
    assert np.allclose(W @ W.T, P @ P.T, rtol=0.0, atol=1e-12)
    assert np.allclose(np.sort(W[:, len(PORTS):], axis=1),
                       np.sort(P[:, len(PORTS):], axis=1))


def test_optimal_scalar_recovers_known_gain():
    rng = np.random.default_rng(11)
    x = rng.standard_normal((16, 15))
    y = 3.25 * x
    assert abs(optimal_scalar(x, y) - 3.25) < 1e-12
