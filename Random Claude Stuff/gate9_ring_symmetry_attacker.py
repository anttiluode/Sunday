"""
Is Gate 9's operator a property of the MATERIAL, or of the TERMINAL RING?

Gate 9 finds that relation-program space maps into structural relation
response through an approximately linear operator whose top three singular
modes carry ~97-99% of the energy, and whose input subspace is stable across
independently randomised substrates (principal cosines .989 / .972 / .934).

There is a cheaper explanation that has to be ruled out first.

The six terminals sit on a circle. A hexagon has exactly THREE chord classes:
adjacent (d=1), skip-one (d=2), opposite (d=3). Sunday's controlled contrasts
are required to have matched circular pair-distance multisets, so the design
lives inside a distance-balanced subspace of the 15-dimensional pair space.
If the operator is even approximately equivariant under the cyclic group C6
acting on the terminal ring, it is block-diagonal in the Z6 Fourier basis and
its structure is fixed by the ring, not by the 256 randomly placed bulk
elements.

Three chord classes.  Three dominant modes.  That coincidence needs a test.

WHAT THIS SCRIPT DOES
  1. enumerates the controlled contrasts exactly as Gate 9 specifies
  2. trains both arms of each and builds Q (programs) and Y (responses)
  3. fits W by least squares, checks leave-one-out prediction
  4. SVD of W, then asks how much of each top mode lies inside
       (a) the three chord-class subspaces
       (b) the Z6 Fourier / C6-isotypic decomposition
  5. compares the operator across independently randomised substrates in the
     RING basis rather than in the raw pair basis

INTERPRETATION
  If the top three modes are essentially the three chord classes, then the
  cross-substrate stability Gate 9 reports is a statement about the terminal
  ring and is guaranteed by symmetry, not evidence that the material
  implements a learned transformation.  The correct attacker then becomes a
  substrate with terminals placed ASYMMETRICALLY, where C6 buys nothing and
  the three-mode structure must be earned.
"""

import itertools
import numpy as np

from sunday.composition import (CompositionConfig, TERMINALS, ALL_PAIRS,
                                train_program, pair_interaction)

PAIR_INDEX = {p: i for i, p in enumerate(ALL_PAIRS)}


def circ(pair):
    d = abs(pair[0] - pair[1])
    return min(d, 6 - d)


def matchings():
    """All 15 perfect matchings of the six terminals."""
    out = []
    t = list(TERMINALS)
    for a in itertools.combinations(t[1:], 1):
        pass
    def rec(rest):
        if not rest:
            yield ()
            return
        first, others = rest[0], rest[1:]
        for k in range(len(others)):
            pair = tuple(sorted((first, others[k])))
            for tail in rec(others[:k] + others[k + 1:]):
                yield (pair,) + tail
    for m in rec(tuple(t)):
        out.append(tuple(sorted(m)))
    return out


def contrasts():
    """Gate 9's strict control: disjoint edges, matched marginals (automatic
    for perfect matchings), matched circular distance multiset, +/- deduped."""
    ms = matchings()
    seen, out = set(), []
    for a, b in itertools.combinations(ms, 2):
        if set(a) & set(b):
            continue
        if sorted(circ(p) for p in a) != sorted(circ(p) for p in b):
            continue
        key = frozenset((a, b))
        if key in seen:
            continue
        seen.add(key)
        out.append((a, b))
    return out


def qvec(a, b):
    q = np.zeros(len(ALL_PAIRS))
    for p in a:
        q[PAIR_INDEX[p]] += 1.0
    for p in b:
        q[PAIR_INDEX[p]] -= 1.0
    return q


def response(seed, matching, cfg):
    mat = train_program(seed, matching, cfg)
    return np.array([pair_interaction(mat, i, j) for i, j in ALL_PAIRS])


# ------------------------------------------------------- symmetry bases

def chord_basis():
    """Indicator of each chord class, orthonormalised. Three columns."""
    B = np.zeros((len(ALL_PAIRS), 3))
    for i, p in enumerate(ALL_PAIRS):
        B[i, circ(p) - 1] = 1.0
    return B / np.linalg.norm(B, axis=0, keepdims=True)


def c6_isotypic():
    """Project pair space onto C6 isotypic components.

    C6 acts on terminals by rotation; that induces a permutation action on the
    15 pairs. Decompose into the irreducible components and return one
    orthonormal basis per component.
    """
    perm = np.zeros((len(ALL_PAIRS), len(ALL_PAIRS)))
    for i, (a, b) in enumerate(ALL_PAIRS):
        r = tuple(sorted(((a % 6) + 1, (b % 6) + 1)))
        r = tuple(sorted((x if x <= 6 else 1 for x in r)))
        perm[PAIR_INDEX[r], i] = 1.0
    # symmetrised projectors onto e^{2 pi i k / 6} eigenspaces
    comps = {}
    for k in range(6):
        w = np.exp(-2j * np.pi * k / 6)
        P = sum((w ** m) * np.linalg.matrix_power(perm, m) for m in range(6)) / 6
        U, s, _ = np.linalg.svd(np.hstack([P.real, P.imag]))
        r = int((s > 1e-8).sum())
        if r:
            comps[k] = U[:, :r]
    return comps


def frac_in(v, B):
    """Fraction of v's energy inside span(B)."""
    Q, _ = np.linalg.qr(B)
    return float(np.linalg.norm(Q.T @ v) ** 2 / (np.linalg.norm(v) ** 2 + 1e-30))


# -------------------------------------------------------------- the run

def run(seeds=(430000, 430001), cfg=None, log=print):
    cfg = cfg or CompositionConfig()
    cs = contrasts()
    log(f"controlled contrasts enumerated: {len(cs)}")
    Q = np.array([qvec(a, b) for a, b in cs])
    log(f"rank of Q: {np.linalg.matrix_rank(Q)}  (Gate 9 reports 7)")

    CH = chord_basis()
    ISO = c6_isotypic()
    log(f"chord classes: 3   C6 isotypic components: "
        f"{ {k: v.shape[1] for k, v in ISO.items()} }")

    Ws = []
    for seed in seeds:
        cache = {}
        Y = []
        for a, b in cs:
            for m in (a, b):
                if m not in cache:
                    cache[m] = response(seed, m, cfg)
            Y.append(cache[a] - cache[b])
        Y = np.array(Y)

        W, *_ = np.linalg.lstsq(Q, Y, rcond=None)
        # leave-one-out
        errs = []
        for i in range(len(cs)):
            idx = [j for j in range(len(cs)) if j != i]
            Wi, *_ = np.linalg.lstsq(Q[idx], Y[idx], rcond=None)
            pred = Q[i] @ Wi
            errs.append(np.linalg.norm(pred - Y[i]) ** 2 / (np.linalg.norm(Y[i]) ** 2 + 1e-30))
        U, s, Vt = np.linalg.svd(W)
        e = s ** 2 / (s ** 2).sum()
        log(f"\nseed {seed}   LOO NMSE {np.mean(errs):.6f}   "
            f"top-3 energy {e[:3].sum()*100:.2f}%   "
            f"spectrum {np.round(e[:5], 4)}")
        for r in range(3):
            uin, uout = U[:, r], Vt[r]
            log(f"  mode {r}: input  in chord-classes {100*frac_in(uin, CH):5.1f}%"
                f"   output in chord-classes {100*frac_in(uout, CH):5.1f}%")
            best = max(ISO, key=lambda k: frac_in(uin, ISO[k]))
            log(f"          input best C6 component k={best} "
                f"({100*frac_in(uin, ISO[best]):.1f}% of its energy)")
        Ws.append((U, s, Vt))

    if len(Ws) == 2:
        A = Ws[0][0][:, :3]; B = Ws[1][0][:, :3]
        cos = np.linalg.svd(np.linalg.qr(A)[0].T @ np.linalg.qr(B)[0])[1]
        log(f"\ncross-substrate top-3 input principal cosines: {np.round(cos, 4)}"
            f"   (Gate 9 dev: .989 .972 .934)")
        cosA = np.linalg.svd(np.linalg.qr(A)[0].T @ np.linalg.qr(chord_basis())[0])[1]
        log(f"substrate-1 top-3 vs the CHORD-CLASS basis:     {np.round(cosA, 4)}")
        cosB = np.linalg.svd(np.linalg.qr(B)[0].T @ np.linalg.qr(chord_basis())[0])[1]
        log(f"substrate-2 top-3 vs the CHORD-CLASS basis:     {np.round(cosB, 4)}")
        log("\nIf the last two lines are close to the first, the shared subspace "
            "is the ring's, not the material's.")


if __name__ == "__main__":
    import time
    t0 = time.time()
    run()
    print(f"\nelapsed {time.time()-t0:.0f}s")
