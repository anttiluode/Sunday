"""Is the order residual sequence memory, or just WHERE IN THE CYCLE you stop?

The training loop applies three maps per cycle. The converged material is a
periodic orbit, not a point. Reading it after episode 3 rather than after
episode 1 gives a different mass field even with zero memory of order.
Measure the intra-cycle wobble and compare it to the 'order effect'.
"""
import numpy as np, dataclasses
from sunday import nonlinear_overlap as no

cfg = dataclasses.replace(no.OverlapConfig(), cycles=200)
mask = np.ones(cfg.n_elements, bool); mask[list(no.PORTS)] = False
fwd = ((no.A, no.B), (no.C,), (no.D,))

mat = no.initialize(240000, cfg)
for _ in range(cfg.cycles):
    for ep in fwd:
        no.redistribute_mass(mat, no.teacher_episode(mat, ep))

# one more cycle, snapshotting after each episode
snaps, pis = [], []
for ep in fwd:
    no.redistribute_mass(mat, no.teacher_episode(mat, ep))
    snaps.append(mat.mass[mask].copy())
    pis.append(no.pair_interaction(mat, no.A, no.B))

ref = snaps[-1]                      # the published reading point
print("intra-cycle wobble at the converged orbit (zero memory required):")
for i, (s, p) in enumerate(zip(snaps, pis)):
    print(f"  after episode {i+1}: max|dmass vs published point| {np.max(np.abs(s-ref)):.6f}"
          f"   pair_interaction {p:+.7f}")
print(f"\n  orbit diameter (mass)            {np.max(np.abs(snaps[0]-snaps[1])):.6f}")
print(f"  orbit diameter (pair_interaction) {max(pis)-min(pis):+.7f}")
print(f"\n  'order effect' measured earlier   0.200110   /  -0.0004494")
