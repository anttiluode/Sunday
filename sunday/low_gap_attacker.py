from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from sunday.graph_attacker import (
    _edge_list,
    _is_connected,
    _strength_scale,
    make_degree_strength_rewire,
    stable_pair_interaction,
    train_on_base,
)
from sunday.nonlinear_overlap import (
    A,
    B,
    C,
    D,
    PROGRAM_AB,
    PROGRAM_CD,
    OverlapConfig,
    make_base,
    make_positions,
    route_overlap,
)
from sunday.topology_dial import _graph_metrics


PARTITIONS_PER_SEED = 3
WEIGHT_LOG_TOL = 0.20
CHECK_EVERY = 20


@dataclass(frozen=True)
class ModularReceipt:
    base: np.ndarray
    group: np.ndarray
    accepted_swaps: int
    connected: bool
    degree_exact: bool
    strength_rel_error: float
    gap: float
    gap_ratio: float
    long_edge_fraction: float
    clustering: float
    clustering_ratio: float


def _base_from_weighted_edges(
    n: int,
    edges: list[tuple[int, int]],
    weights: np.ndarray,
) -> np.ndarray:
    base = np.zeros((n, n), dtype=np.float64)
    for (i, j), weight in zip(edges, weights):
        base[i, j] = weight
        base[j, i] = weight
    return base


def _balanced_random_partition(n: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    perm = rng.permutation(n)
    group = np.zeros(n, dtype=np.int8)
    group[perm[n // 2 :]] = 1
    return group


def make_low_gap_modular(
    positions: np.ndarray,
    geometric_base: np.ndarray,
    expander_base: np.ndarray,
    cfg: OverlapConfig,
    *,
    seed: int,
    partition_index: int,
) -> ModularReceipt:
    """Impose a random non-geometric community bottleneck while preserving node degree."""
    geo_degree = np.sum(geometric_base > 0.0, axis=1)
    target_strength = geometric_base.sum(axis=1)
    geo_clustering, _, _, geo_gap = _graph_metrics(geometric_base)
    target_gap = 1.15 * geo_gap

    group = _balanced_random_partition(
        cfg.n_elements,
        seed + 1300003 + 7919 * partition_index,
    )
    edges = _edge_list(expander_base)
    weights = np.asarray([expander_base[i, j] for i, j in edges], dtype=np.float64)
    work = [tuple(edge) for edge in edges]
    edge_set = set(work)

    rng = np.random.default_rng(seed + 1700009 + 104729 * partition_index)
    accepted = 0
    tries = 0
    max_swaps = max(10000, 8 * len(edges))
    max_tries = max_swaps * 200
    final: tuple[np.ndarray, float, float] | None = None

    while accepted < max_swaps and tries < max_tries:
        tries += 1
        ia, ib = rng.integers(0, len(work), size=2)
        if ia == ib:
            continue
        ia = int(ia)
        ib = int(ib)
        a, b = work[ia]
        c, d = work[ib]
        if len({a, b, c, d}) < 4:
            continue

        # Both selected edges must cross the random cut.
        if group[a] == group[b] or group[c] == group[d]:
            continue
        if group[a] == 1:
            a, b = b, a
        if group[c] == 1:
            c, d = d, c
        if not (group[a] == group[c] == 0 and group[b] == group[d] == 1):
            continue

        w1 = float(weights[ia])
        w2 = float(weights[ib])
        if abs(math.log((w1 + 1e-15) / (w2 + 1e-15))) > WEIGHT_LOG_TOL:
            continue

        e1 = tuple(sorted((a, c)))
        e2 = tuple(sorted((b, d)))
        old1, old2 = work[ia], work[ib]
        if e1 == e2 or e1[0] == e1[1] or e2[0] == e2[1]:
            continue
        occupied = edge_set - {old1, old2}
        if e1 in occupied or e2 in occupied:
            continue

        edge_set.remove(old1)
        edge_set.remove(old2)
        edge_set.add(e1)
        edge_set.add(e2)
        work[ia] = e1
        work[ib] = e2
        accepted += 1

        if accepted % CHECK_EVERY != 0:
            continue

        raw = _base_from_weighted_edges(cfg.n_elements, work, weights)
        scaled, strength_rel_error = _strength_scale(raw, target_strength)
        if not _is_connected(cfg.n_elements, _edge_list(scaled)):
            continue
        _, _, _, gap = _graph_metrics(scaled)
        if gap <= target_gap:
            final = (scaled, strength_rel_error, gap)
            break

    if final is None:
        raise RuntimeError(
            f"could not reach low-gap modular target for seed={seed} partition={partition_index}; "
            f"accepted={accepted} tries={tries} target_gap={target_gap}"
        )

    base, strength_rel_error, gap = final
    degree = np.sum(base > 0.0, axis=1)
    clustering, _, _, _ = _graph_metrics(base)
    modular_edges = _edge_list(base)
    edge_lengths = np.asarray([
        np.linalg.norm(positions[i] - positions[j]) for i, j in modular_edges
    ])

    return ModularReceipt(
        base=base,
        group=group,
        accepted_swaps=accepted,
        connected=_is_connected(cfg.n_elements, modular_edges),
        degree_exact=bool(np.array_equal(degree, geo_degree)),
        strength_rel_error=float(strength_rel_error),
        gap=float(gap),
        gap_ratio=float(gap / max(geo_gap, 1e-15)),
        long_edge_fraction=float(np.mean(edge_lengths > cfg.overlap_cutoff)),
        clustering=float(clustering),
        clustering_ratio=float(clustering / max(geo_clustering, 1e-15)),
    )


def relation_metrics(
    positions: np.ndarray,
    base: np.ndarray,
    cfg: OverlapConfig,
) -> dict[str, float]:
    hab = train_on_base(positions, base, PROGRAM_AB, cfg)
    hcd = train_on_base(positions, base, PROGRAM_CD, cfg)

    overlap_ab = route_overlap(hcd, A, B) - route_overlap(hab, A, B)
    overlap_cd = route_overlap(hab, C, D) - route_overlap(hcd, C, D)
    interaction_ab = stable_pair_interaction(hcd, A, B) - stable_pair_interaction(hab, A, B)
    interaction_cd = stable_pair_interaction(hab, C, D) - stable_pair_interaction(hcd, C, D)

    return {
        "overlap_AB": float(overlap_ab),
        "overlap_CD": float(overlap_cd),
        "mean_overlap": float((overlap_ab + overlap_cd) / 2.0),
        "interaction_AB": float(interaction_ab),
        "interaction_CD": float(interaction_cd),
        "mean_interaction": float((interaction_ab + interaction_cd) / 2.0),
    }


def run_seed(
    seed: int,
    cfg: OverlapConfig | None = None,
    *,
    partitions: int = PARTITIONS_PER_SEED,
) -> dict:
    cfg = cfg or OverlapConfig()
    positions = make_positions(seed, cfg)
    geo_base = make_base(positions, cfg)
    geo_relation = relation_metrics(positions, geo_base, cfg)

    expander = make_degree_strength_rewire(
        positions,
        geo_base,
        cfg,
        seed=seed + 500000,
    )
    expander_relation = relation_metrics(positions, expander.base, cfg)

    modular_rows: list[dict] = []
    geo_abs_interaction = abs(geo_relation["mean_interaction"])
    for partition_index in range(partitions):
        modular = make_low_gap_modular(
            positions,
            geo_base,
            expander.base,
            cfg,
            seed=seed,
            partition_index=partition_index,
        )
        relation = relation_metrics(positions, modular.base, cfg)
        modular_rows.append({
            "partition_index": partition_index,
            "ports_group": modular.group[:5].astype(int).tolist(),
            "accepted_swaps": modular.accepted_swaps,
            "connected": modular.connected,
            "degree_exact": modular.degree_exact,
            "strength_rel_error": modular.strength_rel_error,
            "gap": modular.gap,
            "gap_ratio": modular.gap_ratio,
            "long_edge_fraction": modular.long_edge_fraction,
            "clustering": modular.clustering,
            "clustering_ratio": modular.clustering_ratio,
            "recovery": abs(relation["mean_interaction"]) / max(geo_abs_interaction, 1e-15),
            **relation,
        })

    return {
        "seed": int(seed),
        "geo": geo_relation,
        "expander": {
            **expander_relation,
            "gap": float(_graph_metrics(expander.base)[3]),
            "long_edge_fraction": expander.long_edge_fraction,
            "strength_rel_error": expander.strength_rel_error,
        },
        "modular": modular_rows,
    }
