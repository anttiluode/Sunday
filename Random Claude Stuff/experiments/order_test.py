"""Does episode ORDER inside a Sunday program change the material?

If the rule has a unique attractor per program, it cannot represent
sequence -- only the multiset of episodes. That is testable directly.
"""
import numpy as np
from sunday import nonlinear_overlap as no
from sunday import composition as co

def train(mod, seed, program, cfg):
    mat = mod.initialize(seed, cfg)
    for _ in range(cfg.cycles):
        for ep in program:
            mod.redistribute_mass(mat, mod.teacher_episode(mat, ep))
    return mat

cfg = no.OverlapConfig()
mask = np.ones(cfg.n_elements, bool); mask[list(no.PORTS)] = False
AB = no.PROGRAM_AB                      # ((A,B),(C,),(D,))
orders = {
    "AB,C,D  (published)": ((no.A, no.B), (no.C,), (no.D,)),
    "D,C,AB  (reversed)":  ((no.D,), (no.C,), (no.A, no.B)),
    "C,AB,D  (rotated)":   ((no.C,), (no.A, no.B), (no.D,)),
}
print("### nonlinear_overlap: same episodes, different order within each cycle")
for s in (240000, 240001):
    fields, pis = {}, {}
    for name, prog in orders.items():
        m = train(no, s, prog, cfg)
        fields[name] = m.mass[mask].copy()
        pis[name] = no.pair_interaction(m, no.A, no.B)
    ks = list(orders)
    ref = fields[ks[0]]
    print(f"  seed {s}")
    for k in ks:
        c = np.corrcoef(ref, fields[k])[0,1]
        d = np.max(np.abs(ref - fields[k]))
        print(f"    {k:22s} corr {c:.8f}  max|dmass| {d:.2e}  "
              f"pair_interaction {pis[k]:+.6f}")

print("\n### composition (Gate 6/7): MATCHING_1 in three orders")
ccfg = co.CompositionConfig()
cmask = np.ones(ccfg.n_elements, bool); cmask[list(co.PORTS)] = False
m1 = co.MATCHING_1
corders = {"published": m1, "reversed": tuple(reversed(m1)),
           "rotated": (m1[1], m1[2], m1[0])}
for s in (400000,):
    fields, rels = {}, {}
    for name, prog in corders.items():
        m = train(co, s, prog, ccfg)
        fields[name] = m.mass[cmask].copy()
        rels[name] = np.array([co.pair_interaction(m,i,j) for i,j in co.ALL_PAIRS])
    ref, refr = fields["published"], rels["published"]
    for k in corders:
        print(f"    {k:10s} corr {np.corrcoef(ref, fields[k])[0,1]:.8f}  "
              f"max|dmass| {np.max(np.abs(ref-fields[k])):.2e}  "
              f"max|d relation| {np.max(np.abs(refr-rels[k])):.2e}")
