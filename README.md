# Sunday

**A falsification-driven toy lab for structural relational memory.**

Sunday began with a much more visual question: could a cloud of splat-like material become something dendrite-like when repeated signal changed the material it travelled through?

The repository has spent most of its life attacking that story.

The current, much narrower question is:

> **Can equal-marginal relational history be written by a local rule into persistent distributed substrate state, so that the same future signals interact differently after the teaching history is gone?**

The answer in this toy system is **yes**. The stronger claims — that 3-D itself is the primitive, that the system is an efficient new neural architecture, or that its preferred modes are mysterious — have not survived.

Sunday is useful mainly because the failed interpretations stay in the repository.

---

## The minimal machine

The main six-terminal experiments use a fixed 256-node substrate.

```text
six input terminals
        |
        v
fixed sparse/local graph
        |
        v
fast diffusion-like state v(t)
        |
        +---- local current / eligibility
        |             |
        |             v
        |        slow structural mass m
        |        fixed total mass budget
        |             |
        +-------------+
        |
        v
fixed distributed local nonlinearity
        |
        v
pair interaction readout
```

Structural learning does **not** add nodes or arbitrary pair weights. It redistributes a fixed amount of node mass using local traversal/current information. After training, the fast state is reset but the mass distribution remains.

The important control throughout the repo is therefore:

```text
history changed the medium
not merely the current activation
```

Rendering is observational only. Pixels are never recurrent state.

---

## What survived the gates

| Stage | Result |
| --- | --- |
| Gate 0 | Signal history can write persistent transfer structure under a fixed mass budget. The frozen fast dynamics are exactly linear, so this is routing memory, not calculation. |
| Gate 1 | With identical terminal marginals, changing only which inputs co-occur writes a pair-specific relation. A fixed distributed nonlinearity reads route overlap as an interaction. |
| Gate 2 | Erasing `xyz` after graph construction changes nothing. The primitive is graph-generic; 3-D is not required at execution time. |
| Gates 3–4 | Local geometry helps strongly, but clustering alone and low spectral gap / slow mixing alone are insufficient explanations. |
| Gate 5 | On the **same frozen graph**, changing only how semantic inputs are assigned to physical terminals changes how strongly a relation can be written. Boundary/topology alignment matters. |
| Gate 6 | One fixed mass field can carry several simultaneous coactivity relations. Fresh trained-edge signs: `60/60`; trained/unused differential magnitude: `12.3x`. |
| Gate 7 | The relation matrix is not reducible to one additive or multiplicative scalar per terminal. Leave-one-trained-edge-out additive sign prediction: `1/60`. |
| Gate 8 | Arbitrary relation directions are **not** equally writable. Isotropic/general relation-memory claim killed. |
| Gate 9 | On the controlled rank-7 relation span, finite learning behaves approximately as a linear cross-edge operator; held-out direction cosine `0.9965`; about `97.8%` of operator energy is in three modes. |
| Gate 10 | Much of that operator is visible before long training in dormant one-step WRITE geometry composed with dormant READ sensitivity; fresh cosine `0.9695`. |
| Gate 11 | Dormant WRITE geometry can prospectively choose better semantic-to-physical routing before training; best/worst finite contrast `12.4x`. |
| Gate 12 | READ-aware routing predicted cleanliness but missed its preregistered incremental-control threshold: `1.076767 < 1.08`. **Fail preserved.** |

Full receipts and the exact stop lines live in [`HANDOFF_CURRENT.md`](HANDOFF_CURRENT.md), [`KILL_LEDGER.md`](KILL_LEDGER.md), [`docs/`](docs/), and [`receipts/`](receipts/).

---

## 2026-08-23 audit: did this just become reservoir computing?

Largely, for the broad computation story.

Two explicit audits were added before continuing.

### Fixed-reservoir + trained-readout null

Gate 10 already provides a dormant one-step feature map

```text
x(q) = q W
```

for a controlled relation program `q`.

On six new substrates (`520000..520005`):

```text
rank of registered relation span      7
rank of dormant qW features           7 / 7 on every seed
minimum leave-one-code-out rank       7
linear LOO reconstruction q <- qW
    NMSE                               5.65e-30
    cosine                             1.0
```

So the dormant fixed substrate is a lossless linear embedding of the entire controlled relation span. Since Gate 9's finite outputs are already almost linear in `q`, a conventional trained linear readout on fixed dormant features can represent the same class of relation transforms.

**Demotion:** Gate 9's operator is not by itself evidence for a new computing primitive beyond fixed-feature / reservoir-style computation.

**Surviving distinction:** Sunday writes training history into persistent substrate state. A fixed reservoir plus trained readout stores the learned information in the readout instead.

See [`docs/AUDIT_RESULT.md`](docs/AUDIT_RESULT.md) and [`receipts/audit_reservoir_null_fresh6.json`](receipts/audit_reservoir_null_fresh6.json).

### Six-terminal ring symmetry null

The controlled rank-7 relation space decomposes under ordinary ring rotation into harmonic sectors of dimensions:

```text
k=1    2-D
k=2    4-D
k=3    1-D
```

On four new **fully trained** Gate-9 substrates (`522000..522003`):

```text
finite top-3 operator energy                    0.9781
broad k=2+k=3 symmetry-sector capture           0.9633

fixed geometry-only 3-D candidate:
  nearest-edge k=2 copy + k=3 parity
  learned top-3 subspace capture                0.8783
  mean weakest principal cosine                 0.8587
```

So most of the apparent "three preferred modes" comes from ordinary six-terminal geometry/symmetry. The exact three-dimensional orientation is **not** completely explained; a smaller substrate-specific rotation remains.

See [`receipts/audit_ring_symmetry_fresh4.json`](receipts/audit_ring_symmetry_fresh4.json).

---

## What Sunday does **not** claim

Sunday currently does **not** establish:

- a new general neural-network architecture;
- an efficiency advantage over an explicit relation table;
- 3-D coordinates as the computational primitive;
- biological dendritic realism;
- arbitrary/isotropic relation memory;
- a unique advantage over adaptive or physical reservoir computing;
- quantum, phase, tunnelling, ferroic, or fractal mechanisms;
- that three preferred Gate-9 modes are mysterious rather than mostly symmetry-derived.

The old dendrite / splat / Feigenbaum / instanton motivations are provenance, not current evidence.

---

## What may still be worth studying

The strongest surviving object is deliberately modest:

> **Under a fixed total resource budget, a local plasticity rule can convert equal-marginal co-occurrence history into persistent distributed edge/cycle-space structure that changes later physical interactions after the teaching history and fast state are gone.**

The useful next question is not "how do we make Sunday bigger?"

It is:

> **When does writing history into the medium itself buy something over keeping the substrate fixed and learning an observer/readout?**

A second mechanistic residual is now precise: ordinary ring symmetry explains most of the preferred relation modes, but not the exact substrate-specific orientation inside the symmetry-allowed sector. Current-flow / corridor geometry may explain that remaining rotation.

---

## Run

Python 3.10+ and NumPy are sufficient for the core experiments.

```bash
pip install -e .
```

A few useful entry points:

```bash
# early structural relation result
python experiments/gate1_local_nonlinear_overlap.py

# compositional relation matrix
python experiments/gate6_relation_matrix.py

# relation-space tomography
python experiments/gate9_writable_subspace.py

# dormant write/read mechanism
python experiments/gate10_dormant_jacobian.py

# audit A: fixed reservoir + trained linear readout
python experiments/audit_reservoir_null.py

# audit B: ring symmetry (slow: full Gate-9 training on four fresh substrates)
python experiments/audit_ring_symmetry.py

# tests
python -m unittest discover -s tests -v
```

If an experiment has a stored confirmation receipt, prefer the registered seed range and thresholds in its matching `docs/` file over ad-hoc tuning.

---

## Repository map

```text
sunday/        mechanisms used by the experiments
experiments/   executable gates, attackers and audits
docs/          preregistrations, results and audit interpretation
receipts/      stored fresh-seed machine-readable results
tests/         invariants and regression tests

HANDOFF_CURRENT.md   exact restart state for the next work session
KILL_LEDGER.md       claims/mechanisms that may not be quietly resurrected
```

Sunday's rule is simple:

> **A pretty mechanism gets no credit until the boring attacker has had a turn.**
