"""Stage 2's learned position value: training on the GPU
(docs/oxide/scorer-speed-plan.md, "Stage 2, the learned value").

Runs only in the PyTorch environment:

    ~/venvs/oxide-ml/bin/python -m tools.oxide.balance.plnet --name v1

The network reads a position as plfeat describes it. One small encoder,
shared by all twelve Pokemon slots, turns each Pokemon's numbers and its
type, ability, item and move ids (through learned tables) into a short
vector; a larger network then reads the twelve vectors, the field and the
matchup grid and predicts the position's value (plplan.value at the fight's
end), with the faints still to come and the chance the fight is lost as side
outputs that help it learn.

Training holds out whole sixes, the last few of each fight, so the held-out
error says how well it judges a team it has never seen. The trained weights
are written as a PyTorch file and as plain arrays (plvalue reads those with
numpy, so the planner's workers need no PyTorch).
"""
import argparse
import glob
import json
import math
import os
import sys
import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from . import plfeat

DATA = os.path.expanduser("~/oxide-trials/scorer-stage2/data")
MODELS = os.path.expanduser("~/oxide-trials/scorer-stage2/models")
TYPE_DIM, NAME_DIM, EFFECT_DIM = 8, 16, 16
MON_DIM, TRUNK = 128, (512, 256)
VALUE_SCALE = 4.0             # values run from about -16 to +0.6; trained divided by this


class ValueNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.types = nn.Embedding(len(plfeat.TYPES) + 1, TYPE_DIM)
        self.names = nn.Embedding(plfeat.NAME_IDS, NAME_DIM)
        self.effects = nn.Embedding(plfeat.EFFECT_IDS, EFFECT_DIM)
        mon_in = plfeat.MON_FLOATS + 2 * TYPE_DIM + 2 * NAME_DIM + plfeat.MOVES * (TYPE_DIM + EFFECT_DIM)
        self.mon1 = nn.Linear(mon_in, MON_DIM)
        self.mon2 = nn.Linear(MON_DIM, MON_DIM)
        trunk_in = plfeat.FIELD_FLOATS + plfeat.SLOTS * MON_DIM + plfeat.PAIR_FLOATS
        self.t1 = nn.Linear(trunk_in, TRUNK[0])
        self.t2 = nn.Linear(TRUNK[0], TRUNK[1])
        self.head = nn.Linear(TRUNK[1], 3)       # value / VALUE_SCALE, future faints, loss logit

    def forward(self, x, ids):
        n = x.shape[0]
        fe = plfeat.FIELD_FLOATS
        me = fe + plfeat.SLOTS * plfeat.MON_FLOATS
        field, mons, pairs = x[:, :fe], x[:, fe:me].reshape(n, plfeat.SLOTS, plfeat.MON_FLOATS), x[:, me:]
        ids = ids.reshape(n, plfeat.SLOTS, plfeat.MON_IDS).long()
        emb = [self.types(ids[:, :, 0:2]).flatten(2), self.names(ids[:, :, 2:4]).flatten(2),
               self.types(ids[:, :, 4::2]).flatten(2), self.effects(ids[:, :, 5::2]).flatten(2)]
        m = torch.cat([mons] + emb, dim=2)
        m = F.relu(self.mon2(F.relu(self.mon1(m))))
        h = torch.cat([field, m.flatten(1), pairs], dim=1)
        h = F.relu(self.t2(F.relu(self.t1(h))))
        return self.head(h)


def load(data_dirs, held_out):
    """(train, validation) as dicts of tensors, the last `held_out` sixes of
    each fight kept for validation (with none held out, every tenth shard)."""
    shards = []
    for data_dir in data_dirs:
        for p in glob.glob(os.path.join(data_dir, "*.json")):
            with open(p) as fh:
                shards.append(json.load(fh) | {"path": p[:-5] + ".npz"})
    by_fight = {}
    for s in sorted(shards, key=lambda s: s["seed"]):
        by_fight.setdefault(s["fight"], []).append(s)
    parts = {"train": [], "val": []}
    for fight, ss in by_fight.items():
        sixes = []
        for s in ss:
            if tuple(s["six"]) not in sixes:
                sixes.append(tuple(s["six"]))
        held = set(sixes[len(sixes) - held_out:]) if held_out else set()
        for k, s in enumerate(ss):
            val = tuple(s["six"]) in held if held_out else k % 10 == 9
            parts["val" if val else "train"].append(s)

    def cat(group):
        arrays = [np.load(s["path"]) for s in group]
        return {k: torch.from_numpy(np.concatenate([a[k] for a in arrays])) for k in ("x", "ids", "value", "future", "lost")}
    return cat(parts["train"]), cat(parts["val"]), parts


def losses(out, batch):
    v = batch["value"] / VALUE_SCALE
    lv = F.huber_loss(out[:, 0], v)
    lf = F.mse_loss(out[:, 1], batch["future"].float()) / 4
    ll = F.binary_cross_entropy_with_logits(out[:, 2], batch["lost"].float())
    return lv + 0.25 * lf + 0.25 * ll, lv


def batches(data, size, device, shuffle, gen=None):
    n = data["value"].shape[0]
    order = torch.randperm(n, generator=gen) if shuffle else torch.arange(n)
    for s in range(0, n, size):
        idx = order[s:s + size]
        yield {k: v[idx].to(device, non_blocking=True) for k, v in data.items()}


def evaluate(net, data, device):
    net.eval()
    preds = []
    with torch.no_grad():
        for b in batches(data, 16384, device, False):
            preds.append(net(b["x"].float(), b["ids"])[:, 0].float().cpu() * VALUE_SCALE)
    net.train()
    p = torch.cat(preds)
    y = data["value"].float()
    rmse = math.sqrt(float(((p - y) ** 2).mean()))
    corr = float(torch.corrcoef(torch.stack([p, y]))[0, 1])
    return rmse, corr, float(y.std())


def export(net, path):
    """The weights as plain arrays, for numpy inference (plvalue)."""
    np.savez(path, **{k: v.detach().cpu().numpy() for k, v in net.state_dict().items()})


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--data", nargs="+", default=[DATA], help="one or more folders of shards")
    ap.add_argument("--from", dest="start", help="a trained network to start from (fine-tuning)")
    ap.add_argument("--held-out", type=int, default=3, help="sixes per fight kept for validation")
    ap.add_argument("--epochs", type=int, default=8)
    ap.add_argument("--batch", type=int, default=4096)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args(argv)
    torch.manual_seed(args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    t0 = time.time()
    train, val, parts = load(args.data, args.held_out)
    print(f"{train['value'].shape[0]} training and {val['value'].shape[0]} held-out positions "
          f"({len(parts['train'])} and {len(parts['val'])} sixes), loaded in {time.time() - t0:.0f} s", flush=True)
    net = ValueNet().to(device)
    if args.start:
        net.load_state_dict(torch.load(os.path.join(MODELS, args.start + ".pt"), map_location=device))
    opt = torch.optim.AdamW(net.parameters(), lr=args.lr, weight_decay=1e-4)
    steps = args.epochs * math.ceil(train["value"].shape[0] / args.batch)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=args.lr, total_steps=steps)
    gen = torch.Generator().manual_seed(args.seed)
    for epoch in range(args.epochs):
        t1, tot, nb = time.time(), 0.0, 0
        for b in batches(train, args.batch, device, True, gen):
            out = net(b["x"].float(), b["ids"])
            loss, _lv = losses(out, b)
            opt.zero_grad()
            loss.backward()
            opt.step()
            sched.step()
            tot += float(loss.detach())
            nb += 1
        rmse, corr, sd = evaluate(net, val, device)
        print(f"epoch {epoch + 1}: training loss {tot / nb:.4f}; held-out value error {rmse:.3f} "
              f"(spread of labels {sd:.3f}), correlation {corr:.3f}; {time.time() - t1:.0f} s", flush=True)
    os.makedirs(MODELS, exist_ok=True)
    torch.save(net.state_dict(), os.path.join(MODELS, args.name + ".pt"))
    export(net, os.path.join(MODELS, args.name + ".npz"))
    meta = {"name": args.name, "floats": plfeat.FLOATS, "ids": plfeat.IDS, "value_scale": VALUE_SCALE,
            "train_positions": int(train["value"].shape[0]), "held_out_positions": int(val["value"].shape[0]),
            "held_out_sixes": [[s["fight"], s["six"]] for s in parts["val"]],
            "held_out_error": rmse, "held_out_correlation": corr, "epochs": args.epochs}
    with open(os.path.join(MODELS, args.name + ".json"), "w") as fh:
        json.dump(meta, fh, indent=1)
    # The planner reads the exported arrays with numpy (plvalue): the two
    # must agree, or the planner is not using the network trained here.
    from . import plvalue
    k = min(4096, val["value"].shape[0])
    net.eval()
    with torch.no_grad():
        want = net(val["x"][:k].to(device).float(), val["ids"][:k].to(device))[:, 0].float().cpu().numpy() * VALUE_SCALE
    got = plvalue.Value(args.name).predict(val["x"][:k].numpy(), val["ids"][:k].numpy())
    gap = float(np.abs(want - got).max())
    print(f"numpy against PyTorch on {k} positions: largest gap {gap:.2e}", flush=True)
    if gap > 1e-3:
        raise SystemExit("the exported network does not match the trained one")
    print(f"saved {args.name} to {MODELS}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
