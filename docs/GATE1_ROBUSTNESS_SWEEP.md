# Gate 1 attacker — nonlinear operating-point sweep

Gate 1 originally used one fixed nonlinear probe setting:

```text
gamma = 50
pulse amplitude = 10
```

That leaves an obvious attacker: perhaps the pair-relation effect exists only at one tuned saturation level.

## Confirmation design

Learning is unchanged and does not use the nonlinear term. For each new 3-D cloud, train H_AB and H_CD once, freeze both morphologies, then probe the same learned materials across:

```text
gamma      = 5, 10, 20, 50, 100
amplitude  = 2, 5, 10
```

Fifteen operating points total.

Before the confirmation seed range, the robustness receipt was:

```text
overall positive pair-effect fraction        >= 0.95
every grid cell positive fraction            >= 0.80
weakest grid-cell mean separation             > 0
```

The confirmation range was `260000..260005`, disjoint from the Gate 1 `240000..240019` range.

## Six-seed result

There are:

```text
6 clouds x 15 operating points x 2 learned pairs = 180 pair effects
```

Result:

```text
overall positive fraction          1.000   (180/180)
minimum grid-cell positive fraction 1.000
minimum observed separation         5.8988e-05
weakest grid-cell mean separation   1.2607e-04
```

Every tested operating point preserved the Gate 1 sign.

The weakest corner was, unsurprisingly, the weakest nonlinearity:

```text
amplitude = 2
gamma     = 5
mean separation ~1.26e-4
```

The effect grows smoothly as the nonlinear operating strength increases. For example, the strongest tested point:

```text
amplitude = 10
gamma     = 100
mean separation ~1.12e-2
```

## Verdict

This attacker does **not** kill Gate 1.

It removes the simplest tuning objection: the learned pair relation is not visible only at `gamma=50, amplitude=10`.

It still does not establish broad robustness. The sweep did not vary:

- geometry/overlap radius;
- learning rate;
- mass floor;
- number of elements;
- port placement;
- form of the local nonlinearity.

In particular, the cubic term is still one arbitrary smooth saturation family. A future attacker should replace `-gamma v^3` with a qualitatively different bounded/local nonlinearity and ask whether route overlap still predicts pair interaction.

## Reproduce

Quick smoke:

```bash
python experiments/gate1_robustness_sweep.py
```

Stored six-seed confirmation:

```bash
python experiments/gate1_robustness_sweep.py --seed-start 260000 --seeds 6
```
