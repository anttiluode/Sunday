# Sunday audit result — reservoir null and ring-symmetry null

Date: 2026-08-23

## Why this audit happened

By Gate 12, Sunday had moved far from the original "3-D dendrite" motivation. Gates 9–12 increasingly resembled a fixed substrate with preferred response modes, a feature map, and pre-training input routing — all familiar territory around reservoir computing and physical reservoir computing.

Rather than add Gate 13, this audit asks what is actually left after giving the strongest boring explanations a fair chance.

---

# Audit A — fixed dormant reservoir + trained linear readout

## Verdict

**The reservoir null wins against the claim that Gate 9's relation-space transform is itself a new computing primitive.**

It does **not** reproduce Sunday's persistent in-medium history storage without putting the learned information somewhere else.

Fresh audit range:

```text
520000..520005
```

For each dormant substrate, compute the existing one-step write matrix

```text
W : 15 physical pair inputs x 256 structural coordinates
```

and the controlled Gate-9 relation programs

```text
Q : 16 codes x 15 pair coordinates
rank(Q) = 7.
```

Use the fixed dormant feature map

```text
X = Q W.
```

No 40-cycle structural training occurs.

## Fresh receipt

```text
rank(Q)                                  7
rank(QW)                                 7 / 7 on all 6 seeds
minimum leave-one-code-out rank(QW)      7

LOO linear reconstruction q <- qW
mean NMSE                                5.65e-30
mean cosine                              1.000000000000

minimum restricted s_min / s_max         0.0862
mutable Sunday mass scalars              249
```

So `q -> qW` is injective on the entire controlled seven-dimensional relation span in every fresh substrate tested. Even after removing any one of the 16 registered codes, the other 15 dormant feature vectors still span all seven controlled degrees of freedom.

That gives an exact algebraic reduction:

```text
Gate 9:          y ~= q B
Dormant feature: x  = q W

because q can be linearly recovered from x on the controlled span,
there exists R such that

                 y ~= x R.
```

Therefore a **fixed dormant substrate plus a trained linear readout** can represent the same linear relation maps that Gate 9 measured, without structural mass learning being required for the transform itself.

Gate 10's old write-only attacker `-W W^T` did not test this null: it imposed one specific similarity readout. This audit gives the dormant features the conventional reservoir-computing privilege of a fully trained linear output map.

## What this kills

Do not claim:

> Gate 9/10 discovered a new class of computation merely because a complicated substrate maps relation programs into a low-dimensional, predictable response space.

That broad phenomenon is compatible with ordinary fixed-feature / reservoir computation.

There is also no parameter-efficiency victory here. Sunday has 249 mutable internal mass scalars in this six-terminal toy, while an explicit 15-entry pair table is dramatically smaller and a linear map on a seven-dimensional controlled input span can be parameterized much more compactly than the substrate.

## What this null does **not** reproduce

The fixed-reservoir audit keeps `W` dormant and puts learned task information into an external readout.

Sunday's structural experiment instead does:

```text
teaching history
      |
      v
local mass redistribution
      |
      v
teaching signal removed
fast dynamical state reset
      |
      v
persistent changed substrate
      |
      v
same future probe now interacts differently
```

A fixed reservoir whose fast state is reset has no variable that distinguishes the two past training histories. To match that property it needs an external learned readout, persistent recurrent state, synaptic/structural plasticity, or some other memory store.

So the surviving distinction is **where history is stored**, not whether a rich substrate plus linear readout can compute the relation transform.

---

# Audit B — six-terminal ring symmetry / spectral null

## Verdict

**Ring symmetry explains most, but not all, of Gate 9's three-mode story.**

The phrase "three mysterious preferred material modes" should be retired. A large majority of that structure is already visible in ordinary symmetry sectors of the six-terminal ring.

Fresh full-training audit range:

```text
522000..522003
```

## Exact geometry-only decomposition

The controlled relation-program span has rank seven.

Under one-terminal rotation of the six-port ring, that seven-dimensional span decomposes into real cyclic harmonic sectors:

```text
k=1 sector     dimension 2
k=2 sector     dimension 4
k=3 sector     dimension 1
               -----------
total          dimension 7
```

No learned output is used to obtain this decomposition.

Exploratory dormant work fixed one specific three-dimensional geometry-only candidate before the fresh full-training range:

```text
nearest-neighbour edge-orbit k=2 harmonic copy   2-D
+
k=3 parity harmonic                              1-D
                                                   ---
                                                    3-D
```

## Fresh finite-operator receipt

For each fresh substrate, train all 16 controlled Gate-9 relation programs, fit the same all-direction minimum-norm finite operator for mode analysis, and compare its top-three input singular subspace with the fixed geometry-only spaces.

```text
mean finite top-3 operator energy             0.9781

fixed geometry-only 3-D candidate:
mean weakest principal cosine                 0.8587
mean subspace capture                         0.8783

broader k=2 + k=3 symmetry sector (5-D):
mean weakest principal cosine                 0.9475
mean subspace capture                         0.9633

fraction of learned top-3 subspace by sector:
k=1                                           0.0367
k=2                                           0.6564
k=3                                           0.3069
```

Per-seed weakest principal cosine for the fixed three-dimensional geometry-only candidate:

```text
522000    0.7769
522001    0.8993
522002    0.8948
522003    0.8640
```

## Interpretation

The coarse result is strong:

> Gate 9's preferred modes overwhelmingly occupy the ordinary `k=2` and `k=3` sectors of the six-terminal ring.

Only about 3.7% of top-three subspace weight lies in the `k=1` sector on average. The broad five-dimensional `k=2+k=3` symmetry sector captures about 96% of the learned top-three subspace.

More surprisingly, a fixed three-dimensional construction using only terminal-ring geometry captures about 88% of the actual learned top-three subspace.

So much of Gate 9's apparent low-dimensional mystery is an ordinary consequence of the controlled port geometry.

But symmetry alone is **not a complete explanation**. The `k=2` sector has multiplicity four; ring symmetry by itself does not choose the exact two-dimensional copy used by each learned operator. The fixed geometry-only 3-D candidate misses about 12% of subspace energy on average and has one weakest principal cosine of only `0.777`.

The remaining question is therefore narrower:

> What graph/current-flow/write-read structure selects and rotates the particular two-dimensional slice inside the symmetry-allowed `k=2` sector?

That residual is real. It is no longer evidence for a mysterious universal three-mode material algebra.

---

# Relation to known reservoir-computing territory

Sunday overlaps established reservoir ideas substantially.

Classic reservoir computing keeps a complex recurrent or physical substrate fixed and trains a simple output readout. Input masks/routing are known to control which reservoir degrees of freedom are excited. Structural-plasticity variants also exist, so "reservoir whose internal structure changes" is not a new category by itself.

Useful orientation:

- Roy & Basu, **An Online Structural Plasticity Rule for Generating Better Reservoirs**, Neural Computation 28(11), 2016. DOI: 10.1162/NECO_a_00886.
- Appeltant et al., **Constructing optimized binary masks for reservoir computing with delay systems**, Scientific Reports 4, 3629 (2014), https://www.nature.com/articles/srep03629

The Sunday-specific experimental object should therefore be described narrowly and without a novelty claim until compared more deeply with adaptive/physical reservoir literature.

---

# What is still worth keeping

After the audit, the strongest surviving Sunday statement is:

> **Under a fixed total resource budget, equal-marginal co-occurrence history can be written by a local structural rule into persistent distributed substrate state. That state carries nontrivial edge/cycle-space relation information and changes later nonlinear interactions after the teaching history is gone. The writable/readable relation geometry is strongly constrained by ordinary substrate symmetry and can often be predicted from dormant response.**

This is not yet an efficient architecture and not yet a new neural-network primitive.

It is a clean experimental object for asking a more specific question:

> When does writing history into the medium itself buy something over keeping a fixed reservoir and learning an observer?

That is the audit boundary Sunday should respect going forward.
