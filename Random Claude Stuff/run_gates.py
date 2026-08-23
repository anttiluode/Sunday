"""
Headless gates.  No GUI, no tkinter needed.

  python run_gates.py                          synthetic set, one seed
  python run_gates.py --repeats 5              the paired suite
  python run_gates.py --data path/to/folder    your own images
  python run_gates.py --carve-every 20 --carve-eta 0.06
"""
import argparse
from instanton_field import synthetic, load_folder
from instanton_field.experiment import run_gates, run_suite, DEFAULTS

p = argparse.ArgumentParser()
p.add_argument("--data", default=None, help="image folder (subfolders = classes)")
p.add_argument("--per-class", type=int, default=60)
p.add_argument("--repeats", type=int, default=1)
p.add_argument("--n", type=int, default=DEFAULTS["n"])
p.add_argument("--steps", type=int, default=DEFAULTS["steps"])
p.add_argument("--epochs", type=int, default=DEFAULTS["epochs"])
p.add_argument("--kappa", type=float, default=DEFAULTS["kappa"])
p.add_argument("--eta", type=float, default=DEFAULTS["eta"])
p.add_argument("--lam", type=float, default=DEFAULTS["lam"])
p.add_argument("--carve-every", type=int, default=0)
p.add_argument("--carve-eta", type=float, default=0.06)
p.add_argument("--seed", type=int, default=0)
a = p.parse_args()

ds = load_folder(a.data, size=8) if a.data else synthetic(size=8, per_class=a.per_class, seed=1)
cfg = dict(n=a.n, steps=a.steps, epochs=a.epochs, kappa=a.kappa, eta=a.eta,
           lam=a.lam, carve_every=a.carve_every, carve_eta=a.carve_eta, seed=a.seed)

if a.repeats > 1:
    run_suite(ds, cfg=cfg, repeats=a.repeats)
else:
    tr, te = ds.split(0.7, seed=a.seed)
    run_gates(tr, te, cfg=cfg)
