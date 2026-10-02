"""Stage 2's learned position value, read with numpy in the planner
(docs/oxide/scorer-speed-plan.md, "Stage 2, the learned value").

plnet trains the network on the GPU and writes its weights as plain arrays;
this module runs the same layers with numpy, so the planner's many worker
processes need neither PyTorch nor a GPU context each. A batch of a few
hundred positions takes a few milliseconds on one core.
"""
import json
import os

import numpy as np

from . import plfeat

MODELS = os.path.expanduser("~/oxide-trials/scorer-stage2/models")


def _relu(a):
    return np.maximum(a, 0.0)


class Value:
    """A trained network's position value: predict(floats, ids) for a batch."""

    def __init__(self, name, models=MODELS):
        with open(os.path.join(models, name + ".json")) as fh:
            self.meta = json.load(fh)
        if self.meta["floats"] != plfeat.FLOATS or self.meta["ids"] != plfeat.IDS:
            raise ValueError(f"model {name} was trained on other features")
        w = np.load(os.path.join(models, name + ".npz"))
        self.w = {k: w[k].astype(np.float32) for k in w.files}
        self.scale = self.meta["value_scale"]
        self.name = name

    def predict(self, x, ids):
        """Values for n positions: x [n, FLOATS] floats, ids [n, IDS] ints.
        The floats pass through float16 first, as the training data did."""
        w = self.w
        x = np.asarray(x, dtype=np.float16).astype(np.float32)
        n = x.shape[0]
        fe = plfeat.FIELD_FLOATS
        me = fe + plfeat.SLOTS * plfeat.MON_FLOATS
        field, mons, pairs = x[:, :fe], x[:, fe:me].reshape(n, plfeat.SLOTS, plfeat.MON_FLOATS), x[:, me:]
        ids = np.asarray(ids).reshape(n, plfeat.SLOTS, plfeat.MON_IDS).astype(np.int64)
        types, names, effects = w["types.weight"], w["names.weight"], w["effects.weight"]
        emb = [types[ids[:, :, 0:2]].reshape(n, plfeat.SLOTS, -1), names[ids[:, :, 2:4]].reshape(n, plfeat.SLOTS, -1),
               types[ids[:, :, 4::2]].reshape(n, plfeat.SLOTS, -1), effects[ids[:, :, 5::2]].reshape(n, plfeat.SLOTS, -1)]
        m = np.concatenate([mons] + emb, axis=2)
        m = _relu(m @ w["mon1.weight"].T + w["mon1.bias"])
        m = _relu(m @ w["mon2.weight"].T + w["mon2.bias"])
        h = np.concatenate([field, m.reshape(n, -1), pairs], axis=1)
        h = _relu(h @ w["t1.weight"].T + w["t1.bias"])
        h = _relu(h @ w["t2.weight"].T + w["t2.bias"])
        out = h @ w["head.weight"].T + w["head.bias"]
        return out[:, 0] * self.scale


def check(name, eval_dir=os.path.expanduser("~/oxide-trials/scorer-stage2/data-eval")):
    """The network against positions each valued by many play-outs (pldata
    --eval): its error from their mean, beside the error an average of k
    play-outs would carry (the play-outs' spread over the root of k), both
    with the mean's own small error taken out."""
    import glob
    net = Value(name)
    rows = []
    for p in sorted(glob.glob(os.path.join(eval_dir, "*.npz"))):
        d = np.load(p)
        pred = net.predict(d["x"], d["ids"])
        k = int(d["k"])
        rows.append((os.path.basename(p), pred, d["mean"], d["sd"], k))
    pred = np.concatenate([r[1] for r in rows])
    mean = np.concatenate([r[2] for r in rows])
    sd = np.concatenate([r[3] for r in rows])
    k = rows[0][4]
    own = float(np.mean(sd ** 2) / k)                       # the mean's own error, squared
    err = float(np.sqrt(max(0.0, np.mean((pred - mean) ** 2) - own)))
    print(f"{name}: {len(mean)} positions from {len(rows)} held-out sixes, each valued by {k} play-outs")
    print(f"  the network's error from the true value: {err:.3f}; correlation {np.corrcoef(pred, mean)[0, 1]:.3f}")
    for n in (1, 8, 32, 96, 192):
        print(f"  an average of {n:3d} play-outs: {float(np.sqrt(np.mean(sd ** 2) / n)):.3f}")
    print(f"  spread of the true values: {float(mean.std()):.3f}")
    for fname, p, m, s, _k in rows:
        print(f"  {fname}: error {float(np.sqrt(max(0.0, np.mean((p - m) ** 2) - np.mean(s ** 2) / k))):.3f}, "
              f"mean value {float(m.mean()):+.2f}")
    return err


if __name__ == "__main__":
    import sys
    check(sys.argv[1])
