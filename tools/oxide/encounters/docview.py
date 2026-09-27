"""Oxide's documents, rendered in the encounter tool's own style.

    http://localhost:8765/doc                              every document
    http://localhost:8765/doc/docs/oxide/tracker.md        one, as on disk
    http://localhost:8765/doc/docs/oxide/x.md?ref=BRANCH   one, at a branch

Ian reads reports on a second monitor (2026-09-27), and the doc-links skill
gives every document a session points him at a link of this form. A plain link
reads the file in the main checkout as it is on disk, fresh on every request:
that checkout is on `oxide`, while this server may be running in a worktree on
some other branch. `?ref=` reads a branch or commit through `git show`, trying
`origin/<ref>` when there is no local branch of that name, because reports
often sit on branches that have not merged. Links between documents are
rewritten to this route and keep the ref; a link to a code file goes to
GitHub, which can show it.

Only files under docs/ and .claude/skills/ are served, and nothing here writes
a file. The Markdown is the subset the documents use (headings, paragraphs,
lists, tables, fenced code, quotes, rules, links, bold, italic, inline code),
rendered with the standard library, like the rest of the tool.
"""
import html
import os
import posixpath
import re
import subprocess
import urllib.parse

ROOTS = ("docs/", ".claude/skills/")
# A document is Markdown; these other text files under the same roots are
# shown as they are, since reports link their data. Anything else is refused.
PLAIN = (".txt", ".csv", ".tsv", ".json")
GITHUB = "https://github.com/iradspinner/pokeplatinum/blob"


class DocError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


# -- where a document comes from -------------------------------------------


def main_checkout(root):
    """The repository's main working tree: git's shared directory is its
    `.git`, whichever worktree asks."""
    out = subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
                         cwd=root, capture_output=True, text=True)
    common = out.stdout.strip()
    if out.returncode == 0 and os.path.basename(common) == ".git":
        return os.path.dirname(common)
    return root


def clean_path(path):
    """A repository path under ROOTS, or DocError. Normalising first means
    `docs/../x` is judged as `x` and refused."""
    p = posixpath.normpath(path.replace("\\", "/").lstrip("/"))
    if p in (".", "") or p.startswith("..") or not (p + "/").startswith(ROOTS):
        raise DocError(404, f"only documents under {' and '.join(ROOTS)} are served")
    return p


def resolve_ref(root, ref):
    """The commit a ref names, trying origin/<ref> after <ref>."""
    if not re.fullmatch(r"[\w./~^@{}-]+", ref) or ref.startswith("-") or ".." in ref:
        raise DocError(400, f"not a branch or commit name: {ref}")
    for cand in (ref, "origin/" + ref):
        out = subprocess.run(["git", "rev-parse", "--verify", "-q", cand + "^{commit}"],
                             cwd=root, capture_output=True, text=True)
        if out.returncode == 0:
            return out.stdout.strip()
    raise DocError(404, f"no branch or commit named {ref} here; it may need a git fetch")


def read(root, path, ref=None):
    """The text of one file, from the main checkout or from `ref`."""
    if ref:
        sha = resolve_ref(root, ref)
        out = subprocess.run(["git", "show", f"{sha}:{path}"], cwd=root, capture_output=True)
        if out.returncode != 0:
            raise DocError(404, f"{path} is not in {ref}")
        raw = out.stdout
    else:
        try:
            with open(os.path.join(main_checkout(root), path), "rb") as f:
                raw = f.read()
        except (FileNotFoundError, IsADirectoryError, NotADirectoryError):
            raise DocError(404, f"{path} does not exist in the main checkout")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        raise DocError(415, f"{path} is not a text file")


def listing(root, ref=None):
    """Every document under ROOTS, sorted, from the main checkout or `ref`."""
    if ref:
        sha = resolve_ref(root, ref)
        out = subprocess.run(["git", "ls-tree", "-r", "--name-only", sha, "--"]
                             + [r.rstrip("/") for r in ROOTS],
                             cwd=root, capture_output=True, text=True)
        names = out.stdout.split("\n")
    else:
        base = main_checkout(root)
        names = []
        for top in ROOTS:
            for dirpath, dirnames, files in os.walk(os.path.join(base, top)):
                dirnames.sort()
                rel = os.path.relpath(dirpath, base).replace(os.sep, "/")
                names += [f"{rel}/{f}" for f in files]
    return sorted(n for n in names if n.endswith(".md"))


# -- Markdown ----------------------------------------------------------------

_FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})\s*([\w+-]*)")
_HEADING = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)(?:\s+#+)?\s*$")
_RULE = re.compile(r"^\s{0,3}([-*_])(?:\s*\1){2,}\s*$")
_BULLET = re.compile(r"^(\s*)([-*+])\s+(.*)$")
_ORDERED = re.compile(r"^(\s*)(\d{1,9})[.)]\s+(.*)$")
_QUOTE = re.compile(r"^\s{0,3}>\s?(.*)$")
_DELIM = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")


def _indent(line):
    return len(line) - len(line.lstrip(" "))


def _is_table(lines, i):
    return ("|" in lines[i] and i + 1 < len(lines) and "-" in lines[i + 1]
            and bool(_DELIM.match(lines[i + 1])))


def _starts_block(lines, i):
    """Whether line i opens a block that ends a paragraph. An ordered list
    interrupts one only when it starts at 1, as in CommonMark, so a wrapped
    line that begins with a number stays text."""
    line = lines[i]
    m = _ORDERED.match(line)
    return bool(_FENCE.match(line) or _HEADING.match(line) or _RULE.match(line)
                or _QUOTE.match(line) or _BULLET.match(line)
                or (m and m.group(2) == "1") or _is_table(lines, i))


def _cells(row):
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|") and not row.endswith("\\|"):
        row = row[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", row)]


class Renderer:
    """One document's HTML. `path` and `ref` place its relative links."""

    def __init__(self, path, ref=None):
        self.path, self.ref = path, ref
        self.slugs = {}
        self.title = None

    # inline ------------------------------------------------------------

    def href(self, url):
        """Where a link in this document goes, from the viewer."""
        if re.match(r"^(https?|mailto):", url, re.I):
            return url
        if re.match(r"^[a-z][a-z0-9+.-]*:", url, re.I):
            return "#"                       # javascript: and the like
        if url.startswith("#"):
            return url
        target, _, frag = url.partition("#")
        target = urllib.parse.unquote(target)
        if target.startswith("/"):
            full = posixpath.normpath(target.lstrip("/"))
        else:
            full = posixpath.normpath(posixpath.join(posixpath.dirname(self.path), target))
        frag = "#" + frag if frag else ""
        if full.startswith(".."):
            return "#"
        if (full + "/").startswith(ROOTS):
            return doc_url(full, self.ref) + frag
        branch = (self.ref or "oxide").replace("origin/", "", 1)
        return f"{GITHUB}/{urllib.parse.quote(branch)}/{urllib.parse.quote(full)}{frag}"

    def inline(self, text, stash=None):
        # Finished pieces wait in `stash` behind placeholders until the end.
        # A link's text is rendered by a nested call that shares the stash,
        # since it may already hold a placeholder of this call's (a code span
        # inside the brackets); only the outermost call puts them back.
        top = stash is None
        stash = [] if top else stash

        def keep(s):
            stash.append(s)
            return f"\x00{len(stash) - 1}\x00"

        def anchor(url, label):
            return keep(f'<a href="{html.escape(self.href(url))}">{label}</a>')

        # Code first, so nothing inside it is read as markup; then links, so a
        # URL's underscores are not read as emphasis.
        text = re.sub(r"(`+)(.+?)\1", lambda m: keep(
            "<code>" + html.escape(m.group(2).strip()) + "</code>"), text)
        text = re.sub(r"<(https?://[^>\s]+)>",
                      lambda m: anchor(m.group(1), html.escape(m.group(1))), text)
        text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)",
                      lambda m: anchor(m.group(2), self.inline(m.group(1), stash)), text)
        text = re.sub(r"(?<![\w/\"=\x00])(https?://[^\s<>()]*[^\s<>().,;:!?'\"])",
                      lambda m: anchor(m.group(1), html.escape(m.group(1))), text)
        text = html.escape(text, quote=False)
        text = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"(?<!\w)__(?=\S)(.+?)(?<=\S)__(?!\w)", r"<strong>\1</strong>", text)
        text = re.sub(r"(?<![\w*])\*(?=[^\s*])(.+?)(?<=[^\s*])\*(?![\w*])", r"<em>\1</em>", text)
        text = re.sub(r"(?<![\w])_(?=\S)(.+?)(?<=\S)_(?!\w)", r"<em>\1</em>", text)
        # A piece can hold placeholders of its own (a link's text), so this
        # repeats; the bound only guards against a stray NUL in a file.
        for _ in range(8):
            if not top or "\x00" not in text:
                break
            text = re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], text)
        return text

    def slug(self, text):
        plain = re.sub(r"<[^>]+>", "", text)
        base = re.sub(r"[^\w\- ]", "", html.unescape(plain).lower()).strip().replace(" ", "-")
        n = self.slugs.get(base, 0)
        self.slugs[base] = n + 1
        return base if n == 0 else f"{base}-{n}"

    # blocks ------------------------------------------------------------

    def blocks(self, lines):
        out, i, n = [], 0, len(lines)
        while i < n:
            line = lines[i]
            if not line.strip():
                i += 1
                continue
            m = _FENCE.match(line)
            if m:
                indent, fence, lang = len(m.group(1)), m.group(2), m.group(3)
                body, i = [], i + 1
                while i < n and not (lines[i].strip().startswith(fence)
                                     and set(lines[i].strip()) == {fence[0]}):
                    body.append(lines[i][min(indent, _indent(lines[i])):])
                    i += 1
                i += 1
                cls = f' class="lang-{html.escape(lang)}"' if lang else ""
                out.append(f"<pre><code{cls}>{html.escape(chr(10).join(body))}</code></pre>")
                continue
            m = _HEADING.match(line)
            if m:
                level, inner = len(m.group(1)), self.inline(m.group(2))
                if level == 1 and self.title is None:
                    self.title = html.unescape(re.sub(r"<[^>]+>", "", inner))
                out.append(f'<h{level} id="{self.slug(inner)}">{inner}</h{level}>')
                i += 1
                continue
            if _RULE.match(line):
                out.append("<hr>")
                i += 1
                continue
            if _is_table(lines, i):
                i = self.table(lines, i, out)
                continue
            if _QUOTE.match(line):
                body = []
                while i < n and lines[i].strip():
                    q = _QUOTE.match(lines[i])
                    body.append(q.group(1) if q else lines[i].strip())
                    i += 1
                out.append("<blockquote>" + self.blocks(body) + "</blockquote>")
                continue
            if _BULLET.match(line) or _ORDERED.match(line):
                i = self.list(lines, i, out)
                continue
            para = [line.strip()]
            i += 1
            while i < n and lines[i].strip() and not _starts_block(lines, i):
                para.append(lines[i].strip())
                i += 1
            out.append("<p>" + self.inline(" ".join(para)) + "</p>")
        return "\n".join(out)

    def table(self, lines, i, out):
        head = _cells(lines[i])
        aligns = []
        for c in _cells(lines[i + 1]):
            left, right = c.startswith(":"), c.endswith(":")
            aligns.append("center" if left and right else "right" if right else "left")
        rows, i = [], i + 2
        while i < len(lines) and lines[i].strip() and "|" in lines[i]:
            rows.append(_cells(lines[i]))
            i += 1

        def cell(tag, text, k):
            align = aligns[k] if k < len(aligns) else "left"
            style = f' style="text-align:{align}"' if align != "left" else ""
            return f"<{tag}{style}>{self.inline(text)}</{tag}>"
        parts = ["<table><thead><tr>"
                 + "".join(cell("th", c, k) for k, c in enumerate(head)) + "</tr></thead><tbody>"]
        for r in rows:
            r = (r + [""] * len(head))[:len(head)]
            parts.append("<tr>" + "".join(cell("td", c, k) for k, c in enumerate(r)) + "</tr>")
        out.append("<div class=\"wide\">" + "".join(parts) + "</tbody></table></div>")
        return i

    def list(self, lines, i, out):
        """One list. An item runs on while its lines are indented past its
        marker, which is looser than CommonMark on purpose: the docs indent
        an item's later paragraphs three spaces even after "10.", where
        CommonMark would want four and end the list."""
        n = len(lines)
        first = _BULLET.match(lines[i])
        ordered = first is None
        pattern = _ORDERED if ordered else _BULLET
        base = _indent(lines[i])
        items, loose = [], False
        while i < n:
            m = pattern.match(lines[i])
            if not m or _indent(lines[i]) != base or (not ordered and _RULE.match(lines[i])):
                break
            content = m.start(3)
            body, i = [m.group(3)], i + 1
            while i < n:
                line = lines[i]
                if not line.strip():
                    j = i
                    while j < n and not lines[j].strip():
                        j += 1
                    if j < n and _indent(lines[j]) > base:
                        body += [""] * (j - i)
                        i = j
                        continue
                    break
                ind = _indent(line)
                if ind > base:
                    body.append(line[min(content, ind):])
                elif pattern.match(line) or _starts_block(lines, i):
                    break
                else:
                    body.append(line.strip())      # a lazy continuation line
                i += 1
            if any(not b.strip() for b in body):
                loose = True
            items.append((m.group(2) if ordered else None, body))
            j = i
            while j < n and not lines[j].strip():
                j += 1
            if j > i and j < n:
                nxt = pattern.match(lines[j])
                if nxt and _indent(lines[j]) == base:
                    loose, i = True, j
                    continue
            if j > i:
                break
        tag = "ol" if ordered else "ul"
        parts = [f"<{tag}>"]
        for value, body in items:
            inner = self.blocks(body)
            if not loose and inner.startswith("<p>"):
                end = inner.index("</p>")
                inner = inner[3:end] + inner[end + 4:]
            attr = f' value="{value}"' if value else ""
            parts.append(f"<li{attr}>{inner}</li>")
        parts.append(f"</{tag}>")
        out.append("".join(parts))
        return i

    def render(self, text):
        lines = text.replace("\r\n", "\n").expandtabs(4).split("\n")
        front = ""
        # A skill opens with YAML front matter: name and description.
        if lines and lines[0].strip() == "---" and "---" in [l.strip() for l in lines[1:]]:
            end = [l.strip() for l in lines[1:]].index("---") + 1
            pairs = [l.split(":", 1) for l in lines[1:end] if ":" in l]
            front = ("<table class=\"front\"><tbody>" + "".join(
                f"<tr><th>{html.escape(k.strip())}</th><td>{self.inline(v.strip())}</td></tr>"
                for k, v in pairs) + "</tbody></table>")
            lines = lines[end + 1:]
        return front + self.blocks(lines)


def render(text, path, ref=None):
    """(title, body HTML) for one Markdown document."""
    r = Renderer(path, ref)
    body = r.render(text)
    return r.title or posixpath.basename(path), body


# -- pages -------------------------------------------------------------------


def doc_url(path, ref=None):
    q = "?ref=" + urllib.parse.quote(ref, safe="/") if ref else ""
    return "/doc/" + urllib.parse.quote(path) + q


# Layout and type only: every colour and face is a token from theme.css, as in
# the tool's own page, so the two themes follow the same switch.
CSS = """
* { box-sizing: border-box; }
body { margin: 0; background: var(--ground); color: var(--ink); font: 17px/1.6 var(--sans); }
a { color: var(--ink); text-decoration-color: var(--faint); }
a:hover { color: var(--place-ink); text-decoration-color: currentColor; }
:focus-visible { outline: 2px solid var(--mass); outline-offset: 1px; }
header { display: flex; align-items: center; gap: 16px; min-height: 44px; padding: 4px 16px;
         background: var(--panel); border-bottom: 1px solid var(--rule);
         position: sticky; top: 0; }
header .title { font: 600 18.5px/1 var(--pixel); white-space: nowrap; text-decoration: none; }
header .title .ox { color: var(--place-ink); }
header .where { font: 14.5px/1.3 var(--mono); color: var(--faint); flex: 1; min-width: 0;
                overflow-wrap: anywhere; }
header .where b { color: var(--place-ink); font-weight: 500; }
button, input { font: inherit; color: var(--ink); background: var(--panel);
                border: 1px solid var(--rule); border-radius: 3px; padding: 3px 6px; }
button { cursor: pointer; }
button:hover { border-color: var(--mass); }
main { max-width: 980px; margin: 0 auto; padding: 20px 24px 80px; }
h1, h2, h3, h4, h5, h6 { line-height: 1.25; margin: 1.5em 0 .5em; }
h1 { font-size: 30px; margin-top: .4em; }
h2 { font-size: 24px; padding-bottom: 4px; border-bottom: 1px solid var(--rule); }
h3 { font-size: 20px; }
h4, h5, h6 { font-size: 17px; }
p, ul, ol, blockquote, pre, .wide, table.front { margin: 0 0 14px; }
li { margin: 3px 0; }
li > ul, li > ol { margin: 4px 0; }
ul, ol { padding-left: 28px; }
code { font: 14.5px/1.4 var(--mono); background: var(--sunken); border-radius: 3px;
       padding: 1px 4px; overflow-wrap: anywhere; }
pre { background: var(--panel); border: 1px solid var(--rule); border-radius: 3px;
      padding: 10px 14px; overflow-x: auto; }
pre code { background: none; padding: 0; overflow-wrap: normal; }
blockquote { border-left: 3px solid var(--rule); padding: 2px 0 2px 14px; color: var(--dim); }
hr { border: 0; border-top: 1px solid var(--rule); margin: 22px 0; }
.wide { overflow-x: auto; }
table { border-collapse: collapse; }
th { text-align: left; font-weight: 600; font-size: 15px; color: var(--dim); }
th, td { padding: 4px 10px; border-bottom: 1px solid var(--rule); vertical-align: top; }
table.front { background: var(--panel); border: 1px solid var(--rule); font-size: 15px; }
.plain { white-space: pre-wrap; }
.index h2 { font: 14.5px/1.3 var(--mono); color: var(--dim); border: 0; margin: 20px 0 4px; }
.index ul { list-style: none; padding-left: 0; columns: 2 320px; }
.index li { break-inside: avoid; }
.error { color: var(--error); }
"""


def page(title, body, where):
    """A whole page: the tool's header with its theme switch, then `body`."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="color-scheme" content="light dark">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="/theme.css">
<script src="/theme.js"></script>
<style>{CSS}</style>
</head>
<body>
<header>
  <a class="title" href="/doc">Platinum <span class="ox">Oxide</span></a>
  <span class="where">{where}</span>
  <button data-theme-toggle>Dark</button>
</header>
<main>
{body}
</main>
</body>
</html>
"""


def _where(path, ref):
    at = f"<b>{html.escape(ref)}</b>" if ref else "main checkout"
    return (html.escape(path) + " at " if path else "") + at


def document_page(root, path, ref=None):
    """The page for one document, or DocError. A folder (a trailing slash, or
    a last part with no extension) is an index of the documents under it."""
    folder = path.endswith("/")
    path = clean_path(path)
    if folder or "." not in posixpath.basename(path):
        return index_page(root, ref, path + "/")
    text = read(root, path, ref)
    if path.endswith(".md"):
        title, body = render(text, path, ref)
    elif path.endswith(PLAIN):
        title, body = posixpath.basename(path), f'<pre class="plain">{html.escape(text)}</pre>'
    else:
        raise DocError(415, f"{path} is not a document the viewer shows")
    return page(title, body, _where(path, ref))


def index_page(root, ref=None, prefix=""):
    """Every document under ROOTS (or under `prefix`), grouped by folder."""
    names = [n for n in listing(root, ref) if n.startswith(prefix)]
    groups = {}
    for name in names:
        groups.setdefault(posixpath.dirname(name), []).append(name)
    parts = ['<div class="index"><h1>Documents</h1>',
             '<form action="/doc" method="get"><input name="ref" size="32" '
             f'placeholder="branch or commit" value="{html.escape(ref or "")}"> '
             '<button>Show</button></form>']
    for folder in sorted(groups):
        parts.append(f"<h2>{html.escape(folder)}/</h2><ul>")
        parts += [f'<li><a href="{html.escape(doc_url(n, ref))}">{html.escape(posixpath.basename(n))}</a></li>'
                  for n in groups[folder]]
        parts.append("</ul>")
    if not names:
        parts.append("<p>No documents here.</p>")
    parts.append("</div>")
    return page("Documents", "".join(parts), _where(prefix, ref))


def error_page(err):
    return page("Not shown", f'<p class="error">{html.escape(str(err))}</p>'
                '<p><a href="/doc">Every document</a></p>', "")
