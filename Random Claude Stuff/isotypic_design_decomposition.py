"""Pure linear algebra, no training: how much of Gate 9's structure is fixed
by the C6 symmetry of the terminal ring BEFORE any material is involved?"""
import numpy as np, sys
sys.path.insert(0,'.')
from experiments.gate9_ring_symmetry_attacker import contrasts, qvec, c6_isotypic, chord_basis
from sunday.composition import ALL_PAIRS

cs = contrasts(); Q = np.array([qvec(a,b) for a,b in cs])
U,s,Vt = np.linalg.svd(Q); r = int((s>1e-9).sum())
R = Vt[:r].T                                   # 15 x 7 design (row) space
ISO = c6_isotypic()
print(f"design space rank {r}")
print("\nisotypic k : dim(component) : dim(component ∩ design space)")
tot=0
for k,B in ISO.items():
    Qb,_ = np.linalg.qr(B); Qr,_ = np.linalg.qr(R)
    cos = np.linalg.svd(Qb.T@Qr)[1]
    d = int((cos > 1-1e-8).sum())
    tot += d
    print(f"   k={k}      {B.shape[1]:2d}              {d}      "
          f"principal cosines {np.round(cos[:4],3)}")
print(f"   total accounted: {tot} of {r}")
CH = chord_basis(); Qc,_=np.linalg.qr(CH); Qr,_=np.linalg.qr(R)
print(f"\nchord-class (k=0, invariant) overlap with design space: "
      f"{np.round(np.linalg.svd(Qc.T@Qr)[1],4)}")
print("  -> the matched-distance-multiset control REMOVES the invariant part by")
print("     construction, which is why my chord hypothesis read 0.0%.")
