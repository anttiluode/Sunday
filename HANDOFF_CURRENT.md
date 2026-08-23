# Sunday — current handoff

Date: 2026-08-23

## Restart rule

Restart from receipts, not from the 3-D/dendrite/QM metaphor.

Sunday's live object is now much sharper than the original morphology story:

> **A fixed substrate plus a fixed local structural learning/readout rule induces an approximately linear, strongly anisotropic operator on controlled pair-relation space.**

The next question is mechanistic:

> **Can that finite trained operator be predicted from the dormant substrate by a first-order write/read Jacobian, before 40-cycle training?**

Do not add capacity, phase, growth, images, or biology before attacking that.

## Lineage

```text
Gate 0  signal writes spatial transfer                  PASS
        frozen dynamics exactly linear                  calculation claim KILLED

Gate 1  matched coactivity writes a pair relation       PASS
        distributed local nonlinearity reads relation

Gate 2  same graph with xyz erased                      EXACT TIE
        3-D necessity                                   KILLED

Gate 3  locality destruction dial                       effect collapses
        clustering prereg                               FAIL

Gate 4  low-gap non-geometric attacker                  PASS
        slow global mixing sufficient                   KILLED

Gate 5  same graph, input-role alignment changed        PASS
        signal/topology boundary alignment matters

Gate 6  six-terminal relation-matrix composition        PASS
        60/60 trained relation signs correct
        explicit pair table                             CHEAPER

Gate 7  endpoint-factor null                            PASS
        additive endpoint scalar                        KILLED
        multiplicative scalar sign factor               KILLED

Gate 8  independent relation-code generality            FAIL
        isotropic/arbitrary relation memory              KILLED
        anisotropic writable relation space              SURVIVES

Gate 9  writable-subspace tomography                    PASS
        16 controlled codes, input span rank 7
        held-out q -> dI operator prediction             PASS
        scalar identity/gain                             KILLED
        independent per-edge gains                       KILLED
        ~3 preferred cross-seed-stable modes             SURVIVES
```

## What survived Gates 0–5

- fixed total structural mass can store signal history by redistributing conductance;
- frozen Gate-0 dynamics are linear routing, not already a calculating dendrite;
- coordinates are not execution-time primitives once the graph exists;
- Euclidean locality is a strong graph prior, but clustering alone did not explain the effect;
- low spectral gap / slow global mixing is insufficient;
- where semantic coactivity roles land relative to graph boundaries strongly affects the relation written.

## Gate 6 — compositional pair relation PASS

Six terminals; two matched disjoint perfect matchings. Train two copies, freeze, probe all 15 unordered terminal pairs.

Fresh `380000..380009`:

```text
trained-edge expected signs            60/60
mean signed trained-edge contrast      0.002666
trained / unused magnitude             12.303x
same-permutation mass-shuffle ratio    0.061
```

Safe statement: a fixed-budget distributed structural state can simultaneously encode several matched coactivity relations without explicit pair-specific learned weights.

Do not claim efficiency. An explicit 15-entry relation table is vastly cheaper.

## Gate 7 — endpoint scalar nulls PASS

Fresh `400000..400009`:

```text
additive endpoint all-pair R^2 mean        0.0753
additive held-out trained signs             1/60
alternating-cycle contrast mean             0.018913  (endpoint-additive null requires 0)
negative multiplicative cycle product       10/10
```

So the Gate-6 matrix is not merely six node scalars in additive disguise, and its sign code cannot be a pure `a_i a_j` factor.

## Gate 8 — broad relation-code generality FAIL

Four independent geometry-balanced code directions on fresh `420000..420005`:

```text
                     sign      trained/unused     specificity     self-top
C0                   1.000          9.487x          10.266x        6/6
C1                   0.917          1.089x           1.506x        6/6
C2                   0.778          4.169x           2.999x        6/6
C3                   0.833          0.305x           0.611x        1/6
```

The same-permutation shuffle still destroys ~90% of registered contrast. The failure therefore demoted the **isotropic/arbitrary relation memory** claim, not the structural-memory phenomenon.

This failure suggested that the substrate rotates/suppresses relation directions rather than simply storing some and forgetting others.

## Gate 9 — writable-subspace tomography PASS

Enumerate every controlled perfect-matching contrast satisfying:

```text
same six physical terminals
perfect matching on each arm
no common trained edge between arms
identical terminal marginals
identical circular pair-distance multiset
q and -q duplicates removed
```

There are 16 such directions. Their 15-edge code vectors span rank 7; deleting any one row still leaves rank 7.

For each fresh substrate `440000..440003`, train all 16 directions and measure the frozen 15-pair output vector `y=dI`.

Primary test: for each held-out relation direction, fit

```text
Q_train B ~= Y_train
```

on the other 15 and predict the complete unseen output vector `q_heldout B`.

Fresh pooled receipt:

```text
mean full-linear LOO NMSE                    0.003138
mean full held-out cosine                    0.996531

scalar identity/gain attacker NMSE           0.807419
edge-diagonal gain attacker NMSE             0.557227
full/scalar error ratio                      0.003887
full/diagonal error ratio                    0.005632

mean top-3 operator energy                   0.977688
mean rank-3 LOO NMSE                         0.037298
mean rank-3 held-out cosine                  0.954902

mean weakest top-3 input principal cosine
across fresh substrate pairs                 0.902540

max mass-budget error                        ~5.7e-14
```

All preregistered blocks pass.

Safe statement:

> **Over the seven-dimensional controlled relation-program span, Sunday's fixed structural learning dynamics act approximately as a predictable linear write/read operator. Roughly 98% of the fitted operator energy lies in three singular modes, and the preferred three-dimensional input subspace is stable across fresh random substrates.**

This explains Gate 8: C0/C1/C2/C3 were directions being passed through an anisotropic cross-edge operator, not four unrelated special cases.

## What Gate 9 killed

Do not resurrect either explanation without a new intervention:

```text
y ~= g q                     scalar preserve/amplify model

y_j ~= d_j q_j               independent physical-pair gains
```

Both lose catastrophically to the held-out full operator. Cross-edge mixing is load-bearing.

## Current residual — derive the operator

Gate 9 measured `B`; it did not explain it.

The clean mechanistic hypothesis is a first-order factorization around dormant uniform mass:

```text
relation-program direction q
          |
          v
teacher / eligibility response
          |
          v
pair-specific mass-write directions       W
          |
          v
mass perturbation
          |
          v
frozen pair-interaction sensitivity       R
          |
          v
predicted relation response

              B_first_order ~ W R
```

A strong Gate 10 should build this without using 40-cycle trained outputs to fit its direction:

1. start from the same dormant graph and uniform mass;
2. for each of the 15 possible coactive terminal pairs, measure the **one-step structural write vector** produced by the existing teacher/eligibility/update rule;
3. around dormant mass, measure how the 15 pair-interaction outputs change along those write directions using symmetric small perturbations;
4. compose the resulting write/read Jacobian into a predicted 15x15 relation operator;
5. restrict it to the rank-7 controlled `Q` span;
6. compare its held-out predictions, singular spectrum and preferred input subspace with the independently measured finite-training Gate-9 operator on fresh substrates.

Attackers should include at least:

```text
identity/scalar map
edge-diagonal map
write-only similarity (ignore read Jacobian)
read-only endpoint/pair sensitivity if meaningful
randomly permuted write directions preserving their norms
```

The key falsifier is not in-sample matrix correlation. It is whether the dormant first-order operator predicts **unseen finite-training relation-direction outputs** and the preferred Gate-9 modes.

Possible outcomes:

- **PASS:** the low-dimensional relation geometry is already latent in the dormant graph + local rule; long training amplifies it rather than inventing it.
- **finite operator predictable but modes differ:** first-order response captures outputs but not the compact preferred subspace.
- **write/read Jacobian fails:** the operator is generated by nonlinear structural evolution across training cycles.

## Secondary residuals — keep parked

- Gate 7 did not kill rank-2/nonlinear endpoint embeddings of one output matrix. This is a description-length attacker, not the Gate-10 mechanism question.
- Capacity/growth becomes justified only if a measured writable mode limit blocks a task we actually care about.
- Image/world inputs should only enter after we know what information the current relation operator can and cannot represent.

## Hard stop lines

- fixed total structural mass unless a gate explicitly tests growth;
- no explicit learned pair table while claiming morphology stores relations;
- renderer stays read-only;
- Gate 0 is linear routing;
- 3-D coordinates are not the primitive;
- clustering not established causal;
- slow global mixing insufficient;
- Gate 6 has no efficiency advantage over explicit tables;
- Gate 7 kills scalar endpoint reductions only;
- Gate 8 kills broad isotropic relation-memory generality;
- Gate 9 establishes an empirical operator, not its mechanism;
- no QM/phase/ferroic/growth/visual-world mechanism until a demonstrated residual specifically requires it.

## Instanton / QM / Feigenbaum

Parked. The instanton-side work supplied useful negative controls about unstable vacua and readout artifacts, plus a separate wave-reservoir experiment whose self-carving rule failed its own shuffle/learning tests. Nothing in Gate 9 requires tunneling, complex phase, fractal branching, or instanton dynamics.
