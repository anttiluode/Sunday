# Instanton Field

A 2-D wave medium whose local speed is set by a slow **mass** field, where the
mass is deposited by the waves themselves under a fixed total budget. Train it
on a folder of images, query it with a new one, and — the part that matters —
run the gates that are allowed to kill it.

Pure `numpy` + `matplotlib` + `Pillow`. No torch, no GPU.

```
python run_gui.py                      # GUI: train, watch mu grow, query
python run_gates.py                    # headless, synthetic set, one seed
python run_gates.py --repeats 5        # the paired suite (this is the real one)
python run_gates.py --data C:\pics     # your images, subfolders = classes
```

---

## What it is

```
image  ->  8x8 port amplitudes  ->  Gaussian stamps into the field
                                          |
                                    phi:  d2phi/dt2 = div( c2(mu) grad phi ) - damp - ...
                                          |            c2(mu) = c0^2 / (1 + kappa*mu)
                                          |
                                    mu:   mu <- (1-lam)*mu + eta*<phi^2>_local
                                          then PROJECTED back onto a fixed budget
                                          |
                                    64 probes x 4 time bins  ->  256 features
                                          |
                                    ridge readout  /  cosine retrieval
```

Waves travel, deposit mass where they linger, mass slows the medium there,
and the next wave is refracted by what the last one left. Total mass is
constant, so a region can only gain by taking from somewhere else — this is a
competition, not a runaway.

**Nothing is trained by gradient descent.** The medium is unsupervised and
label-blind. Only the final ridge regression sees labels, and it is
deliberately the dumbest possible classifier, so any difference between arms
has to come from the medium.

### Two rules that are load-bearing

1. **The vacuum is stable.** `phi = 0` is a minimum. The original
   `anttis-instanton.py` used `V = -a/2 phi^2 + b/4 phi^4`, which makes the
   *empty background* tachyonic — it decays into domains on its own at rate
   `sqrt(a)`. Measured on that file: far-field rms goes `1.9e-2` at t=5 to
   `3.4e-1` at t=15, rate ≈ 0.29 against the predicted 0.316. The "particle
   jumping to random places in 2-D" was that decay plus a `center_of_mass`
   readout over a mask that had become multimodal (blob count 1 -> 12, CoM hops
   of 4–13 cells tracking it). Both are fixed here.

2. **The fast field is never the memory.** `phi` is reset to zero before every
   presentation; only `mu` persists. Feature extraction runs with deposition
   **off**, so the feature for image *i* does not depend on how many images
   came before it. Presentation order cannot leak into a result.

---

## The gates

Six arms. The first four are the same medium with different `mu`; the last two
are attackers that do not use the medium at all.

| arm | what it asks |
|---|---|
| `MEDIUM-LEARNED` | the medium after training |
| `MEDIUM-DORMANT` | uniform `mu`, never learned — *did deposition do anything?* |
| `MEDIUM-SHUFFLED` | learned `mu`, positions permuted — *is the geometry load-bearing?* |
| `MEDIUM-RANDOM` | matched-histogram random `mu` — *or is it just heterogeneity?* |
| `PIXELS` | ridge on the raw 8x8 input — *is the medium needed at all?* |
| `RANDOM-FEATURES` | untrained `tanh(Wx+b)` at the same 256 dims — *is any expansion enough?* |

The shuffle is exact: sum, mean, variance, histogram, min and max of `mu` are
all preserved bit-for-bit. Only *where* the mass sits changes. That check is
asserted in the run and printed.

`run_suite` repeats the whole ladder over seeds and reports **paired**
differences with a standard error, because a single run of this size has a
noise floor of several accuracy points.

---

## Measured, on the synthetic 4-shape set (240 images, 8x8, brightness matched)

**Config A — deposition at the end of each presentation, 5 seeds:**

```
MEDIUM-LEARNED   0.708 +/- 0.031
MEDIUM-DORMANT   0.706 +/- 0.023
MEDIUM-SHUFFLED  0.719 +/- 0.052
MEDIUM-RANDOM    0.733 +/- 0.041
PIXELS           0.347 +/- 0.010
RANDOM-FEATURES  0.669 +/- 0.039

LEARNED - DORMANT   +0.003 +/- 0.035   within noise
LEARNED - SHUFFLED  -0.011 +/- 0.055   within noise
LEARNED - RANDOM    -0.025 +/- 0.030   within noise
LEARNED - PIXELS    +0.361 +/- 0.026   SIGNIFICANT
```

**Config B — `carve_every=20`, so the wave feels the trail it is laying down
within the same presentation, 4 seeds:**

```
LEARNED - DORMANT   -0.038 +/- 0.013   SIGNIFICANT (worse)
LEARNED - SHUFFLED  -0.045 +/- 0.013   SIGNIFICANT (worse)
LEARNED - RANDOM    -0.056 +/- 0.032   SIGNIFICANT (worse)
LEARNED - PIXELS    +0.222 +/- 0.059   SIGNIFICANT
```

### Honest ledger

**ALIVE.** The wave medium is a genuinely useful untrained spatial reservoir.
Every medium arm beats raw pixels by 0.22–0.36, well clear of noise. Nonlinear
spatial mixing through a physical field is doing real work.

**DEAD, as of these runs.** The deposition rule contributes nothing. Config A:
learning is indistinguishable from not learning, and the shuffle test does not
fire — which means the learned geometry is not load-bearing and this is, so
far, an arbitrary heterogeneous filter. Config B is worse: making the wave
carve its own route actively *hurts*.

**The diagnosis, which is the useful part.** Energy-proportional deposition
under a shared budget converges toward the *dataset mean*. It piles mass where
the average image already drives, which makes the medium respond more similarly
to everything — it homogenises the very diversity the reservoir was
classifying with. Config B just does it harder.

That points at a specific next rule rather than at more tuning, and it is the
same shape as Sunday Gate 1's surprise: the useful rule pushed routes **apart**,
it did not pile mass where energy already was. So the deposition rule to try
next is a decorrelating / novelty-gated one — deposit on the component of the
local energy that the current mass does *not* already explain, rather than on
the energy itself. That is a small edit to `Medium.deposit`.

**A trap this repo will show you.** Run `python run_gates.py --per-class 12
--epochs 1` and every gate reports PASS. Sixteen test images; the noise floor
is bigger than every effect. That is why `run_suite` exists and why single-run
verdicts should not be believed.

---

## Files

```
instanton_field/medium.py      field + mass, CFL check, budget projection, shuffle surgery
instanton_field/encode.py      image -> ports, probes -> features, within-trial carving
instanton_field/dataset.py     image folder loader + synthetic shapes
instanton_field/readout.py     ridge, cross-validated alpha, cosine retrieval
instanton_field/experiment.py  train / extract / arm ladder / gates / paired suite
instanton_field/gui.py         Tk GUI
```

## What this is not

It is not a brain, a dendrite, or a better architecture than anything. It is a
physical reservoir with a self-modifying geometry and an honest set of tests
for whether that self-modification buys anything. Right now it does not, and
the repo says so in its own output.
