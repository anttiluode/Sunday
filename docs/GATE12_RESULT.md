# Gate 12 result — read-aware pre-training routing

Date: 2026-08-23

## Verdict

**Gate 12: FAIL.**

The failure is narrow but registered: every preregistered block passes except the required pooled clean-utility improvement over Gate 11's write-only router.

Fresh range:

```text
500000..500005
```

No threshold or utility definition was changed after seeing fresh data.

## What was tested

The target semantic relation remains historically weak C3. The physical candidate set remains Gate 11's exact 18-assignment geometry-equivalence class:

```text
arm A distance multiset = (1,2,2)
arm B distance multiset = (1,2,2)
identical terminal marginals
A/B trained edges disjoint
```

Before finite training, Gate 12 computes the dormant Gate-10 write/read operator `B0` and predicts the full 15-pair response for every candidate:

```text
y0 = q B0
```

The preregistered clean utility is

```text
contrast(q,y) = (q . y) / 6
cosine(q,y)   = (q . y) / (||q|| ||y||)
U(q,y)        = contrast(q,y) * |cosine(q,y)|
```

READ-AWARE chooses the candidate maximizing predicted `U`.

Attackers:

```text
WRITE-ONLY       maximize ||qW||               (Gate 11)
CONTRAST-ONLY    maximize contrast(q, qB0)     (same dormant read operator, no cleanliness term)
```

All 18 assignments are then trained with the unchanged 40-cycle schedule and evaluated using their actual finite 15-pair response.

## Fresh receipt

```text
mean predicted-U / finite-U Pearson             0.939125
mean Spearman                                    0.863889

READ finite U >= WRITE finite U                  6/6
mean READ clean utility                          0.0007218965
mean WRITE clean utility                         0.0006704296
READ / WRITE clean utility                       1.076767x
registered requirement                           >= 1.080000x   FAIL

mean CONTRAST-ONLY clean utility                 0.0006780098
READ / CONTRAST-ONLY clean utility               1.064729x       PASS

mean READ trained/unused                         1.351945x
mean WRITE trained/unused                        1.049575x
READ / WRITE selectivity                         1.288088x       PASS

mean READ registered contrast                    0.001520529
mean WRITE registered contrast                   0.001516564
READ / WRITE contrast                            1.002614x       PASS

mean READ trained-edge sign fraction             0.916667        PASS
max finite mass-budget error                     2.27e-13
max one-step write mass-sum error                2.42e-13
```

Every registered check passes except `READ / WRITE clean utility >= 1.08`.

The observed value is `1.076767`, about 0.00323 below the ratio threshold. The gate remains failed.

## Per-seed scars

```text
seed     READ   CONTRAST  WRITE   READ U       WRITE U      READ select.  WRITE select.
500000   R06    R06       R06     .00075725    .00075725       1.049          1.049
500001   R02    R02       R00     .00049797    .00026530       1.533          0.686
500002   R07    R00       R07     .00098022    .00098022       1.290          1.290
500003   R02    R02       R02     .00100116    .00100116       1.416          1.416
500004   R00    R04       R02     .00033912    .00026298       1.756          0.788
500005   R00    R00       R00     .00075566    .00075566       1.068          1.068
```

Two different phenomena are visible:

- `500001`: read-aware routing improves both strength and cleanliness over write-only (`1.88x` clean utility; selectivity `0.686 -> 1.533`).
- `500002`: read-aware ties write-only but beats contrast-only by ~34%, so the cleanliness term itself can matter.
- `500004`: read-aware strongly improves selectivity (`0.788 -> 1.756`) but sacrifices registered contrast and gets only `4/6` trained signs. Clean routing remains a real tradeoff, not a solved coding problem.

## What survived despite the failed gate

These were preregistered and pass:

1. **Dormant read-aware predictions are genuinely informative.** Across all 18 assignments, predicted clean utility tracks finite clean utility with mean Pearson `0.939` and Spearman `0.864`.
2. **The read Jacobian contains routing information beyond predicted contrast alone.** READ beats the CONTRAST-ONLY router by `1.0647x` in pooled finite clean utility.
3. **Read-aware routing substantially improves selectivity.** Mean trained/unused improves by `1.288x` while mean registered contrast is essentially unchanged (`1.003x`).
4. **The improvement is not universal enough for the preregistered Gate-12 claim.** Three of six fresh substrates are exact READ/WRITE route ties, leaving pooled utility improvement at `1.0768x`, below the required `1.08x`.

## Safe statement

> **The dormant write+read operator predicts route-level finite cleanliness well and contains useful selectivity information beyond both write strength and predicted contrast, but Gate 12 did not meet its preregistered minimum incremental clean-utility gain over the already strong Gate-11 write-only router.**

Do not call Gate 12 a pass by rounding `1.0768` to `1.08`.

## Interpretation

The failed block suggests that Gate 11's write modes and Gate 10's read modes are often aligned enough that a read-aware router chooses the same assignment as write-only. On other substrates, read information can produce large gains. The effect is therefore **real but intermittent under this fixed 18-candidate task**, not yet a robust additional control layer by the registered standard.

The next experiment should not lower the threshold or retune the utility on the same task.

A scientifically cleaner next residual is to ask **when** read-aware routing differs from write-only using dormant observables alone, or to move to a task/candidate family where write strength and read cleanliness are deliberately decorrelated before seeing outcomes. That would test the read-control mechanism rather than repeatedly optimizing C3.
