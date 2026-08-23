# Gate 9 preregistration — writable-subspace tomography

Date: 2026-08-23

## Question

Gate 8 showed that balanced pair-relation directions are not equally writable/readable. Some are clean, some diffuse, and some rotate into other directions.

Gate 9 stops treating those outcomes as four separate cases and asks:

> **Is there a stable low-dimensional operator that maps a registered relation-training direction to the frozen relation vector written by the substrate?**

This gate changes no physical mechanism. It only expands the controlled relation-program family and analyzes the resulting input/output map.

## Development / calibration provenance

Consumed development seeds:

```text
430000..430001
```

They are not Gate-9 evidence.

The complete controlled program family was enumerated before the fresh range. On six terminals there are 16 unique contrasts satisfying all of:

```text
A and B are perfect matchings
A and B share no trained edge
every terminal occurs once in A and once in B
A and B have the same circular pair-distance multiset
code sign is canonicalized to remove q versus -q duplicates
```

Their 15-edge registered vectors span rank **7**. Removing any one of the 16 directions leaves training rank 7, so leave-one-direction-out prediction is identifiable over the admissible input span.

Development diagnostics:

```text
seed       full-linear LOO NMSE   mean cosine   identity NMSE   diagonal NMSE   top-3 operator energy
430000          0.001497            0.99902         0.8163          0.6148             0.9722
430001          0.000983            0.99948         0.7947          0.4299             0.9934
```

A rank-3 truncated operator, still evaluated leave-one-direction-out, gave:

```text
seed       rank-3 LOO NMSE       mean cosine
430000          0.04363             0.95184
430001          0.01164             0.98614
```

The top-three **input** singular subspaces from the two development substrates had principal cosines:

```text
0.989, 0.972, 0.934
```

These values were used only to freeze the generous thresholds below.

## Fresh range

```text
440000..440003
```

Four independent random substrates. Each substrate is interrogated with all 16 controlled relation directions.

## Registered input matrix Q

For each program contrast `r`, define a 15-edge row vector:

```text
q_r(i,j) = +1  if pair (i,j) belongs to arm A
           -1  if pair (i,j) belongs to arm B
            0  otherwise
```

Stack the 16 rows into `Q`.

Required design facts:

```text
Q shape                   16 x 15
rank(Q)                   7
rank(Q without row r)     7 for every r
```

## Measured output matrix Y

For each substrate seed and each registered direction:

1. train arm A and arm B exactly as in Gates 6–8;
2. freeze learning;
3. probe all 15 terminal pairs;
4. compute the differential interaction vector `y_r = dI`;
5. stack all 16 output rows into `Y`.

No pair-specific weights or endpoint embeddings are introduced.

## Primary attacker — leave-one-direction-out linear operator

For each held-out direction `r`:

1. fit the minimum-norm linear operator `B` on the other 15 rows:

```text
Q_train B ~= Y_train
```

2. predict the unseen frozen relation vector:

```text
y_hat_r = q_r B
```

3. score the held-out 15-vector only.

Aggregate across all 16 held-out directions.

Metrics:

```text
LOO normalized MSE = sum ||y_hat-y||^2 / sum ||y||^2
mean held-out cosine(y_hat, y)
```

This is the central falsifier. An in-sample operator fit does not count.

## Simpler attackers

Two deliberately simpler held-out models are scored identically:

### Scalar identity/gain

```text
y_hat = g q
```

One scalar `g` fit on the 15 training directions. This asks whether the substrate merely preserves/amplifies the taught relation pattern.

### Edge-diagonal gain

```text
y_hat_j = d_j q_j
```

One gain per physical pair edge, with no cross-edge rotation. This asks whether Gate 8 can be explained by fixed per-edge ease/difficulty rather than a genuine mixing operator.

## Low-rank operator

For every LOO full operator fit, take its rank-3 SVD truncation and predict the held-out direction with that truncated map.

Also fit the full operator on all 16 directions solely for descriptive singular-spectrum/subspace measurements. Those in-sample spectra are **not** the prediction receipt.

Report:

```text
fraction of operator Frobenius energy in top 3 singular values
rank-3 LOO NMSE
rank-3 LOO mean cosine
```

## Cross-seed preferred-mode stability

For each fresh seed fit the all-direction minimum-norm operator only for mode analysis. Compare every pair of seeds using the top-three **input** singular subspaces.

Report the three principal cosines for each seed pair and the pooled mean of the smallest of the three. Input modes are primary because they answer which registered relation directions the substrate preferentially accepts; output modes may rotate more strongly and are descriptive only.

## Controls

- exact 256-element mass budget;
- unchanged Gate-6/7/8 dynamics and nonlinear probe;
- exact terminal marginals inside every A/B contrast;
- exact within-contrast circular distance multiset;
- no common trained edge between A/B;
- no code direction selected after seeing fresh results;
- no endpoint-factor or pair-table fit inside the material.

Gate 8 already established that same-permutation mass shuffle destroys the learned registered contrast (`~0.105` pooled ratio). Gate 9 does not spend another factor of two in readout cost re-proving that control; it tests the structure of the surviving write/read map.

## Preregistered receipt

Design and conservation:

```text
code count                              = 16
registered input rank                   = 7
all leave-one-out training ranks        = 7
max mass-budget error                   < 1e-10
all values finite
```

The full held-out linear operator must satisfy, pooled across fresh seeds:

```text
mean per-seed full-linear LOO NMSE      <= 0.020
mean per-seed held-out cosine           >= 0.980
```

and must materially beat both simpler attackers:

```text
full-linear NMSE / scalar-gain NMSE     <= 0.10
full-linear NMSE / diagonal-gain NMSE   <= 0.10
```

The compact-mode claim requires:

```text
mean top-3 operator energy fraction     >= 0.90
mean rank-3 LOO NMSE                    <= 0.10
mean rank-3 held-out cosine             >= 0.90
```

Preferred input modes count as cross-seed stable only if:

```text
mean over seed-pairs of the smallest top-3 principal cosine >= 0.75
```

**Gate 9 passes only if every block above passes.**

## Interpretation if PASS

Safe statement:

> Over the seven-dimensional controlled relation-program span, Sunday's fixed structural learning dynamics act approximately as a predictable linear write/read operator, and most of that operator's energy lies in a small set of cross-seed-stable preferred input modes.

This would explain Gate 8's apparent successes/failures as direction-dependent gain and rotation rather than four unrelated accidents.

It would **not** mean the underlying material dynamics are globally linear, nor that three modes are universally sufficient outside this fixed training amplitude/program family.

## Interpretation if FAIL

The failure location matters:

- full linear LOO fails -> the relation map is nonlinear/context-dependent at this training amplitude;
- full linear succeeds but rank-3 fails -> stable operator, but not compact;
- within-seed succeeds but input modes are unstable across seeds -> writable geometry is substrate-instance specific;
- diagonal attacker matches full -> no evidence for cross-edge relational rotation; fixed per-edge gains suffice.

Do not rescue a failed block by changing the learning rule inside this gate.
