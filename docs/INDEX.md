# Sunday document index

Sunday accumulated many gate documents in one day. This file is the map; it is not another result.

## Start here

1. [`../README.md`](../README.md) — current project introduction after the reservoir/symmetry audit.
2. [`../HANDOFF_CURRENT.md`](../HANDOFF_CURRENT.md) — exact restart state and surviving residuals.
3. [`AUDIT_RESULT.md`](AUDIT_RESULT.md) — fixed-reservoir/readout and six-terminal symmetry audits.
4. [`../KILL_LEDGER.md`](../KILL_LEDGER.md) — interpretations that may not be silently resurrected.

## The shortest path through the science

If you do not want to read every gate, the important arc is:

```text
Gate 0     history can write persistent transfer
             but fast frozen dynamics are linear

Gate 1     equal-marginal coactivity writes a pair relation

Gates 2-5  3-D itself dies; topology and input/topology alignment matter

Gates 6-7  several relations coexist; endpoint-scalar explanations die

Gate 8     arbitrary/isotropic relation memory fails

Gates 9-10 anisotropic relation operator + dormant first-order predictor

Gate 11    dormant write geometry can route a weak relation prospectively

Gate 12    read-aware incremental-control claim narrowly fails

AUDIT       fixed-reservoir/readout null explains the broad operator story;
            ordinary six-terminal symmetry explains most of the 3-mode story
```

## Gate groups

### Foundations: Gates 0–1

Look for:

```text
GATE0_SIGNAL_CARVED_MICROARBOR.md
GATE0_LINEARITY_ATTACKER.md
GATE1_LOCAL_NONLINEAR_OVERLAP.md
GATE1_ROBUSTNESS_SWEEP.md
```

These establish the basic persistent-mass mechanism and then kill the temptation to call linear adaptive routing a calculating dendrite.

### Topology attackers: Gates 2–5

These ask whether the pair relation requires 3-D coordinates, clustering, slow mixing, or instead depends on how boundary inputs align to topology.

Key conclusions:

```text
3-D coordinates necessary        no
clustering sufficient            not established
low spectral gap sufficient      no
same graph + different port use  can change relational writability
```

The exact filenames begin with `GATE2_`, `GATE3_`, `GATE4_`, and `GATE5_`.

### Relational memory: Gates 6–8

These are the strongest pre-audit evidence for something more specific than reservoir projection.

```text
Gate 6   compositional six-terminal relation matrix
Gate 7   additive/multiplicative endpoint nulls
Gate 8   independent relation-code generality failure
```

Gate 8 is a failure on purpose: it is what exposed the anisotropic writable relation space.

### Tomography and dormant prediction: Gates 9–10

```text
Gate 9   relation-space operator tomography
Gate 10  dormant one-step WRITE + READ Jacobian
```

These results are real but their broad interpretation is now demoted by the audit. Read `AUDIT_RESULT.md` immediately after them.

### Pre-training control: Gates 11–12

```text
Gate 11  WRITE-only routing        PASS
Gate 12  READ-aware clean routing  FAIL at preregistered 1.08 threshold
```

Do not continue optimizing the same C3/18-route toy merely to make Gate 12 pass.

## Audit files

```text
AUDIT_PLAN.md
AUDIT_RESULT.md

../experiments/audit_reservoir_null.py
../experiments/audit_ring_symmetry.py

../receipts/audit_reservoir_null_fresh6.json
../receipts/audit_ring_symmetry_fresh4.json
```

## Receipts are evidence, docs are interpretation

When numbers disagree between prose written at different times, prefer:

1. the registered fresh JSON receipt;
2. the matching result document;
3. the current handoff;
4. old exploratory prose last.

Never rerun a stored confirmation range, tune the mechanism, and overwrite its meaning.
