"""
Sunday's Gate 1 / Gate 7 asked of a CONTINUOUS medium.

Sunday's result lives in a splat graph.  This is the same question put to a
continuum wave field -- a completely different discretisation.  Replication
here is evidence of mechanism; failure means the graph was doing it.

DESIGN (Sol's, and the six-terminal ring is not decorative -- with four
terminals the pair matrix has 6 entries and 4 endpoint parameters, so an
endpoint model can fit almost anything and the null is untestable).

    six terminals on a ring, two perfect matchings

        history 1:  (1,2) (3,4) (5,6)   driven as coactive pairs
        history 2:  (2,3) (4,5) (6,1)

Every terminal fires exactly once per cycle in BOTH histories.  Identical
marginals, identical total drive, identical episode count.  Only WHO
OCCURRED WITH WHOM differs, so any surviving difference is relational by
construction.

READOUT.  Freeze mu, drive terminal i alone, get its energy map E_i.
    O(i,j) = <E_i, E_j> / (||E_i|| ||E_j||)
    dO(i,j) = O(i,j | history 1) - O(i,j | history 2)

THE ENDPOINT NULL, and why the ring kills it.  For any additive model
dO(i,j) = a_i + a_j, the alternating cycle sum

    d12 - d23 + d34 - d45 + d56 - d61

is identically ZERO: every terminal scalar appears once with each sign.
A non-zero cycle contrast therefore cannot come from one scalar per
terminal.  That is the whole test.
"""

import numpy as np
from .medium import Medium
from .encode import _stamps, envelope

N_TERM = 6
M1 = [(0, 1), (2, 3), (4, 5)]
M2 = [(1, 2), (3, 4), (0, 5)]
CYCLE = [((0, 1), +1), ((1, 2), -1), ((2, 3), +1),
         ((3, 4), -1), ((4, 5), +1), ((0, 5), -1)]


class RingRig:
    def __init__(self, n=72, sigma=2.0, steps=240, omega=0.78, drive_gain=6.0,
                 radius=0.32, seed=0, heterogeneity=0.25, **medium_kw):
        self.n, self.steps, self.omega, self.gain = n, steps, omega, drive_gain
        self.seed, self.het, self.medium_kw = seed, heterogeneity, medium_kw
        ang = 2 * np.pi * np.arange(N_TERM) / N_TERM + 0.3
        xy = np.stack([n * (0.5 + radius * np.sin(ang)),
                       n * (0.5 + radius * np.cos(ang))], axis=1)
        self.stamps = _stamps(n, xy, sigma)
        self.env = envelope(steps)

    def fresh(self):
        return Medium(n=self.n, seed=self.seed, heterogeneity=self.het,
                      **self.medium_kw)

    def _drive(self, med, idxs, deposit):
        S = sum(self.stamps[i] for i in idxs) * self.gain
        med.reset_fast()
        for t in range(self.steps):
            e = self.env[t]
            med.step(S * (e * np.sin(self.omega * t * med.dt)) if e > 0 else None)
        if deposit:
            med.deposit()
        return med.local_energy()

    def train(self, matching, cycles=40):
        med = self.fresh()
        for _ in range(cycles):
            for pair in matching:
                self._drive(med, pair, deposit=True)
        return med

    def overlaps(self, med, mu):
        med.set_mu(mu)
        E = []
        for i in range(N_TERM):
            e = self._drive(med, (i,), deposit=False)
            E.append(e / (np.linalg.norm(e) + 1e-30))
        O = {}
        for i in range(N_TERM):
            for j in range(i + 1, N_TERM):
                O[(i, j)] = float((E[i] * E[j]).sum())
        return O


def _cycle_contrast(d):
    return sum(s * d[k] for k, s in CYCLE)


def _endpoint_r2(d, keys):
    M = np.zeros((len(keys), N_TERM))
    for r, (i, j) in enumerate(keys):
        M[r, i] = 1; M[r, j] = 1
    y = np.array([d[k] for k in keys])
    a, *_ = np.linalg.lstsq(M, y, rcond=None)
    res = y - M @ a
    return 1 - res.var() / max(1e-30, y.var())


def run(seeds=range(600000, 600006), cycles=40, log=print, **kw):
    rows, shufs = [], []
    keys = [(i, j) for i in range(N_TERM) for j in range(i + 1, N_TERM)]
    m1set = set(M1); m2set = set(M2)
    for s in seeds:
        rig = RingRig(seed=s, **kw)
        a = rig.train(M1, cycles); mu_a = a.mu.copy()
        b = rig.train(M2, cycles); mu_b = b.mu.copy()
        O1, O2 = rig.overlaps(a, mu_a), rig.overlaps(a, mu_b)
        d = {k: O1[k] - O2[k] for k in keys}
        rows.append(d)
        a.set_mu(mu_a); sa = a.shuffled_mu(seed=s)
        a.set_mu(mu_b); sb = a.shuffled_mu(seed=s)
        S1, S2 = rig.overlaps(a, sa), rig.overlaps(a, sb)
        shufs.append({k: S1[k] - S2[k] for k in keys})
        n_ok = sum(1 for k in m1set if d[k] > 0) + sum(1 for k in m2set if d[k] < 0)
        log(f"seed {s}  matching-1 edges {[f'{d[k]:+.4f}' for k in M1]}  "
            f"matching-2 {[f'{d[k]:+.4f}' for k in M2]}  signs {n_ok}/6  "
            f"cycle {_cycle_contrast(d):+.5f}  R2_endpoint {_endpoint_r2(d,keys):.3f}")

    tot = len(rows) * 6
    ok = sum(sum(1 for k in m1set if r[k] > 0) + sum(1 for k in m2set if r[k] < 0)
             for r in rows)
    cyc = np.array([_cycle_contrast(r) for r in rows])
    scy = np.array([_cycle_contrast(r) for r in shufs])
    r2 = np.array([_endpoint_r2(r, keys) for r in rows])
    tr = np.array([abs(r[k]) for r in rows for k in list(m1set) + list(m2set)])
    sh = np.array([abs(r[k]) for r in shufs for k in list(m1set) + list(m2set)])
    log("")
    log(f"trained-edge signs correct   {ok}/{tot}")
    log(f"|cycle contrast|             {np.abs(cyc).mean():.5f}  "
        f"min {np.abs(cyc).min():.5f}   (0 for ANY endpoint-additive model)")
    log(f"  same masses, shuffled      {np.abs(scy).mean():.5f}  -> "
        f"{100*np.abs(scy).mean()/max(1e-12,np.abs(cyc).mean()):.1f}% survives")
    log(f"trained-edge |dO|            {tr.mean():.5f}   shuffled {sh.mean():.5f} "
        f"({100*sh.mean()/max(1e-12,tr.mean()):.1f}%)")
    log(f"endpoint-additive R^2        {100*r2.mean():.1f}%  "
        f"(a_i + a_j fitted to all 15 entries)")
    return rows, shufs
