# Gate 8 result — independent relation codes

Date: 2026-08-23

## Question

Gates 6–7 established one pair-specific relation code and killed one-scalar endpoint reductions. Gate 8 asked whether that result generalized across several independent, geometry-balanced relation directions under the **same** fixed-budget learning rule.

Fresh range:

```text
420000..420005
```

Four preregistered code directions were tested on each of six fresh substrates. The registered 15-edge code vectors have rank 4. Within every code comparison, terminal marginals and the circular pair-distance multiset are exactly matched between the two training programs.

## Fresh receipt

```text
                     sign      own contrast     trained/unused     specificity     self-top
C0                   1.000       0.002182           9.487x          10.266x          1.000
C1                   0.917       0.001004           1.089x           1.506x          1.000
C2                   0.778       0.002188           4.169x           2.999x          1.000
C3                   0.833       0.000350           0.305x           0.611x          0.167

pooled same-permutation shuffle/original contrast ratio    0.1053
max mass-budget error                                      5.7e-14
registered code rank                                       4
```

Preregistered robustness thresholds per code were:

```text
mean trained-edge sign fraction       >= 0.80
mean own-code signed contrast         >= 0.00050
mean trained/unused |dI| ratio        >= 2.0
mean own-vs-cross specificity         >= 1.5
self-top fraction                     >= 0.75
```

and pooled shuffle/original contrast ratio had to be `<= 0.40`.

## Verdict

**Gate 8: FAIL.**

The gate required **all four** independent code directions to satisfy every robustness criterion.

- **C0 is robust.** It clears every threshold comfortably.
- **C1 is sign-correct and self-specific, but not selective.** Its trained edges are only `1.089x` the unused-edge magnitude. The training history changes the relation matrix, but the change is diffuse rather than concentrated on the registered pairs.
- **C2 is strong in amplitude, selectivity and specificity, but misses the preregistered sign threshold:** `0.778 < 0.80`. This is a near miss, not a null result.
- **C3 is the decisive failure.** Its own contrast is too small (`0.000350`), trained edges are actually weaker than unused edges (`0.305x`), specificity is below one (`0.611x`), and its own registered code is the largest code projection in only `1/6` fresh substrates.

The pooled mass shuffle still crushes the registered contrast to `0.105` of the original, so this is **not** evidence that structural mass placement became decorative. The learned placement remains load-bearing. What fails is the broad claim that arbitrary balanced pair-relation directions are equally writable/readable by this substrate.

## Safe interpretation

Demote the generality claim to:

> **Sunday supports pair-specific distributed relation memory, but the writable/readable relation space is strongly anisotropic: some balanced relation directions are stored cleanly, some diffusely, and some are rotated or suppressed by the fixed substrate and boundary arrangement.**

That is more informative than either “Gate 6 was a fluke” or “Sunday stores arbitrary relations.” Gates 6–7 survive. Gate 8 reveals their scope.

## The new object

The natural next object is not another hand-picked relation code. It is the empirical map

```text
training relation direction q
              |
              v
     fixed learning dynamics
              |
              v
frozen differential readout dI
```

Call this the **relation-space write/read operator**.

At the fixed training amplitude and schedule it need not be literally linear, but we can still probe it as an empirical finite-amplitude operator. The Gate-8 behavior already says its gain is direction-dependent:

```text
C0  high gain, clean/selective
C1  moderate gain, diffuse leakage
C2  high gain, mostly correct
C3  low gain, rotated/non-specific
```

That suggests singular modes / preferred writable directions rather than an isotropic pair memory.

## Next gate

**Gate 9 — writable-subspace tomography.**

Enumerate a larger balanced set of perfect-matching contrasts, span as much of the admissible edge-space as the geometry-matching constraints allow, train/read each direction on matched substrates, then measure:

```text
own-direction gain
orthogonal leakage / rotation
output rank and singular spectrum
cross-seed stability of preferred modes
mass-shuffle destruction
```

A linear attacker can then be fit on some code directions and asked to predict held-out `dI` vectors. If a low-dimensional operator predicts held-out directions, Sunday has a compact writable relation subspace. If not, the map is more nonlinear/context-dependent than the first four codes suggest.

## What not to do yet

Do not add:

- instanton / QM phase stories;
- element birth or dendritic growth;
- world images or a learned decoder;
- recurrence;
- richer nonlinearities merely to rescue C3.

Gate 8 has produced a concrete residual that the existing mechanism can answer directly.
