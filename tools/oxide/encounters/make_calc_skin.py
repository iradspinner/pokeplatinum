"""Write calc/oxide-skin.css: the vendored calculator's colours, on the tool's tokens.

    PYTHONPATH=. python3 -m tools.oxide.encounters.make_calc_skin

The visual design (section 8) asks for the calculator to keep its own markup and
layout and to take the tool's colours, following the same light and dark toggle.
Upstream draws a dark theme only, in about 1,100 colour literals across its
stylesheets, so the skin is generated rather than written: every rule that sets
a colour is repeated with each literal replaced by the token for its role, and
nothing else. The skin loads after every upstream stylesheet, so a repeated rule
wins by order at the same specificity, and the upstream files stay untouched.
Rerun this after updating the calculator; `test_m8` fails if the skin is stale.

How a literal becomes a token. What it colours decides the family: a background,
a text colour or a line. How light and how saturated it is picks the member.
Upstream's greys run from its page ground (#181818) up to its text (#f1f1f1),
so a dark grey behind something is the ground, a panel or a sunken field, a
light grey in front of something is ink, and a middle grey is dim text or a
rule. Its accents are few: violet (#bb86fc) marks what is selected, which is
the tool's "place" pink; teal, green, cyan and blue are data, which is "mass";
red is an error; yellow and orange are the one number worth acting on or a
warning. A saturated background is tinted into the panel rather than painted
at full strength, so text on it stays readable in both themes. Translucency is
kept, as a mix of the token into transparent.

Colours the calculator's scripts set inline are few (speed comparisons, boosted
stats, a highlighted border), and the header maps those by their exact values.
What it does not reach: any other inline colour, and the battle console's and
the fragsheet grid's own stylesheets, which style panels the calculator view
does not use.
"""
import colorsys
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CALC = os.path.join(HERE, "calc")
OUT = os.path.join(CALC, "oxide-skin.css")

# In the order the page loads them, so the skin keeps upstream's cascade.
SOURCES = ["js/vendor/select2/select2.css", "css/vendor/bootstrap.css",
           "css/main.css", "css/frags.css", "css/encounters.css",
           "css/settings-ui.css"]

BACKGROUND = {"background", "background-color", "background-image"}
TEXT = {"color", "fill", "caret-color", "-webkit-text-fill-color",
        "text-decoration-color", "text-shadow"}
LINE = {"border", "border-color", "border-top", "border-right", "border-bottom",
        "border-left", "border-top-color", "border-right-color",
        "border-bottom-color", "border-left-color", "outline", "outline-color",
        "stroke", "column-rule", "column-rule-color"}
SHADOW = {"box-shadow"}

NAMED = {"white": (255, 255, 255), "black": (0, 0, 0)}
LITERAL = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba?\(\s*[\d.]+%?\s*,\s*[\d.]+%?\s*,"
                     r"\s*[\d.]+%?\s*(?:,\s*[\d.]+%?\s*)?\)|\b(?:white|black)\b")


def parse(literal):
    """(r, g, b, alpha) for a colour literal, or None."""
    lit = literal.lower()
    if lit in NAMED:
        return NAMED[lit] + (1.0,)
    if lit.startswith("#"):
        h = lit[1:]
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        if len(h) not in (6, 8):
            return None
        rgb = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
        return rgb + ((int(h[6:8], 16) / 255) if len(h) == 8 else 1.0,)
    nums = re.findall(r"[\d.]+%?", lit)
    vals = [float(n[:-1]) * 2.55 if n.endswith("%") else float(n) for n in nums[:3]]
    alpha = 1.0
    if len(nums) > 3:
        a = nums[3]
        alpha = float(a[:-1]) / 100 if a.endswith("%") else float(a)
    return tuple(int(round(v)) for v in vals) + (alpha,)


def luminance(r, g, b):
    def lin(v):
        v /= 255
        return v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4
    return .2126 * lin(r) + .7152 * lin(g) + .0722 * lin(b)


def family(r, g, b):
    """The accent a saturated colour belongs to, or None for a grey."""
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if s < 0.3 or l < 0.08 or l > 0.95:
        return None
    deg = h * 360
    if 245 <= deg < 320:
        return "place"                      # upstream's violet: what is selected
    if deg >= 320 or deg < 15:
        return "error"
    if 15 <= deg < 45:
        return "warn"
    if 45 <= deg < 70:
        return "act"
    return "mass"                           # green, teal, cyan and blue: data


def token(role, rgba):
    r, g, b, _ = rgba
    fam = family(r, g, b)
    lum = luminance(r, g, b)
    if role == "background":
        if fam == "place":
            return "var(--place-bg)"
        if fam:
            return f"color-mix(in srgb, var(--{'mass' if fam == 'mass' else fam}) 22%, var(--panel))"
        if lum < 0.012:
            return "var(--ground)"
        if lum < 0.03:
            return "var(--panel)"
        if lum < 0.35:
            return "var(--sunken)"
        return "var(--sunken)"              # a light chip in a dark theme
    if role == "text":
        if fam == "place":
            return "var(--place-ink)"
        if fam:
            return f"var(--{fam})"
        if lum > 0.3 or lum < 0.02:
            return "var(--ink)"             # upstream's text, or dark text on a chip
        return "var(--dim)"
    if role == "line":
        if fam == "place":
            return "var(--place-ink)"
        if fam:
            return f"var(--{fam})"
        return "var(--faint)" if lum > 0.3 else "var(--rule)"
    return "var(--shadow)"                  # a box shadow


def swap(value, role):
    """The value with every colour literal replaced, or None if it has none."""
    changed = False

    def one(m):
        nonlocal changed
        rgba = parse(m.group(0))
        if rgba is None:
            return m.group(0)
        changed = True
        tok = token(role, rgba)
        a = rgba[3]
        if a >= 0.999 or role == "shadow":
            return tok
        return f"color-mix(in srgb, {tok} {round(a * 100)}%, transparent)"

    out = LITERAL.sub(one, value)
    return out if changed else None


def role_of(prop):
    if prop in BACKGROUND:
        return "background"
    if prop in TEXT:
        return "text"
    if prop in LINE:
        return "line"
    if prop in SHADOW:
        return "shadow"
    return None


def rules(css):
    """[(at-rule prelude or None, selector, declarations)] for each style rule,
    one level of @media or @supports deep. Keyframes and font faces are
    skipped: they carry no colour worth mapping."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    n = len(css)
    found = []

    def block(start):
        depth, j = 0, start
        while j < n:
            if css[j] == "{":
                depth += 1
            elif css[j] == "}":
                depth -= 1
                if depth == 0:
                    return j
            j += 1
        return n

    def walk(lo, hi, at):
        j = lo
        while j < hi:
            brace = css.find("{", j, hi)
            if brace < 0:
                return
            prelude = css[j:brace].strip()
            end = block(brace)
            if prelude.startswith("@"):
                if prelude.startswith(("@media", "@supports")) and at is None:
                    walk(brace + 1, end, prelude)
            elif prelude:
                found.append((at, prelude, css[brace + 1:end]))
            j = end + 1

    walk(0, n, None)
    return found


def skin_rules(css):
    out = []
    for at, selector, body in rules(css):
        decls = []
        for decl in body.split(";"):
            if ":" not in decl:
                continue
            prop, value = decl.split(":", 1)
            prop = prop.strip().lower()
            role = role_of(prop)
            if not role or "var(" in value:
                continue
            new = swap(value.strip(), role)
            if new:
                decls.append(f"{prop}: {new}")
        if decls:
            out.append((at, " ".join(selector.split()), decls))
    return out


HEADER = """/* GENERATED by tools/oxide/encounters/make_calc_skin.py; do not edit by hand.

   The vendored calculator's colours on the encounter tool's tokens, so it
   follows the same palette and the same light and dark toggle (visual design
   section 8). Each rule repeats an upstream rule that sets a colour, with the
   literal replaced by the token for its role; layout is untouched. Loaded
   after every upstream stylesheet, so a repeated rule wins by order. */

@import url("/theme.css");

html, body { background: var(--ground); color: var(--ink); }

/* Colours the calculator's scripts set inline, which no stylesheet rule can
   reach without !important: a faster speed in cyan and a slower one in red,
   a boosted stat in violet, a highlighted border in red. Matched at the start
   of the style or after a semicolon, so a background of the same colour is
   not taken for a text colour. */
[style^="color: rgb(139, 233, 253)"], [style*="; color: rgb(139, 233, 253)"] { color: var(--mass) !important; }
[style^="color: rgb(255, 85, 85)"], [style*="; color: rgb(255, 85, 85)"] { color: var(--error) !important; }
[style^="color: rgb(187, 134, 252)"], [style*="; color: rgb(187, 134, 252)"],
[style^="color: rgb(189, 147, 249)"], [style*="; color: rgb(189, 147, 249)"] { color: var(--place-ink) !important; }
[style*="border-color: rgb(255, 85, 85)"] { border-color: var(--error) !important; }
"""


def build():
    parts = [HEADER]
    for rel in SOURCES:
        with open(os.path.join(CALC, rel), encoding="utf-8") as f:
            found = skin_rules(f.read())
        parts.append(f"\n/* ---- {rel} ({len(found)} rules) ---- */\n")
        for at, selector, decls in found:
            body = "; ".join(decls)
            rule = f"{selector} {{ {body}; }}"
            parts.append(f"{at} {{ {rule} }}\n" if at else rule + "\n")
    return "".join(parts)


def main():
    text = build()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"wrote {os.path.relpath(OUT)}: {text.count(chr(10))} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
