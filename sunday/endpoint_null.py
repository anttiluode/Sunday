from __future__ import annotations

import numpy as np

from sunday.composition import ALL_PAIRS, run_seed as run_composition_seed


TRAINED_CYCLE = (
    ((1, 2), +1),
    ((2, 3), -1),
    ((3, 4), +1),
    ((4, 5), -1),
    ((5, 6), +1),
    ((1, 6), -1),
)


def _design_matrix() -> np.ndarray:
    X = np.zeros((len(ALL_PAIRS), 6), dtype=np.float64)
    for row, (left, right) in enumerate(ALL_PAIRS):
        X[row, left - 1] = 1.0
        X[row, right - 1] = 1.0
    return X


def _expected_sign(pair: tuple[int, int]) -> int:
    key = tuple(sorted(pair))
    for trained_pair, sign in TRAINED_CYCLE:
        if tuple(sorted(trained_pair)) == key:
            return sign
    return 0


def analyze_rows(rows: list[dict]) -> dict:
    y = np.asarray([float(row["dI"]) for row in rows], dtype=np.float64)
    X = _design_matrix()
    endpoint = np.linalg.lstsq(X, y, rcond=None)[0]
    pred = X @ endpoint

    centered = y - float(y.mean())
    denom = float(np.sum(centered**2))
    r2 = 1.0 - float(np.sum((y - pred) ** 2)) / max(denom, 1e-30)

    expected = np.asarray([_expected_sign(pair) for pair in ALL_PAIRS], dtype=np.int8)
    trained_mask = expected != 0
    in_sample_sign = float(np.mean(np.sign(pred[trained_mask]) == expected[trained_mask]))
    observed_sign = float(np.mean(np.sign(y[trained_mask]) == expected[trained_mask]))

    loo_correct: list[bool] = []
    trained_indices = np.flatnonzero(trained_mask)
    for held_out in trained_indices:
        keep = np.ones(len(y), dtype=bool)
        keep[held_out] = False
        endpoint_loo = np.linalg.lstsq(X[keep], y[keep], rcond=None)[0]
        prediction = float(X[held_out] @ endpoint_loo)
        loo_correct.append(bool(np.sign(prediction) == expected[held_out]))

    by_pair = {
        tuple(row["pair"]): float(row["dI"])
        for row in rows
    }
    cycle_contrast = float(
        by_pair[(1, 2)]
        - by_pair[(2, 3)]
        + by_pair[(3, 4)]
        - by_pair[(4, 5)]
        + by_pair[(5, 6)]
        - by_pair[(1, 6)]
    )

    trained_values = np.asarray([
        by_pair[tuple(sorted(pair))]
        for pair, _ in TRAINED_CYCLE
    ])
    cycle_product = float(np.prod(trained_values))

    return {
        "observed_trained_sign_fraction": observed_sign,
        "additive_r2": float(r2),
        "additive_in_sample_trained_sign_accuracy": in_sample_sign,
        "additive_loo_trained_sign_accuracy": float(np.mean(loo_correct)),
        "cycle_contrast": cycle_contrast,
        "trained_cycle_product": cycle_product,
        "trained_cycle_product_negative": bool(cycle_product < 0.0),
        "endpoint_scalars": endpoint.tolist(),
    }


def run_seed(seed: int) -> dict:
    composition = run_composition_seed(seed)
    analysis = analyze_rows(composition["rows"])
    return {
        "seed": int(seed),
        "mass_sum_T1": composition["mass_sum_T1"],
        "mass_sum_T2": composition["mass_sum_T2"],
        "matching_1_counts": composition["matching_1_counts"],
        "matching_2_counts": composition["matching_2_counts"],
        **analysis,
    }
