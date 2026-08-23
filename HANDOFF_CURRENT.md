# Sunday — current handoff

Date: 2026-08-23

## Restart rule

Restart from receipts, not from the 3-D/dendrite/QM metaphor.

Sunday's live question is now:

> **What is the writable/readable subspace of pair-relation space induced by this fixed substrate and learning rule?**

Gate 8 killed the broad claim that several balanced relation directions are equally writable. The surviving phenomenon is anisotropic: some relation directions are written cleanly, some diffusely, and some are rotated/suppressed.

The next object is therefore the empirical finite-amplitude map

```text
registered training direction q  --->  frozen differential readout dI
```

not another hand-picked code and not a richer mechanism.

## Lineage

```text
Gate 0  signal writes spatial transfer                  PASS
        frozen dynamics exactly linear                  calculation claim KILLED

Gate 1  matched coactivity writes a pair relation       PASS
        distributed local nonlinearity reads relation

Gate 2  same graph with xyz erased                      EXACT TIE
        3-D necessity                                   KILLED
        non-geometric graph still carries weak effect

Gate 3  locality destruction dial                       effect collapses
        clustering prereg                               FAIL

Gate 4  non-geometric low-gap modular attacker          PASS
        slow global mixing sufficient                   KILLED

Gate 5  identical graph, input-role alignment changed   PASS
        signal/topology boundary alignment matters

Gate 6  six-terminal relation-matrix composition        PASS
        60/60 trained relation signs correct
        explicit pair table efficiency attacker         TABLE WINS

Gate 7  endpoint-factor null attack                     PASS
        additive endpoint reduction                     KILLED
        pure multiplicative sign factor                 KILLED
        rank-2 / nonlinear endpoint embedding            OPEN

Gate 8  four independent balanced relation codes        FAIL
        broad/isotropic relation-memory claim            KILLED
        topology-filtered writable subspace              SURVIVES
```

## Gate 0 — route, not calculation

Fixed 256-element substrate, fixed mass budget, no birth/deletion/free learned edges. Signal history changes later transfer, but frozen dynamics obey exact superposition to floating precision. Gate 0 is adaptive routing/structural memory.

## Gate 1 — pair relation

Matched programs `H_AB=[A+B],[C],[D]` and `H_CD=[C+D],[A],[B]` use identical terminal marginals.

Fresh `240000..240019`:

```text
route sign                       20/20 both pairs
nonlinear sign                   20/20 both pairs
mean route separation            0.116056
mean nonlinear separation        0.008948
mass-shuffle signed ratio        ~0.04
```

Coactivity produces route **separation** under this fixed-budget current-reinforcement rule. Do not rewrite as Hebbian merging.

## Gates 2–5 — what topology is doing

Gate 2: coordinates are dead metadata after the graph is built. Erasing xyz with the same graph gives an exact tie. Euclidean locality survives only as a strong graph-construction prior.

Gate 3: destroying locality progressively weakens the relation, but the preregistered clustering explanation missed (`rho=+.575 < +.60`). Clustering alone is not established causal.

Gate 4: matching low spectral gap with random non-geometric modular graphs does not restore the effect. Mean nonlinear recovery is `0.223`; all 15 attackers stay below `0.5`. Slow global mixing is insufficient.

Gate 5: with the **same graph**, moving the semantic coactivity pairing relative to community boundaries changes the nonlinear relation by about `4.34x` on average. Signal/topology boundary alignment matters, although one scar seed reverses nonlinear sign.

## Gate 6 — relation-matrix composition PASS

Six terminals. Two matched disjoint perfect matchings:

```text
M1: (1,2) (3,4) (5,6)
M2: (2,3) (4,5) (6,1)
```

Train two copies, freeze, probe all 15 unordered pairs, and define `dI = I_T2 - I_T1`.

Fresh `380000..380009`:

```text
trained-edge expected signs            60/60
seeds with all 6/6 correct             10/10
mean signed trained-edge contrast      0.002666
mean |trained dI|                      0.002666
mean |unused dI|                       0.000217
trained / unused magnitude             12.303x
same-permutation mass-shuffle ratio    0.061
mass budget error                      ~5.7e-14
```

Safe statement:

> A fixed-budget distributed structural state can simultaneously encode several matched coactivity relations such that a frozen nonlinear pair-interaction matrix distinguishes which relations belonged to which training program, without explicit pair-specific learned weights.

Do not claim efficiency. An explicit 15-entry pair table is dramatically cheaper.

## Gate 7 — endpoint-factor null PASS

Fresh `400000..400009` attacks the Gate-6 differential matrix with endpoint-only scalar models.

For additive endpoint factors `dI(i,j)=a_i+a_j`, the exact alternating-cycle invariant requires

```text
C = d12 - d23 + d34 - d45 + d56 - d16 = 0.
```

Fresh result:

```text
observed trained signs                       60/60
mean C                                       0.018913
minimum C                                    0.009918
additive all-pair R^2 mean/max               0.0753 / 0.2448
additive leave-one-trained-edge-out signs     1/60
negative trained-cycle product seeds          10/10
```

The negative six-cycle product also kills the pure multiplicative scalar sign model `a_i a_j`, whose cycle product must be nonnegative.

Safe statement:

> The Gate-6 relation matrix contains a reproducible edge/cycle-space component that cannot be reduced to one additive scalar per endpoint, and its registered sign code is incompatible with a pure multiplicative endpoint-sign factorization.

Rank-2 / nonlinear endpoint embeddings remain open.

## Gate 8 — independent relation codes FAIL

Four preregistered rank-4 code directions compare disjoint perfect matchings while matching terminal marginals and, within each code, the circular pair-distance multiset.

Fresh `420000..420005`:

```text
                     sign      own contrast     trained/unused     specificity     self-top
C0                   1.000       0.002182           9.487x          10.266x          1.000
C1                   0.917       0.001004           1.089x           1.506x          1.000
C2                   0.778       0.002188           4.169x           2.999x          1.000
C3                   0.833       0.000350           0.305x           0.611x          0.167

pooled same-permutation shuffle ratio         0.1053
mass budget error                              ~5.7e-14
```

Preregistered per-code thresholds required sign `>=.80`, own contrast `>=.00050`, trained/unused `>=2`, specificity `>=1.5`, self-top `>=.75`; all four directions had to pass.

**Gate 8 fails.**

The important scars are different:

- C0 is a clean writable direction.
- C1 remembers something but diffusely: trained pairs do not stand out from unused pairs.
- C2 has strong/selective amplitude but narrowly misses the sign threshold (`.778 < .80`).
- C3 is weak and rotated/non-specific: trained edges are weaker than unused ones and its own registered code is the largest projection only `1/6` times.

The shuffle still destroys ~90% of registered contrast, so learned mass placement remains load-bearing. What died is the isotropic/arbitrary relation-memory story.

Safe statement:

> **Sunday supports pair-specific distributed relation memory, but its writable/readable relation space is strongly anisotropic.**

## Current residual — Gate 9: writable-subspace tomography

Stop choosing one code at a time.

Enumerate a larger family of balanced perfect-matching contrasts satisfying the same terminal-marginal and geometry controls. Let each registered 15-edge direction be `q_r`, and measure the frozen output vector `y_r=dI` after the standard training schedule.

Build matrices

```text
Q = rows of registered training directions q_r
Y = rows of measured frozen relation vectors y_r
```

Then ask what map connects them.

Primary measurements:

```text
own-direction gain              <q_r, y_r> / ||q_r||^2
orthogonal leakage / rotation
cross-code prediction
singular spectrum of the empirical Q -> Y map
cross-seed stability of preferred input/output modes
same-permutation mass-shuffle destruction
```

The important attacker is **held-out direction prediction**. Fit a low-dimensional linear map on some relation directions and predict `dI` for unseen relation directions. Do not fit and score the same codes.

Possible outcomes:

1. **Low-rank stable operator.** A few preferred relation modes predict held-out outputs across seeds. Then Sunday has a compact topology-induced writable subspace.
2. **High-rank but stable operator.** Many directions matter; the substrate still imposes a reproducible relation geometry.
3. **Poor cross-direction prediction but stable per-code effects.** The write/read map is nonlinear or finite-amplitude context-dependent.
4. **No cross-seed stable modes.** Demote further: the observed directions are substrate-instance idiosyncrasies.

Only after this do we know whether capacity, topology adaptation, or a different learning rule addresses a demonstrated limit.

## Secondary residual — endpoint latent compression

Gate 7 did not kill rank-2 / nonlinear endpoint embeddings of a single 15-entry output matrix. Keep this attacker alive, but do not confuse it with Gate 9. Gate 9 asks about the mapping **between relation directions and material responses**, not merely description length of one output.

## Hard stop lines

- fixed total structural mass unless a gate explicitly tests growth;
- no explicit learned pair table while claiming morphology stores relations;
- renderer stays read-only;
- Gate 0 is linear routing;
- 3-D coordinates are not the primitive;
- clustering not established causal;
- slow global mixing insufficient;
- Gate 5 alignment does not guarantee nonlinear sign on every graph;
- Gate 6 has no efficiency advantage over explicit tables;
- Gate 7 kills scalar endpoint reductions only;
- Gate 8 kills broad isotropic relation-memory generality for the current substrate/rule;
- do not tune the mechanism to rescue C1/C2/C3 before measuring the writable subspace;
- no QM/phase/ferroic/growth/visual-world mechanism until a specific residual requires it.

## QM / Feigenbaum / instanton

Parked. The instanton-side work supplied useful negative controls about unstable vacua/readout artifacts and a separate reservoir experiment, but Sunday currently has no residual requiring tunneling, complex phase, fractal branching, or instanton dynamics. Do not merge that story back in by metaphor.
