"""
Encoding an image into the medium, and reading the medium back out.

Encoding: the image is reduced to a P x P grid of port amplitudes.  Each
port stamps a small Gaussian source into the field.  ALL PORTS SHARE ONE
CARRIER FREQUENCY AND PHASE.  That is deliberate.  If every port had its
own frequency the medium would be a filter bank and the answer would be
"of course the ports are separable".  With one carrier, the only thing
that distinguishes two images with the same total brightness is the
SPATIAL ARRANGEMENT of the drive and how the geometry of mu transports
it.  That is the claim under test.

Readout: Q probes sample phi over the presentation window.  Features are
per-probe RMS in T consecutive time bins, so the feature vector carries
both where energy arrived and roughly when.
"""

import numpy as np


class Ports:
    def __init__(self, n, grid=8, margin_frac=0.22, sigma=1.4):
        self.n = n
        self.grid = grid
        self.sigma = sigma
        lo = int(n * margin_frac)
        hi = n - lo - 1
        pos = np.linspace(lo, hi, grid)
        yy, xx = np.meshgrid(pos, pos, indexing="ij")
        self.xy = np.stack([yy.ravel(), xx.ravel()], axis=1)     # (P^2, 2)
        self.stamps = _stamps(n, self.xy, sigma)                 # (P^2, n, n)
        # flatten for a fast weighted sum
        self._flat = self.stamps.reshape(len(self.xy), -1)

    def drive_pattern(self, amps):
        """Sum of port stamps weighted by amplitudes -> one (n,n) array."""
        a = np.asarray(amps, dtype=np.float64).ravel()
        return (a @ self._flat).reshape(self.n, self.n)


class Probes:
    def __init__(self, n, grid=8, margin_frac=0.12, seed=0, jitter=1.0):
        lo = int(n * margin_frac)
        hi = n - lo - 1
        pos = np.linspace(lo, hi, grid)
        yy, xx = np.meshgrid(pos, pos, indexing="ij")
        xy = np.stack([yy.ravel(), xx.ravel()], axis=1)
        if jitter:
            rng = np.random.default_rng(seed)
            xy = xy + rng.uniform(-jitter, jitter, xy.shape)
        xy = np.clip(np.round(xy).astype(int), 0, n - 1)
        self.xy = xy
        self.idx = (xy[:, 0], xy[:, 1])
        self.n_probes = len(xy)


def envelope(steps, frac=0.35):
    """Hann pulse over the first `frac` of the window, silence after."""
    m = max(2, int(steps * frac))
    e = np.zeros(steps)
    e[:m] = 0.5 * (1.0 - np.cos(2 * np.pi * np.arange(m) / (m - 1)))
    return e


def present(medium, ports, probes, amps, steps=300, omega=0.78,
            drive_gain=1.0, record_field_every=0,
            carve_every=0, carve_eta=0.0, carve_tau=40.0, carve_smooth=1.2):
    """
    Run one presentation.  Returns (features, trace, frames).

    The fast field is reset first, so nothing from the previous image can
    reach this one.  Only mu carries over.
    """
    medium.reset_fast()
    S = ports.drive_pattern(amps) * drive_gain
    env = envelope(steps)
    trace = np.empty((steps, probes.n_probes), dtype=np.float64)
    frames = []

    carving = carve_every > 0 and carve_eta > 0
    if carving:
        from .medium import _gauss
        medium.push_mu()
        acc = np.zeros_like(medium.phi)
        decay = np.exp(-carve_every / max(1e-9, carve_tau))

    for t in range(steps):
        d = S * (env[t] * np.sin(omega * t * medium.dt)) if env[t] > 0 else None
        medium.step(d)
        trace[t] = medium.phi[probes.idx]
        if carving:
            acc += medium.phi * medium.phi
            if (t + 1) % carve_every == 0:
                medium.carve(_gauss(acc, carve_smooth), carve_eta)
                acc *= decay
        if record_field_every and (t % record_field_every == 0):
            frames.append(medium.phi.copy())

    if carving:
        carved = medium.mu.copy()
        medium.pop_mu()
        return trace, frames, carved
    return trace, frames, None


def features_from_trace(trace, bins=4, eps=1e-12):
    """Per-probe RMS in `bins` equal time bins -> flat feature vector."""
    steps, q = trace.shape
    edges = np.linspace(0, steps, bins + 1).astype(int)
    out = np.empty((bins, q), dtype=np.float64)
    for b in range(bins):
        seg = trace[edges[b]:edges[b + 1]]
        out[b] = np.sqrt((seg * seg).mean(axis=0) + eps)
    f = out.ravel()
    # log compression: dynamic range across probes is large and we do not
    # want the readout to be a brightness detector
    return np.log1p(f / (f.mean() + eps))


def _stamps(n, xy, sigma):
    ax = np.arange(n)
    out = np.empty((len(xy), n, n), dtype=np.float64)
    for i, (cy, cx) in enumerate(xy):
        gy = np.exp(-0.5 * ((ax - cy) / sigma) ** 2)
        gx = np.exp(-0.5 * ((ax - cx) / sigma) ** 2)
        g = np.outer(gy, gx)
        out[i] = g / (g.sum() + 1e-12)
    return out
