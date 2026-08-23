# Sunday — current handoff

Date: 2026-08-23

## Message to the next Sol instance

Do not restart this project from the motivating metaphor. Restart it from the receipts below.

Sunday began with the question:

> Can repeated signal write persistent 3-D transfer structure into a fixed amount of computational material, and can that structure become more than routing?

Two gates have now separated those questions.

## Branch lineage

```text
main
  charter / gate protocol / kill ledger / initial handoff

sol/gate0-signal-carved-microarbor
  Gate 0 implementation + receipt
  exact linearity attacker

sol/gate1-local-nonlinear-overlap
  inherits Gate 0
  Gate 1 implementation + held-out confirmation
  CURRENT ACTIVE BRANCH
```

## Gate 0 — PASS, but narrower than the dream

Question:

> Can signal redistribute a fixed slow-mass budget in a fixed 3-D cloud so later transfer depends on the learned spatial arrangement?

Answer: **yes in this instrument.**

Fixed resources:

```text
256 elements
same xyz positions
same base geometry graph
same initial uniform mass
total mass budget = 256
no birth/deletion
no learned free-form edges
no pixel feedback
```

First deterministic receipt:

```text
A selectivity                 1.3286x
B selectivity                 1.5472x
A gain over uniform           1.3900x
B gain over uniform           1.4548x
A gain over mass shuffle      1.7370x
B gain over mass shuffle      1.7506x
observer on/off trace         exactly identical
mass budget                   preserved
```

Files:

```text
sunday/microarbor.py
experiments/gate0_signal_carved_microarbor.py
receipts/gate0_v0.json
docs/GATE0_SIGNAL_CARVED_MICROARBOR.md
```

Safe statement:

> Signal history can become persistent spatial transfer geometry under a fixed material budget.

### Gate 0 linearity attacker — attacker WINS

The frozen fast dynamics are linear. Whole-state superposition errors are only floating-point roundoff:

```text
R(A+B) - [R(A)+R(B)]  ~ 1e-17 max
soma error             ~ 1e-19
R(2A) - 2R(A)          exactly 0 in the tested run
```

Therefore Gate 0 is **routing / structural memory, not a dendritic calculating primitive**.

Files:

```text
experiments/gate0_linearity_attacker.py
docs/GATE0_LINEARITY_ATTACKER.md
```

Do not forget this negative result later just because a 3-D plot looks dendritic.

## Gate 1 — PASS: coactivation history writes a pair relation

Gate 1 asked a stronger question:

> With each terminal used equally often, can changing only which inputs co-occur write a pair-specific relationship into the transfer geometry, and can a fixed distributed local nonlinearity read that structural relation as an interaction?

Four ports A/B/C/D are fixed symmetrically. Internal material is still a random 256-element 3-D cloud.

Matched programs:

```text
H_AB:
  [A+B together]
  [C alone]
  [D alone]

H_CD:
  [C+D together]
  [A alone]
  [B alone]
```

Every cycle uses A, B, C and D exactly once in both histories. Same episode count, same total source/sink drive, same learning rule, same mass budget. Only coactivation grouping changes.

### Surprise

The exploratory seed did **not** show "coactive inputs wire together." It showed the opposite under this current-reinforcement/resource-budget rule:

> the coactive pair later had *less overlapping internal transfer routes*.

Do not retrofit a Hebbian story onto this. The sign/mechanism is unresolved.

### Held-out confirmation

After the exploratory seed, thresholds were frozen and seeds `240000..240019` were run.

Results:

```text
AB route-separation positive fraction        20/20
CD route-separation positive fraction        20/20
AB interaction-separation positive fraction  20/20
CD interaction-separation positive fraction  20/20

mean route-overlap separation                0.116056
mean nonlinear interaction separation        0.008948

mean |soma-only effect|                      8.64e-06
distributed / soma-only ratio                1035.7x

mass-shuffle signed ratio, overlap            0.0400
mass-shuffle signed ratio, interaction        0.0418

max mass-budget error                         5.68e-14
```

The ~1036x ratio is mostly because the soma-only effect is almost zero. Do **not** hype the absolute effect: the normalized distributed interaction program effect is about **0.9 percentage points**. Small, but very consistent.

Files:

```text
sunday/nonlinear_overlap.py
experiments/gate1_local_nonlinear_overlap.py
docs/GATE1_LOCAL_NONLINEAR_OVERLAP.md
receipts/gate1_confirm20.json
tests/test_gate1.py
```

Quick reproduction:

```bash
python -m unittest discover -s tests -v
python experiments/gate1_local_nonlinear_overlap.py
```

Full stored confirmation:

```bash
python experiments/gate1_local_nonlinear_overlap.py --seed-start 240000 --seeds 20 --json
```

## What Gate 1 may mean

The strongest current interpretation is not "a neuron has been built." It is:

> Experience can write a *relation between inputs* into spatial transfer geometry without pair-specific learned weights. A fixed local nonlinearity later turns route overlap into a pairwise interaction.

That is the first Sunday result closer to a calculating primitive than mere adaptive routing.

The interesting object is the **local transfer relation**, not the visible branch shape.

## Things the next instance must not silently change

- Keep total material mass fixed unless a new gate explicitly tests growth.
- Do not introduce learned edge weights independent of geometry and still call the result a morphology effect.
- Do not feed rendered pixels back into state.
- Do not hand-design an internal tree.
- Do not call Gate 0 nonlinear; the superposition attacker killed that interpretation.
- Do not describe Gate 1 as Hebbian binding; coactivation currently produces route *separation*.
- Do not use the 1036x soma ratio without also stating the absolute interaction effect is ~0.009.
- Do not claim Euclidean 3-D is necessary. An abstract graph can reproduce the current conductance matrix; that attacker remains open.
- Do not bring faces, VKITTI, CLIP, oscillations, ferroic hysteresis or world-model recurrence into the active mechanism yet.

## Feigenbaum / branching note

The initiating conversation included the naive question "what are Feigenbaum trees?" and the image of strange replicating/branching structures. It remains deliberately parked.

If later dynamics produce branching, repeated motifs, bifurcation cascades or self-similar geometry **without us planting them**, measure them. Do not install a fractal/tree generator and then claim emergence.

## Immediate next falsifiers

Before Gate 2 gets a grand name:

1. **Robustness sweep** — vary local nonlinear strength and probe amplitude. Gate 1 must not exist at one tuned operating point.
2. Vary overlap radius, learning rate and mass floor.
3. **Abstract-graph attacker** — discard xyz after constructing the graph and ask what, if anything, 3-D locality contributes beyond a sparse graph parameterization.
4. **Composition gate** — can several learned pair relations support a real discrimination/calculation without adding explicit pair weights?
5. Only then consider persistent local state/hysteresis, order sensitivity, autonomous passing modes, or actual growth.

The project is currently interesting because each new mechanism has been forced to answer for a specific residual. Keep it that way.
