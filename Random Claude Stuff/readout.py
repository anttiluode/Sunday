"""
Readout.

The medium is not trained by gradients.  Everything downstream of the
probes is a plain ridge regression onto one-hot labels, fitted in closed
form, plus a nearest-neighbour index for retrieval.  Keeping the readout
this dumb is the point: any capability difference between arms has to
come from the medium, not from the classifier.
"""

import numpy as np


class Standardizer:
    def fit(self, X):
        self.mu = X.mean(axis=0)
        self.sd = X.std(axis=0) + 1e-9
        return self

    def __call__(self, X):
        return (X - self.mu) / self.sd


class RidgeReadout:
    def __init__(self, alpha=1.0):
        self.alpha = float(alpha)

    def fit(self, X, y, n_classes):
        self.std = Standardizer().fit(X)
        Z = self.std(X)
        Z = np.hstack([Z, np.ones((len(Z), 1))])
        Y = np.zeros((len(y), n_classes))
        Y[np.arange(len(y)), y] = 1.0
        A = Z.T @ Z + self.alpha * np.eye(Z.shape[1])
        A[-1, -1] -= self.alpha                       # do not penalise bias
        self.W = np.linalg.solve(A, Z.T @ Y)
        return self

    def scores(self, X):
        Z = self.std(X)
        Z = np.hstack([Z, np.ones((len(Z), 1))])
        return Z @ self.W

    def predict(self, X):
        return np.argmax(self.scores(X), axis=1)

    def accuracy(self, X, y):
        return float((self.predict(X) == np.asarray(y)).mean())


class Retriever:
    """Cosine nearest-neighbour over standardized features."""

    def fit(self, X, labels, paths=None, images=None):
        self.std = Standardizer().fit(X)
        Z = self.std(X)
        self.Z = Z / (np.linalg.norm(Z, axis=1, keepdims=True) + 1e-12)
        self.labels = np.asarray(labels)
        self.paths = paths
        self.images = images
        return self

    def query(self, x, k=5):
        z = self.std(x.reshape(1, -1))
        z = z / (np.linalg.norm(z) + 1e-12)
        sim = (self.Z @ z.ravel())
        order = np.argsort(-sim)[:k]
        return order, sim[order]

    def precision_at_1(self, X, y):
        hits = 0
        for i in range(len(X)):
            order, _ = self.query(X[i], k=1)
            hits += int(self.labels[order[0]] == y[i])
        return hits / max(1, len(X))


def cv_alpha(X, y, n_classes, alphas=(0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0),
             folds=4, seed=0):
    """Pick the ridge penalty honestly, on the training set only."""
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(X))
    parts = np.array_split(idx, folds)
    best, best_a = -1.0, 1.0
    for a in alphas:
        accs = []
        for f in range(folds):
            te = parts[f]
            tr = np.concatenate([parts[g] for g in range(folds) if g != f])
            if len(np.unique(y[tr])) < 2:
                continue
            r = RidgeReadout(a).fit(X[tr], y[tr], n_classes)
            accs.append(r.accuracy(X[te], y[te]))
        if accs and np.mean(accs) > best:
            best, best_a = float(np.mean(accs)), a
    return best_a, best
