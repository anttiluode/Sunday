# Sunday — current handoff

Date: 2026-08-23

## Restart rule

Do not restart from the dendrite/3-D/QM metaphor. Restart from the receipts and dead claims.

Sunday's live question is now:

> **What topology lets local signal-driven mass plasticity write strong relations between inputs, and can those relations compose into useful computation without explicit pair weights?**

## Lineage

```text
Gate 0  signal-carved microarbor             PASS as routing memory
        exact superposition attacker         KILLS calculation claim

Gate 1  matched coactivation histories       PASS
        pair relation + distributed nonlinear readout

Gate 2  abstract graph attacker v0           INVALID numerical overflow
Gate 2  stable graph attacker v1             PASS
        3-D necessity claim                  KILLED
        locality amplification               SURVIVES

Gate 3  topology/locality dial               FAIL prereg
        clustering explanation               NOT established
        effect collapses leaving local regime SURVIVES

Gate 4  low-gap non-geometric attacker       PASS
        slow global mixing sufficient?       KILLED
        signal/topology alignment residual   OPEN
```

## Gate 0 — route, not calculation

Fixed 256-element substrate, fixed total structural mass, no birth/deletion, no free learned edges.

Representative receipt:

```text
correct-route gain over uniform      ~1.4x
correct-route gain over mass shuffle ~1.7x
```

But frozen dynamics obey superposition to floating precision (`~1e-17` whole-state error). Gate 0 is adaptive routing / structural memory, **not** a calculating dendrite.

## Gate 1 — experience writes a relation between inputs

Matched histories:

```text
H_AB: [A+B], [C], [D]
H_CD: [C+D], [A], [B]
```

Every terminal occurs once per cycle in both histories. Only coactivation grouping differs.

Held-out `240000..240019`:

```text
route-separation sign             20/20 both pairs
nonlinear-interaction sign        20/20 both pairs
mean route separation             0.116056
mean nonlinear separation         0.008948
mass-shuffle signed ratio         ~0.04
```

A 15-point nonlinear operating sweep on six fresh clouds gave the expected sign 180/180.

Important surprise: coactivity causes **route separation** under the current fixed-budget current-reinforcement rule. Do not retrofit a Hebbian-merging story.

Safe statement:

> Experience can write a pair relation into transfer geometry without explicit pair weights; a fixed distributed local nonlinearity can read that relation as pairwise interaction.

## Gate 2 — 3-D demoted

Stable v1 fresh `300000..300011`:

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

The rewire still had the expected qualitative relation 12/12.

Therefore:

> **The primitive is graph-generic in this instrument. 3-D coordinates are not execution-time necessities. Euclidean locality is an inductive/topological constraint that strongly amplifies the relation.**

Gate-2 v0 remains explicitly invalid because some rewired nonlinear probes numerically overflowed. Do not count NaNs as geometry winning.

## Gate 3 — locality dial FAILS prereg, leaves a regime transition

Fresh `320000..320005`, nested degree-preserving similar-weight rewires with node strength rematched:

```text
swaps/E  clustering  path   gap    nonlinear separation
0.0      0.5865      2.992  .0716  0.008354
0.1      0.3494      2.271  .2361  0.003079
0.5      0.1224      2.088  .5661  0.001604
1.0      0.1050      2.068  .6066  0.001561
2.0      0.1052      2.063  .6132  0.001716
5.0      0.1053      2.059  .6177  0.001662
```

By 0.5E rewiring the nonlinear relation fell to ~19% of GEO and then remained on a small generic-graph floor.

But preregistered `rho(clustering, |interaction|) >= .60` observed only `+0.575`, so Gate 3 is **FAIL**. Spectral-gap anticorrelation passed (`-0.679`); mean path length was stronger post-hoc (`+0.720`). None is causal evidence yet.

## Gate 4 — slow mixing is not sufficient

Fresh `340000..340004`, three independent random balanced partitions per cloud = 15 attackers.

Construction:

```text
GEO radial graph
  -> degree+strength-matched non-geometric expander
  -> degree-preserving swaps turn cross-community edges into within-community edges
  -> stop when normalized-Laplacian gap returns near GEO
  -> rematch every node's initial strength
  -> retrain the same histories
```

The random communities are unrelated to xyz and unrelated to the terminal/soma roles.

Fresh receipt:

```text
GEO mean nonlinear interaction        0.007800
EXPANDER recovery                     0.211850

MODULAR mean recovery                 0.223308
MODULAR median recovery               0.209767
MODULAR maximum recovery              0.468354
MODULAR <= 0.50 recovery              15/15

gap ratio MODULAR/GEO                 0.814 .. 1.131
mean gap ratio                        1.006
minimum nonlocal-edge fraction        0.879
maximum clustering/GEO ratio          0.340
maximum node-strength relative error  9.49e-11
all connected / exact degree          yes
```

**Gate 4 PASS.**

Kill:

> low spectral gap / slow global mixing by itself explains the strong relation.

Random modular bottlenecks can reproduce GEO's global slow-mixing scale and still recover only ~22% of the nonlinear relation.

See:

```text
docs/GATE4_RESULT.md
receipts/gate4_low_gap_confirm5.json
```

## Current residual — follow this

The candidate object is increasingly **relational topology**, not a global scalar:

```text
where sources enter
      +
where routes remain separate
      +
where routes are forced to meet
      +
where the soma/readout sits
            ↓
local current history
            ↓
fixed-budget mass redistribution
            ↓
persistent pair relation
            ↓
distributed local nonlinearity
            ↓
interaction
```

Gate 4 says arbitrary bottlenecks elsewhere in the graph are insufficient.

### Immediate next causal attacker: aligned corridors

Construct non-geometric graphs with matched degree/strength and similar broad mixing statistics, but manipulate **alignment to signal traffic**:

```text
ALIGNED
  corridor/community structure deliberately separates the relevant source routes
  and controls where they converge toward soma

MISALIGNED
  same structural recipe/statistics but port identities are permuted relative to it

RANDOM
  Gate-4 style unrelated partition
```

Do not hand-design a dendritic answer too strongly. Prefer an algorithmic construction from port distances / graph distances, then attack it with role permutation.

Question:

> Does matching topology to the signal boundary conditions recover the strong relation without Euclidean coordinates?

If yes, Sunday has isolated something closer to a dendritic primitive: **computation by arranging where signals stay distinct and where they may interact**.

If no, kill this alignment hypothesis and move on.

### Composition gate after the topology mechanism

Once the topology residual is clearer, ask whether one fixed mass budget can store several pair relations at once and expose them in a frozen interaction matrix without explicit pair-specific weights. That is closer to an actual calculating primitive than another routing plot.

## Hard stop lines

- total structural mass stays fixed unless a gate explicitly tests growth;
- no explicit pair-specific learned edge weights while claiming morphology stores pair relation;
- renderer is read-only; no pixel recurrence;
- no hand-designed dendritic tree;
- Gate 0 is linear routing;
- Gate 1 is not established Hebbian binding;
- 3-D coordinates are not the current computational primitive;
- Gate 3 did not establish clustering as causal;
- Gate 4 killed slow global mixing as a sufficient explanation;
- no faces, VKITTI, CLIP, oscillations, ferroic memory, QM phase, growth or autonomous visual recurrence until a specific residual calls for them.

## QM / phase side thought

Park it. Current Sunday has no complex phase, tunneling, quantum interference, or exclusion law. If complex/U(1)-like local state is tested later, it must beat a matched two-real-channel control at equal state/parameter/work budget. Do not use it to explain Gate 1 retroactively.

## Feigenbaum note

Still parked. No evidence yet for fractal branching, bifurcation cascades or self-similar morphology. If such structure emerges without being planted, quantify it then.
