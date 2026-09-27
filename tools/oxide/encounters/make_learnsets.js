// Two of the team builder's three move lists (build plan item 28), from
// Pokemon Showdown's learnsets: what a species could legally know in
// Generation IV, and in the newest generation it appears in. The third list,
// what it can know in Oxide, is read live from res/ and needs nothing here.
//
// An authoring step, run when the Showdown package is updated, never when the
// tool runs (the tool is Python stdlib and reads the JSON this writes):
//
//     npm pack pokemon-showdown@0.11.11 && tar -xzf pokemon-showdown-0.11.11.tgz
//     node tools/oxide/encounters/make_learnsets.js package \
//         > tools/oxide/encounters/canon_learnsets.json
//
// canon_src/README.md records the package's version, hash and licence.
//
// For each species, both lists hold its own moves, the moves of every earlier
// stage in Showdown's chain (as Showdown's own validator allows them), and for
// a form that changes in battle (Rotom-Wash) its base form's. The newest
// generation is the highest one with any source for the species. Showdown's
// main file has Scarlet and Violet (9) and Sword and Shield (8); Brilliant
// Diamond and Shining Pearl are in its gen8bdsp mod, and a Sinnoh species cut
// from Scarlet and Violet (Bidoof, Spinda) is there and nowhere newer, so a
// Generation 8 list is Sword and Shield with BDSP. Legends: Arceus is left out
// (no TMs, another way of learning), except for a species found nowhere else
// from Generation 8 on.
const path = require('path');

const pkg = process.argv[2];
if (!pkg) {
  process.stderr.write('usage: node make_learnsets.js <unpacked pokemon-showdown package>\n');
  process.exit(2);
}
const data = f => require(path.resolve(pkg, 'dist', 'data', f));
const MAIN = data('learnsets.js').Learnsets;
const BDSP = data('mods/gen8bdsp/learnsets.js').Learnsets;
const LEGENDS = data('mods/gen8legends/learnsets.js').Learnsets;
const DEX = data('pokedex.js').Pokedex;
const VERSION = require(path.resolve(pkg, 'package.json')).version;

const toId = s => String(s || '').toLowerCase().replace(/[^a-z0-9]/g, '');
// "4L12" -> gen 4, "L12"; "8S3" (an event, by index) -> gen 8, "S". A "V"
// (moved over from the Virtual Console games) is no source in its generation.
function parse(src) {
  const m = /^(\d)([A-Z])(\d*)$/.exec(src);
  if (!m || m[2] === 'V') return null;
  return { gen: +m[1], how: m[2] === 'L' ? 'L' + m[3] : m[2] };
}

// The species whose learnsets make up `id`'s: itself, its battle base, and
// its earlier stages, each with the id it is credited to (null for its own).
function sources(id) {
  const out = [[id, null]];
  const entry = DEX[id] || {};
  if (entry.changesFrom) out.push([toId(entry.changesFrom), toId(entry.changesFrom)]);
  if (!MAIN[id] && entry.baseSpecies) out.push([toId(entry.baseSpecies), null]);
  let prevo = entry.prevo;
  const seen = new Set([id]);
  while (prevo && !seen.has(toId(prevo))) {
    const p = toId(prevo);
    seen.add(p);
    out.push([p, p]);
    prevo = (DEX[p] || {}).prevo;
  }
  return out;
}

// {move: {hows: Set, from}} for one generation, from one or more files.
function collect(id, gen, files) {
  const moves = new Map();
  for (const [sid, from] of sources(id)) {
    for (const file of files) {
      const ls = (file[sid] || {}).learnset || {};
      for (const [move, srcs] of Object.entries(ls)) {
        for (const s of srcs) {
          const p = parse(s);
          if (!p || p.gen !== gen) continue;
          if (!moves.has(move)) moves.set(move, { hows: new Set(), from });
          const rec = moves.get(move);
          // A species' own way of learning a move wins over an earlier stage's.
          if (rec.from && !from) { rec.from = null; rec.hows = new Set(); }
          if (rec.from === from || !from) rec.hows.add(p.how);
        }
      }
    }
  }
  return [...moves.entries()].sort(([a], [b]) => a.localeCompare(b))
    .map(([move, r]) => r.from ? [move, [...r.hows].join(','), r.from]
                               : [move, [...r.hows].join(',')]);
}

function newest(id) {
  let best = 0;
  for (const [sid] of sources(id).slice(0, 1).concat(DEX[id] && !MAIN[id] && DEX[id].baseSpecies
                                                     ? [[toId(DEX[id].baseSpecies)]] : [])) {
    for (const file of [MAIN, BDSP]) {
      for (const srcs of Object.values((file[sid] || {}).learnset || {})) {
        for (const s of srcs) {
          const p = parse(s);
          if (p && p.gen > best) best = p.gen;
        }
      }
    }
  }
  return best;
}

// A trainer's party cannot hold a form that exists only in battle (a Mega, a
// Gigantamax, a Totem) or one of Showdown's own made-up species (number 0 or
// below), so those are left out; they were most of the file's size.
const skip = id => {
  const e = DEX[id];
  return !e || e.num <= 0 || e.battleOnly || /Mega|Gmax|Totem|Primal/.test(e.forme || '');
};
const out = { _about: { package: `pokemon-showdown@${VERSION}` } };
const ids = new Set([...Object.keys(MAIN), ...Object.keys(DEX).filter(id => DEX[id].baseSpecies)]);
for (const id of [...ids].sort()) {
  if (skip(id)) continue;
  const gen4 = collect(id, 4, [MAIN]);
  let gen = newest(id), games = null, latest;
  if (gen >= 8) {
    latest = collect(id, gen, gen === 8 ? [MAIN, BDSP] : [MAIN]);
    games = gen === 9 ? 'Scarlet and Violet' : 'Sword and Shield, Brilliant Diamond and Shining Pearl';
  } else if (LEGENDS[id]) {
    gen = 8;
    latest = collect(id, 8, [LEGENDS]);
    games = 'Legends: Arceus';
  } else {
    latest = gen ? collect(id, gen, [MAIN]) : [];
  }
  if (!gen4.length && !latest.length) continue;
  out[id] = { gen4, latest: { gen, games, moves: latest } };
}
// Showdown's own name for every move the lists use, since a move Oxide lacks
// has no name on the Python side.
const MOVES = data('moves.js').Moves;
const used = new Set();
for (const [id, e] of Object.entries(out)) {
  if (id === '_about') continue;
  for (const m of e.gen4.concat(e.latest.moves)) used.add(m[0]);
}
out._moves = Object.fromEntries([...used].sort().map(id => [id, (MOVES[id] || {}).name || id]));
// One species a line, so an update reads as a diff of the species it touched.
const lines = Object.entries(out).map(([k, v]) => JSON.stringify(k) + ': ' + JSON.stringify(v));
process.stdout.write('{\n' + lines.join(',\n') + '\n}\n');
