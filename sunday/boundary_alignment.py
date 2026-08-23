from __future__ import annotations

import numpy as np

from sunday.graph_attacker import (
    make_degree_strength_rewire,
    stable_pair_interaction,
    train_on_base,
)
from sunday.low_gap_attacker import (
    _balanced_random_partition,
    make_low_gap_modular,
)
from sunday.nonlinear_overlap import (
    A,
    B,
    C,
    D,
    OverlapConfig,
    make_base,
    make_positions,
    route_overlap,
)


PAIRINGS = (
    ((A, B), (C, D)),
    ((A, C), (B, D)),
    ((A, D), (B, C)),
)


def first_two_two_partition(seed: int, cfg: OverlapConfig, max_index: int = 128) -> tuple[int, np.ndarray]:
    """Deterministically choose the first Gate-4 random partition with a 2+2 terminal split."""
    for partition_index in range(max_index):
        group = _balanced_random_partition(
            cfg.n_elements,
            seed + 1300003 + 7919 * partition_index,
        )
        terminal_groups = group[[A, B, C, D]]
        if int(terminal_groups.sum()) == 2:
            return partition_index, group
    raise RuntimeError(f"no 2+2 terminal partition found for seed={seed}")


def pairing_is_aligned(group: np.ndarray, pairing: tuple[tuple[int, int], tuple[int, int]]) -> bool:
    left, right = pairing
    return bool(
        group[left[0]] == group[left[1]]
        and group[right[0]] == group[right[1]]
    )


def pairing_is_crossed(group: np.ndarray, pairing: tuple[tuple[int, int], tuple[int, int]]) -> bool:
    left, right = pairing
    return bool(
        group[left[0]] != group[left[1]]
        and group[right[0]] != group[right[1]]
    )


def relation_for_pairing(
    positions: np.ndarray,
    base: np.ndarray,
    pairing: tuple[tuple[int, int], tuple[int, int]],
    cfg: OverlapConfig,
) -> dict[str, float]:
    """Run Gate-1 matched histories after assigning semantic pair roles to physical terminals."""
    (a, b), (c, d) = pairing
    program_ab = ((a, b), (c,), (d,))
    program_cd = ((c, d), (a,), (b,))

    hab = train_on_base(positions, base, program_ab, cfg)
    hcd = train_on_base(positions, base, program_cd, cfg)

    overlap_ab = route_overlap(hcd, a, b) - route_overlap(hab, a, b)
    overlap_cd = route_overlap(hab, c, d) - route_overlap(hcd, c, d)
    interaction_ab = stable_pair_interaction(hcd, a, b) - stable_pair_interaction(hab, a, b)
    interaction_cd = stable_pair_interaction(hab, c, d) - stable_pair_interaction(hcd, c, d)

    return {
        "overlap_AB": float(overlap_ab),
        "overlap_CD": float(overlap_cd),
        "mean_overlap": float((overlap_ab + overlap_cd) / 2.0),
        "interaction_AB": float(interaction_ab),
        "interaction_CD": float(interaction_cd),
        "mean_interaction": float((interaction_ab + interaction_cd) / 2.0),
    }


def run_seed(seed: int, cfg: OverlapConfig | None = None) -> dict:
    cfg = cfg or OverlapConfig()
    positions = make_positions(seed, cfg)
    geometric_base = make_base(positions, cfg)

    expander = make_degree_strength_rewire(
        positions,
        geometric_base,
        cfg,
        seed=seed + 500000,
    )

    partition_index, group = first_two_two_partition(seed, cfg)
    modular = make_low_gap_modular(
        positions,
        geometric_base,
        expander.base,
        cfg,
        seed=seed,
        partition_index=partition_index,
    )

    pairing_rows: list[dict] = []
    for pairing_index, pairing in enumerate(PAIRINGS):
        aligned = pairing_is_aligned(group, pairing)
        crossed = pairing_is_crossed(group, pairing)
        relation = relation_for_pairing(positions, modular.base, pairing, cfg)
        pairing_rows.append({
            "pairing_index": pairing_index,
            "pairing": [list(pairing[0]), list(pairing[1])],
            "aligned": aligned,
            "crossed": crossed,
            **relation,
        })

    aligned_rows = [row for row in pairing_rows if row["aligned"]]
    crossed_rows = [row for row in pairing_rows if row["crossed"]]
    if len(aligned_rows) != 1 or len(crossed_rows) != 2:
        raise RuntimeError(
            f"expected one aligned and two crossed pairings; got {len(aligned_rows)} and {len(crossed_rows)}"
        )

    aligned = aligned_rows[0]
    cross_interactions = np.asarray([row["mean_interaction"] for row in crossed_rows], dtype=np.float64)
    cross_overlaps = np.asarray([row["mean_overlap"] for row in crossed_rows], dtype=np.float64)
    cross_mean_interaction = float(cross_interactions.mean())
    cross_mean_overlap = float(cross_overlaps.mean())

    return {
        "seed": int(seed),
        "partition_index": int(partition_index),
        "ports_group": group[:5].astype(int).tolist(),
        "graph": {
            "connected": modular.connected,
            "degree_exact": modular.degree_exact,
            "strength_rel_error": modular.strength_rel_error,
            "gap_ratio": modular.gap_ratio,
            "long_edge_fraction": modular.long_edge_fraction,
            "clustering_ratio": modular.clustering_ratio,
        },
        "pairings": pairing_rows,
        "aligned_interaction": float(aligned["mean_interaction"]),
        "cross_mean_interaction": cross_mean_interaction,
        "cross_max_interaction": float(cross_interactions.max()),
        "aligned_overlap": float(aligned["mean_overlap"]),
        "cross_mean_overlap": cross_mean_overlap,
        "alignment_gain": float(
            aligned["mean_interaction"] / max(cross_mean_interaction, 1e-15)
        ),
        "aligned_beats_cross_mean": bool(aligned["mean_interaction"] > cross_mean_interaction),
        "aligned_beats_both_crosses": bool(aligned["mean_interaction"] > cross_interactions.max()),
    }
