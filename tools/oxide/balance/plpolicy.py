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

from . import plnet

DATA = os.path.expanduser("~/oxide-trials/scorer-stage2/data-choices")
SLOTS = 10


class PolicyNet(plnet.ValueNet):
    def __init__(self):
        super().__init__()
        self.head = nn.Linear(plnet.TRUNK[1], SLOTS)


def load(folder):
    """(train, validation) tensors from the choice shards, every tenth shard
    kept for validation."""
    paths = sorted(glob.glob(os.path.join(folder, "*.npz")))
    parts = {"train": [], "val": []}
    for i, p in enumerate(paths):
        parts["val" if i % 10 == 9 else "train"].append(p)
    if not parts["val"]:                     # too few shards to hold any out
        parts["val"] = parts["train"][:1]

    def cat(group):
        arrays = [np.load(p) for p in group]
        return {k: torch.from_numpy(np.concatenate([a[k] for a in arrays])) for k in ("x", "ids", "legal", "chosen")}
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
    args = ap.parse_args(argv)
    torch.manual_seed(args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    train, val = load(args.data)
    print(f"{train['chosen'].shape[0]} training and {val['chosen'].shape[0]} held-out decisions", flush=True)
    net = PolicyNet().to(device)
    if args.start:
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
        json.dump({"name": args.name, "kind": "policy", "slots": SLOTS, "agreement": acc, "floor": floor,
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
