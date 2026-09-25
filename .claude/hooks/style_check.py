#!/usr/bin/env python3
"""PreToolUse style check for Ian's writing rules (~/.claude/CLAUDE.md).

Runs before a Write or Edit to a Markdown file, and before a Bash `git commit`,
and refuses the call (exit 2, reason on stderr) when the new text adds an em
dash, an en dash used as punctuation, or one of the phrases the rules ban as
machine-written. Only what the call adds is judged: an Edit that leaves an old
dash in place passes, one that adds a new dash does not. Text inside code
spans and fenced code blocks is ignored, so quoting a command or an error
message is fine.

The words the rules can only ban in a figurative sense (landscape, navigate,
journey, and unpack, which a ROM project uses literally) are not checked,
because a script cannot tell the senses apart.
"""
import json
import os
import re
import shlex
import sys

EM, EN = "—", "–"

# Each entry: a regex, and the rule it stands for, for the refusal message.
PHRASES = [
    (r"\bit'?s worth noting\b", "filler"),
    (r"\bit is (important|worth) (to note|noting)\b", "filler"),
    (r"\bnotably\b", "filler"),
    (r"\bessentially\b", "filler"),
    (r"\bcrucially\b", "filler"),
    (r"\bat the end of the day\b", "filler"),
    (r"\bin today'?s\b", "filler"),
    (r"\bdelv(e|es|ed|ing)\b", "banned word"),
    (r"\brobust(ly|ness)?\b", "banned word"),
    (r"\bseamless(ly)?\b", "banned word"),
    (r"\bleverag(e|es|ed|ing)\b", "banned word"),
    (r"\bstreamlin(e|es|ed|ing)\b", "banned word"),
    (r"\belevat(e|es|ed|ing)\b", "banned word"),
    (r"\btapestry\b", "banned word"),
    (r"\bdiv(e|es|ing) into\b", "banned phrase"),
    (r"\bgame[- ]changer\b", "banned word"),
    (r"\bcutting[- ]edge\b", "banned word"),
    (r"\bholistic(ally)?\b", "banned word"),
    (r"\bsynerg(y|ies|istic)\b", "banned word"),
    (r"\bhere'?s the thing\b", "banned phrase"),
    (r"\blet'?s break (this|it) down\b", "banned phrase"),
    (r"\bthe key takeaway\b", "banned phrase"),
    (r"\bhope this helps\b", "sign-off"),
    (r"\blet me know if\b", "sign-off"),
    (r"\bfeel free to\b", "sign-off"),
    (r"\bhappy to help\b", "sign-off"),
    (r"\bgreat question\b", "opening praise"),
    (r"\bgood catch\b", "opening praise"),
    (r"\byou'?re (absolutely )?right to ask\b", "opening praise"),
    (r"\bnot just\b[^.\n]{1,60}\bbut\b", "\"not just X but Y\""),
]

PROSE_EXT = (".md", ".mdx", ".markdown")


def prose(text):
    """Text with fenced code blocks and inline code spans removed."""
    text = re.sub(r"(?ms)^\s*(```|~~~).*?^\s*\1[^\n]*$", "", text)
    return re.sub(r"`[^`\n]*`", "", text)


def en_dashes(text):
    """En dashes used as punctuation, i.e. with a space on either side; an en
    dash between two numbers (a range) is typography, not punctuation."""
    return len(re.findall(r"\s–|–\s", text))


def findings(text):
    """{label: count} for everything the rules forbid in text."""
    t = prose(text)
    out = {}
    if t.count(EM):
        out["em dash"] = t.count(EM)
    if en_dashes(t):
        out["en dash as punctuation"] = en_dashes(t)
    low = t.lower()
    for pat, why in PHRASES:
        hits = re.findall(pat, low)
        if hits:
            m = re.search(pat, low).group(0)
            out['"%s" (%s)' % (m, why)] = len(hits)
    return out


def added(new, old):
    """What new adds over old: labels whose count went up."""
    a, b = findings(new), findings(old)
    return [k for k, n in a.items() if n > b.get(k, 0)]


def commit_message(command, cwd):
    """The message a `git commit` command carries, or None if it is not one."""
    if not re.search(r"\bgit\b(\s+-C\s+\S+)?\s+commit\b", command):
        return None
    parts = []
    # A heredoc body (git commit -F - <<'EOF' ... EOF) is the message.
    for m in re.finditer(r"<<-?\s*['\"]?(\w+)['\"]?\n(.*?)\n\1\b", command, re.S):
        parts.append(m.group(2))
    try:
        ws = shlex.split(command.split("<<")[0])
    except ValueError:
        ws = command.split()
    for i, w in enumerate(ws):
        if w in ("-m", "--message") and i + 1 < len(ws):
            parts.append(ws[i + 1])
        elif w.startswith("--message="):
            parts.append(w.split("=", 1)[1])
        elif w in ("-F", "--file") and i + 1 < len(ws) and ws[i + 1] != "-":
            path = os.path.join(cwd, os.path.expanduser(ws[i + 1]))
            try:
                parts.append(open(path, encoding="utf-8").read())
            except OSError:
                pass
    return "\n".join(parts)


def main():
    # This is the repo's copy of ~/.claude/hooks/style_check.py, registered in
    # .claude/settings.json for cloud sessions, which do not load ~/.claude/.
    # A local session already runs the user-level hook, so this copy steps
    # aside there rather than checking everything twice.
    if os.path.exists(os.path.expanduser("~/.claude/hooks/style_check.py")) \
            and os.path.realpath(__file__) != os.path.realpath(os.path.expanduser("~/.claude/hooks/style_check.py")):
        return 0
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return 0
    tool, inp = data.get("tool_name"), data.get("tool_input") or {}
    cwd = data.get("cwd") or os.getcwd()
    bad, where = [], ""
    if tool in ("Write", "Edit", "MultiEdit"):
        path = inp.get("file_path") or ""
        if not path.lower().endswith(PROSE_EXT):
            return 0
        where = os.path.basename(path)
        if tool == "Write":
            try:
                old = open(path, encoding="utf-8").read()
            except OSError:
                old = ""
            bad = added(inp.get("content") or "", old)
        else:
            edits = inp.get("edits") or [inp]
            for e in edits:
                bad += added(e.get("new_string") or "", e.get("old_string") or "")
    elif tool == "Bash":
        msg = commit_message(inp.get("command") or "", cwd)
        if msg:
            where = "the commit message"
            bad = list(findings(msg))
    if not bad:
        return 0
    print("Refused by Ian's writing rules (~/.claude/CLAUDE.md): %s adds %s. "
          "Rewrite without it: a comma, full stop, colon or parentheses for a "
          "dash, and plain words for a banned phrase. Text in code spans is not "
          "checked." % (where, ", ".join(sorted(set(bad)))), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
