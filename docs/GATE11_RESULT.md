# Gate 11 result — pre-training semantic routing

Date: 2026-08-23

## Question

Gate 10 suggested that the dormant one-step write geometry selects the relation directions that later become easiest to store. Gate 11 asks whether this can be used **before training** to route a fixed semantic relation onto physical terminals.

Target semantic code is the historically weak Gate-8 `C3`.

Fresh range:

```text
480000..480005
```

## Geometry control

All semantic permutations are reduced to distinct oriented physical relation vectors, then restricted to the exact class where both physical training arms have circular pair-distance multiset

```text
(1,2,2).
```

Exactly **18** assignments remain.

Thus every candidate has:

```text
same six physical terminals
same terminal marginals
three trained pairs per arm
disjoint A/B trained edges
arm-A distances (1,2,2)
arm-B distances (1,2,2)
```

A circular-distance-only model is exactly tied across all candidates.

## Dormant routing score

Before finite training, construct the Gate-10 dormant one-step write matrix `W` and score every candidate relation vector `q` by

```text
s(q) = ||q W||.
```

Register BEST and WORST from this score before measuring finite outcomes.

Then train all 18 assignments independently with the unchanged 40-cycle rule and measure

```text
finite own contrast = (q dot dI) / 6.
```

## Fresh receipt

Per seed:

```text
seed      Pearson   Spearman   shuffled Pearson   shuffled Spearman   BEST contrast   WORST contrast
480000     0.9687     0.9833        -0.1639             -0.2000         0.002386        0.000228
480001     0.9541     0.9333        -0.0264             -0.0500         0.001532        0.000064
480002     0.9255     0.8167         0.1959              0.2667         0.001389        0.000066
480003     0.8717     0.9500         0.1376              0.0667         0.000933        0.000071
480004     0.9381     0.9667        -0.4459             -0.4500         0.001490        0.000204
480005     0.9634     0.9500        -0.3133             -0.0333         0.001541        0.000116
```

Pooled:

```text
mean Pearson(true dormant score, finite contrast)       0.936925
mean Spearman                                           0.933333

mean Pearson(pair-label-shuffled score, finite)        -0.102667
mean Spearman(pair-label-shuffled score, finite)       -0.066667
Pearson advantage                                       1.039592
Spearman advantage                                      1.000000

fresh seeds BEST > WORST                                6/6
mean BEST finite contrast                               0.00154504
mean |WORST| finite contrast                            0.00012465
pooled BEST / |WORST|                                   12.395x

max finite mass-budget error                            5.68e-14
max dormant one-step mass-sum error                     4.54e-14
```

All preregistered blocks pass.

**Gate 11: PASS.**

## Pair-label attacker

The attacker contains the exact same 15 dormant write vectors as the true model. It only permutes which physical terminal pair owns which row of `W`.

Therefore it preserves:

```text
write-vector multiset
row norms
matrix singular values
```

but destroys physical pair ownership.

Its mean fresh correlations are near zero/slightly negative, while the correctly labeled dormant score has Pearson `0.937` and Spearman `0.933`.

So the routing signal is not merely total write magnitude or the singular spectrum of `W`; **which physical pair produces which dormant write trace is load-bearing.**

## Universal-routing diagnostic

A development-average fixed BEST/WORST routing was frozen before fresh evidence but was not a pass/fail block.

Fresh pooled:

```text
substrate-specific dormant-W BEST mean          0.00154504
fixed universal BEST mean                       0.00119589
local / universal BEST                          1.292x

substrate-specific dormant-W WORST mean |.|     0.00012465
fixed universal WORST mean                      0.00016647
```

The universal route is already useful, showing a large family-level preferred routing geometry. Substrate-specific dormant `W` adds a smaller but real average advantage: about 29% on the BEST side and a lower predicted WORST.

Do not claim the local route wins on every individual seed: on `480003` and `480005` the frozen universal BEST happens to achieve slightly higher finite contrast than the local score-selected BEST because the dormant score is predictive, not perfect.

## Safe statement

> **Before finite training, the dormant one-step structural write geometry predicts which geometry-matched physical assignment will make a fixed semantic pair relation more writable. Correct physical pair ownership of the write traces is required, and substrate-specific dormant routing improves on a strong family-level fixed routing on average.**

This converts Sunday's relation-space anisotropy from a post-hoc description into a usable pre-training control signal.

## Important limitation / scar

Gate 11 optimizes **registered signed relation contrast**. It does not guarantee a clean pair code in every other sense.

For example, fresh seed `480003` has BEST trained-vs-unused magnitude only about `0.63x`: its registered relation contrast is strongly improved relative to WORST, yet unused pair responses can still be larger in absolute magnitude.

So Gate 11 establishes control of writability, not universal selectivity or task-ready semantic decoding.

## Next residual

There are now two genuinely different next questions.

### 1. Mechanism of the dormant write score

What graph property predicts `W` and therefore the routing ranking without simulating teacher episodes?

Candidate mechanisms must face the now-observed complete 18-route ranking, not just BEST/WORST:

```text
terminal-to-soma current-flow overlap
pairwise corridor overlap
Laplacian / diffusion embedding
community-boundary incidence
local bottleneck placement
```

Gate 3 already blocks a clustering-only story and Gate 4 blocks a low-gap-only story.

### 2. Can routing improve selectivity, not only contrast?

Use dormant write **and read** information to select assignments by a pre-training objective that predicts both:

```text
registered own contrast
unused-edge leakage
```

A successful gate would turn C3 from merely stronger into a cleaner relation code, while keeping all candidate geometry matched.

The second route is closer to practical computation; the first is closer to explaining why Sunday works.
