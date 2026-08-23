# Gate 7 preregistration — endpoint-factor null attack

Date: 2026-08-23

## Question

Gate 6 showed a clean six-edge relation code in a 15-entry differential pair-interaction matrix. The next null is:

> **Is that apparent pair code really irreducible pair information, or is it just a complicated way of assigning each terminal one scalar state?**

Gate 7 changes no mechanism. It repeats the Gate-6 matched composition experiment on fresh substrates and attacks the resulting matrix with endpoint-only models.

## Fresh range

```text
400000..400009
```

Ten independent substrates. None are Gate-6 confirmation or calibration seeds.

## Relation program

Exactly Gate 6:

```text
M1: (1,2) (3,4) (5,6)
M2: (2,3) (4,5) (6,1)
```

Train identical copies T1/T2, freeze, probe all 15 unordered pairs, and define:

```text
dI(i,j) = I_T2(i,j) - I_T1(i,j)
```

Registered trained signs:

```text
M1 edge: dI > 0
M2 edge: dI < 0
```

## Null 1 — additive endpoint scalars

Fit the best least-squares model over all 15 observed off-diagonal pair entries:

```text
dI_hat(i,j) = a_i + a_j
```

There are six fitted endpoint scalars. A constant offset requires no extra parameter because it is represented by adding the same constant/2 to every `a_i`.

Report:

```text
in-sample R^2 over all 15 pairs
trained-edge sign accuracy of the fitted matrix
```

Then perform six leave-one-trained-edge-out attacks per seed:

1. remove one trained edge from the fit;
2. fit the six endpoint scalars on the other 14 pair entries;
3. predict the held-out trained edge;
4. score its registered sign.

This prevents the null from being credited for fitting and scoring the same relation entry.

## Exact additive invariant

For every endpoint-additive model:

```text
C = d12 - d23 + d34 - d45 + d56 - d16 = 0
```

because each endpoint scalar cancels once positively and once negatively.

For Sunday's registered code, every term contributes with its expected sign. Report `C` per seed and its mean.

This is a structural annihilator of the additive endpoint subspace, not a fitted statistic.

## Null 2 — pure multiplicative endpoint signs

A pure endpoint product model

```text
dI_hat(i,j) = a_i a_j
```

cannot realize the full registered six-cycle sign pattern. The product of its six edge values around the cycle is

```text
(a1 a2)(a2 a3)(a3 a4)(a4 a5)(a5 a6)(a6 a1)
= product_i a_i^2 >= 0.
```

But the registered M1/M2 cycle has three negative edges, so six correct nonzero trained signs imply a **negative** cycle product.

Report the fraction of fresh seeds with negative observed trained-edge product. This attacks only the pure multiplicative endpoint null; it does not kill arbitrary nonlinear endpoint functions.

## Preregistered receipt

First, the underlying Gate-6 code must still be present:

```text
pooled observed trained-edge sign fraction   >= 0.90
mean alternating cycle contrast C            >= 0.0042
```

Then the additive endpoint attacker must remain weak:

```text
mean additive all-pair R^2                   <= 0.30
pooled additive in-sample trained sign acc   <= 0.75
pooled additive leave-one-edge-out sign acc  <= 0.35
```

And the pure multiplicative sign null must be frustrated:

```text
fraction seeds with negative trained-cycle product >= 0.80
```

All values must be finite and the Gate-6 fixed-mass/marginal controls remain unchanged.

## Interpretation if PASS

Safe statement:

> The learned differential relation matrix contains a reproducible edge-space component that cannot be reduced to six additive endpoint scalars, and its registered six-cycle sign code is incompatible with a pure multiplicative endpoint-sign factorization.

This would strengthen the claim that Gate 6 stores **pair-specific relational structure**, not merely per-terminal state.

It would not rule out all low-dimensional nonlinear latent models, rank-2 embeddings, or an explicit pair table.

## Interpretation if FAIL

Demote Gate 6's composition claim. If endpoint scalars predict the trained entries well out of sample, the morphology is mainly carrying node factors rather than irreducible pair relations.

## Calibration provenance

Consumed Gate-6 confirmation matrices `380000..380009` were used only to freeze these thresholds. On them, additive all-pair R^2 averaged ~0.080 (max ~0.185), in-sample trained sign accuracy averaged ~0.45, and leave-one-trained-edge-out sign accuracy was ~0.017 pooled. Those values are not Gate-7 evidence.
