from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from sunday.nonlinear_overlap import (
    A,
    B,
    C,
    D,
    PORTS,
    PROGRAM_AB,
    PROGRAM_CD,
    OverlapConfig,
    OverlapMaterial,
    make_base,
    make_positions,
    pair_interaction,
    redistribute_mass,
    route_overlap,
    teacher_episode,
)


@dataclass(frozen=True)
class RewireReceipt:
    base: np.ndarray
    degree_exact: bool
    strength_rel_error: float
    long_edge_fraction: float
    connected: bool
    accepted_swaps: int


def _edge_list(base: np.ndarray) -> list[tuple[int, int]]:
    ii, jj = np.where(np.triu(base > 0.0, 1))
    return list(zip(ii.tolist(), jj.tolist()))


def _is_connected(n: int, edges: list[tuple[int, int]]) -> bool:
    adj: list[list[int]] = [[] for _ in range(n)]
    for i, j in edges:
        adj[i].append(j)
        adj[j].append(i)
    seen = {0}
    stack = [0]
    while stack:
        i = stack.pop()
        for j in adj[i]:
            if j not in seen:
                seen.add(j)
                stack.append(j)
    return len(seen) == n


def _degree_preserving_swaps(
    edges: list[tuple[int, int]],
    n_nodes: int,
    *,
    seed: int,
    requested_swaps: int,
) -> tuple[list[tuple[int, int]], int]:
    """Simple undirected double-edge swaps. Degree sequence is invariant by construction."""
    rng = np.random.default_rng(seed)
    work = [tuple(sorted(e)) for e in edges]
    edge_set = set(work)
    accepted = 0
    tries = 0
    max_tries = max(1000, requested_swaps * 40)

    while accepted < requested_swaps and tries < max_tries:
        tries += 1
        ia, ib = rng.integers(0, len(work), size=2)
        if ia == ib:
            continue
        a, b = work[int(ia)]
        c, d = work[int(ib)]
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

        old1, old2 = work[int(ia)], work[int(ib)]
        occupied = edge_set - {old1, old2}
        if e1 in occupied or e2 in occupied:
            continue

        edge_set.remove(old1)
        edge_set.remove(old2)
        edge_set.add(e1)
        edge_set.add(e2)
        work[int(ia)] = e1
        work[int(ib)] = e2
        accepted += 1

    if len(edge_set) != len(edges):
        raise RuntimeError("edge swap changed edge count")
    if any(i < 0 or j >= n_nodes for i, j in edge_set):
        raise RuntimeError("edge swap produced invalid node")
    return work, accepted


def _strength_scale(
    base: np.ndarray,
    target_strength: np.ndarray,
    *,
    tol: float = 1e-10,
    max_iter: int = 2000,
) -> tuple[np.ndarray, float]:
    """Symmetric diagonal scaling so row sums match target node strengths."""
    out = base.copy()
    for _ in range(max_iter):
        current = out.sum(axis=1)
        if np.any(current <= 0.0):
            raise RuntimeError("cannot strength-scale graph with isolated node")
        factor = np.sqrt(target_strength / current)
        out = factor[:, None] * out * factor[None, :]
        rel = float(np.max(np.abs(out.sum(axis=1) - target_strength) / np.maximum(target_strength, 1e-15)))
        if rel < tol:
            return out, rel
    rel = float(np.max(np.abs(out.sum(axis=1) - target_strength) / np.maximum(target_strength, 1e-15)))
    return out, rel


def make_degree_strength_rewire(
    positions: np.ndarray,
    geometric_base: np.ndarray,
    cfg: OverlapConfig,
    *,
    seed: int,
    swaps_per_edge: int = 5,
) -> RewireReceipt:
    """Destroy Euclidean adjacency while matching exact degree and initial node strength."""
    original_edges = _edge_list(geometric_base)
    original_degree = np.sum(geometric_base > 0.0, axis=1)
    original_strength = geometric_base.sum(axis=1)
    weights = np.asarray([geometric_base[i, j] for i, j in original_edges], dtype=np.float64)

    chosen_edges: list[tuple[int, int]] | None = None
    accepted = 0
    for attempt in range(8):
        candidate, accepted = _degree_preserving_swaps(
            original_edges,
            cfg.n_elements,
            seed=seed + 1009 * attempt,
            requested_swaps=swaps_per_edge * len(original_edges),
        )
        if _is_connected(cfg.n_elements, candidate):
            chosen_edges = candidate
            break
    if chosen_edges is None:
        raise RuntimeError("could not produce connected degree-preserving rewire")

    rng = np.random.default_rng(seed + 700001)
    shuffled_weights = weights.copy()
    rng.shuffle(shuffled_weights)
    rewired = np.zeros_like(geometric_base)
    for (i, j), w in zip(chosen_edges, shuffled_weights):
        rewired[i, j] = w
        rewired[j, i] = w

    rewired, strength_rel_error = _strength_scale(rewired, original_strength)
    rewired_degree = np.sum(rewired > 0.0, axis=1)

    edge_lengths = np.asarray([
        np.linalg.norm(positions[i] - positions[j]) for i, j in chosen_edges
    ])
    long_edge_fraction = float(np.mean(edge_lengths > cfg.overlap_cutoff))

    return RewireReceipt(
        base=rewired,
        degree_exact=bool(np.array_equal(original_degree, rewired_degree)),
        strength_rel_error=strength_rel_error,
        long_edge_fraction=long_edge_fraction,
        connected=_is_connected(cfg.n_elements, chosen_edges),
        accepted_swaps=accepted,
    )


def material_from_base(
    positions: np.ndarray,
    base: np.ndarray,
    cfg: OverlapConfig,
) -> OverlapMaterial:
    return OverlapMaterial(
        positions=positions.copy(),
        base=base.copy(),
        mass=np.ones(cfg.n_elements, dtype=np.float64),
        cfg=cfg,
    )


def train_on_base(
    positions: np.ndarray,
    base: np.ndarray,
    program: tuple[tuple[int, ...], ...],
    cfg: OverlapConfig,
) -> OverlapMaterial:
    material = material_from_base(positions, base, cfg)
    for _ in range(cfg.cycles):
        for episode in program:
            eligibility = teacher_episode(material, episode)
            redistribute_mass(material, eligibility)
    return material


def pair_metrics(
    hab: OverlapMaterial,
    hcd: OverlapMaterial,
) -> dict[str, float]:
    overlap_ab = route_overlap(hcd, A, B) - route_overlap(hab, A, B)
    overlap_cd = route_overlap(hab, C, D) - route_overlap(hcd, C, D)
    interaction_ab = pair_interaction(hcd, A, B, mode="distributed") - pair_interaction(hab, A, B, mode="distributed")
    interaction_cd = pair_interaction(hab, C, D, mode="distributed") - pair_interaction(hcd, C, D, mode="distributed")
    return {
        "overlap_AB": float(overlap_ab),
        "overlap_CD": float(overlap_cd),
        "interaction_AB": float(interaction_ab),
        "interaction_CD": float(interaction_cd),
    }


def run_seed(seed: int, cfg: OverlapConfig | None = None) -> dict:
    cfg = cfg or OverlapConfig()
    positions = make_positions(seed, cfg)
    geometric_base = make_base(positions, cfg)

    geo_ab = train_on_base(positions, geometric_base, PROGRAM_AB, cfg)
    geo_cd = train_on_base(positions, geometric_base, PROGRAM_CD, cfg)
    geo = pair_metrics(geo_ab, geo_cd)

    # Same graph, deliberately meaningless coordinates. This should be exactly equivalent.
    erased_positions = np.zeros_like(positions)
    same_ab = train_on_base(erased_positions, geometric_base, PROGRAM_AB, cfg)
    same_cd = train_on_base(erased_positions, geometric_base, PROGRAM_CD, cfg)
    same = pair_metrics(same_ab, same_cd)
    graph_same_max_diff = max(
        float(np.max(np.abs(geo_ab.mass - same_ab.mass))),
        float(np.max(np.abs(geo_cd.mass - same_cd.mass))),
        *(abs(geo[k] - same[k]) for k in geo),
    )

    rw = make_degree_strength_rewire(
        positions,
        geometric_base,
        cfg,
        seed=seed + 500000,
    )
    rw_ab = train_on_base(positions, rw.base, PROGRAM_AB, cfg)
    rw_cd = train_on_base(positions, rw.base, PROGRAM_CD, cfg)
    rewired = pair_metrics(rw_ab, rw_cd)

    return {
        "seed": int(seed),
        "geo": geo,
        "rewired": rewired,
        "graph_same_max_diff": graph_same_max_diff,
        "degree_exact": rw.degree_exact,
        "strength_rel_error": rw.strength_rel_error,
        "long_edge_fraction": rw.long_edge_fraction,
        "rewire_connected": rw.connected,
        "accepted_swaps": rw.accepted_swaps,
        "edge_count": len(_edge_list(geometric_base)),
    }
