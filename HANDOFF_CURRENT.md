# Sunday — current handoff

Date: 2026-08-23

## Restart rule

Restart from receipts, not from the 3-D/dendrite/QM metaphor.

Sunday's current object is now:

> **A fixed graph and local structural rule induce an anisotropic relation-space operator. Dormant one-step responses predict most of that operator and can be used before training to choose physical routings for semantic relations.**

Gate 12 tested whether adding dormant READ information robustly improves that routing beyond Gate 11's already strong WRITE-only score. It **failed narrowly**. Do not round it into a pass.

The live residual is therefore not “find a nicer utility.” It is:

> **Can we predict from dormant state when read-aware routing will differ enough from write-only routing to be worth using?**

## Lineage

```text
Gate 0   signal writes spatial transfer                 PASS
         frozen dynamics linear                         calculation claim KILLED
Gate 1   matched coactivity writes pair relation        PASS
Gate 2   same graph with xyz erased                     EXACT TIE / 3-D primitive KILLED
Gate 3   locality destruction weakens relation          clustering-only explanation FAIL
Gate 4   matched low-gap attacker                       slow mixing sufficiency KILLED
Gate 5   semantic/topology boundary alignment           PASS
Gate 6   six-terminal compositional relation matrix     PASS / explicit table cheaper
Gate 7   additive & multiplicative endpoint scalars     KILLED
Gate 8   arbitrary/isotropic relation memory            FAIL / KILLED
Gate 9   16-code relation-space tomography              PASS
Gate 10  dormant one-step write/read Jacobian           PASS
Gate 11  pre-training WRITE routing                     PASS
Gate 12  read-aware clean routing                       FAIL narrowly
```

## Gates 6–8 — relation memory and anisotropy

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

Gate 8 then shows that several balanced relation directions are not equally writable. This kills the isotropic pair-table story and exposes a writable relation geometry.

## Gate 9 — relation-space tomography PASS

All 16 controlled geometry-balanced perfect-matching contrasts span rank 7. Leave one whole relation direction out, fit on the other 15, predict the unseen 15-pair output.

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

Safe statement: over the controlled rank-7 relation-program span, finite learning/readout behaves approximately as a predictable linear cross-edge operator with most energy in about three preferred input modes.

## Gate 10 — dormant write/read mechanism PASS

For each of 15 coactive physical terminal pairs, start from uniform mass, perform one ordinary teacher episode and one redistribution, giving pair-specific write direction `w_e`. Measure dormant nonlinear read sensitivity along each `w_e` and compose the first-order operator.

Fresh `460000..460003`:

```text
zero-fresh-fit NMSE                         0.074607
mean per-direction cosine                   0.969453
dormant projected top-3 energy              0.964520
weakest dormant-vs-finite mode mean         0.918134

write-only output attacker NMSE             0.916042
same-permutation write-location attacker    0.920388
```

Safe statement:

> Most dominant relation geometry is already latent in dormant one-step write directions composed with dormant nonlinear read sensitivity; long training mainly amplifies and perturbs it.

## Gate 11 — pre-training WRITE routing PASS

Target semantic relation is fixed to historically weak C3. Keep only semantic-to-physical mappings where both arms have exact circular distance multiset `(1,2,2)`. Exactly 18 assignments remain, so circular geometry alone ties them all.

Before training, score each assignment by

```text
s(q) = ||q W||.
```

Then train all 18.

Fresh `480000..480005`:

```text
mean Pearson(score, finite contrast)          0.936925
mean Spearman                                 0.933333
pair-label-shuffled W Pearson                -0.102667
pair-label-shuffled W Spearman               -0.066667
BEST > WORST                                  6/6
BEST / |WORST| finite contrast                12.395x
```

A development-fixed universal route is already useful, but substrate-specific `W` raises mean BEST contrast about 29%.

Gate-11 scar: maximizing write strength does not guarantee low leakage. Fresh `480003` BEST has trained/unused only `0.631x` despite all registered signs being correct.

## Gate 12 — read-aware clean routing FAIL

Gate 12 keeps the exact same C3 target and 18 geometry-matched assignments.

Before training, use Gate 10's dormant operator

```text
y0(q) = q B0
```

and define the fixed clean utility

```text
contrast(q,y) = (q . y) / 6
cosine(q,y)   = (q . y) / (||q|| ||y||)
U(q,y)        = contrast(q,y) * |cosine(q,y)|
```

READ-AWARE chooses max predicted `U`.

Attackers:

```text
WRITE-ONLY       max ||qW||
CONTRAST-ONLY    max contrast(q, qB0)
```

Development seeds `490000..490003` were consumed only to freeze thresholds. Fresh evidence is `500000..500005`.

### Fresh receipt

```text
mean predicted-U / finite-U Pearson             0.939125   PASS
mean Spearman                                    0.863889   PASS

READ finite U >= WRITE finite U                  6/6        PASS
mean READ clean utility                          0.0007218965
mean WRITE clean utility                         0.0006704296
READ / WRITE clean utility                       1.076767x
required                                         >=1.080000x  FAIL

mean CONTRAST-ONLY clean utility                 0.0006780098
READ / CONTRAST-ONLY clean utility               1.064729x   PASS

mean READ trained/unused                         1.351945x
mean WRITE trained/unused                        1.049575x
READ / WRITE selectivity                         1.288088x   PASS

READ / WRITE registered contrast                 1.002614x   PASS
mean READ trained-edge sign fraction             0.916667    PASS
```

**Gate 12 fails because `1.076767 < 1.08`. Do not rescue it by rounding.**

### What nevertheless survived

Preregistered secondary blocks say something real:

- dormant `B0` predicts route-level clean utility strongly across all 18 assignments;
- the read-aware cleanliness term beats a contrast-only router by `1.0647x`;
- mean trained/unused selectivity improves by `1.288x` while mean registered contrast is unchanged;
- the read-aware route beats or ties write-only on every fresh seed;
- but three of six seeds choose the same READ and WRITE route, leaving pooled incremental utility just below the registered minimum.

Important scars:

```text
500001   READ R02 vs WRITE R00
         clean utility ~1.88x higher
         selectivity 0.686 -> 1.533

500002   READ ties WRITE R07 but beats CONTRAST R00
         cleanliness term itself matters

500004   READ R00 vs WRITE R02
         selectivity 0.788 -> 1.756
         but contrast falls and only 4/6 trained signs are correct
```

Safe statement:

> **Dormant read information is predictive and can materially improve routing on some substrates, especially selectivity, but Gate 12 did not establish the preregistered minimum robust incremental clean-utility gain over Gate 11's write-only router.**

## Current residual — predict when READ matters

Do **not** lower `1.08`, retune the same utility, or rerun C3 until it passes.

The useful phenomenon is now the disagreement structure:

```text
some substrates: READ == WRITE assignment
other substrates: READ != WRITE and gains can be large
```

A clean next gate would use dormant quantities only to predict, before finite training, whether a substrate/candidate family lies in a high-disagreement regime where read-aware routing should matter.

Possible dormant diagnostics to preregister and attack:

```text
angle / principal-angle gap between write-only and write+read preferred modes
ranking disagreement between ||qW|| and U(q,qB0)
spread between top candidate scores
read-induced rotation magnitude ||qB0 - alpha qW_like||
leakage predicted specifically on the WRITE-best route
```

Then test a policy such as:

```text
if dormant disagreement is small: use cheap WRITE routing
if dormant disagreement is large: pay for READ-aware routing
```

The policy must be chosen on development and tested on new substrates/tasks. The target should be **decision value**, not another post-hoc correlation.

A second clean option is to construct a new candidate family where WRITE strength and READ cleanliness are deliberately decorrelated by design, then test whether read-aware routing wins prospectively. Do not search that family using fresh outcomes.

## Secondary mechanistic residual — derive W from graph quantities

Gate 11/12 still require teacher episodes to measure dormant `W`. A deeper mechanism would predict `W` from ordinary graph structure:

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
- Gate 11 controls writability/contrast, not guaranteed selectivity;
- Gate 12 is a **failed** incremental-control gate despite strong secondary evidence;
- no QM/phase/ferroic/growth/visual-world mechanism until a demonstrated residual requires it.

## Instanton / QM / Feigenbaum

Parked. Nothing in the live Sunday residual requires tunneling, phase, or fractal growth.
