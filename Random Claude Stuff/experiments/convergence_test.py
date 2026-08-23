"""Is the small order-effect real sequence memory, or just incomplete
convergence (recency from the last partial update)?  If it is convergence,
it must decay as the fixed-point iteration is run longer."""
import numpy as np, dataclasses
from sunday import nonlinear_overlap as no

def train(seed, program, cfg):
    mat = no.initialize(seed, cfg)
    for _ in range(cfg.cycles):
        for ep in program:
            no.redistribute_mass(mat, no.teacher_episode(mat, ep))
    return mat

fwd = ((no.A, no.B), (no.C,), (no.D,))
rev = ((no.D,), (no.C,), (no.A, no.B))
print(" cycles   max|dmass| fwd-vs-rev   d pair_interaction   |dPI| / PI")
for cycles in (20, 40, 80, 160, 320):
    cfg = dataclasses.replace(no.OverlapConfig(), cycles=cycles)
    mask = np.ones(cfg.n_elements, bool); mask[list(no.PORTS)] = False
    a, b = train(240000, fwd, cfg), train(240000, rev, cfg)
    pa = no.pair_interaction(a, no.A, no.B); pb = no.pair_interaction(b, no.A, no.B)
    d = np.max(np.abs(a.mass[mask]-b.mass[mask]))
    print(f" {cycles:5d}   {d:.6f}                {pa-pb:+.7f}          "
          f"{abs(pa-pb)/abs(pa)*100:5.2f}%")
