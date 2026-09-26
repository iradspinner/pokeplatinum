"use strict";
exports.__esModule = true;

// Oxide patch (encounter tool, 2026-09-26): Platinum Oxide's own damage rules,
// as its engine applies them in src/battle/battle_lib.c's
// BattleSystem_CalcMoveDamage, in the same places and with the same integer
// rounding. Element 5's abilities that change damage or a stat stage (Ian's
// ruling), the moves whose power or damage Oxide works out in code, the
// always-critical moves, and a dual type's two factors applied in the type
// chart's row order. The move lists come from platinum-oxide-data.js, which
// make_calc_mechanics.py generates from the engine, so they are Oxide's and
// not Showdown's.

var helpers_1 = require("../helpers");
var data_1 = require("./platinum-oxide-data");

function data() {
    return data_1.platinumOxideData || {};
}

function inList(list, move) {
    return (data()[list] || []).indexOf(move.name) !== -1;
}

function isContact(ctx) {
    // Long Reach's holder makes no contact (Battler_MoveMakesContact).
    return inList("contact", ctx.move) && !ctx.attacker.hasAbility("Long Reach");
}

function anyAbility(ctx) {
    var names = Array.prototype.slice.call(arguments, 1);
    return ctx.attacker.hasAbility.apply(ctx.attacker, names) ||
        ctx.defender.hasAbility.apply(ctx.defender, names);
}

var platinumOxideProfile = (0, helpers_1.makeProfile)({
    id: "platinum-oxide",
    gens: [4],
    titleMatchers: [{ equals: "Platinum Oxide" }],
    hooks: {
        // Pixilate and Liquid Voice change the move's type before anything
        // reads it (BattleSystem_SetMoveTypeByAbility).
        afterMoveType: [
            function (ctx) {
                var move = ctx.move;
                if (!move.bp) {
                    return;
                }
                if (ctx.attacker.hasAbility("Pixilate") && move.hasType("Normal") &&
                    !inList("pixilateKeepsType", move)) {
                    move.type = "Fairy";
                    ctx.state.pixilated = true;
                    ctx.desc.attackerAbility = ctx.attacker.ability;
                    ctx.desc.moveType = move.type;
                }
                else if (ctx.attacker.hasAbility("Liquid Voice") && inList("sound", move)) {
                    move.type = "Water";
                    ctx.desc.attackerAbility = ctx.attacker.ability;
                    ctx.desc.moveType = move.type;
                }
            }
        ],
        // Sap Sipper takes Grass moves, Bulletproof ball and bomb moves and
        // Overcoat powder moves. Mold Breaker has already cleared the
        // defender's ability by the time this runs.
        moveImmunity: [
            function (ctx, immune) {
                var move = ctx.move, def = ctx.defender;
                if ((def.hasAbility("Sap Sipper") && move.hasType("Grass")) ||
                    (def.hasAbility("Bulletproof") && inList("bullet", move)) ||
                    (def.hasAbility("Overcoat") && inList("powder", move))) {
                    ctx.desc.defenderAbility = def.ability;
                    return true;
                }
                return immune;
            }
        ],
        // The always-critical moves, and Merciless against a poisoned target.
        criticalHit: [
            function (ctx, isCritical) {
                if (ctx.defender.hasAbility("Battle Armor", "Shell Armor")) {
                    return isCritical;
                }
                if (inList("alwaysCrit", ctx.move)) {
                    return true;
                }
                if (ctx.attacker.hasAbility("Merciless") && ctx.defender.hasStatus("psn", "tox")) {
                    ctx.desc.attackerAbility = ctx.attacker.ability;
                    return true;
                }
                return isCritical;
            }
        ],
        // Psywave deals the user's level times a random 5 to 15, over 10, at
        // least 1 (effect script 88); Super Fang half the target's current HP
        // (effect script 40). Both ignore the rest of the formula.
        fixedDamage: [
            function (ctx, damage) {
                var move = ctx.move;
                if (move.named("Psywave")) {
                    var lv = ctx.attacker.level, rolls = [];
                    for (var i = 0; i < 16; i++) {
                        var r = 5 + Math.round(i * 10 / 15);
                        rolls.push(Math.max(1, Math.floor(lv * r / 10)));
                    }
                    return rolls;
                }
                if (move.named("Super Fang")) {
                    return Math.max(1, Math.floor(ctx.defender.curHP() / 2));
                }
                return damage;
            }
        ],
        // Powers Oxide works out in code (battle_script.c): Heavy Slam from
        // the weight ratio at hg-engine's thresholds, Trump Card from the PP
        // left (the calculator cannot know it, so full PP: 40). Electro Ball
        // has no power code in the engine yet, so the game hits with its
        // data's power of 1, and so does this.
        moveBasePower: [
            function (ctx, basePower) {
                var move = ctx.move;
                if (move.named("Heavy Slam")) {
                    var aw = Math.max(1, Math.round(ctx.attacker.weightkg * 10));
                    var dw = Math.round(ctx.defender.weightkg * 10);
                    var ratio = Math.floor(dw * 10000 / aw);
                    basePower = ratio <= 2000 ? 120 : ratio <= 2500 ? 100 : ratio <= 3334 ? 80
                        : ratio <= 5000 ? 60 : 40;
                    ctx.desc.moveBP = basePower;
                    return basePower;
                }
                if (move.named("Trump Card")) {
                    ctx.desc.moveBP = 40;
                    return 40;
                }
                if (move.named("Electro Ball")) {
                    ctx.desc.moveBP = 1;
                    return 1;
                }
            }
        ],
        // After Technician, in the engine's order: Sharpness, Pixilate, Sheer
        // Force, the auras, Battery.
        powerAfterTechnician: [
            function (ctx, basePower) {
                var move = ctx.move, att = ctx.attacker, desc = ctx.desc;
                if (att.hasAbility("Sharpness") && inList("slicing", move)) {
                    basePower = Math.floor(basePower * 15 / 10);
                    desc.attackerAbility = att.ability;
                }
                if (ctx.state.pixilated) {
                    basePower = Math.floor(basePower * 12 / 10);
                }
                if (att.hasAbility("Sheer Force") && inList("sheerForce", move)) {
                    basePower = Math.floor(basePower * 13 / 10);
                    desc.attackerAbility = att.ability;
                }
                if ((move.hasType("Dark") && anyAbility(ctx, "Dark Aura")) ||
                    (move.hasType("Fairy") && anyAbility(ctx, "Fairy Aura"))) {
                    basePower = anyAbility(ctx, "Aura Break")
                        ? Math.floor(basePower * 75 / 100)
                        : Math.floor(basePower * 133 / 100);
                }
                if (move.category === "Special" && ctx.field.attackerSide.isBattery) {
                    basePower = Math.floor(basePower * 130 / 100);
                }
                return basePower;
            }
        ],
        // Beside Thick Fat: Purifying Salt halves Ghost moves and Water Bubble
        // Fire moves against its holder.
        defenderPowerMods: [
            function (ctx, basePower) {
                var move = ctx.move, def = ctx.defender;
                if (def.hasAbility("Purifying Salt") && move.hasType("Ghost")) {
                    basePower = Math.floor(basePower / 2);
                    ctx.desc.defenderAbility = def.ability;
                }
                if (def.hasAbility("Water Bubble") && move.hasType("Fire")) {
                    basePower = Math.floor(basePower / 2);
                    ctx.desc.defenderAbility = def.ability;
                }
                return basePower;
            }
        ],
        // Steelworker raises the attacking stat of Steel moves by half, and
        // Water Bubble doubles it for Water moves.
        attackStat: [
            function (ctx, attack) {
                var move = ctx.move, att = ctx.attacker;
                if (att.hasAbility("Steelworker") && move.hasType("Steel")) {
                    ctx.desc.attackerAbility = att.ability;
                    return Math.floor(attack * 150 / 100);
                }
                if (att.hasAbility("Water Bubble") && move.hasType("Water")) {
                    ctx.desc.attackerAbility = att.ability;
                    return attack * 2;
                }
                return attack;
            }
        ],
        // After Flash Fire and before the formula's +2: Fluffy halves contact
        // moves and doubles Fire ones, and Ice Scales halves special moves.
        beforeFinalDamage: [
            function (ctx, baseDamage) {
                var move = ctx.move, def = ctx.defender;
                if (def.hasAbility("Fluffy")) {
                    if (isContact(ctx)) {
                        baseDamage = Math.floor(baseDamage / 2);
                    }
                    if (move.hasType("Fire")) {
                        baseDamage = baseDamage * 2;
                    }
                    ctx.desc.defenderAbility = def.ability;
                }
                if (def.hasAbility("Ice Scales") && move.category === "Special") {
                    baseDamage = Math.floor(baseDamage / 2);
                    ctx.desc.defenderAbility = def.ability;
                }
                return baseDamage;
            }
        ],
        // A dual type's factors in the chart's row order (Ian, 2026-09-22):
        // the engine walks its table and applies each matching row in turn, so
        // the factor whose row comes first is applied, and rounded, first.
        typeFactorOrder: [
            function (ctx, factors) {
                var order = data().chartOrder || {};
                var row = order[ctx.move.type] || {};
                var types = ctx.defender.types;
                var r1 = row[types[0]], r2 = types[1] ? row[types[1]] : undefined;
                if (r1 !== undefined && r2 !== undefined && r2 < r1) {
                    return [factors[1], factors[0]];
                }
                return factors;
            }
        ]
    }
});
exports.platinumOxideProfile = platinumOxideProfile;
