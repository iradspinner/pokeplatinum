// Dump the vendored calculator's canonical species table as JSON, so the tool
// can read it without node at runtime. The encounter tool is Python stdlib and
// stays that way; this is an authoring step, run when the calculator is
// updated, not when the tool runs.
//
//     node tools/oxide/encounters/make_canon.js > tools/oxide/encounters/canon.json
//
// The table is the calculator's own, which makes it the right baseline twice
// over: it is what a species really has in its home generation, and it is what
// the calculator will believe when D5 feeds it ours.
const path = require('path');
// Upstream @smogon/calc, not the vendored calculator's own copy: that one ships
// whatever data it was last built with, which is a romhack's, and it would have
// the dex report changes this project never made. canon_src/README.md has the
// evidence.
const file = path.join(__dirname, 'canon_src', 'data', 'species.js');
const { SPECIES } = require(file);

// The last entry is the newest generation. Upstream has ten and hzla's fork
// had nine, so counting from the end is the only stable way to say "newest".
const gen9 = SPECIES[SPECIES.length - 1];
const out = {};
for (const name of Object.keys(gen9).sort()) {
  const s = gen9[name];
  if (!s || !s.bs) continue;
  out[name] = {
    types: s.types,
    stats: {
      hp: s.bs.hp, attack: s.bs.at, defense: s.bs.df,
      special_attack: s.bs.sa, special_defense: s.bs.sd, speed: s.bs.sp,
    },
    weightkg: s.weightkg,
    abilities: s.abilities ? Object.values(s.abilities) : [],
  };
  if (s.baseSpecies) out[name].base_species = s.baseSpecies;
}
process.stdout.write(JSON.stringify(out, null, 0) + '\n');
