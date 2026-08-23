# Gate 7 result — endpoint-factor null attack

Date: 2026-08-23

## Question

Gate 6 produced a six-terminal differential pair-interaction matrix with 60/60 registered trained-edge signs correct on fresh seeds. Gate 7 asks whether that apparent pair code can be reduced to one scalar state per terminal.

Fresh range:

```text
400000..400009
```

The Gate-6 composition experiment is repeated unchanged. Only the resulting 15-entry differential matrix is analyzed.

## Null 1 — additive endpoint scalars

Fit the best least-squares model

```text
dI(i,j) = a_i + a_j
```

using six endpoint scalars.

For every such model the alternating six-cycle contrast cancels exactly:

```text
C = d12 - d23 + d34 - d45 + d56 - d16 = 0.
```

Sunday's registered M1/M2 edge signs make all six terms contribute positively to this contrast.

## Null 2 — pure multiplicative endpoint signs

For

```text
dI(i,j) = a_i a_j
```

the product around the six-cycle is

```text
(a1a2)(a2a3)(a3a4)(a4a5)(a5a6)(a6a1)
= product_i a_i^2 >= 0.
```

The registered alternating code contains three negative edges, so six correct nonzero signs imply a negative observed cycle product and cannot come from pure endpoint products.

## Fresh receipt

```text
observed trained-edge sign fraction          1.000 = 60/60

mean alternating cycle contrast C            0.018913
minimum fresh C                              0.009918
(additive endpoint invariant requires)       0 exactly

mean additive all-pair R^2                   0.0753
maximum fresh additive R^2                   0.2448

additive in-sample trained sign accuracy      0.5833
additive leave-one-trained-edge-out accuracy  0.0167 = 1/60

negative trained-cycle product fraction       1.000 = 10/10
max mass-budget error                         ~5.7e-14
```

**Gate 7: PASS.**

All preregistered thresholds pass.

## Per-seed diagnostics

```text
seed     additive R2   in-sample sign   LOO sign   cycle C
400000   0.0546        0.500            0.000      0.013750
400001   0.0975        0.667            0.000      0.027904
400002   0.0301        0.667            0.000      0.020125
400003   0.2448        0.500            0.000      0.009918
400004   0.1927        0.667            0.167      0.020971
400005   0.0317        0.667            0.000      0.016222
400006   0.0146        0.667            0.000      0.018655
400007   0.0199        0.500            0.000      0.014041
400008   0.0179        0.500            0.000      0.022556
400009   0.0490        0.500            0.000      0.024992
```

Only one of the 60 leave-one-trained-edge-out predictions has the registered sign.

## Interpretation

Kill these reductions for the Gate-6 code:

```text
one additive scalar per endpoint
dI(i,j) = a_i + a_j

one pure multiplicative scalar per endpoint
dI(i,j) = a_i a_j   (at least as a sign-factor explanation)
```

Safe statement:

> **The learned differential relation matrix contains a reproducible edge/cycle-space component that cannot be reduced to six additive endpoint scalars, and its six-cycle sign code is incompatible with a pure multiplicative endpoint-sign factorization.**

This strengthens Gate 6's interpretation as pair-specific relational structure rather than merely node state.

## What this does not kill

Gate 7 does **not** rule out:

- a low-rank latent embedding with dimension >1;
- arbitrary nonlinear functions of endpoint embeddings;
- a small learned graph embedding;
- an explicit pair table;
- geometry-specific shortcuts for this single matching contrast.

The explicit pair-table attacker still wins description length by an enormous margin.

## Next residual

Do not add biology or capacity yet.

Two strong next attacks are:

1. **low-rank latent attacker** — ask how many endpoint latent dimensions are required to reconstruct or predict the 15-entry relation matrix, with held-out pair scoring and degrees-of-freedom accounting;
2. **independent-code generality** — repeat the composition test for several distinct geometry-balanced relation contrasts instead of one alternating six-cycle, so Sunday cannot win by specializing to one convenient edge-space direction.

The second is scientifically stronger if kept cheap: if several independent relation codes survive with the same substrate/rule, the result is less likely to be a peculiarity of the chosen hexagonal matching pair.
