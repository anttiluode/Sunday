# Gate 4 prereg — low-gap non-geometric attacker

Date: 2026-08-23

## Residual

Gate 3 failed to establish clustering as the leading descriptive statistic. Its preregistered spectral-gap anticorrelation passed, and post-hoc mean path length tracked the effect strongly.

That suggests a broad hypothesis:

> local geometry helps because it produces slow-mixing / corridor-like graphs in which signals retain route identity long enough for fixed-budget local plasticity to sculpt relations.

Gate 4 attacks the **sufficiency** of slow mixing.

## Three graph arms

For each base seed:

### GEO

Normal 3-D radial-overlap graph.

### EXPANDER

Gate-2 degree+strength-matched full non-geometric rewire. This is the high-gap / rapidly mixed baseline.

### MODULAR-NONGEO

Start from EXPANDER. Draw a random balanced binary partition of all nodes, independent of xyz and independent of port identities.

Repeatedly choose two cross-community edges with similar carried weights:

```text
abs(log(w1 / w2)) <= 0.20
```

and degree-preserving-swap them into two within-community edges when legal. This reduces the random cut while preserving every node's unweighted degree exactly.

Every 20 accepted swaps, symmetrically rescale edge weights to match every node's original GEO strength. Stop at the first connected graph satisfying:

```text
normalized-Laplacian gap <= 1.15 * GEO gap
```

The random partition is never given to learning or readout; it is only a graph-construction device.

## Multiple partitions

For each base seed build:

```text
3 independent random partitions
```

This reduces dependence on one accidental assignment of soma/ports to communities.

## Required attacker validity

For every modular graph:

```text
connected                                      true
exact unweighted degree sequence               true
node-strength relative error                   < 1e-8
gap ratio MODULAR/GEO                          between 0.60 and 1.25
long-edge fraction in original xyz             >= 0.75
clustering ratio MODULAR/GEO                   <= 0.45
all nonlinear values finite                    true
```

Thus the attacker restores low gap while remaining strongly non-geometric and much less clustered than GEO.

## Learning and readout

Use unchanged Gate-1 matched histories and Gate-2's stable 8-substep nonlinear probe.

No community labels, pair weights, learned edges or extra state.

Primary per-partition quantity:

```text
recovery = abs(MODULAR mean nonlinear pair separation)
           / abs(GEO mean nonlinear pair separation)
```

Also record EXPANDER recovery, route separation, graph statistics and the random community assignments of the five ports for audit.

## Fresh confirmation range

```text
seed_start = 340000
seed_count = 5
partitions_per_seed = 3
```

Total modular attackers: 15.

## Frozen hypothesis and thresholds

Exploratory consumed seeds showed low-gap modular/GEO interaction ratios near `-0.01, 0.08, 0.28`; these motivated but do not count toward the gate.

Gate 4 asks whether **slow mixing is sufficient**. The registered hypothesis is that it is not.

Require:

```text
GEO mean nonlinear separation                       >= 0.0015
all modular attacker validity checks                 pass

mean modular nonlinear recovery                     <= 0.50
fraction of modular partitions with recovery <= .50 >= 0.70
```

If mean recovery is > 0.75, the slow-mixing hypothesis receives strong support instead and Gate 4 fails its registered direction.

Values between 0.50 and 0.75 are also a gate failure/inconclusive result; do not move thresholds after seeing them.

## Interpretation stop line

A Gate-4 pass would **not** prove port-aligned corridors are the answer. It would establish only:

> Matching a global slow-mixing statistic with random non-geometric modular structure is insufficient to restore the strong relation.

That would push the residual toward **where bottlenecks/corridors sit relative to sources, sink and local plasticity**, or toward a richer local structural statistic.

A Gate-4 failure with strong recovery would instead demote geometry further: low-gap modular topology would be enough.
