# Gate 2 v0 — INVALID nonlinear comparison

Date: 2026-08-23

Branch:

```text
sol/gate2-abstract-graph-attacker
```

Frozen held-out range had been registered as:

```text
280000..280011
```

The run was stopped after seed `280006` because the attacker arm exposed a numerical defect in the comparison.

## What failed

Gate 1's distributed cubic probe uses explicit Euler at the ordinary material timestep:

```text
dt = 0.035
gamma = 50
probe amplitude = 10
```

For GEO this operating point remained finite. For degree+strength-matched rewires at held-out seeds `280005` and `280006`, the learned graph produced states large enough that the explicit cubic step overflowed and returned `NaN` interaction values.

Those NaNs are **not evidence that geometry wins**. They mean the nonlinear comparison is numerically invalid for those attacker topologies.

Per project protocol, do not patch the integrator and continue using the same confirmation range.

## Valid observations that survive the invalidation

The following are algebraic/linear observations and are not invalidated by the cubic overflow:

1. Copying the exact base graph and erasing coordinates gives exactly the same training and route metrics. Coordinates are not used after graph construction by the current mechanism.
2. The degree-preserving rewire code preserved exact unweighted degree sequence.
3. Symmetric scaling matched every node's initial weighted degree/strength to ~1e-10 relative error.
4. Rewiring destroyed Euclidean locality strongly (held-out long-edge fractions seen before stopping were about 0.88–0.90).
5. Linear route-separation in the rewired arm was generally much smaller than GEO in the seeds seen before stopping.

These are useful audit facts, not a completed Gate-2 receipt.

## Engineering calibration for v1

On the invalid seeds only, replacing each nonlinear response step with 8 equal Euler substeps (same total simulated time and same drive duration) removed the overflow in both arms. This is calibration on already-consumed seeds, not confirmation.

Gate 2 v1 must preregister the stable probe and use an entirely fresh seed range.
