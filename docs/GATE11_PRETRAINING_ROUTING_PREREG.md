# Gate 11 preregistration — pre-training semantic routing

Date: 2026-08-23

## Question

Gate 10 showed that the dormant one-step write geometry already contains most of the preferred **input** relation modes of the eventual finite-training operator.

Gate 11 turns that post-hoc clue into a control test:

> **Can the dormant substrate, before finite training, predict how to assign a fixed semantic relation to physical terminals so that the relation will later be written strongly?**

The target semantic relation is fixed before fresh evidence to the historically weak Gate-8 code `C3`:

```text
semantic arm A: (1,3) (2,5) (4,6)
semantic arm B: (1,4) (2,6) (3,5)
```

No graph, learning rule, mass budget, readout, or training schedule changes.

## Development / calibration provenance

Consumed development substrates:

```text
470000..470002
```

They are not Gate-11 evidence.

The unrestricted semantic permutations collapse to 120 distinct oriented physical relation vectors. To remove the easy ring-distance explanation, Gate 11 uses only the exact geometry-equivalence class in which **both** physical training arms have circular pair-distance multiset

```text
(1, 2, 2).
```

Exactly **18** distinct oriented assignments satisfy this condition.

On development, using all 18 assignments per substrate:

```text
seed      Pearson(score, finite contrast)   Spearman   finite BEST/WORST
470000              0.95899                  0.9000         71.07x
470001              0.94639                  0.9000          3.64x
470002              0.93589                  0.8667          4.94x
```

The pooled mean BEST contrast is about `6.98x` the pooled mean absolute WORST contrast.

A pair-label shuffle attacker was also frozen before fresh evidence. Apply one deterministic permutation to the **15 rows** of the dormant write matrix `W`, thereby preserving the complete set of write vectors, row norms, singular values and row-vector Gram structure but scrambling which physical terminal pair owns which write trace.

Development shuffled-score Pearson correlations are:

```text
470000   -0.02598
470001   -0.17753
470002   -0.27151
```

and Spearman correlations are `-0.1500, -0.1167, -0.3667`.

These development values are used only to set the generous thresholds below.

## Fresh range

```text
480000..480005
```

Six independent random substrates. No Gate-10 or Gate-11 development seed is reused.

## Dormant write matrix

For each fresh physical substrate, before any finite training, construct exactly the Gate-10 one-step write matrix

```text
W : 15 physical terminal pairs x 256 mass coordinates
```

where each row is the mass displacement caused by one existing teacher episode plus one existing redistribution update from uniform dormant mass.

No finite-training output is used to construct `W`.

## Fixed candidate set

Consider all mappings of semantic terminal labels `1..6` onto physical terminal labels `1..6`.

For each mapping:

1. map the fixed semantic C3 arm A/B pairs onto physical pairs;
2. construct the oriented 15-edge physical relation vector

```text
q_e = +1   physical edge belongs to mapped arm A
      -1   physical edge belongs to mapped arm B
       0   otherwise;
```

3. remove duplicate physical `q` vectors;
4. retain only mappings for which

```text
distance_multiset(arm A) == (1,2,2)
distance_multiset(arm B) == (1,2,2).
```

Required candidate count:

```text
18
```

Every retained candidate therefore has exactly the same terminal marginals, same number of trained pairs, disjoint A/B edges, and the same physical circular-distance multiset in both arms.

A geometry-only score based on these circular distances is exactly tied across all 18 candidates and cannot rank them.

## Pre-training routing score

For every retained assignment compute only

```text
s(q) = || q W ||_2.
```

Interpretation: `q W` is the one-step dormant mass displacement produced by the semantic contrast when routed through that physical assignment. The score asks only how strongly the dormant write stage can separate the two semantic histories.

Before finite training, rank all 18 assignments by `s(q)` and register:

```text
BEST  = argmax s(q)
WORST = argmin s(q).
```

No finite readout information enters this ranking.

## Finite target

After all dormant rankings are frozen, train **all 18** candidate assignments independently using the unchanged 40-cycle Sunday training rule.

For each assignment freeze learning, measure all 15 nonlinear pair interactions, and compute

```text
y = interaction(B-trained material) - interaction(A-trained material)
finite own contrast = (q dot y) / 6.
```

Also report trained-edge sign fraction and trained-vs-unused absolute magnitude as diagnostics.

Because all 18 finite outcomes are measured, Gate 11 tests the complete ranking rather than only two hand-picked extrema.

## Primary receipt

Per fresh seed, compute across all 18 assignments:

```text
Pearson correlation(s(q), finite own contrast)
Spearman correlation(s(q), finite own contrast)
finite own contrast of preregistered BEST
finite own contrast of preregistered WORST
```

Pooled metrics:

```text
mean Pearson
mean Spearman
fraction seeds BEST > WORST
mean BEST contrast / mean absolute WORST contrast
```

## Attacker — shuffled physical pair ownership of W

For each fresh seed create a deterministic row permutation

```text
rng seed = 990000 + substrate_seed
W_shuffle = W[row_permutation]
```

The same 256-dimensional write vectors remain present; only their physical pair labels are scrambled.

Score the same 18 candidate assignments with

```text
s_shuffle(q) = || q W_shuffle ||.
```

Report Pearson and Spearman correlation of this shuffled score with the already measured finite outcomes.

This attacker is stronger than a random-number ranking because it preserves the empirical write-vector distribution and the entire matrix singular spectrum. It destroys only which physical pair owns which dormant structural response.

## Development-frozen universal routing diagnostic

For diagnosis only, freeze the development-average BEST and WORST physical relation vectors:

```text
UNIVERSAL_WORST = (0,-1,0,1,0, 1,-1,0,0, 0,0,0, 0,1,-1)
UNIVERSAL_BEST  = (-1,1,0,0,0, 0,1,0,0, 0,-1,0, 0,-1,1)
```

Entries are in the repository's `ALL_PAIRS` order.

Report their finite fresh outcomes alongside substrate-specific dormant-W BEST/WORST. **This diagnostic is not a pass/fail block.** If universal routing performs almost as well, the useful writable ranking is largely common to this graph family; if substrate-specific W improves on it, there is additional instance-specific control value.

## Controls

- same six physical terminals and same seeded graph within all candidate arms;
- fixed semantic target C3;
- candidate set frozen by exact `(1,2,2)/(1,2,2)` geometry class;
- candidate count exactly 18;
- exact terminal marginals;
- disjoint A/B trained edges;
- fixed total structural mass;
- dormant score computed before finite training;
- no finite readout or Gate-9/10 operator used in the primary routing score;
- all finite outcomes measured only after ranking;
- deterministic pair-label shuffle attacker;
- all values finite.

## Preregistered receipt

Primary complete-ranking prediction:

```text
mean fresh Pearson correlation             >= 0.70
mean fresh Spearman correlation            >= 0.65
```

Preselected extrema:

```text
fraction fresh seeds with BEST > WORST     >= 5/6
pooled mean BEST / mean |WORST| contrast   >= 2.5
```

Pair-label ownership attacker:

```text
mean Pearson(true score) -
mean Pearson(shuffled score)               >= 0.40

mean Spearman(true score) -
mean Spearman(shuffled score)              >= 0.35
```

Design / conservation:

```text
candidate count                            = 18
all candidates arm-A distances             = (1,2,2)
all candidates arm-B distances             = (1,2,2)
all terminal marginals matched
all A/B edge sets disjoint
max trained mass-budget error              < 1e-10
all values finite
```

**Gate 11 passes only if every block above passes.**

## Interpretation if PASS

Safe statement:

> The dormant one-step structural write geometry predicts, before training and beyond circular terminal distance, which physical assignment will make a fixed semantic pair-relation more writable under the unchanged finite learning rule.

This would turn Sunday's anisotropic relation geometry from a descriptive property into a pre-training routing/control signal.

Do not automatically call the control substrate-specific: the frozen universal-routing diagnostic determines how much of the advantage is shared across the graph family.

## Interpretation if FAIL

Failure location matters:

- weak full-ranking correlation but BEST > WORST: dormant score may only identify extremes, not continuously predict writability;
- strong correlation but poor BEST/WORST ratio: score is predictive but practically weak;
- shuffled labels correlate similarly: physical pair ownership of write traces is not the useful information;
- universal routing equals local routing: control is mostly family-level rather than instance-specific;
- all ranking fails: Gate-10 write-mode alignment was post-hoc/descriptive and is not actionable.

Do not tune the learning rule or candidate geometry to rescue this gate.
