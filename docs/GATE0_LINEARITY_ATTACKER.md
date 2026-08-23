# Gate 0 attacker — exact linear superposition

Gate 0 passes its spatial-transfer receipt, but the fast frozen material obeys a linear state equation. Therefore it must not be described as a dendritic calculating primitive merely because the learned mass looks branch-like.

## Attack

For each trained material, build two identical short pulse drives `A` and `B` and compare the complete compartment trajectories:

```text
R(A + B)

versus

R(A) + R(B)
```

Also test scaling:

```text
R(2A) ?= 2 R(A)
```

Run:

```bash
python experiments/gate0_linearity_attacker.py
```

## First result

```text
A-trained
  whole-state superposition max abs error   1.387778780781e-17
  relative error                            1.310429866590e-16
  scaling max abs error                     0.0
  soma superposition max abs error          5.421010862428e-20

B-trained
  whole-state superposition max abs error   2.775557561563e-17
  relative error                            2.367314046826e-16
  scaling max abs error                     0.0
  soma superposition max abs error          1.084202172486e-19
```

These are floating-point roundoff.

## Verdict

**Attacker succeeds.**

Gate 0 is a learned spatial transfer operator. Its morphology matters, but simultaneous inputs do not interact except by linear addition.

What survives:

> Signal history can become persistent 3-D transfer geometry under a fixed mass budget.

What is not earned:

> dendritic nonlinear computation

The next gate must introduce one minimal local nonlinear ingredient and ask whether 3-D route overlap makes that nonlinearity do something structurally specific. Merely inserting `tanh` and observing `R(A+B) != R(A)+R(B)` is too easy; the interaction must depend on morphology and face shuffle/overlap attackers.
