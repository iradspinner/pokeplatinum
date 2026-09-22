# Encounter and Dex tool: visual design

Project: Platinum Oxide. Written 2026-09-22. Status: v1.1, palette decided, ready for the encounter track to implement.

This document covers how the tool looks: color, type, spacing, both themes, and each component. What the tool does is in `encounter-tool-design.md`, and what already exists is in the build plan's M4 and M8 entries. Nothing here changes behavior, an API, or a test's expectations. It is written against the `worktree-encounter-step0` branch as of 2026-09-22, where the Dex view (M8 D1 to D3) lives and has not yet merged into `oxide`.

Palette: B, Lake Guardians (Azelf teal for odds, Mesprit pink for place, Uxie gold for the number to act on), chosen by Ian on 2026-09-22 from the four options in the palette preview (`palette-options.html`, sent in that day's Cowork chat).

## 0. What changes and what stays

The layout, every interaction, and the existing color logic stay. The M4 design pass settled on one hue per meaning and on drawing anything caught as absence, and both rules carry over unchanged. What changes is the palette (teal, pink and gold replacing teal and ochre), a dark theme beside the light one, a pixel display face for the tool's identity, color on type chips and gym splits, and more presence on the Dex species page.

The tool's constraints still hold: no CDN, no npm, no build step, a stdlib server. The one new binary is a single font file of about 8 KB committed to the repo with its licence.

Browser policy: the current Chrome or Edge on Ian's Windows desktop. `light-dark()` (Chrome and Edge 123 and later) is used without a fallback.

## 1. Principles

These decide every case the component list does not cover.

1. Each hue has one meaning. Teal is probability mass: odds, ladder segments, a passing game metric. Pink is place: the selected area, the active tab, the species being viewed, a hidden ability. Gold is the one number worth acting on: the uplift headline and the best rung of the ladder. Red is a lint error and nothing else, and orange-brown is a lint warning.
2. Anything caught is drawn as absence. A caught or duped species is hatched, faded or struck through, and never gets a color of its own.
3. The eighteen type colors appear only on type chips and on gym-split tags, which borrow the leader's type. Kept to those two places, an eighteen-color set cannot compete with the five meanings above.
4. The pixel face is for identity. It sets the title, the view tabs, the uplift headline and the dex number, while anything read or compared stays in the sans or the tabular mono.
5. Each view has one loud element: the repel ladder on Tables, the sprite on Dex.

## 2. Color tokens

All colors live in one new file, `tools/oxide/encounters/ui/theme.css`, as custom properties on `:root`, each written once with `light-dark()`. No hex value appears anywhere else in the page or its scripts.

| Token | Used for | Light | Dark |
|---|---|---|---|
| `--ground` | Page and centre-column background | #EEF4F3 | #0E1819 |
| `--panel` | Side columns, header, menus, inputs | #FAFCFC | #142122 |
| `--sunken` | Hover, tracks, tags, hatching | #E1EBEA | #1D2E30 |
| `--rule` | Borders and dividers | #C9D8D6 | #2A3E40 |
| `--ink` | Body text | #172524 | #E3EEED |
| `--dim` | Secondary text and labels | #536667 | #93AAA9 |
| `--faint` | Caught rows, disabled text, placeholders | #7A9191 | #5A7272 |
| `--mass` | Odds, passing metrics, focus ring | #1B7879 | #4CC3C0 |
| `--on-mass` | Text on a `--mass` fill | #FFFFFF | #0E1819 |
| `--place-bg` | Selected row, active tab fill | #F8D7E3 | #3B2230 |
| `--place-ink` | Selected row bar, active tab text, "Oxide" in the title | #A33E63 | #F6A9C6 |
| `--act` | Uplift headline, best rung, planner percentages | #926C0E | #E6BD55 |
| `--warn` | Lint warnings | #B35E17 | #E89250 |
| `--error` | Lint errors, a failing game metric | #A02433 | #F06B78 |
| `--seg-1` to `--seg-5` | Ladder segments, in order | teal, pink, teal, pink, teal | same pattern |
| `--stat-0` to `--stat-4` | Stat bands, low to high | pink-red to teal | same |

The ladder alternates teal and pink so that neighbouring species separate at a glance without either hue meaning anything new. The stat bands run warm to cool, which the type-matchup grid in section 7 reuses: warm is bad for the species, cool is good for it.

The light values are slightly darker than the ones in `palette-options.html`. The preview's light-mode secondary text, faint text, pink ink and gold missed WCAG AA by a few tenths, and were darkened in small steps until every pairing in section 10 passed.

```css
:root {
  color-scheme: light dark;
  --ground: light-dark(#EEF4F3, #0E1819);
  --panel: light-dark(#FAFCFC, #142122);
  --sunken: light-dark(#E1EBEA, #1D2E30);
  --rule: light-dark(#C9D8D6, #2A3E40);
  --ink: light-dark(#172524, #E3EEED);
  --dim: light-dark(#536667, #93AAA9);
  --faint: light-dark(#7A9191, #5A7272);
  --mass: light-dark(#1B7879, #4CC3C0);
  --place-bg: light-dark(#F8D7E3, #3B2230);
  --place-ink: light-dark(#A33E63, #F6A9C6);
  --act: light-dark(#926C0E, #E6BD55);
  --warn: light-dark(#B35E17, #E89250);
  --error: light-dark(#A02433, #F06B78);
  --on-mass: light-dark(#FFFFFF, #0E1819);
  --seg-1: light-dark(#1C7C7D, #4CC3C0);
  --seg-2: light-dark(#E48AAE, #F29CBE);
  --seg-3: light-dark(#5AB0AE, #2A9290);
  --seg-4: light-dark(#F2B8CE, #F7C3D6);
  --seg-5: light-dark(#12605F, #7ED8D5);
  --stat-0: light-dark(#D0708F, #E07A9A);
  --stat-1: light-dark(#D9A35B, #E6AA62);
  --stat-2: light-dark(#C9B85A, #D7C765);
  --stat-3: light-dark(#5AB0AE, #7ED8D5);
  --stat-4: light-dark(#1C7C7D, #4CC3C0);
  accent-color: var(--mass);              /* native checkboxes and radios */
  scrollbar-color: var(--faint) var(--panel);
}
```

### Type colors

These are the usual community values. Chips blend them into the panel rather than using them at full strength, so the ink text stays readable on all eighteen: the lowest contrast is 10.5 to 1 in light mode (Fighting) and 5.7 to 1 in dark (Electric).

| Type | Hex | Type | Hex | Type | Hex |
|---|---|---|---|---|---|
| Normal | #A8A77A | Fighting | #C22E28 | Bug | #A6B91A |
| Fire | #EE8130 | Poison | #A33EA1 | Rock | #B6A136 |
| Water | #6390F0 | Ground | #E2BF65 | Ghost | #735797 |
| Electric | #F7D02C | Flying | #A98FF3 | Dragon | #6F35FC |
| Grass | #7AC74C | Psychic | #F95587 | Dark | #705746 |
| Ice | #96D9D6 | Steel | #B7B7CE | Fairy | #D685AD |

The chip rule. `light-dark()` accepts only colors, so the blend strength cannot be a token of its own; the rule wraps two `color-mix()` calls instead:

```css
.chip {
  --t: var(--type-normal);                /* set per chip, e.g. style="--t: var(--type-fire)" */
  background: light-dark(color-mix(in srgb, var(--t) 24%, var(--panel)),
                         color-mix(in srgb, var(--t) 34%, var(--panel)));
  border: 1px solid color-mix(in srgb, var(--t) 60%, var(--panel));
  color: var(--ink);
  border-radius: 999px; padding: 0 7px; font-size: 11.5px; font-weight: 600;
}
```

Declare the eighteen as `--type-<name>` in `theme.css`. They are the same in both themes.

### Gym splits

Split tags take the leader's type through the chip rule, so the area list reads as the game's progression at a glance.

| Split | Type | Split | Type |
|---|---|---|---|
| Roark | Rock | Byron | Steel |
| Gardenia | Grass | Candice | Ice |
| Maylene | Fighting | Volkner | Electric |
| Wake | Water | League | Dragon (Cynthia's Garchomp) |
| Fantina | Ghost | Post | plain tag, no type |

## 3. Light, dark and the toggle

The page follows Windows by default and offers a toggle for the moments it should not.

1. `index.html` gets `<meta name="color-scheme" content="light dark">` in its head, before any stylesheet.
2. `theme.css` sets `color-scheme: light dark` on `:root` and never pins it there. With JavaScript off, the page still follows the system.
3. A small `ui/theme.js`, loaded as an ordinary blocking script in the head (not a module, not `defer`), reads `localStorage["oxide-color-scheme"]` and, if it holds `light` or `dark`, writes that into the meta tag before first paint. Wrap every storage read and write in try/catch; an empty or throwing store means "follow the system".
4. The toggle is one button at the right end of the header with two states, following current guidance: "System" and the opposite of whatever the system currently is. Pressing it pins that exact scheme, so if Windows later switches to match, the page stays where Ian put it. The button's label names what pressing it will do ("Dark", "Light", or "System"), and it updates from a `matchMedia("(prefers-color-scheme: dark)")` change listener.
5. The theme preference is per browser and belongs in `localStorage`. It is the one piece of state that should not go through the server the way the caught list does.

## 4. Typography

| Role | Face | Size | Weight |
|---|---|---|---|
| Title "Platinum Oxide" | Pixelify Sans | 16px | 600 |
| View tabs, time-of-day tabs | Pixelify Sans | 13px | 600 |
| Uplift headline | Pixelify Sans | 28px | 600 |
| Dex number | Pixelify Sans | 16px | 600 |
| Area or species name | sans | 18px (22px on the species page) | 650 |
| Centre column body | sans | 15.5px | 400 |
| Base body | sans | 13.5px | 400 |
| Section labels, captions | sans | 12.5px | 600 labels, 400 captions |
| Meta and tags | sans | 11.5px | 400 |
| Every aligned number | mono, tabular figures | size of its context | 400 or 600 |

The 15.5px centre column is Ian's M4 request and stays.

Changed 2026-09-22 at Ian's request: every size in this table is 2.5px larger in
the build (base 16px, centre 18px, title 18.5px), the left column is 460px, and
the slot table's party icons are 64px in 68px rows. "What a player meets" sits
beside the slot table without a heading, and the slot table no longer has a real
odds column. The build plan's entry for that date has the details.

Stacks: sans is `system-ui, "Segoe UI Variable", "Segoe UI", sans-serif`; mono is `ui-monospace, "Cascadia Mono", Consolas, monospace` with `font-variant-numeric: tabular-nums`.

### The pixel face

Pixelify Sans, SIL Open Font License 1.1, weight 600, latin subset, from the fontsource 5.3.0 package. Commit it as `ui/fonts/PixelifySans-600-latin.woff2` with the licence beside it as `ui/fonts/OFL.txt`, and add a line to the track's vendoring notes saying where it came from. Declare it with `font-display: block`: the file is local and tiny, and a swap would make the title jump. Python's `mimetypes` already maps `.woff2` to `font/woff2`, so `server.py` needs no change.

The latin subset covers digits, `%`, `×` and A to Z, which is everything the pixel roles print. A species name with a symbol (Nidoran♀) never appears in the pixel face; if one ever does, the browser falls back per glyph, which is acceptable. Pixel faces smear at some sizes: check the four pixel sizes above at Ian's Windows display scaling and move any that look soft by one pixel.

## 5. Layout and spacing

Keep the grid exactly as it is: a 44px header, then three columns of 420px, `minmax(520px, 1fr)` and 400px, on both views. The side columns are `--panel` and the centre is `--ground`, so the centre reads as the work surface inside a frame.

Spacing uses 4, 8, 12, 16 and 24px and nothing between. Radii are 3px for controls and tags, 999px for chips, and 6px for the dex sprite stage. Borders are 1px `--rule` everywhere.

| Element | Height |
|---|---|
| Header | 44px |
| Area list row | 44px (two lines) |
| Slot table row | 36px (fits a 32px party icon) |
| Dex list row | 36px |
| Ladder bar | 22px |
| Stat bar | 9px |

The header runs left to right: title, view tabs, the game-metric strip (wraps if it must), a flexible gap, the checkout name in faint mono, the theme toggle.

## 6. Tables view

### Header metrics

Label in `--dim`, value in mono 600. A passing value is `--mass`; a failing one is `--error`, and its words ("2 to fix") already say so, so color is never the only signal. Each metric's tooltip names its threshold.

### Area list

Hover is `--sunken`. The selected row gets `--place-bg` with a 3px inset bar of `--place-ink` on its left edge. The lint dot stays 6px, in `--error` or `--warn`. The four-step progress fade stays. The split moves out of the "· Roark" suffix into a split tag. When an area has a recorded catch, its 32px party icon leads the encounter column; the M8 note held icons back from this list because most rows would be blank, and drawing one only where a catch exists answers that.

### Buttons and tabs

Resting buttons are `--panel` with a `--rule` border. Every "on" state (sort bar, Grass/Surf/rod tabs, Morning/Day/Night, the view tabs) becomes `--place-bg` fill with `--place-ink` text and border. Today these fill with teal; under the new rules teal is reserved for mass, and "which one am I on" is place.

### Slot table

36px rows, 32px icons with `image-rendering: pixelated`, no zebra striping, `--sunken` on hover. A caught row turns `--faint`, strikes the name, and drops the icon to 35% opacity. Rate is `--dim` mono; real odds are `--ink` mono. Level inputs are mono.

### Inputs and combobox

`--panel` background, `--rule` border, 3px radius. Focus is a 2px `--mass` outline offset by 1px. The combobox menu is `--panel` with a `--mass` border and a soft shadow, using `light-dark(rgba(20,40,40,.16), rgba(0,0,0,.5))` for its color.

### Encounter block

(top right of the centre column). Label in `--dim` 12.5px; the caught species in sans 600 24px, with its 32px icon before it.

### Repel ladder

A 22px bar with a 3px radius and a `--rule` border. Segments take `--seg-1` to `--seg-5` in order and cycle. Separate segments with a 1px `--panel` gap. Text on a segment is `--ink` or `--on-mass`, picked per segment from the fill's relative luminance at a 0.33 threshold, as `palette-options.html` does. Caught segments are hatched: `repeating-linear-gradient(135deg, var(--panel) 0 3px, var(--sunken) 3px 6px)`. The best rung's label is `--act` at 600.

### Uplift headline

Pixel face, 28px. `--act` when the value meets R3's threshold, `--error` when it misses. The explanation beneath stays `--dim`.

### Planner

Unchanged structure; percentages in the plan lines are `--act` at 600.

### Findings

The rule code is mono in `--error` or `--warn`; the message is `--ink`; the "a target beyond vanilla" aside is `--faint`.

### Toast

`--ink` background with `--ground` text, which inverts correctly in both themes; the error variant uses `--error` with `--on-mass` text.

## 7. Dex view

### List rows

36px: icon, name, two mini type chips, and the base-stat total in mono with its delta. A new species shows "new" in `--place-ink`. Deltas are `--mass` when up and `--dim` when down; a stat change is information, not the one number to act on, so it does not use gold.

### Species header

The front sprite at 2x (160 by 160, pixelated) standing on a stage: a 120 by 24px ellipse of `--sunken` under its feet, the platform the DS draws under a battler. Beside it, the dex number in the pixel face in `--faint`, the name in sans 22px 650, the type chips, and the canon note in `--dim`.

### Stats

9px bars on a `--sunken` track, filled by band with `--stat-0` to `--stat-4`; value in mono, delta beside it.

### Abilities

Neutral chips; the hidden ability's chip is `--place-bg` with `--place-ink` and the word "hidden".

### Evolution line

32px icons with name and table count, separated by a `›` in `--faint`. The stage being viewed gets a 2px `--place-ink` underline.

### Learnset

Level in mono, move name, a small type chip, the class as `--dim` text, power and accuracy in mono.

### Where it is met

Rows are clickable and turn `--sunken` on hover; each has its split tag and its share in `--mass` mono.

### Type matchups

A grid of the eighteen type chips, six by three, each with its multiplier. Weaknesses take the warm end of the stat bands and resistances the cool end, so the grid and the stat bars agree on what warm and cool mean:

| Multiplier | Fill |
|---|---|
| ×4 | `--stat-0` at 45% into `--panel` |
| ×2 | `--stat-0` at 24% |
| ×1 | no fill, `--faint` text |
| ×0.5 | `--stat-4` at 24% |
| ×0.25 | `--stat-4` at 45% |
| ×0 | no fill, dashed `--rule` border: an immunity drawn as absence |

## 8. The damage calculator (D5)

The vendored Dynamic Calc keeps its own markup and layout. When D5 lands, add `calc/oxide-skin.css` after its stylesheets. The skin links `../ui/theme.css`, loads `../ui/theme.js` so the calculator follows the same toggle, and maps its backgrounds, text, borders, buttons and select menus onto the tokens. Record the skin in `VENDORED.md`'s patch list so an upstream update re-applies it. Do not restyle its layout.

## 9. Flavor, each optional and small

1. The title reads "Platinum Oxide" with the second word in `--place-ink`.
2. A favicon as an inline SVG data URI: a 16 by 16 pixel mark, a teal diamond with a pink core. No Poké Ball.
3. The empty centre column ("Choose an area") shows one party icon from the pick-list at 40% opacity, chosen at random on each load.
4. Ladder segments ease their widths over 200ms when a species is ticked, so the redistribution the M4 comment describes can actually be watched. This needs the ladder updated in place rather than rebuilt through `innerHTML`. Skip it under `prefers-reduced-motion`.

## 10. Accessibility

Contrast for palette B after tuning, WCAG ratios:

| Pair | Light | Dark |
|---|---|---|
| ink on ground | 14.2 | 15.2 |
| ink on place-bg | 11.9 | 12.2 |
| dim on panel | 5.9 | 6.7 |
| dim on place-bg | 4.6 | 5.9 |
| faint on panel (de-emphasised only, target 3.0) | 3.2 | 3.2 |
| mass on panel | 5.1 | 7.8 |
| mass on ground | 4.7 | 8.5 |
| place-ink on place-bg | 4.6 | 7.8 |
| place-ink on panel | 6.0 | 9.0 |
| act on panel | 4.7 | 9.3 |
| warn on panel | 4.5 | 6.8 |
| error on panel | 7.3 | 5.6 |
| on-mass on mass | 5.2 | 8.5 |

Every text role meets AA's 4.5 except `--faint`, which is reserved for caught, disabled and placeholder text and meets 3.0. Color never carries a meaning alone: lint has a dot and a rule code, metrics have words, caught has a strike-through. The focus ring is visible in both themes. Motion respects `prefers-reduced-motion`. Keyboard behavior is unchanged.

## 11. Implementation notes for Claude Code

Work on a worktree branch of the encounter track and merge when the suites are green.

Files: new `ui/theme.css`, new `ui/theme.js`, new `ui/fonts/PixelifySans-600-latin.woff2` and `ui/fonts/OFL.txt`, and `ui/index.html`. `server.py` should need nothing, since it already serves `ui/` as static files and knows the font's MIME type.

Order:

1. Tokens and theme mechanics: `theme.css`, `theme.js`, the meta tag, the toggle.
2. Replace every literal color in `index.html` with a token. Today's file has them in the stylesheet (`#fff`, `#e6eaef`, `#dfeaf0` and others), in the `SEGMENT` array, and in the stat bands `.s0` to `.s4` on the M8 branch.
3. The pixel face and the type scale.
4. Type chips, split tags, and the "on" states moving from teal to place.
5. The Dex species page: stage, chips, matchup grid.
6. Flavor items, if wanted.

Add one check to `test_m4`: `index.html` and `theme.js` contain no hex color literal, so a stray one fails the suite instead of breaking a theme quietly. `test_m4` and `test_m8` must otherwise stay at their current counts.

Acceptance: Ian opens the tool in both themes at his usual display scaling and signs off, and the contrast pairs above are re-checked against the final token values if any were changed during implementation.
