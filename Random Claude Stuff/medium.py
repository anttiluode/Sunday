"""
The medium.

A 2-D scalar wave field phi(x,t) whose local wave speed is set by a slow
"mass" field mu(x).  mu is deposited where wave energy lingers, decays
everywhere, and is projected back onto a FIXED TOTAL BUDGET after every
update.  Nothing else is learned inside the medium.

Two design rules are load-bearing and are asserted in the gates:

  1. STABLE VACUUM.  phi = 0 is a minimum, not a maximum.  (The original
     anttis-instanton.py used V = -a/2 phi^2 + b/4 phi^4, which makes the
     empty background tachyonic: it decays into domains on its own with
     growth rate sqrt(a).  Everything that looked like "the particle
     jumping" was that decay plus a multimodal centre-of-mass readout.)

  2. FAST STATE IS NEVER THE MEMORY.  phi is reset to zero before every
     presentation.  All persistence lives in mu.  So the medium cannot
     accumulate junk across presentations, and presentation order cannot
     silently leak into a "result".

Discretisation: leapfrog in time, divergence-form Laplacian in space so
that a spatially varying speed does not manufacture energy at the
gradients of mu.  A sponge layer damps the boundary so the box does not
act as a resonator.
"""

import numpy as np


class Medium:
    def __init__(
        self,
        n=96,
        c0=1.0,
        dt=0.25,
        kappa=6.0,             # how strongly mass slows the medium
        mu_floor=0.01,         # nothing ever vanishes completely
        mu_init=0.08,          # dormant matter everywhere (no birth events)
        mu_max=1.0,
        eta=0.03,              # deposition rate
        lam=0.02,              # decay / forgetting rate
        base_damp=0.004,       # bulk damping
        sponge_width=8,
        sponge_damp=0.35,
        nonlin=0.0,            # optional cubic restoring term, phi^3
        power=1.0,             # deposition exponent; >1 = winner-take-all
        heterogeneity=0.0,     # per-seed roughness of the dormant matter
        seed=0,
    ):
        self.n = int(n)
        self.c0 = float(c0)
        self.dt = float(dt)
        self.kappa = float(kappa)
        self.mu_floor = float(mu_floor)
        self.mu_init = float(mu_init)
        self.mu_max = float(mu_max)
        if not (self.mu_floor < self.mu_init < self.mu_max):
            raise ValueError("need mu_floor < mu_init < mu_max for a "
                             "budget with headroom")
        self.eta = float(eta)
        self.lam = float(lam)
        self.base_damp = float(base_damp)
        self.nonlin = float(nonlin)
        self.power = float(power)
        self.rng = np.random.default_rng(seed)

        # CFL for the 2-D leapfrog: c*dt/dx <= 1/sqrt(2).  c only ever
        # DECREASES with mass, so checking c0 is sufficient.
        cfl = self.c0 * self.dt
        if cfl > 0.70:
            raise ValueError(f"CFL violated: c0*dt = {cfl:.3f} > 0.707")

        self.mu = np.full((n, n), self.mu_init, dtype=np.float64)
        if heterogeneity:
            # dormant matter is not perfectly uniform; this is what makes
            # different seeds different substrates rather than one substrate
            # run several times.
            self.mu *= 1.0 + heterogeneity * self.rng.standard_normal((n, n))
            np.clip(self.mu, self.mu_floor, self.mu_max, out=self.mu)
        self.mu_budget = float(self.mu.sum())
        self._floor_total = float(self.mu_floor * n * n)

        self.phi = np.zeros((n, n), dtype=np.float64)
        self.phi_prev = np.zeros((n, n), dtype=np.float64)

        self.damp = np.full((n, n), self.base_damp, dtype=np.float64)
        if sponge_width > 0:
            ramp = np.zeros(n)
            w = int(sponge_width)
            edge = np.linspace(1.0, 0.0, w) ** 2
            ramp[:w] = edge
            ramp[-w:] = edge[::-1]
            prof = np.maximum(ramp[:, None], ramp[None, :])
            self.damp = self.damp + sponge_damp * prof

        self._energy = np.zeros((n, n), dtype=np.float64)
        self._energy_steps = 0

    # ---------------------------------------------------------------- fast

    @property
    def c2(self):
        """Local squared wave speed.  More mass -> slower."""
        return (self.c0 ** 2) / (1.0 + self.kappa * self.mu)

    def reset_fast(self):
        self.phi[:] = 0.0
        self.phi_prev[:] = 0.0
        self._energy[:] = 0.0
        self._energy_steps = 0

    def _div_c2_grad(self, f):
        """div( c2(x) grad f ) with Neumann edges, staggered coefficients."""
        c2 = self.c2
        # x-fluxes on the i+1/2 faces
        cx = 0.5 * (c2[:, 1:] + c2[:, :-1])
        fx = cx * (f[:, 1:] - f[:, :-1])
        out = np.zeros_like(f)
        out[:, 1:] -= fx
        out[:, :-1] += fx
        # y-fluxes
        cy = 0.5 * (c2[1:, :] + c2[:-1, :])
        fy = cy * (f[1:, :] - f[:-1, :])
        out[1:, :] -= fy
        out[:-1, :] += fy
        return out

    def step(self, drive=None):
        """One leapfrog step.  `drive` is an additive source field."""
        lap = self._div_c2_grad(self.phi)
        rhs = lap
        if self.nonlin:
            rhs = rhs - self.nonlin * self.phi ** 3
        if drive is not None:
            rhs = rhs + drive

        g = self.damp * self.dt
        phi_new = (2.0 * self.phi - (1.0 - 0.5 * g) * self.phi_prev
                   + self.dt ** 2 * rhs) / (1.0 + 0.5 * g)

        self.phi_prev = self.phi
        self.phi = phi_new

        self._energy += phi_new * phi_new
        self._energy_steps += 1

    # ---------------------------------------------------------------- slow

    def local_energy(self):
        if self._energy_steps == 0:
            return np.zeros_like(self.mu)
        return self._energy / self._energy_steps

    def deposit(self, smooth=1.5, power=None):
        """
        Slow update.  Mass grows where energy lingered, decays everywhere,
        and is then projected back onto the fixed budget.

        The projection is what makes this a competition rather than a
        runaway: a region can only gain mass by taking it from elsewhere.
        """
        e = self.local_energy()
        if smooth > 0:
            e = _gauss(e, smooth)
        m = e.mean()
        if m <= 0 or not np.isfinite(m):
            return
        gain = e / m                                  # dimensionless, mean 1
        p = self.power if power is None else power
        if p != 1.0:
            gain = gain ** p
            gain = gain / (gain.mean() + 1e-30)

        mu = (1.0 - self.lam) * self.mu + self.eta * gain
        np.clip(mu, self.mu_floor, self.mu_max, out=mu)

        self.mu = self._project(mu)

    def _project(self, mu):
        """Project onto {sum(mu) == budget, mu_floor <= mu <= mu_max}.

        Only the mass ABOVE the floor is rescaled, so the floor is never
        violated and the constraint set stays non-empty.  Iterated because
        the upper clip and the rescale fight each other.
        """
        target = self.mu_budget - self._floor_total
        for _ in range(24):
            excess = mu - self.mu_floor
            s = excess.sum()
            if s <= 1e-12:
                mu = np.full_like(mu, self.mu_budget / mu.size)
                break
            mu = self.mu_floor + excess * (target / s)
            hit = mu > self.mu_max
            if not hit.any():
                break
            mu = np.minimum(mu, self.mu_max)
            free = ~hit
            if not free.any():
                break
            deficit = self.mu_budget - mu.sum()
            fe = (mu[free] - self.mu_floor).sum()
            if fe <= 1e-12:
                break
            mu[free] = self.mu_floor + (mu[free] - self.mu_floor) * (1 + deficit / fe)
            if abs(mu.sum() - self.mu_budget) / self.mu_budget < 1e-12:
                break
        return mu

    # -------------------------------------------------- within-trial carve

    def push_mu(self):
        self._mu_stack = getattr(self, "_mu_stack", [])
        self._mu_stack.append(self.mu.copy())

    def pop_mu(self):
        self.mu = self._mu_stack.pop()

    def carve(self, e, eta):
        """Fast, within-presentation deposition.

        This is the part that makes the wave experience the matter it is
        laying down.  Without it, deposition happens once at the end of a
        presentation and the travelling wave never feels its own trail --
        which makes the whole "signal carves its route" story untestable.
        Always used inside push_mu()/pop_mu(), so it never leaks between
        images.
        """
        m = e.mean()
        if m <= 0 or not np.isfinite(m):
            return
        mu = self.mu + eta * (e / m)
        np.clip(mu, self.mu_floor, self.mu_max, out=mu)
        self.mu = self._project(mu)

    # ------------------------------------------------------------ surgery

    def set_mu(self, mu):
        mu = np.asarray(mu, dtype=np.float64).reshape(self.n, self.n).copy()
        np.clip(mu, self.mu_floor, self.mu_max, out=mu)
        self.mu = mu

    def shuffled_mu(self, seed=0):
        """Same multiset of mass values, different spatial arrangement.

        Every scalar statistic of mu is preserved exactly: sum, mean,
        variance, histogram, min, max.  Only WHERE the mass is changes.
        """
        rng = np.random.default_rng(seed)
        flat = self.mu.ravel().copy()
        rng.shuffle(flat)
        return flat.reshape(self.n, self.n)

    def matched_random_mu(self, seed=0):
        """Random mass with the same histogram, drawn independently of
        anything the medium ever saw."""
        return self.shuffled_mu(seed=seed + 991)

    def stats(self):
        mu = self.mu
        return dict(
            mu_sum=float(mu.sum()),
            mu_mean=float(mu.mean()),
            mu_std=float(mu.std()),
            mu_min=float(mu.min()),
            mu_max=float(mu.max()),
            budget=float(self.mu_budget),
        )


def _gauss(a, sigma):
    """Small separable Gaussian blur (no scipy dependency in the hot path)."""
    r = max(1, int(3 * sigma))
    x = np.arange(-r, r + 1, dtype=np.float64)
    k = np.exp(-0.5 * (x / sigma) ** 2)
    k /= k.sum()
    pad = np.pad(a, ((0, 0), (r, r)), mode="edge")
    out = np.apply_along_axis(lambda m: np.convolve(m, k, mode="valid"), 1, pad)
    pad = np.pad(out, ((r, r), (0, 0)), mode="edge")
    out = np.apply_along_axis(lambda m: np.convolve(m, k, mode="valid"), 0, pad)
    return out
