"""Decisive: break the terminal ring's C6 symmetry.

Gate 9's cross-substrate stability compares substrates whose 256 bulk
elements are independently randomised -- but whose SIX TERMINALS sit at
identical positions, 2*pi*q/6 on a circle, in every single substrate.
If the shared top-3 subspace is a property of that ring, then substrates
with DIFFERENT terminal geometry should not share it.
"""
import numpy as np, sys
sys.path.insert(0,'.')
from experiments.gate9_ring_symmetry_attacker import contrasts, qvec
from sunday.composition import (CompositionConfig, ALL_PAIRS, PORTS, SOMA, TERMINALS,
                                make_base, initialize, teacher_episode,
                                redistribute_mass, pair_interaction)

cfg = CompositionConfig()

def build(seed, jitter):
    """Same substrate construction, but terminal angles are jittered."""
    mat = initialize(seed, cfg)
    if jitter > 0:
        rng = np.random.default_rng(seed * 7 + 13)
        ang = 2*np.pi*np.arange(6)/6 + rng.uniform(-jitter, jitter, 6)
        rad = cfg.terminal_radius * (1 + rng.uniform(-jitter, jitter, 6))
        for q, t in enumerate(TERMINALS):
            mat.positions[t] = np.array([-0.95, rad[q]*np.cos(ang[q]), rad[q]*np.sin(ang[q])])
        mat.base = make_base(mat.positions, cfg)
    return mat

def train(seed, matching, jitter):
    mat = build(seed, jitter)
    for _ in range(cfg.cycles):
        for ep in matching:
            redistribute_mass(mat, teacher_episode(mat, ep))
    return np.array([pair_interaction(mat, i, j) for i, j in ALL_PAIRS])

cs = contrasts(); Q = np.array([qvec(a,b) for a,b in cs])

def operator(seed, jitter):
    cache, Y = {}, []
    for a, b in cs:
        for m in (a, b):
            if m not in cache: cache[m] = train(seed, m, jitter)
        Y.append(cache[a] - cache[b])
    W, *_ = np.linalg.lstsq(Q, np.array(Y), rcond=None)
    U, s, _ = np.linalg.svd(W)
    e = s**2/(s**2).sum()
    return U[:, :3], e

for jitter, label in ((0.0, "SYMMETRIC ring (published)"), (0.35, "JITTERED ring (C6 broken)")):
    A, eA = operator(430000, jitter)
    B, eB = operator(430001, jitter)
    cos = np.linalg.svd(np.linalg.qr(A)[0].T @ np.linalg.qr(B)[0])[1]
    print(f"{label:28s} top-3 energy {eA[:3].sum()*100:5.2f}% / {eB[:3].sum()*100:5.2f}%"
          f"   cross-substrate cosines {np.round(cos,4)}")
