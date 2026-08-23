# Gate 6 preregistration — relation-matrix composition

Date: 2026-08-23

## Question

Gates 1–5 establish a robust pairwise phenomenon and show that topology/boundary alignment matters. Gate 6 stops asking about one pair at a time:

> **Can one fixed structural mass field store several coactivity relations simultaneously and expose them in a frozen pairwise interaction matrix, without explicit pair-specific learned weights?**

This gate tests composition/storage only. It does **not** test parameter efficiency.

## Fresh range

```text
380000..380009
```

Ten independent geometric substrates. These seeds have not been used for calibration or prior gates.

## Six-terminal geometry

Use the existing 256-element local radial graph, but protect one soma plus six input terminals. The terminals are equally spaced on the same input-side circle.

Two disjoint perfect matchings are chosen so every trained pair has the same adjacent-terminal geometric separation:

```text
M1: (1,2) (3,4) (5,6)
M2: (2,3) (4,5) (6,1)
```

They are rotations of one another around the six-terminal ring.

## Matched histories

Train two copies of the identical initial substrate:

```text
T1: present all three M1 pairs once per cycle
T2: present all three M2 pairs once per cycle
```

Each terminal is active exactly once per cycle in each program. Both programs therefore have identical per-terminal marginals, number of pair episodes, total source drive, soma sink drive, learning rate, epoch count, graph, total structural mass, and nonlinear readout.

No pair-specific weight or pair label is stored in the substrate.

## Freeze and probe

After training, freeze both mass fields.

For every unordered terminal pair among six terminals (15 pairs total), measure the same stable distributed nonlinear interaction used in Gates 2–5:

```text
I_T1(i,j)
I_T2(i,j)
dI(i,j) = I_T2(i,j) - I_T1(i,j)
```

Expected differential signs:

```text
edge in M1:  dI > 0   because T1 coactivity should reduce that pair's interaction
edge in M2:  dI < 0   because T2 coactivity should reduce that pair's interaction
unused pair: no registered sign
```

Thus six trained relations must coexist in the differential matrix: three positive and three negative according to which material experienced that pair.

## Controls

### Marginal-count control

Every terminal must occur once per cycle in M1 and once per cycle in M2.

### Fixed resource

Total structural mass remains exactly 256 in both trained materials. No element birth/deletion and no learned free-form edge table.

### Same-permutation mass shuffle

Apply one random permutation to the non-port masses of both trained materials, preserving each mass histogram and exact total budget while destroying its placement on the geometry. Re-probe the trained six edges.

### Uniform/no-plasticity sanity

Two identical uniform substrates have an exactly zero differential matrix by construction. This is a unit/sanity control, not scientific evidence.

### Explicit pair-table attacker

An explicit relation table trivially stores this toy task more cheaply. Even a 15-bit binary table for all unordered pairs is tiny compared with ~249 plastic floating masses, before graph storage is counted.

Therefore **Gate 6 must not claim description-length or memory efficiency**. A PASS means only that the distributed morphology can compose multiple relations without explicit pair-specific learned parameters.

## Primary metrics

For the six trained edges define an expected-signed differential:

```text
s(i,j) = +dI  for M1 edges
s(i,j) = -dI  for M2 edges
```

Then report:

```text
pooled expected-sign fraction across 10 x 6 trained edges
mean signed contrast
minimum / distribution of signed trained-edge effects
mean |dI| on trained edges
mean |dI| on the nine unused pairs
trained/unused differential-magnitude ratio
same-permutation shuffle signed contrast ratio
```

## Preregistered PASS receipt

All resource/finite checks must pass, plus:

```text
pooled trained-edge expected-sign fraction        >= 0.90
mean signed trained-edge contrast                 >= 0.00070
mean |trained dI| / mean |unused dI|              >= 5.0
mean shuffled signed contrast / original contrast <= 0.35
```

Also report the fraction of seeds with all 6/6 trained-edge signs correct, but it is secondary and has no pass threshold.

If the original mean signed contrast is non-positive, the shuffle ratio cannot rescue the gate.

## Interpretation if PASS

Safe statement:

> A fixed-budget distributed structural state can simultaneously encode several matched coactivity relations such that the frozen nonlinear pair-interaction matrix distinguishes which relations belonged to which training program, without explicit pair-specific learned weights.

That would move Sunday from a single pairwise effect toward a **relation-composing computational substrate**.

## Interpretation if FAIL

Do not add more terminals or capacity immediately. Determine whether interference, mass competition, geometry, or the nonlinear readout caused the failure. Sunday would remain a robust pairwise plastic-routing phenomenon rather than a compositional primitive.

## Calibration provenance

Consumed seeds `370000..370004` were used only to establish executability and freeze thresholds. All five had 6/6 trained-edge signs correct; signed contrasts ranged ~0.00087–0.00383; trained/unused differential ratios were ~12–20; shuffle contrast ratios were <=~0.21. None counts toward Gate 6.
