"""Dump JSON in the style used by pokeplatinum's res/ data files.

Objects are always multi-line with 4-space indent. Arrays of scalars with at
most `max_inline` elements are written inline ("[ a, b ]"); longer arrays and
arrays of containers go one element per line.

The repo's res/ folders are not all in one style, so the differences are
options rather than guesses. `res/moves/*/data.json` is
`max_inline=0, ascii_strings=False, empty_array="[]"`, which round-trips all
468 of those files byte for byte; the defaults are the older res/pokemon
style. Check with a round-trip before trusting either on a folder that is not
one of those two.
"""
import json

WIDTH = 80

def _scalar(v, ascii_strings=True):
    if isinstance(v, bool): return "true" if v else "false"
    if v is None: return "null"
    if isinstance(v, str): return json.dumps(v, ensure_ascii=ascii_strings)
    if isinstance(v, float):
        s = repr(v)
        return s
    return str(v)

def dumps(obj, indent=0, width=WIDTH, max_inline=2, ascii_strings=True,
          empty_array="[  ]"):
    pad = " " * indent
    kw = dict(max_inline=max_inline, ascii_strings=ascii_strings,
              empty_array=empty_array)
    if isinstance(obj, dict):
        if not obj: return "{}"
        lines = []
        for k, v in obj.items():
            lines.append(f'{pad}    {json.dumps(k, ensure_ascii=False)}: {dumps(v, indent + 4, width, **kw)}')
        return "{\n" + ",\n".join(lines) + f"\n{pad}}}"
    if isinstance(obj, list):
        if not obj: return empty_array
        if all(not isinstance(x, (dict, list)) for x in obj):
            inline = "[ " + ", ".join(_scalar(x, ascii_strings) for x in obj) + " ]"
            if len(obj) <= max_inline:
                return inline
        lines = [f"{pad}    {dumps(x, indent + 4, width, **kw)}" for x in obj]
        return "[\n" + ",\n".join(lines) + f"\n{pad}]"
    return _scalar(obj, ascii_strings)

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

def _nth_array_element(text, arr_start, arr_end, n):
    """Given the span of an array value (arr_start points at '[', arr_end is
    one past ']'), return (elem_start, elem_end) for its n-th element."""
    i = arr_start + 1
    for idx in range(n + 1):
        while text[i] in " \t\n\r": i += 1
        if text[i] == "]":
            raise IndexError(f"array index {n} out of range")
        vs = i
        ve = _find_value_span(text, vs)
        if idx == n:
            return vs, ve
        i = ve
        while text[i] in " \t\n\r": i += 1
        if text[i] == ",": i += 1
    raise IndexError(n)

def _find_key(text, path, base=0, end=None):
    """Locate the value of a nested key path and return (value_start,
    value_end, indent). A path element may be a string (object member) or an
    int (array index into the array value found by the previous element)."""
    end = len(text) if end is None else end
    key = path[0]

    if isinstance(key, int):
        vs, ve = _nth_array_element(text, base, end, key)
        ls = text.rfind("\n", 0, vs) + 1
        indent = (vs - ls) if text[ls:vs].strip() == "" else 0
        if len(path) == 1: return vs, ve, indent
        return _find_key(text, path[1:], vs, ve)

    needle = json.dumps(key) + ":"
    i = base
    while True:
        i = text.find(needle, i, end)
        if i < 0: raise KeyError(".".join(str(p) for p in path))
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

def insert_key(text, obj_path, after_key, new_key, value):
    """Insert `new_key: value` as a new key immediately following `after_key`,
    within the object located at obj_path (obj_path may be [] for the
    top-level object; its elements may include array indices). For adding a
    key that doesn't exist anywhere yet, which replace_value can't do since it
    only edits an existing key's value."""
    if obj_path:
        vs, ve, _ = _find_key(text, obj_path)
    else:
        vs, ve = 0, len(text)
    _, ave, indent = _find_key(text, [after_key], vs, ve)
    entry = f'\n{" " * indent}{json.dumps(new_key)}: {dumps(value, indent)}'
    if text[ave] == ",":
        return text[:ave + 1] + entry + "," + text[ave + 1:]
    return text[:ave] + "," + entry + text[ave:]
