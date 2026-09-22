#!/usr/bin/env python3
"""Measure and wrap game text the way the game itself measures it.

Added for Phase 4 element 4, where 452 imported move descriptions had to be
made to fit Platinum's box. Nothing here is move-specific.

How the width is computed, from the engine rather than by eye:
`Font_CalcStringWidth` calls `FontManager_CalcStringWidth`, which sums
`glyphWidthFunc(fontManager, charcode - 1) + letterSpacing` over the string.
`sFontAttributes` in `src/font.c` gives FONT_SYSTEM, FONT_MESSAGE and
FONT_SUBSCREEN a `letterSpacing` of 0 and a `maxLetterHeight` of 16 with a
`lineSpacing` of 0, so a line is 16 pixels tall and a string is just the sum of
its glyph widths. The widths themselves are `res/fonts/font_message.json`, and
the charcode comes from `tools/msgenc/charmap.txt`. Note the minus one: the
charmap's code is one more than the glyph index.

The metric is calibrated, not assumed. Platinum's own longest move description
line measures exactly 120 pixels, which is exactly the width of the window that
draws it (15 tiles). If a change to this file makes that stop being true, the
change is wrong.

Known box sizes, read off the WindowTemplate that draws each one:

  move description   120 px x 5 lines   `SUMMARY_WINDOW_BATTLE_MOVE_DESCRIPTION`
                                        and `MOVE_REMINDER_WIN_MOVE_BATTLE_DESCRIPTION`,
                                        both 15 x 10 tiles
  move name           87 px x 1 line    `SUMMARY_WINDOW_BATTLE_MOVE_1`..`_5`,
                                        11 tiles wide, printed at x = 1

    tools/oxide/oxide-python tools/oxide/textfit.py "some text to measure"
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CHARMAP = os.path.join(ROOT, "tools", "msgenc", "charmap.txt")
FONT = os.path.join(ROOT, "res", "fonts", "font_message.json")

MOVE_DESC_WIDTH = 120
MOVE_DESC_LINES = 5
MOVE_NAME_WIDTH = 87


def _load_charmap(path=CHARMAP):
    m = {}
    for line in open(path, encoding="utf-8"):
        line = line.split("//")[0].rstrip("\n")
        if "=" not in line:
            continue
        code, ch = line.split("=", 1)
        code = code.strip()
        if len(ch) == 1 and len(code) == 4:
            m[ch] = int(code, 16)
    return m


CMAP = _load_charmap()
WIDTHS = json.load(open(FONT, encoding="utf-8"))["glyphWidths"]


def px(s):
    """Width of one line in pixels. Raises on a character the game has no
    glyph for, which is the point: a silent zero would hide the problem."""
    total = 0
    for c in s:
        code = CMAP.get(c)
        if code is None:
            raise KeyError("no charmap entry for %r" % c)
        g = code - 1
        if g >= len(WIDTHS):
            raise KeyError("%r is charcode %#x, past the %d glyphs this font has"
                           % (c, code, len(WIDTHS)))
        total += WIDTHS[g]
    return total


def wrap(text, width=MOVE_DESC_WIDTH):
    """Greedy word wrap to a pixel width. A single word wider than the box is
    left on its own line rather than broken, and `fits` will then say no."""
    out, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if px(trial) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def fits(lines, width=MOVE_DESC_WIDTH, max_lines=MOVE_DESC_LINES):
    return len(lines) <= max_lines and all(px(l) <= width for l in lines)


def as_description(lines):
    """A wrapped block in the shape res/moves/*/data.json stores: every line
    but the last carries the newline that ends it."""
    return [l + "\n" for l in lines[:-1]] + lines[-1:]


def flatten(description):
    """The inverse: a data.json description back to one paragraph of words."""
    return " ".join(l.replace("\r", "").replace("\n", " ") for l in description)


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        return
    for arg in sys.argv[1:]:
        lines = wrap(arg)
        print("%d px, %d line(s), fits: %s" % (max(px(l) for l in lines), len(lines),
                                               "yes" if fits(lines) else "no"))
        for l in lines:
            print("  %3d px  %s" % (px(l), l))


if __name__ == "__main__":
    import pinned_python
    pinned_python.ensure()
    main()
