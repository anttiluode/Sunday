# Gate 12 preregistration — read-aware pre-training routing

Date: 2026-08-23

## Question

Gate 11 showed that dormant one-step **write** geometry can route a semantic relation into a physical assignment that later writes a stronger registered contrast. Its scar is equally clear: maximizing `||qW||` does not guarantee a clean relation readout. One fresh Gate-11 BEST had trained/unused magnitude only `0.631x`.

Gate 12 asks:

> **Does the dormant write+read operator contain enough pre-training information to choose a physical assignment that is both strong and directionally clean, beyond what write strength or predicted contrast alone can choose?**

No physical mechanism changes. The target semantic code is still Gate-8 C3 and the candidate set is still Gate 11's exact 18-member geometry-equivalent routing class.

## Development / calibration provenance

Consumed development seeds:

```text
490000..490003
```

They are not Gate-12 evidence.

The local accelerated implementation was first validated against archived Gate-11 seed `480000`; it reproduced the registered BEST `R07`, write score `0.30310939797722`, finite contrast `0.00238565028709`, and trained/unused ratio `1.599645` to numerical precision before any development result was used.

On development, the read-aware route beat the Gate-11 write-only BEST in finite clean utility on `4/4` substrates, with per-seed ratios approximately:

```text
1.33, 1.22, 1.35, 1.09
```

The read-aware predicted utility versus finite utility Pearson correlations were:

```text
0.950, 0.985, 0.966, 0.950
```

and Spearman correlations were approximately:

```text
0.926, 0.845, 0.948, 0.851
```

These development values are used only to freeze the generous thresholds below.

## Fresh range

```text
500000..500005
```

Six independent random substrates.

## Candidate class — unchanged from Gate 11

All 18 candidates are semantic-to-physical assignments of C3 satisfying exactly:

```text
arm A circular pair-distance multiset = (1,2,2)
arm B circular pair-distance multiset = (1,2,2)
identical terminal marginals
three disjoint trained pairs in each arm
same six physical terminals
same training count, mass budget and dynamics
```

Therefore circular distance alone ties all 18 candidates exactly.

## Dormant predictor

For each fresh substrate, before finite training:

1. build the 15 pair-specific one-step structural write matrix `W` from uniform dormant mass;
2. measure the dormant nonlinear directional read derivative `D` along those same write directions using the already registered Gate-10 central difference `epsilon=0.25`;
3. define the dormant relation operator

```text
B0 = -D
```

No Gate-10 global amplitude gain is needed for routing because every candidate on one substrate would receive the same positive scalar.

For physical code vector `q`, predict the complete 15-pair response

```text
y0(q) = q B0.
```

## Registered clean utility

For any target code `q` and response `y`, define

```text
contrast(q,y) = (q . y) / 6
cosine(q,y)   = (q . y) / (||q|| ||y||)

U(q,y) = contrast(q,y) * |cosine(q,y)|
```

The first factor rewards registered relation strength. The second discounts response energy pointing away from the desired sparse relation direction, including wrong-sign trained structure and unused-edge leakage.

The absolute value does **not** erase relation reversal: `contrast` remains signed, so a reversed response has negative utility.

This utility has no fitted leakage coefficient and cannot win merely by shrinking all responses toward zero.

## Three pre-training routers

All routes are selected before finite training.

### READ-AWARE — primary

Choose the candidate maximizing

```text
U(q, q B0).
```

### CONTRAST-ONLY attacker

Give the same dormant write+read operator to an attacker but discard its leakage/directional information. Choose the candidate maximizing

```text
contrast(q, q B0).
```

This is the hardest attacker: if READ-AWARE cannot beat it, the cleanliness term adds no routing value.

### WRITE-ONLY attacker

Gate 11's successful score:

```text
||qW||
```

This asks whether the read Jacobian adds anything beyond predicted structural writability.

## Finite evaluation

After all three route choices are frozen for the substrate, train **all 18 candidates** with the unchanged 40-cycle schedule and measure the actual 15-pair differential response.

Using all 18 prevents a lucky selected-pair comparison and allows correlation of predicted and finite clean utility across the complete geometry-equivalent class.

Report per substrate:

```text
Pearson(predicted U, finite U)
Spearman(predicted U, finite U)
READ-AWARE finite U
CONTRAST-ONLY finite U
WRITE-ONLY finite U
READ/WRITE finite registered contrast
READ/WRITE trained-unused magnitude ratio
READ best trained-edge sign fraction
```

## Preregistered receipt

Design/conservation:

```text
candidate count                         = 18
all arm-A distance multisets            = (1,2,2)
all arm-B distance multisets            = (1,2,2)
all terminal marginals match
all A/B trained edge sets are disjoint
finite mass-budget error                < 1e-10
one-step write mass-sum error            < 1e-10
all values finite
```

Prediction across all 18 assignments must satisfy:

```text
mean utility Pearson                    >= 0.85
mean utility Spearman                   >= 0.75
```

Incremental routing value over Gate 11:

```text
fraction fresh seeds READ U >= WRITE U  >= 5/6
pooled mean READ U / mean WRITE U       >= 1.08
mean READ selectivity / WRITE           >= 1.05
```

Incremental value of the cleanliness term itself:

```text
mean READ U / mean CONTRAST-ONLY U      >= 1.04
```

The cleaner route is not allowed to solve the task by discarding relation strength:

```text
mean READ contrast / WRITE contrast     >= 0.85
mean READ trained-edge sign fraction    >= 0.90
```

**Gate 12 passes only if every registered block passes.**

## Interpretation if PASS

Safe statement:

> **The dormant write+read operator can be used before training to route the same semantic relation into a geometry-matched physical assignment with better finite strength-weighted directional cleanliness than either write-strength routing or dormant contrast-only routing.**

This would turn Gate 10's dormant read sensitivity into actionable design information, not just post-hoc explanation.

It would not establish arbitrary semantic capacity, optimal coding, or task-level intelligence.

## Interpretation if FAIL

Failure location matters:

- predicted U correlations fail -> Gate-10 read geometry does not transfer reliably to route-level cleanliness;
- READ fails against WRITE -> the read Jacobian adds explanation but no useful routing control;
- READ beats WRITE but not CONTRAST-ONLY -> amplitude prediction is enough; explicit leakage/fidelity information is redundant;
- utility improves only by losing too much contrast -> clean routing is a strength/selectivity trade rather than a free improvement.

Do not tune the material dynamics or utility after seeing the fresh range.
