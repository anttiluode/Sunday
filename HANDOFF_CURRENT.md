# Sunday — current handoff

Date: 2026-08-23

## Restart rule

Restart from receipts, not from the 3-D/dendrite/QM metaphor.

Sunday's current object is:

> **A fixed graph plus a fixed local write/read rule induces a strongly anisotropic operator on pair-relation space. Most of that operator's dominant geometry is already present in the dormant substrate before long training.**

The next useful move should be predictive/control-oriented, not another metaphor:

> **Can dormant write geometry be used before training to route a desired semantic relation into a physical terminal assignment that the substrate can store well?**

## Lineage

```text
Gate 0   signal writes spatial transfer                 PASS
         frozen dynamics exactly linear                 calculation claim KILLED

Gate 1   matched coactivity writes pair relation        PASS

Gate 2   same graph with xyz erased                     EXACT TIE
         3-D execution primitive                         KILLED

Gate 3   locality destruction weakens relation
         clustering explanation                          FAIL

Gate 4   matched low spectral gap attacker               PASS
         slow global mixing sufficient                   KILLED

Gate 5   same graph, semantic boundary alignment         PASS

Gate 6   six-terminal relation composition               PASS
         explicit pair table                             CHEAPER

Gate 7   additive endpoint scalar                        KILLED
         multiplicative endpoint sign factor             KILLED

Gate 8   arbitrary/isotropic relation memory             FAIL / KILLED
         anisotropic writable relation space             SURVIVES

Gate 9   16-code writable-subspace tomography            PASS
         rank-7 controlled input span
         empirical q -> dI operator nearly linear
         scalar / per-edge gain explanations             KILLED
         ~3 preferred stable modes                        SURVIVES

Gate 10  dormant one-step write/read Jacobian            PASS
         predicts 40-cycle operator with no fresh fit
         write-only overlap                               KILLED
         write/read spatial misalignment                  KILLED
         long training invents dominant geometry          KILLED as first explanation
```

## Gates 0–5 — substrate facts

- signal history redistributes a fixed total structural mass and changes later transfer;
- frozen Gate-0 dynamics are exactly linear routing;
- coordinates are dead metadata once the graph is constructed;
- Euclidean locality is a useful graph prior, but clustering alone was not established causal;
- low spectral gap / slow global mixing alone does not recover the pair relation;
- semantic coactivity roles relative to graph boundaries strongly affect what relation is written.

## Gate 6 — compositional relation memory PASS

Fresh `380000..380009`:

```text
trained-edge expected signs         60/60
mean signed contrast                0.002666
trained / unused magnitude          12.303x
same-permutation mass shuffle       0.061x residual
```

Safe statement: distributed fixed-budget structural state can simultaneously store several matched coactivity relations without explicit learned pair weights.

Do not claim efficiency; a tiny explicit relation table is cheaper.

## Gate 7 — endpoint scalar nulls PASS

Fresh `400000..400009`:

```text
additive all-pair R^2 mean          0.0753
held-out trained signs              1/60
cycle contrast mean                 0.018913  (additive null requires 0)
negative product cycle              10/10
```

So the Gate-6 code has genuine edge/cycle-space content beyond one scalar per terminal.

## Gate 8 — arbitrary code generality FAIL

Fresh `420000..420005`:

```text
                     sign      trained/unused     specificity     self-top
C0                   1.000          9.487x          10.266x        6/6
C1                   0.917          1.089x           1.506x        6/6
C2                   0.778          4.169x           2.999x        6/6
C3                   0.833          0.305x           0.611x        1/6
```

The substrate is not an isotropic pair-table-in-matter. It has preferred relation directions and rotates/suppresses others.

## Gate 9 — relation-space operator PASS

Enumerate all 16 controlled perfect-matching contrasts satisfying matched terminal marginals and matched circular pair-distance multisets. Their 15-edge code vectors span rank 7.

Fresh `440000..440003`, leave one relation direction out, fit on the other 15, predict the entire unseen 15-pair output:

```text
full operator LOO NMSE              0.003138
held-out cosine                     0.996531
scalar-gain attacker NMSE           0.807419
edge-diagonal attacker NMSE         0.557227

top-3 operator energy               0.977688
rank-3 held-out NMSE                0.037298
rank-3 held-out cosine              0.954902
cross-seed weakest-mode mean        0.902540
```

Safe statement:

> Over the rank-7 controlled relation-program span, the finite write/read behavior is approximately a predictable linear cross-edge operator with most energy in ~3 preferred input modes.

## Gate 10 — dormant write/read Jacobian PASS

Question: does long training create that operator, or amplify one already latent in the dormant graph/rule?

For each of the 15 coactive terminal pairs, from uniform dormant mass:

```text
one existing teacher episode
one existing redistribution update
w_e = mass_after - mass_uniform
```

Then measure the dormant nonlinear read derivative along each `w_e`:

```text
D_e = [F(1 + .25 w_e) - F(1 - .25 w_e)] / .5
B0 = -D
Y0 = Q B0
```

Only one amplitude scalar is allowed, calibrated on development seeds `450000..450001` and frozen before fresh evidence:

```text
GLOBAL_GAIN = 4.805610803751662
```

Fresh `460000..460003`:

```text
zero-fresh-fit NMSE                         0.074607
mean per-direction cosine                   0.969453
flattened dormant/finite cosine             0.970639

dormant projected top-3 energy             0.964520
mean weakest dormant-vs-finite mode cosine 0.918134

write-only -W W^T attacker NMSE             0.916042
same-permutation write-location NMSE        0.920388
primary/write error ratio                   0.08145
primary/permuted error ratio                0.08106
```

Both attackers were advantaged with an optimal **fresh per-seed scalar**; the primary model was not.

Safe statement:

> **Most of the relation-space transform seen after long training is already predictable from the dormant graph's one-step structural write directions composed with its dormant nonlinear read sensitivity. Long training mainly amplifies and perturbs a pre-existing operator.**

Do not say exact first-order dynamics. Residual finite-training NMSE is ~0.075.

### Gate-10 scar

Seed `460001` predicts outputs well (`cosine 0.963`) but its third dormant-vs-finite input-mode cosine is only `0.698`. The pooled mode block passes; individual singular directions are not rigid.

## Post-hoc clue from Gate 10 — not yet promoted

The relation-to-write map `QW` itself remains rank 7 but is already anisotropic:

```text
seed      top-3 energy QW
460000       0.9230
460001       0.8270
460002       0.8849
460003       0.9384
```

Yet its top-three **input modes** match the final finite operator strikingly well:

```text
seed      weakest top-3 write-vs-finite principal cosine
460000       0.9945
460001       0.9652
460002       0.9943
460003       0.9918
mean          ~0.9865
```

At the same time, `-W W^T` fails as an output predictor (NMSE ~0.916).

Working hypothesis:

```text
WRITE STAGE    chooses which relation directions are naturally writable
READ STAGE     determines how those directions become cross-edge output vectors
```

This is post-hoc and needs new seeds before becoming a claim.

## Current residual — turn prediction into control

A better Gate 11 than another passive decomposition is a **pre-training routing/design test**.

Choose one semantic relation code, preferably one that was weak in Gate 8 (e.g. C3). For each fresh physical substrate:

1. compute only dormant one-step write matrix `W`;
2. consider all semantic-to-physical terminal permutations (or a preregistered symmetry-reduced set);
3. for each assignment, map the target semantic code into physical pair space;
4. score its predicted writable strength using only dormant write geometry, for example

```text
|| q_physical W ||
```

or a preregistered projection onto the dominant write subspace;
5. choose **BEST** and **WORST** assignments before any finite training;
6. train the exact same semantic relation under those two assignments on otherwise identical physical substrates;
7. compare finite registered contrast / selectivity / readout strength.

The point is not to prove terminal permutations exist. Gate 5 already showed alignment matters. The new claim would be:

> **The dormant substrate can predict in advance how to route a desired semantic relation into its writable modes.**

Strong attackers:

- random semantic assignment;
- geometry-only assignment score using circular terminal distances;
- terminal degree/strength score;
- shuffled row labels of `W` preserving its singular spectrum;
- use a development-derived universal ranking instead of substrate-specific `W`.

If dormant-W BEST does not beat WORST on fresh finite training, the post-hoc write-mode story is decorative.

## Secondary mechanistic residual

If Gate 11 succeeds, then ask what graph property creates `W`'s preferred modes. Candidate analyses should be attacked rather than named casually:

```text
terminal-to-soma corridor overlap
pairwise current-flow geometry
Laplacian / diffusion modes
community-boundary incidence
local bottleneck placement
```

Gate 3 already killed an easy clustering-only story and Gate 4 killed low-gap-only sufficiency.

## Hard stop lines

- fixed total structural mass unless a new gate explicitly tests growth;
- no explicit learned pair table while claiming morphology stores relations;
- renderer remains read-only;
- Gate 0 is linear routing;
- coordinates are not the execution primitive;
- clustering alone not established;
- low spectral gap alone insufficient;
- Gate 6 has no efficiency advantage;
- Gate 8 killed isotropic arbitrary relation memory;
- Gate 9 measured the finite operator;
- Gate 10 explains most of it first-order but not all finite evolution;
- no QM/phase/ferroic/growth/visual-world mechanism until a demonstrated residual specifically requires it.

## Instanton / QM / Feigenbaum

Parked. The instanton branch supplied useful artifact controls and a separate wave-reservoir negative learning result, but nothing in the live Sunday mechanism requires tunneling, phase, or fractal growth.
