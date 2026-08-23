# Sunday — current handoff

Date: 2026-08-23

## Restart rule

Do not restart from the dendrite/3-D metaphor. Restart from the receipts and dead claims below.

Sunday's live question is now:

> **What graph structure lets local signal-driven mass plasticity write strong relations between inputs, and can those relations compose into useful computation?**

## Lineage

```text
Gate 0  signal-carved microarbor             PASS as routing memory
        exact superposition attacker         KILLS calculation claim

Gate 1  matched coactivation histories       PASS
        pair relation + distributed nonlinear readout

Gate 2  abstract graph attacker v0            INVALID numerical overflow
Gate 2  stable graph attacker v1              PASS
        3-D necessity claim                   KILLED
        locality amplification                SURVIVES

Gate 3  topology/locality dial                FAIL prereg
        clustering as leading descriptor      NOT established
        mixing/corridor hypothesis            sharpened post-hoc only
```

Accepted/default branch should contain all of the above before the next gate.

## Gate 0 receipt

Fixed 256-element substrate, fixed total mass, no birth/deletion, no learned free-form edges.

Signal history redistributes slow node mass and changes later transfer. Correct-route gains were ~1.4x over uniform and ~1.7x over mass-shuffled controls.

But frozen dynamics obey superposition to floating precision (`~1e-17` whole-state error). Therefore Gate 0 is **adaptive routing / structural memory, not a calculating dendrite**.

See:

```text
docs/GATE0_SIGNAL_CARVED_MICROARBOR.md
docs/GATE0_LINEARITY_ATTACKER.md
```

## Gate 1 receipt

Matched programs:

```text
H_AB: [A+B], [C], [D]
H_CD: [C+D], [A], [B]
```

Each terminal occurs exactly once per cycle in both histories. Only coactivation grouping changes.

Held-out `240000..240019`:

```text
route-separation sign             20/20 both pairs
nonlinear-interaction sign        20/20 both pairs
mean route separation             0.116056
mean nonlinear separation         0.008948
mass-shuffle signed ratio         ~0.04
```

Coactivity currently causes **route separation**, not Hebbian-style route merging. Do not rewrite that story.

A 15-point operating sweep on six fresh clouds gave the expected interaction sign 180/180.

Safe statement:

> Experience can write a pair relation into transfer geometry without explicit pair weights; a fixed distributed local nonlinearity can read that relation as a pairwise interaction.

See:

```text
docs/GATE1_LOCAL_NONLINEAR_OVERLAP.md
docs/GATE1_ROBUSTNESS_SWEEP.md
```

## Gate 2 receipt — 3-D demoted

Gate-2 v0 is invalid because the original explicit-Euler cubic probe overflowed on some rewired graphs. Preserve `docs/GATE2_V0_INVALID.md`; NaNs were not counted as geometry winning.

Stable v1 fresh range `300000..300011`:

```text
GEO route separation                 0.121534
REWIRE |route separation|            0.018915
ratio                                6.425x

GEO nonlinear separation             0.008661
REWIRE |nonlinear separation|        0.001860
ratio                                4.657x

same graph + coordinates erased      exactly identical
rewires exact degree                 yes
rewires connected                    yes
initial node strength error          < 1e-10
rewired long-edge fraction           ~0.88
```

The rewire arm still had the expected pair-relation sign 12/12 for every measure.

Therefore:

> **The current primitive is graph-generic. 3-D coordinates are not execution-time necessities. Euclidean locality is an inductive/topological constraint that strongly amplifies the effect.**

See:

```text
docs/GATE2_V1_RESULT.md
receipts/gate2_v1_confirm12.json
```

## Gate 3 receipt — FAIL, useful residual

A nested degree-preserving locality dial used similar-weight edge swaps and rematched every node's strength. Fresh range `320000..320005`, six topology levels each.

Level means:

```text
swaps/E  clustering  path   gap    nonlinear separation
0.0      0.5865      2.992  .0716  0.008354
0.1      0.3494      2.271  .2361  0.003079
0.5      0.1224      2.088  .5661  0.001604
1.0      0.1050      2.068  .6066  0.001561
2.0      0.1052      2.063  .6132  0.001716
5.0      0.1053      2.059  .6177  0.001662
```

Strong collapse survived:

```text
0.5E clustering / GEO                 0.209
0.5E |interaction| / GEO             0.192
saturated |interaction| / GEO        0.202
```

But preregistered:

```text
rho(clustering, |interaction|) >= .60
```

observed only:

```text
+0.575
```

so **Gate 3 FAILS**.

The preregistered spectral-gap anticorrelation passed (`rho=-0.679`). Post-hoc only, mean path length tracked |interaction| at `rho=+0.720` and route separation even more strongly.

Do not call clustering causal.

See:

```text
docs/GATE3_RESULT.md
receipts/gate3_topology_dial_confirm6.json
```

## Current residual

The live hypothesis is broader than clustering:

```text
local / corridor-like / poorly mixed topology
    -> signals retain distinguishable route structure
    -> fixed-budget node-mass plasticity can sculpt relations strongly

expander-like / rapidly mixed topology
    -> routes diffuse together
    -> only the weak generic-graph relation survives
```

This is still only a hypothesis.

### Next targeted attacker

Construct a **highly non-geometric graph with low spectral gap / slow mixing** by imposing random communities unrelated to xyz while preserving exact node degree and rematching node strength.

Consumed exploratory seeds already show that restoring low gap alone did *not* restore the GEO nonlinear effect (rough modular/GEO interaction ratios: -0.01, 0.08, 0.28). This is calibration only.

The next fresh gate should test:

> Is slow mixing sufficient, or is the important object the alignment of local corridors with where signals enter and leave?

If random low-gap modular graphs remain weak, the useful structure is more specific than any single global mixing statistic.

## Hard stop lines

- total structural mass stays fixed unless a gate explicitly tests growth;
- no learned pair-specific edge weights while claiming morphology carries the relation;
- rendering stays read-only;
- no hand-designed dendritic tree;
- Gate 0 is linear routing;
- Gate 1 is not established Hebbian binding;
- 3-D coordinates are not the current computational primitive;
- Gate 3 did not establish clustering as causal;
- no faces, VKITTI, CLIP, oscillations, ferroic memory, growth or autonomous visual recurrence until a specific residual requires them.

## Feigenbaum note

Still parked. No evidence yet for fractal branching, bifurcation cascades or self-similar morphology. If such structure emerges without being planted, measure it then.
