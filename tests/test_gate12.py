import numpy as np

from sunday.pretraining_routing import CANDIDATES, TARGET_DISTANCES, design_controls
from sunday.read_aware_routing import relation_metrics


def test_gate12_candidate_geometry_is_exactly_matched():
    controls = design_controls()
    assert controls["candidate_count"] == 18
    assert len(CANDIDATES) == 18
    for control in controls["per_candidate"].values():
        assert tuple(control["arm_a_distances"]) == TARGET_DISTANCES
        assert tuple(control["arm_b_distances"]) == TARGET_DISTANCES
        assert control["terminal_marginals_match"]
        assert control["trained_edges_disjoint"]


def test_clean_utility_keeps_relation_reversal_signed():
    q = np.array([1, -1, 0, 0, 0, 0], dtype=float)
    good = relation_metrics(q, q)
    bad = relation_metrics(q, -q)
    assert good["clean_utility"] > 0
    assert bad["clean_utility"] < 0
    assert np.isclose(abs(good["clean_utility"]), abs(bad["clean_utility"]))


def test_clean_utility_penalizes_orthogonal_leakage():
    q = np.array([1, -1, 0, 0, 0, 0], dtype=float)
    clean = q.copy()
    leaky = q.copy()
    leaky[2:] = 5.0
    assert relation_metrics(q, clean)["clean_utility"] > relation_metrics(q, leaky)["clean_utility"]
