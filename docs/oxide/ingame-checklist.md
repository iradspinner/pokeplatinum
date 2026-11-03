# Platinum Oxide: the in-game checklist

For the order to work in, read `qa-plan.md` first: one page, one line per check, with the run itself covering most of what follows.

Every check that waits on Ian playing the game, in one place and in the order a
playtest day meets them (Ian, 2026-09-26: all at once when the new CPU is in).
The tracker's "Waiting on Ian" points here; this file holds the full wording.
The `playtest-day` skill runs the day from it. When a check passes, tick it and
move it to the bottom section with the date; when it fails, it becomes an
"Open bug" entry under the tracker's Phase 5, and the line here says so.

Checks marked **(live)** need a local agent attached to melonDS over the GDB stub
(the `debug-live` skill). Ian drives; the agent reads memory. Nothing here asks
an agent to launch an emulator.

## The first five splits, in play order (compiled 2026-10-31)

Every unticked check below that the work on Roark's to Wake's splits added
or depends on, in the order a run meets it, so one session can play them
together. Each row points to the item that holds the full wording; tick the
item there, not here. The kit's warps and sets are in `docs/oxide/test-kit.md`.
A warp ahead of the story can meet story scripts, so the boss rows want a
real save at that point. The times are rough, for one try each.

| # | Check (section, item) | Quickest way there | Time |
|---:|---|---|---:|
| 1 | Section 2, **Soft level caps** | Test kit, Level caps menu | 10 min |
| 2 | Section 2, **Silk Trap's Speed drop** and **Obstruct's Defense drop** | Test kit, move sets 89 and 90 | 5 min |
| 3 | Section 2, **Corrosion through Baneful Bunker** | Test kit, move set 91 | 3 min |
| 4 | Section 2, **King's Shield lets status moves through**, **King's Shield's Attack drop** and **Burning Bulwark lets status moves through** | Test kit, move sets 92 and 93 | 5 min |
| 5 | Section 3, Rare Candy chaining past the level cap | Test kit's Items menu, or the first candy of a run | 3 min |
| 6 | Section 3, **Mandatory fights, Roark's split** | A new game, or the kit's Sandgem warp | 20 min |
| 7 | Section 3, Roark's new team | A real save at Roark's gym | 10 min |
| 8 | Section 3, Level caps: after beating Roark | The same save, then the OxiDex's save bar | 2 min |
| 9 | Below, the OxiDex's honour caps (new) | Real saves before and after Mars 1, then the OxiDex | 10 min |
| 10 | Section 3, **Mandatory fights, Gardenia's split** | The kit's Jubilife warp, then north | 20 min |
| 11 | Section 3, Gardenia's new team | A real save at Eterna's gym | 10 min |
| 12 | Section 4, Level caps through the story (Gardenia to Wake) | Each badge of the run, then the save bar | 1 min a badge |
| 13 | Section 2, **Gauntlets**, the Eterna Galactic building's section, which now ends on 3F's main side | The kit's Eterna City gauntlet warp | 15 min |
| 14 | Section 3, **Mandatory fights, Fantina's split** | A save with the bike, Route 206 south to 207 and 208 | 15 min |
| 15 | Section 3, Wayward Cave 1F's Ice Stone (Diego and Tori's pair) | A save with the bike, Route 206's cave | 10 min |
| 16 | Section 2, **Knock Off on the first turn out** (Ace Trainer Allen's Sableye) | A real save in Hearthome's gym | 5 min |
| 17 | Section 4, **Barry 3 at the Route 209 gate**, at or under 36 | A real save just after Fantina's badge | 15 min |
| 18 | Section 4, **Mandatory fights, Maylene's split** (Route 210 South's way in among them) | The same save, Hearthome to Veilstone | 25 min |
| 19 | Section 4, the Lost Tower's location names | Route 209, on the way | 3 min |
| 20 | Section 4, **Route 214's gate waits on the Cobble Badge** | The kit's Veilstone warp on a new kit game, then the all-badges warp, Fly home and Veilstone again; or real saves before and after Maylene | 5 min |
| 21 | Section 4, Dahlia gates the Game Corner's prizes | The kit's Veilstone warp, or a real save after Maylene | 15 min |
| 22 | Section 4, **The Veilstone tag battle, Officers Tyche and Hermes**, at or under 42 | A real save after Maylene's badge | 15 min |
| 23 | Section 4, **Mandatory fights, Wake's split** | The same save, Route 214 to Pastoria | 25 min |
| 24 | Section 4, Darach and Caitlin block the Pokemon Mansion, the egg on the win, the office's maid, the Trophy Garden | The kit's Pastoria warp, then Route 212 North | 20 min |
| 25 | Section 4, Manaphy's Tail Glow | The egg from row 24, hatched | 10 min |
| 26 | Section 4, The Pokemon Mansion's maid knockout | After row 24, in the mansion's hall | 20 min |
| 27 | Section 4, Pastoria's Ability Capsule ball is gone | The kit's Pastoria warp | 2 min |
| 28 | Section 4, **Surf waits on Cyrus at Celestic Town** | A real save with the Fen Badge, before Celestic | 5 min |
| 29 | Section 2, **A Corrosion holder uses Toxic on a Steel type** | Whenever a trainer's Salandit or Salazzle with Toxic meets a Steel or Poison type; none does yet | as met |

About six hours in all, half of it the four mandatory-fight walks and the
mansion. The bosses with no item of their own (Mars 1, Jupiter 1, Lucas and
Dawn 2, Fantina, Maylene, Barry 4 and Wake) are met in the run itself; note
how many of your Pokemon faint in each.

- [ ] **The OxiDex's honour caps** (2026-10-31, `overseer-cleanup-five`).
  With a save in Gardenia's split before Mars 1 at the Valley Windworks,
  and a party member above Lv. 20, the OxiDex's save bar and the Alpha
  tab's bar read "Over Mars 1's honour cap of 20" and name it; at Lv. 20
  exactly it is not named. After beating Mars 1 and saving, the same
  member is named only above Lv. 26, Gardenia's cap. The same holds for
  Barry 2 (11, before Route 203's battle), Jupiter 1 (29), Lucas and Dawn 2
  (31, after Jupiter 1), Barry 3 (36) and Barry 4 (42, from Maylene's badge
  to Pastoria). The game itself shows nothing.

## 1. The ROMs and the save

- [ ] Build the ordinary ROM and the test kit ROM of the current, pushed
  `oxide` here (`make rom` and `make testkit`) and copy both into
  `~/oxide-playtest`; a build that looks wrong is rebuilt clean here
  (GitHub's build is retired, 2026-10-28).
- [ ] **Start a new game.** An old save reads every ability as NONE by design
  (element 2 moved the field) and is no valid test bed.
- [ ] **The base ROM's visual overhaul** (`carry-over`, merged), compared
  with Ian's own base ROM where anything looks off: the title screen's logo;
  the new Pokemon sprites front and back in battle, sitting at the right
  height on their platforms (the heights came with the sprites); a shiny with
  a custom palette where one turns up (the test kit can make one); the new
  battle backgrounds and platforms on grass, in a cave and indoors; the HP
  box's colours; the party menu's colours; the four new box wallpapers; and,
  post-game, May, Steven, Red and Gold showing their own battle sprites.
  Shadow Force's animation carries one changed byte nobody has explained;
  note anything odd about it.
- [ ] **The battle recorder logs your moves** (alpha readiness step 11; the
  game side landed at 0a27a2b0d, beside the melonDS fork's `beacon-moves`
  build). With any ROM since, and that melonDS build swapped into your
  playing folder while melonDS is closed, start `record.py` in
  `~/oxide-playtest/battle-recordings/`. Fight one wild battle and one
  trainer; in each, use one attacking move, one stat move such as Growl or
  Leer if a Pokemon has one, and one switch. Afterwards, the recorder's file
  for each battle, read with `analyze.py`, should show each Pokemon's four
  moves, the PP of the move you used falling by one, a stat stage after the
  stat move (Atk-1 on the target of Growl, Def-1 for Leer), and under
  "actions by turn" your move, your switch, and the foe's move for every
  turn. `http://127.0.0.1:31124/status` should report `"turnData":true`.
  Note any turn missing from the list. Nothing of this shows during the
  fight itself.

## 2. The test kit ROM

The kit's NPC and menus are described in `docs/oxide/test-kit.md`, set by set,
with what each should show. The kit cannot set up double battles, a frozen
Pokemon, or a foe holding an item; those checks are marked for normal play.

- [ ] **The kit's menus after the bank fix** (2026-10-07, `main-kit-bank`).
  Talk to the kit NPC: the top menu responds to the D-pad and A, fits the
  screen, and its entry before Warp reads "Meister’s trade", not "See you
  next week". The Warp menu's last entry reads "Gauntlet: Victory Road". Move
  sets page 3 ends with "More sets", which opens sets 82 to 88. The Items
  menu's Ice Stone, abilities, Mints and Caps, and TMs entries, and the
  Meister's trade, each print their own line.
- [ ] **Element 4, the move sets.** Sets 1 to 22 passed in rounds 1 to 3
  (2026-09-22 to 23). Of sets 23 to 70, sample only the 34 whose new move a
  trainer or the player can carry (cut on 2026-10-13: a level-up list of an
  obtainable line, a placed TM, a tutor, or a trainer's team today or in the
  comb's drafts). Sets 23 to 26: Dragon Tail and Parting Shot, Lock-On,
  Ingrain and Aqua Ring, Smack Down. Sets 27 to 31: Sticky Web, After You,
  Aurora Veil, the four side guards against the kit's two new wild foes, and
  Belch with the Sitrus Berry the set gives. On the "More sets" page: Electro
  Ball by Speed ratio (32), Stored Power (33), Retaliate (34), Echoed Voice
  (35), Stomping Tantrum and Temper Flare (36), Lash Out (40), Foul Play
  (42), Body Press (43), Psyshock (44), Sacred Sword and Darkest Lariat (45),
  Freeze-Dry and Flying Press (46 and 47), Rage Fist, 50 plus 50 per hit
  taken and kept through switches (48), and Transform copying the whole
  ability (49). Set 51: Shore Up against a Chansey's Seismic Toss, healing
  half Mew's HP in sun or rain and two thirds in a sandstorm. Set 52: Meteor
  Beam charging for a turn with a Sp. Atk raise, then hitting, or hitting at
  once holding the Power Herb the set gives. On the third page: Scale Shot's
  Defense drop and Speed rise (57), Salt Cure's damage each turn, doubled
  after Soak (60), Octolock's drops each turn (61), Magic Room stopping
  Leftovers for five turns (62), Teatime eating a Liechi Berry at full HP
  (63), Beak Blast burning a Tackle (65), and Sky Drop lifting a Chansey that
  then cannot act (66) and not affecting a Skarmory (67). Set 70: after a
  Ninjask's Throat Chop, Hyper Voice fails that turn and neither it nor Heal
  Bell can be chosen the next, then both come back. Five that the cut left
  out have since reached an obtainable line's level-up list, so sample them
  too: Hard Press (38; Steelix, Bastiodon), Grav Apple (41; Shiftry),
  Nature's Madness (56; Clefable, Florges), Core Enforcer (64; Goodra,
  Kingdra) and Lunar Blessing (69; Cresselia, an Acuity Cavern draw). Left
  out, since nothing the player catches or a trainer fields carries their
  moves: sets 37, 39, 50, 53 to 55, 58, 59 and 68 (Last Respects and Baneful
  Bunker are on egg lists only, Wonder Room and Mind Blown only on Nihilego
  and Blacephalon; Pika Papow, Veevee Volley, Electro Shot, Spiky Shield,
  Freeze Shock and Ice Burn on nothing), and Jungle Healing in set 69;
  sample one if a team or list takes its move.
  A stub effect does its damage and skips its extra, or says "But nothing
  happened!"; that is expected. Autotomize prints no "became nimble!", as Ian
  ruled.
- [ ] **Element 5, the Abilities menu** (two pages, Neutralizing Gas last): one
  entry per ability that shows itself, each with its own wild foe. For
  Neutralizing Gas: Galarian Weezing against a wild Chansey given Pressure
  shows the entry message as Weezing comes in, no extra PP is spent while the
  gas is out, and switching Weezing out prints the exit message followed by
  Chansey's Pressure message again.
- [ ] **Sheer Force with a Life Orb** (2026-10-07, `main-tm-items`): the
  Abilities menu's Sheer Force entry gives a Toucannon holding a Life Orb.
  Against the wild Chansey, Flame Charge costs Toucannon no HP, while Bullet
  Seed and Brave Bird each cost it a tenth of its HP to the Life Orb (Brave
  Bird its own recoil too). Before this fix every move took the recoil.
- [ ] **Element 5's hidden abilities, the Abilities menu's third page**
  (reached from "More abilities" at the end of the second; 16 entries,
  `docs/oxide/test-kit.md` has what each should show). Those with a message:
  Justified, Magic Bounce, Moody, Moxie, Pickpocket (and the item back after
  the battle), Poison Touch and Rattled. Those that change a number: Analytic,
  Flare Boost and Toxic Boost (the foe's hit on your Snorlax grows by a third
  or a half), Heavy Metal and Light Metal (Heavy Slam against Iron Head),
  Multiscale (the hit at full HP is halved), Sand Force and Sand Rush (no sand
  damage; Sandslash moves first in the sand) and Wonder Skin (Growl misses
  about half the time). Friend Guard, and Rattled's answer to Intimidate, need
  a double battle or a switch the kit cannot arrange; they are for normal
  play.
- [ ] **The staples rulings, the Modern rules menu** (its first 19 of 27
  entries; the other eight have their own checks below): Sturdy as a
  Focus Sash, Lightning Rod and Storm Drain immunity, the Intimidate blockers,
  Grass against powder, Electric against paralysis, 1.5x critical hits, Defog
  clearing hazards from both sides and screens only from the target's, Rapid
  Spin's Speed raise, and the rest the menu lists.
- [ ] **Native moves at modern numbers.** Fury Cutter hits three times in one
  turn at 10, 20 and 30 power, and Triple Kick at 20, 30 and 40, each later
  hit able to miss and end the move (Ian, 2026-10-12); Roar and Whirlwind
  never miss.
- [ ] **Fairy.** A Dragon move does nothing to Clefairy or Ralts, a Poison or
  Steel move does double, the summary screen reads FAIRY, and the Pokedex info
  page shows the NORMAL plate (the known gap) rather than garbage. The Poketch
  move tester agrees with the battle engine.
- [ ] **Ghost and Dark hit Steel at neutral** (2026-11-03,
  `overseer-steel-chart`; Ian moved Steel to the later chart). On move set
  45, Crunch and Darkest Lariat into the wild Skarmory show no "It's not
  very effective..." message, and on the Poketch move tester a Ghost or a
  Dark move into Steel shows the plain result, not the weak one. Before the
  change both read not very effective.
- [ ] **Water is not very effective on Ice** (2026-11-03,
  `overseer-ice-levers`; Ian gave Ice a resistance to Water, the Ice
  proposal's first lever). In normal play, a Water move into a pure Ice type
  (Snorunt, Glaceon) shows "It's not very effective...", one into Lapras or
  Cloyster (Water and Ice) does about a quarter of its neutral damage, and one
  into Mamoswine (Ice and Ground) shows neither message. On the Poketch move
  tester, Water into Ice shows the weak result. Before the change a Water move
  was neutral on Ice.
- [ ] **Hail does no damage** (2026-11-03, `overseer-ice-levers`; Ian put
  snow in hail's place, the Ice proposal's second lever). On move set 29,
  Hail prints "It started to snow!", each turn's end prints "Snow continues
  to fall." and neither Mew nor the wild foe loses any HP to it, and five
  turns later "The snow stopped." shows. In a hail fight in normal play
  (Snowpoint Gym, Route 217, or a foe's Snow Warning, whose message now
  says "whipped up a snowstorm!"), no Pokemon loses HP at a turn's end, and
  an Ice Body holder still heals. Before the change every Pokemon but an
  Ice type lost a sixteenth a turn.
- [ ] **An Ice type takes less from a physical hit in hail** (2026-11-03,
  `overseer-ice-levers`, the same lever). In a hail fight in normal play, a
  physical hit on one of your Ice types does about two thirds of what the
  OxiDex calculator shows for clear weather, and what it shows with Hail set;
  a special hit does the clear-weather figure. Before the change the two
  matched.
- [ ] **The Move Relearner and learnsets.** At the Move Relearner, no move name
  clips beyond the eight known ones, descriptions read sensibly in five lines,
  and a new species' moves are listed. Level a Pokemon through a move it should
  learn and confirm the right move at the right level (a wrong widening would
  be wrong for all 667 learnsets). A Rotom in a form, or a Giratina holding the
  Griseous Orb, shows its form's stats.
- [ ] **Soft level caps** (2026-10-29; the Level caps menu,
  `docs/oxide/test-kit.md` has the detail): at a new game's cap of 16, a
  Pokemon at Lv. 16 wins a battle, gets the Exp. message, gains a level to
  17, and keeps levelling from later battles; it is still at its new level
  after a trip into the PC. A Rare Candy on a Pokemon at Lv. 16 lifts it to
  17 and is used up, and more candies keep working. After saving, the
  OxiDex's save bar and the Alpha tab's bar name it as over the cap of 16,
  and a party member at Lv. 16 exactly is not named. The game itself shows
  nothing.
- [ ] **Protect in a row** (Modern rules, `cloud/element6-changes`): King's
  Shield used every turn works the first time, then about one time in two, then
  one in four, with "But it failed!"; Spiky Shield the same. Before the fix
  both worked every turn.
- [ ] **Five recorded hits against the calculator** (the encounter tool, M8):
  during the alpha run, with the battle recorder on, record five ordinary hits.
  The Overseer compares each against the calculator's roll range from the
  recorder's logged stats and HP (Ian, 2026-11-02).
- [ ] **Element 8, hidden abilities and restored items** (the three Modern
  rules entries before "Kaizo move data"):
  "Hidden ability gift" gives a Lv. 15 Litten whose summary reads
  Intimidate, not Blaze; one Rare Candy makes a Torracat that still reads
  Intimidate. "Hidden ability wild" opens with the wild Litten's Intimidate
  lowering your lead's Attack; the flag clears itself after that one use.
  "Items restored": Mew eats its Sitrus Berry after Belly Drum, and has it
  back in its summary after the battle.
- [ ] **The Kaizo move data** (Modern rules, "Kaizo move data";
  `cloud/element4-kaizo-move-data`, Ian's rulings of 2026-09-27). Switch Mew
  in on the first turn. From then the wild Shuckle's Fake Out ("But it
  failed!") comes before Mew's Extreme Speed every turn, though Mew is far
  faster. Minimize says "sharply rose!". Mew's summary shows Minimize at 3 PP.
- [ ] **Infiltrator** (Modern rules, "Infiltrator, Substitute" and
  "Infiltrator, Safeguard"; `main-element5-gaps`). Against the Snorlax, once
  its Substitute is up, Crobat's Cross Poison takes Snorlax's own HP and can
  poison it, Screech lowers its Defense, and Confuse Ray confuses it, with the
  doll still standing. Against the Chansey, with Safeguard up, Toxic badly
  poisons it and Confuse Ray confuses it. And the Geodude of Modern rules'
  "Sturdy" entry shows the new description in its summary: "It survives any
  hit at full HP and 1-hit KO attacks."
- [ ] **The TV's random move** (`main-engine-cleanups`, 2026-10-07), in normal
  play whenever it comes up: the Variety Hour's "Sinnoh Hot Hit Tunes" names a
  real move in its no. 1 song ("...Our Summer of" a move), never "-".
- [ ] **Infiltrator with Mimic and Psycho Shift** (Modern rules, "Infiltrator,
  Mimic"; `main-engine-cleanups`, 2026-10-07). Splash while Snorlax's doll
  goes up and the Flame Orb burns Crobat. Psycho Shift then burns Snorlax and
  cures Crobat, and Mimic copies Substitute, both with the doll still
  standing. Before the fix both failed.
- [ ] **The test kit's late lines** (`main-engine-cleanups`, 2026-10-07): the
  Items menu's Ice Stone, abilities, Mints and Caps, and TMs entries each
  print their own line, not another entry's.

- [ ] **The new species on the field** (the "Sprite heights" entry, with
  `main-sprite-heights` merged). Four wild Pokemon come in turn: Wooloo,
  Rookidee and Fletchling stand on their shadows, and Sinistea hovers a
  little above its own. Run from each. In ordinary play, any new species
  that still floats clear of its shadow, or sinks into it, is worth a note
  with its name.
- [ ] **Element 7, the items** (the "Element 7 items" menu, 27 entries;
  `docs/oxide/test-kit.md`, "The item entries", says what each should show).
  "All new items" first: all 46 and the Ice Stone arrive, each with its name,
  icon, pocket and a description that fits the Bag's box, and the long names
  (Weakness Policy, Gold Bottle Cap, Ability Capsule) fit the summary and the
  give-item messages. Then each held item beside a Pokemon holding nothing;
  the Pixie Plate's Arceus pink in its summary and in battle; the Roseli Berry
  with no number, Check Tag, planting or Poffin in the Bag. From the Bag on a
  party member: the Ability Capsule and Patch (each asks yes or no first), the
  Mints and the Bottle Caps, with the Bottle Cap's stat list and the IV viewer
  showing 31 afterwards. The TM Case check: No. 01, No. 92, HM 01, HM 08 in
  that order, each with its move. Then save, turn the game off and reload: the
  Bag (it grew), a swapped ability, a Mint's stats and a trained IV all come
  back as they were. "Vulpix, Ice Stone": the Ice Stone evolves one Vulpix
  into Alolan Ninetales, the Fire Stone the other into Ninetales, and the
  Alolan one is named A-NINETALS (the form names' check, section 4).
- [ ] **Element 7, for normal play** once the balance track has placed items
  and given trainers theirs (the kit cannot give a foe an item or run a
  double battle): a foe's Red Card dragging out a teammate in a trainer
  battle, a foe's Air Balloon, Eject Button, Rocky Helmet and Weakness Policy,
  and Ability Shield and Covert Cloak in a double battle.

- [ ] **Evolution moves** (the "Eevee with Charm" entry, with `main-evo-moves`
  merged). In the kit ROM only, Sylveon has a stand-in evolution move. One
  Rare Candy evolves the kit's Eevee, and on evolving it learns Moonblast,
  with the forget-a-move prompt if it knows four. The Move Relearner then
  lists Moonblast for it. Since 2026-10-12 fifteen lines outside the kit
  have one; in the ordinary ROM, a Nacli reaching 24 learns Salt Cure as it
  becomes Naclstack, and a Sewaddle evolving into Leavanny learns Slash.
- [ ] **Single-use TMs** (the "Two TMs" entry, with `main-tm-single-use`
  merged). The TM Case shows TM01 x2; teaching it once leaves x1, and a
  second use empties it. An HM is used up the same way and shows its count
  as a TM does, since the HMs became single-use TMs in the TM pass.
- [ ] **Meloetta's forms** (the "Form changers" entry, with `main-meloetta`
  merged). The kit gives a Lv. 50 Meloetta with Relic Song in its first slot.
  In one of the menu's wild battles, switch it in: a Relic Song that hits turns
  it into Pirouette (orange hair, Normal and Fighting, "transformed!"), and the
  next one that hits turns it back to Aria. A Relic Song that misses changes
  nothing. Switched out as Pirouette, it comes back in as Aria. After a battle
  ended with it as Pirouette, its summary shows Aria, Normal and Psychic, and
  Aria's stats.
- [ ] **The move reworks** (`cloud/main-move-reworks`, 2026-10-07; Ian's
  rulings of 2026-10-06), sets 71 to 84 on the move-set menu's third page,
  each against the wild foe it names (`docs/oxide/test-kit.md` has what
  each should show). Hyper Beam and its kin hit with half recoil and no
  recharge turn (71); Blast Burn, Frenzy Plant and Hydro Cannon the same
  with their recoil and status (72); Sky Attack strikes the turn it is
  chosen (73); Dig and Dive strike at once and Chansey's Tackle reaches Mew
  the same turn (74); the two to five hit moves end "Hit 2 time(s)!" to
  "Hit 5 time(s)!", mostly two or three (75), and always five on the Skill
  Link Cloyster (76); Fury Cutter hits three times, each harder (77);
  Spite shows 5 PP (78); Thrash, Petal Dance, Outrage and Uproar strike once
  with no lock and no confusion of Mew (79), and Raging Fury the same with
  its recoil (80); Upper Hand flinches a Rattata that chose Quick Attack and
  fails against Tackle (81); Shell Trap strikes after a Tackle and fails
  after a Swift (82); Burning Jealousy burns a Ninjask only on a turn it
  used Swords Dance (83); Bone Rush shows 100 accuracy and never misses
  (84). Watch the strike animations of Sky Attack, Dig and Dive, which were
  the second halves of two-turn animations: Mew should be drawn whole
  throughout.
- [ ] **Eerie Spell's drain** (set 85 on the move-set menu's fourth page,
  `overseer-eerie-spell`; Ian, 2026-10-14). Switch Mew in on the first turn
  against the wild Chansey, which knows only Softboiled, then use Eerie Spell
  every turn. The first two hits are each followed by "It reduced the PP of
  the wild CHANSEY's SOFTBOILED by 3!", and the third by the same line
  ending "by 1!". Chansey then uses Struggle, and the fourth hit brings no PP
  line. Before the change no hit drained PP.
- [ ] **Burning Bulwark's burn** (set 86 on the move-set menu's fourth
  page, `overseer-eerie-spell`; Ian, 2026-10-14). Against the wild Rattata,
  switch Mew in on the first turn, then alternate Burning Bulwark and
  Splash. When Rattata's Tackle meets the bulwark, "MEW protected itself!"
  is followed by "The wild RATTATA was burned!" and the burn icon on its
  health box; a later Tackle into it brings only "MEW protected itself!",
  as does a Swift. Before the change it was a plain Protect.
- [ ] **Dragon Tail drags after the hit is answered** (set 87 on the
  move-set menu's fourth page, `overseer-engine-dragon-tail`; Ian,
  2026-10-15). Switch the set's Skarmory in on the first turn. The wild
  Chansey's Dragon Tail or Circle Throw hits it, then "SKARMORY's Rough Skin
  hurt the wild CHANSEY!" and "The wild CHANSEY is hurt by SKARMORY's Rocky
  Helmet!" appear, and only then is Skarmory dragged out, which in a wild
  battle ends it. Before the change the drag came first and the battle
  faded out straight after the hit. In normal play (no trainer carries
  either move, so with your own Jangmo-o line from 21, Turtonator from 24,
  Goomy line from 28 or Clobbopus line from 30): in a trainer battle, a foe
  with Rough Skin or Iron Barbs, or holding a Rocky Helmet, hurts your user
  before it is dragged out. The foe dragged in says nothing of its own, no
  Rough Skin and no item, and a dragged-out foe's Red Card or Eject Button
  is never used. Hiker Daniel's Sandshrew on Route 205 South has Rough Skin.
- [ ] **Pickpocket does not steal before a drag** (set 88 on the move-set
  menu's fourth page, `overseer-engine-9b`; Ian, 2026-10-15). Switch the
  set's Mew, holding Leftovers, in on the first turn, then use Dragon Tail
  on the wild Wobbuffet, which has Pickpocket: it is dragged out, which in
  a wild battle ends it, with no "stole" line, and Mew's summary still shows
  its Leftovers. Before the change "The wild WOBBUFFET stole MEW's
  Leftovers!" came first. Take the set again and use Tackle: Wobbuffet
  steals the Leftovers, since no drag follows.
- [ ] **Silk Trap's Speed drop** (set 89 on the move-set menu's fourth
  page, `overseer-engine-gaps`; Ian, 2026-10-29). Against the wild Rattata,
  which knows Tackle and Tail Whip, switch Mew in on the first turn, then
  alternate Silk Trap and Splash. When a Tackle meets the trap, "MEW
  protected itself!" is followed by "The wild RATTATA's Speed fell!"; when
  a Tail Whip meets it, "MEW's Defense fell!" as if Mew had not protected.
  Before the change it was a plain Protect, and both moves were stopped.
- [ ] **Obstruct's Defense drop** (set 90, as set 89). A Tackle into it
  brings "MEW protected itself!" and then "The wild RATTATA's Defense
  harshly fell!", and Mew's next Tackle does clearly more; a Tail Whip gets
  through. Before the change it was a plain Protect.
- [ ] **Corrosion through Baneful Bunker** (set 91, `overseer-engine-gaps`).
  Switch the set's Salazzle in on the first turn against the wild Skarmory,
  which knows only Steel Wing, then alternate Baneful Bunker and Splash.
  When Steel Wing meets the bunker, "SALAZZLE protected itself!" is
  followed by "The wild SKARMORY was poisoned!" and the poison icon. Before
  the change the Steel type was not poisoned. Toxic poisons Skarmory too, as
  the Corrosion entry of the Abilities menu already shows.
- [ ] **King's Shield lets status moves through** (set 92 on the move-set
  menu's fourth page, `overseer-protect-ai`; Ian, 2026-10-29). Against the
  wild Rattata, which knows Tackle and Tail Whip, switch Mew in on the first
  turn, then alternate King's Shield and Splash. A Tackle into the shield
  brings "MEW protected itself!"; a Tail Whip brings "MEW's Defense fell!"
  as if Mew had not protected. Before the change both were stopped.
- [ ] **Burning Bulwark lets status moves through** (set 93, as set 92). A
  Tackle brings "MEW protected itself!" and then "The wild RATTATA was
  burned!"; a Tail Whip gets through ("MEW's Defense fell!"). Before the
  change the Tail Whip was stopped too.
- [ ] **King's Shield's Attack drop** (set 92 again, `overseer-kings-shield`;
  Ian, 2026-11-02: "Give it the Attack drop"). Play set 92 as above. When a
  Tackle meets the shield, "MEW protected itself!" is now followed by "The
  wild RATTATA's Attack fell!", and Rattata's next Tackle that lands does
  clearly less. A Tail Whip still gets through and lowers nothing on
  Rattata. Before the change King's Shield only protected.
- [ ] **A Corrosion holder uses Toxic on a Steel type** (normal play,
  `overseer-protect-ai`; Ian, 2026-10-29). The trainer AI no longer refuses
  a Corrosion holder's Toxic, Poison Powder and the like, a flung Toxic Orb
  or Poison Barb, or Psycho Shift's poison into a Poison or Steel type. The
  kit cannot show it, since a wild Pokemon picks its moves at random, and on
  2026-10-30 no trainer's Corrosion holder knows such a move. When a
  trainer's Salandit or Salazzle with Toxic meets a Steel or Poison type of
  yours, it should use Toxic on it, and the poison icon follows. Before the
  change it never chose Toxic there.
- [ ] **Knock Off on the first turn out** (normal play,
  `overseer-protect-ai`; Ian, 2026-10-29). A trainer's Pokemon with Knock
  Off now favours it from its first turn in battle, against a Pokemon of
  yours that holds an item and has 30% HP or more, about two times in three
  where nothing stronger competes (Ace Trainer Allen's Sableye in Hearthome's gym
  is an early one). Before the change it never had the bonus on its first
  turn, and only about one time in three afterwards. Against a Pokemon
  holding nothing it still avoids Knock Off.
- [ ] **Judgment with the Pixie Plate** (the "Pixie Plate" entry on the
  "Element 7 items" menu, `overseer-signature-moves-2`; Ian, 2026-10-20).
  The first Arceus holds the plate and is pink. Its Judgment on the wild
  Dragonite brings "It's super effective!"; the second Arceus's Judgment,
  with no plate, is a Normal hit with no message. Before the fix both hit
  as Normal, since Judgment's effect script had no branch for the plate.
- [ ] **The move reworks, for normal play** (the kit cannot run them):
  Petal Dance hitting both foes in a double battle; Dig still digging out of
  a cave from the field menu; a trainer's Hyper Beam, Giga Impact or Outrage
  used as an ordinary attack, with no recharge turn and the recoil message.
  Since step 12's teams (2026-10-07) 49 trainers carry one, from Ruin Maniac
  Calvin's Outrage at 33, Skier Bjorn's Giga Impact at 51 and Swimmer
  Glenn's Hyper Beam at 55; Cynthia, Volkner and the Flint and Volkner tag
  no longer do.
- [ ] **The AI rates multi-hit moves on their expected hits** (the kit cannot
  show it, since a wild Pokemon picks its move at random and never runs the
  trainer AI). In a trainer battle against a Pokemon with a two to five hit
  move (Gardenia's team carries Bullet Seed), it should now use that move
  where it is the strongest attack counted over about three hits, where it
  used to rate it as a single 25 power hit and seldom chose it.
- [ ] **The AI rates two-hit and three-hit moves on every hit**
  (`overseer-ai-fixes`, Ian's approval of 2026-10-21; the kit cannot show
  it, for the same reason). Against Barry on Route 203 (the Turtwig
  player's version), his Chimchar knows Ember and Double Kick: lead with a
  Normal type and it should choose Double Kick nearly every turn, since two
  30 power hits at double damage now count twice Ember's worth, where one
  hit counted about the same as Ember and the two were close. Barry's
  Ambipom from Route 209 on leans on Double Hit the same way.
- [ ] **Gauntlets** (`main-gauntlets`, `docs/oxide/gauntlets.md`), on the
  test kit ROM. Take "Route 208, all badges" first, then the Warp menu's five
  gauntlet entries, each of which lands one step from a section's way in; walk
  through it. The trainers are far above the kit's Pokemon, so keep out of
  their sight where the check does not need a fight. In each section, while it
  is open: the Pocket PC says "You can’t use that here yet! / Press on, or beat
  the Trainers here." in the bag; Dig, Fly and Teleport say the same in the
  party menu; an Escape Rope in a cave says it too; and the way back says
  "There’s no turning back now! / Press on, or beat the Trainers here.", after
  which a staircase or warp panel stepped onto walks the player back off it.
  Then, one per entry:
  - Eterna: with a 1F or 2F grunt still unbeaten, take 2F's east stairs
    into 3F's small dead-end room: the Pocket PC still refuses there. Then
    take 2F's other stairs up to 3F's main side: since 2026-10-31
    (`overseer-byron-prep`) the section ends on arrival, so the Pocket PC
    works at once, before Scientist Travon and Officer Moira, and the stairs
    back down no longer refuse.
  - Galactic HQ, two sections since 2026-11-02 (`overseer-hq-pass`,
    `docs/oxide/hq-split.md`). The basement run: the warehouse's stairs
    lead into B2F, and with any of its five trainers unbeaten (B2F's two
    grunts, B1F's grunt, 1F's grunt, Scientist Fredrick) the stairs back to
    the warehouse refuse, and so does the Pocket PC, on B1F, 1F, 2F west
    and 3F west too. Fetch the Galactic Key from B2F's north end: the
    stairs to the warehouse now let you go even with a basement trainer
    unbeaten. Come back in with the key, climb to 3F west and open its
    locked room: the Pocket PC works there, and the stairs back down let
    you go. The tower: key in hand, enter the HQ's front door in
    Veilstone, open the lobby's inner door and take the stairs up to 2F's
    east side. With any of its five trainers unbeaten (2F's grunt pair,
    Scientist Darrius, 3F's grunt pair) the stairs back to the lobby
    refuse, the Pocket PC refuses in the hall and on 3F's east side, and
    the nap room's bed says "There’s no time to rest now! / Press on, or
    beat the Trainers here." without healing. Go on up to 4F: the Pocket
    PC works there, before Cyrus, and the bed heals again if you walk back
    down to it.
  - Coronet 1F: south into the tunnel room, then back north: refused. At the
    far end, out onto the north ledge, the Pocket PC works again.
  - Coronet 3F: up the stairs from 2F, then out onto the south ledge. Fly
    refuses there, although the ledge is outdoors. On the north ledge, the
    cave mouth into the tunnel refuses. Since 2026-10-31
    (`overseer-route-fixes`) the section ends at 5F: with a 3F or 4F grunt
    still unbeaten, go up 4F's third room to 5F, and the Pocket PC works at
    once, before Officers Somnu and Moira, who stand further south.
  - Victory Road: north from the League's gate. The gate refuses. Walk north
    through the one-tile corridor that passes under the long bridge west of
    the middle (x 13, z 26 to 27), then turn back south: the player is turned
    back north with the message. Walking out at the far end, the Pocket PC
    works on the League's side.
  A whiteout inside a section closes it too: the Pocket PC works from the
  Pokemon Center.
- [ ] **Step 10's rewards** (2026-10-07, `main-tm-items`; the table is
  `docs/oxide/reward-placements.tsv`), on the test kit ROM after "Route 208,
  all badges", then the Warp menu's Veilstone. One of each kind:
  - A gift: the roughneck who says Veilstone is the city of stone ends "take
    this Berry!", gives a Sitrus Berry and explains it. Talking again gives
    only the explanation.
  - The TMs sold once: the Department Store's 3F counters list each TM once,
    with all eight badges every one of them. Buy Earthquake (TM26): one copy
    comes, and the counter no longer lists it, after leaving the floor too.
  - The Game Corner challenger: Rocco, beside the coins clerk, battles once.
    Straight after the win, with no talk, two TM32 (Zen Headbutt) come.
    Talking to him again gives nothing more, and the clerk gives no TM.
  - A trainer reward: on Route 215, west of Veilstone, Jogger Scott gives
    TM40 (Aerial Ace) straight after the win.
  - A ball: Route 215's ball that held TM34 holds a Lum Berry.
  A trainer with two rewards is checked in normal play (section 3, Hiker
  Theodore).
- [ ] **(live)** The new moves in the other AI flags (`cloud/main-ai-flags`,
  readiness step 18; the kit cannot show it, since a wild Pokemon never runs
  the trainer AI). No trainer carries any of the 21 routed moves on the
  branch's base, so this waits until a team does (the comb's teams of step 12
  or the trainer pass); `docs/oxide/battle-ai/other-flags-new-moves.md` lists
  the moves and flags. Take one trainer whose flags include Setup First Turn
  and whose Pokemon knows one of that table's routed moves (Hone Claws, Coil,
  Cotton Guard, Autotomize, Noble Roar, Tearful Look or Aurora Veil), and one
  with Check HP and a routed move. Break at the end of
  `TrainerAI_MainSingles` and read `moveScore`, as for Ace Trainer Shannon. On the
  battle's first turn the Setup First Turn move should carry the same +2 as a
  Platinum setup move most turns (about two in three); the Check HP move
  should lose 2 most turns (about four in five) once its user is at 70% HP
  or less. Before the branch neither moved. Compare the change, not the totals,
  since Basic and Expert score the same move too.

## 3. The ordinary ROM, early game (Twinleaf to Hearthome)

- [ ] **30 PC boxes** (`main-30-boxes`, a new game; an older save does not
  load). In Storage, L from BOX 1 goes to BOX 30, and R from BOX 30 back to
  BOX 1; the names run BOX 1 to BOX 30. The bottom screen's box dial scrolls
  through all thirty and wraps between 30 and 1, and the count under each box
  is right, box 30's included. Deposit a Pokemon in BOX 30, open its summary
  from there and back out, then save, turn the game off and load: it is still
  in BOX 30. The PC screen rebuilds its graphics memory, 16 KB larger now, on
  three more paths, and each should come back to Storage cleanly: rename a box
  between 19 and 30, give an item from the Bag to a Pokemon in a box, and
  change BOX 30's wallpaper. After a trainer battle and a save, the OxiDex's
  Sync shows box 30 and the battle log still lists the battle, and
  melonDS-oxide's `http://127.0.0.1:31124/status` reports 30 boxes.
- [ ] **The national listing from the start** (`main-national-dex`). As soon
  as the Pokedex is received, it opens on the regional dex, and its switch
  goes to the national listing, all 652 and the forms, and back. After
  switching, it opens on the listing used last. A species' area map shows the
  same places as before; nothing else changes until the story gives the
  National Dex.
- [ ] **The Pocket PC** (`carry-over`, merged; received in Sandgem; Ian's
  rulings are in `docs/oxide/pocket-pc.md`). From the bag and from the Y
  button, outdoors, in a building and in a cave, it opens a PC with Pokemon
  Storage, Healing Waves, Rare Candy and Misc. (Name Rater APP, Hidden Power
  APP) and nothing else. Rare Candy fills the stack to 999 from any count,
  including 0 and 999. The Hidden Power APP names a type and a power between
  30 and 70. Storage deposits, withdraws and backs out cleanly (the box hang
  in Phase 5 is on this path). A Pokemon Center PC shows Storage, the player's
  PC, Oak's PC, Healing Waves and Misc., with the Hall of Fame in Misc. only
  after the League, and no tutors, Teleport System, Online Shop or resets. No
  trainer ever asks for a Vs. Seeker rematch. The item's icon is a small PC.
- [ ] **The Pocket PC's own lines** (fixed 2026-10-07, `main-tm-items`). The
  menu's fourth entry reads "Rare Candy", not a blank. Choosing it says "Your
  Rare Candy stock was filled to 999.", and the Hidden Power APP says "This
  Pokémon's Hidden Power is the" a type "type, with" a number "power."
  Before the fix the first printed the Pokemon Center nurse's greeting and
  the second "OK, I'll take your Pokémon for a few seconds."
- [ ] Rare Candy chaining works, past the level cap too (soft since
  2026-10-29).
- [ ] With Scorbunny as the starter (fixed 2026-09-27, `fix-rival-starter`):
  Barry leads with Piplup on Route 201 and at every later fight, and Dawn or
  Lucas uses the Turtwig line. With Turtwig, Barry has the Chimchar line; with
  Piplup, Turtwig, and Dawn or Lucas the Chimchar line (Ian, 2026-10-07:
  Scorbunny took only Chimchar's place in the briefcase). The Jubilife TV
  mask, the Veilstone Department Store socialite's mask and the Underground
  Man's doll are the fire starter's.
- [ ] The rival's and the counterpart's starter by name (2026-10-07,
  `main-tm-items`). With Turtwig, Barry's lines on Route 201 and in the
  Sandgem lab name Chimchar, as his team shows. With Piplup, Dawn or Lucas
  names Chimchar in the lab and as a partner, and the catching demo on Route
  202 uses a Chimchar. Before this fix both said Scorbunny.
- [ ] **Step 10's gifts and rewards, early game** (2026-10-07,
  `main-tm-items`). Each giver names and explains what it now hands over:
  Rowan a Roost TM, Roark Toxic, the Oreburgh Gate man Block (and, seeing
  the Coal Badge, says Pokemon can now smash boulders), Cynthia in Eterna two
  Brick Breaks, Gardenia two Secret Powers, the Eterna Condominiums 2F woman
  a Lum Berry, the Floaroma middle house woman two Defog HMs, the Route 204
  teacher a Lum Berry, and Fantina two Strength HMs. No line names the old
  item. On Route 206, Hiker Theodore gives TM03 (Water Pulse) and then TM28
  (Dig) straight after the win, and nothing more when talked to again.
- [ ] The Kaizo move data in normal play (`cloud/element4-kaizo-move-data`):
  TM08 Bulk Up shows 3 PP in a summary, and Screech 5; a Pokemon's Cotton
  Spore in a double battle lowers both foes' Speed; Drill Peck and Dragon
  Claw land critical hits noticeably more often than Peck or Scratch.
- [ ] Roark's new team (Ian, 2026-10-13; `docs/oxide/roark-redesign.md`):
  Naclstack leads and lays Stealth Rock; against a healthy Pokemon it uses
  Salt Cure ("is being salt cured!", then a loss every turn, a quarter of
  the HP on a Water type), not again on one already salted, and below about
  70% HP it uses Recover. A Water move aimed at Lileep is drawn in by Storm
  Drain and raises its Sp. Atk. Sandshrew moves before nearly everything in
  the gym's sand, and its Rapid Spin raises its Speed. Cranidos's Mold
  Breaker shows when it hits through Sturdy.
- [ ] Gardenia's new team (Ian, 2026-10-13; `docs/oxide/gardenia-redesign.md`):
  six Pokemon, Solrock leading, and Drought's sun lasts the whole fight.
  Exeggutor's Harvest gives back its Occa Berry each turn in the sun, so its
  Natural Gift (Fire) comes again and again. Cherrim's Flower Gift shows in
  the sun, and Lumineon (Chlorophyll) moves before anything in the box. Each
  member holds a different resist berry, and a two-hit move into one (Golbat's
  Dual Wingbeat into Breloom's Coba Berry) is weakened on its first hit only.
- [ ] Level caps: after beating Roark the badge message plays as before and
  the OxiDex's save bar reads Gardenia's split, cap 26. The caps are soft
  (2026-10-29), so nothing in battle or from a candy stops at them.
- [ ] The options menu reads UNLOCK FPS, with OFF and BATTLE only
  (`main-60fps`), and its description says "Unlock the frame rate in battle,
  so / battles run at twice the speed." A save made with ALWAYS shows BATTLE,
  and the overworld runs at normal speed.
- [ ] Held items come back after battle (element 8): give a Pokemon an Oran or
  Sitrus Berry, let a trainer's Pokemon bring it below half so it eats the
  Berry, and after the battle its summary shows the Berry again. The same for
  a Focus Sash that saved it. The kit's "Items restored" entry shows it first.
- [ ] Battle style is always Set (element 8): the options menu shows SET
  highlighted and left and right do not move it, and when a trainer's Pokemon
  faints the game sends the next one out without asking whether you want to
  switch.
- [ ] Shinx's ability is always Rivalry, never Intimidate; Bidoof and Starly
  hatch in about 255 steps, down from about 3,825.
- [ ] Answering yes to "use another Repel?" works (the one carried-over thing
  that was broken and is fixed).
- [ ] A walk through a few bulk-generated maps, the gift houses first.
- [ ] Trainer gender: the ability and gender nibble is read as 1 male, 2 female,
  which is a guess no Route 202 trainer exercises; swap it if anything reads
  wrong.
- [ ] Element 6's absorber switch (`cloud/element6-changes`), Picnicker Siena
  on Route 205 South (since step 12's teams, a Plusle at 23 leading and an
  Electrike with Lightning Rod behind it): hit Plusle with an Electric attack
  that does not knock it out, from a Pokemon her Spark is not super effective
  against, since a super-effective move of her own skips the switch two
  times in three. On about half such turns she switches to Electrike instead
  of attacking; before the change she never did. Take several tries before
  calling it.
- [ ] **(live)** Rapid Spin's clearing (`cloud/element6-followups`), Bug
  Catcher Donald in Eterna Forest (a Pineco at 23 with Rapid Spin, Expert
  flag): seed Pineco with Leech Seed (a Cherubi learns it at level 7), break at
  the end of `TrainerAI_MainSingles` and read `moveScore`. Rapid Spin reads 2
  higher than on the turn before the seed, give or take the 1 its Speed raise
  earns on half the turns. Keep a Ghost type out of the front, since Rapid
  Spin clears nothing into one.
- [ ] Honey trees at one badge: slather a tree and check the species and levels
  against table 1 of `res/field/encounters/encounters_honey_tree.json`. The
  Munchlax trees are gone.
- [ ] Valley Windworks: the Drifloon balloon no longer appears.
- [ ] The Hearthome Fan Club member only says goodbye, with no starter gift.
- [ ] The starter's summary reads met at "Rowan's Briefcase", not Route 201.
- [ ] The Underground is closed: the Underground Man in Eterna says the
  tunnels are sealed off and gives nothing, and no Explorer Kit is ever in
  the Bag. After the Bicycle, Eterna's south exit (to Cycling Road) and west
  exit are open, with no woman stepping in; talking to her gives the sealed
  tunnels line. In Oreburgh's Mining Museum the fossil researcher offers to
  revive a fossil without the kit (once a fossil can be had).
- [ ] A trainer's hidden ability: in the Eterna Galactic building, 3F, the
  grunt's level 25 Snover sets hail as it enters (Snow Warning, its hidden
  slot, through the party's ability 3; 20 trainers use it since aa3bbc3356).
- [ ] Route 207: after Mira is found in Wayward Cave, the woman who asked for
  her says thank you and gives no evolution stones; her first line no longer
  promises any.
- [ ] **No Lucky Egg on Route 207** (`overseer-route-fixes`, Ian,
  2026-10-31). After the battle with Lucas or Dawn at Mt. Coronet's mouth,
  there is no "choose a hand" menu and no item: Dawn says "I've got
  something nice for you." (Lucas: "...with a neat tool. I'll share it with
  you."), then asks about the Pokétch and gives the Dowsing Machine app as
  before, and the bag holds no Lucky Egg. The Pocket PC from Sandgem still
  works.
- [ ] **Lucas and Dawn 2's tune** (`overseer-ld2-tune`, Ian, 2026-11-02;
  `ld2-tune.md`). On a real save at the battle at Mt. Coronet's mouth, at or
  under the honour cap of 31: Umbreon leads and uses Foul Play, not Payback.
  If one of your Pokemon has used Curse, Foul Play still hits it about as
  hard as before the Curse, not less. For a Piplup player, Monferno comes
  last and has Grass Knot, not Rock Slide (it takes a Rock or Ground type
  such as Onix in one hit). Note how many of your Pokemon faint; the target
  was about 90 to 94 percent won, and Ian has said a slightly easy fight is
  acceptable.
- [ ] Wayward Cave 1F's Ice Stone (Ian, 2026-10-13): in the far northwest,
  walking between Camper Diego and Picnicker Tori starts one battle against
  both, and the ball in the nook behind them gives an Ice Stone, not a
  Revive. Used on a Vulpix, it evolves into Alolan Ninetales.
- [ ] The base ROM's overworld sprites and the teleporting Abra's removal
  (`carry-over` and `carry-over-abra`, merged): no Abra stands outside Sandgem's
  Pokemon Center or in any other town, on Routes 207, 221 or 224, on Mt.
  Coronet or Stark Mountain, or in Turnback Cave. The gym shortcut Abra still
  stand at the entrance and by the leader of the Canalave, Pastoria,
  Snowpoint, Veilstone and Sunyshore gyms, draw as an Abra, and face and
  turn properly when talked to. Later in the game, May at the Resort Area,
  Steven in Stark Mountain's first room, and Ethan and Red on Mt. Coronet's
  north and south slopes draw as themselves.
- [ ] **The colour variation** (the base ROM's hue shift, `carry-over-hue`,
  merged): each Pokemon's colours are turned a little, up to about 20
  degrees of hue either way, by its personality. Several Starly or Bidoof on
  Route 201 differ slightly from one another, as the foe's front sprite and as
  your own back sprite. One caught Pokemon shows the same colours in battle,
  in move animations that draw a copy of it, on its summary, in the PC's
  preview, through its evolution scene, in the Rock Smash and Cut cut-ins, and
  in the Hearthome contest. The Pokedex, the party and box icons, the starter
  choice, Rowan's introduction and the Great Marsh binoculars keep standard
  colours, and so does a Substitute doll (the base ROM tinted the doll).
- [ ] A species added by Oxide (any of the 159, or Meloetta) entered in the
  Hearthome Super Contest draws its own sprite. Contests draw from Diamond and
  Pearl's sprite archive, which stops at Arceus; before the fix of 2026-09-27
  these species read past its end.
- [ ] The pick-list retypes (`main-retypes`), whenever one of them turns up,
  wild, a trainer's or the player's: its summary and the battle's type
  effectiveness follow the new types. Charizard Fire/Dragon, Ninetales
  Fire/Fairy, Electivire Electric/Fighting, Larvitar and Pupitar Dark/Ground,
  Tyranitar Dark/Rock, Sceptile Grass/Dragon, Masquerain Bug/Water, Trapinch
  Bug/Ground, Vibrava Bug/Flying, Flygon Bug/Dragon, Milotic Water/Dragon,
  Glalie Ice/Rock, Luxray Electric/Dark, and Uxie, Mesprit and Azelf
  Psychic/Fairy. The Pokedex's info page shows the NORMAL plate for Fairy, the
  known gap in Phase 4's Fairy entry.
- [ ] The box deposit hang is gone (`main-box-hang`, 2026-09-30): at a
  Pokemon Center PC and with the Pocket PC, open Deposit, back out with B and
  again with the on-screen exit; each returns to the PC menu. Then Withdraw
  and Move Pokemon the same way, and a Pokemon's ability shows in the storage
  screen's preview as before.
- [ ] Fossils wait for Cycling Road (`main-production`, Ian, 2026-09-30).
  With a Root, Armor or Skull Fossil from Oreburgh Mine B2F, talk to the
  researcher in the Mining Museum before riding Cycling Road: he greets you,
  says his machine's parts come from Eterna by way of Cycling Road, and
  revives nothing. Ride down Cycling Road into its south gate, come back, and
  he offers to revive it as before (level 20, the next time you talk to him).

- [ ] **Mandatory fights, Roark's split** (`overseer-mandatory-early`, Ian,
  2026-10-29; `docs/oxide/mandatory-fights-early.md`). Walk the story path
  without dodging anyone. Each trainer below should see you and walk up
  before you can pass, and after the battle the way on is still open with the
  trainer standing where it was:
  - Youngster Sebastian, Route 203, one step north of where he stood, looking
    south across the path a few steps west of the turn north to Oreburgh
    Gate.
  - Lass Madeline, Route 203, in the grass at the west edge of the passage
    north to Oreburgh Gate, looking east across it; Lass Kaitlin still
    wanders below her and should not join her battle.
  - Picnicker Diana, Oreburgh Gate 1F, one step north of where she stood,
    looking south down the column every way east crosses.
  - Camper Curtis, Oreburgh Gate 1F, one step east of where he stood, looking
    north; he and Diana are fought one at a time.
  - Worker Mason, Oreburgh Mine B2F, beside the Machop at the foot of the
    shaft down from B1F, looking west along the row the way on crosses.
    Roark's scene further in plays as before (he walks off east after the
    talk).
- [ ] **Mandatory fights, Gardenia's split** (`overseer-mandatory-early`,
  Ian, 2026-10-29; `docs/oxide/mandatory-fights-early.md`). As above, one
  trainer at a time:
  - Lass Samantha, Route 204 South, at the west edge of the narrow stretch
    south of the Ravaged Path, looking east across it.
  - Twins Liv and Liz, Route 204 North, side by side at the west edge of the
    path north into Floaroma, looking east; they fight as their usual double.
  - Psychics Kody and Rachael, Eterna Forest, facing each other across the
    passage north towards the exit, with Cheryl along; one double with her as
    your partner, as before.
  - Fisherman Joseph, Route 205 South, on the bank beside the south end of
    the bridge to Eterna Forest, looking west across its foot. He is no
    longer on Route 205 North's piers.
  - Fisherman Andrew, Route 205 South, on the bank beside the north end of
    the same bridge, looking east across its top, fought after the Valley
    Windworks once the grunts there are gone. Before the Windworks, stepping
    onto the bridge still has the grunts push you back with no battle from
    Andrew. He is no longer on Route 205 North's piers either.
- [ ] **Mandatory fights, Fantina's split** (`overseer-mandatory-fights`,
  Ian, 2026-10-29; `docs/oxide/mandatory-fights.md`). Walk the story path
  without dodging anyone. Each trainer below should see you and walk up
  before you can pass, and after the battle the way on is still open with the
  trainer standing where it was:
  - Hiker Kevin, Route 207, at the east edge of the way in from Cycling
    Road; he looks west across it.
  - Battle Girl Helen, Route 207, a few steps west of the Mt. Coronet
    entrance, looking south down the column every way to it crosses; she
    should be fought alone (Hiker Justin should not join her) and before
    Lucas or Dawn's scene at the entrance, and that scene plays as before
    (they walk in from the west and leave the same way).
  - Aroma Lady Hannah, Route 208, in the grass just east of where the
    mountain path opens into the flower field; she looks west at the opening.

## 4. The ordinary ROM, mid-game

- [ ] **Solaceon's north house** (2026-10-07, `main-tm-items`): only the old
  woman and the lass, who talk about the Day Care's Eggs. The Utility Stop's
  three vendors, selling Berries, evolution items, Heart Scales, herbs and
  shards, are gone. The Survival Area's south house likewise holds only the
  Black Belt, who gives TM25 (Thunder) once; its Utility Stop greeter and
  vendors are gone too.
- [ ] **Barry 3 at the Route 209 gate** (`overseer-barry-pool`, `barry-pool.md`,
  "The sets"), after Fantina, with the party at or under the honour cap of
  36. Barry brings six, led by Staraptor at 34 (Primeape, Snorlax and the
  partners at 34 and 35, his starter's final at 36): with a Turtwig, Infernape
  beside Serperior and Greninja; with Scorbunny, Empoleon beside Serperior and
  Turtonator; with Piplup, Torterra beside Greninja and Turtonator. Note
  whether Staraptor's Intimidate shows on entry, whether Primeape uses Bulk Up
  when it comes in on a Rock or Steel Pokemon of yours, whether Snorlax's
  Curse and Rest (with its Chesto Berry) and the ace's setup move come up, and
  how many of your Pokemon faint.
- [ ] **Route 214's gate waits on the Cobble Badge** (`overseer-route214-gate`,
  Ian, 2026-10-31, a vanilla fix). In the gate south of Veilstone, a
  policeman stands at the top of the corridor, beside it on the east. Before
  Maylene's badge, stepping into the corridor makes him show a "!" and say
  "Sorry, I can't let you through. The road ahead is badly chewed up. Only
  Trainers with Veilstone's Gym Badge may go on to Route 214.", and the
  player steps back north, on each of the corridor's three columns; talking
  to him gives the same line. After the badge the corridor is open, nothing
  stops the player, and he says "Ah, that's Veilstone's Gym Badge. Go on
  through, and mind your step!" On the test kit: a new kit game's Veilstone
  warp (no badges) for the first half; then "Route 208, all badges", Fly
  back to Twinleaf, and the bedroom's Veilstone warp again for the second.
- [ ] **The Veilstone tag battle, Officers Tyche and Hermes** (`overseer-tyche-hermes-1`,
  `tyche-hermes-1.md`), after Maylene's badge, with the party at or under the
  honour cap of 42, which runs to Barry 4 (their aces are at 41). The north warehouse grunt is a female grunt; the scene's
  lines read "Tyche:" and "Hermes:", and Hermes says "And make ourselves
  scarce." Lucas or Dawn (the counterpart of the other gender) brings six,
  led by Umbreon, with Scyther and the starter line yours beats at 41. The
  officers bring five each: Tyche's Golbat, Murkrow, Ariados, Weezing and
  Haunter, Hermes's Electrode, Mightyena, Seviper, Sharpedo and Dugtrio.
  Note how often Tyche's side protects (Ariados's Silk Trap and Mightyena's
  Obstruct should read as protecting itself), whether Hermes's Pokemon use
  Earthquake or Bulldoze while Golbat, Murkrow, Weezing or Haunter stand
  beside them and hold back beside Ariados, whether Dugtrio's Arena Trap
  stops a switch, and how many of your Pokemon faint. Afterwards, Tyche at
  Spear Pillar says "The toughest of all the officers!" when beaten.
- [ ] **Pastel Veil and Unnerve** (`main-element5-gaps`), whenever they come
  up, since the kit cannot run a double battle or give a foe an item. A
  Galarian Rapidash (Pastel Veil) sent in during a double battle beside a
  poisoned partner cures it: "{partner} was cured of its poisoning!", and the
  poison icon goes. A Pokemon of yours holding a type-resist Berry (an Occa
  and the like) takes a super-effective hit in full, the Berry unused, while a
  foe with Unnerve (Rookidee's and Joltik's lines have it) is out.
- [ ] **Field moves by badge** (`main-field-moves`), with no HM in the bag and
  no Pokemon that knows the move, as each badge comes. After Roark, a
  breakable rock offers Rock Smash; after Gardenia, a small tree offers Cut;
  after Byron, a boulder offers Strength and moves; after Wake, facing water
  offers Surf; after Candice, a rocky wall offers Rock Climb and the climb
  finishes; after Volkner, a waterfall offers Waterfall up, and surfing into
  one from above goes down. Each shows the first Pokemon in the party that is
  not an Egg using the move. Before its badge, each obstacle gives its usual
  "a Pokemon may be able to" line and nothing else. In the party menu, every
  Pokemon lists FLY after Maylene, SURF after Wake and DEFOG after Fantina,
  under the field moves it knows; FLY opens the map, and SURF and DEFOG work
  where they apply. After Rock Climb or Waterfall, walk about for a minute:
  nothing in the field should misbehave (the base ROM's scripts corrupted the
  field code there before this). The test kit's Warp menu, "Route 208, all
  badges", gives all eight badges and lands at a rocky wall two tiles from
  water with a waterfall, so Rock Climb, Surf, Waterfall both ways and the
  menu's FLY, SURF and DEFOG can be checked there first.
- [ ] **Surf waits on Cyrus at Celestic Town** (Ian, 2026-10-31), in normal
  play: with the Fen Badge but before Cyrus is beaten in Celestic's ruins,
  facing water offers nothing, the party menu lists no SURF unless a
  Pokemon knows it, and a Pokemon that knows Surf is refused with "can't be
  used here". Straight after the win over Cyrus, all three work. The test
  kit's "Route 208, all badges" marks Celestic's story done, so Surf works
  there.
- [ ] **Iron Island before Byron's gym, and Barry at the library**
  (`overseer-route-fixes`, then `overseer-byron-prep`, Ian, 2026-10-31). In
  Canalave, before Iron Island, walk into the gym and take one step north
  from the door: the Gym Guide shows "!" and says "Whoa, hold it right
  there, champ-to-be! Byron only takes challengers who've proven themselves
  on Iron Island. Ask the sailor at the harbor to take you there, then come
  back!", and the player steps back south. Try it from each end of the row
  inside the door too. The sailor at the harbor sails to Iron Island, Riley
  meets the player outside, and the island can be walked down to B2F with
  no badge check on the way. After Riley's tag battle on B2F is won (with
  his egg taken, or refused for a full party), the gym lets the player
  through. Then, with Byron beaten, Barry stands at the library door; he says
  "Too slow!" and goes in, and the library's scene on 3F plays as before. His
  other line ("Aww, you haven't gone to Iron Island, have you? You've got to
  toughen up there first, like I told you!") should no longer be seen, since
  the gym cannot be won before the island.
- [ ] **The Pal Park partner double** (`overseer-byron-scripts`, Ian,
  2026-10-31; `byron-scripts.md`). After Cyrus at Celestic, Surf south from
  Sandgem over Routes 219 to 221 and walk into Pal Park's lobby. Oak's scene
  plays as before and he leaves by the door. Straight after it, the player
  walks two steps north (one step west too, from beside the door), Lucas or
  Dawn calls out and walks in by the door to stand beside the player, and
  talks about the park's Pokemon from other regions. Two Galactic grunts,
  named only "Officer", walk in behind and stand in front of the pair, and
  the tag battle starts beside the counterpart of the other gender to the
  player. Check that the partner's ace is the starter the player's starter
  beats (Empoleon for a Turtwig player, Torterra for Scorbunny, Infernape
  for Piplup), at 49. On the win the officers run out by the door, the
  counterpart says the park's Pokemon are safe and leaves too, and the
  lobby's desk works as before. Leave and come back in: nothing plays again.
  Try once from a save that saw Oak's scene before this ROM: the double
  plays on the next entry, from the door.
- [ ] **Barry on Canalave's bridge waits for the Pal Park double**
  (`overseer-byron-scripts`, Ian, 2026-10-31). Before the double is won,
  walk west onto Canalave's bridge from Route 218's side: Barry runs in,
  says "Have you been to Pal Park yet?" and that Team Galactic is snooping
  around there, the player steps back east, and Barry walks back west and
  goes. No battle starts, and the gym and the harbor's sailor cannot be
  reached. Try every row of the bridge's four. After the double, Barry
  stops the player as in vanilla and battles; his win line sends the player
  to Iron Island.
- [ ] **Eterna's Oak waits for the Hall of Fame** (`overseer-byron-scripts`,
  Ian, 2026-10-31). After seeing Pal Park's lobby, talk to Prof. Oak in
  Eterna City's south house before the League: he asks how the Pokedex is
  going and to come back after the Hall of Fame, and gives no Upgrade. No
  Articuno, Zapdos or Moltres roams (the Pokedex's area map shows none).
  After the Hall of Fame he gives the Upgrade and sets the three roaming,
  as in vanilla.
- [ ] **(live)** The Weather flag's fix on Ace Trainer Shannon's first turn
  (Route 221, optional; a Weather-flag trainer whose Victreebel leads with
  Sunny Day and no weather ability, and keeps it in the comb's draft): break
  at the end of `TrainerAI_MainSingles` and read `moveScore`. Sunny Day
  carries the flag's +5 and Solar Beam, Sludge Bomb and Sleep Powder do not;
  before the fix all four did (compare the +5, not the gap). No trainer who
  leads with Rain Dance keeps it through the comb, so this one check covers
  the fix, which Camper Zackary's Castform and Gardenia's Cherrim used to.
- [ ] Honey trees at five badges: check against table 5.
- [ ] Element 6's fixes of 2026-09-30 (`main-element6`), whenever one comes up; none needs a
  set-up of its own. A trainer never aims a status move Magic Coat would bounce at a Pokemon
  of Ian's with Magic Bounce (Natu, Xatu or Espeon with its hidden ability) once it has shown
  it; a trainer's Infiltrator Pokemon still uses sleep, poison or paralysis moves through
  Ian's Safeguard; a trainer's Mold Breaker Pokemon treats one of Ian's holding an Ability
  Shield as keeping its ability (an Earthquake is not aimed at a shielded Levitate holder).
- [ ] Double battles, once a trainer uses these moves in one (none does yet:
  Ace Trainer Catherine in Fantina's gym has Flame Burst, in a single battle;
  `cloud/element4-partial-moves`): Flame Burst hits its target's partner for
  a sixteenth of its HP with "The bursting flame hit ...!"; Teatime's target
  screen shows every battler, as Haze's does, and it feeds every Pokemon on
  the field its Berry; Core Enforcer leaves the ability of a foe that has not
  moved yet alone.
- [ ] **The gauntlets in a real run** (`main-gauntlets`), as each comes up:
  the Eterna building, Galactic HQ (entered from the warehouse), Mt. Coronet
  on the way to Spear Pillar, and Victory Road. From each section's way in,
  the Pocket PC refuses until its trainers are beaten or you move on, and
  nothing shuts you in: the way forward always opens. Note any stretch that
  felt like a gauntlet but let you heal, or refused where it should not.
- [ ] The Pocket PC in places vanilla's Vs. Seeker never reached, now that it
  works everywhere but a gauntlet: the Great Marsh, the Underground, the
  Distortion World, and the Battle Frontier's lobbies. Each should either open
  the PC and return cleanly or refuse; note anything that breaks the area's
  own rules (healing mid-challenge, losing Safari Balls).
- [ ] Iron Island: Riley's egg hatches as a random species, one of eight lines.
- [ ] Snowpoint City: Mindy takes a Snover and gives a Suicune, which is shiny.
- [ ] Route 210 South: talk to the Black Belt the base ROM placed at x 570,
  z 535. His event runs script 13 and the map's script file has 8 (the script
  index, 2026-09-27), so he may hang or crash the game; if he does, he becomes
  an open bug. Save first.
- [ ] The colour variation in eggs and trades: Riley's egg (or any Day Care egg) is
  tinted like the Pokemon inside it while it hatches, and the hatched Pokemon
  shows the same colours on its summary. In Mindy's trade the Snover and the
  Suicune each keep their colours from the send screen, through the wormhole
  (where Oxide goes one step past the base ROM), to the arrival.
- [ ] **(live)** Worker Jackson's Wormadam-Trash (level 49, Relaxed, every IV 27)
  shows 131 HP, 85 Attack, 122 Defense, 85 Sp. Atk, 111 Sp. Def and 47 Speed.
  The comb's draft for Jackson drops it; if that lands first, the Volkner
  rematch's Rotom-Mow in section 5 is the form check left.
- [ ] Galactic HQ, Saturn: the battle opens with "The dimensions became
  distorted!", the slower Pokemon moves first all fight, "The twisted dimensions
  returned to normal!" never appears, a Trick Room from either side fails, and
  Saturn's AI never chooses it.
- [ ] **(live)** Element 6's Phase 4 catch-up (`docs/oxide/battle-ai/README.md`),
  in Volkner's battle: lead with a Lightning Rod Pokemon (Electrike's line or
  Rhyhorn's), break at the end of `TrainerAI_MainSingles` and read
  `moveScore`. Every Electric attack reads 12 or more below its score against
  another lead, and Thunder Wave, if he has it, 10 below. Until the battle has
  recorded the ability the AI guesses between the species' two, so the drop
  shows on about half the turns; take several turns before calling it.
- [ ] Element 6's absorber switch, the VANILLA FIX part: Collector Brady
  (level 28, Kangaskhan first, a Dry Skin Parasect on his bench) switches to
  Parasect on about half the turns his Kangaskhan takes a Water attack that
  does not knock it out; vanilla never did. Attack from a pure Water type, so
  Kangaskhan's Hammer Arm is not super effective, which would keep it in two
  turns in three.
- [ ] Hyper Voice into Soundproof (a VANILLA FIX): against Ace Trainer Skylar
  (Stark Mountain, her Exploud at 62), lead with a Whismur-line Pokemon whose
  summary shows Soundproof, its second ability. Her Exploud never chooses
  Hyper Voice.
- [ ] Level caps through the story: beating Gardenia lifts the cap to 33,
  Fantina to 39, Maylene to 44, Wake to 53, Byron to 56, Candice to 60, Saturn
  at Galactic HQ to 65, Cyrus in the Distortion World to 68, Volkner to 71
  (the Barry split: Victory Road, the Fight Area and the rival fights stay at
  71), and walking into Aaron's room, as its door shuts, to 78. Leaving the
  League before the Elite Four keeps the cap at 71.
- [ ] No gift clown anywhere: the houses in Sandgem, Jubilife (south house 1F),
  Oreburgh (middle house), Floaroma Town (middle house), Floaroma Meadow,
  Eterna (condominiums 1F), Solaceon (north-east house), Veilstone (north-east
  house), Pastoria (north house) and Canalave Library 2F, and the Restaurant on
  Route 213, have no clown; everyone else in them talks as before (the man
  in Veilstone's north-east house gives nothing since 2026-11-02, the check
  below).
- [ ] The new grass (rustle on stepping in it, everywhere): Amity Square's lawn north-east of the pond (x 33 to 43, z 27 to 29) and Verity Lakefront's fenced lawn (x 85 to 95, z 846 to 850) give wild encounters from their tables; in Amity Square a battle with the walking partner out behaves normally. Sandgem's lawn by the beach road, Jubilife's fountain garden, Floaroma's north bed and Solaceon's lawn by the Day Care give encounters from their towns' new tables. Walking the Verity Lakefront lawn before the starter gives no encounter.
- [ ] The battle backdrop on the new grass (`main-production`, Ian's open bug
  of 2026-09-30): a wild battle in Sandgem's, Jubilife's, Floaroma's or
  Solaceon's grass shows the route backdrop over a grass platform, as on Route
  201, not the town's indoor-looking arena; Amity Square and Verity Lakefront
  look the same as ever. A trainer fight on a town's paved ground (the
  Galactic pair in Jubilife with Dawn) keeps the town backdrop.
- [ ] A Burmy in a Sandy or Trash cloak evolves into a Wormadam with Anticipation, not Snow Cloak.
- [ ] The man in Veilstone City's north-east house gives nothing
  (`overseer-elekid-gift`, 2026-11-02): talking to him, once or again, shows
  only "Team Galactic's building bugs me so much, I can't sleep well. It's
  so bizarre, like a robot that's about to start moving.", with no yes or no
  question, no Pokemon and no PORYGON or ELEKID named; the woman beside him
  still talks about the building's thorny things. On a save that took the
  Elekid before this ROM he says the same.
- [ ] Route 222's grass gives a wild Electivire at level 40 now and then
  (`overseer-elekid-gift`, 2026-11-02; 10%, in Toucannon's old slot), and
  no Toucannon.
- [ ] Fuego Ironworks: inside the building the location reads Ironworks Hall (anything received there is met at
  Ironworks Hall, and the journal says "Departed from Ironworks Hall" on leaving); the yard still reads Fuego Ironworks.
- [ ] The Lost Tower: stepping in from Route 209 shows "Lost Tower" in the indoor window, with no new window between
  its floors; a Pokemon caught on any floor is met at Lost Tower; leaving it puts "Departed from Lost Tower" in the
  journal; stepping back out shows "Route 209", and a catch on the route is still met at Route 209.
- [ ] Fomantis evolves into Lurantis at level 34.
- [ ] A Dusk Stone has no effect on Polteageist; on Sinistea a Dusk Stone
  makes Polteageist and a Leaf Stone makes Sinistcha. Galactic HQ B2F: the nine stone balls around the Galactic Key
  (x 19 to 22, z 3 to 6) are gone; the Galactic Key, TM36 and the Secret Key
  balls are still there. Once taken, the Secret Key ball does not come back
  the next day. Stark Mountain room 2 has no fossil balls at all.
- [ ] Oreburgh Mine B2F holds three fossil balls, the Armor, Skull and Root
  Fossils, and none comes back the next day once taken; there is no Helix,
  Dome or Claw Fossil and no Old Amber (its ball holds an Everstone). Taking
  the Armor Fossil does not change what the Sunyshore north-east house's
  visit-tomorrow NPC says.
- [ ] Ian's stone plan: no stone at Fuego Ironworks (the Fire Stone ball),
  Stark Mountain room 2, Route 230, Route 229 (by the Resort Area), Great
  Marsh 3, Route 225 (neither the hidden Leaf Stone nor the Dawn Stone ball),
  Mt. Coronet 4F rooms 1 and 2, or Route 210 north; the hidden item on Route
  212 south is a Shiny Stone, and the ball on Oreburgh Mine B2F an Everstone.
  The Dowsing Machine finds nothing where those stones were. Fuego Ironworks'
  workers and Route 225's trainers and berry soil behave as before.
- [ ] Route 212 (north and south): a wild Shellos or Gastrodon is the pink West
  Sea form.
- [ ] The classic starters as rare finds: Squirtle by day on Route 205 north,
  Charmander in the grass of Route 211 west (a 5% slot), Mudkip on Oreburgh
  Gate B1F (a 5% slot), Treecko in the morning and Torchic by day on Route 204
  north.
- [ ] No evolution waits on friendship: Pichu, Cleffa, Igglybuff, Togepi and
  Azurill evolve at 10, Buneary and Chingling at 20, Riolu at 28, Luvdisc at
  30, Munchlax at 36, Golbat and Chansey at 40; Budew only on a level-up in
  Eterna Forest (the Moss Rock) and Snom only on Route 217 (the Ice Rock); a
  Sun Stone makes Eevee an Espeon and a Moon Stone an Umbreon.
- [ ] The form species have names (`main-form-names`), not "-----". A wild
  Alolan Ninetales on Route 216 or 217 appears as "A wild A-NINETALS
  appeared!", and its name reads A-NINETALS whole, not cut short, in the
  battle HP box and, once caught, in the party, the summary and the PC. The
  National Dex lists it by that name, and the alphabetical sort puts it with
  the A to C group. The other eleven are G-WEEZING, G-RAPIDASH, G-MR. MIME,
  G-ARTICUNO, G-ZAPDOS, G-MOLTRES, M-GYARADOS, M-LOPUNNY, H-SLIGGOO, H-GOODRA
  and ZYGARDE-10. A Pokemon already caught as "-----" in an older save keeps
  that nickname until the Name Rater in Eterna City renames it.
- [ ] Snowpoint City: fishing gives the species of
  `res/field/encounters/encounters_snowpoint_city.json` for each rod.
- [ ] Snowpoint ferry, before Galactic HQ: the sailor refuses with the line
  about Team Galactic. After HQ it sails, and the first voyage plays Cynthia's
  scene.
- [ ] Fight Area without the Beacon Badge: the rival walks you to Volkner and
  Flint, Volkner turns the challenge down, the rival says he will wait, Buck
  introduces himself and leaves in a fade. Route 225 is open. Talking to the
  rival by the Frontier gate gives his "still don't have Volkner's Badge"
  line. Buck is on Route 227, and not also at the Fight Area.
- [ ] Fight Area with the Beacon Badge: talking to the rival starts the tag
  battle, and afterwards the Palmer scene plays, without Buck's part if you
  first arrived without the badge. Arriving with the badge the first time
  plays vanilla's whole scene, Buck included.
- [ ] No Life Orb or Choice item reaches the player (Ian, 2026-10-13): the
  item ball outside Stark Mountain gives a PP Up, and the man in Celestic
  Town's northwest house gives BlackGlasses from 4:00 to 19:59 and Wise
  Glasses at night, never a Choice Specs.
- [ ] Manaphy's Tail Glow (Ian, 2026-10-31): the Pokemon Mansion's egg hatches
  into a Manaphy that does not know Tail Glow; it learns it at level 70.
- [ ] Pastoria's Ability Capsule ball is gone (Ian, 2026-10-31): the
  southern end of the one-tile strip between the two ponds in the city's
  southwest corner is empty. The game's one Ability Capsule is the Pokemon
  Mansion knockout's prize (the next check).
- [ ] The Pokemon Mansion's maid knockout (Ian, 2026-10-31;
  `maid-knockout.md`), on Route 212 North, behind Darach and Caitlin's
  gate (the checks below), so beat them first. The maid at the west of the hall
  explains the challenge with no turn target. The five maids each name
  their household job as they come out (Belinda's Araquanid, Sophie's
  Lurantis, Emily's Cinccino, Elena's Torkoal, Clare's Klefki and
  Gothitelle), and then Lady Celeste leads with Clefable, Milotic behind.
  All six battle back to back with no healing, and Celeste uses no bag
  item. Straight after the win over her, before she leaves, she gives an
  Ability Capsule. Used on a Pokemon, it asks first, naming the other
  regular ability. The maid then says the challenge is complete, and she
  never offers it again, the next day included. With a full Medicine
  pocket the Capsule is refused, and talking to the maid later hands it
  over.
- [ ] Dahlia gates the Game Corner's prizes (Ian, 2026-09-27 and
  2026-10-31). In Veilstone, the prize counter's receptionist, in the
  building beside the Game Corner, refuses to trade and points to Dahlia.
  The slots and the coins clerk still work. Dahlia stands just inside the
  Game Corner's door, to its upper right; she asks before the fight without
  naming the Wonder Room (Ian, 2026-10-31: a surprise), and
  "No" leaves her standing. Her fight opens with Wonder Room already up
  and it never ends (the move Wonder Room fails). After the win the prize
  counter trades, its badge-gated TMs as before, and Dahlia has her
  once-beaten line.
- [ ] Darach and Caitlin block the Pokemon Mansion (Ian, 2026-10-31). On
  Route 212 North, enter the mansion and walk up the aisle from the door.
  Two steps in, where the aisle narrows, Darach notices you and asks. "No",
  or fewer than two Pokemon able to fight, walks you back a step, and no
  tile of the aisle lets you past. "Yes" starts a double battle against one
  trainer, Darach's class with Caitlin beside him in his sprite.
- [ ] The egg comes on the win: straight after it, Darach hands over the
  Manaphy egg. With a full party he keeps it, and talking to him later
  gives it. Once given, he and Caitlin have their once-beaten lines.
- [ ] The office no longer offers the egg: the maid in Mr. Backlot's
  office, before the win, says Darach keeps it for a Trainer who beats
  him, with no yes or no; after you have the egg she hopes you care for it.
- [ ] The Trophy Garden opens behind them: after the win the aisle is open,
  and the office, the maids' rooms and the Trophy Garden at the back of the
  hall can all be entered.
- [ ] Thorton asks first (Ian, 2026-09-27 and 2026-10-31). In Ironworks
  Hall, ride the moving floor to Mr. Fuego's room: the slide that brings
  you in stops beside Thorton, who stands just below and to the left of
  that tile, facing north. Nothing happens until you speak to him; then he
  asks before the fight, and "No" leaves him standing. Mr. Fuego, the
  TM35 ball and the way back down to the door can all still be reached
  with him there.
- [ ] Thorton's fight opens in a Trick Room that never ends: before the
  first turn the screen says "The dimensions became distorted!", the
  slower Pokemon move first all fight long, "The twisted dimensions
  returned to normal!" never shows, and the move Trick Room fails. His defeat line shows
  on the win.
- [ ] Thorton's prize menu offers the right two starters at 40: straight
  after the win he offers a menu of the final stages of the two starter
  lines you did not choose (Cinderace and Empoleon after Turtwig, Torterra
  and Empoleon after Scorbunny, Torterra and Cinderace after Piplup), with
  "Not now". A no at "So, the ... it is?" goes back to the menu. The one
  picked is level 40, and its summary says it was met at Ironworks Hall;
  the OxiDex counts it as Ironworks Hall's capture, not the yard's.
- [ ] A full party keeps the gift: beat Thorton with six Pokemon, and he
  says your party is full and keeps the rental; "Not now" does the same.
  Talking to him again with room offers the menu again; once a rental is
  given he has his closing line and offers nothing more.
- [ ] Argenta waits for the Pal Park double (`overseer-argenta-place`,
  Ian, 2026-11-01). In Pal Park's lobby before the partner double is won,
  walk up the east corridor into the north gallery: the four spectators
  are there and Argenta is not. Win the double, and without leaving the
  lobby walk up again: Argenta, the Hall Matron, stands at the gallery's
  west end, facing east. Leave and come back: she is still there.
- [ ] Argenta asks first: nothing happens until you speak to her. She says
  who she is, that she came to see the Pokemon from faraway regions, and
  that a win earns a gift, then asks; "No" gives her "Not today?" line and
  leaves her standing. Every line fits its box.
- [ ] Argenta's battle (from a save, since a loss ends the run): an
  ordinary single battle, no room or field effect, against her six at 50,
  Skarmory first. Her defeat line, "Oh, dear... The trouble with fun is
  that it is over so quickly.", shows on the win.
- [ ] Argenta's bundle comes once: straight after the win she gives a Gold
  Bottle Cap, then three Bottle Caps, each give with its own "obtained"
  message, then her closing line. One Gold Bottle Cap and three Bottle Caps
  are in the Bag. Speaking to her again, after leaving and coming back, and
  after saving and reloading, gives only her closing line: no battle and
  no items.
- [ ] The Ability Patch (Ian, 2026-10-13): beating Ace Trainer Jose on
  Route 228 gives an Ability Patch and then TM64, straight after the win.
  With a full Bag, talking to him again gives what was refused.
- [ ] Stark Mountain's last room is empty after the Charon scene; Valor Cavern
  is empty after Galactic HQ.
- [ ] Acuity Cavern: Uxie's sprite, but the cry and the level 50 battle are one
  of Articuno, Cresselia or Pheromosa, and running or fainting it prints that
  name in "disappeared deep into its cavern". A new game can draw a different
  one; a soft reset cannot.
- [ ] Verity Cavern: Mesprit's sprite, but the preview, the cry and the names
  in "flew off" and in Rowan's two lines are the roamer draw (one of Mesprit,
  Tapu Koko, Buzzwole, Galarian Zapdos, Poipole, Xurkitree or Galarian
  Articuno). That species then roams at level 50, the Marking Map shows it with
  Mesprit's icon (known), and after defeating it Verity Cavern brings it back.
- [ ] Victory Road, the first step north inside the south entrance: Dawn (or
  Lucas, for a female player) notices you, you are walked in front of her, and
  the level 71 fight uses the team for your starter (trainers 779 to 784).
  Winning fades her out for good; losing leaves her there for another try.
- [ ] Koffing and Ponyta take a Moon Stone (`main-galar-stones`). With either
  in the party, choose Use on a Moon Stone from the Bag. Koffing and Ponyta
  are marked ABLE, and the rest of the party NOT ABLE unless it has a Moon
  Stone evolution of its own. Using it plays the evolution scene into
  Galarian Weezing or Galarian Rapidash, with the Galarian sprite and name.
  An untouched Koffing still becomes ordinary Weezing at level 35, and a
  Ponyta ordinary Rapidash at 40.

- [ ] **The Meister's trade** on Route 226. In the test kit, the menu's
  "Meister's trade" gives a level-50 Finneon and puts you at his door. Talk
  to him twice (the first time powers up the Pokedex): he asks for a Finneon
  for his precious MELOETTA. The trade gives a Meloetta nicknamed Sera, OT
  Meister, holding a Lum Berry, at the Finneon's level, with Relic Song in
  its first move slot at full PP (his script sets it after the trade), and
  his thanks name it. Its other three moves are its last level-up moves at
  that level, at 50 Echoed Voice, U-turn and Wake-Up Slap. Its cry plays,
  and its Pokedex entry reads "Its melodies sway the hearts of all who hear
  them..." with the Melody Pokemon category. With the emulator's bridge
  running, the Overseer can check the received Meloetta field by field from
  the box export.

- [ ] **Mandatory fights, Maylene's split** (`overseer-mandatory-fights`,
  Ian, 2026-10-29; `docs/oxide/mandatory-fights.md`). Walk the story path
  from Hearthome to Veilstone without dodging anyone. Each trainer below
  should see you and walk up before you can pass, and after the battle the
  way on is still open with the trainer standing where it was:
  - Breeder Albert, Route 209, just south of the three-row strip east of the
    grass; he looks north. Taking the ledge out of the grass should land you
    in his sight too. The fisherman's pier beside him is still reachable.
  - Poke Kid Danielle, Route 209, at the east edge of the strip that climbs
    to the bridge, looking west.
  - Cowgirl Shelley, Route 209, at the west end of the row where the walk
    north and the bike slope come out, looking east. Ride up the slope once:
    you should come off it and be seen, not bump into her.
  - Rancher Marco, Route 210 South, at the west edge of the corridor in from
    Solaceon, looking east.
  - Twins Teri and Tia, Route 210 South, two rows north of Marco at the same
    edge, looking east; one double battle, whichever of them sees you.
  - Belle and Pa Ava and Matt, Route 210 South, side by side where the
    meadow meets the bike slope and the grass column, looking west. Both
    come for a double battle, whichever of them sees you.
  - Black Belt Gregory, Route 215, at the corner where the path leaves the
    grass and turns east, looking east.
  - Black Belt Nathaniel, Route 215, at the top of the column the path
    crosses before the ledges towards Veilstone, looking south.
  - Black Belt Derek, Route 215, at the east edge of the three-wide column
    the path turns down after the raised walkway, looking west. Jogger
    Craig should not join him in one battle.
- [ ] **Mandatory fights, Wake's split** (`overseer-wake-split`, Ian,
  2026-10-31; `docs/oxide/wake-split.md`). Walk from
  Route 214 to Pastoria without dodging anyone. Each trainer below should see
  you and walk up before you can pass, and after the battle the way on is
  still open with the trainer standing where it was:
  - Psychic Abigail, Route 214, where she stood below the gate, now looking
    only west.
  - Psychic Mitchell, Route 214, where he started his walk, now standing
    still and looking south down the path.
  - PI Carlos, Route 214, at the east edge of the narrows south of the berry
    field, looking west. Beauty Devon's walking copy nearby should not join
    his battle.
  - Gentleman Jeremy, Valor Lakefront, at the west edge of the four-wide
    path in from Route 214, looking east. He has left Route 212 North.
  - Socialite Reina, Valor Lakefront, at the west edge of the six-wide stretch
    above the hotel, looking east; Cynthia's and Barry's later scenes there
    walk past her. She has left Route 212 North too.
  - Beauty Cyndy, Route 213, at the west edge of the three-wide way down from
    the hotel to the beach, looking east.
  - Tuber Chelsea, Route 213, just north of the one-tile sand strip west of
    the hotel's beach, looking south onto its entrance.
  - Tuber Jared and Fisherman Travis, Route 213, at the two edges of the
    two-row neck between the beach and the grass to Pastoria: Jared looks
    east along the south row, Travis west along the north row. Two battles
    one after the other, never one double. Travis has left Route 212 South's
    bridge. After Fen Badge the Galactic grunt chase on Route 213 should
    still run without bumping into either.
- [ ] **Mandatory fights, Candice's split** (`overseer-candice-pass`, Ian,
  2026-11-01; `docs/oxide/candice-split.md`). From Byron's badge, walk the
  story path to Snowpoint without dodging anyone: Lake Valor, Valor Cavern,
  Lake Verity, Mt. Coronet, Routes 216 and 217. Each trainer below should see
  you and walk up before you can pass, and after the battle the way on is
  still open with the trainer standing where it was:
  - Grunt 1 on the drained Lake Valor, just west of the one-tile gap on the
    way to Valor Cavern, looking east through it. He has left the open
    ground where he looked north.
  - A new grunt at Lake Verity's mouth, the Galactic version after Saturn,
    on the west tile just inside the entrance, looking east: he should battle
    as you take your first step in, with his own lines ("That old-timer packs
    a punch!"), where he used to stand by the shore only saying "Ow! Ouch!".
    After Mars's win he is gone with the other grunts.
  - Skier Edward, Route 216, at the west neck north of Snowbound Lodge,
    looking east. He no longer walks about the middle of the route.
  - Skier Shawn, Route 217, at the south neck just north of Maylene's scene,
    looking east. Maylene's scene should still run as you come in from Route
    216, and Ace Trainer Dalton's battle should stay his own, never a double
    with Shawn.
  - Ninja Boy Ethan and Black Belt Luke, Route 217, at the north neck by the
    signpost: Ethan stands undisguised looking east, Luke stands still looking
    north. Two battles one after the other, never one double.
  Also check that the four Rock Climb trainers above Route 216's walls are
  still out of reach before the Icicle Badge.
- [ ] **Mandatory fights, HQ's split** (`overseer-hq-pass`, Ian, 2026-11-02;
  `docs/oxide/hq-split.md`). From Candice's badge, walk the story path
  without dodging anyone. Each trainer below should see you and walk up
  before you can pass, and after the battle the way on is still open:
  - A new Hiker, Gunnar, at the foot of Acuity Lakefront's climb, looking
    east across it, once Rock Climb takes you up the wall; out of reach
    before the Icicle Badge.
  - Veilstone's storage-key grunt, by the Galactic building: talking to him
    starts a battle after "I don’t know anything about any Storage Key!",
    and only when you win does he drop the key and Looker arrive. Lose, and
    you black out with the key still his.
  - B1F's grunt, now a trainer at his own tile, looking west: he battles as
    you arrive from B2F, with his own lines ("They finally gave me some
    Pokémon!").
  - Scientist Fredrick in his 1F room, now at the two-tile gap east of his
    old spot, looking south; Scientist Darrius on 2F's east side at the gap
    between the arrival and the grunt pair, looking south. Both fights come
    before the grunts beyond them.
  - Officers Phobos and Deimos in the lobby, either side of the corridor
    beyond the key door, facing each other: one double battle as you step
    up from the door, never two singles if two of your Pokemon can fight.
  - Officers Boreas and Laverna on 4F, either side of the row below
    Cyrus's key door, facing each other: one double battle before the door.
  - Officer Argo on 4F's north side after Cyrus, at the gap on the way to
    the laboratory's panel, looking south.
  - In the laboratory, the male scientist, Oskar, now standing still at the
    west gap between the pillars, looking south; and Officer Hesperid in the
    top-left corner of the room by the door to the control room, looking
    east along the row before it.
  - Cyrus 2's ace (Weavile) at 59 and Saturn 2's (Toxicroak) at 60.
  Also check the Ability Capsule: 3F west's locked room, opened with the
  Galactic Key, holds a ball at its top-left alcove that gives the Ability
  Capsule once, and the TM ball there still gives its TM. Hiker Alexander
  (Route 208) and Dragon Tamer Patrick (Route 210 North) are still behind
  their Rock Climb walls, now at 56 and 57.

## 5. The ordinary ROM, after the League

On a save with the National Dex and the game beaten:

- [ ] No level cap is left after beating Cynthia: the OxiDex's save bar reads
  the Post split and flags no party member, at any level.
- [ ] The Hall of Fame keeps its entry through a reload (`main-30-boxes`
  moved it from flash sectors 32 to 34 to 45 to 47): after the League, save,
  turn off, load, and the PC's Hall of Fame viewer shows the team.
- [ ] The colour variation in the Hall of Fame: it shows each Pokemon in the
  same colours as its summary, and so does the PC's Hall of Fame viewer.
- [ ] **(live)** Volkner's rematch: his Rotom-Mow (level 88, Timid, every IV
  28) reads Electric and Grass, not Electric and Ghost, and shows 210 HP, 129
  Attack, 217 Defense, 214 Sp. Atk, 217 Sp. Def and 207 Speed. Oxide's plain
  Rotom has the same base stats as its forms, so the types are what tell the
  form apart; without the stub, a Fire move is super effective on it. This
  replaces the gym fight's Rotom-Mow check, since his gym Rotom is plain now.

- [ ] Acuity Lakefront's grass and the Poke Radar there give no Weavile,
  Abomasnow, Mamoswine or Glalie, and radar chains still build on the area's
  own species.
- [ ] The rival's younger sibling in Sandgem keeps her ordinary line when talked
  to twice.
- [ ] Sinnoh Now, watched a few times, shows no swarm news flash.
- [ ] The Great Marsh binoculars show only what the marsh can give.
- [ ] With the lookout's daily Pokemon cut (2026-09-30, `oxidex-bugs-0930`): a Safari Game in any Great Marsh area meets only that area's own table, and the lookout's binoculars show a species from it.
- [ ] If a GBA game can be put in melonDS's second slot, no route gains its
  species.

## Passed

Ticked checks move here with the date they passed.

- [x] **The battle log**: done 2026-09-28, three wins on Route 202 on
  51fa6cdaa; the OxiDex's Battle Log listed all three, and Sync and the log
  also work on melonDS-oxide's live feed. Still unseen: a lost fight logging
  as lost.
- [x] **The new CPU** (2026-09-29): the old chip's workarounds came out, the
  BIOS went back to Intel Default Settings, the parallel check passed 0 of 960
  on Windows and 0 of 1,760 in WSL, and two clean local builds matched
  GitHub's SHA-1 for 252111fe3. The design doc's findings log (2026-09-29) has
  the detail.
- [x] **Eight items the balance census cannot reach** (2026-09-29): Ian
  answered all eight the same day (Wayward Cave B1F's four by the bike ramps,
  Amity Square's Spooky Plate by the ruins' teleporters, Victory Road's three
  by its waterfall, Strength and the bike's short jump), and the census
  models each.
