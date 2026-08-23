# Sunday — current handoff

Date: 2026-08-23

## Restart rule

Restart from receipts, not from the original 3-D/dendrite/QM metaphor.

Sunday's current question:

> **Can a fixed material substrate store and compose relations between inputs through topology + local plasticity, without explicit pair-specific weights?**

## Lineage in one screen

```text
Gate 0  signal writes spatial transfer                  PASS
        frozen dynamics exactly linear                  calculation claim KILLED

Gate 1  matched coactivity writes a pair relation       PASS
        distributed local nonlinearity reads relation

Gate 2  coordinates erased after graph construction     EXACT TIE
        non-geometric rewires retain weak relation       3-D necessity KILLED
        Euclidean locality amplifies relation            SURVIVES

Gate 3  progressive locality destruction                useful collapse
        clustering prereg misses threshold               GATE FAIL

Gate 4  random non-geometric low-gap modular graphs      PASS
        slow global mixing restores strong relation?     NO — KILLED

Gate 5  same graph, different input-role alignment       PASS
        boundary/topology alignment matters              SURVIVES
```

## Gate 0

256 fixed elements, fixed total mass, no element birth, no free learned edges. Signal history redistributes node mass and changes later transfer. Correct route ~1.4x over uniform and ~1.7x over mass shuffle.

But superposition holds to ~1e-17 whole-state error. Gate 0 is adaptive routing/structural memory, not a calculating dendrite.

## Gate 1

Matched programs:

```text
H_AB: [A+B], [C], [D]
H_CD: [C+D], [A], [B]
```

Every terminal occurs once per cycle in both histories; only coactivity grouping changes.

Fresh `240000..240019`:

```text
route sign                        20/20 both pairs
nonlinear interaction sign        20/20 both pairs
mean route separation             0.116056
mean nonlinear separation         0.008948
mass-shuffle signed ratio         ~0.04
```

Surprise: coactivity causes route **separation**, not Hebbian-style merging, under this fixed-budget current-reinforcement rule.

A later 15-point nonlinear operating sweep gave expected sign 180/180.

Safe statement: experience can write a pair relation into transfer geometry without explicit pair weights, and a fixed distributed local nonlinearity can read it as pairwise interaction.

## Gate 2

Stable abstract-graph attacker `300000..300011`:

```text
GEO route separation              0.121534
REWIRE |route|                    0.018915   ratio 6.425x
GEO nonlinear separation          0.008661
REWIRE |nonlinear|                0.001860   ratio 4.657x
same graph + xyz erased           exactly identical
rewire degree                     exact
node strength error               <1e-10
nonlocal edges                    ~0.88
```

The rewired graph still retained the qualitative pair relation on all seeds.

Therefore 3-D coordinates are not the execution-time primitive. Locality is a strong graph prior/constraint.

Gate-2 v0 remains invalid due nonlinear integrator overflow on attacker graphs; NaNs were never counted as geometry winning.

## Gate 3

Nested degree-preserving locality dial `320000..320005`:

```text
swaps/E   clustering   path   gap     nonlinear
0.0       .5865        2.992  .0716   .008354
0.1       .3494        2.271  .2361   .003079
0.5       .1224        2.088  .5661   .001604
1.0+      ~.105        ~2.06  ~.61    ~.0016-.0017
```

The effect collapses to ~20% after leaving the local regime. But preregistered `rho(clustering, |interaction|) >= .60` observed only `+.575`; Gate 3 FAILS. Do not call clustering causal.

## Gate 4

Low-gap non-geometric attacker `340000..340004`, three random balanced partitions per cloud = 15 attackers.

Random community bottlenecks were imposed on non-geometric graphs until spectral gap returned close to GEO while preserving degree and rematching node strength.

```text
GEO mean nonlinear interaction       0.007800
MODULAR recovery mean                 0.223308
MODULAR recovery median               0.209767
MODULAR max recovery                  0.468354
MODULAR <= .50 recovery               15/15
mean gap ratio                        1.006
minimum nonlocal-edge fraction        0.879
max clustering/GEO ratio              0.340
strength error                        <9.5e-11
```

Gate 4 PASS: low global mixing is not sufficient. Arbitrary bottlenecks in the wrong places do not restore the strong relation.

See `docs/GATE4_RESULT.md` and `receipts/gate4_low_gap_confirm5.json`.

## Gate 5 — boundary/topology alignment PASS

This is the cleanest causal topology result so far.

For each fresh seed `360000..360007`, build one valid non-geometric low-gap modular graph whose four physical terminals split 2+2 across its two communities. Freeze that graph.

There are exactly three perfect pairings of the four physical input nodes. One pairing puts both semantic pairs within communities (`ALIGNED`); the other two put both semantic pairs across the community boundary (`CROSSED`).

**The graph is identical between these arms.** Only which physical terminals are called A/B/C/D for the matched coactivity programs changes.

Receipt:

```text
mean ALIGNED nonlinear relation       0.002379
mean CROSSED relation                 0.000548
ratio                                 4.340x
ALIGNED > crossed mean                7/8
ALIGNED > both crossed pairings       7/8

mean ALIGNED route separation         0.034871
mean CROSSED route separation         0.015749
route ratio                           2.214x
```

All graph validity controls pass.

Important scars:

```text
360002: route alignment strengthens, but nonlinear interaction reverses sign
360003: almost silent graph; huge ratio is denominator-driven
```

Do not hide either.

Safe statement:

> **The same fixed topology can support a substantially stronger learned pair relation when semantic coactivity boundary conditions align with its internal community/corridor layout.**

This supports signal/topology alignment, not 3-D necessity and not a universal biological claim.

See:

```text
docs/GATE5_BOUNDARY_ALIGNMENT_PREREG.md
docs/GATE5_RESULT.md
receipts/gate5_boundary_alignment_confirm8.json
```

## What the object now looks like

The surviving mechanism is increasingly:

```text
fixed topology
 + where inputs land
 + which inputs arrive together
        ↓
local current history
        ↓
fixed-budget mass redistribution
        ↓
persistent relation between routes
        ↓
distributed local nonlinearity
        ↓
pairwise interaction
```

This is closer to a dendritic computational abstraction than a 3-D picture is. The key candidate primitive is **arranging where signals stay distinct and where they are allowed to meet**.

## Next gate — composition, not another topology statistic

Stop proving one pair forever.

Ask:

> Can one fixed mass budget experience several pair relations and later expose a structured interaction matrix without explicit pair-specific learned weights?

A clean first composition task should use more terminals and train multiple matched coactivity statistics while keeping every terminal's marginal activity equal. After freezing morphology, probe every terminal pair and ask whether the learned interaction matrix recovers the training relation graph.

Mandatory controls:

- same marginal terminal counts across relation programs;
- fixed total structural mass;
- no pair-specific learned edges/readout weights;
- shuffled structural mass;
- uniform/no-plasticity substrate;
- ordinary explicit pair-table attacker with byte/parameter accounting;
- test held-out seeds and relation graphs;
- do not reward merely storing one scalar per pair under another name.

If composition fails, Sunday remains an interesting pairwise plastic routing phenomenon rather than a general calculating primitive.

## Hard stop lines

- fixed total material unless a gate explicitly tests growth;
- no learned pair-specific edge weights while claiming morphology stores relations;
- rendering read-only;
- Gate 0 is linear routing;
- Gate 1 is not established Hebbian binding;
- 3-D coordinates are not the current primitive;
- clustering not established causal;
- slow global mixing insufficient;
- Gate 5 alignment does not guarantee nonlinear sign on every graph;
- no faces/VKITTI/CLIP/oscillations/ferroic/QM/growth/autonomous visual recurrence unless a specific residual requires them.

## QM / Feigenbaum notes

Both remain parked. Current Sunday has no complex phase or quantum mechanism, and no emergent fractal branching result. If either is introduced later, it needs its own matched attacker and receipt rather than a retrospective story.
