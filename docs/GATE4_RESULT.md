# Gate 4 result — low-gap non-geometric attacker

Date: 2026-08-23

## Question

Gate 3 suggested, post-hoc, that slow mixing / low normalized-Laplacian gap might be the reason geometric locality amplifies the Gate-1 pair relation.

Gate 4 attacks that explanation directly:

> If a highly non-geometric graph is given a spectral gap comparable to the geometric graph, does the strong learned nonlinear pair relation return?

## Preregistered construction

Fresh seeds:

```text
340000..340004
```

For each seed:

1. build the original Euclidean radial-cutoff graph (`GEO`);
2. build the Gate-2 degree+strength-matched non-geometric rewire (`EXPANDER`);
3. for three independent balanced random node partitions, convert cross-community edges into within-community edges with degree-preserving similar-weight swaps until the normalized-Laplacian gap returns near GEO;
4. re-match every node's initial weighted degree / strength;
5. retrain the same matched Gate-1 histories;
6. measure the same stable distributed nonlinear interaction.

The random communities are unrelated to xyz and unrelated to the A/B/C/D/soma roles.

Preregistered validity bounds:

```text
GEO mean interaction              >= 0.0015
strength relative error           < 1e-8
modular/GEO gap ratio             0.60 .. 1.25
minimum nonlocal-edge fraction    >= 0.75
maximum clustering/GEO ratio      <= 0.45
```

Preregistered slow-mixing insufficiency receipt:

```text
mean modular recovery             <= 0.50
fraction of attackers <= 0.50     >= 0.70
```

## Fresh receipt

Five clouds x three random partitions = 15 low-gap modular attackers.

```text
GEO mean nonlinear interaction        0.007800
EXPANDER mean recovery                 0.211850

MODULAR mean recovery                  0.223308
MODULAR median recovery                0.209767
MODULAR maximum recovery               0.468354
MODULAR recovery <= 0.50               15/15 = 1.00

MODULAR/GEO spectral-gap ratio         0.814 .. 1.131
mean gap ratio                         1.006
minimum nonlocal-edge fraction         0.879
mean nonlocal-edge fraction            0.888
maximum clustering/GEO ratio           0.340
mean clustering/GEO ratio              0.315
maximum node-strength relative error   9.49e-11
all connected                          yes
all exact degree                       yes
all nonlinear values finite            yes
```

Per-seed modular recovery fractions:

```text
340000: 0.109  0.328  0.271
340001: 0.272  0.125  0.468
340002: 0.250  0.253  0.127
340003: 0.086  0.177  0.460
340004: 0.067  0.210  0.147
```

**Gate 4: PASS.**

## Interpretation

Kill the simple explanation:

> The geometric graph is strong because it mixes slowly / has a small spectral gap.

A random non-geometric modular graph can be made just as slow-mixing globally while preserving exact degree and initial node strength, yet it recovers only about 22% of GEO's nonlinear relation on average.

Therefore low global mixing is **not sufficient**.

The current residual is more local and relational:

> The useful topology may have to place corridors, bottlenecks, and meeting regions in relation to where signals actually enter and leave, rather than merely possessing a favorable global statistic.

This does not establish that Euclidean geometry is necessary. Gate 2 already killed that claim. It says only that the random modular surrogate fails to reproduce the particular topology induced by locality that matters to this learning rule.

## Next falsifier

Do not search more global scalar graph statistics first.

Construct matched non-geometric graphs whose corridor/community layout is deliberately **aligned** or **misaligned** with the terminal-to-soma traffic, while preserving degree, node strength, and comparable global mixing as tightly as practical.

If signal-aligned non-geometric topology recovers the GEO relation while an otherwise matched misaligned topology does not, then Sunday has isolated a more specific primitive:

> topology determines where signals remain separate and where they are allowed to meet; local plasticity writes relations into that arrangement.

If alignment does not recover the effect, this hypothesis dies too.
