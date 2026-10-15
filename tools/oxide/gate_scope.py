#!/usr/bin/env python3
"""Which of the gate's checks a landing needs, from the files it changes.

Platinum Oxide project. `integrate.sh --since REF` runs a check only when the
landing changes something that check reads (Ian, 2026-10-13: most of the
gate's time went to tool suites that most landings never touch). What a check
reads is worked out from the code each time, so a new check or a new import
needs no list kept by hand. A check's module reads:

  - every tools/oxide module its imports reach, including a module it loads
    by path or launches by name (`import_module("bulk_events")`, a server
    under test run with `-m tools.oxide.encounters.server`);
  - any other file that a module in that closure names in its code: a string
    that is the file's name or ends in "/" and its name, a path the file lies
    under, or a path joined into a folder it sits in that stops there or goes
    on with a name worked out at run time (os.path.join(ROOT, "docs",
    "oxide", "learnset-sheets")). A module in the file's own tool package
    names its folders by the bare word too (os.path.join(HERE, "ui")).
    Docstrings, printed messages and argparse help are left out, since they
    mention docs for a person to open, not for the tool to read.

Some changes run the whole gate: anything outside docs/, .claude/ and
tools/oxide/ (the game's data and engine, the build), apart from Markdown at
the top of the repo; the gate's own scripts; a deleted tool file; a tool file
the build reads; and a data file (anything but Markdown) under docs/ or
tools/oxide/ that no module names, since its reader is unknown. Markdown that
no module names is prose, and needs only the checks that always run.

    python3 tools/oxide/gate_scope.py REF [--to COMMIT] [--explain]

prints "full <reason>", or "scoped <summary>" followed by every tools/oxide
module the changes reach, one path per line; integrate.sh runs a check when
its module is on that list. --to compares REF with COMMIT instead of HEAD
(closures still come from the tree checked out), and --explain prints what
each changed file reaches, for a person reading why a check ran.
"""
import argparse
import ast
import functools
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOOLS = "tools/oxide/"

# A change to one of these changes what the gate does, so it runs whole.
GATE_SCRIPTS = {"tools/oxide/integrate.sh", "tools/oxide/merge-branch.sh",
                "tools/oxide/gate_scope.py"}
# Checks with a tool module that run on every landing anyway: the scheduled
# items scan every doc for a dated deferral, and the doc viewer's test renders
# every doc. A change to sync-docs.sh needs nothing more than the mirror
# integrate.sh always runs, so it is not an unknown reader's file either.
ALWAYS = ("tools/oxide/deferred_check.py", "tools/oxide/encounters/test_docview.py")
ALSO_ALWAYS_RUN = {"tools/oxide/sync-docs.sh"}
# Folder names too common to count as a module naming a file inside them,
# and the top folders whose every file a module may list without reading one
# in particular (the doc viewer serves docs/ and .claude/skills/, and its own
# test, which always runs, renders them all).
TOO_COMMON = {"docs", "oxide", "tools"}
TOP_FOLDERS = {"docs", "docs/oxide", "tools", "tools/oxide", ".claude", ".claude/skills", ".claude/rules"}

MODULE_NAME = re.compile(r"tools\.oxide(\.\w+)+")
IDENTIFIER = re.compile(r"[A-Za-z_]\w*")


def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True, check=True).stdout


def tracked():
    return git("ls-files", "-z").split("\0")[:-1]


@functools.lru_cache(maxsize=None)
def tool_modules():
    """Every tracked Python file under tools/oxide, as a repo path."""
    return tuple(sorted(p for p in tracked() if p.startswith(TOOLS) and p.endswith(".py")))


@functools.lru_cache(maxsize=None)
def tool_set():
    return frozenset(tool_modules())


def build_reads():
    """Tool files the build itself reads: any tools/oxide path a meson file
    or the Makefile names, in either of the two spellings meson allows."""
    out = set()
    for path in tracked():
        if os.path.basename(path) not in ("meson.build", "meson.options", "Makefile"):
            continue
        try:
            text = open(os.path.join(ROOT, path), encoding="utf-8").read()
        except OSError:
            continue
        out.update(re.findall(r"tools/oxide/[\w./-]+", text))
        out.update("tools/oxide/" + m for m in re.findall(r"'tools'\s*/\s*'oxide'\s*/\s*'([^']+)'", text))
    return out


def parse(path):
    """(imports, strings, dynamic, joins) of one module: the imports as
    (name, level) pairs, every string constant in its code apart from
    docstrings, whether it imports a module whose name it works out at run
    time, and the parts of each path it joins (os.path.join and the like),
    a constant split at "/" and anything else as None."""
    try:
        tree = ast.parse(open(os.path.join(ROOT, path), encoding="utf-8").read())
    except (OSError, SyntaxError, ValueError):
        return [], [], False, []
    docstrings = {id(n.value) for n in ast.walk(tree)
                  if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant)
                  and isinstance(n.value.value, str)}
    # Messages name docs for a reader to open, not for the tool to read: the
    # text of a print() and of an argparse help, description or epilog.
    for n in ast.walk(tree):
        if not isinstance(n, ast.Call):
            continue
        said = list(n.args) if getattr(n.func, "id", "") == "print" else []
        said += [k.value for k in n.keywords if k.arg in ("help", "description", "epilog")]
        for part in said:
            docstrings.update(id(c) for c in ast.walk(part) if isinstance(c, ast.Constant))
    imports, strings, dynamic, joins = [], [], False, []
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            imports += [(a.name, 0) for a in n.names]
        elif isinstance(n, ast.ImportFrom):
            base = n.module or ""
            imports.append((base, n.level))
            imports += [((base + "." if base else "") + a.name, n.level) for a in n.names]
        elif isinstance(n, ast.Call) and n.args:
            f = n.func
            called = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")
            if called in ("import_module", "__import__"):
                a = n.args[0]
                if isinstance(a, ast.Constant) and isinstance(a.value, str):
                    imports.append((a.value, 0))
                else:
                    dynamic = True
            elif called == "join" and not (isinstance(f, ast.Attribute) and isinstance(f.value, ast.Constant)):
                parts = []
                for a in n.args:
                    if isinstance(a, ast.Constant) and isinstance(a.value, str):
                        parts += [x for x in a.value.split("/") if x]
                    else:
                        parts.append(None)
                joins.append(tuple(parts))
        elif isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in docstrings:
            strings.append(n.value)
    return imports, strings, dynamic, joins


@functools.lru_cache(maxsize=None)
def parsed(path):
    return parse(path)


def module_file(parts):
    """The repo path of a module given as path parts, or None."""
    base = os.path.join(*parts) if parts else ""
    for cand in (base + ".py", os.path.join(base, "__init__.py")):
        if cand.replace(os.sep, "/") in tool_set():
            return cand.replace(os.sep, "/")
    return None


@functools.lru_cache(maxsize=None)
def direct_deps(path):
    """The tool modules one module uses directly."""
    here = os.path.dirname(path)
    imports, strings, dynamic, _joins = parsed(path)
    out = set()
    for name, level in imports:
        parts = name.split(".") if name else []
        if level:
            base = here.split("/")
            if level > 1:
                base = base[:-(level - 1)]
            cands = [base + parts]
        else:
            # As a package path from the repo root, as a sibling (a script's
            # own folder is on sys.path), or from tools/oxide itself.
            cands = [parts, here.split("/") + parts, ["tools", "oxide"] + parts]
        for c in cands:
            f = module_file(c)
            if f:
                out.add(f)
                break
    siblings = {os.path.basename(m)[:-3]: m for m in tool_modules() if os.path.dirname(m) == here}
    for s in strings:
        if MODULE_NAME.fullmatch(s):
            f = module_file(s.split("."))
            if f:
                out.add(f)
        elif s.endswith(".py"):
            # A module loaded or run by path, from its own folder or the root.
            for cand in (os.path.normpath(os.path.join(here, s)), os.path.normpath(s),
                         os.path.normpath(os.path.join("tools", "oxide", s))):
                if cand.replace(os.sep, "/") in tool_set():
                    out.add(cand.replace(os.sep, "/"))
                    break
        elif dynamic and IDENTIFIER.fullmatch(s) and s in siblings:
            # In a module that imports by a name it works out at run time
            # (place_rewards.py loops importlib.import_module over
            # "bulk_scripts" and "bulk_events"), a string that is a sibling
            # module's name is taken for an import of it.
            out.add(siblings[s])
    # Importing a module runs its package's __init__.py first.
    d = here
    while d.startswith("tools/oxide"):
        if d + "/__init__.py" in tool_set():
            out.add(d + "/__init__.py")
        d = os.path.dirname(d)
    out.discard(path)
    return frozenset(out)


@functools.lru_cache(maxsize=None)
def closure(path):
    """The module and every tool module it reaches."""
    seen, todo = {path}, [path]
    while todo:
        for d in direct_deps(todo.pop()):
            if d not in seen:
                seen.add(d)
                todo.append(d)
    return frozenset(seen)


def package_dir(path):
    """The deepest folder holding the file that is a tool package (has a
    Python module of its own), or None outside tools/oxide."""
    if not path.startswith(TOOLS):
        return None
    dirs = {os.path.dirname(m) for m in tool_modules()}
    d = os.path.dirname(path)
    while d and d not in dirs:
        d = os.path.dirname(d)
    return d or None


def folder_names(path):
    """The names of the folders a file sits in that count as naming it: below
    its tool package under tools/oxide, or below docs/ (or .claude/)."""
    d = os.path.dirname(path)
    if path.startswith(TOOLS):
        top = package_dir(path) or "tools/oxide"
    elif path.startswith("docs/"):
        top = "docs/oxide" if path.startswith("docs/oxide/") else "docs"
    elif path.startswith(".claude/"):
        top = ".claude"
    else:
        return set()
    rel = os.path.relpath(d, top) if d != top else "."
    return {p for p in rel.split("/") if p not in (".", "") and p not in TOO_COMMON}


def joins_into(joins, chain, i):
    """True when a joined path runs into folder chain[i] through its parent
    and stops there or goes on with a name worked out at run time:
    os.path.join(ROOT, "docs", "oxide", "learnset-sheets") lists or picks
    from learnset-sheets, while a join that goes on to a constant name
    ("values.json") reads that one file, which its name already covers."""
    want = tuple(chain[i - 1:i + 1])
    for j in joins:
        for k in range(len(j) - 1):
            if j[k:k + 2] == want and (k + 2 == len(j) or j[k + 2] is None):
                return True
    return False


def names(module, path):
    """True when a module's code names the file: a string that is its name or
    ends in "/" and its name, a path the file lies under, or a folder it sits
    in. A bare folder name counts from a module in the same tool package; from
    anywhere else only a path joined into that folder counts, since words
    such as "encounters" or "rules" are also JSON keys and res/ folders."""
    _imports, strings, _dynamic, joins = parsed(module)
    base = os.path.basename(path)
    folders = folder_names(path)
    chain = path.split("/")[:-1]
    same_package = path.startswith(TOOLS) and os.path.dirname(module) == package_dir(path)
    for s in strings:
        t = s.strip().rstrip("/")
        if t.startswith("./"):
            t = t[2:]
        if t == base or t.endswith("/" + base):
            return True
        if "/" in t and t not in TOP_FOLDERS and path.startswith(t + "/"):
            return True
        if same_package and t in folders:
            return True
    return any(chain[i] in folders and joins_into(joins, chain, i) for i in range(1, len(chain)))


def readers(path):
    """The tool modules whose code names a file."""
    return {m for m in tool_modules() if names(m, path)}


def classify(path, deleted):
    """('full', why), ('prose', why) or ('reads', set of modules reached)."""
    if path in GATE_SCRIPTS:
        return "full", f"{path} is one of the gate's own scripts"
    if path in ALSO_ALWAYS_RUN:
        return "prose", "the docs mirror runs on every landing"
    top_md = "/" not in path and path.endswith(".md")
    if not (path.startswith(("docs/", ".claude/", TOOLS)) or top_md):
        return "full", f"{path} changed (game data, the engine or the build)"
    if path.startswith(TOOLS) and path in deleted:
        return "full", f"{path} was deleted"
    if path in build_reads():
        return "full", f"the build reads {path}"
    if path.endswith(".py") and path in tool_set():
        return "reads", {path}
    found = readers(path)
    if found:
        return "reads", found
    if path.endswith(".md") or path.startswith(".claude/") or top_md:
        return "prose", "no module names it"
    return "full", f"{path} is data no tool names, so its reader is unknown"


def scope(ref, to):
    changed = [p for p in git("diff", "--name-only", "--no-renames", "-z", ref, to).split("\0") if p]
    deleted = set(p for p in git("diff", "--name-only", "--no-renames", "--diff-filter=D", "-z",
                                 ref, to).split("\0") if p)
    verdicts = {p: classify(p, deleted) for p in changed}
    return changed, verdicts


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("ref", help="the commit the landing starts from (merge-branch.sh passes origin/oxide)")
    ap.add_argument("--to", default="HEAD", help="the commit to compare with REF (default HEAD)")
    ap.add_argument("--explain", action="store_true", help="say what each changed file reaches")
    args = ap.parse_args(argv)
    try:
        changed, verdicts = scope(args.ref, args.to)
    except subprocess.CalledProcessError as e:
        print(f"gate_scope: git failed: {e.stderr.strip()}", file=sys.stderr)
        return 2
    if args.explain:
        for p in changed:
            kind, what = verdicts[p]
            if kind == "reads":
                print(f"{p}: read by {', '.join(sorted(what))}", file=sys.stderr)
            else:
                print(f"{p}: {kind}, {what}", file=sys.stderr)
    full = [what for kind, what in verdicts.values() if kind == "full"]
    if full:
        more = f" (and {len(full) - 1} more)" if len(full) > 1 else ""
        print(f"full {full[0]}{more}")
        return 0
    reached = set()
    for kind, what in verdicts.values():
        if kind == "reads":
            reached |= what
    # A module is needed when anything it reaches changed; the two checks
    # that always run are needed whatever changed.
    needed = sorted({m for m in tool_modules() if closure(m) & reached} | set(ALWAYS))
    print(f"scoped {len(changed)} files changed since {args.ref}")
    for m in needed:
        print(m)
    return 0


if __name__ == "__main__":
    sys.exit(main())
