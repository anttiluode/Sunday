# Gate 2 prereg — abstract graph attacker

Date: 2026-08-23

## Question

Gate 1 showed that matched coactivation histories can write a pair relation into a fixed-material transfer medium. But the current dynamics use the 3-D coordinates only to construct a fixed base conductance graph. After that, all fast dynamics and slow mass learning operate on the graph.

Gate 2 asks two separate questions:

1. **Necessity:** are Euclidean 3-D coordinates themselves required by the current mechanism after the graph exists?
2. **Inductive constraint:** even if coordinates are not required at execution time, does a locality-generated graph make the learned relational effect substantially stronger or more reproducible than a non-geometric graph with matched coarse resources?

Do not merge these questions. A graph can be a sufficient statistic while 3-D locality is still a useful way to constrain/generate that graph.

## Arms

For each seed, construct one 256-element cloud and its normal geometry graph.

### GEO

The existing Gate-1 base graph:

```text
xyz -> radial overlap kernel + cutoff -> base conductance graph
```

### GRAPH-SAME

Copy the exact `base` matrix, erase/scramble the coordinates, and run the same learning and probing.

Expected result: bit/numerical identity. If not, some hidden coordinate dependence exists and the implementation must be audited.

This arm is the necessity attacker. If GRAPH-SAME is identical to GEO, the safe statement is:

> The present dynamics do not require coordinates after graph construction.

### REWIRE-DS

Start from the GEO graph, then destroy Euclidean adjacency with repeated double-edge swaps while preserving:

```text
number of nodes
exact unweighted degree of every node
connectivity when possible
```

Initialize rewired edge weights from the geometric weight multiset, then apply symmetric diagonal scaling until every node's initial weighted degree / strength matches the GEO graph to relative error < 1e-8.

Thus this attacker preserves much more than edge density. It deliberately does **not** preserve higher-order topology, Euclidean locality, edge-length distribution, graph spectrum, or the exact edge-weight multiset after strength scaling.

That limitation must be stated with any result.

## Histories and readout

Use the unchanged Gate-1 histories:

```text
H_AB: [A+B], [C], [D]
H_CD: [C+D], [A], [B]
```

Each terminal occurs exactly once per cycle in both programs.

Measure for both GEO and REWIRE-DS:

```text
AB route-overlap separation
CD route-overlap separation
AB distributed-nonlinear interaction separation
CD distributed-nonlinear interaction separation
```

Positive sign has the same meaning as Gate 1: the coactive pair became less route-overlapping / less interacting than the same pair under the opposite history.

## Frozen confirmation thresholds

These thresholds are registered before the held-out Gate-2 confirmation range.

```text
GEO overlap positive fraction           >= 0.90 for each pair
GEO interaction positive fraction       >= 0.90 for each pair
GEO mean overlap separation             >= 0.04
GEO mean interaction separation         >= 0.0015

GRAPH-SAME max state/metric difference  < 1e-12

REWIRE initial degree sequence           exact
REWIRE initial node-strength rel error  < 1e-8
REWIRE long-edge fraction               >= 0.50

GEO / REWIRE mean overlap ratio         >= 3.0
GEO / REWIRE mean |interaction| ratio   >= 2.0
```

The rewire arm is *not* required to have zero effect. In fact, exploratory work already showed a smaller relation on generic sparse graphs. Gate 2 is testing whether locality is an amplifier/constraint, not whether abstract graphs are incapable of the phenomenon.

If REWIRE matches or beats GEO under these controls, demote the 3-D locality story strongly.

## Exploratory calibration already seen before prereg

These values motivated the thresholds and are **not confirmation data**.

A simple random sparse graph with exact edge count and exact weight multiset gave, over 10 exploratory clouds, mean route separation around `0.0106` versus Gate 1's stored GEO mean `0.116`, and mean nonlinear separation around `0.00149` versus `0.00895`.

A stronger degree+strength matched rewire gave, over 8 exploratory clouds, mean pair route separations around `0.0185 / 0.0147`; interaction signs were less stable than GEO.

Do not cite those exploratory values as the Gate-2 receipt.

## Interpretation stop lines

Even if Gate 2 passes:

- do not say 3-D is computationally necessary;
- do not say the effect is unique to geometric graphs;
- do not claim a hardware or energy advantage from software description length;
- do not claim the current random cloud is dendritic morphology;
- do not treat a graph-spectrum mismatch as irrelevant.

The strongest possible Gate-2 statement is narrower:

> For this learning rule, Euclidean locality is not required after graph construction, but it acts as an inductive topological constraint under which the relational effect is stronger/more reliable than under a degree- and strength-matched non-geometric rewire.
