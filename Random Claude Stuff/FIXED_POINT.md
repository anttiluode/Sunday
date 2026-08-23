# The deposition rule is a contraction, and that is the whole story

Three measurements. Reproduce with:

```
python -c "from instanton_field import pair_relation as pr; pr.run()"
```

## 1. Sunday's Gate 1, ported to the continuum (6-terminal ring, 6 seeds)

Two perfect matchings on a hexagon. Every terminal fires exactly once per
cycle in both histories — identical marginals, identical total drive,
identical episode count. Only who-occurred-with-whom differs.

```
trained-edge signs correct   18/36        <- chance
|cycle contrast|             0.02901      <- nonzero (0 for ANY endpoint model)
  same masses, shuffled      0.00478         so 83.5% of it is geometric
endpoint-additive R^2        73.1%        <- 27% is irreducible to a_i + a_j
```

So there *is* pair structure in the frozen medium that one scalar per
terminal cannot express, and shuffling the mass destroys most of it. But it
is **not aligned with the trained matchings**. The medium has relational
structure; training did not put it there.

(The six-terminal ring is not decorative. With four terminals the pair
matrix has 6 entries and the endpoint model has 4 free parameters, so it
fits essentially anything — a first attempt at this experiment with four
terminals returned `R^2 = 100%` and was uninformative. The alternating
cycle sum `d12 - d23 + d34 - d45 + d56 - d61` is identically zero for any
additive model, which is what makes a nonzero cycle contrast mean
something.)

## 2. Why: the rule has a unique attractor

Same drive history, two very different starting substrates (uniform vs 60%
roughness), 120 episodes, correlating the final mass fields:

```
power 1.0  lam 0.03    corr(final_A, final_B) = 0.999969
power 1.0  lam 0.003   corr(final_A, final_B) = 0.999970
power 2.5  lam 0.03    corr(final_A, final_B) = 0.999927
power 2.5  lam 0.003   corr(final_A, final_B) = 0.999949
```

The medium forgets where it started. Completely, at every setting tried,
including near-zero forgetting and strong winner-take-all. The final mass
is a deterministic function of the **marginal drive statistics** and
nothing else:

```
mu*  ~  (eta / lam) * <local energy>,  projected onto the budget
```

That one fact explains every earlier null in this repo:

- the image classifier saw no benefit, because `mu*` is the dataset mean,
  which carries no per-image and no class information;
- the ring experiment scored at chance, because the design **matches the
  marginals** — and matched marginals means an identical fixed point;
- seeds made no difference, because there is only one place to land.

A rule that contracts to a single attractor cannot store history. It can
only store an average.

## 3. The gate this hands back to Sunday

Sunday reports relational structure that survives endpoint nulls. The cheap
and nasty question is whether Sunday's plasticity is *also* a contraction.

> Take one fixed training history. Run it from several different random
> initial mass fields. Correlate the final mass fields.
>
> If `corr ~ 1`, Sunday's relational structure is a function of the drive
> statistics rather than of the history — and the endpoint nulls it has
> been defeating are the wrong nulls. The right null becomes *a substrate
> given the same marginals with no episode structure at all*.
>
> If `corr` is well below 1, Sunday has genuine path dependence and this
> medium does not, and the difference between the two rules is the
> mechanism worth isolating.

One run either way, and it costs nothing.

## 4. The named fix

Multiple attractors need something that is not a memoryless function of the
current drive. Winner-take-all does not supply it — `power=2.5` is tested
above and still lands on one attractor. Hysteresis does: a local latch with
a coercive threshold that flips at one drive level and holds until a lower
one. That is path-dependent by construction, and it is the one ingredient
that survives silence.
