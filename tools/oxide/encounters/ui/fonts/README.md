# Vendored: the tool's three faces

The layout redesign (Ian, 2026-09-29) took the mockups' three faces, shipped
here so the tool loads nothing from the network. Each is the latin subset
from its @fontsource 5.3.0 package, taken with `npm pack` on 2026-09-29, and
each is under the SIL Open Font License 1.1, whose text is kept beside it.

| File | From | Bytes |
|---|---|---|
| `AtkinsonHyperlegible-400-latin.woff2` | `@fontsource/atkinson-hyperlegible`, `files/atkinson-hyperlegible-latin-400-normal.woff2` | 17,208 |
| `AtkinsonHyperlegible-700-latin.woff2` | the same package, `latin-700-normal` | 17,524 |
| `AtkinsonHyperlegible-400-italic-latin.woff2` | the same package, `latin-400-italic` | 18,292 |
| `AtkinsonHyperlegible-700-italic-latin.woff2` | the same package, `latin-700-italic` | 18,484 |
| `JetBrainsMono-400-latin.woff2` | `@fontsource/jetbrains-mono`, `files/jetbrains-mono-latin-400-normal.woff2` | 21,168 |
| `JetBrainsMono-600-latin.woff2` | the same package, `latin-600-normal` | 21,860 |
| `Silkscreen-400-latin.woff2` | `@fontsource/silkscreen`, `files/silkscreen-latin-400-normal.woff2` | 8,404 |

The licences: `OFL-AtkinsonHyperlegible.txt` (Copyright 2020 Braille
Institute of America, Inc.), `OFL-JetBrainsMono.txt` (Copyright 2020 The
JetBrains Mono Project Authors) and `OFL-Silkscreen.txt` (Copyright 2001 The
Silkscreen Project Authors), each the package's own LICENSE file.

Atkinson Hyperlegible is the sans for everything read, JetBrains Mono the
tabular mono for everything compared, and Silkscreen the pixel face, which
the visual design limits to identity: the title, the view and time-of-day
tabs, the uplift headline and the dex number. The latin subset covers the
digits, `%`, `×`, `½`, `¼`, `·` and A to Z. `theme.css` declares them with
`font-display: block`, because the files are local and small and a swap
would make the page jump.

Pixelify Sans, the pixel face from 2026-09-22 until the redesign, is gone,
with its licence.
