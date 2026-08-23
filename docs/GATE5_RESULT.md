# Gate 5 result — boundary-condition alignment

Date: 2026-08-23

## Question

Gate 4 showed that random slow-mixing modular topology is insufficient. Gate 5 asks a more causal question:

> **On the exact same frozen non-geometric graph, does local plasticity write a stronger pair relation when semantic coactivity roles align with the graph's community/corridor layout?**

## Fresh confirmation

```text
360000..360007
```

For every seed the graph is frozen before comparing conditions. The four physical terminal nodes admit exactly three perfect pairings. Because the modular graph is constructed with a 2+2 terminal split, one pairing lies wholly within the two communities (`ALIGNED`) and the other two cross the community boundary (`CROSSED`).

No edge, weight, degree, node strength, spectral gap, clustering value, 3-D coordinate, mass budget, learning rule, or nonlinear probe changes between these three conditions. Only the semantic assignment of A/B/C/D coactivity roles to the same physical terminal nodes changes.

## Preregistered thresholds

```text
mean ALIGNED interaction                  >= 0.0015
fraction ALIGNED > crossed mean           >= 0.75
fraction ALIGNED > both crosses           >= 0.75
mean ALIGNED / mean crossed               >= 1.50
```

Graph validity:

```text
strength relative error                   < 1e-8
gap ratio                                 0.60 .. 1.25
nonlocal-edge fraction                    >= 0.75
clustering/GEO ratio                      <= 0.45
connected + exact degree                  required
```

## Receipt

```text
mean ALIGNED nonlinear interaction        0.002379
mean CROSSED nonlinear interaction        0.000548
mean alignment ratio                      4.340x
ALIGNED > crossed mean                    7/8 = 0.875
ALIGNED > both crossed pairings           7/8 = 0.875

mean ALIGNED linear route separation      0.034871
mean CROSSED linear route separation      0.015749
route alignment ratio                     2.214x

spectral-gap ratio range                  0.865 .. 1.112
minimum nonlocal-edge fraction            0.866
maximum clustering/GEO ratio              0.354
maximum node-strength relative error      9.85e-11
all connected / exact degree / finite     yes
```

**Gate 5: PASS.**

## Per-seed nonlinear receipt

```text
seed      ALIGNED       crossed mean    gain
360000    +0.004324     +0.000610       7.08x
360001    +0.003149     +0.000635       4.96x
360002    -0.003315     +0.000653      -5.07x   <-- reversal
360003    +0.000065     +0.000001      54.33x   <-- nearly silent graph
360004    +0.004893     +0.000473      10.34x
360005    +0.004101     +0.000498       8.23x
360006    +0.002874     +0.000840       3.42x
360007    +0.002938     +0.000673       4.37x
```

Do not hide `360002`. It matters.

On that seed alignment still strengthened the *linear route separation* (`0.03945` aligned vs `0.01918` crossed mean), but the distributed cubic readout changed sign. Therefore topology/boundary alignment controls the routes more reliably than it determines the final sign of this particular nonlinear readout.

Likewise `360003` is nearly silent in route separation; its enormous ratio is denominator-driven and is not evidence of a huge absolute effect.

## Interpretation

What survives:

> **Boundary conditions matter. The same graph can support a substantially stronger learned pair relation when the coactivity semantics are aligned with its internal modular/corridor layout.**

That is stronger than Gate 4's graph-statistic observations because the primary comparison changes no graph property at all.

A useful current picture is:

```text
fixed topology
   + where signals enter
   + which signals arrive together
           ↓
local current pattern
           ↓
fixed-budget mass plasticity
           ↓
persistent route relation
           ↓
local nonlinear readout
```

This is closer to the artificial-dendrite question than "3-D splats compute." Biological-style relevance, however, remains only an analogy: Sunday has not established a biological mechanism.

## What Gate 5 does not establish

- community alignment is not sufficient to fix the sign of nonlinear computation;
- the cubic readout is not unique or biologically privileged;
- the topology is not proven optimal;
- 3-D coordinates remain unnecessary after graph construction;
- this is still a pair relation, not yet a general calculating unit.

## Next gate

Stop dissecting one pair forever. Ask whether the substrate can **compose** relations.

Can one fixed material budget experience several pair statistics and later expose a structured pairwise interaction matrix, without explicit pair-specific learned weights?

That is the next step toward deciding whether this is a calculating primitive rather than a succession of elegant routing effects.
