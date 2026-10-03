"""The learned stand-in player (Ian's go, 2026-10-02): a network that picks
each turn's option as the play-out planner does, to play the play-outs in
place of the plain policy, so that a smaller play-out budget chooses as
well. Its body is the value network's (plnet.ValueNet), started from a
trained value network's weights; its head scores the ten option slots (the
active Pokemon's four moves, then a switch to each of the six party
places), and it learns the planner's choice among the legal ones from
pldata --choices. Runs in the PyTorch environment:

    ~/venvs/oxide-ml/bin/python -m tools.oxide.balance.plpolicy --name pi1 --from d1b
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

from . import plfeat, plnet

DATA = os.path.expanduser("~/oxide-trials/scorer-stage2/data-choices")
SLOTS = 10


class PolicyNet(plnet.ValueNet):
    def __init__(self):
        super().__init__()
        self.head = nn.Linear(plnet.TRUNK[1], SLOTS)


class CompactNet(nn.Module):
    """The compact stand-in: the field, the two active Pokemon (each through
    one small layer, their ids through learned tables as the value network
    reads them) and the matchup grid, one hidden layer, ten slot scores. A
    play-out turn needs only plfeat.compact, a fraction of the whole
    features' cost."""

    def __init__(self, mon_dim=64, hidden=128):
        super().__init__()
        self.types = nn.Embedding(len(plfeat.TYPES) + 1, plnet.TYPE_DIM)
        self.names = nn.Embedding(plfeat.NAME_IDS, plnet.NAME_DIM)
        self.effects = nn.Embedding(plfeat.EFFECT_IDS, plnet.EFFECT_DIM)
        mon_in = (plfeat.MON_FLOATS + 2 * plnet.TYPE_DIM + 2 * plnet.NAME_DIM
                  + plfeat.MOVES * (plnet.TYPE_DIM + plnet.EFFECT_DIM))
        self.mon1 = nn.Linear(mon_in, mon_dim)
        self.t1 = nn.Linear(plfeat.FIELD_FLOATS + 2 * mon_dim + plfeat.PAIR_FLOATS, hidden)
        self.head = nn.Linear(hidden, SLOTS)

    def forward(self, x, ids):
        n = x.shape[0]
        fe, mf = plfeat.FIELD_FLOATS, plfeat.MON_FLOATS
        field, mons, pairs = x[:, :fe], x[:, fe:fe + 2 * mf].reshape(n, 2, mf), x[:, fe + 2 * mf:]
        ids = ids.reshape(n, 2, plfeat.MON_IDS).long()
        emb = [self.types(ids[:, :, 0:2]).flatten(2), self.names(ids[:, :, 2:4]).flatten(2),
               self.types(ids[:, :, 4::2]).flatten(2), self.effects(ids[:, :, 5::2]).flatten(2)]
        m = F.relu(self.mon1(torch.cat([mons] + emb, dim=2)))
        h = F.relu(self.t1(torch.cat([field, m.flatten(1), pairs], dim=1)))
        return self.head(h)


def load(folder, compact=False):
    """(train, validation) tensors from the choice shards, every tenth shard
    kept for validation; with `compact`, only the compact stand-in's part of
    each position (plfeat.compact_of)."""
    paths = sorted(glob.glob(os.path.join(folder, "*.npz")))
    parts = {"train": [], "val": []}
    for i, p in enumerate(paths):
        parts["val" if i % 10 == 9 else "train"].append(p)
    if not parts["val"]:                     # too few shards to hold any out
        parts["val"] = parts["train"][:1]

    def cat(group):
        arrays = [np.load(p) for p in group]
        out = {k: np.concatenate([a[k] for a in arrays]) for k in ("x", "ids", "legal", "chosen")}
        if compact:
            out["x"], out["ids"] = plfeat.compact_of(out["x"], out["ids"])
        return {k: torch.from_numpy(np.ascontiguousarray(v)) for k, v in out.items()}
    return cat(parts["train"]), cat(parts["val"])


def logits(net, b):
    out = net(b["x"].float(), b["ids"])
    return out.masked_fill(~b["legal"], -1e9)


def agreement(net, data, device):
    net.eval()
    hits = n = 0
    with torch.no_grad():
        for s in range(0, data["chosen"].shape[0], 8192):
            b = {k: v[s:s + 8192].to(device) for k, v in data.items()}
            hits += int((logits(net, b).argmax(1) == b["chosen"].long()).sum())
            n += b["chosen"].shape[0]
    net.train()
    return hits / max(1, n)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--data", default=DATA)
    ap.add_argument("--from", dest="start", help="a value network whose body to start from")
    ap.add_argument("--epochs", type=int, default=12)
    ap.add_argument("--batch", type=int, default=1024)
    ap.add_argument("--lr", type=float, default=5e-4)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--compact", action="store_true", help="the compact stand-in (CompactNet)")
    args = ap.parse_args(argv)
    torch.manual_seed(args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    train, val = load(args.data, args.compact)
    print(f"{train['chosen'].shape[0]} training and {val['chosen'].shape[0]} held-out decisions", flush=True)
    net = (CompactNet() if args.compact else PolicyNet()).to(device)
    if args.start and not args.compact:
        body = torch.load(os.path.join(plnet.MODELS, args.start + ".pt"), map_location=device)
        net.load_state_dict({k: v for k, v in body.items() if not k.startswith("head.")}, strict=False)
    # How often a uniform pick among the legal options would agree, as a floor.
    floor = float((1.0 / val["legal"].float().sum(1)).mean())
    print(f"before training: agreement {agreement(net, val, device):.3f} (a random legal pick: {floor:.3f})",
          flush=True)
    opt = torch.optim.AdamW(net.parameters(), lr=args.lr, weight_decay=1e-4)
    steps = args.epochs * math.ceil(train["chosen"].shape[0] / args.batch)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=args.lr, total_steps=steps)
    gen = torch.Generator().manual_seed(args.seed)
    for epoch in range(args.epochs):
        t1, tot, nb = time.time(), 0.0, 0
        order = torch.randperm(train["chosen"].shape[0], generator=gen)
        for s in range(0, len(order), args.batch):
            idx = order[s:s + args.batch]
            b = {k: v[idx].to(device) for k, v in train.items()}
            loss = F.cross_entropy(logits(net, b), b["chosen"].long())
            opt.zero_grad()
            loss.backward()
            opt.step()
            sched.step()
            tot += float(loss.detach())
            nb += 1
        print(f"epoch {epoch + 1}: loss {tot / nb:.4f}; held-out agreement {agreement(net, val, device):.3f}; "
              f"{time.time() - t1:.0f} s", flush=True)
    os.makedirs(plnet.MODELS, exist_ok=True)
    torch.save(net.state_dict(), os.path.join(plnet.MODELS, args.name + ".pt"))
    plnet.export(net, os.path.join(plnet.MODELS, args.name + ".npz"))
    acc = agreement(net, val, device)
    with open(os.path.join(plnet.MODELS, args.name + ".json"), "w") as fh:
        json.dump({"name": args.name, "kind": "compact" if args.compact else "policy", "slots": SLOTS,
                   "agreement": acc, "floor": floor,
                   "train_decisions": int(train["chosen"].shape[0]), "from": args.start}, fh, indent=1)
    # The planner reads the exported arrays with numpy (plvalue.Policy).
    from . import plvalue
    k = min(2048, val["chosen"].shape[0])
    net.eval()
    with torch.no_grad():
        want = net(val["x"][:k].to(device).float(), val["ids"][:k].to(device)).float().cpu().numpy()
    got = plvalue.Policy(args.name).logits(val["x"][:k].numpy(), val["ids"][:k].numpy())
    gap = float(np.abs(want - got).max())
    print(f"numpy against PyTorch on {k} decisions: largest gap {gap:.2e}; saved {args.name}", flush=True)
    if gap > 1e-3:
        raise SystemExit("the exported network does not match the trained one")
    return 0


if __name__ == "__main__":
    sys.exit(main())
