# Sunday — current handoff

Date: 2026-08-23

## Message to the next Sol instance

Do not begin by adding more ideas.

Sunday currently has one job:

> Determine whether repeated signal can redistribute a fixed amount of slow structural mass inside a fixed 3-D cloud so that later signal transfer depends on the learned spatial arrangement.

The project exists because several older lines now meet at a testable boundary:

- 3-D splats can be an inspectable material representation;
- morphology can define a transfer operator;
- traversal can change persistent conductance;
- fixed dormant capacity is a cleaner attacker than literal growth;
- local response geometry is more trustworthy than assigning semantic meaning to coordinates;
- rendering must never be recurrent state.

Do **not** turn this into a face, world-model, oscillation, chemistry, or biology project before Gate 0 is resolved.

## Current mainline

`main` contains only project memory/discipline. Active experimental work begins on:

```text
sol/gate0-signal-carved-microarbor
```

## Gate 0 registered question

Can a fixed amount of slow structural mass, redistributed by traversing signal inside a fixed 3-D cloud, create a spatially specific transfer operator?

### Fixed resources

```text
256 spatial elements
same xyz positions
same extents / base overlap graph
same soma and terminal locations
same initial uniform mass
same total mass budget
same fast dynamics
no birth / deletion
no pixel feedback
```

### Training histories

Two identical copies are trained separately:

```text
A: terminal A is source, soma is sink
B: terminal B is source, soma is sink
```

Local incident current supplies eligibility. Slow mass is moved toward repeatedly used regions, with a floor and strict projection back to the original total budget.

After training, mass freezes. Terminal-only impulses probe both frozen materials.

### Required receipt

The exact thresholds live in the Gate 0 branch, but the intended qualitative receipt is:

1. A-trained material transmits A better than B by a registered margin.
2. B-trained material transmits B better than A by a registered margin.
3. Correct-terminal transfer beats the uniform-material baseline.
4. Shuffling the learned mass values among the same non-terminal positions, preserving the exact mass histogram and budget, substantially damages the trained-terminal transfer.
5. Calling the observer/render path does not change state or later trajectories.

If these fail, do not rescue the gate by tuning the story after seeing the result. Record the failure and decide what mechanism actually died.

## Local pre-repo calibration

Before committing the branch implementation, a deterministic NumPy scratch version was run with 256 fixed points. This is **engineering calibration, not an accepted scientific receipt**.

Representative peak soma response values were approximately:

```text
uniform:  A 9.76e-5   B 1.00e-4
A-trained A 1.23e-4   B 9.17e-5
B-trained A 8.00e-5   B 1.34e-4
```

Thirty geometry shuffles reduced correct-terminal peak response to roughly half of the unshuffled learned geometry (about 1.9x learned/shuffle mean in that scratch run).

These numbers are useful only to show that the proposed gate is executable and not obviously numerically dead. The committed implementation must reproduce its own printed receipt and tests.

## Things not to silently change

- Do not increase the number of elements in one arm.
- Do not let total mass grow.
- Do not add learned edge weights independent of geometry.
- Do not make the renderer part of the update.
- Do not hand-design a tree or preferred path.
- Do not call a mass picture a dendrite before the shuffle/function tests survive.
- Do not use a learned 3-D decoder in Gate 0.

## Feigenbaum / branching note

The conversation that started Sunday included the naive question "what are Feigenbaum trees?" and the intuition of odd replicating branching things. Keep this as a parked observation. If branching, repeated motifs, or bifurcation cascades emerge from later material dynamics, quantify them then. Gate 0 must not assume them.

## Intended next sequence

```text
Gate 0  spatial mass -> functional transfer
   |
   +-- fail: identify whether learning rule, geometry, or morphology claim died
   |
   +-- survive
         v
Gate 1  same event multiset, different order -> persistent different machine
         v
Gate 2  full local transfer-rig / impulse-response atlas
         v
Gate 3  autonomous passing modes / rhythm, only if still justified
```

Update this file before any long break or branch transition.
