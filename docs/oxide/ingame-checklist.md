# Platinum Oxide: the in-game checklist

Every check that waits on Ian playing the game, in one place and in the order a
playtest day meets them (Ian, 2026-09-26: all at once when the new CPU is in).
The tracker's "Waiting on Ian" points here; this file holds the full wording.
The `playtest-day` skill runs the day from it. When a check passes, tick it and
move it to the bottom section with the date; when it fails, it becomes an
"Open bug" entry under the tracker's Phase 5, and the line here says so.

Checks marked **(live)** need a local agent attached to melonDS over the GDB stub
(the `debug-live` skill). Ian drives; the agent reads memory. Nothing here asks
an agent to launch an emulator.

## 0. Before anything: the new CPU

The old i9-14900K was degraded (design doc findings log, 2026-09-22). Its
replacement went in on 2026-09-29, and all of this was done that day:

- [x] Delete the venv block in the `Makefile`, the build retry in
  `integrate.sh`, the wedge guard (its rule in `.claude/hooks/oxide_guard.py`,
  `wedge_status.sh` and its test beside it, and the `statusLine` entry in
  `~/.claude/settings.json`, which Ian edits himself), the local-build rule in
  `.claude/hooks/oxide_guard.py` that refuses full builds, its paragraph in
  CLAUDE.md's Build section, and the memory file
  `no-local-builds-until-new-cpu.md`. `integrate.sh --rom` can stay.
  Done 2026-09-29, after a gentle check of the new chip (microcode 0x12F; single-core
  and four-copy runs all clean and repeatable). The `statusLine` entry is Ian's
  to remove; CLAUDE.md and the standing rulings keep the three-job limit until
  the stress check below passes, and GitHub ROMs until the build check does.
- [x] Undo the BIOS change made for the old chip, before the stress check:
  the P-cores' all-core ratio cap of 55 (2026-09-22, design doc findings
  log) goes back to Auto, with MSI's Intel Default Settings profile on, so
  the check runs the new chip as it will be used. The only other change,
  Windows' maximum processor state at 99%, Ian undid on 2026-09-29.
  Done by Ian the same day: P-core ratio 55 to Auto, CPU Cooler Tuning on
  Intel Default Settings, P-Core Beyond 6GHz+ off.
- [x] Rerun the parallel check (`C:\Users\Ian\oxide-flake-check\parallel.py`,
  and the same file from WSL). WSL failed about ten times as often as Windows
  under the same load, and the wedge may be a second, WSL-kernel problem that
  the CPU has been hiding. Passed 2026-09-29, 32 copies at a time: 0 of 960
  failed on Windows and 0 of 1,760 in WSL (the old chip: 1 and 16 of 160), no
  wedge, and no WHEA error or crash in Windows' logs.
- [x] Build `oxide` locally once and compare its SHA-1 with GitHub's build of
  the same commit. Until they match, keep using `tools/oxide/fetch-rom`.
  Passed 2026-09-29: two builds from an empty folder on every core, 17,816
  steps in 47 and 48 seconds, both `917eb9a5` like GitHub's build of
  252111fe3.

## 1. The ROMs and the save

- [ ] Fetch the ordinary ROM and the test kit ROM of the current `oxide`:
  `tools/oxide/fetch-rom <commit>` and `tools/oxide/fetch-rom --testkit <commit>`.
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
- [ ] Once `main-meloetta` merges, **your current save still loads**: the
  Pokedex keeps its seen and caught counts, and mail and greetings read as
  before. On mail written before it, an egg or a Deoxys, Unown, Burmy,
  Wormadam, Shellos or Gastrodon form shows the icon one place along; that is
  known and harmless (`save-layout.md`, the Meloetta section).

- [x] **The battle log**: done 2026-09-28, three wins on Route 202 on
  51fa6cdaa; the OxiDex's Battle Log listed all three, and Sync and the log
  also work on melonDS-oxide's live feed. Still unseen: a lost fight logging
  as lost.

## 2. The test kit ROM

The kit's NPC and menus are described in `docs/oxide/test-kit.md`, set by set,
with what each should show. The kit cannot set up double battles, a frozen
Pokemon, or a foe holding an item; those checks are marked for normal play.

- [ ] **Element 4, the move sets.** Sets 1 to 22 passed in rounds 1 to 3
  (2026-09-22 to 23). Still to see: sets 23 to 26; sets 27 to 31 (Sticky Web,
  After You, Aurora Veil, the four side guards against the kit's two new wild
  foes, and Belch with the Sitrus Berry the set gives), which the paged menu
  now reaches safely; and sets 32 to 41 on the "More sets" page (Electro Ball
  by Speed ratio, Stored Power, Retaliate, Echoed Voice, Stomping Tantrum,
  Last Respects, Hard Press, Pika Papow and Veevee Volley, Lash Out, Grav
  Apple). Sets 42 to 49 on the same page: Foul Play, Body Press, Psyshock
  (with Psystrike and Secret Sword), Sacred Sword and Darkest Lariat, Freeze-Dry,
  Flying Press, Rage Fist (50 plus 50 per hit taken, kept through switches) and
  Transform copying the whole ability. Set 50 on the same page: Wonder Room
  against a Cloyster that recovers every turn, Tackle and Swift trading
  places while the room is up and back again when it wears off five turns
  later. Set 51 on the same page: Shore Up against a Chansey's Seismic Toss,
  healing half Mew's HP in sun or rain and two thirds in a sandstorm. Set 52:
  Meteor Beam charging for a turn with a Sp. Atk raise, then hitting, or
  hitting at once holding the Power Herb the set gives. Set 53: Electro Shot
  the same way out of rain, and raising Sp. Atk and hitting in one turn after
  Rain Dance. Sets 54 to 67, the partly working moves (2026-09-27), set 54 on
  the same page and the rest on the third: Mind Blown costing half Mew's HP
  even into Protect (54) and stopped by Damp at no cost (55), Nature's
  Madness usable under Taunt (56), Scale Shot's Defense drop and Speed rise
  (57), Spiky Shield hurting and Baneful Bunker poisoning a Tackle but not a
  Swift (58, 59), Salt Cure's damage each turn, doubled after Soak (60),
  Octolock's drops each turn (61), Magic Room stopping Leftovers for five
  turns (62), Teatime eating a Liechi Berry at full HP (63), Core Enforcer
  against a faster Volt Absorb Jolteon (64), Beak Blast burning a Tackle
  (65), and Sky Drop lifting a Chansey that then cannot act (66) and not
  affecting a Skarmory (67). A stub
  effect does its damage and skips its extra, or says "But
  nothing happened!"; that is expected. Autotomize prints no "became nimble!",
  as Ian ruled.
- [ ] **Element 5, the Abilities menu** (two pages, Neutralizing Gas last): one
  entry per ability that shows itself, each with its own wild foe. For
  Neutralizing Gas: Galarian Weezing against a wild Chansey given Pressure
  shows the entry message as Weezing comes in, no extra PP is spent while the
  gas is out, and switching Weezing out prints the exit message followed by
  Chansey's Pressure message again.
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
- [ ] **The staples rulings, the Modern rules menu** (its first 19 of 24
  entries; the other five have their own checks below): Sturdy as a
  Focus Sash, Lightning Rod and Storm Drain immunity, the Intimidate blockers,
  Grass against powder, Electric against paralysis, 1.5x critical hits, Defog
  clearing hazards from both sides and screens only from the target's, Rapid
  Spin's Speed raise, and the rest the menu lists.
- [ ] **Native moves at modern numbers.** Fury Cutter used five times in a row
  goes 40, 80, 160, 160, 160 in power, so its damage stops growing after the
  third hit; Roar and Whirlwind never miss.
- [ ] **Fairy.** A Dragon move does nothing to Clefairy or Ralts, a Poison or
  Steel move does double, the summary screen reads FAIRY, and the Pokedex info
  page shows the NORMAL plate (the known gap) rather than garbage. The Poketch
  move tester agrees with the battle engine.
- [ ] **The Move Relearner and learnsets.** At the Move Relearner, no move name
  clips beyond the eight known ones, descriptions read sensibly in five lines,
  and a new species' moves are listed. Level a Pokemon through a move it should
  learn and confirm the right move at the right level (a wrong widening would
  be wrong for all 667 learnsets). A Rotom in a form, or a Giratina holding the
  Griseous Orb, shows its form's stats.
- [ ] **Element 8, the level caps** (the Level caps menu, `docs/oxide/test-kit.md`
  has the detail): at a new game's cap of 16, Rare Candies stop at Lv. 16 and
  the next one has no effect and is kept; a Lv. 50 Pokemon wins with no Exp.
  message; a Pokemon one level under the cap stops at it however much it
  earns, and is still at it after a trip into the PC; a higher split lets it
  grow again.
- [ ] **Protect in a row** (Modern rules, `cloud/element6-changes`): King's
  Shield used every turn works the first time, then about one time in two, then
  one in four, with "But it failed!"; Spiky Shield the same. Before the fix
  both worked every turn.
- [ ] **One calculator roll** (the encounter tool, M8): in a battle, note an
  attacker's and a defender's level and stats and the damage a move does, enter
  the same two in the encounter tool's calculator, and check the damage falls
  in its range.
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
  into Alolan Ninetales, the Fire Stone the other into Ninetales; note the
  name the Alolan one takes, since its species name is still the form
  placeholder "-----".
- [ ] **Element 7, for normal play** once the balance track has placed items
  and given trainers theirs (the kit cannot give a foe an item or run a
  double battle): a foe's Red Card dragging out a teammate in a trainer
  battle, a foe's Air Balloon, Eject Button, Rocky Helmet and Weakness Policy,
  and Ability Shield and Covert Cloak in a double battle.

- [ ] **Evolution moves** (the "Eevee with Charm" entry, with `main-evo-moves`
  merged). In the kit ROM only, Sylveon has a stand-in evolution move. One
  Rare Candy evolves the kit's Eevee, and on evolving it learns Moonblast,
  with the forget-a-move prompt if it knows four. The Move Relearner then
  lists Moonblast for it. No species outside the kit has an evolution move
  until the balance track sets them.
- [ ] **Single-use TMs** (the "Two TMs" entry, with `main-tm-single-use`
  merged). The TM Case shows TM01 x2; teaching it once leaves x1, and a
  second use empties it. An HM taught from the case stays.
- [ ] **Meloetta's forms** (the "Form changers" entry, with `main-meloetta`
  merged). The kit gives a Lv. 50 Meloetta with Relic Song in its first slot.
  In one of the menu's wild battles, switch it in: a Relic Song that hits turns
  it into Pirouette (orange hair, Normal and Fighting, "transformed!"), and the
  next one that hits turns it back to Aria. A Relic Song that misses changes
  nothing. Switched out as Pirouette, it comes back in as Aria. After a battle
  ended with it as Pirouette, its summary shows Aria, Normal and Psychic, and
  Aria's stats.

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
- [ ] Once `carry-over` merges, **the Pocket PC** (received in Sandgem; Ian's
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
- [ ] Rare Candy chaining works, up to the level cap (16 before Roark).
- [ ] With Scorbunny as the starter (fixed 2026-09-27, `fix-rival-starter`):
  Barry leads with Piplup on Route 201 and at every later fight, and Dawn or
  Lucas uses the Turtwig line. With Turtwig, Barry has Scorbunny; with Piplup,
  Turtwig. The Jubilife TV mask, the Veilstone Department Store socialite's
  mask and the Underground Man's doll are the fire starter's.
- [x] The battle log (done 2026-09-28, section 1).
- [ ] The Kaizo move data in normal play (`cloud/element4-kaizo-move-data`):
  TM08 Bulk Up shows 3 PP in a summary, and Screech 5; a Pokemon's Cotton
  Spore in a double battle lowers both foes' Speed; Drill Peck and Dragon
  Claw land critical hits noticeably more often than Peck or Scratch.
- [ ] Level caps: before Roark nothing passes Lv. 16, from battle or candy;
  after beating him the badge message plays as before and Lv. 26 is the new
  ceiling. The Day Care man's level and price stop at the cap too.
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
- [ ] **(live)** The AI fix on Camper Zackary's first turn (level 15, a Castform
  with Rain Dance, a Weather-flag trainer): break at the end of
  `TrainerAI_MainSingles` and read `moveScore`. Rain Dance reads 105 and
  neither attack carries the Weather flag's +5 (compare the +5, not the gap).
- [ ] Element 6's absorber switch (`cloud/element6-changes`), Picnicker Siena
  (level 15, Zigzagoon then an Electrike with Lightning Rod): hit Zigzagoon
  with an Electric attack that does not knock it out. On about half such
  turns she switches to Electrike instead of attacking; before the change she
  never did. Take several tries before calling it.
- [ ] **(live)** Rapid Spin's clearing (`cloud/element6-followups`), Bug
  Catcher Donald in Eterna Forest (level 17, a Pineco with Rapid Spin, Expert
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
  grunt's level 24 Snover sets hail as it enters (Snow Warning, its hidden
  slot, through the party's ability 3; 20 trainers use it since aa3bbc3356).
- [ ] Route 207: after Mira is found in Wayward Cave, the woman who asked for
  her says thank you and gives no evolution stones; her first line no longer
  promises any.
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

## 4. The ordinary ROM, mid-game

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
- [ ] **(live)** Gardenia's Cherrim with Sunny Day: the same AI check as Camper
  Zackary's.
- [ ] Honey trees at five badges: check against table 5.
- [ ] Double battles, once a trainer uses these moves (none does yet;
  `cloud/element4-partial-moves`): Flame Burst hits its target's partner for
  a sixteenth of its HP with "The bursting flame hit ...!"; Teatime's target
  screen shows every battler, as Haze's does, and it feeds every Pokemon on
  the field its Berry; Core Enforcer leaves the ability of a foe that has not
  moved yet alone.
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
  (level 60), lead with a Whismur-line Pokemon, whose only ability is
  Soundproof. Her Exploud never chooses Hyper Voice.
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
  Route 213, have no clown; everyone else in them talks as before, and
  Veilstone's Elekid gift still gives Elekid.
- [ ] The new grass (rustle on stepping in it, everywhere): Amity Square's lawn north-east of the pond (x 33 to 43, z 27 to 29) and Verity Lakefront's fenced lawn (x 85 to 95, z 846 to 850) give wild encounters from their tables; in Amity Square a battle with the walking partner out behaves normally. Sandgem's lawn by the beach road, Jubilife's fountain garden, Floaroma's north bed and Solaceon's lawn by the Day Care give encounters from their towns' new tables. Walking the Verity Lakefront lawn before the starter gives no encounter.
- [ ] A Burmy in a Sandy or Trash cloak evolves into a Wormadam with Anticipation, not Snow Cloak.
- [ ] Fuego Ironworks: inside the building the location reads Ironworks Hall (anything received there is met at
  Ironworks Hall, and the journal says "Departed from Ironworks Hall" on leaving); the yard still reads Fuego Ironworks.
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
- [ ] **(live)** Volkner's battle: his Rotom-Mow (level 61, Modest, every IV 29)
  shows 149 HP, 90 Attack, 153 Defense, 165 Sp. Atk, 153 Sp. Def and 133 Speed.
- [ ] Koffing and Ponyta take a Moon Stone (`main-galar-stones`). With either
  in the party, choose Use on a Moon Stone from the Bag. Koffing and Ponyta
  are marked ABLE, and the rest of the party NOT ABLE unless it has a Moon
  Stone evolution of its own. Using it plays the evolution scene into
  Galarian Weezing or Galarian Rapidash, with the Galarian sprite and name.
  An untouched Koffing still becomes ordinary Weezing at level 35, and a
  Ponyta ordinary Rapidash at 40.

- [ ] With `main-meloetta` merged, **the Meister's trade** on Route 226 (talk
  to him twice; the first time powers up the Pokedex): he asks for a Finneon
  for his precious MELOETTA. The trade gives a Meloetta named MELOETTA, OT
  Meister, holding a Lum Berry, at the Finneon's level and knowing Relic
  Song, and his thanks name it. Its cry plays, and its Pokedex entry reads
  "Its melodies sway the hearts of all who hear them..." with the Melody
  Pokemon category.

- [x] **Eight items the balance census cannot reach** (2026-09-29): its map
  flood finds no way to them, so no score counts them. For each, say whether
  the player can pick it up and what it takes (which field move or path):
  Wayward Cave B1F's Rare Candy, Grip Claw, Max Ether and hidden Stardust;
  Victory Road's TM59, Max Elixir and Full Restore on the upper levels; and
  Amity Square's Spooky Plate in the fenced pen. Tell the balance track.
  Wayward Cave answered by Ian the same day: bike ramps carry the player
  three tiles ahead, over the two between even when a rock sits on them, and
  the basement's items are reached that way; the census models it.
  Ian on the rest: Amity Square's ruins hold scripted teleporters into the
  pen, and Victory Road's three are probably behind the way that opens only
  after the Champion; the census follows both. Tick this once the balance
  track reports all eight placed.
  The balance track placed seven the same day: Wayward Cave's four and the
  Spooky Plate in Fantina's split, Victory Road B1F's TM59 in Barry's (its
  waterfall) and 2F's Full Restore in Barry's (Strength). One is left for
  Ian: Victory Road 2F's Max Elixir (tile 4,5), in a pocket whose only ways
  in are ledges out and the tile the bike ramp at (10,10) jumps over. Does a
  slow ride onto that ramp stop on it, or is there another way in?
  Ian, the same day: yes, the bike's slow gear jumps shorter, which reaches
  it; the balance track models the short jump. All eight answered.

## 5. The ordinary ROM, after the League

On a save with the National Dex and the game beaten:

- [ ] No level cap is left after beating Cynthia: a Pokemon at 78 gains Exp.
  and takes Rare Candies again.
- [ ] The Hall of Fame keeps its entry through a reload (`main-30-boxes`
  moved it from flash sectors 32 to 34 to 45 to 47): after the League, save,
  turn off, load, and the PC's Hall of Fame viewer shows the team.
- [ ] The colour variation in the Hall of Fame: it shows each Pokemon in the
  same colours as its summary, and so does the PC's Hall of Fame viewer.

- [ ] Acuity Lakefront's grass and the Poke Radar there give no Weavile,
  Abomasnow, Mamoswine or Glalie, and radar chains still build on the area's
  own species.
- [ ] The rival's younger sibling in Sandgem keeps her ordinary line when talked
  to twice.
- [ ] Sinnoh Now, watched a few times, shows no swarm news flash.
- [ ] The Great Marsh binoculars show only what the marsh can give.
- [ ] If a GBA game can be put in melonDS's second slot, no route gains its
  species.

## Passed

Ticked checks move here with the date they passed.
