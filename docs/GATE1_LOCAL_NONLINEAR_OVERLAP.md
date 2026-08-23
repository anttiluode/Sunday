# Gate 1 — local nonlinear overlap

## Question

Can experience write a **pairwise relationship between inputs** into the 3-D transfer medium, and can a fixed local nonlinearity read that relationship as an input interaction?

Gate 0 established signal-written routing but failed the linearity attacker exactly: frozen responses superpose. Gate 1 therefore changes one thing at a time:

1. first ask whether coactivation history changes *route overlap* while learning itself remains linear;
2. only after freezing morphology, add the same fixed local nonlinearity everywhere and ask whether that structural difference becomes a pairwise interaction.

## Four ports, no planted internal tree

The internal substrate is again a seeded random 256-element 3-D cloud. The soma is fixed on one side. Four input ports A/B/C/D are placed symmetrically on a circle on the other side.

The ports are hand-specified. The internal route is not.

All five port masses remain fixed at 1. The other 251 elements redistribute the remaining mass under the same exact global budget of 256.

## The key matched-history control

Two histories contain the same number of uses of every terminal:

```text
H_AB cycle:
    [A+B together]
    [C alone]
    [D alone]

H_CD cycle:
    [C+D together]
    [A alone]
    [B alone]
```

Therefore each cycle contains exactly one activation of A, B, C and D in both histories. Both histories also contain three episodes and the same total source/sink drive. Only **which pair co-occurs** changes.

Learning is still the Gate 0 current-eligibility / fixed-budget redistribution rule. There are no pair-specific weights.

## Exploratory observation

Seed `230826` produced an initially counterintuitive effect: the pair that was coactive during learning became **less overlapping**, not more overlapping, in the later linear transfer geometry.

That observation was treated as exploratory. The confirmation thresholds were then frozen and a disjoint seed range `240000..240019` was run.

Do not rewrite this as a Hebbian "fire together, wire together" result. Under this particular resource-constrained current-reinforcement rule, coactivation appears to *separate* the pair's internal transfer routes. The mechanism of the sign is still open.

## Measuring route overlap

After learning, freeze mass and use a small linear pulse at one terminal. For each terminal, form an internal route signature from the time-integrated absolute compartment activity, excluding soma and ports, then L2-normalize it.

For terminals `i,j`:

```text
route_overlap(i,j) = cosine(signature_i, signature_j)
```

Define positive program effects so that positive means the coactive pair became less overlapping:

```text
AB separation = overlap_HCD(A,B) - overlap_HAB(A,B)
CD separation = overlap_HAB(C,D) - overlap_HCD(C,D)
```

## Fixed local nonlinear readout

The learned morphology is frozen. No nonlinear term participated in writing the mass.

For the nonlinear probe, every compartment receives the same fixed saturation term:

```text
dv/dt = linear_transfer - gamma * v^3 + input

gamma = 50
probe amplitude = 10
```

The pair interaction is normalized sublinearity at the soma:

```text
I(i,j) = [AUC(i) + AUC(j) - AUC(i+j)] / [AUC(i) + AUC(j)]
```

The relevant program effect is again defined so positive means the coactive pair has the smaller interaction after learning.

A mandatory control puts the *same cubic nonlinearity only at the soma*. If that explains the effect, distributed material is unnecessary.

## Spatial shuffle attacker

For each seed, H_AB and H_CD keep:

```text
same positions
same base geometry graph
same mass budgets
same exact mass multisets for each history
```

but a common random permutation moves the learned non-port masses to different positions. This destroys the learned mass/geometry relationship while preserving scalar distributions.

## Confirmation thresholds

Frozen before the `240000..240019` confirmation range:

```text
positive effect fraction for each pair              >= 0.80
mean route-overlap separation                       >= 0.04
mean nonlinear interaction separation               >= 0.0015
distributed / soma-only program effect               >= 20x
shuffle signed effect / learned signed effect        <= 0.25
mass-budget error                                    < 1e-10
```

## Held-out 20-seed receipt

```text
AB route-separation positive fraction       1.00
CD route-separation positive fraction       1.00
AB interaction-separation positive fraction 1.00
CD interaction-separation positive fraction 1.00

mean route-overlap separation                0.116056
  AB                                          0.123632
  CD                                          0.108479

mean nonlinear interaction separation        0.008948
  AB                                          0.008802
  CD                                          0.009094

mean |soma-only program effect|               8.6397e-06
distributed / soma-only ratio                1035.7x

shuffle route signed ratio                   0.0400
shuffle interaction signed ratio             0.0418

max mass-budget error                        5.68e-14

Gate 1                                        PASS
```

The ratio against the soma-only control is enormous because the soma-only effect is nearly zero. Do not confuse that ratio with effect size: the distributed pair-interaction program effect itself is about **0.9 percentage points** in the normalized interaction metric. It is small but extremely consistent in this instrument.

## What survived

A careful statement is:

> With identical terminal usage counts and a fixed total material budget, changing only which inputs co-occurred wrote a repeatable pair-specific relationship into the spatial transfer geometry. A fixed distributed local nonlinearity later converted that learned route relationship into a pairwise interaction; a soma-only nonlinearity did not, and spatial mass shuffling largely erased the signed effect.

This is closer to a dendritic computational primitive than Gate 0 because the material now contains something relational: not just "A has a good road," but "the history of A with B changes how their routes overlap and therefore how they interact when jointly active."

## What this does not establish

- It does not establish useful task computation.
- It does not establish that the *sign* of the effect is desirable. Coactivation caused route separation here; why is unresolved.
- It does not establish biological plausibility.
- It does not establish superiority to a small graph/RNN with explicit parameters.
- It does not establish that Euclidean 3-D is essential; an abstract graph can reproduce the same effective conductance matrix.
- It does not establish robustness to broad hyperparameter changes yet.
- The cubic nonlinearity was chosen deliberately as the smallest smooth local saturation attacker, not as a biological dendrite model.

## Reproduce

Quick confirmation (8 seeds):

```bash
python experiments/gate1_local_nonlinear_overlap.py
```

Stored 20-seed confirmation:

```bash
python experiments/gate1_local_nonlinear_overlap.py --seed-start 240000 --seeds 20 --json
```

## Next falsifiers

Before adding oscillations, hysteresis, growth or world-model data:

1. sweep nonlinear strength and probe amplitude; the pair-order effect should not exist only at one tuned operating point;
2. vary learning rate, mass floor and overlap radius;
3. compare against an abstract matched graph that discards 3-D coordinates after building `G`;
4. ask whether a small number of such pairwise structural relations can compose into a real discrimination/calculation without adding pair-specific weights.
