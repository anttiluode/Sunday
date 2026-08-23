# Sunday — current handoff

Date: 2026-08-23

## Message to the next Sol instance

Do not restart from the motivating metaphor. Restart from the receipts.

Sunday asks:

> Can repeated signal write persistent transfer structure into a fixed amount of computational material, and can that structure become a calculating primitive rather than merely a route?

The project has now separated three layers:

```text
Gate 0  signal can write spatial routing              PASS
        but frozen dynamics are exactly linear        ATTACKER WINS

Gate 1  coactivation can write a pair relation        PASS
        local nonlinearity reads it as interaction

Gate 2  is that relation inherently 3-D?              NO
        does Euclidean locality amplify it?            YES in current instrument
```

## Branch lineage

```text
sol/gate0-signal-carved-microarbor
sol/gate1-local-nonlinear-overlap
sol/gate2-abstract-graph-attacker          INVALID v0 nonlinear comparison
sol/gate2-v1-stable-graph-attacker         CURRENT ACCEPTED GATE 2
```

`main` should be fast-forwarded to the accepted Gate-2 v1 lineage before beginning the next gate.

---

## Gate 0 — spatial transfer memory, not calculation

Fixed resources:

```text
256 elements
same xyz positions
same geometry graph
same initial uniform mass
total mass budget = 256
no birth/deletion
no learned free-form edges
no pixel feedback
```

Representative accepted receipt:

```text
A selectivity                 1.3286x
B selectivity                 1.5472x
A gain over uniform           1.3900x
B gain over uniform           1.4548x
A gain over mass shuffle      1.7370x
B gain over mass shuffle      1.7506x
observer on/off trace         exactly identical
```

Safe statement:

> Signal history can become persistent spatial transfer geometry under a fixed material budget.

### Gate-0 linearity attacker

The attacker wins exactly:

```text
R(A+B) - [R(A)+R(B)]  ~1e-17 whole-state
soma error             ~1e-19
R(2A)-2R(A)            0 in tested run
```

Do not call Gate 0 a dendritic calculating primitive. It is adaptive routing / structural memory.

Files:

```text
sunday/microarbor.py
experiments/gate0_signal_carved_microarbor.py
experiments/gate0_linearity_attacker.py
docs/GATE0_SIGNAL_CARVED_MICROARBOR.md
docs/GATE0_LINEARITY_ATTACKER.md
```

---

## Gate 1 — a relation between inputs can be written into the medium

Matched histories:

```text
H_AB: [A+B], [C], [D]
H_CD: [C+D], [A], [B]
```

Every terminal occurs exactly once per cycle in both histories. Only coactivation grouping changes.

Surprise: under the current current-reinforcement + fixed-budget rule, the coactive pair becomes **less internally route-overlapping**, not more. Do not retrofit a Hebbian story.

Held-out confirmation `240000..240019`:

```text
AB route-separation positive              20/20
CD route-separation positive              20/20
AB nonlinear-interaction separation       20/20
CD nonlinear-interaction separation       20/20
mean route-overlap separation             0.116056
mean nonlinear interaction separation     0.008948
mass-shuffle signed ratio                 ~0.04
```

A soma-only nonlinearity produces almost no program effect. The distributed/soma ratio is ~1036x only because the soma-only denominator is microscopic; always state the absolute distributed effect (~0.009).

A fresh operating sweep over 5 cubic strengths x 3 amplitudes x 6 clouds x 2 pairs gave the expected sign **180/180**. So the sign is not a one-operating-point accident.

Safe statement:

> Experience can write a pair relation into transfer geometry without explicit pair-specific learned weights. A fixed local nonlinearity later converts route overlap into a pairwise interaction.

Files:

```text
sunday/nonlinear_overlap.py
experiments/gate1_local_nonlinear_overlap.py
experiments/gate1_robustness_sweep.py
docs/GATE1_LOCAL_NONLINEAR_OVERLAP.md
docs/GATE1_ROBUSTNESS_SWEEP.md
receipts/gate1_confirm20.json
receipts/gate1_robustness_confirm6.json
```

---

## Gate 2 v0 — INVALID, preserve the failure

The first abstract-graph confirmation used Gate 1's original explicit-Euler cubic probe. Some degree+strength-matched rewired graphs at held-out seeds `280005` and `280006` overflowed and produced NaNs.

Those NaNs were **not counted as geometry winning**.

The range was abandoned and recorded in:

```text
docs/GATE2_V0_INVALID.md
```

Do not reuse `280000..280011` as fresh confirmation.

---

## Gate 2 v1 — PASS, but 3-D is demoted

Fresh range:

```text
300000..300011
```

The nonlinear response was integrated with 8 equal response-only substeps in both arms. Learning was unchanged.

### Arms

```text
GEO
  xyz -> radial kernel/cutoff -> base graph

GRAPH-SAME
  exact same base graph
  coordinates replaced with zeros

REWIRE-DS
  repeated double-edge swaps
  exact unweighted degree per node
  connected
  initial weighted degree/node strength matched to <1e-10
  ~88% of edges longer than original Euclidean cutoff
```

### Receipt

```text
GEO mean route separation                 0.121534
REWIRE mean |route separation|            0.018915
GEO / REWIRE                              6.425x

GEO mean nonlinear interaction separation 0.008661
REWIRE mean |interaction separation|      0.001860
GEO / REWIRE                              4.657x

all expected GEO signs                    12/12 for all four measures
all expected REWIRE signs                 12/12 for all four measures
GRAPH-SAME max difference                 0.0
all rewires exact degree                  yes
all rewires connected                     yes
max initial strength relative error       9.82e-11
minimum long-edge fraction                0.872
all nonlinear values finite               yes
```

### Decisive interpretation

The abstract rewire is **not a null**. It preserves the same qualitative relational phenomenon on every confirmation seed.

Therefore kill this claim:

> 3-D geometry itself is the calculating primitive.

Current equations reduce to:

```text
xyz -> base graph -> all later learning and dynamics
```

Once `base` exists, coordinates are dead metadata. GRAPH-SAME proves this exactly.

What survives:

> **The pair-relation mechanism is graph-generic in this instrument. Euclidean locality is a strong inductive/topological constraint that amplifies and regularizes it.**

This is still interesting, but it changes the target from "3-D matter computes" to "what topology makes this local relational computation strong?"

Gate 2 does not identify that topology because REWIRE-DS does not preserve graph spectrum, clustering, shortest-path distribution, community structure, motifs, or exact post-scaling edge-weight multiset.

Files:

```text
sunday/graph_attacker.py
experiments/gate2_v1_stable_graph_attacker.py
docs/GATE2_GRAPH_ATTACKER_PREREG.md
docs/GATE2_V0_INVALID.md
docs/GATE2_V1_STABLE_PREREG.md
docs/GATE2_V1_RESULT.md
receipts/gate2_v1_confirm12.json
tests/test_gate2.py
```

---

## Current residual — follow this, not the old metaphor

The next question is:

> **Which topology induced by locality amplifies the pair relation?**

The clean next instrument is a **locality dial**:

```text
same geometric graph
  -> progressively more degree-preserving edge swaps
  -> re-match initial node strength
  -> retrain identical histories
  -> measure pair relation + graph statistics
```

Measure at least:

```text
fraction of long/nonlocal edges
clustering / transitivity
mean shortest path if connected
Laplacian / normalized spectral gap
route separation
nonlinear interaction separation
```

Do not simply correlate one exploratory run and announce mechanism. Use the dial to identify candidates, then construct a targeted attacker that matches the candidate statistic while breaking others.

A small composition gate may run after or alongside the topology autopsy:

> Can one fixed mass budget store several pair relations at once and expose them in the frozen pairwise interaction matrix without explicit pair weights?

That is closer to the original dendrite/calculating-primitive question.

---

## Things the next instance must not silently change

- Keep total structural mass fixed unless a new gate explicitly tests growth.
- No learned edge weights independent of geometry/topology while claiming a morphology effect.
- Rendering is read-only; never feed pixels back into state.
- Do not hand-design a tree.
- Gate 0 is linear routing; that interpretation is dead.
- Gate 1 is not established Hebbian binding; coactivity currently causes route separation.
- 3-D coordinates are not execution-time necessities in the current equations.
- Do not claim the 6.4x / 4.7x ratios prove 3-D superiority generally; they compare GEO to one degree+strength-matched rewire family.
- Do not add faces, VKITTI, CLIP, oscillations, ferroic hysteresis, growth, or autonomous recurrence until a specific residual calls for them.

## Feigenbaum / branching note

Still parked. No gate has produced evidence for fractal branching, bifurcation cascades, or self-similar morphology. If such structure later emerges without being planted, quantify it then.
