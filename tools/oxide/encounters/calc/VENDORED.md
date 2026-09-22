# Vendored: Dynamic Calc (decomps)

Upstream: https://github.com/hzla/Dynamic-Calc-Decomps
Commit: `b347b337ec8ff2a6fcc46093f59d7376d3299ba7`, 2026-09-20
Licence: MIT, kept at `calc/LICENSE` (Honko and contributors; the Showdown
calculator this is a fork of, with hzla's romhack changes).

Vendored on 2026-09-22 for the encounter tool's M8, on Ian's call to commit it
rather than fetch it, so the tool works offline and a checkout from any date
builds the same thing.

## What was taken, and what was left

Taken: `index.html`, `calc/`, `css/` and `js/`. That is what the page loads.

Left behind, and why, from a 649 MB clone:

- `img/`, 319 MB of Pokemon, trainer and item sprites. Oxide's own sprites are
  in `res/pokemon/`, which is the only place they are right for this fork, so
  the plan is to serve those instead. Until that is wired up the calculator
  shows broken images, which costs nothing but looks untidy.
- `backups/`, 132 MB, and `cypress/`, `lua/`, `scripts/`, `tools/`,
  `agent_notes/` and the loose `.md` notes: upstream's own working material.
- `js/mastersheet/`, 4.8 MB, which only `mastersheet.html` loads, and that page
  was not taken.

That leaves 12 MB over 195 files.

## Updating it

Clone upstream fresh, copy the same four paths over this directory, drop
`js/mastersheet` again, and re-apply the patches listed below. Record the new
commit at the top of this file. Nothing here is edited by hand except those
patches, so a clean copy plus the patch list is always the whole story.

## Patches this fork applies

None yet. When the data loader is pointed at our own server rather than
npoint.io (M8's D5), the change goes here with the file and the reason, so the
next update knows what to re-apply.

That patch alone does not make the page offline (QA pass, 2026-09-22). As
vendored, `index.html` also loads jQuery and other libraries from Google's,
jsDelivr's and unpkg's CDNs, a Google Tag Manager analytics tag, and game data
from `hzla.github.io`, about 100 remote references. D5 has to vendor or drop
every CDN script, remove the analytics tag and remove every remote data URL,
and record each change here. None of it runs today: the server serves only
`ui/`, so nothing under `calc/` is reachable yet.
