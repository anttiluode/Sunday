from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import math

import numpy as np

from sunday.graph_attacker import (
    _edge_list,
    _is_connected,
    _strength_scale,
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


LEVELS = (0.0, 0.1, 0.5, 1.0, 2.0, 5.0)
WEIGHT_LOG_TOL = 0.12


@dataclass(frozen=True)
class TopologySnapshot:
    swaps_per_edge: float
    base: np.ndarray
    degree_exact: bool
    connected: bool
    strength_rel_error: float
    long_edge_fraction: float
    clustering: float
    transitivity: float
    mean_shortest_path: float
    normalized_laplacian_gap: float


def _graph_metrics(base: np.ndarray) -> tuple[float, float, float, float]:
    adj = (base > 0.0).astype(np.float64)
    degree = adj.sum(axis=1)

    # Triangles touching each node: each triangle is seen twice in (A^2 .* A) row sum.
    two_step = adj @ adj
    triangles_per_node = (two_step * adj).sum(axis=1) / 2.0
    triples_per_node = degree * (degree - 1.0) / 2.0
    local_clustering = np.divide(
        triangles_per_node,
        triples_per_node,
        out=np.zeros_like(degree),
        where=triples_per_node > 0.0,
    )
    clustering = float(local_clustering.mean())

    triangles = float(triangles_per_node.sum() / 3.0)
    triples = float(triples_per_node.sum())
    transitivity = float(3.0 * triangles / triples) if triples > 0.0 else 0.0

    n = len(adj)
    neighbors = [np.flatnonzero(adj[i]).tolist() for i in range(n)]
    distance_sum = 0.0
    distance_count = 0
    for source in range(n):
        distance = np.full(n, -1, dtype=np.int64)
        distance[source] = 0
        q: deque[int] = deque([source])
        while q:
            u = q.popleft()
            for v in neighbors[u]:
                if distance[v] < 0:
                    distance[v] = distance[u] + 1
                    q.append(v)
        reachable = distance[distance > 0]
        distance_sum += float(reachable.sum())
        distance_count += int(len(reachable))
    mean_shortest_path = distance_sum / max(distance_count, 1)

    inv_sqrt_degree = np.divide(
        1.0,
        np.sqrt(degree),
        out=np.zeros_like(degree),
        where=degree > 0.0,
    )
    normalized_adjacency = inv_sqrt_degree[:, None] * adj * inv_sqrt_degree[None, :]
    normalized_laplacian = np.eye(n) - normalized_adjacency
    eigenvalues = np.linalg.eigvalsh(normalized_laplacian)
    spectral_gap = float(eigenvalues[1]) if len(eigenvalues) > 1 else float("nan")

    return clustering, transitivity, mean_shortest_path, spectral_gap


def _snapshot(
    original_base: np.ndarray,
    positions: np.ndarray,
    cfg: OverlapConfig,
    work_edges: list[tuple[int, int]],
    weights: np.ndarray,
    swaps_per_edge: float,
) -> TopologySnapshot:
    raw = np.zeros_like(original_base)
    for (i, j), weight in zip(work_edges, weights):
        raw[i, j] = weight
        raw[j, i] = weight

    if swaps_per_edge == 0.0:
        base = original_base.copy()
        strength_rel_error = 0.0
    else:
        base, strength_rel_error = _strength_scale(raw, original_base.sum(axis=1))

    original_degree = np.sum(original_base > 0.0, axis=1)
    degree = np.sum(base > 0.0, axis=1)
    connected = _is_connected(cfg.n_elements, _edge_list(base))

    edge_lengths = np.asarray([
        np.linalg.norm(positions[i] - positions[j]) for i, j in _edge_list(base)
    ])
    long_edge_fraction = float(np.mean(edge_lengths > cfg.overlap_cutoff))
    clustering, transitivity, mean_path, gap = _graph_metrics(base)

    return TopologySnapshot(
        swaps_per_edge=float(swaps_per_edge),
        base=base,
        degree_exact=bool(np.array_equal(original_degree, degree)),
        connected=connected,
        strength_rel_error=float(strength_rel_error),
        long_edge_fraction=long_edge_fraction,
        clustering=clustering,
        transitivity=transitivity,
        mean_shortest_path=mean_path,
        normalized_laplacian_gap=gap,
    )


def make_topology_dial(
    seed: int,
    cfg: OverlapConfig | None = None,
    *,
    levels: tuple[float, ...] = LEVELS,
    weight_log_tolerance: float = WEIGHT_LOG_TOL,
) -> tuple[np.ndarray, list[TopologySnapshot]]:
    """Nested degree-preserving rewire trajectory with similar-weight swaps."""
    cfg = cfg or OverlapConfig()
    positions = make_positions(seed, cfg)
    original_base = make_base(positions, cfg)
    original_edges = _edge_list(original_base)
    edge_count = len(original_edges)
    weights = np.asarray([original_base[i, j] for i, j in original_edges], dtype=np.float64)

    requested = [int(round(level * edge_count)) for level in levels]
    targets = dict(zip(requested, levels))
    max_target = max(requested)

    work = [tuple(edge) for edge in original_edges]
    edge_set = set(work)
    rng = np.random.default_rng(seed + 910003)
    accepted = 0
    tries = 0
    max_tries = max(10000, max_target * 300)
    snapshots_by_count: dict[int, TopologySnapshot] = {}

    if 0 in targets:
        snapshots_by_count[0] = _snapshot(
            original_base, positions, cfg, work, weights, targets[0]
        )

    while accepted < max_target and tries < max_tries:
        tries += 1
        ia, ib = rng.integers(0, len(work), size=2)
        if ia == ib:
            continue
        ia = int(ia)
        ib = int(ib)
        w1 = float(weights[ia])
        w2 = float(weights[ib])
        if abs(math.log((w1 + 1e-15) / (w2 + 1e-15))) > weight_log_tolerance:
            continue

        a, b = work[ia]
        c, d = work[ib]
        if len({a, b, c, d}) < 4:
            continue

        if rng.random() < 0.5:
            e1 = tuple(sorted((a, d)))
            e2 = tuple(sorted((c, b)))
        else:
            e1 = tuple(sorted((a, c)))
            e2 = tuple(sorted((b, d)))

        if e1[0] == e1[1] or e2[0] == e2[1] or e1 == e2:
            continue
        old1, old2 = work[ia], work[ib]
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

        if accepted in targets:
            snapshots_by_count[accepted] = _snapshot(
                original_base, positions, cfg, work, weights, targets[accepted]
            )

    missing = [count for count in requested if count not in snapshots_by_count]
    if missing:
        raise RuntimeError(f"rewire trajectory did not reach targets: {missing}; accepted={accepted} tries={tries}")

    return positions, [snapshots_by_count[count] for count in requested]


def relation_metrics(
    positions: np.ndarray,
    snapshot: TopologySnapshot,
    cfg: OverlapConfig | None = None,
) -> dict[str, float]:
    cfg = cfg or OverlapConfig()
    hab = train_on_base(positions, snapshot.base, PROGRAM_AB, cfg)
    hcd = train_on_base(positions, snapshot.base, PROGRAM_CD, cfg)

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


def run_seed(seed: int, cfg: OverlapConfig | None = None) -> list[dict]:
    cfg = cfg or OverlapConfig()
    positions, snapshots = make_topology_dial(seed, cfg)
    rows: list[dict] = []
    for snapshot in snapshots:
        relation = relation_metrics(positions, snapshot, cfg)
        rows.append({
            "seed": int(seed),
            "swaps_per_edge": snapshot.swaps_per_edge,
            "degree_exact": snapshot.degree_exact,
            "connected": snapshot.connected,
            "strength_rel_error": snapshot.strength_rel_error,
            "long_edge_fraction": snapshot.long_edge_fraction,
            "clustering": snapshot.clustering,
            "transitivity": snapshot.transitivity,
            "mean_shortest_path": snapshot.mean_shortest_path,
            "normalized_laplacian_gap": snapshot.normalized_laplacian_gap,
            **relation,
        })
    return rows
