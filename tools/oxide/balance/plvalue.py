"""Stage 2's learned position value, read with numpy in the planner
(docs/oxide/scorer-speed-plan.md, "Stage 2, the learned value").

plnet trains the network on the GPU and writes its weights as plain arrays;
this module runs the same layers with numpy, so the planner's many worker
processes need neither PyTorch nor a GPU context each. A batch of a few
hundred positions takes a few milliseconds on one core.
"""
import json
import os

from . import plthreads  # noqa: F401  (one numpy thread per process, before numpy loads)
import numpy as np  # noqa: E402

from . import plfeat

MODELS = os.path.expanduser("~/oxide-trials/scorer-stage2/models")


def _relu(a):
    return np.maximum(a, 0.0)


class Value:
    """A trained network's position value: predict(floats, ids) for a batch.
    A name joining several with "+" (d1b+d2) is their average: networks
    trained on different data err differently, so the mean errs less than
    either."""

    def __init__(self, name, models=MODELS):
        self.name = name
        self.parts = [Value(n, models) for n in name.split("+")] if "+" in name else None
        if self.parts:
            return
        with open(os.path.join(models, name + ".json")) as fh:
            self.meta = json.load(fh)
        if self.meta["floats"] != plfeat.FLOATS or self.meta["ids"] != plfeat.IDS:
            raise ValueError(f"model {name} was trained on other features")
        w = np.load(os.path.join(models, name + ".npz"))
        self.w = {k: w[k].astype(np.float32) for k in w.files}
        self.scale = self.meta["value_scale"]

    def predict(self, x, ids):
        """Values for n positions: x [n, FLOATS] floats, ids [n, IDS] ints.
        The floats pass through float16 first, as the training data did."""
        return self.heads(x, ids)[0]

    def heads(self, x, ids):
        """All three outputs for n positions: (the value, the faints still
        to come, the chance the fight is lost), each averaged over the parts
        of an average of networks."""
        if self.parts:
            outs = [p.heads(x, ids) for p in self.parts]
            return tuple(sum(o[k] for o in outs) / len(outs) for k in range(3))
        out = hidden(self.w, x, ids) @ self.w["head.weight"].T + self.w["head.bias"]
        return out[:, 0] * self.scale, out[:, 1], 1.0 / (1.0 + np.exp(-out[:, 2]))


class Policy:
    """The learned stand-in player (plpolicy): scores for a batch of
    positions over the ten option slots (the active Pokemon's four moves,
    then a switch to each of the six party places)."""

    def __init__(self, name, models=MODELS):
        with open(os.path.join(models, name + ".json")) as fh:
            self.meta = json.load(fh)
        w = np.load(os.path.join(models, name + ".npz"))
        self.w = {k: w[k].astype(np.float32) for k in w.files}
        self.name = name

        self.compact = self.meta.get("kind") == "compact"

    def logits(self, x, ids):
        """Slot scores for n positions: whole features, or for a compact
        stand-in (plpolicy.CompactNet) its compact features."""
        if not self.compact:
            return hidden(self.w, x, ids) @ self.w["head.weight"].T + self.w["head.bias"]
        w = self.w
        x = np.asarray(x, dtype=np.float16).astype(np.float32)
        n = x.shape[0]
        fe, mf = plfeat.FIELD_FLOATS, plfeat.MON_FLOATS
        field, mons, pairs = x[:, :fe], x[:, fe:fe + 2 * mf].reshape(n, 2, mf), x[:, fe + 2 * mf:]
        ids = np.asarray(ids).reshape(n, 2, plfeat.MON_IDS).astype(np.int64)
        types, names, effects = w["types.weight"], w["names.weight"], w["effects.weight"]
        emb = [types[ids[:, :, 0:2]].reshape(n, 2, -1), names[ids[:, :, 2:4]].reshape(n, 2, -1),
               types[ids[:, :, 4::2]].reshape(n, 2, -1), effects[ids[:, :, 5::2]].reshape(n, 2, -1)]
        m = _relu(np.concatenate([mons] + emb, axis=2) @ w["mon1.weight"].T + w["mon1.bias"])
        h = _relu(np.concatenate([field, m.reshape(n, -1), pairs], axis=1) @ w["t1.weight"].T + w["t1.bias"])
        return h @ w["head.weight"].T + w["head.bias"]


def hidden(w, x, ids):
    """The shared body's last layer for n positions (plnet.ValueNet's, which
    the policy network shares): x [n, FLOATS] floats, passed through float16
    first as the training data was, and ids [n, IDS]."""
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
    return _relu(h @ w["t2.weight"].T + w["t2.bias"])


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
    if len(sys.argv) > 2:
        check(sys.argv[1], os.path.expanduser(sys.argv[2]))
    else:
        check(sys.argv[1])
