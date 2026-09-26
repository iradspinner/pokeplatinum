#!/usr/bin/env python3
"""Render a map from above, textured, with its tiles and events marked.

Platinum Oxide project. Added for the grass that replaces the gift clowns
(2026-09-27): a patch of tall grass is chosen by looking at the map, and Ian
approves it from a picture, so the picture has to show what the player sees.
Nothing here writes to res/.

How a map is drawn, from the files the game reads:
  - each 32 x 32 tile chunk is one res/field/maps/data/map_data_NNN.bin: the
    tile permissions, a list of props, the terrain model (an NSBMD) and its
    heights, in that order behind a header of four sizes;
  - the terrain's textures are the area's map texture set
    (res/field/area_data -> res/field/maps/texture_sets), and each prop is a
    model from res/field/props/models with textures from the prop texture set
    of the same number as the area's prop model set;
  - one tile is 16 world units, a chunk spans -256 to 256 on x and z, and a
    vertex is a 4.12 fixed-point value times the model's position scale.

The picture is an orthographic view from straight above: for each pixel the
highest surface wins. Buildings (props) are drawn the same way, so a house
roof hides the ground under it, as in the game's own top-down camera.

Overlays: a faint grid, one line per tile; collision tiles darkened; tall
grass outlined in green; object events as numbered red squares; warps as blue
squares; and any --mark rectangle in yellow. Coordinates are the ones event
files use (global on the overworld matrix), with a label every eight tiles.

    python3 tools/oxide/maprender.py MAP_HEADER_AMITY_SQUARE --out amity.png
    python3 tools/oxide/maprender.py MAP_HEADER_SANDGEM_TOWN --mark 180,830,185,833
"""

import argparse
import json
import os
import re
import struct
import sys

import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TILE = 16.0
CHUNK = 32
# Lamps and their glow (Hearthome's c5_light, Jubilife's c1_lamp01) are tall translucent
# geometry that covers the ground from straight above, though the game's own
# camera sees them from the side. They are left out unless --all is given.
SKIP_MATERIALS = re.compile(r"light|lamp", re.I)


# ------------------------------------------------------------ G3D containers
def read_dict(buf, off):
    """An NNS G3D resource dictionary at `off`: [(name, entry bytes)]."""
    _rev, num, _size = struct.unpack_from("<BBH", buf, off)
    ofs_entry = struct.unpack_from("<H", buf, off + 6)[0]
    e = off + ofs_entry
    unit, ofs_name = struct.unpack_from("<HH", buf, e)
    out = []
    for i in range(num):
        data = buf[e + 4 + i * unit:e + 4 + (i + 1) * unit]
        raw = buf[e + ofs_name + i * 16:e + ofs_name + (i + 1) * 16]
        out.append((raw.split(b"\0")[0].decode("ascii", "replace"), data))
    return out


def blocks(buf):
    n = struct.unpack_from("<H", buf, 14)[0]
    return {buf[o:o + 4]: o for o in struct.unpack_from(f"<{n}I", buf, 16)}


# ------------------------------------------------------------ textures
def bgr555(v):
    return ((v & 31) * 255 // 31, ((v >> 5) & 31) * 255 // 31, ((v >> 10) & 31) * 255 // 31)


class TextureSet:
    """An NSBTX's TEX0 block, decoded on demand to RGBA arrays by name."""

    def __init__(self, buf):
        self.buf = buf
        t = blocks(buf).get(b"TEX0")
        self.t = t
        self.textures, self.palettes = {}, {}
        if t is None:
            return
        tex_dict = struct.unpack_from("<H", buf, t + 0x0E)[0]
        self.tex_data = t + struct.unpack_from("<I", buf, t + 0x14)[0]
        self.comp_data = t + struct.unpack_from("<I", buf, t + 0x24)[0]
        self.comp_info = t + struct.unpack_from("<I", buf, t + 0x28)[0]
        pl_dict = struct.unpack_from("<I", buf, t + 0x34)[0]
        self.pl_data = t + struct.unpack_from("<I", buf, t + 0x38)[0]
        for name, e in read_dict(buf, t + tex_dict):
            self.textures[name] = struct.unpack("<I", e[:4])[0]
        for name, e in read_dict(buf, t + pl_dict):
            self.palettes[name] = struct.unpack("<H", e[:2])[0] << 3
        self.cache = {}

    def palette(self, name, count):
        off = self.pl_data + self.palettes[name]
        return [bgr555(struct.unpack_from("<H", self.buf, off + 2 * i)[0]) for i in range(count)]

    def decode(self, tex, pal):
        key = (tex, pal)
        if key in self.cache:
            return self.cache[key]
        img = self._decode(tex, pal)
        self.cache[key] = img
        return img

    def _decode(self, tex, pal):
        param = self.textures[tex]
        off = (param & 0xFFFF) << 3
        w, h = 8 << ((param >> 20) & 7), 8 << ((param >> 23) & 7)
        fmt, c0_clear = (param >> 26) & 7, (param >> 29) & 1
        b = self.buf
        out = np.zeros((h, w, 4), np.uint8)
        n = w * h
        if fmt == 7:
            px = np.frombuffer(b, np.uint16, n, self.tex_data + off).astype(np.uint32)
            out[..., 0] = ((px & 31) * 255 // 31).reshape(h, w)
            out[..., 1] = (((px >> 5) & 31) * 255 // 31).reshape(h, w)
            out[..., 2] = (((px >> 10) & 31) * 255 // 31).reshape(h, w)
            out[..., 3] = np.where(px & 0x8000, 255, 0).reshape(h, w)
            return out
        if fmt == 5:
            return self._decode_4x4(off, w, h, pal)
        bits = {1: 8, 2: 2, 3: 4, 4: 8, 6: 8}[fmt]
        raw = np.frombuffer(b, np.uint8, n * bits // 8, self.tex_data + off)
        if bits == 8:
            vals = raw.astype(np.int32)
        elif bits == 4:
            vals = np.stack([raw & 15, raw >> 4], 1).reshape(-1).astype(np.int32)
        else:
            vals = np.stack([raw & 3, (raw >> 2) & 3, (raw >> 4) & 3, raw >> 6], 1).reshape(-1).astype(np.int32)
        if fmt == 1:
            idx, alpha = vals & 31, (vals >> 5) * 255 // 7
            ncol = 32
        elif fmt == 6:
            idx, alpha = vals & 7, (vals >> 3) * 255 // 31
            ncol = 8
        else:
            idx, alpha = vals, np.full_like(vals, 255)
            ncol = {2: 4, 3: 16, 4: 256}[fmt]
            if c0_clear:
                alpha = np.where(idx == 0, 0, 255)
        colours = np.array(self.palette(pal, ncol) if pal in self.palettes else [(255, 0, 255)] * ncol, np.uint8)
        out[..., :3] = colours[np.clip(idx, 0, ncol - 1)].reshape(h, w, 3)
        out[..., 3] = alpha.reshape(h, w)
        return out

    def _decode_4x4(self, off, w, h, pal):
        b = self.buf
        out = np.zeros((h, w, 4), np.uint8)
        pbase = self.pl_data + self.palettes.get(pal, 0)

        def col(i):
            return bgr555(struct.unpack_from("<H", b, pbase + 2 * i)[0])

        blk = 0
        for by in range(h // 4):
            for bx in range(w // 4):
                texels = struct.unpack_from("<I", b, self.comp_data + off + blk * 4)[0]
                info = struct.unpack_from("<H", b, self.comp_info + off // 2 + blk * 2)[0]
                blk += 1
                pofs, mode = (info & 0x3FFF) * 2, info >> 14
                c = [col(pofs + i) for i in range(2)]
                if mode == 0:
                    c += [col(pofs + 2), None]
                elif mode == 1:
                    c += [tuple((c[0][k] + c[1][k]) // 2 for k in range(3)), None]
                elif mode == 2:
                    c += [col(pofs + 2), col(pofs + 3)]
                else:
                    c += [tuple((5 * c[0][k] + 3 * c[1][k]) // 8 for k in range(3)),
                          tuple((3 * c[0][k] + 5 * c[1][k]) // 8 for k in range(3))]
                for y in range(4):
                    for x in range(4):
                        v = c[(texels >> ((y * 4 + x) * 2)) & 3]
                        if v is not None:
                            out[by * 4 + y, bx * 4 + x] = (*v, 255)
        return out


# ------------------------------------------------------------ models
class Model:
    """The first model of an NSBMD: its materials and triangles in world units."""

    def __init__(self, buf):
        self.buf = buf
        b = buf
        mdl0 = blocks(b)[b"MDL0"]
        models = read_dict(b, mdl0 + 8)
        mo = mdl0 + struct.unpack("<I", models[0][1][:4])[0]
        _size, ofs_sbc, ofs_mat, ofs_shp, _ofs_evp = struct.unpack_from("<5I", b, mo)
        self.pos_scale = struct.unpack_from("<i", b, mo + 0x14 + 8)[0] / 4096.0
        self.box = [v / 4096.0 for v in struct.unpack_from("<6h", b, mo + 0x14 + 24)]
        self.box_scale = struct.unpack_from("<i", b, mo + 0x14 + 36)[0] / 4096.0
        mat_base = mo + ofs_mat
        ofs_tex, ofs_pl = struct.unpack_from("<HH", b, mat_base)
        mats = read_dict(b, mat_base + 4)
        self.materials = []
        for name, e in mats:
            mofs = mat_base + struct.unpack("<I", e[:4])[0]
            poly_attr = struct.unpack_from("<I", b, mofs + 12)[0]
            teximg = struct.unpack_from("<I", b, mofs + 20)[0]
            flag = struct.unpack_from("<H", b, mofs + 30)[0]
            ow, oh = struct.unpack_from("<HH", b, mofs + 32)
            p = mofs + 44
            scale = (1.0, 1.0)
            if flag & 1 and not flag & 2:
                scale = (struct.unpack_from("<i", b, p)[0] / 4096.0, struct.unpack_from("<i", b, p + 4)[0] / 4096.0)
            self.materials.append({"name": name, "tex": None, "pal": None,
                                   "alpha": (poly_attr >> 16) & 31, "param": teximg,
                                   "orig": (ow, oh), "scale": scale})
        for key, ofs in (("tex", ofs_tex), ("pal", ofs_pl)):
            for name, e in read_dict(b, mat_base + ofs):
                v = struct.unpack("<I", e[:4])[0]
                lofs, count = v & 0xFFFF, (v >> 16) & 0xFF
                for k in range(count):
                    self.materials[b[mat_base + lofs + k]][key] = name
        shps = read_dict(b, mo + ofs_shp)
        self.shapes = []
        for _name, e in shps:
            so = mo + ofs_shp + struct.unpack("<I", e[:4])[0]
            ofs_dl, size_dl = struct.unpack_from("<II", b, so + 8)
            self.shapes.append(b[so + ofs_dl:so + ofs_dl + size_dl])
        self.draws = self._sbc(b[mo + ofs_sbc:mo + ofs_mat])

    @staticmethod
    def _sbc(s):
        """(material, shape) pairs in the order the render bytecode draws them."""
        out, i, mat = [], 0, None
        sizes = {0x00: 1, 0x01: 1, 0x02: 3, 0x03: 2, 0x04: 2, 0x05: 2, 0x06: 4, 0x07: 2, 0x08: 2,
                 0x0A: 9, 0x0B: 1, 0x0C: 3, 0x0D: 3}
        while i < len(s):
            op = s[i]
            base, flags = op & 0x1F, op >> 5
            if base == 0x01:
                break
            if base == 0x04:
                mat = s[i + 1]
            elif base == 0x05 and mat is not None:
                out.append((mat, s[i + 1]))
            if base == 0x09:
                n = s[i + 2]
                i += 3 + n * 3
                continue
            size = sizes.get(base, 1)
            if base == 0x06:
                size += (1 if flags & 1 else 0) + (1 if flags & 2 else 0)
            elif base in (0x07, 0x08):
                size += (1 if flags & 1 else 0) + (1 if flags & 2 else 0)
            i += size
        return out

    def triangles(self, dl):
        """[(3 x (x, y, z), 3 x (s, t))] in model units before position scale."""
        tris, verts, prim = [], [], None
        v = [0.0, 0.0, 0.0]
        st = (0.0, 0.0)
        nparams = {0x10: 1, 0x11: 0, 0x12: 1, 0x13: 1, 0x14: 1, 0x15: 0, 0x16: 16, 0x17: 12,
                   0x18: 16, 0x19: 12, 0x1A: 9, 0x1B: 3, 0x1C: 3, 0x20: 1, 0x21: 1, 0x22: 1,
                   0x23: 2, 0x24: 1, 0x25: 1, 0x26: 1, 0x27: 1, 0x28: 1, 0x29: 1, 0x2A: 1,
                   0x2B: 1, 0x30: 1, 0x31: 1, 0x32: 1, 0x33: 1, 0x34: 32, 0x40: 1, 0x41: 0,
                   0x50: 1, 0x60: 1, 0x70: 3, 0x71: 2, 0x72: 1, 0x00: 0}

        def s16(x):
            return x - 0x10000 if x & 0x8000 else x

        def s10(x):
            return x - 0x400 if x & 0x200 else x

        def flush():
            if prim is None or not verts:
                return
            if prim == 0:
                for k in range(0, len(verts) - 2, 3):
                    tris.append(verts[k:k + 3])
            elif prim == 1:
                for k in range(0, len(verts) - 3, 4):
                    q = verts[k:k + 4]
                    tris.extend([[q[0], q[1], q[2]], [q[0], q[2], q[3]]])
            elif prim == 2:
                for k in range(len(verts) - 2):
                    tris.append(verts[k:k + 3])
            else:
                for k in range(0, len(verts) - 3, 2):
                    a, b, c, d = verts[k:k + 4]
                    tris.extend([[a, b, d], [a, d, c]])

        i = 0
        while i + 4 <= len(dl):
            cmds = dl[i:i + 4]
            i += 4
            for c in cmds:
                n = nparams.get(c, 0)
                p = struct.unpack_from(f"<{n}I", dl, i) if n else ()
                i += 4 * n
                if c == 0x40:
                    flush()
                    verts, prim = [], p[0] & 3
                elif c == 0x41:
                    flush()
                    verts, prim = [], None
                elif c == 0x22:
                    st = (s16(p[0] & 0xFFFF) / 16.0, s16(p[0] >> 16) / 16.0)
                elif c in (0x23, 0x24, 0x25, 0x26, 0x27, 0x28):
                    if c == 0x23:
                        v = [s16(p[0] & 0xFFFF) / 4096.0, s16(p[0] >> 16) / 4096.0, s16(p[1] & 0xFFFF) / 4096.0]
                    elif c == 0x24:
                        v = [s10(p[0] & 0x3FF) / 64.0, s10((p[0] >> 10) & 0x3FF) / 64.0, s10((p[0] >> 20) & 0x3FF) / 64.0]
                    elif c == 0x25:
                        v = [s16(p[0] & 0xFFFF) / 4096.0, s16(p[0] >> 16) / 4096.0, v[2]]
                    elif c == 0x26:
                        v = [s16(p[0] & 0xFFFF) / 4096.0, v[1], s16(p[0] >> 16) / 4096.0]
                    elif c == 0x27:
                        v = [v[0], s16(p[0] & 0xFFFF) / 4096.0, s16(p[0] >> 16) / 4096.0]
                    else:
                        v = [v[0] + s10(p[0] & 0x3FF) / 512.0, v[1] + s10((p[0] >> 10) & 0x3FF) / 512.0,
                             v[2] + s10((p[0] >> 20) & 0x3FF) / 512.0]
                    verts.append((tuple(v), st))
        flush()
        return [([a[0] for a in t], [a[1] for a in t]) for t in tris if len(t) == 3]


# ------------------------------------------------------------ rasteriser
class Canvas:
    """A top-down colour and height buffer, pixels per tile `px`."""

    def __init__(self, tiles_w, tiles_h, px):
        self.px = px
        self.rgb = np.zeros((tiles_h * px, tiles_w * px, 3), np.uint8)
        self.rgb[:] = (20, 20, 28)
        self.height = np.full((tiles_h * px, tiles_w * px), -1e9)

    def draw(self, tris, texture, tex_scale, ox, oz, alpha=31):
        """Triangles in world units; ox, oz is the world position of pixel 0.
        `alpha` is the material's 0..31. A translucent surface (a prop's shadow,
        water) is blended over what is below and only claims the height buffer
        where it is mostly opaque; alpha 0 draws nothing, as on the DS."""
        if alpha == 0:
            return
        px = self.px
        H, W = self.height.shape
        th, tw = (texture.shape[0], texture.shape[1]) if texture is not None else (1, 1)
        for pos, st in tris:
            X = np.array([(p[0] - ox) / TILE * px for p in pos])
            Z = np.array([(p[2] - oz) / TILE * px for p in pos])
            Y = np.array([p[1] for p in pos])
            x0, x1 = max(int(np.floor(X.min())), 0), min(int(np.ceil(X.max())), W)
            z0, z1 = max(int(np.floor(Z.min())), 0), min(int(np.ceil(Z.max())), H)
            if x0 >= x1 or z0 >= z1:
                continue
            den = (Z[1] - Z[2]) * (X[0] - X[2]) + (X[2] - X[1]) * (Z[0] - Z[2])
            if abs(den) < 1e-9:
                continue
            gx, gz = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(z0, z1) + 0.5)
            l0 = ((Z[1] - Z[2]) * (gx - X[2]) + (X[2] - X[1]) * (gz - Z[2])) / den
            l1 = ((Z[2] - Z[0]) * (gx - X[2]) + (X[0] - X[2]) * (gz - Z[2])) / den
            l2 = 1 - l0 - l1
            inside = (l0 >= -1e-6) & (l1 >= -1e-6) & (l2 >= -1e-6)
            if not inside.any():
                continue
            y = l0 * Y[0] + l1 * Y[1] + l2 * Y[2]
            hb = self.height[z0:z1, x0:x1]
            win = inside & (y >= hb)
            if texture is None:
                sel = win
                cols = np.broadcast_to(np.array([90, 90, 90], np.float64), (sel.sum(), 3))
                a = np.full(sel.sum(), alpha / 31.0)
            else:
                s = (l0 * st[0][0] + l1 * st[1][0] + l2 * st[2][0]) * tex_scale[0]
                t = (l0 * st[0][1] + l1 * st[1][1] + l2 * st[2][1]) * tex_scale[1]
                si = np.floor(s).astype(int) % tw
                ti = np.floor(t).astype(int) % th
                texel = texture[ti, si]
                sel = win & (texel[..., 3] > 0)
                cols = texel[..., :3][sel].astype(np.float64)
                a = texel[..., 3][sel] / 255.0 * (alpha / 31.0)
            if not sel.any():
                continue
            block = self.rgb[z0:z1, x0:x1]
            old = block[sel].astype(np.float64)
            block[sel] = (old * (1 - a[:, None]) + cols * a[:, None]).astype(np.uint8)
            solid = np.zeros_like(sel)
            solid[sel] = a >= 0.5
            hb[solid] = y[solid]


# ------------------------------------------------------------ the map
def load_json(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return json.load(f)


def header_fields(header):
    text = open(os.path.join(ROOT, "include", "data", "map_headers.h")).read()
    i = text.index(f"[{header}] = {{")
    block = text[i:text.index("}", i)]
    return {k: v for k, v in re.findall(r"\.(\w+) = ([^,]+),", block)}


def chunks_of(header, fields):
    """[(matrix row, col, map_data number)] of the header's chunks."""
    mat = load_json(f"res/field/matrices/{fields['mapMatrixID']}.json")
    out = []
    for r, row in enumerate(mat["maps"]):
        for c, name in enumerate(row):
            hdr = mat["headers"][r][c] if mat.get("headers") else header
            if hdr == header and name.startswith("MAP_"):
                out.append((r, c, int(name.split("_")[1])))
    return out, bool(mat.get("headers"))


def split_land(data):
    perm, props, model, _bdhc = struct.unpack_from("<4I", data, 0)
    p = 16
    return (data[p:p + perm], data[p + perm:p + perm + props],
            data[p + perm + props:p + perm + props + model])


def render(header, px=8, marks=(), out=None, draw_all=False):
    fields = header_fields(header)
    area = load_json(f"res/field/area_data/{fields['areaDataArchiveID']}.json")
    maptex = TextureSet(open(os.path.join(ROOT, "res/field/maps/texture_sets", area["mapTextureSet"] + ".nsbtx"), "rb").read())
    prop_set_no = area["mapPropSet"].split("_")[-1]
    ppath = os.path.join(ROOT, "res/field/props/texture_sets", f"prop_texture_set_{prop_set_no}.nsbtx")
    proptex = TextureSet(open(ppath, "rb").read()) if os.path.exists(ppath) else None
    # a prop's model id is its index in the archive's build order, and some
    # models are named (doors, slopes) rather than numbered
    with open(os.path.join(ROOT, "res/field/props/models/map_prop_models.order")) as f:
        prop_order = [line.strip() for line in f if line.strip()]
    chunks, global_coords = chunks_of(header, fields)
    if not chunks:
        sys.exit(f"{header}: no chunks found")
    rows = [r for r, _, _ in chunks]
    cols = [c for _, c, _ in chunks]
    r0, c0 = min(rows), min(cols)
    tw, th = (max(cols) - c0 + 1) * CHUNK, (max(rows) - r0 + 1) * CHUNK
    canvas = Canvas(tw, th, px)
    perms = {}
    missing = set()
    for r, c, n in chunks:
        data = open(os.path.join(ROOT, f"res/field/maps/data/map_data_{n:03d}.bin"), "rb").read()
        perm, props, model = split_land(data)
        perms[(r, c)] = perm
        # world x of the canvas' left edge, in this chunk's model space
        ox = -256.0 - (c - c0) * CHUNK * TILE
        oz = -256.0 - (r - r0) * CHUNK * TILE
        m = Model(model)
        for mi, si in m.draws:
            mat = m.materials[mi]
            if not draw_all and SKIP_MATERIALS.search(mat["name"]):
                continue
            tex = None
            if mat["tex"] in maptex.textures:
                try:
                    tex = maptex.decode(mat["tex"], mat["pal"])
                except Exception:
                    tex = None
            elif mat["tex"]:
                missing.add(mat["tex"])
            tris = [([(p[0] * m.pos_scale, p[1] * m.pos_scale, p[2] * m.pos_scale) for p in pos], st)
                    for pos, st in m.triangles(m.shapes[si])]
            canvas.draw(tris, tex, mat["scale"], ox, oz, mat["alpha"])
        for k in range(len(props) // 0x30):
            mid, x, y, z, _rx, _ry, _rz, sx, sy, sz = struct.unpack_from("<i3i3i3i", props, k * 0x30)
            if not 0 <= mid < len(prop_order):
                continue
            path = os.path.join(ROOT, "res/field/props/models", prop_order[mid])
            pm = Model(open(path, "rb").read())
            px_, py_, pz_ = x / 4096.0, y / 4096.0, z / 4096.0
            scl = (sx / 4096.0 or 1.0, sy / 4096.0 or 1.0, sz / 4096.0 or 1.0)
            for mi, si in pm.draws:
                mat = pm.materials[mi]
                tex = None
                if proptex and mat["tex"] in proptex.textures:
                    try:
                        tex = proptex.decode(mat["tex"], mat["pal"])
                    except Exception:
                        tex = None
                tris = [([(p[0] * pm.pos_scale * scl[0] + px_, p[1] * pm.pos_scale * scl[1] + py_,
                           p[2] * pm.pos_scale * scl[2] + pz_) for p in pos], st)
                        for pos, st in pm.triangles(pm.shapes[si])]
                canvas.draw(tris, tex, mat["scale"], ox, oz, mat["alpha"])
    img = Image.fromarray(canvas.rgb).convert("RGBA")
    over = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    gx0 = c0 * CHUNK if global_coords else 0
    gz0 = r0 * CHUNK if global_coords else 0
    for (r, c), perm in perms.items():
        for tz in range(CHUNK):
            for tx in range(CHUNK):
                v = struct.unpack_from("<H", perm, (tz * CHUNK + tx) * 2)[0]
                X = ((c - c0) * CHUNK + tx) * px
                Z = ((r - r0) * CHUNK + tz) * px
                if v >> 15:
                    d.rectangle([X, Z, X + px - 1, Z + px - 1], fill=(0, 0, 0, 70))
                if v & 0xFF in (0x02, 0x03):
                    d.rectangle([X, Z, X + px - 1, Z + px - 1], outline=(40, 255, 40, 200))
    for x in range(0, img.size[0], px):
        d.line([x, 0, x, img.size[1]], fill=(255, 255, 255, 18 if (x // px) % 8 else 60))
    for z in range(0, img.size[1], px):
        d.line([0, z, img.size[0], z], fill=(255, 255, 255, 18 if (z // px) % 8 else 60))
    ev_name = fields["eventsArchiveID"]
    ev = load_json(f"res/field/events/{ev_name}.json")

    def cell(x, z):
        return ((x - gx0) * px, (z - gz0) * px)

    for w in ev.get("warp_events", []):
        X, Z = cell(w["x"], w["z"])
        d.rectangle([X + 1, Z + 1, X + px - 2, Z + px - 2], outline=(80, 140, 255, 255), width=2)
    for k, o in enumerate(ev.get("object_events", [])):
        X, Z = cell(o["x"], o["z"])
        d.rectangle([X + 1, Z + 1, X + px - 2, Z + px - 2], fill=(230, 40, 40, 200))
        d.text((X + 1, Z - 1), str(k), fill=(255, 255, 255, 255))
    for x0, z0, x1, z1 in marks:
        X0, Z0 = cell(x0, z0)
        X1, Z1 = cell(x1 + 1, z1 + 1)
        d.rectangle([X0, Z0, X1 - 1, Z1 - 1], outline=(255, 230, 0, 255), width=2)
    img = Image.alpha_composite(img, over)
    # a margin with coordinate labels every eight tiles
    margin = 28
    framed = Image.new("RGBA", (img.size[0] + margin, img.size[1] + margin), (255, 255, 255, 255))
    framed.paste(img, (margin, margin))
    fd = ImageDraw.Draw(framed)
    for t in range(0, tw, 8):
        fd.text((margin + t * px, 2), str(gx0 + t), fill=(0, 0, 0, 255))
    for t in range(0, th, 8):
        fd.text((1, margin + t * px), str(gz0 + t), fill=(0, 0, 0, 255))
    fd.text((margin, margin + img.size[1] - 12), header, fill=(255, 255, 255, 255))
    if out:
        framed.convert("RGB").save(out)
    return framed, missing, (gx0, gz0, tw, th)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("header", help="a MAP_HEADER_* name")
    ap.add_argument("--out", default=None)
    ap.add_argument("--px", type=int, default=8, help="pixels per tile")
    ap.add_argument("--all", action="store_true", help="also draw lamps and their glow")
    ap.add_argument("--mark", action="append", default=[],
                    help="x0,z0,x1,z1 in event coordinates, inclusive; repeatable")
    a = ap.parse_args()
    marks = [tuple(int(v) for v in m.split(",")) for m in a.mark]
    out = a.out or f"{a.header.lower()}.png"
    _img, missing, (gx0, gz0, tw, th) = render(a.header, a.px, marks, out, a.all)
    print(f"{out}: tiles x {gx0}..{gx0 + tw - 1}, z {gz0}..{gz0 + th - 1}"
          + (f"; textures not in the set: {sorted(missing)}" if missing else ""))


if __name__ == "__main__":
    main()
