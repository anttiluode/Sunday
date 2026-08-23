# Sunday — current handoff

Date: 2026-08-23

## Restart rule

Restart from receipts, not from the 3-D/dendrite/QM metaphor.

Sunday's live object is now both measurable **and controllable**:

> **A fixed graph and local structural rule induce an anisotropic relation-space operator. Dormant one-step responses predict that operator, and the dormant write geometry can be used before training to choose a physical routing for a semantic relation.**

The remaining limitation is important: Gate 11 controls **registered relation contrast**, not guaranteed selectivity against unused pair responses.

The strongest next practical residual is therefore:

> **Can dormant write+read information choose a geometry-matched routing that will produce a clean/selective relation code, not merely a stronger registered contrast?**

## Lineage

```text
Gate 0   signal writes spatial transfer                 PASS
         frozen dynamics linear                         calculation claim KILLED
Gate 1   matched coactivity writes pair relation        PASS
Gate 2   xyz erased with same graph                     EXACT TIE / 3-D primitive KILLED
Gate 3   locality destruction weakens relation          clustering-only explanation FAIL
Gate 4   matched low-gap attacker                       slow mixing sufficiency KILLED
Gate 5   semantic/topology boundary alignment           PASS
Gate 6   six-terminal compositional relation matrix     PASS / explicit table cheaper
Gate 7   additive & multiplicative endpoint scalars     KILLED
Gate 8   arbitrary/isotropic relation memory            FAIL / KILLED
Gate 9   16-code relation-space tomography              PASS
         empirical q -> dI map nearly linear
Gate 10  dormant one-step write/read Jacobian           PASS
         predicts most finite operator geometry
Gate 11  pre-training semantic routing                  PASS
         dormant ||qW|| predicts geometry-matched writability
```

## Gates 6–8 — relation memory, then the useful failure

Gate 6 fresh `380000..380009`:

```text
trained-edge signs                 60/60
mean signed contrast               0.002666
trained / unused magnitude         12.303x
mass-shuffle residual              0.061x
```

Gate 7 fresh `400000..400009` kills one-scalar endpoint reductions:

```text
additive all-pair R^2              0.0753 mean
held-out additive trained signs    1/60
negative multiplicative cycle      10/10
```

Gate 8 then deliberately asks whether several balanced relation codes are equally writable. They are not:

```text
                     sign      trained/unused     specificity     self-top
C0                   1.000          9.487x          10.266x        6/6
C1                   0.917          1.089x           1.506x        6/6
C2                   0.778          4.169x           2.999x        6/6
C3                   0.833          0.305x           0.611x        1/6
```

That failure killed the isotropic pair-table story and exposed a **writable relation geometry**.

## Gate 9 — tomography PASS

Enumerate all 16 controlled geometry-balanced perfect-matching contrasts. Their 15-edge input vectors span rank 7.

Leave one entire relation direction out, fit the map on the other 15, predict the unseen 15-pair output vector.

Fresh `440000..440003`:

```text
full operator LOO NMSE               0.003138
held-out cosine                      0.996531
scalar-gain attacker NMSE            0.807419
edge-diagonal attacker NMSE          0.557227

top-3 operator energy                0.977688
rank-3 held-out NMSE                 0.037298
rank-3 held-out cosine               0.954902
cross-seed weakest-mode mean         0.902540
```

Safe statement:

> Over the controlled rank-7 relation-program span, finite learning/readout behaves approximately as a predictable linear cross-edge operator with most energy in about three preferred input modes.

## Gate 10 — dormant mechanism PASS

For each of 15 coactive physical terminal pairs, from uniform dormant mass:

```text
one teacher episode + one redistribution
w_e = one-step mass displacement
```

Then measure dormant read sensitivity along each `w_e` and compose the first-order operator.

One global amplitude gain is frozen from development only; no fresh per-substrate fitting.

Fresh `460000..460003`:

```text
zero-fresh-fit NMSE                         0.074607
mean per-direction cosine                   0.969453
dormant projected top-3 energy              0.964520
weakest dormant-vs-finite mode mean         0.918134

write-only attacker NMSE                    0.916042
same-permutation write-location attacker    0.920388
```

Safe statement:

> Most dominant relation geometry is already latent in the dormant graph's one-step write directions composed with dormant nonlinear read sensitivity; long training mainly amplifies and perturbs it.

Scar: seed `460001` has third-mode cosine `0.698` despite good overall output prediction. Do not call each singular direction rigid.

## Gate 11 — pre-training routing PASS

Target semantic relation is fixed to historically weak `C3`.

Consider semantic-to-physical terminal mappings, but remove the easy geometry explanation by keeping only assignments where both physical arms have exact circular distance multiset

```text
(1,2,2).
```

Exactly 18 distinct oriented assignments remain. Every geometry-only circular-distance score is therefore tied.

Before any finite training, compute dormant one-step write matrix `W` and score each assignment by

```text
s(q) = ||q W||.
```

Then train **all 18** and compare the complete dormant ranking against finite registered contrast.

Fresh `480000..480005`:

```text
mean Pearson(score, finite contrast)             0.936925
mean Spearman                                    0.933333

pair-label-shuffled W Pearson                   -0.102667
pair-label-shuffled W Spearman                  -0.066667
Pearson advantage                                1.039592
Spearman advantage                               1.000000

preregistered BEST > WORST                       6/6
mean BEST contrast                               0.00154504
mean |WORST| contrast                            0.00012465
BEST / |WORST|                                   12.395x
```

The row-label attacker preserves the exact set and singular spectrum of dormant write vectors, but scrambles which physical pair owns each trace. It loses prediction. Physical pair ownership is load-bearing.

### Universal versus substrate-specific routing

A fixed development-average routing is already good:

```text
universal BEST mean finite contrast              0.00119589
substrate-specific W BEST                        0.00154504
local / universal                                1.292x
```

So there is a strong graph-family-level routing preference plus an additional substrate-specific advantage. Do not claim local BEST wins every seed; universal happens to beat it slightly on `480003` and `480005` because the dormant score is predictive, not exact.

### Gate-11 limitation

BEST was chosen to maximize registered signed contrast. It does **not** guarantee low leakage.

Fresh `480003` is the scar:

```text
BEST registered sign fraction          1.000
BEST trained / unused magnitude        0.631x
```

The intended relation is strengthened, yet unused pair responses can still be larger.

Safe statement:

> **Dormant write geometry can route a semantic relation into a more writable physical assignment before training, beyond matched circular geometry, but this alone does not guarantee a clean/selective relation representation.**

## Current residual — pre-train for selectivity

Gate 10 already gives more information than Gate 11 used. Gate 11 used only the WRITE magnitude `||qW||`; Gate 10 can predict the whole dormant first-order output vector

```text
q -> y0 = q B0
```

where `B0` composes one-step write directions with dormant nonlinear read sensitivity.

A strong Gate 12 should keep the **same fixed C3 semantic target and the same 18 geometry-matched assignments**, but rank assignments before training by a read-aware objective that penalizes predicted unused-edge leakage.

For candidate physical `q`, possible preregistered score:

```text
predicted y0 = q B0
predicted own = (q dot y0) / 6
predicted leakage = mean |y0_e| over q_e == 0
quality = predicted own / (predicted leakage + eps)
```

Do not tune this on fresh seeds.

Then train all 18 on fresh substrates and test whether the dormant quality ranking predicts finite:

```text
trained / unused magnitude
own-vs-cross specificity
or a fixed combined quality metric
```

Attackers should include:

```text
Gate-11 write-only ||qW|| ranking
circular geometry (tied by construction)
pair-label-shuffled dormant B0
fixed universal assignment from development
```

The important question is whether dormant READ information buys something beyond write strength.

If yes, Sunday can choose not only where a relation is easiest to write, but where it will be **read cleanly**.

## Secondary residual — derive W from ordinary graph quantities

After control is established, explain the write geometry without running teacher episodes. Candidate mechanisms:

```text
terminal-to-soma current-flow overlap
pairwise corridor overlap
Laplacian / diffusion modes
community-boundary incidence
local bottleneck placement
```

Gate 3 already blocks clustering alone; Gate 4 blocks spectral-gap alone.

## Hard stop lines

- fixed total structural mass unless a gate explicitly tests growth;
- no explicit learned pair table while claiming morphology stores relations;
- renderer stays read-only;
- Gate 0 remains linear routing;
- coordinates are not the execution primitive;
- clustering alone not established;
- low spectral gap alone insufficient;
- Gate 6 has no efficiency advantage over explicit tables;
- Gate 8 killed arbitrary/isotropic relation memory;
- Gate 10 is first-order approximate, not exact finite dynamics;
- Gate 11 controls contrast, not guaranteed selectivity;
- no QM/phase/ferroic/growth/visual-world mechanism until a demonstrated residual requires it.

## Instanton / QM / Feigenbaum

Parked. The instanton side supplied useful artifact controls and a separate negative self-carving result, but nothing in Sunday's current mechanism requires tunneling, phase, or fractal growth.
