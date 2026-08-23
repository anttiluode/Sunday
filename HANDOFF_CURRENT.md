# Sunday — current handoff

Date: 2026-08-23

## Restart from here

Do **not** restart from the original 3-D dendrite / splat / instanton story.

Sunday has been audited. The current object is narrower:

> **A local fixed-budget plasticity rule can write equal-marginal relational history into persistent distributed substrate state, changing later pair interactions after the teaching history and fast state are gone. Much of the substrate's apparent computation is nevertheless explainable as fixed-reservoir feature geometry plus ordinary six-terminal symmetry.**

That sentence contains both the surviving result and the demotion.

Read, in order:

```text
README.md
this file
docs/AUDIT_RESULT.md
KILL_LEDGER.md
```

Historical gate details remain in `docs/` and machine-readable fresh receipts in `receipts/`.

---

## Current verdict in four pieces

### 1. Persistent structural relation memory survives

The strongest pre-audit result is still Gates 6–7.

Two matched six-terminal training programs have identical terminal marginals; only which terminals co-occur differs. Under a fixed total structural-mass budget, the local current-based rule leaves different persistent mass states. After teaching ends and fast dynamical state is reset, the two frozen substrates respond differently to later pair probes.

Gate 6 fresh `380000..380009`:

```text
registered trained-edge signs        60/60
mean signed differential contrast    0.002666
trained / unused |dI|                12.303x
mass-shuffle residual                0.061x
```

Gate 7 kills one-scalar endpoint reductions:

```text
additive endpoint all-pair R^2       0.0753 mean
held-out trained-edge sign           1/60
negative multiplicative cycle        10/10
```

Safe statement:

> Relational co-occurrence history can become persistent distributed edge/cycle-space structure in this toy substrate without explicit learned pair weights.

This does **not** imply parameter efficiency; an explicit pair table is much cheaper.

---

### 2. Reservoir audit demotes the computation claim

Audit A uses six new dormant substrates `520000..520005`.

Gate 10 already defines the dormant one-step write feature map

```text
x(q) = q W
```

for the controlled Gate-9 relation program `q`.

Fresh audit:

```text
rank(Q)                              7
rank(QW)                             7 on 6/6 seeds
minimum leave-one-code-out rank      7
LOO linear q <- qW NMSE              5.65e-30
LOO cosine                           1.0
```

Therefore the fixed dormant substrate features preserve the complete tested relation span. Since Gate 9 already established an almost-linear finite map `y ~= qB`, a conventional trained linear readout on fixed `qW` features can represent the same class of transforms:

```text
q --W--> fixed dormant features x --trained linear readout--> y
```

So kill this broad interpretation:

> Gate 9/10 by itself discovered a new computing primitive beyond reservoir-style fixed features + trained readout.

What remains different is **where memory lives**. Sunday changes persistent internal `mass`. The fixed-reservoir null leaves the substrate unchanged and stores learned task information in an external readout.

Receipt:

```text
receipts/audit_reservoir_null_fresh6.json
```

Script:

```text
experiments/audit_reservoir_null.py
```

---

### 3. Ring-symmetry audit demotes the mysterious-three-mode story

Gate 9 reported a stable ~three-dimensional preferred relation subspace. The six terminals are placed on an exact ring, so Audit B attacks that before assigning any deeper meaning.

The controlled rank-7 relation span decomposes under ring rotation into:

```text
k=1   dimension 2
k=2   dimension 4
k=3   dimension 1
```

A geometry-only three-dimensional candidate was fixed from exploratory dormant analysis:

```text
nearest-neighbour edge-orbit k=2 copy (2-D)
+
k=3 parity mode (1-D)
```

Fresh **full 40-cycle Gate-9 training** on `522000..522003`:

```text
finite operator top-3 energy               0.9781

broad k2+k3 sector:
  mean top-3 subspace capture              0.9633
  mean weakest principal cosine            0.9475

fixed geometry-only 3-D candidate:
  mean top-3 subspace capture              0.8783
  mean weakest principal cosine            0.8587
```

Mean learned top-three sector fractions:

```text
k1    0.0367
k2    0.6564
k3    0.3069
```

So most of the preferred-mode story is ordinary port geometry/symmetry.

But not all of it. The `k=2` sector is four-dimensional; symmetry alone does not choose the particular two-dimensional copy/rotation used by a substrate. The fixed 3-D geometry candidate misses about 12% of subspace energy on average, with one weakest fresh cosine `0.777`.

Live mechanistic residual:

> **What graph/current-flow/write-read structure selects the substrate-specific orientation inside the symmetry-allowed `k=2` sector?**

Receipt:

```text
receipts/audit_ring_symmetry_fresh4.json
```

Script:

```text
experiments/audit_ring_symmetry.py
```

---

### 4. Gate 12 remains a failure

Do not lose this during cleanup.

Fresh `500000..500005`:

```text
READ / WRITE clean utility     1.076767x
registered minimum             1.080000x
```

Therefore Gate 12 **FAILS**.

Dormant READ information still predicts cleanliness and improves selectivity on some substrates, but do not lower the threshold or keep optimizing the same C3/18-route toy.

---

## What has been killed or demoted

Short version; `KILL_LEDGER.md` is authoritative.

```text
pixels as recurrent state                         killed
literal branch birth as first explanation         demoted
Gate-0 structure == calculation                   killed (linear)
3-D coordinates == primitive                      killed
clustering alone                                  not established
low spectral gap / slow mixing alone              killed
endpoint scalar explanation                       killed
isotropic arbitrary relation memory               killed
long training invents preferred modes             killed as first explanation
Gate-9 transform beyond reservoir readout          killed by audit
mysterious/new three-mode algebra                 demoted by symmetry audit
Gate-12 >=8% incremental READ control             failed
```

Do not import QM, phase, ferroic memory, growth, visual/world data, Feigenbaum/fractal stories, or a learned decoder merely to escape an audit result.

---

## Relation to reservoir computing

Sunday is now explicitly in the adaptive/physical-reservoir neighborhood.

Known reservoir ideas already cover:

- a complex fixed substrate exposing useful nonlinear features;
- trained linear readouts;
- input masks/routing that determine which modes are excited;
- structural-plasticity variants that modify reservoir connectivity/state.

Therefore do not claim broad novelty from those ingredients.

The remaining Sunday-specific experimental question is more constrained:

> **When, if ever, is it useful to store relational history by physically changing the substrate itself rather than leaving the substrate fixed and putting learning in an observer/readout?**

That requires a fair resource/task comparison, not another metaphor.

See `docs/AUDIT_RESULT.md` for references and exact interpretation.

---

## Good next experiments — choose one, do not automatically stack them

### A. Persistent-memory vs reservoir audit

Construct a task where:

```text
training/history input ends
fast state is explicitly reset
future query arrives later
```

Compare:

```text
Sunday structural memory
fixed reservoir + trained external readout
adaptive/structural reservoir baseline
explicit relation table
```

Account for where learned state is stored and how many trainable/persistent scalars each method receives.

The question is not accuracy alone. Ask whether in-medium persistence buys anything under matched resource/latency/locality constraints.

### B. Explain the remaining symmetry-sector rotation

Stay dormant/linear and try to predict the selected two-dimensional slice inside the four-dimensional `k=2` relation sector from ordinary graph quantities:

```text
terminal-to-soma current-flow fields
pairwise current overlap
edge betweenness / corridor incidence
Laplacian diffusion modes
write/read Jacobian alignment
```

Any candidate must predict held-out substrate orientation, not merely correlate after seeing it.

### C. Leave the tangent regime deliberately

Gate 10 says dormant first-order geometry predicts 40-cycle training surprisingly well. Sweep training strength:

```text
1, 2, 5, 10, 20, 40, 80, 160 cycles
```

Track when dormant prediction fails and whether **new useful structural modes** appear. If no new modes appear, Sunday is mostly a fixed low-dimensional response geometry being amplified.

This is a better test of genuine self-construction than making the current toy larger.

---

## Reproduction shortcuts

```bash
pip install -e .

python experiments/gate6_relation_matrix.py
python experiments/gate7_endpoint_null.py
python experiments/gate9_writable_subspace.py
python experiments/gate10_dormant_jacobian.py

python experiments/audit_reservoir_null.py
# slow: retrains all 16 Gate-9 codes on four substrates
python experiments/audit_ring_symmetry.py

python -m unittest discover -s tests -v
```

Stored fresh audit numbers should be compared against the JSON receipts rather than regenerated until they look nicer.

---

## Restart rule for the next Sol

Do not add an idea first.

Ask:

1. What exact surviving claim is being tested?
2. What boring known mechanism would reproduce it?
3. Where is learned information allowed to live in each arm?
4. What is held fixed?
5. What result would actually demote the Sunday story further?

If the boring attacker wins, record it and move the boundary.
