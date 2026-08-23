# Gate 10 preregistration — dormant write/read Jacobian

Date: 2026-08-23

## Question

Gate 9 measured an empirical finite-training relation operator over the seven-dimensional controlled program span. The next mechanistic null is:

> **Is that operator already latent in the dormant graph plus the existing local write/read rules, or is it created only by nonlinear structural evolution across 40 training cycles?**

Gate 10 changes no physical mechanism.

## Development / calibration provenance

Consumed development seeds:

```text
450000..450001
```

They are not Gate-10 evidence.

The symmetric read perturbation was checked at `epsilon = 0.125, 0.25, 0.5, 1.0`; the operator prediction and mode alignment changed negligibly across that range. Freeze:

```text
epsilon = 0.25
```

For the two development substrates, using a per-seed optimal scalar only as a diagnostic:

```text
seed      first-order NMSE   mean cosine   top-3 input mode cosines vs finite
450000        0.08713          0.95829      0.9993  0.9901  0.9743
450001        0.06445          0.95436      0.9998  0.9988  0.9932
```

The one-step write-only Gram attacker gives NMSE `0.9196 / 0.9976` after receiving its own optimal per-seed scalar. A same-permutation write-location attacker gives `0.9648 / 0.6150`, also after its own optimal per-seed scalar.

A single pooled least-squares gain was calibrated from the two development substrates and is now frozen:

```text
GLOBAL_GAIN = 4.805610803751662
```

Using that one frozen gain, development NMSE is `0.09390 / 0.06530`.

## Fresh range

```text
460000..460003
```

Four independent random substrates. No Gate-9 or Gate-10 calibration seed is reused.

## One-step structural write matrix W

Start from the dormant material:

```text
mass_i = 1 for all elements
same seeded base graph as the finite experiment
```

For each of the 15 unordered terminal pairs `e=(i,j)`:

1. run exactly one existing `teacher_episode` from dormant mass;
2. apply exactly one existing `redistribute_mass` update;
3. record

```text
w_e = mass_after - mass_dormant.
```

Stack these rows into

```text
W : 15 x 256.
```

No labels from Gate-9 outputs are used.

## Dormant read derivative

For each one-step write direction `w_e`, construct two dormant materials

```text
m_plus  = 1 + epsilon * w_e
m_minus = 1 - epsilon * w_e
```

with `epsilon=0.25`.

Freeze mass and measure the full 15-entry nonlinear pair-interaction vector `F(m)` using the same readout as Gates 6–9.

Define the central directional derivative

```text
D_e = [F(m_plus) - F(m_minus)] / (2 epsilon).
```

Stack rows into `D : 15 x 15`.

Gate-9 code vectors use `+1` for arm A and `-1` for arm B, while the measured finite output is `F(B)-F(A)`. Therefore the dormant first-order relation operator is

```text
B0 = -D.
```

For the 16 registered controlled directions `Q`, the completely dormant prediction is

```text
Y0 = Q B0.
```

The only amplitude calibration allowed on fresh substrates is the frozen development scalar:

```text
Y_hat = GLOBAL_GAIN * Y0.
```

No fresh finite-training output is used to fit direction, edge gains, modes or per-seed scale.

## Finite target

For each fresh seed, independently run the unchanged Gate-9 finite experiment:

```text
16 controlled relation directions
40 training cycles
frozen 15-pair interaction vector for each direction
```

Call the resulting `16 x 15` matrix `Y_finite`.

This is the target only.

## Primary zero-shot prediction receipt

Per seed and pooled, report:

```text
frozen-gain NMSE(Y_hat, Y_finite)
mean per-direction cosine(Y_hat_r, Y_finite_r)
flattened cosine(Y0, Y_finite)
```

A per-seed optimal scalar may be reported only as a diagnostic and cannot enter the pass/fail prediction.

## Preferred-mode comparison

Fit the Gate-9 minimum-norm finite operator only for analysis:

```text
B_finite = argmin ||Q B - Y_finite||.
```

Project `B0` onto the identifiable rank-7 input span of `Q` before comparing singular modes.

Report:

```text
top-3 energy fraction of projected dormant B0
principal cosines between top-3 dormant and finite input singular subspaces
```

The finite operator is not used to modify `B0`.

## Attacker 1 — write-only similarity

Ignore the read Jacobian and use only overlap among one-step structural write directions:

```text
B_write = - W W^T.
Y_write = Q B_write.
```

Give this attacker an **optimal scalar on each fresh seed**, which is more help than the primary model receives. Score NMSE.

If this competes with the composite dormant operator, the read sensitivity is unnecessary.

## Attacker 2 — same-permutation write-location surgery

Apply one deterministic permutation `P` of the internal (non-port) mass coordinates to **every** row of `W`:

```text
W_perm = W P.
```

This preserves exactly:

```text
each write-direction norm
all pairwise write-direction dot products
W W^T
mass sum of every write direction
```

but destroys where each structural change lands relative to the dormant graph/read sensitivity.

Repeat the central read derivative using the permuted `w_e` rows to produce `B_perm` and `Y_perm`.

Give this attacker its own optimal scalar per fresh seed and score NMSE.

If it competes with the true dormant operator, write/read spatial alignment is not load-bearing.

## Controls

- same 256-element seeded substrate as finite target;
- exact existing teacher, redistribution and nonlinear readout rules;
- fixed total structural mass;
- ports remain fixed at mass 1;
- `epsilon=0.25` frozen before fresh range;
- `GLOBAL_GAIN=4.805610803751662` frozen before fresh range;
- no fresh per-seed fitting in the primary prediction;
- same permutation across all write directions in the permutation attacker;
- all values finite.

## Preregistered receipt

Primary zero-shot finite-output prediction:

```text
mean fresh frozen-gain NMSE                 <= 0.15
mean fresh per-direction cosine             >= 0.90
```

Dormant preferred modes:

```text
mean projected dormant top-3 energy         >= 0.90
mean over seeds of weakest top-3
  dormant-vs-finite principal cosine        >= 0.85
```

Mechanism attackers, each granted its own optimal fresh scalar:

```text
primary frozen-gain NMSE / write-only NMSE  <= 0.25
primary frozen-gain NMSE / permuted NMSE    <= 0.35
```

Conservation:

```text
max one-step write mass-sum error           < 1e-10
max finite trained mass-budget error         < 1e-10
all values finite
```

**Gate 10 passes only if every block above passes.**

## Interpretation if PASS

Safe statement:

> The preferred relation-space transformation measured after long training is already largely determined by the dormant graph and the local write/read sensitivities. Long training primarily amplifies a pre-existing operator rather than inventing its dominant relation modes.

A pass would not mean the 40-cycle evolution is exactly first-order: residual NMSE quantifies the nonlinear finite-training correction.

## Interpretation if FAIL

Failure location matters:

- poor output cosine -> first-order dormant mechanism has the wrong relation mixing;
- good cosine but poor frozen-gain NMSE -> operator shape is latent but finite-training amplification is substrate-dependent;
- modes disagree -> apparent Gate-9 low-rank structure is generated by training evolution;
- write-only competes -> read Jacobian is unnecessary;
- same-permutation attacker competes -> spatial alignment between writes and read sensitivity is not the mechanism.

Do not tune learning to rescue the gate.
