import numpy as np

from sunday.pretraining_routing import (
    CANDIDATES,
    TARGET_DISTANCES,
    UNIVERSAL_BEST,
    UNIVERSAL_WORST,
    design_controls,
    score_candidates,
    shuffled_write_rows,
)


def test_geometry_equivalent_candidate_class():
    design = design_controls()
    assert design["candidate_count"] == 18
    assert design["universal_best_present"]
    assert design["universal_worst_present"]
    assert len({candidate.vector for candidate in CANDIDATES}) == 18
    assert UNIVERSAL_BEST in {candidate.vector for candidate in CANDIDATES}
    assert UNIVERSAL_WORST in {candidate.vector for candidate in CANDIDATES}

    for control in design["per_candidate"].values():
        assert tuple(control["arm_a_distances"]) == TARGET_DISTANCES
        assert tuple(control["arm_b_distances"]) == TARGET_DISTANCES
        assert control["terminal_marginals_match"]
        assert control["trained_edges_disjoint"]


def test_row_shuffle_preserves_write_singular_values_not_scores():
    rng = np.random.default_rng(123)
    W = rng.standard_normal((15, 40))
    shuffled = shuffled_write_rows(W, seed=99)
    assert np.allclose(
        np.linalg.svd(W, compute_uv=False),
        np.linalg.svd(shuffled, compute_uv=False),
        rtol=0.0,
        atol=1e-12,
    )
    assert not np.allclose(score_candidates(W), score_candidates(shuffled))
