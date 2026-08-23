# Gate 6 result — relation-matrix composition

Date: 2026-08-23

## Question

> Can one fixed structural mass field store several coactivity relations simultaneously and expose them in a frozen pairwise nonlinear interaction matrix, without explicit pair-specific learned weights?

## Fresh range

```text
380000..380009
```

Six terminals, two disjoint adjacent-edge perfect matchings:

```text
M1: (1,2) (3,4) (5,6)
M2: (2,3) (4,5) (6,1)
```

Each terminal appears exactly once per cycle in both programs. The two matchings have the same adjacent-terminal geometric distance distribution.

Two copies of the identical substrate are trained, one on M1 and one on M2. After freezing, all 15 unordered terminal pairs are probed.

Define:

```text
dI(i,j) = I_T2(i,j) - I_T1(i,j)
```

Expected trained-edge signs:

```text
M1 edge: dI > 0
M2 edge: dI < 0
```

Nine unused pairs have no registered sign.

## Preregistered thresholds

```text
pooled expected-sign fraction                >= 0.90
mean signed trained-edge contrast            >= 0.00070
mean |trained dI| / mean |unused dI|         >= 5.0
pooled shuffle signed-contrast ratio         <= 0.35
```

Fixed mass and finite-state checks are mandatory.

## Receipt

```text
pooled trained-edge expected-sign fraction   1.000  = 60/60
fraction seeds with all 6/6 signs correct    1.000  = 10/10

mean signed trained-edge contrast            0.002666
mean |trained dI|                            0.002666
mean |unused dI|                             0.000217
trained / unused magnitude                   12.303x

mean shuffled signed contrast               -0.000164
pooled shuffle contrast ratio                0.0614
max per-seed shuffle ratio                   0.451
minimum trained signed edge                  0.000125
max structural-mass budget error             5.68e-14
```

**Gate 6: PASS.**

## Per-seed notes

All ten seeds have all six trained-edge signs correct.

The weakest diagnostics are worth preserving:

```text
380003  per-seed shuffle ratio ~0.451
380008  trained/unused |dI| ratio ~3.70
380005  minimum trained signed edge is only ~0.000125
```

The preregistered gate uses pooled shuffle and trained/unused metrics, so these do not fail Gate 6. They show that the strength and spatial specificity of the morphology effect vary substantially by substrate realization even though the trained-edge sign code is remarkably stable.

## What passed

The material is not limited to one relation.

One learned mass distribution can reflect three pair relations simultaneously. Comparing two matched relation programs yields a 15-entry differential interaction matrix in which all six trained edges carry the correct program-specific sign on all ten fresh substrates.

Safe statement:

> **A fixed-budget distributed structural state can simultaneously encode several matched coactivity relations such that a frozen nonlinear pair-interaction matrix distinguishes which relations belonged to which training program, without explicit pair-specific learned weights.**

This is Sunday's first compositional result.

## The mass-shuffle control

Applying the same random permutation to the non-port masses of both trained materials preserves their mass histograms and exact budgets but destroys their placement on the substrate. The pooled signed relation contrast falls to about 6% of the original.

So the relation code is primarily in **where the structural mass sits**, not merely in the histogram of learned mass values.

## The embarrassing attacker: explicit pair table

Do not claim efficiency.

This toy relation task can be stored explicitly with a tiny pair table. Even a full binary table over all 15 unordered pairs needs only 15 bits before ordinary implementation overhead. Sunday uses roughly 249 plastic floating masses plus the fixed graph.

The table therefore wins description length by an absurd margin.

Gate 6 establishes distributed compositional storage/interaction, **not** compression, parameter efficiency, or hardware advantage.

## New residual

The next attacker should ask whether the six-edge matrix is genuinely a distributed relational code or merely a complicated way of assigning each terminal a scalar/local state whose pair score factorizes.

Candidate nulls include:

```text
terminal additive:      dI(i,j) ~= a_i + a_j
terminal multiplicative dI(i,j) ~= a_i a_j
low-rank pair matrix
simple function of endpoint mass / endpoint route strength
```

If a very low-rank endpoint model reconstructs the trained-edge sign matrix, the apparent composition is much less impressive.

Therefore the next gate should attack **pair specificity beyond endpoint factors** before adding more terminals, recurrence, phase, growth, or visual data.
