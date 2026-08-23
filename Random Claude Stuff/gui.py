"""
GUI.

Left: the two fields.  mu (the slow matter that is the memory) and phi
(the fast wave, which is only ever a display).  Right: controls, log, and
a query panel.

Everything heavy runs on a worker thread and talks to Tk through a queue;
nothing but the Tk main thread touches a widget.
"""

import os
import queue
import threading
import traceback

import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from .dataset import load_folder, synthetic
from .experiment import (InstantonField, DEFAULTS, run_gates, run_suite,
                         pixel_features, random_features)
from .readout import RidgeReadout, Retriever, cv_alpha
from .encode import features_from_trace


FIELDS = [
    ("n", "grid size", 72),
    ("steps", "steps / image", 260),
    ("epochs", "epochs", 3),
    ("kappa", "kappa (mass slows)", 6.0),
    ("eta", "eta (deposit)", 0.04),
    ("lam", "lambda (forget)", 0.03),
    ("drive_gain", "drive gain", 6.0),
    ("carve_every", "carve every (0=off)", 0),
    ("carve_eta", "carve eta", 0.06),
    ("seed", "seed", 0),
]


class App:
    def __init__(self, root):
        self.root = root
        root.title("Instanton Field  -  a medium that remembers where the waves went")
        root.geometry("1360x860")

        self.q = queue.Queue()
        self.worker = None
        self._stop = threading.Event()

        self.ds = None
        self.net = None
        self.readout = None
        self.retriever = None
        self.train_ds = None
        self.test_ds = None

        self._build()
        self.root.after(80, self._pump)
        self.log("Ready.  Load a folder of images (subfolders = classes) "
                 "or press 'Synthetic' to get a controlled test set.")

    # -------------------------------------------------------------- layout

    def _build(self):
        main = ttk.Frame(self.root, padding=6)
        main.pack(fill="both", expand=True)

        left = ttk.Frame(main)
        left.pack(side="left", fill="both", expand=True)
        right = ttk.Frame(main, width=430)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        self.fig = Figure(figsize=(7.6, 8.0), dpi=96)
        self.ax_mu = self.fig.add_subplot(2, 2, 1)
        self.ax_phi = self.fig.add_subplot(2, 2, 2)
        self.ax_hist = self.fig.add_subplot(2, 2, 3)
        self.ax_bars = self.fig.add_subplot(2, 2, 4)
        for a, t in ((self.ax_mu, "mu  (slow matter = the memory)"),
                     (self.ax_phi, "phi  (fast wave = display only)"),
                     (self.ax_hist, "mass distribution"),
                     (self.ax_bars, "arm scores")):
            a.set_title(t, fontsize=9)
            a.tick_params(labelsize=7)
        self.im_mu = self.ax_mu.imshow(np.zeros((8, 8)), cmap="magma", origin="lower")
        self.im_phi = self.ax_phi.imshow(np.zeros((8, 8)), cmap="RdBu_r", origin="lower")
        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=left)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # ---- data
        box = ttk.LabelFrame(right, text="data", padding=6)
        box.pack(fill="x", pady=3)
        ttk.Button(box, text="Load image folder...", command=self.pick_folder
                   ).pack(fill="x")
        r = ttk.Frame(box); r.pack(fill="x", pady=3)
        ttk.Button(r, text="Synthetic set", command=self.make_synth).pack(side="left")
        ttk.Label(r, text="  per class").pack(side="left")
        self.per_class = tk.StringVar(value="60")
        ttk.Entry(r, textvariable=self.per_class, width=5).pack(side="left")
        self.data_lbl = ttk.Label(box, text="no data", foreground="#a00")
        self.data_lbl.pack(anchor="w")

        # ---- config
        box = ttk.LabelFrame(right, text="medium", padding=6)
        box.pack(fill="x", pady=3)
        self.vars = {}
        grid = ttk.Frame(box); grid.pack(fill="x")
        for i, (key, label, default) in enumerate(FIELDS):
            ttk.Label(grid, text=label, font=("TkDefaultFont", 8)).grid(
                row=i // 2, column=(i % 2) * 2, sticky="e", padx=2, pady=1)
            v = tk.StringVar(value=str(DEFAULTS.get(key, default)))
            self.vars[key] = v
            ttk.Entry(grid, textvariable=v, width=7).grid(
                row=i // 2, column=(i % 2) * 2 + 1, sticky="w", padx=2)

        # ---- run
        box = ttk.LabelFrame(right, text="run", padding=6)
        box.pack(fill="x", pady=3)
        ttk.Button(box, text="1.  Train  (unsupervised, watch mu grow)",
                   command=self.do_train).pack(fill="x", pady=1)
        ttk.Button(box, text="2.  Fit readout  (enables Query)",
                   command=self.do_fit).pack(fill="x", pady=1)
        ttk.Button(box, text="3.  Run gates  (one seed, full ladder)",
                   command=self.do_gates).pack(fill="x", pady=1)
        r = ttk.Frame(box); r.pack(fill="x", pady=1)
        ttk.Button(r, text="4.  Run suite", command=self.do_suite).pack(side="left")
        ttk.Label(r, text=" repeats").pack(side="left")
        self.repeats = tk.StringVar(value="4")
        ttk.Entry(r, textvariable=self.repeats, width=4).pack(side="left")
        ttk.Button(box, text="Stop", command=lambda: self._stop.set()
                   ).pack(fill="x", pady=1)

        # ---- query
        box = ttk.LabelFrame(right, text="query", padding=6)
        box.pack(fill="x", pady=3)
        ttk.Button(box, text="Query with an image file...",
                   command=self.do_query_file).pack(fill="x")
        ttk.Button(box, text="Query with a random held-out image",
                   command=self.do_query_holdout).pack(fill="x", pady=1)
        self.query_lbl = ttk.Label(box, text="", justify="left",
                                   font=("TkFixedFont", 8))
        self.query_lbl.pack(anchor="w")

        # ---- log
        box = ttk.LabelFrame(right, text="log", padding=4)
        box.pack(fill="both", expand=True, pady=3)
        self.txt = tk.Text(box, height=18, width=52, font=("TkFixedFont", 8),
                           wrap="none")
        sb = ttk.Scrollbar(box, command=self.txt.yview)
        self.txt.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.txt.pack(side="left", fill="both", expand=True)

    # --------------------------------------------------------------- utils

    def log(self, s):
        self.q.put(("log", str(s)))

    def cfg(self):
        c = dict(DEFAULTS)
        for k, v in self.vars.items():
            t = v.get().strip()
            try:
                c[k] = int(t) if k in ("n", "steps", "epochs", "seed",
                                       "carve_every") else float(t)
            except ValueError:
                pass
        return c

    def _busy(self):
        if self.worker and self.worker.is_alive():
            messagebox.showinfo("busy", "Something is already running.  "
                                        "Press Stop first.")
            return True
        return False

    def _spawn(self, fn):
        if self._busy():
            return
        self._stop.clear()

        def wrap():
            try:
                fn()
            except Exception:
                self.q.put(("log", "ERROR\n" + traceback.format_exc()))
        self.worker = threading.Thread(target=wrap, daemon=True)
        self.worker.start()

    def _pump(self):
        try:
            while True:
                kind, payload = self.q.get_nowait()
                if kind == "log":
                    self.txt.insert("end", payload + "\n")
                    self.txt.see("end")
                elif kind == "mu":
                    self._draw_mu(payload)
                elif kind == "phi":
                    self._draw_phi(payload)
                elif kind == "bars":
                    self._draw_bars(payload)
                elif kind == "data":
                    self.data_lbl.config(text=payload, foreground="#060")
                elif kind == "query":
                    self.query_lbl.config(text=payload)
        except queue.Empty:
            pass
        self.root.after(80, self._pump)

    def _draw_mu(self, mu):
        self.im_mu.set_data(mu)
        self.im_mu.set_clim(mu.min(), max(mu.max(), mu.min() + 1e-9))
        self.im_mu.set_extent([0, mu.shape[1], 0, mu.shape[0]])
        self.ax_hist.clear()
        self.ax_hist.hist(mu.ravel(), bins=60, color="#b03060")
        self.ax_hist.set_title(
            f"mass  sum {mu.sum():.1f}  std {mu.std():.4f}", fontsize=9)
        self.ax_hist.tick_params(labelsize=7)
        self.canvas.draw_idle()

    def _draw_phi(self, phi):
        self.im_phi.set_data(phi)
        m = max(1e-9, np.abs(phi).max())
        self.im_phi.set_clim(-m, m)
        self.im_phi.set_extent([0, phi.shape[1], 0, phi.shape[0]])
        self.canvas.draw_idle()

    def _draw_bars(self, res):
        self.ax_bars.clear()
        names = [k for k in ("MEDIUM-LEARNED", "MEDIUM-DORMANT",
                             "MEDIUM-SHUFFLED", "MEDIUM-RANDOM",
                             "PIXELS", "RANDOM-FEATURES") if k in res]
        vals = [res[k]["test_acc"] if isinstance(res[k], dict) else res[k]
                for k in names]
        cols = ["#b03060" if n == "MEDIUM-LEARNED" else "#607080" for n in names]
        self.ax_bars.barh(range(len(names)), vals, color=cols)
        self.ax_bars.set_yticks(range(len(names)))
        self.ax_bars.set_yticklabels([n.replace("MEDIUM-", "M-") for n in names],
                                     fontsize=7)
        self.ax_bars.set_xlim(0, 1)
        self.ax_bars.set_title("test accuracy", fontsize=9)
        self.ax_bars.tick_params(labelsize=7)
        self.canvas.draw_idle()

    def _need(self, what):
        if what == "data" and self.ds is None:
            messagebox.showwarning("no data", "Load a folder or make the "
                                              "synthetic set first.")
            return True
        if what == "net" and self.net is None:
            messagebox.showwarning("not trained", "Press Train first.")
            return True
        if what == "fit" and self.readout is None:
            messagebox.showwarning("no readout", "Press 'Fit readout' first.")
            return True
        return False

    # ---------------------------------------------------------------- data

    def pick_folder(self):
        d = filedialog.askdirectory(title="folder of images "
                                          "(subfolders become classes)")
        if not d:
            return

        def job():
            self.log(f"loading {d} ...")
            self.ds = load_folder(d, size=8)
            self.train_ds, self.test_ds = self.ds.split(0.7, seed=0)
            msg = (f"{len(self.ds)} images, {self.ds.n_classes} classes: "
                   f"{', '.join(self.ds.class_names[:6])}"
                   f"{' ...' if self.ds.n_classes > 6 else ''}")
            self.q.put(("data", msg))
            self.log(msg + f"   train {len(self.train_ds)} / "
                           f"test {len(self.test_ds)}")
            if self.ds.n_classes < 2:
                self.log("NOTE: one class only -- classification is "
                         "meaningless here, retrieval still works.")
        self._spawn(job)

    def make_synth(self):
        def job():
            try:
                pc = int(self.per_class.get())
            except ValueError:
                pc = 60
            self.ds = synthetic(size=8, per_class=pc, seed=1)
            self.train_ds, self.test_ds = self.ds.split(0.7, seed=0)
            msg = f"{len(self.ds)} synthetic images, 4 classes"
            self.q.put(("data", msg))
            self.log(msg)
        self._spawn(job)

    # ----------------------------------------------------------------- run

    def do_train(self):
        if self._need("data"):
            return

        def job():
            c = self.cfg()
            self.net = InstantonField(**c)
            self.log(f"training: grid {c['n']}, {c['steps']} steps/image, "
                     f"{c['epochs']} epochs, "
                     f"carve {'ON' if c['carve_every'] else 'off'}")

            def prog(done, total, st, mu, el):
                if done % 20 == 0 or done == total:
                    self.q.put(("mu", mu.copy()))
                    self.q.put(("phi", self.net.medium.phi.copy()))
                    self.log(f"  {done}/{total}  mu std {st['mu_std']:.4f}  "
                             f"max {st['mu_max']:.3f}  {el:.0f}s")
            self.net.train(self.train_ds, progress=prog,
                           stop=self._stop.is_set)
            if self._stop.is_set():
                self.log("stopped.")
                return
            st = self.net.medium.stats()
            err = abs(st["mu_sum"] - st["budget"]) / st["budget"]
            self.log(f"done.  mass budget error {err:.2e} "
                     f"({'conserved' if err < 1e-6 else 'NOT CONSERVED'})")
            self.q.put(("mu", self.net.mu_learned.copy()))
        self._spawn(job)

    def do_fit(self):
        if self._need("data") or self._need("net"):
            return

        def job():
            self.log("extracting features (deposition off) ...")
            Xtr = self.net.extract(self.train_ds, mu=self.net.mu_learned,
                                   stop=self._stop.is_set)
            if Xtr is None:
                return
            Xte = self.net.extract(self.test_ds, mu=self.net.mu_learned,
                                   stop=self._stop.is_set)
            if Xte is None:
                return
            nc = max(2, self.ds.n_classes)
            a, cv = cv_alpha(Xtr, self.train_ds.labels, nc)
            self.readout = RidgeReadout(a).fit(Xtr, self.train_ds.labels, nc)
            self.retriever = Retriever().fit(
                Xtr, self.train_ds.labels, self.train_ds.paths,
                self.train_ds.images)
            self._Xte = Xte
            acc = self.readout.accuracy(Xte, self.test_ds.labels)
            p1 = self.retriever.precision_at_1(Xte, self.test_ds.labels)
            self.log(f"readout fitted.  held-out accuracy {acc:.3f}, "
                     f"retrieval P@1 {p1:.3f}  (alpha {a:g})")
            self.log("Query is now enabled.")
        self._spawn(job)

    def do_gates(self):
        if self._need("data"):
            return

        def job():
            out = run_gates(self.train_ds, self.test_ds, cfg=self.cfg(),
                            log=self.log, stop=self._stop.is_set,
                            on_mu=lambda mu, tag: self.q.put(("mu", mu.copy())))
            if isinstance(out, tuple):
                self.q.put(("bars", out[0]))
        self._spawn(job)

    def do_suite(self):
        if self._need("data"):
            return

        def job():
            try:
                r = int(self.repeats.get())
            except ValueError:
                r = 4
            arms, _ = run_suite(self.ds, cfg=self.cfg(), repeats=r,
                                log=self.log, stop=self._stop.is_set)
            if arms:
                self.q.put(("bars", {k: float(np.mean(v))
                                     for k, v in arms.items()}))
        self._spawn(job)

    # --------------------------------------------------------------- query

    def _query(self, img, title):
        trace, _, _ = self.net._present(img)
        f = features_from_trace(trace, bins=self.net.cfg["bins"])
        lines = [title]
        if self.ds.n_classes >= 2:
            sc = self.readout.scores(f.reshape(1, -1)).ravel()
            order = np.argsort(-sc)[:3]
            lines.append("class: " + ", ".join(
                f"{self.ds.class_names[i]} ({sc[i]:.2f})" for i in order))
        idx, sim = self.retriever.query(f, k=5)
        lines.append("nearest in the trained medium:")
        for j, s in zip(idx, sim):
            p = self.train_ds.paths[j]
            nm = os.path.basename(p) if p else \
                self.ds.class_names[self.train_ds.labels[j]]
            lines.append(f"  {s:.3f}  {nm}")
        self.q.put(("query", "\n".join(lines)))
        self.q.put(("phi", self.net.medium.phi.copy()))
        self.log("\n".join(lines))

    def do_query_file(self):
        if self._need("net") or self._need("fit"):
            return
        f = filedialog.askopenfilename(
            title="image to query",
            filetypes=[("images", "*.png *.jpg *.jpeg *.bmp *.gif *.webp"),
                       ("all", "*.*")])
        if not f:
            return

        def job():
            from .dataset import _to_array
            img = _to_array(f, 8)
            self.net.medium.set_mu(self.net.mu_learned)
            self._query(img, os.path.basename(f))
        self._spawn(job)

    def do_query_holdout(self):
        if self._need("net") or self._need("fit"):
            return

        def job():
            i = int(np.random.default_rng().integers(len(self.test_ds)))
            img = self.test_ds.images[i]
            true = self.ds.class_names[self.test_ds.labels[i]]
            self.net.medium.set_mu(self.net.mu_learned)
            self._query(img, f"held-out image (true class: {true})")
        self._spawn(job)


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
