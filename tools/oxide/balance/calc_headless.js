// B3: the vendored damage calculator's own engine, run headless in Node.
//
//     node tools/oxide/balance/calc_headless.js <blob.json> <jobs.json> <out.json>
//
// The blob is what the encounter tool's server hands the calculator's page
// (calc_export.build()). The jobs file names Pokemon and the matchups to
// run; the output holds each matchup's sixteen damage rolls. pressure.py
// writes the jobs and reads the answers.
//
// The page is copied, not reimplemented. The engine files are read from
// tools/oxide/encounters/calc/ in the order index.html loads them, into one
// shared scope with the same require() shim the page defines, so the engine
// runs exactly the code the page runs. The page's own data loader
// (initialize.js) needs jQuery and the DOM, so the few steps of it that
// touch the engine are repeated here, and the helper they call to merge a
// move record is lifted out of initialize.js's text rather than copied.
// What each step mirrors is named where it happens.
//
// One process, synchronous, no workers: the degraded CPU runs one busy core
// cleanly and falls over under many.
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const CALC = path.join(__dirname, '..', 'encounters', 'calc');
const GEN = 8;              // the page's species and move tables (settings.gen)
const DAMAGE_GEN = 4;       // the Oxide branch of setGameSettings
const CHART_ID = 13;        // BACKUP_DATA_TYPE_CHART in initialize.js

function engineFiles() {
  // Every ./calc/ script tag in index.html, in order, skipping commented-out
  // lines. data/evos.js is loaded twice by the page, and twice here too.
  const html = fs.readFileSync(path.join(CALC, 'index.html'), 'utf8');
  const out = [];
  for (const line of html.split('\n')) {
    if (line.trim().startsWith('<!--')) continue;
    const m = line.match(/<script[^>]*src="\.\/(calc\/[^"?]+)/);
    if (m) out.push(m[1]);
  }
  return out;
}

function liftFunction(source, name) {
  // The text of one top-level function from a page script, by brace count.
  const start = source.indexOf('function ' + name + '(');
  if (start < 0) throw new Error('initialize.js has no ' + name);
  let depth = 0;
  for (let i = source.indexOf('{', start); i < source.length; i++) {
    if (source[i] === '{') depth++;
    else if (source[i] === '}' && --depth === 0) return source.slice(start, i + 1);
  }
  throw new Error('unbalanced ' + name);
}

function makeEngine(blob) {
  const ctx = {
    console: { log() {}, warn() {}, error: console.error },
    TITLE: blob.title,
    gameGen: DAMAGE_GEN,     // setGameSettings' Oxide branch
    mechanics: 'vanilla',    // initialize.js's default, which Oxide keeps
    calcingForSwitchIns: false,
    settings: {
      gen: GEN, damageGen: DAMAGE_GEN, critGen: DAMAGE_GEN, typeChart: CHART_ID,
      type_chart: CHART_ID, physSpecSplit: true, invertTypes: false, sourceType: 'full',
    },
    localStorage: {},
    pokedex: {},
  };
  vm.createContext(ctx);
  // The page's shim, from the inline script before the engine's tags.
  vm.runInContext(
    'this.__createBinding = function(o, m, k) { o[k] = m[k]; };\n' +
    'var calc = exports = {};\nfunction require() { return exports };', ctx);
  for (const rel of engineFiles()) {
    vm.runInContext(fs.readFileSync(path.join(CALC, rel), 'utf8'), ctx, { filename: rel });
  }
  const init = fs.readFileSync(path.join(CALC, 'js', 'initialize.js'), 'utf8');
  for (const name of ['applyExportedMoveData', 'toImportedBaseStats']) {
    vm.runInContext(liftFunction(init, name), ctx);
  }
  ctx.__blob = blob;
  vm.runInContext(`
    (function () {
      var g = ${GEN};
      function clean(s) { return String(s).replace(/[^a-zA-Z0-9]/g, '').toLowerCase(); }
      // applyBackupDataTypeChart: the blob's chart, as chart 13 and as the
      // global typeChart that mechanics/util.js reads for effectiveness.
      calc.registerCustomTypeChart(__blob.type_chart, ${CHART_ID});
      typeChart = __blob.type_chart;
      // loadMovesData's second loop: every exported move merged into
      // MOVES_BY_ID, or created when the calculator has no such move.
      for (var move in __blob.moves) {
        var id = clean(move);
        var src = __blob.moves[move];
        if (MOVES_BY_ID[g][id]) {
          MOVES_BY_ID[g][id] = applyExportedMoveData(MOVES_BY_ID[g][id], src, MOVES_BY_ID[g][id].name, id);
        } else {
          src.flags = src.flags || {};
          src.name = move;
          MOVES_BY_ID[g][id] = applyExportedMoveData(Object.assign({}, MOVES_BY_ID[8][id] || {}), src, move, id);
        }
      }
      // loadPoksData: known species take the blob's stats and types, and
      // (customPoks) an unknown one is created from its record.
      for (var pok in __blob.poks) {
        var rec = __blob.poks[pok];
        var pid = clean(pok);
        var entry = SPECIES_BY_ID[g][pid];
        if (entry && entry.name === pok) {
          entry.types = rec.types;
          entry.baseStats = toImportedBaseStats(rec.bs);
          if (rec.abilities) entry.abilities = rec.abilities;
        } else {
          rec.baseStats = toImportedBaseStats(rec.bs);
          rec.id = pid; rec.kind = 'Species'; rec.name = pok;
          SPECIES_BY_ID[g][pid] = rec;
        }
      }
    })();`, ctx);
  return ctx;
}

function ownSpecies(rec) {
  // B3b: a reference hack's Pokemon carries its own game's base stats,
  // types and weight ("species_data"), since each hack rebalances species;
  // these replace Oxide's record for that one Pokemon only.
  const bs = rec.bs;
  const out = {
    baseStats: { hp: bs.hp, atk: bs.at, def: bs.df, spa: bs.sa, spd: bs.sd, spe: bs.sp },
    types: rec.types.filter(Boolean).slice(0, 2),
  };
  if (rec.weightkg !== undefined) out.weightkg = rec.weightkg;
  return out;
}

function speciesOverrides(blob, name) {
  // createPokemon's set branch: the page passes the species' own stats,
  // types, weight and abilities as overrides on every Pokemon it builds.
  const rec = blob.poks[name];
  if (!rec) return undefined;
  const bs = rec.bs;
  const out = {
    baseStats: { hp: bs.hp, atk: bs.at, def: bs.df, spa: bs.sa, spd: bs.sd, spe: bs.sp },
    types: rec.types.filter(Boolean).slice(0, 2),
  };
  if (rec.weightkg !== undefined) out.weightkg = rec.weightkg;
  if (rec.abilities) out.abilities = rec.abilities;
  return out;
}

function stats(o) {
  // The balance tool's stat keys to the calculator's.
  if (!o) return undefined;
  return { hp: o.hp, atk: o.at, def: o.df, spa: o.sa, spd: o.sd, spe: o.sp };
}

function moveOverrides(blob, name) {
  // getMoveDetails: power, type and category come from the page's move
  // fields, which loadMovesData filled from the blob.
  const rec = blob.moves[name];
  if (!rec) return {};
  const bp = rec.basePower !== undefined ? rec.basePower : rec.bp;
  const out = { type: rec.type, category: rec.category };
  if (bp !== undefined) out.basePower = bp;
  return out;
}

// Generation 4's Hidden Power, from the IVs, as the page's
// getHiddenPowerDetailsFromIVs works it out: the low bit of each IV picks
// the type, the second bit the power, and it is always special.
const HP_TYPES = ['Fighting', 'Flying', 'Poison', 'Ground', 'Rock', 'Bug', 'Ghost', 'Steel',
  'Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ice', 'Dragon', 'Dark'];
function hiddenPower(ivs) {
  const order = ['hp', 'at', 'df', 'sp', 'sa', 'sd'];
  let t = 0, p = 0;
  order.forEach((k, i) => {
    const v = ivs && ivs[k] !== undefined ? ivs[k] : 31;
    t += (v & 1) << i;
    p += ((v >> 1) & 1) << i;
  });
  return { type: HP_TYPES[Math.floor(t * 15 / 63)], basePower: Math.floor(p * 40 / 63) + 30,
           category: 'Special' };
}

function rolls(damage) {
  // A multi-hit move reports one roll list per hit; its total is the sum.
  if (typeof damage === 'number') return [damage];
  if (Array.isArray(damage[0])) {
    return damage[0].map((_, i) => damage.reduce((s, hit) => s + hit[i], 0));
  }
  return damage.slice();
}

function run(blob, jobs) {
  const ctx = makeEngine(blob);
  const calc = ctx.calc;
  const built = {};
  function mon(key) {
    if (built[key]) return built[key];
    const p = jobs.pokemon[key];
    built[key] = new calc.Pokemon(GEN, p.species, {
      level: p.level, ability: p.ability || undefined, abilityOn: true,
      item: p.item || '', nature: p.nature || 'Hardy',
      ivs: stats(p.ivs), evs: stats(p.evs),
      // B5: a setup branch's stat stages ({"atk": 1, "spe": -1}).
      boosts: p.boosts || undefined,
      overrides: p.species_data ? ownSpecies(p.species_data) : speciesOverrides(blob, p.species),
    });
    return built[key];
  }
  const out = { pokemon: {}, results: [] };
  for (const [a, d, moveNames, weather] of jobs.pairs) {
    const att = mon(a), def = mon(d);
    const field = new calc.Field({ gameType: 'Singles', weather: weather || undefined });
    // Speed under this matchup's weather, as the engine's own getFinalSpeed
    // reads it (Swift Swim and Chlorophyll change who moves first).
    const g4 = calc.Generations.get(DAMAGE_GEN);
    const row = { a, d, weather: weather || null, moves: {},
      speeds: [calc.getFinalSpeed(g4, att, field, field.attackerSide),
               calc.getFinalSpeed(g4, def, field, field.defenderSide)] };
    const own = jobs.pokemon[a].move_data || {};
    for (const name of moveNames) {
      // B3b: a reference hack's Pokemon names its moves' type, power,
      // category and priority from its own game's table ("move_data"). The
      // empty flags let a move the engine has never heard of be built.
      const overrides = own[name] ? Object.assign({ flags: {} }, own[name])
        : name === 'Hidden Power' ? hiddenPower(jobs.pokemon[a].ivs) : moveOverrides(blob, name);
      const move = new calc.Move(GEN, name, {
        ability: att.ability, item: att.item, species: att.name, overrides,
      });
      let r;
      try {
        r = calc.calculate(DAMAGE_GEN, att, def, move, field);
      } catch (e) {
        row.moves[name] = { error: String(e && e.message || e) };
        continue;
      }
      const rs = rolls(r.damage);
      if (!rs.every(Number.isFinite)) {
        // A result the engine could not work out (NaN), reported rather than
        // read as zero.
        row.moves[name] = { error: 'damage is not a number' };
        continue;
      }
      // The category lets B5 apply Hustle's accuracy cost to physical moves only.
      row.moves[name] = { rolls: rs.sort((x, y) => x - y), priority: move.priority || 0,
        category: move.category };
    }
    out.results.push(row);
  }
  for (const key of Object.keys(built)) {
    const p = built[key];
    const field = new calc.Field({ gameType: 'Singles' });
    out.pokemon[key] = {
      hp: p.maxHP(), stats: p.stats,
      speed: calc.getFinalSpeed(calc.Generations.get(DAMAGE_GEN), p, field, field.attackerSide),
      types: p.types, ability: p.ability, item: p.item,
    };
  }
  return out;
}

if (require.main === module) {
  const [blobPath, jobsPath, outPath] = process.argv.slice(2);
  const blob = JSON.parse(fs.readFileSync(blobPath, 'utf8'));
  const jobs = JSON.parse(fs.readFileSync(jobsPath, 'utf8'));
  const t0 = Date.now();
  const out = run(blob, jobs);
  out.seconds = (Date.now() - t0) / 1000;
  fs.writeFileSync(outPath, JSON.stringify(out));
}

module.exports = { run, engineFiles };
