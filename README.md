# Sunday

**Signal-carved 3-D computational matter.**

Sunday asks one narrow question:

> Can repeated signal redistribute a fixed amount of dormant 3-D splat matter into a persistent morphology that changes how later signals propagate?

The ambition is dendrite-like computation, but the word **dendrite** has to be earned. A branch-shaped rendering is not enough. Sunday only has a dendrite candidate if:

1. where an input lands matters;
2. 3-D morphology determines subsequent transfer;
3. previous traversal changes persistent local structure/conductance;
4. the changed structure changes future transfer under the same test input.

## Where the ingredients came from

Sunday is a fusion only at the level of surviving mechanisms:

- **WorldModel / WorldSplat** supplied inspectable 3-D splat primitives.
- **BlockNeuron** supplied the question `morphology -> transfer operator` and the idea that traversal can write future conductance.
- **SplatNeuron / Slapstack** supplied the lesson that fixed dormant capacity and graded usefulness are cleaner than theatrical birth/death rules.
- **SplatWorld2** supplied two crucial rules: interrogate local response geometry rather than assigning semantics to coordinates, and never let a lossy display become recurrent state.

Sunday does **not** initially import faces, VKITTI, CLIP, oscillations, ferroelectric claims, biological realism, or a learned decoder. Those can only enter after a smaller gate earns them.

## Architectural invariant: pixels are never state

The true state is numerical material:

```text
position r_i
extent   sigma_i
fast     v_i(t)
slow     mass m_i
```

A renderer may observe that state:

```text
material state ---> dynamics
       |
       +----------> renderer ---> human
```

but never:

```text
renderer -> pixels -> encoder -> next material state
```

A correct observer must be removable without changing the trajectory. This is Sunday's stronger descendant of SplatWorld2's immutable-anchor anti-fire lesson.

## Gate 0 — signal-carved microarbor

Start with a seeded cloud of **256 fixed 3-D elements**, one soma site and two input terminals. All runs begin with the same positions, same uniform structural mass, same total mass budget, and same dynamics.

Spatial overlap determines baseline coupling. Current structural mass modulates that coupling. Training drives current between one terminal and the soma; local current eligibility redistributes slow mass under a strict global budget. No element is born or deleted.

Two copies receive different histories:

```text
history A: repeatedly drive terminal A <-> soma
history B: repeatedly drive terminal B <-> soma
```

Learning is then frozen. Both copies receive the same terminal-only probes.

Gate 0 asks whether the learned structure is functionally spatial rather than merely a changed histogram of scalar values.

Required controls include:

- uniform untrained material;
- cross-terminal probes;
- mass-budget equality;
- shuffling the learned masses among the same 3-D positions while preserving the exact mass multiset;
- observer/render-on versus observer/render-off trajectory equality.

See `docs/GATES.md` and the active gate branch.

## Gate discipline

A gate is not a chapter number. It is a registered falsifier.

Every gate must state:

```text
question
mechanism being changed
what is held fixed
controls / attackers
receipt required to advance
kill or demotion condition
```

Negative results remain in the repository. If an ingredient fails, later gates do not quietly redefine what it was supposed to prove.

## A note on Feigenbaum trees

The motivating conversation included the naive question, "what are Feigenbaum trees?" and the image of odd replicating/branching structures. Sunday deliberately does **not** assume that replicated tree geometry is the answer. If branching, repeated motifs, bifurcation cascades, or self-similar structure appear later as a consequence of signal/material dynamics, we can measure them then. Tree-ness is currently an observation to watch for, not a mechanism to install.

## Status

The repo begins on **2026-08-23**. Main holds the charter, gate protocol, kill ledger and current handoff. Experimental work proceeds on gate branches and is promoted only with a receipt.
