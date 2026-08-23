# Gate 10 result — dormant write/read Jacobian

Date: 2026-08-23

## Question

Gate 9 measured an approximately linear, low-dimensional finite-training relation operator. Gate 10 asks whether that operator is already latent in the **dormant** graph plus the unchanged local write/read rules.

Fresh range:

```text
460000..460003
```

No fresh finite-training output is allowed to fit the primary prediction. The only amplitude calibration is the development-only constant

```text
GLOBAL_GAIN = 4.805610803751662
```

and the dormant read derivative uses the preregistered symmetric perturbation `epsilon=0.25`.

## Dormant construction

For each of the 15 possible coactive terminal pairs, start from uniform mass and apply exactly one existing teacher + redistribution update:

```text
w_e = mass_after_one_update - mass_uniform
```

Then, still around dormant mass, measure the full 15-pair interaction derivative along each `w_e`:

```text
D_e = [F(1 + epsilon w_e) - F(1 - epsilon w_e)] / (2 epsilon)
```

Because registered code vectors use `+A -B` while the finite output is `F(B)-F(A)`, define

```text
B0 = -D
Y0 = Q B0
Y_hat = GLOBAL_GAIN * Y0.
```

`Y_hat` is therefore a zero-fresh-fit prediction of the 40-cycle finite target.

## Fresh receipt

Per seed:

```text
seed     primary NMSE   mean cosine   best-seed NMSE*   dormant top3   weakest mode cosine   write-only NMSE   permuted NMSE
460000      0.05870       0.96831          0.05305          0.98217          0.99400              0.97385          0.99383
460001      0.12462       0.96321          0.08677          0.90802          0.69773              0.72170          0.94996
460002      0.03239       0.98391          0.03194          0.97335          0.98750              0.97592          0.88446
460003      0.08272       0.96238          0.05927          0.99454          0.99331              0.99270          0.85330
```

`*` Best-seed NMSE uses a per-seed optimal scalar only as a diagnostic and is **not** part of the primary prediction.

Pooled:

```text
mean frozen-development-gain NMSE                 0.074607
mean per-direction cosine                         0.969453
mean flattened dormant-vs-finite cosine           0.970639
mean diagnostic optimal-seed NMSE                 0.057758

mean dormant projected top-3 energy               0.964520
mean weakest dormant-vs-finite top-3 cosine       0.918134

mean write-only attacker NMSE                     0.916042
mean same-permutation attacker NMSE               0.920388
primary / write-only error ratio                  0.081445
primary / permuted error ratio                    0.081061

max one-step write mass-sum error                 4.54e-14
max finite mass-budget error                      5.68e-14
```

All preregistered blocks pass.

**Gate 10: PASS.**

## Attacker interpretation

### Write-only similarity fails

The attacker

```text
B_write = -W W^T
```

is allowed its own optimal scalar on every fresh substrate and still has pooled NMSE `0.916`.

Therefore similarity among pair-specific structural write traces is not enough to predict the final relation vector. The dormant read sensitivity matters.

### Same-permutation write-location surgery fails

The same internal-node permutation is applied to **every** row of `W`. This preserves exactly:

```text
all row norms
all W-row dot products
W W^T
per-row mass sums
```

but moves the structural writes relative to the graph/read sensitivity.

Even after its own optimal fresh scalar, this attacker has pooled NMSE `0.920`.

Therefore *where* the teacher writes relative to what the dormant substrate can read is load-bearing.

## Safe statement

> **Most of the relation-space transformation observed after 40-cycle training is already predictable from the dormant graph's one-step structural write directions composed with its dormant nonlinear read sensitivity. Long training primarily amplifies and perturbs a pre-existing write/read operator rather than inventing its dominant relation geometry from scratch.**

The residual finite-training correction is real: the zero-fresh-fit NMSE is ~0.075 rather than Gate 9's ~0.003 empirical-operator error.

## Scar

Seed `460001` predicts finite outputs well (`cosine 0.963`) but its third dormant-vs-finite input-mode cosine is only `0.698`. The pooled three-mode alignment passes, but do not claim every singular direction is rigid seed by seed.

## Post-hoc clue — not part of the Gate-10 receipt

Decomposing the fresh seeds after the gate:

```text
seed      rank(QW)   top-3 energy of relation->write map
460000       7                    0.9230
460001       7                    0.8270
460002       7                    0.8849
460003       7                    0.9384
```

So the write stage is already anisotropic but less compressed than the full dormant write/read operator (`mean top-3 0.9645`).

More strikingly, the top-three **write-stage input modes** match the final finite operator's top-three input modes with weakest principal cosine:

```text
460000   0.9945
460001   0.9652
460002   0.9943
460003   0.9918
mean     ~0.9865
```

Yet write-only output prediction fails badly. This suggests a useful stage split:

```text
teacher/write geometry     -> selects preferred input relation directions
read sensitivity           -> supplies the cross-edge output transformation
```

This was noticed after Gate 10 and must be tested on new seeds before being promoted to a claim.

## Next residual

A strong Gate 11 should test the stage split on fresh substrates and, if it survives, turn it into a **pre-training design test** rather than another descriptive matrix comparison.

One concrete route:

1. use only the dormant one-step write matrix to score how well a target semantic relation code aligns with the substrate's preferred write modes under alternative assignments of semantic terminals to the same physical ports;
2. choose a predicted BEST and WORST assignment **before finite training**;
3. train only the target relation under those assignments on identical physical graphs;
4. ask whether the dormant write score predicts the finite writable contrast/selectivity gap.

That would turn Sunday's relation geometry into something actionable: pre-route a desired relation into a substrate direction that it can actually store.
