# Gate 0 — signal-carved 3-D microarbor

## Question

Can repeated signal redistribute a **fixed amount** of slow structural mass inside a **fixed 3-D cloud** so that later transfer depends on the learned spatial arrangement?

This gate does not ask whether the system is a good neural network. It asks whether history can become embodied in geometry-sensitive transfer without adding elements or learned free-form edges.

## Candidate mechanism

The substrate has 256 fixed elements. Each element has a 3-D position and a slow mass `m_i`.

A geometry-only overlap matrix is built once:

```text
base_ij = exp(-||r_i-r_j||^2 / (2 ell^2))
```

with a finite distance cutoff. No entry of `base` is learned.

Current conductance is:

```text
G_ij = base_ij * sqrt(m_i m_j)
```

Fast state is linear leaky diffusion on `G` plus external drive.

During a training episode one terminal acts as source and the soma as sink. Local incident current supplies eligibility. Slow mass moves toward repeatedly used regions under:

- a per-element floor;
- fixed soma/terminal masses;
- an exact global mass budget equal to the initial budget.

No element is born, deleted or moved.

## Held fixed

The A and B histories use exactly the same:

```text
256 xyz positions
base overlap graph
soma position
terminal positions
initial uniform mass
mass budget = 256
fast dynamics
learning rule
number of training episodes
```

Only which terminal is repeatedly driven changes.

## Registered controls

1. **Uniform material** — same cloud before structural learning.
2. **Cross-terminal probe** — A-trained material is probed from A and B; likewise B-trained.
3. **Mass-budget equality** — learned copies must remain at the original total mass.
4. **Geometry shuffle** — learned non-port mass values are randomly permuted among the same positions. This preserves the exact mass multiset, positions, number of elements and total budget while destroying the learned spatial arrangement.
5. **Observer purity** — calling the observer every time step must leave the numerical trajectory bit-identical.

## Registered receipt thresholds

```text
correct / cross-terminal peak        >= 1.20x for A and B
correct / uniform-material peak      >= 1.20x for A and B
correct / median mass-shuffle peak   >= 1.35x for A and B
mass budget error                    < 1e-10
observer-on trace                    exactly equals observer-off trace
```

Forty independently seeded geometry shuffles are used for each trained material.

## Reproduction

```bash
python -m unittest discover -s tests -v
python experiments/gate0_signal_carved_microarbor.py
python experiments/gate0_signal_carved_microarbor.py --json
```

Optional read-only 3-D observer:

```bash
pip install -e '.[plot]'
python experiments/gate0_signal_carved_microarbor.py --plot gate0.png
```

The plot is not used by the simulation.

## First deterministic receipt

Local validation before push used Python 3.13.5 and NumPy 2.3.5.

```text
uniform peak A        9.759775e-05
uniform peak B        1.003117e-04

A-trained peak A      1.356617e-04
A-trained peak B      1.021100e-04
A selectivity         1.3286x
A gain over uniform   1.3900x
A gain over shuffle   1.7370x

B-trained peak A      9.432185e-05
B-trained peak B      1.459337e-04
B selectivity         1.5472x
B gain over uniform   1.4548x
B gain over shuffle   1.7506x

mass sum A            256.0
mass sum B            ~256.0 floating precision
observer identical    True

4/4 unit tests pass
Gate 0 receipt        PASS
```

The machine-readable copy is in `receipts/gate0_v0.json`.

## What survived

A different signal history can redistribute the same scalar material values into a different 3-D arrangement, and that arrangement changes later transfer. The mass-shuffle attacker matters: the result is not explained by total mass or the learned mass histogram alone.

A safe description is:

> **signal-written, spatially embodied transfer geometry**

or, more colloquially, a signal-carved microarbor.

## What did not survive merely by passing this gate

This is **not yet a dendritic calculating primitive**.

The frozen fast dynamics are linear. Therefore a strong immediate attacker is superposition:

```text
response(A + B) ?= response(A) + response(B)
```

If equality holds to numerical precision, the current object is adaptive routing/memory in structure, not nonlinear branch computation. That is expected from the equation and must be made explicit before advancing.

The gate also does not establish:

- advantage over adaptive transport networks;
- learning efficiency;
- biological realism;
- literal energetic advantage;
- autonomous growth;
- a reason to prefer 3-D over an abstract graph for software execution;
- visual/world-model ability.

## Stop lines

Demote the morphology claim if mass shuffling does not materially reduce transfer after replication across seeds/clouds.

Demote the 3-D claim if an attacker that discards spatial embedding while preserving the effective graph reproduces everything of interest more cheaply.

Do not call the object a dendritic *computer* until a later gate demonstrates an interaction/nonlinearity that the present linear transfer system cannot reproduce by superposition.
