"""Classify every member the base ROM changed in the given archives: a re-save
(same content, different packing) or an edit (different content).

For each member where the base ROM differs from vanilla:
  1. LZ10-compressed on either side: decompress both. Equal after that means
     the member was only recompressed.
  2. A Nitro graphics file: compare block by block, splitting each block into
     its header fields and its content (tile data for CHAR, colours for PLTT,
     everything past the 8-byte block header for the rest). Tile data is also
     compared after Platinum's sprite decryption, since a re-save may
     re-encrypt with a new seed.
  3. Anything else: raw bytes.

Also says whether the Oxide build carries the base ROM's version.

    python3 tools/oxide/editcheck.py ~/roms/vanilla.nds ~/roms/base.nds BUILT.nds ARCHIVE [ARCHIVE ...]

Written 2026-09-26 when the inventory's "tool side effect" archives turned out
to be edits. A DSPRE re-save writes file version 0x0100, a wrong file size, a
CHAR block size of 0, palette colours with bit 15 cleared, Pokemon sprites
re-encrypted under a new seed, tile data padded with zero tiles, and palettes
without their optional PCMP block; none of that changes what the game draws,
so each is compared away before a member is called an edit. verify_narcs.py
applies the same rules to the archives it lists in CONTENT_ARCHIVES.
"""
import struct
import sys

import ndspy.lz10
import ndspy.narc
import ndspy.rom


def walk(folder, prefix=""):
    out = {}
    for i, n in enumerate(folder.files):
        out[prefix + n] = folder.firstID + i
    for sub, f in folder.folders:
        out.update(walk(f, prefix + sub + "/"))
    return out


def maybe_lz(b):
    if len(b) >= 4 and b[0] == 0x10:
        try:
            return bytes(ndspy.lz10.decompress(b)), True
        except Exception:
            pass
    return bytes(b), False


def decrypt(data):
    """Platinum's sprite tile decryption, front to back (nitrogfx's Decode, mode 2)."""
    out = bytearray(data)
    if len(out) < 2:
        return bytes(out)
    enc = out[0] | out[1] << 8
    for i in range(0, len(out) - 1, 2):
        v = (out[i] | out[i + 1] << 8) ^ (enc & 0xFFFF)
        out[i], out[i + 1] = v & 0xFF, v >> 8
        enc = (enc * 1103515245 + 24691) & 0xFFFFFFFF
    return bytes(out)


ENCRYPTED = False

# Block magic (as stored, reversed) -> size of its own header, fields included.
BLOCK_HEADER = {b"RAHC": 0x20, b"TTLP": 0x18, b"SOPC": 0x10, b"PMCP": 0x08}


def blocks(b):
    """(magic, header bytes, content bytes) for each block, or None if b is not
    a Nitro file."""
    if len(b) < 16 or struct.unpack_from("<H", b, 4)[0] != 0xFEFF:
        return None
    hsize, n = struct.unpack_from("<HH", b, 12)
    out, at = [], hsize
    for _ in range(n):
        if at + 8 > len(b):
            return None
        magic = bytes(b[at:at + 4])
        size = struct.unpack_from("<I", b, at + 4)[0]
        if size == 0:
            # DSPRE's re-save writes 0 here; the block runs to the file's end
            size = len(b) - at
        if size < 8 or at + size > len(b) + 16:
            return None
        h = BLOCK_HEADER.get(magic, 8)
        out.append((magic, bytes(b[at:at + h]), bytes(b[at + h:at + size])))
        at += size
    return out


def classify(base, van):
    db, lzb = maybe_lz(base)
    dv, lzv = maybe_lz(van)
    if (lzb or lzv) and db == dv:
        return "recompressed only"
    bb, bv = blocks(db), blocks(dv)
    if bb is None or bv is None:
        if len(db) != len(dv):
            return f"raw data, size {len(dv)} to {len(db)}"
        n = sum(1 for x, y in zip(db, dv) if x != y)
        return f"raw data, {n} of {len(db)} bytes"
    parts = []
    # PCMP is an optional index of the palettes a file holds, and DSPRE drops it
    # on save; the colours are in PLTT either way, so only PLTT is compared.
    if any(m == b"PMCP" for m, _, _ in bb) != any(m == b"PMCP" for m, _, _ in bv):
        parts.append("PCMP block only on one side")
    bb = [x for x in bb if x[0] != b"PMCP"]
    bv = [x for x in bv if x[0] != b"PMCP"]
    if [m for m, _, _ in bb] != [m for m, _, _ in bv]:
        return f"blocks differ: {[m[::-1].decode() for m, _, _ in bv]} to {[m[::-1].decode() for m, _, _ in bb]}"
    for (m, hb, cb), (_, hv, cv) in zip(bb, bv):
        name = m[::-1].decode()
        if m == b"TTLP" and len(cb) == len(cv) and cb != cv:
            # Bit 15 of a colour is unused; DSPRE clears it, which changes nothing
            mb = [x & 0x7FFF for x in struct.unpack(f"<{len(cb) // 2}H", cb)]
            mv = [x & 0x7FFF for x in struct.unpack(f"<{len(cv) // 2}H", cv)]
            if mb == mv:
                parts.append(f"{name} top colour bit only")
                cb = cv
            else:
                n = sum(1 for x, y in zip(mb, mv) if x != y)
                parts.append(f"{name} content {n} of {len(mb)} colours")
                cb = cv
        if cb != cv:
            if m == b"RAHC" and len(cb) == len(cv) and decrypt(cb) == decrypt(cv):
                parts.append(f"{name} re-encrypted only")
            elif m == b"RAHC" and len(cb) == len(cv) and ENCRYPTED:
                n = sum(1 for x, y in zip(decrypt(cb), decrypt(cv)) if x != y)
                parts.append(f"{name} content {n} of {len(cb)} bytes once decrypted")
            elif m == b"RAHC" and not ENCRYPTED and cb.rstrip(b"\0") == cv.rstrip(b"\0"):
                # DSPRE pads tile data with zero tiles, which draw as nothing
                parts.append(f"{name} zero tiles appended only")
            elif len(cb) != len(cv):
                parts.append(f"{name} content {len(cv)} to {len(cb)} bytes")
            else:
                n = sum(1 for x, y in zip(cb, cv) if x != y)
                parts.append(f"{name} content {n} of {len(cb)} bytes")
        if hb != hv:
            offs = [i for i in range(min(len(hb), len(hv))) if hb[i] != hv[i]]
            parts.append(f"{name} header at {offs}")
    if not parts:
        return "file header only"
    return "; ".join(parts)


def is_edit(kind):
    return "content" in kind or kind.startswith("raw data") or kind.startswith("blocks differ")


def main():
    van, base, built = (ndspy.rom.NintendoDSRom.fromFile(p) for p in sys.argv[1:4])
    nv, nb, nu = walk(van.filenames), walk(base.filenames), walk(built.filenames)
    global ENCRYPTED
    for path in sys.argv[4:]:
        ENCRYPTED = "pokegra/" in path
        mv = ndspy.narc.NARC(van.files[nv[path]]).files
        mb = ndspy.narc.NARC(base.files[nb[path]]).files
        mu = ndspy.narc.NARC(built.files[nu[path]]).files
        changed = [i for i in range(len(mb)) if i >= len(mv) or mb[i] != mv[i]]
        edits = resaves = 0
        lines = []
        for i in changed:
            kind = classify(mb[i], mv[i]) if i < len(mv) else "new member"
            carried = i < len(mu) and mu[i] == mb[i]
            edit = kind == "new member" or is_edit(kind)
            edits += edit
            resaves += not edit
            lines.append(f"    {i}: {'EDIT' if edit else 're-save'}, {kind}"
                         f"{', carried over' if carried else ''}")
        print(f"{path}: {len(changed)} changed, {edits} edits, {resaves} re-saves")
        for line in lines:
            print(line)


if __name__ == "__main__":
    main()
