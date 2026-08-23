# Gate 3 prereg — topology / locality dial

Date: 2026-08-23

## Residual from Gate 2

Gate 2 established two things at once:

1. the exact graph is sufficient after construction; coordinates themselves are not execution-time state;
2. the Gate-1 pair relation survives on non-geometric degree+strength-matched rewires, but is much weaker.

Gate 3 asks:

> **Which broad topological change accompanies the loss of the relational effect as Euclidean locality is progressively destroyed?**

This is an autopsy / candidate-finding gate, not yet a causal identification gate.

## Cleaner locality dial

A naive partial rewire would randomize all edge weights even at tiny rewire levels. Gate 3 must not do that.

Start from the normal geometric base graph. Perform a single nested trajectory of degree-preserving double-edge swaps. Candidate edge pairs may swap only when their carried weights are similar:

```text
abs(log(w1 / w2)) <= 0.12
```

The weights travel with their edge slots. At each snapshot, apply symmetric diagonal scaling to match every node's original weighted degree / strength to relative error `< 1e-8`.

Thus a small topology change is also a small weight reassignment before the final strength correction.

## Rewire levels

Let `E` be the geometric undirected edge count. Snapshot the same nested rewire trajectory at:

```text
0.0 E
0.1 E
0.5 E
1.0 E
2.0 E
5.0 E
```

`0.0 E` is the untouched geometric graph.

Every snapshot must preserve:

```text
node count
exact unweighted degree sequence
connectivity
initial node strength to <1e-8 relative error
```

## Learning and probe

Use the unchanged Gate-1 matched histories:

```text
H_AB: [A+B], [C], [D]
H_CD: [C+D], [A], [B]
```

Use Gate-2 v1's stable nonlinear response probe:

```text
8 response-only substeps per original dt
same total simulated time
same total drive duration
```

No new learned parameters.

## Graph measurements at every level

Measure before learning:

```text
fraction of edges longer than original Euclidean cutoff
mean local clustering coefficient
transitivity
mean unweighted shortest-path length
normalized-Laplacian lambda_2 (spectral gap)
```

Measure after the two histories:

```text
mean AB/CD route-overlap separation
mean AB/CD distributed nonlinear-interaction separation
```

## Frozen fresh range

```text
seed_start = 320000
seed_count = 6
```

Consumed Gate-2 and exploratory seeds are not confirmation.

## Frozen checks

The first consumed exploratory dial showed a sharp early collapse rather than strict monotonicity all the way to 5E, so Gate 3 does **not** preregister a monotone-every-step claim.

Across the fresh confirmation set require:

```text
all snapshots connected                              true
all degree sequences exact                          true
max node-strength relative error                    < 1e-8
all nonlinear values finite                         true

GEO mean route separation                           >= 0.04
GEO mean interaction separation                     >= 0.0015

mean clustering at 0.5E / GEO clustering            <= 0.60
mean |interaction| at 0.5E / GEO |interaction|      <= 0.65
mean |interaction| at saturated (2E,5E) / GEO       <= 0.50

pooled Spearman(clustering, |interaction|)           >= +0.60
pooled Spearman(norm-Laplacian gap, |interaction|)   <= -0.60
```

The pooled correlation contains 6 seeds x 6 levels = 36 points. Seed identity is not removed; this is a descriptive topology dial, not an independence proof.

## Interpretation stop line

Even if every check passes, do **not** say clustering is causal.

Clustering, path length, long-edge fraction, spectral gap, motifs and separator structure all co-vary under this dial.

A Gate-3 pass means only:

> As local geometric topology is destroyed under fixed degree and node strength, the learned pair effect collapses toward the generic-graph floor, and that collapse tracks a clustered/local versus expander-like topology axis.

The next causal attacker would need to preserve the leading candidate statistic while breaking the others.

## Exploratory calibration that may not be used as confirmation

One consumed seed gave approximately:

```text
swaps/E  clustering  long edges  gap    nonlinear effect
0.0      0.587       0.000       .073   .00948
0.1      0.343       0.182       .253   .00414
0.5      0.123       0.598       .562   .00226
1.0      0.110       0.780       .610   .00040
2.0      0.111       0.861       .614   .00180
5.0      0.115       0.877       .612   .00179
```

This motivated the thresholds. It is not evidence for Gate 3.
