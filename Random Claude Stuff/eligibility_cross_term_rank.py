"""Where does rank 3 come from?

Sunday's teacher eligibility uses an ABSOLUTE VALUE, so a joint episode is
not the sum of its singleton episodes. Define the cross term

    C_ij = eligibility(i,j) - eligibility(i) - eligibility(j)     in R^249

That 15 x 249 matrix is the only channel by which pair identity (as opposed
to terminal identity) can reach the mass field at all. Its spectrum should
bound the operator's rank.
"""
import numpy as np, sys
sys.path.insert(0,'.')
from sunday.composition import (CompositionConfig, ALL_PAIRS, TERMINALS, PORTS,
                                initialize, teacher_episode)

cfg = CompositionConfig()
for seed in (430000, 430001):
    mat = initialize(seed, cfg)
    single = {t: teacher_episode(mat, (t,)) for t in TERMINALS}
    C = np.array([teacher_episode(mat, (i, j)) - single[i] - single[j]
                  for i, j in ALL_PAIRS])
    E = np.array([teacher_episode(mat, (i, j)) for i, j in ALL_PAIRS])
    for name, M in (("raw joint eligibility", E), ("CROSS TERM (pair-only)", C)):
        s = np.linalg.svd(M, compute_uv=False); e = s**2/(s**2).sum()
        print(f"seed {seed}  {name:24s} rank-1 {e[0]*100:5.2f}%  "
              f"top-3 {e[:3].sum()*100:6.2f}%  top-5 {e[:5].sum()*100:6.2f}%  "
              f"spectrum {np.round(e[:5],4)}")
    print()
