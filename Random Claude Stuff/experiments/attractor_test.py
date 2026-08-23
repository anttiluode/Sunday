"""
Multi-attractor test for Sunday.

Every Sunday substrate starts from mass = ones. The published gates all run
one fixed history from that one point, so nothing in the repo distinguishes

    "the history wrote this structure"      (path dependence)

from

    "this rule lands here no matter what"   (a unique attractor, and the
                                             structure is a function of the
                                             drive statistics alone)

Both look identical if you only ever start from ones.

This runs each substrate's own training program unchanged, from several
random initial mass fields that satisfy the same constraints the rule does
(exact budget, mass floor, ports pinned at 1.0), and asks whether the finals
agree -- both in the mass field and in the downstream observable the gates
actually score.

Nothing in sunday/ is modified. This only calls its public functions.
"""

import numpy as np

from sunday import microarbor as ma
from sunday import nonlinear_overlap as no
from sunday import composition as co


def perturb(mass, ports, floor, budget, rng, spread=1.0):
    """Random initial mass satisfying budget, floor, and pinned ports."""
    m = mass.copy()
    mask = np.ones(len(m), dtype=bool)
    mask[list(ports)] = False
    n_free = int(mask.sum())
    free_budget = budget - float(len(ports))          # ports sit at 1.0
    allocatable = free_budget - floor * n_free
    w = rng.random(n_free) ** (1.0 + 3.0 * spread)    # heavy-tailed, very unlike ones
    w = w / w.sum()
    m[mask] = floor + allocatable * w
    m[list(ports)] = 1.0
    m[mask] += (budget - m.sum()) / n_free
    return m


def _pairwise_corr(fields):
    out = []
    for i in range(len(fields)):
        for j in range(i + 1, len(fields)):
            out.append(np.corrcoef(fields[i], fields[j])[0, 1])
    return np.array(out)


def _spread(v):
    v = np.asarray(v, dtype=float)
    return f"{v.mean():+.6f}  (min {v.min():+.6f}, max {v.max():+.6f}, sd {v.std(ddof=1):.6f})"


# ------------------------------------------------------------------ arbor

def test_microarbor(n_init=5, seed0=770000, log=print):
    log("\n### microarbor  (Gate 0/1 base substrate, train_history(A))")
    cfg = ma.MicroarborConfig()
    finals, obs = [], []
    for k in range(n_init):
        rng = np.random.default_rng(seed0 + k)
        mat = ma.initialize(cfg)
        mask = np.ones(cfg.n_elements, dtype=bool)
        mask[list(ma.PROTECTED)] = False
        mat.mass = perturb(mat.mass, ma.PROTECTED, cfg.mass_floor,
                           cfg.mass_budget, rng) if k else mat.mass
        start = mat.mass.copy()
        for _ in range(cfg.train_epochs):
            mat.redistribute = None
            el = ma.teacher_episode(mat, ma.TERMINAL_A)
            ma.redistribute_mass(mat, el)
        finals.append(mat.mass[mask].copy())
        ra = ma.impulse_response(mat, ma.TERMINAL_A)
        rb = ma.impulse_response(mat, ma.TERMINAL_B)
        obs.append(ra.auc - rb.auc)
        log(f"  init {k}: start sd {start[mask].std():.4f} -> "
            f"final sd {finals[-1].std():.4f}   A-B auc {obs[-1]:+.6f}")
    c = _pairwise_corr(finals)
    log(f"  corr(final mass) over {len(c)} pairs: mean {c.mean():.6f}  "
        f"min {c.min():.6f}")
    log(f"  observable (auc_A - auc_B): {_spread(obs)}")
    return c, obs


# --------------------------------------------------------------- overlap

def test_overlap(n_init=5, seeds=(240000, 240001, 240002), log=print):
    log("\n### nonlinear_overlap  (Gate 1: PROGRAM_AB, route overlap + pair interaction)")
    cfg = no.OverlapConfig()
    allc, allo = [], []
    for s in seeds:
        finals, ov, pi = [], [], []
        mask = np.ones(cfg.n_elements, dtype=bool)
        mask[list(no.PORTS)] = False
        for k in range(n_init):
            rng = np.random.default_rng(880000 + 97 * s + k)
            mat = no.initialize(s, cfg)
            if k:
                mat.mass = perturb(mat.mass, no.PORTS, cfg.mass_floor,
                                   cfg.mass_budget, rng)
            for _ in range(cfg.cycles):
                for episode in no.PROGRAM_AB:
                    ma_el = no.teacher_episode(mat, episode)
                    no.redistribute_mass(mat, ma_el)
            finals.append(mat.mass[mask].copy())
            ov.append(no.route_overlap(mat, no.A, no.B))
            pi.append(no.pair_interaction(mat, no.A, no.B))
        c = _pairwise_corr(finals)
        allc.append(c); allo.append(pi)
        log(f"  seed {s}: corr(final mass) mean {c.mean():.6f} min {c.min():.6f}")
        log(f"           route_overlap(A,B) {_spread(ov)}")
        log(f"           pair_interaction(A,B) {_spread(pi)}")
    return allc, allo


# ----------------------------------------------------------- composition

def test_composition(n_init=5, seeds=(400000, 400001, 400002), log=print):
    log("\n### composition  (Gate 6/7: MATCHING_1, the relation matrix substrate)")
    cfg = co.CompositionConfig()
    mask = np.ones(cfg.n_elements, dtype=bool)
    mask[list(co.PORTS)] = False
    out = []
    for s in seeds:
        finals, rel = [], []
        for k in range(n_init):
            rng = np.random.default_rng(990000 + 97 * s + k)
            mat = co.initialize(s, cfg)
            if k:
                mat.mass = perturb(mat.mass, co.PORTS, cfg.mass_floor,
                                   cfg.mass_budget, rng)
            for _ in range(cfg.cycles):
                for episode in co.MATCHING_1:
                    el = co.teacher_episode(mat, episode)
                    co.redistribute_mass(mat, el)
            finals.append(mat.mass[mask].copy())
            rel.append([co.pair_interaction(mat, i, j) for i, j in co.ALL_PAIRS])
        c = _pairwise_corr(finals)
        rel = np.array(rel)
        # how much does the 15-entry relation matrix move across initialisations?
        spread = rel.std(axis=0, ddof=1).mean()
        scale = np.abs(rel.mean(axis=0)).mean()
        out.append((c, spread, scale))
        log(f"  seed {s}: corr(final mass) mean {c.mean():.6f} min {c.min():.6f}")
        log(f"           relation matrix: mean |entry| {scale:.6f}, "
            f"sd across inits {spread:.6f}  ({100*spread/max(scale,1e-15):.2f}%)")
        signs = [tuple(np.sign(r[i]) for i in range(len(co.ALL_PAIRS))) for r in rel]
        log(f"           identical sign pattern across all inits: "
            f"{len(set(signs)) == 1}")
    return out


if __name__ == "__main__":
    import time
    t0 = time.time()
    print("MULTI-ATTRACTOR TEST -- same history, different starting mass")
    print("Sunday's own code, unmodified. Only initialize() is perturbed.")
    test_microarbor()
    test_overlap()
    test_composition()
    print(f"\nelapsed {time.time()-t0:.0f}s")
