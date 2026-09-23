// Dump which species are not fully evolved, per generation, from the
// upstream Smogon species table the encounter tool already vendors, so the
// balance tool can read it as JSON without node at run time.
//
//     node tools/oxide/balance/make_nfe.js > tools/oxide/balance/nfe.json
//
// Three generations are kept, because a species can gain an evolution later
// (Girafarig is fully evolved in Generation 4 and not in Generation 9):
// gen4 for the Platinum-based hacks, gen8 for the Generation 8 era hacks with
// no species list of their own, gen9 for the rest. metrics.py says which hack
// reads which.
const path = require('path');
const file = path.join(__dirname, '..', 'encounters', 'canon_src', 'data', 'species.js');
const { SPECIES } = require(file);

const out = {};
for (const [label, index] of [['gen4', 4], ['gen8', 8], ['gen9', 9]]) {
  const gen = SPECIES[index];
  out[label] = Object.keys(gen).filter((name) => gen[name] && gen[name].nfe).sort();
}
process.stdout.write(JSON.stringify(out, null, 1) + '\n');
