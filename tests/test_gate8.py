import numpy as np

from sunday.relation_generality import CODES, analyze_vector, code_matrix, code_vector, design_controls


def test_registered_codes_are_independent_and_balanced():
    d = design_controls()
    assert d["rank"] == 4
    for item in d["per_code"].values():
        assert item["terminal_marginals_match"]
        assert item["distance_multiset_match"]
        assert item["trained_edges_disjoint"]


def test_code_vectors_have_six_registered_edges():
    for code in CODES:
        q = code_vector(code)
        assert np.count_nonzero(q) == 6
        assert np.sum(q == 1.0) == 3
        assert np.sum(q == -1.0) == 3


def test_ideal_registered_vector_reads_as_its_own_code():
    Q = code_matrix()
    for row, code in enumerate(CODES):
        q = Q[row]
        result = analyze_vector(q, code.name)
        assert result["expected_sign_fraction"] == 1.0
        assert result["own_signed_contrast"] == 1.0
        assert result["self_top"]
        assert result["specificity_ratio"] >= 6.0 - 1e-12
