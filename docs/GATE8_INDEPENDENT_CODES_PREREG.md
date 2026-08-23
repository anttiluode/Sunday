# Gate 8 preregistration — independent relation codes

Date: 2026-08-23

## Question

Gates 6–7 established one six-terminal relation code and killed one-scalar endpoint reductions. Gate 8 asks a more dangerous question:

> **Can the same fixed-budget learning rule store several independent geometry-balanced relation codes, or was the alternating adjacent-edge hexagon a specially writable direction?**

This gate changes no learning rule, no mass budget, no nonlinear readout, and no substrate size.

## Development / calibration provenance

Consumed development seeds:

```text
410000..410002
```

These seeds were used only to choose a fixed family of code directions and freeze thresholds. They are not Gate-8 evidence.

The development run already suggested a likely negative: C0 was clean, C2 partially clean, while C1 and especially C3 showed poor trained-vs-unused selectivity / code specificity. Thresholds below are therefore not chosen to make the gate pass.

## Fresh range

```text
420000..420005
```

Six independent substrates, four code directions each.

## Four registered code directions

Each code compares two disjoint perfect matchings over the same six physical terminals. Therefore every terminal appears exactly once in each arm.

Within each code the two programs also have the same multiset of circular terminal distances.

```text
C0  distance multiset (1,1,1)
 A: (1,2) (3,4) (5,6)
 B: (1,6) (2,3) (4,5)

C1  distance multiset (1,2,2)
 A: (1,2) (3,5) (4,6)
 B: (1,3) (2,4) (5,6)

C2  distance multiset (1,1,3)
 A: (1,2) (3,6) (4,5)
 B: (1,6) (2,5) (3,4)

C3  distance multiset (2,2,3)
 A: (1,3) (2,5) (4,6)
 B: (1,4) (2,6) (3,5)
```

Define the 15-entry registered code vector `q_c`:

```text
+1 on A edges
-1 on B edges
 0 on unused edges
```

The four registered vectors have rank 4. C1/C2/C3 are each orthogonal to C0; the remaining pairwise dot products have magnitude 1, versus self-norm squared 6. Thus the set is independent and nearly orthogonal without changing terminal marginals.

## Training and readout

For each fresh substrate seed and each code `c`:

1. train identical T_A and T_B copies on the two registered matchings;
2. freeze learning;
3. probe all 15 unordered terminal pairs;
4. compute `dI = I_B - I_A`;
5. compute the registered own-code score

```text
S_c = (q_c · dI) / 6
```

and cross-code scores

```text
S_k = (q_k · dI) / 6,  k != c.
```

The trained-edge expected sign is `sign(q_c)`.

## Controls

For every code:

- exact terminal marginals between A/B;
- exact pair-distance multiset between A/B;
- disjoint trained edge sets;
- fixed 256-element mass budget;
- same physical graph and dynamics within each A/B comparison;
- same-permutation mass shuffle applied to both learned materials before re-reading the relation vector.

The shuffle preserves each material's mass multiset and destroys only the learned placement.

## Metrics

Per seed/code report:

```text
trained-edge expected-sign fraction
own signed contrast S_c
mean |dI| trained / mean |dI| unused
specificity = S_c / max_{k != c} |S_k|
self-top = S_c > max_{k != c} |S_k|
shuffle ratio = |S_c(shuffled)| / |S_c(original)|
```

Also report pooled code-vector design rank and pairwise dot products.

## Preregistered receipt

Design controls must hold exactly:

```text
registered code rank                         = 4
matching terminal marginals                  exact
within-code distance multiset                exact
mass-budget error                            < 1e-10
```

A relation direction counts as robust only if, averaged over the fresh seeds:

```text
mean trained-edge sign fraction              >= 0.80
mean signed own-code contrast                >= 0.00050
mean trained/unused |dI| ratio               >= 2.0
mean own-vs-cross specificity ratio          >= 1.5
self-top fraction                            >= 0.75
```

Across all code/seed cases, the same-permutation shuffle must also reduce the registered contrast:

```text
pooled absolute shuffle/original ratio       <= 0.40
```

**Gate 8 passes only if all four registered code directions meet every per-code robustness criterion and the pooled shuffle criterion passes.**

This is deliberately stronger than merely recovering some trained signs.

## Interpretation if PASS

Safe statement:

> The same fixed-budget structural rule can store and selectively read several linearly independent matched relation programs, not just the original alternating adjacent-edge code.

That would justify studying the capacity / dimensionality of the writable relation space.

## Interpretation if FAIL

Do not throw away Gates 6–7. Instead demote the scope:

> Sunday stores some pair-specific relation structure, but the writable/readable relation space is strongly constrained by the substrate topology and boundary arrangement.

The next useful object would then be the **write/read operator in pair-edge space**: map registered training-code direction `q` to frozen readout vector `dI`, and measure its singular modes / anisotropy.

That is more informative than adding capacity, phase, recurrence, biology, or a learned world decoder.
