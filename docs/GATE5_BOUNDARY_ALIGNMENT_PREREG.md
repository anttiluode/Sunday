# Gate 5 preregistration — boundary-condition alignment

Date: 2026-08-23

## Residual from Gate 4

Gate 4 killed the claim that low global mixing is sufficient. Random non-geometric modular graphs were matched back to the geometric graph's spectral-gap scale but recovered only ~22% of the Gate-1 nonlinear pair relation on average.

The next causal question is more specific:

> **Does the same topology become a better relational machine when the input roles are aligned with its corridor/community structure?**

This gate changes **boundary conditions only** between the primary arms. The graph itself is identical.

## Fresh range

```text
360000..360007
```

Eight independent clouds. These seeds have not been used in Gates 0–4 or in Gate-5 calibration.

## Graph construction

For each seed:

1. build the ordinary geometric radial-cutoff graph;
2. build the degree+strength-matched non-geometric rewire from Gate 2;
3. choose deterministically the first random balanced Gate-4 partition whose four physical terminal nodes split exactly 2+2 between the two communities;
4. impose that partition using the Gate-4 low-gap modular construction;
5. freeze the resulting graph.

Validity requirements remain:

```text
connected                         yes
exact unweighted degree           yes
node-strength relative error      < 1e-8
MODULAR/GEO spectral-gap ratio    0.60 .. 1.25
nonlocal-edge fraction            >= 0.75
clustering/GEO ratio              <= 0.45
```

## The three pairings

The physical input nodes are fixed indices 1,2,3,4. There are only three perfect pairings:

```text
P0: (1,2) | (3,4)
P1: (1,3) | (2,4)
P2: (1,4) | (2,3)
```

Because the graph partition is 2+2, exactly one pairing puts both pairs *within* communities. Call it `ALIGNED`.

The other two put both pairs *across* the community boundary. Call them `CROSSED-1` and `CROSSED-2`.

For each pairing, reinterpret its first pair as semantic AB and second pair as semantic CD and run the same matched Gate-1 histories:

```text
H_AB: [A+B], [C], [D]
H_CD: [C+D], [A], [B]
```

No edge, edge weight, graph statistic, node mass budget, learning rule, nonlinear probe, or physical terminal node changes between the three pairing conditions. Only which physical terminals are declared to be coactive semantic pairs changes.

## Primary metric

For each frozen graph:

```text
I_aligned = mean nonlinear interaction separation for ALIGNED
I_cross   = mean of the two crossed-pairing interaction separations
alignment_gain = I_aligned / max(I_cross, eps)
```

Use signed interaction separations in the means. Report absolute values as diagnostics but do not silently switch the primary metric after seeing results.

## Preregistered receipt

Gate 5 passes only if all validity checks pass and:

```text
mean I_aligned                         >= 0.0015
fraction(I_aligned > I_cross)          >= 0.75
fraction(I_aligned > both crosses)     >= 0.75
mean(I_aligned) / mean(I_cross)        >= 1.50
```

Additionally report the same comparison for linear route separation, but it is secondary and has no pass/fail threshold.

If `mean(I_cross)` is non-positive, the ratio alone is not accepted as evidence; the absolute aligned threshold and graph-wise fractions still control the gate.

## Interpretation if PASS

Safe statement:

> On an identical fixed non-geometric graph, local plasticity writes a stronger pair relation when the semantic coactivity boundary conditions align with the graph's community/corridor layout than when the same input roles are crossed over that layout.

This would support **signal/topology alignment** as part of the primitive.

It would *not* establish biology, dendrites generally, Euclidean necessity, optimality, or a universal graph law.

## Interpretation if FAIL

Kill the coarse community-alignment hypothesis. Do not rescue it by choosing a different pairing after seeing fresh results.

A failure would mean Gate 4's residual is more detailed than two-community boundary alignment, or that the locality advantage comes from another property entirely.

## Calibration provenance

The protocol was chosen after consumed Gate-4 graphs showed ALIGNED > both CROSSED pairings on six checked 2+2 graphs. Those consumed results are engineering calibration only and are not counted in Gate 5.
