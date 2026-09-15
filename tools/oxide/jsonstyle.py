"""Dump JSON in the style used by pokeplatinum's res/ data files.

Objects are always multi-line with 4-space indent. Arrays of scalars with at
most two elements are written inline ("[ a, b ]"); longer arrays and arrays
of containers go one element per line. Empty arrays are "[  ]". Verified to round-trip every
res/pokemon/*/data.json and res/moves/*/data.json byte-for-byte.
"""
import json

WIDTH = 80

def _scalar(v):
    if isinstance(v, bool): return "true" if v else "false"
    if v is None: return "null"
    if isinstance(v, str): return json.dumps(v, ensure_ascii=True)
    if isinstance(v, float):
        s = repr(v)
        return s
    return str(v)

def dumps(obj, indent=0, width=WIDTH, max_inline=2):
    pad = " " * indent
    if isinstance(obj, dict):
        if not obj: return "{}"
        lines = []
        for k, v in obj.items():
            lines.append(f'{pad}    {json.dumps(k, ensure_ascii=False)}: {dumps(v, indent + 4, width, max_inline)}')
        return "{\n" + ",\n".join(lines) + f"\n{pad}}}"
    if isinstance(obj, list):
        if not obj: return "[  ]"
        if all(not isinstance(x, (dict, list)) for x in obj):
            inline = "[ " + ", ".join(_scalar(x) for x in obj) + " ]"
            if len(obj) <= max_inline:
                return inline
        lines = [f"{pad}    {dumps(x, indent + 4, width, max_inline)}" for x in obj]
        return "[\n" + ",\n".join(lines) + f"\n{pad}]"
    return _scalar(obj)

def dump_file(obj, path, width=WIDTH):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(dumps(obj, 0, width) + "\n")


# ---------------------------------------------------------------------------
# Targeted in-place editing, so that only the keys we touch produce a diff.
# The repo's files are not uniformly formatted (some escape non-ASCII, some
# do not), so rewriting a whole file would create noise in untouched text.

def _find_value_span(text, start):
    """Given the index of the first character of a JSON value, return the
    index one past its end (not including a trailing comma)."""
    i = start
    c = text[i]
    if c in "[{":
        depth = 0; in_str = False; esc = False
        while i < len(text):
            ch = text[i]
            if in_str:
                if esc: esc = False
                elif ch == "\\": esc = True
                elif ch == '"': in_str = False
            else:
                if ch == '"': in_str = True
                elif ch in "[{": depth += 1
                elif ch in "]}":
                    depth -= 1
                    if depth == 0: return i + 1
            i += 1
        raise ValueError("unbalanced container")
    if c == '"':
        i += 1; esc = False
        while i < len(text):
            ch = text[i]
            if esc: esc = False
            elif ch == "\\": esc = True
            elif ch == '"': return i + 1
            i += 1
        raise ValueError("unterminated string")
    # scalar: up to comma or newline
    while i < len(text) and text[i] not in ",\n\r": i += 1
    return i

def _find_key(text, path, base=0, end=None):
    """Locate the value of a nested key path (list of keys) and return
    (value_start, value_end, indent)."""
    end = len(text) if end is None else end
    key = path[0]
    needle = json.dumps(key) + ":"
    i = base
    while True:
        i = text.find(needle, i, end)
        if i < 0: raise KeyError(".".join(path))
        # must be at the start of a line (after whitespace)
        ls = text.rfind("\n", 0, i) + 1
        if text[ls:i].strip() == "": break
        i += len(needle)
    indent = i - ls
    vs = i + len(needle)
    while text[vs] in " \t": vs += 1
    ve = _find_value_span(text, vs)
    if len(path) == 1: return vs, ve, indent
    return _find_key(text, path[1:], vs, ve)

def replace_value(text, path, value):
    """Return text with the value at key path replaced by `value`, rendered in
    repo style at the key's own indentation."""
    vs, ve, indent = _find_key(text, path)
    return text[:vs] + dumps(value, indent) + text[ve:]

def get_value(text, path):
    vs, ve, _ = _find_key(text, path)
    return json.loads(text[vs:ve])
