"""
Training, evaluation, and the gates that are allowed to kill this.

Training is unsupervised and label-free: present images, let mass
sediment, project back to the budget.  Labels are only ever seen by the
ridge readout at the very end.

Feature extraction ALWAYS runs with deposition off, so the feature for
image i does not depend on how many images came before it.

The arm ladder, in order of how much it hurts if the numbers come out
flat:

  MEDIUM-LEARNED     mu shaped by the training images
  MEDIUM-DORMANT     mu uniform, never learned         -> did learning do anything?
  MEDIUM-SHUFFLED    learned mu, spatially permuted    -> is the geometry load-bearing?
  MEDIUM-RANDOM      matched-histogram random mu       -> is it just heterogeneity?
  PIXELS             ridge on the raw port amplitudes  -> is the medium needed at all?
  RANDOM-FEATURES    tanh(Wx+b) at the same feature
                     dimension as the medium           -> is any untrained expansion enough?

PRE-REGISTERED PREDICTIONS (written before the first run, so they cannot
be retrofitted):

  P1  MEDIUM-LEARNED > MEDIUM-DORMANT.  If false, deposition is decorative.
  P2  MEDIUM-LEARNED > MEDIUM-SHUFFLED.  If false, the 3-D/2-D geometry is
      decorative and this is an arbitrary heterogeneous filter.
  P3  RANDOM-FEATURES is expected to be COMPETITIVE and may win.  A random
      nonlinear expansion at matched dimension is a strong classifier on
      easy data.  If the medium merely ties it, the honest claim is
      "a self-organising physical reservoir", not "a better architecture".
  P4  PIXELS is expected to be strong on the synthetic set.  Beating it is
      not the goal; the goal is P1 and P2.
"""

import time
import numpy as np

from .medium import Medium
from .encode import Ports, Probes, present, features_from_trace
from .readout import RidgeReadout, Retriever, cv_alpha


DEFAULTS = dict(
    n=72,
    steps=260,
    omega=0.78,
    drive_gain=6.0,
    port_grid=8,
    probe_grid=8,
    bins=4,
    epochs=3,
    carve_every=0,       # >0 turns on within-presentation carving
    carve_eta=0.0,
    carve_tau=40.0,
    kappa=6.0,
    eta=0.04,
    lam=0.03,
    mu_floor=0.01,
    mu_init=0.08,
    mu_max=1.0,
    dt=0.25,
    seed=0,
)


class InstantonField:
    def __init__(self, **kw):
        self.cfg = dict(DEFAULTS)
        self.cfg.update(kw)
        c = self.cfg
        self.medium = Medium(
            n=c["n"], dt=c["dt"], kappa=c["kappa"], eta=c["eta"], lam=c["lam"],
            mu_floor=c["mu_floor"], mu_init=c["mu_init"],
            mu_max=c["mu_max"], seed=c["seed"],
        )
        self.ports = Ports(c["n"], grid=c["port_grid"])
        self.probes = Probes(c["n"], grid=c["probe_grid"], seed=c["seed"])
        self.mu_dormant = self.medium.mu.copy()
        self.mu_learned = None
        self.history = []

    # ------------------------------------------------------------ physics

    def _present(self, img, record_every=0):
        amps = np.asarray(img, dtype=np.float64).ravel()
        c = self.cfg
        return present(self.medium, self.ports, self.probes, amps,
                       steps=c["steps"], omega=c["omega"],
                       drive_gain=c["drive_gain"],
                       record_field_every=record_every,
                       carve_every=c["carve_every"], carve_eta=c["carve_eta"],
                       carve_tau=c["carve_tau"])

    def train(self, ds, epochs=None, progress=None, stop=None):
        """Unsupervised.  Labels are not touched here."""
        epochs = epochs or self.cfg["epochs"]
        self.medium.set_mu(self.mu_dormant)
        t0 = time.time()
        order_rng = np.random.default_rng(self.cfg["seed"])
        total = epochs * len(ds)
        done = 0
        for ep in range(epochs):
            order = order_rng.permutation(len(ds))
            for i in order:
                if stop is not None and stop():
                    return self
                tr, _, carved = self._present(ds.images[i])
                if carved is not None:
                    self.medium.set_mu(carved)   # keep what the wave carved
                self.medium.deposit()
                done += 1
                if progress and (done % 5 == 0 or done == total):
                    progress(done, total, self.medium.stats(),
                             self.medium.mu, time.time() - t0)
            self.history.append(dict(epoch=ep, **self.medium.stats()))
        self.mu_learned = self.medium.mu.copy()
        return self

    def extract(self, ds, mu=None, progress=None, stop=None):
        """Features with deposition OFF and the fast field reset per image."""
        if mu is not None:
            self.medium.set_mu(mu)
        X = []
        for i in range(len(ds)):
            if stop is not None and stop():
                return None
            trace, _, _ = self._present(ds.images[i])
            X.append(features_from_trace(trace, bins=self.cfg["bins"]))
            if progress and (i % 5 == 0 or i == len(ds) - 1):
                progress(i + 1, len(ds))
        return np.asarray(X)

    # ------------------------------------------------------------ scoring

    def score_arm(self, Xtr, ytr, Xte, yte, n_classes):
        a, cv = cv_alpha(Xtr, ytr, n_classes, seed=self.cfg["seed"])
        r = RidgeReadout(a).fit(Xtr, ytr, n_classes)
        ret = Retriever().fit(Xtr, ytr)
        return dict(
            alpha=a, cv=cv,
            train_acc=r.accuracy(Xtr, ytr),
            test_acc=r.accuracy(Xte, yte),
            p_at_1=ret.precision_at_1(Xte, yte),
            dim=Xtr.shape[1],
        )


# --------------------------------------------------------------- attackers

def pixel_features(ds):
    return ds.images.reshape(len(ds), -1)


def random_features(ds, dim, seed=0):
    """Untrained random nonlinear expansion at matched dimension."""
    X = ds.images.reshape(len(ds), -1)
    rng = np.random.default_rng(seed + 12345)
    W = rng.standard_normal((X.shape[1], dim)) / np.sqrt(X.shape[1])
    b = rng.uniform(-1, 1, dim)
    return np.tanh(X @ W + b)


# ------------------------------------------------------------------- gates

def run_gates(ds_train, ds_test, cfg=None, log=print, stop=None, on_mu=None):
    """
    The full ladder.  Returns a dict of arm -> metrics.

    `log` receives human-readable lines.  `on_mu(mu, tag)` is called when a
    mass map is finalised, so a GUI can draw it.
    """
    cfg = cfg or {}
    net = InstantonField(**cfg)
    nc = max(2, ds_train.n_classes)
    ytr, yte = ds_train.labels, ds_test.labels
    res = {}

    def _stop():
        return stop is not None and stop()

    log(f"[setup] grid {net.cfg['n']}  steps {net.cfg['steps']}  "
        f"ports {net.ports.grid}^2  probes {net.probes.n_probes}  "
        f"features {net.probes.n_probes * net.cfg['bins']}")
    log(f"[data ] train {len(ds_train)}  test {len(ds_test)}  "
        f"classes {ds_train.class_names}")

    # --- dormant medium (control: no learning at all) -------------------
    log("[arm  ] MEDIUM-DORMANT   (uniform mu, never learned)")
    Xtr = net.extract(ds_train, mu=net.mu_dormant)
    if _stop(): return res
    Xte = net.extract(ds_test, mu=net.mu_dormant)
    if _stop(): return res
    res["MEDIUM-DORMANT"] = net.score_arm(Xtr, ytr, Xte, yte, nc)
    _report(log, "MEDIUM-DORMANT", res["MEDIUM-DORMANT"])

    # --- train ----------------------------------------------------------
    log(f"[train] {net.cfg['epochs']} epochs, unsupervised, fixed mass budget")
    net.train(ds_train, stop=stop)
    if _stop(): return res
    st = net.medium.stats()
    log(f"[mu   ] sum {st['mu_sum']:.2f} (budget {st['budget']:.2f})  "
        f"mean {st['mu_mean']:.4f}  std {st['mu_std']:.4f}  "
        f"max {st['mu_max']:.4f}")
    budget_err = abs(st["mu_sum"] - st["budget"]) / st["budget"]
    log(f"[check] budget error {budget_err:.2e}  "
        f"{'OK' if budget_err < 1e-6 else 'FAIL - mass is not conserved'}")
    if on_mu:
        on_mu(net.mu_learned, "learned")

    # --- learned --------------------------------------------------------
    log("[arm  ] MEDIUM-LEARNED")
    Xtr_L = net.extract(ds_train, mu=net.mu_learned)
    if _stop(): return res
    Xte_L = net.extract(ds_test, mu=net.mu_learned)
    if _stop(): return res
    res["MEDIUM-LEARNED"] = net.score_arm(Xtr_L, ytr, Xte_L, yte, nc)
    _report(log, "MEDIUM-LEARNED", res["MEDIUM-LEARNED"])

    # --- shuffled -------------------------------------------------------
    log("[arm  ] MEDIUM-SHUFFLED  (same mass values, scrambled positions)")
    net.medium.set_mu(net.mu_learned)
    mu_sh = net.medium.shuffled_mu(seed=net.cfg["seed"])
    _assert_matched(log, net.mu_learned, mu_sh)
    if on_mu:
        on_mu(mu_sh, "shuffled")
    Xtr_S = net.extract(ds_train, mu=mu_sh)
    if _stop(): return res
    Xte_S = net.extract(ds_test, mu=mu_sh)
    if _stop(): return res
    res["MEDIUM-SHUFFLED"] = net.score_arm(Xtr_S, ytr, Xte_S, yte, nc)
    _report(log, "MEDIUM-SHUFFLED", res["MEDIUM-SHUFFLED"])

    # --- matched random -------------------------------------------------
    log("[arm  ] MEDIUM-RANDOM    (matched histogram, independent draw)")
    net.medium.set_mu(net.mu_learned)
    mu_rd = net.medium.matched_random_mu(seed=net.cfg["seed"])
    Xtr_R = net.extract(ds_train, mu=mu_rd)
    if _stop(): return res
    Xte_R = net.extract(ds_test, mu=mu_rd)
    if _stop(): return res
    res["MEDIUM-RANDOM"] = net.score_arm(Xtr_R, ytr, Xte_R, yte, nc)
    _report(log, "MEDIUM-RANDOM", res["MEDIUM-RANDOM"])

    # --- attackers ------------------------------------------------------
    log("[arm  ] PIXELS           (ridge on the raw port amplitudes)")
    res["PIXELS"] = net.score_arm(pixel_features(ds_train), ytr,
                                  pixel_features(ds_test), yte, nc)
    _report(log, "PIXELS", res["PIXELS"])

    dim = net.probes.n_probes * net.cfg["bins"]
    log(f"[arm  ] RANDOM-FEATURES  (untrained tanh expansion, dim {dim})")
    res["RANDOM-FEATURES"] = net.score_arm(
        random_features(ds_train, dim, net.cfg["seed"]), ytr,
        random_features(ds_test, dim, net.cfg["seed"]), yte, nc)
    _report(log, "RANDOM-FEATURES", res["RANDOM-FEATURES"])

    _verdict(log, res)
    net.results = res
    return res, net


def _report(log, name, m):
    log(f"         {name:16s} test {m['test_acc']:.3f}  "
        f"P@1 {m['p_at_1']:.3f}  (train {m['train_acc']:.3f}, "
        f"alpha {m['alpha']:g}, dim {m['dim']})")


def _assert_matched(log, a, b):
    sa, sb = np.sort(a.ravel()), np.sort(b.ravel())
    ok = np.allclose(sa, sb)
    log(f"[check] shuffle preserves the mass multiset: "
        f"{'OK' if ok else 'FAIL'}  "
        f"(sum {a.sum():.6f} vs {b.sum():.6f}, std {a.std():.6f} vs {b.std():.6f})")


def _verdict(log, res):
    def g(k):
        return res[k]["test_acc"] if k in res else float("nan")
    L, D, S, R = g("MEDIUM-LEARNED"), g("MEDIUM-DORMANT"), g("MEDIUM-SHUFFLED"), g("MEDIUM-RANDOM")
    P, F = g("PIXELS"), g("RANDOM-FEATURES")
    log("")
    log("VERDICT")
    log(f"  P1  learning did something      L-D = {L - D:+.3f}   "
        f"{'PASS' if L > D else 'FAIL: deposition is decorative'}")
    log(f"  P2  geometry is load-bearing    L-S = {L - S:+.3f}   "
        f"{'PASS' if L > S else 'FAIL: this is an arbitrary heterogeneous filter'}")
    log(f"  P2b not just heterogeneity      L-R = {L - R:+.3f}")
    log(f"  P3  vs untrained expansion      L-F = {L - F:+.3f}   "
        f"{'medium ahead' if L > F else 'attacker ties or wins'}")
    log(f"  P4  vs raw pixels               L-P = {L - P:+.3f}   "
        f"{'medium ahead' if L > P else 'attacker ties or wins'}")
    if not (L > D and L > S):
        log("  -> the honest headline is a NEGATIVE result.  Say so.")
    elif L <= max(F, P):
        log("  -> mechanism real, capability advantage NOT established.")
    else:
        log("  -> both mechanism and advantage survive this dataset.  "
            "Re-run on harder data before believing it.")


# ------------------------------------------------------------------- suite

def run_suite(ds, cfg=None, repeats=5, split_frac=0.7, log=print, stop=None):
    """
    The same ladder over several seeds, with PAIRED differences.

    A single run of this size has a noise floor of several accuracy points.
    Reading `L - S = -0.04` off one run as a FAIL is exactly the mistake
    the gates exist to prevent, so the suite reports mean +/- sd of the
    paired difference and only calls a verdict when the effect clears its
    own spread.
    """
    cfg = dict(cfg or {})
    arms, diffs = {}, {}
    for r in range(repeats):
        if stop is not None and stop():
            break
        c = dict(cfg)
        c["seed"] = cfg.get("seed", 0) + r
        tr, te = ds.split(split_frac, seed=c["seed"])
        log(f"\n===== repeat {r + 1}/{repeats} (seed {c['seed']}) =====")
        out = run_gates(tr, te, cfg=c, log=log, stop=stop)
        if not isinstance(out, tuple):
            break
        res, _ = out
        for k, v in res.items():
            arms.setdefault(k, []).append(v["test_acc"])
        for a, b in (("MEDIUM-LEARNED", "MEDIUM-DORMANT"),
                     ("MEDIUM-LEARNED", "MEDIUM-SHUFFLED"),
                     ("MEDIUM-LEARNED", "MEDIUM-RANDOM"),
                     ("MEDIUM-LEARNED", "RANDOM-FEATURES"),
                     ("MEDIUM-LEARNED", "PIXELS")):
            if a in res and b in res:
                diffs.setdefault(f"{a} - {b}", []).append(
                    res[a]["test_acc"] - res[b]["test_acc"])

    log("\n" + "=" * 62)
    log(f"SUITE over {len(next(iter(arms.values()), []))} repeats")
    for k in ("MEDIUM-LEARNED", "MEDIUM-DORMANT", "MEDIUM-SHUFFLED",
              "MEDIUM-RANDOM", "PIXELS", "RANDOM-FEATURES"):
        if k in arms:
            v = np.array(arms[k])
            log(f"  {k:16s} {v.mean():.3f} +/- {v.std(ddof=1) if len(v)>1 else 0:.3f}")
    log("")
    for k, v in diffs.items():
        v = np.array(v)
        sd = v.std(ddof=1) if len(v) > 1 else 0.0
        se = sd / max(1, np.sqrt(len(v)))
        clear = abs(v.mean()) > 2 * se and se > 0
        log(f"  {k:36s} {v.mean():+.3f} +/- {sd:.3f}  "
            f"(se {se:.3f}) {'SIGNIFICANT' if clear else 'within noise'}")
    return arms, diffs
