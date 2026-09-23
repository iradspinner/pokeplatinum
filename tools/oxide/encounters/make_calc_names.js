// Dump the vendored calculator's ability, move and item names as JSON, so the
// export can say which of Oxide's abilities and moves the calculator has
// logic for. Like make_canon.js, this is an authoring step run when the
// calculator is updated, not when the tool runs; the tool stays Python stdlib.
//
//     node tools/oxide/encounters/make_calc_names.js > tools/oxide/encounters/calc_names.json
//
// The calculator keys every effect off these exact names. An Oxide ability or
// move whose name is not here still loads (a move with its own power, type and
// category), but the calculator has no logic for what it does beyond that.
const path = require('path');
const data = path.join(__dirname, 'calc', 'calc', 'data');
const { ABILITIES } = require(path.join(data, 'abilities.js'));
const { MOVES } = require(path.join(data, 'moves.js'));
const { ITEMS } = require(path.join(data, 'items.js'));

// The last entry is the newest generation, which holds every name.
const abilities = ABILITIES[ABILITIES.length - 1];
const moves = MOVES[MOVES.length - 1];
const items = ITEMS[ITEMS.length - 1];
const out = {
  abilities: [...(Array.isArray(abilities) ? abilities : Object.keys(abilities))].sort(),
  // Type and category ride along so a name matched by closeness can be
  // checked against what the move is, not only what it is called.
  moves: Object.fromEntries(Object.keys(moves).filter(n => n !== '(No Move)').sort()
    .map(n => [n, [moves[n].type, moves[n].category || '']])),
  // Held items, for trainer sets.
  items: [...(Array.isArray(items) ? items : Object.keys(items))].sort(),
};
process.stdout.write(JSON.stringify(out, null, 0) + '\n');
