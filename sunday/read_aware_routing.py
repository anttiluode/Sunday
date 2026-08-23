from __future__ import annotations

import numpy as np

from sunday.composition import CompositionConfig
from sunday.dormant_jacobian import dormant_operator
from sunday.pretraining_routing import CANDIDATES, finite_candidate, score_candidates


def relation_metrics(q: np.ndarray, y: np.ndarray) -> dict[str, float]:
    """Strength, fidelity and leakage for one registered relation vector."""
    q = np.asarray(q, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    trained = q != 0.0
    unused = ~trained

    own = float(q @ y / np.count_nonzero(trained))
    cosine = float(
        (q @ y)
        / (np.linalg.norm(q) * np.linalg.norm(y) + 1e-30)
    )
    trained_abs = float(np.mean(np.abs(y[trained])))
    unused_abs = float(np.mean(np.abs(y[unused])))

    # Signed strength discounted by directional impurity.  abs(cosine) keeps
    # the sign of `own`, so a reversed relation cannot win by squaring it.
    clean_utility = float(own * abs(cosine))

    return {
        "own_signed_contrast": own,
        "direction_cosine": cosine,
        "clean_utility": clean_utility,
        "trained_abs_mean": trained_abs,
        "unused_abs_mean": unused_abs,
        "trained_unused_ratio": float(
            trained_abs / max(unused_abs, 1e-15)
        ),
        "expected_sign_fraction": float(np.mean(
            np.sign(y[trained]) == np.sign(q[trained])
        )),
    }


def dormant_candidate_predictions(
    seed: int,
    cfg: CompositionConfig | None = None,
) -> dict:
    """All routing scores computed before finite training."""
    cfg = cfg or CompositionConfig()
    dormant = dormant_operator(seed, cfg=cfg)
    W = np.asarray(dormant["W"], dtype=np.float64)
    B0 = np.asarray(dormant["B0"], dtype=np.float64)

    write_scores = score_candidates(W)
    predictions = []
    for candidate in CANDIDATES:
        q = np.asarray(candidate.vector, dtype=np.float64)
        y0 = q @ B0
        metrics = relation_metrics(q, y0)
        predictions.append({
            "name": candidate.name,
            "predicted_y": y0.tolist(),
            **metrics,
        })

    clean_scores = np.asarray([
        entry["clean_utility"] for entry in predictions
    ], dtype=np.float64)
    contrast_scores = np.asarray([
        entry["own_signed_contrast"] for entry in predictions
    ], dtype=np.float64)

    return {
        "W": W,
        "B0": B0,
        "write_scores": write_scores,
        "predictions": predictions,
        "read_best_index": int(np.argmax(clean_scores)),
        "contrast_best_index": int(np.argmax(contrast_scores)),
        "write_best_index": int(np.argmax(write_scores)),
    }


def run_seed(seed: int, cfg: CompositionConfig | None = None) -> dict:
    cfg = cfg or CompositionConfig()
    dormant = dormant_candidate_predictions(seed, cfg)

    finite = []
    for candidate in CANDIDATES:
        entry = finite_candidate(seed, candidate, cfg)
        q = np.asarray(candidate.vector, dtype=np.float64)
        metrics = relation_metrics(q, np.asarray(entry["differential"], dtype=np.float64))
        finite.append({
            **entry,
            **metrics,
        })

    W = np.asarray(dormant["W"], dtype=np.float64)
    return {
        "seed": int(seed),
        "write_scores": dormant["write_scores"].tolist(),
        "predictions": dormant["predictions"],
        "read_best_index": int(dormant["read_best_index"]),
        "contrast_best_index": int(dormant["contrast_best_index"]),
        "write_best_index": int(dormant["write_best_index"]),
        "finite": finite,
        "max_one_step_write_mass_sum_error": float(
            np.max(np.abs(W.sum(axis=1)))
        ),
    }
