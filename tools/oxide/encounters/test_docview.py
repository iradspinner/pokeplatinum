"""The doc viewer (docview.py, /doc on the tool's server): Ian's documents
rendered in the tool's style, from the main checkout or from a ref.

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_docview

Read-only and quick: it renders text in memory, reads documents through the
viewer, and asks a throwaway server on a free port for a few pages. It checks
that nothing in the checkout changed afterwards.
"""
import glob
import http.client
import os
import subprocess
import sys
import threading

from . import docview
from . import model
from . import server

SAMPLE = """---
name: sample
description: A skill's front matter
---
# The title

A paragraph with **bold**, *italic*, `code <b>` and a [link](other.md#part),
wrapped over two lines.

## A section

| Left | Right |
|:-----|------:|
| a    | 1     |

```python
x = "<escaped>"
```

1. **First.** One line.
2. A second item

   with a later paragraph indented three spaces.
   - a nested bullet
   - and [`code in a link`](../README.md)
28. A number kept as written.

> A quote.

---

See [the tool](../../tools/oxide/encounters/server.py), [a site](https://example.com)
and [a trap](javascript:alert(1)).
"""


def get(port, path):
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=20)
    conn.request("GET", path)            # sent as written: no dot-segment folding
    resp = conn.getresponse()
    body = resp.read().decode("utf-8")
    conn.close()
    return resp.status, body


def main():
    results = []
    root = model.repo_root()
    before = subprocess.run(["git", "status", "--porcelain"], cwd=root,
                            capture_output=True, text=True).stdout

    # -- the Markdown the documents use ----------------------------------------
    title, body = docview.render(SAMPLE, "docs/oxide/sample.md")
    results.append(("headings get ids, and the first one is the title",
                    title == "The title" and '<h2 id="a-section">A section</h2>' in body, title))
    results.append(("bold, italic and code, with code escaped",
                    "<strong>bold</strong>" in body and "<em>italic</em>" in body
                    and "<code>code &lt;b&gt;</code>" in body, ""))
    results.append(("a table keeps its alignment, and fenced code is escaped",
                    '<th style="text-align:right">Right</th>' in body
                    and 'class="lang-python">x = &quot;&lt;escaped&gt;&quot;' in body, ""))
    results.append(("an ordered list keeps its own numbers, and a later paragraph at three "
                    "spaces stays in its item with its nested list",
                    '<li value="28">' in body and '<li value="2"><p>A second item</p>\n<p>with a later'
                    in body and "<ul><li>a nested bullet</li>" in body, ""))
    results.append(("a quote, a rule and a skill's front matter",
                    "<blockquote><p>A quote.</p></blockquote>" in body and "<hr>" in body
                    and '<table class="front">' in body, ""))

    # -- links -------------------------------------------------------------------
    results.append(("a relative link to a document stays in the viewer, with its anchor",
                    'href="/doc/docs/oxide/other.md#part"' in body, ""))
    results.append(("code inside a link's text renders (it once raised an IndexError)",
                    '<a href="/doc/docs/README.md"><code>code in a link</code></a>' in body, ""))
    results.append(("a code file goes to GitHub on oxide, a site stays, a script link is dropped",
                    'href="https://github.com/iradspinner/pokeplatinum/blob/oxide/tools/oxide/'
                    'encounters/server.py"' in body and 'href="https://example.com"' in body
                    and 'href="#">a trap' in body, ""))
    _, at_ref = docview.render(SAMPLE, "docs/oxide/sample.md", "cloud/some-branch")
    results.append(("at a ref, links keep it, and a code file opens on that branch",
                    'href="/doc/docs/oxide/other.md?ref=cloud/some-branch#part"' in at_ref
                    and "/blob/cloud/some-branch/tools/" in at_ref, ""))

    # -- what is served ------------------------------------------------------------
    def refused(path):
        try:
            docview.clean_path(path)
        except docview.DocError:
            return True
        return False
    results.append(("only docs/ and .claude/skills/ are served; a path that climbs out is refused",
                    refused("docs/../CLAUDE.md") and refused("res/pokemon/bulbasaur/data.json")
                    and refused("../etc/passwd") and refused("docsx/a.md")
                    and docview.clean_path(".claude/skills/doc-links/SKILL.md")
                    == ".claude/skills/doc-links/SKILL.md", ""))

    def bad_ref(ref):
        try:
            docview.resolve_ref(root, ref)
        except docview.DocError:
            return True
        return False
    results.append(("a ref that could be read as an option or a range is refused",
                    bad_ref("--help") and bad_ref("main..oxide") and bad_ref("no-such-ref-xyz"), ""))
    path = "docs/oxide/tracker.md"
    with open(os.path.join(docview.main_checkout(root), path), encoding="utf-8") as f:
        on_disk = f.read()
    shown = subprocess.run(["git", "show", "HEAD:" + path], cwd=root,
                           capture_output=True, text=True).stdout
    results.append(("a plain read is the main checkout's file on disk; a ref reads git's copy",
                    docview.read(root, path) == on_disk
                    and docview.read(root, path, "HEAD") == shown, docview.main_checkout(root)))
    docs = sorted(glob.glob(os.path.join(root, "docs", "**", "*.md"), recursive=True)
                  + glob.glob(os.path.join(root, ".claude", "skills", "**", "*.md"), recursive=True))
    failed = []
    for p in docs:
        with open(p, encoding="utf-8") as f:
            text = f.read()
        try:
            docview.render(text, os.path.relpath(p, root))
        except Exception as exc:
            failed.append(f"{os.path.relpath(p, root)}: {exc!r}")
    results.append(("every document under docs/ and .claude/skills/ renders",
                    docs and not failed, f"{len(docs)} documents; " + "; ".join(failed[:3])))

    # -- the server ------------------------------------------------------------------
    httpd = server.Server(("127.0.0.1", 0), server.Handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    try:
        index = get(port, "/doc")
        page = get(port, "/doc/docs/oxide/tracker.md?ref=HEAD")
        climb = get(port, "/doc/docs/../CLAUDE.md")
        missing = get(port, "/doc/docs/oxide/no-such-document.md")
        tool = get(port, "/")
    finally:
        httpd.shutdown()
        httpd.server_close()
    results.append(("/doc lists the documents and a document renders in the tool's theme",
                    index[0] == 200 and "/doc/docs/oxide/tracker.md" in index[1]
                    and page[0] == 200 and 'href="/theme.css"' in page[1]
                    and "data-theme-toggle" in page[1], f"{index[0]} {page[0]}"))
    results.append(("a climb out of docs/ and a missing document are 404 pages, and the tool "
                    "itself still loads", climb[0] == 404 and missing[0] == 404 and tool[0] == 200,
                    f"{climb[0]} {missing[0]} {tool[0]}"))
    after = subprocess.run(["git", "status", "--porcelain"], cwd=root,
                           capture_output=True, text=True).stdout
    results.append(("nothing in the checkout changed", before == after, ""))

    width = max(len(l) for l, _, _ in results)
    failed_n = 0
    for label, ok, note in results:
        failed_n += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed_n}/{len(results)} passed")
    return 1 if failed_n else 0


if __name__ == "__main__":
    sys.exit(main())
