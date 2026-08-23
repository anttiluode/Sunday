# ATTRACTOR TEST — Sunday has a unique attractor and no sequence memory

Run against `anttiluode/Sunday@main` (through Gate 7), unmodified. The four
scripts here only call Sunday's public functions; nothing in `sunday/` is
edited. Put them in `experiments/` and run with `PYTHONPATH=.`.

## Why this test did not exist

All three substrates — `microarbor`, `nonlinear_overlap`, `composition` —
share one plasticity rule:

```
mass <- (1 - lr) * mass + lr * target( eligibility( mass ) )
```

and all three `initialize()` with `mass = np.ones(n)`. Every published gate
runs one fixed history from that one starting point. Nothing in the repo
therefore distinguishes

```
"the history wrote this structure"     (path dependence)
"this rule lands here regardless"      (a unique attractor, and the structure
                                        is a function of the program alone)
```

Both look identical if you only ever start from ones.

## Test 1 — perturbed initialisation (`attractor_test.py`)

Each substrate's own training program, run from 5 random initial mass fields
satisfying the same constraints the rule does: exact budget, mass floor,
ports pinned at 1.0. The perturbation is severe — heavy-tailed, initial
`sd` of 1.15 against the published `sd` of 0.0.

```
microarbor          corr(final mass)  mean 0.999553  min 0.999179
                    observable auc_A - auc_B  identical to 6 d.p. across all inits

nonlinear_overlap   seed 240000  corr 0.999976   pair_interaction(A,B)  sd 1.2e-05
                    seed 240001  corr 0.999982                          sd 1.4e-05
                    seed 240002  corr 0.999981                          sd 5.0e-06

composition         seed 400000  corr 0.999986   relation matrix sd across inits 0.05%
(Gate 6/7)          seed 400001  corr 0.999984                                   0.05%
                    seed 400002  corr 0.999977                                   0.04%
                    identical 15-entry sign pattern from every initialisation
```

**Sunday's plasticity is a contraction.** Start it anywhere legal and it lands
in the same place.

## Test 2 — episode order (`order_test.py`, `convergence_test.py`)

Same episodes, different order within each cycle. A small residual appears
and, crucially, does **not** decay as the fixed-point iteration is run longer:

```
cycles    max|dmass| fwd-vs-rev    d pair_interaction
   20        0.191491                 -0.0004385
   40        0.199893                 -0.0004491
   80        0.200112                 -0.0004494
  160        0.200110                 -0.0004494
  320        0.200110                 -0.0004494
```

So it is not incomplete convergence. But it is not memory either.

## Test 3 — it is measurement phase, not memory (`orbit_phase_test.py`)

The training loop applies three maps per cycle, so the converged material is
a **period-3 orbit**, not a point. Reading it after episode 3 rather than
episode 1 gives a different mass field with zero memory of anything. Measure
that wobble at the converged orbit:

```
orbit diameter (mass)              0.155227
orbit diameter (pair_interaction)  0.0004536
'order effect' from Test 2         0.200110  /  -0.0004494
```

The order effect and the intra-cycle wobble agree to within 1% on the scored
observable. **The order of episodes changes where in the orbit you stop, and
nothing else.**

## What this kills

`mass* = F(positions, program)`. Sunday is an equilibrium solver, not a
memory. Concretely:

- **"Signal-carved matter", "experience writes structure", "history becomes
  embodied in spatial transfer geometry"** all overclaim. `F` is a function
  of *which episodes exist*, not of what happened when.
- This substrate can never exhibit consolidation, interference, recency,
  primacy, or order fossilisation. In particular the ancestral
  `MorphogeneticNeuron` result that motivated the line — `A->B body !=
  B->A body` — is **not** inherited by Sunday. Measured above: it is phase.
- The right null to add is no longer an endpoint model. Since `mass*` is a
  deterministic function of the program, the sharp question is whether `F`
  computes anything a direct statistic of the program could not. That is
  Sunday's own resource attacker (the explicit pair table), and it is now the
  main undefeated one.

## What survives, and is arguably strengthened

- Gate 6/7's non-additivity is intact, and it is **not an initialisation
  lottery**: the identical 15-entry sign pattern appears from every starting
  material. The gates were not measuring seed luck.
- The AB-vs-CD effect is a genuine difference between two fixed points under
  **matched marginals**. Two different programs really do map to two
  different equilibria, and the difference is not endpoint-additive. That
  claim is unaffected.

The honest restatement: *a fixed geometry plus a mass-budget equilibrium rule
maps a training program to a unique structural equilibrium, and that
equilibrium encodes pair relations that no per-terminal scalar can express.*
That is a real and slightly odd result. It is just not learning.

## The fix, and it is the same one either way

A contraction has one attractor by definition. Path dependence needs
multi-stability. Winner-take-all does not supply it — tested independently in
the continuum medium at deposition exponent 2.5, still one attractor.
Hysteresis does: a local bistable latch with a coercive threshold that flips
at one drive level and holds until a lower one. Path-dependent by
construction, and the one ingredient that survives silence.

Gate 8 would then have a real pass condition, which today it cannot have:

> Train from several initial mass fields. If the finals no longer correlate
> at 0.999, and the observable spread across initialisations exceeds the
> intra-cycle orbit diameter, the material has become path-dependent.
