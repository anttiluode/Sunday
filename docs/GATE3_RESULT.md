# Gate 3 — FAIL, with a sharper topology residual

Date: 2026-08-23

Fresh confirmation range:

```text
320000..320005
6 seeds x 6 nested topology levels = 36 points
```

## Verdict

**Gate 3 FAILS its preregistration.**

The failure is narrow but must be honored: the preregistered pooled Spearman correlation between mean clustering and absolute nonlinear interaction was required to be `>= +0.60`; observed was:

```text
rho(clustering, |interaction|) = +0.5750
```

Do not round or reinterpret this as a pass.

The preregistered normalized-Laplacian spectral-gap condition did pass:

```text
rho(lambda_2, |interaction|) = -0.6788
required <= -0.60
```

## Level means

```text
swaps/E  clustering  path     gap     long edges  route sep  nonlinear sep
0.0      0.5865      2.9920   0.0716  0.0000      0.11497    0.008354
0.1      0.3494      2.2715   0.2361  0.1790      0.07022    0.003079
0.5      0.1224      2.0875   0.5661  0.5940      0.02263    0.001604
1.0      0.1050      2.0683   0.6066  0.7788      0.02032    0.001561
2.0      0.1052      2.0631   0.6132  0.8646      0.02105    0.001716
5.0      0.1053      2.0591   0.6177  0.8803      0.01528    0.001662
```

The early regime transition is strong:

```text
clustering at 0.5E / GEO                 0.2086
|interaction| at 0.5E / GEO             0.1920
saturated |interaction| (2E,5E) / GEO   0.2022
```

All snapshots remained connected, preserved exact unweighted degree sequence, and matched original node strengths with maximum relative error `< 1e-10`.

## What the failed gate still tells us

The topology dial does support a broad regime statement:

> The strong Gate-1 relation lives in the local / poorly mixed graph regime. Once the graph is heavily rewired, the effect falls toward the small generic-graph floor found in Gate 2.

But Gate 3 does **not** identify clustering as the carrier.

The topology variables co-vary strongly under rewiring, so the preregistered clustering threshold was deliberately a test of whether clustering was an unusually good descriptive candidate. It missed.

## Post-hoc diagnostics — hypotheses only

These were not preregistered and must not be counted as Gate-3 evidence:

```text
rho(mean shortest path, |interaction|)   +0.7205
rho(long-edge fraction, |interaction|)   -0.5994
rho(transitivity, |interaction|)         +0.5686

rho(clustering, |route separation|)      +0.6190
rho(spectral gap, |route separation|)    -0.7807
rho(mean shortest path, |route sep|)     +0.8216
rho(long-edge fraction, |route sep|)     -0.6990
```

The stronger post-hoc candidates are therefore **mixing / corridor length / spectral organization**, not triangle count alone.

A plausible mechanistic picture is:

```text
local / low-gap graph
    -> signals remain organized into distinguishable corridors longer
    -> node-mass competition can sculpt pair-specific routes
    -> distributed local nonlinearity sees a stronger pair relation

expander-like / high-gap graph
    -> activity mixes broadly and quickly
    -> route identities become diffuse
    -> the same learning rule leaves only a weak generic graph effect
```

This is a hypothesis, not yet a result.

## Next causal attacker

Do not simply run more correlations.

Construct a **non-geometric, highly nonlocal graph with low spectral gap / long mixing time** while keeping degree and node strength matched. For example, impose random communities unrelated to xyz using degree-preserving swaps.

Then ask:

> If slow mixing is restored without Euclidean locality or high geometric clustering, does the strong relational effect return?

If yes, the useful object may be modular/corridor topology rather than 3-D geometry.
If no, some more specifically geometric/local structure remains missing.

That is a substantially sharper next gate than adding biology.
