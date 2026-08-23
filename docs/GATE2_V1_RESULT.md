# Gate 2 v1 — PASS, with a demotion of the 3-D claim

Date: 2026-08-23

Preregistered confirmation:

```text
seed_start = 300000
seed_count = 12
```

Gate 2 v0 was invalidated before this range because the original explicit-Euler cubic probe overflowed on some rewired attacker graphs. v1 uses 8 response-only substeps for both arms and all confirmation values remained finite.

## Receipt

```text
GEO AB overlap positive fraction          12/12
GEO CD overlap positive fraction          12/12
GEO AB interaction positive fraction      12/12
GEO CD interaction positive fraction      12/12

GEO mean route-overlap separation         0.121534
REWIRE mean |route-overlap separation|    0.018915
GEO / REWIRE route ratio                  6.425x

GEO mean nonlinear interaction separation 0.008661
REWIRE mean |interaction separation|      0.001860
GEO / REWIRE interaction ratio            4.657x

REWIRE AB overlap positive fraction       12/12
REWIRE CD overlap positive fraction       12/12
REWIRE AB interaction positive fraction   12/12
REWIRE CD interaction positive fraction   12/12

GRAPH-SAME max difference                 0.0
all rewires exact degree sequence         yes
all rewires connected                     yes
max initial node-strength rel error       9.82e-11
minimum rewired long-edge fraction        0.872
mean rewired long-edge fraction           0.882
all nonlinear values finite               yes
```

All preregistered thresholds pass.

## The important attacker result

The rewire arm is **not a null**.

It preserves the same qualitative pair relation on every confirmation seed: coactivation history still separates the pair's routes and the fixed distributed nonlinearity still reads that relation as a smaller interaction.

Therefore Sunday must give up the strong story:

> "3-D geometry creates a new calculating primitive."

That is not what Gate 2 shows.

The safer surviving picture is:

> **The relational mechanism is graph-generic in this instrument. Euclidean locality strongly amplifies and regularizes it.**

## Coordinates are not execution-time state

The GRAPH-SAME arm copies the exact geometric `base` matrix and replaces every coordinate with zero. Training, mass allocation, route metrics and nonlinear interaction metrics are exactly identical.

So for the current equations:

```text
xyz -> base graph -> all later computation
```

Once `base` exists, `xyz` is dead metadata.

The exact graph is a sufficient statistic for execution.

This is a decisive demotion of the naive "3-D matter itself calculates" interpretation.

## But locality still matters as an inductive constraint

The stronger attacker does not merely match density. It preserves:

```text
node count
exact unweighted degree of every node
connectivity
initial weighted degree / node strength to <1e-10
```

while repeated edge swaps make about 88% of edges longer than the original Euclidean overlap cutoff.

Under that attack the learned relation remains, but is much weaker:

```text
route relation       ~6.4x stronger in GEO
nonlinear relation   ~4.7x stronger in GEO
```

Thus the live question changes from:

> Is 3-D the computational substance?

into:

> What topological property induced by locality makes relational learning stronger?

Candidates include clustering, path redundancy, separator structure, motifs, local bottlenecks, spectral organization, and the way node-mass plasticity couples to those structures.

Do not choose among these by story. Measure them.

## What is not matched yet

REWIRE-DS does **not** preserve:

- graph spectrum;
- clustering coefficient;
- shortest-path distribution;
- community structure;
- higher-order motifs;
- exact edge-weight multiset after symmetric strength scaling;
- Euclidean edge lengths by design.

Therefore Gate 2 does not identify which geometric/topological statistic causes the amplification.

## Next residual

The most useful next gate is no longer "more 3-D."

It is:

> **Which graph property carries the amplification, and can several learned pair relations compose into an actual discrimination/calculation without explicit pair-specific weights?**

There are two legitimate continuations:

1. **Topology autopsy** — progressively match clustering/spectrum/path statistics until the GEO advantage disappears. This tells us what locality bought.
2. **Composition gate** — train multiple relational histories and ask whether the frozen medium solves a held-out relational task using only local dynamics and node-mass structure.

The second is closer to the original dendrite question; the first is the stricter attacker. Do topology autopsy first or run it in parallel with a very small composition gate.

## Feigenbaum / branching note

Still parked. Gate 2 gives no evidence for fractal or bifurcating morphology. If branching motifs later emerge from the graph/topology autopsy or from growth, quantify them then.
