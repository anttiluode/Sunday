import numpy as np

from sunday.relation_tomography import code_matrix, design_controls, enumerate_codes


def test_tomography_family_has_registered_rank_seven():
    codes = enumerate_codes()
    Q = code_matrix()
    assert len(codes) == 16
    assert Q.shape == (16, 15)
    assert np.linalg.matrix_rank(Q) == 7


def test_every_leave_one_out_family_still_spans_rank_seven():
    Q = code_matrix()
    for i in range(len(Q)):
        assert np.linalg.matrix_rank(np.delete(Q, i, axis=0)) == 7


def test_all_codes_match_controls():
    d = design_controls()
    assert d["code_count"] == 16
    assert d["rank"] == 7
    assert d["all_loo_rank"] == 7
    for item in d["per_code"].values():
        assert item["terminal_marginals_match"]
        assert item["distance_multiset_match"]
        assert item["trained_edges_disjoint"]
