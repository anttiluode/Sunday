"""
Datasets.

Two sources:

  load_folder(path)   -- ImageFolder convention.  Subdirectories are class
                         labels.  A flat folder of images also works; then
                         there are no labels and only retrieval is scored.

  synthetic(...)      -- four procedural shape classes, so the app runs
                         with no data at all and so the gates have a
                         controlled world where the answer is known to be
                         in the geometry rather than in the brightness.
"""

import os
import numpy as np

IMG_EXT = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp", ".tif", ".tiff"}


class Dataset:
    def __init__(self, images, labels, class_names, paths=None):
        self.images = np.asarray(images, dtype=np.float64)   # (N, P, P) in [0,1]
        self.labels = np.asarray(labels, dtype=np.int64)
        self.class_names = list(class_names)
        self.paths = paths if paths is not None else [None] * len(self.images)

    def __len__(self):
        return len(self.images)

    @property
    def n_classes(self):
        return len(self.class_names)

    def split(self, frac=0.7, seed=0):
        """Stratified split."""
        rng = np.random.default_rng(seed)
        tr, te = [], []
        for c in range(max(1, self.n_classes)):
            idx = np.where(self.labels == c)[0]
            if len(idx) == 0:
                continue
            rng.shuffle(idx)
            k = max(1, int(round(frac * len(idx))))
            tr.extend(idx[:k])
            te.extend(idx[k:])
        tr, te = np.array(sorted(tr)), np.array(sorted(te))
        if len(te) == 0:          # degenerate: reuse train
            te = tr.copy()
        return self.subset(tr), self.subset(te)

    def subset(self, idx):
        idx = np.asarray(idx)
        return Dataset(self.images[idx], self.labels[idx], self.class_names,
                       [self.paths[i] for i in idx])


def _to_array(path, size):
    from PIL import Image
    im = Image.open(path).convert("L").resize((size, size), Image.BILINEAR)
    a = np.asarray(im, dtype=np.float64) / 255.0
    return a


def load_folder(root, size=8, max_per_class=None, verbose=False):
    root = os.path.abspath(root)
    subs = sorted(d for d in os.listdir(root)
                  if os.path.isdir(os.path.join(root, d)))
    images, labels, paths, names = [], [], [], []

    def gather(d):
        fs = []
        for f in sorted(os.listdir(d)):
            if os.path.splitext(f)[1].lower() in IMG_EXT:
                fs.append(os.path.join(d, f))
        return fs

    if subs:
        for ci, s in enumerate(subs):
            fs = gather(os.path.join(root, s))
            if max_per_class:
                fs = fs[:max_per_class]
            if not fs:
                continue
            names.append(s)
            for f in fs:
                try:
                    images.append(_to_array(f, size))
                except Exception as e:
                    if verbose:
                        print("skip", f, e)
                    continue
                labels.append(len(names) - 1)
                paths.append(f)
    else:
        fs = gather(root)
        if max_per_class:
            fs = fs[:max_per_class]
        names = ["all"]
        for f in fs:
            try:
                images.append(_to_array(f, size))
            except Exception:
                continue
            labels.append(0)
            paths.append(f)

    if not images:
        raise RuntimeError(f"no readable images under {root}")
    return Dataset(images, labels, names, paths)


def synthetic(size=8, per_class=30, seed=0, noise=0.08):
    """
    Four shapes at random position / scale, rendered at `size`x`size`.

    Chosen so that mean brightness is roughly matched across classes:
    the discriminating information is arrangement, not total energy.
    """
    rng = np.random.default_rng(seed)
    names = ["disc", "ring", "bar", "cross"]
    imgs, labs = [], []
    hi = 64                                    # render big, then downsample
    ax = np.arange(hi)
    yy, xx = np.meshgrid(ax, ax, indexing="ij")

    for c, name in enumerate(names):
        for _ in range(per_class):
            cy = rng.uniform(0.35, 0.65) * hi
            cx = rng.uniform(0.35, 0.65) * hi
            r = rng.uniform(0.16, 0.26) * hi
            th = rng.uniform(0, np.pi)
            d = np.sqrt((yy - cy) ** 2 + (xx - cx) ** 2)
            if name == "disc":
                a = (d < r * 0.72).astype(float)
            elif name == "ring":
                a = ((d < r) & (d > r * 0.60)).astype(float)
            elif name == "bar":
                u = (yy - cy) * np.cos(th) + (xx - cx) * np.sin(th)
                v = -(yy - cy) * np.sin(th) + (xx - cx) * np.cos(th)
                a = ((np.abs(u) < r * 0.28) & (np.abs(v) < r * 1.15)).astype(float)
            else:
                u = (yy - cy) * np.cos(th) + (xx - cx) * np.sin(th)
                v = -(yy - cy) * np.sin(th) + (xx - cx) * np.cos(th)
                a = (((np.abs(u) < r * 0.24) & (np.abs(v) < r * 1.0)) |
                     ((np.abs(v) < r * 0.24) & (np.abs(u) < r * 1.0))).astype(float)
            small = a.reshape(size, hi // size, size, hi // size).mean(axis=(1, 3))
            s = small.sum()
            if s > 0:
                small = small / s * (size * size * 0.18)   # match total drive
            small = np.clip(small + noise * rng.standard_normal(small.shape), 0, None)
            imgs.append(small)
            labs.append(c)

    ds = Dataset(imgs, labs, names)
    order = np.random.default_rng(seed + 7).permutation(len(ds))
    return ds.subset(order)
