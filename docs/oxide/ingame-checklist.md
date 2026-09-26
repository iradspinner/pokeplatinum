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

The i9-14900K is degraded (design doc findings log, 2026-09-22) and its
replacement is on the way. When the new chip is in, and before any playtest:

- [ ] Delete the venv block in the `Makefile`, the build retry in
  `integrate.sh`, the wedge guard (its rule in `.claude/hooks/oxide_guard.py`,
  `wedge_status.sh` and its test beside it, and the `statusLine` entry in
  `~/.claude/settings.json`, which Ian edits himself), the local-build rule in
  `.claude/hooks/oxide_guard.py` that refuses full builds, its paragraph in
  CLAUDE.md's Build section, and the memory file
  `no-local-builds-until-new-cpu.md`. `integrate.sh --rom` can stay.
- [ ] Rerun the parallel check (`C:\Users\Ian\oxide-flake-check\parallel.py`,
  and the same file from WSL). WSL failed about ten times as often as Windows
  under the same load, and the wedge may be a second, WSL-kernel problem that
  the CPU has been hiding.
- [ ] Build `oxide` locally once and compare its SHA-1 with GitHub's build of
  the same commit. Until they match, keep using `tools/oxide/fetch-rom`.

## 1. The ROMs and the save

- [ ] Fetch the ordinary ROM and the test kit ROM of the current `oxide`:
  `tools/oxide/fetch-rom <commit>` and `tools/oxide/fetch-rom --testkit <commit>`.
- [ ] **Start a new game.** An old save reads every ability as NONE by design
  (element 2 moved the field) and is no valid test bed.
- [ ] Known crash to avoid until the bug track fixes it: UNLOCK FPS set to
  ALWAYS hard-crashes on entering Sandgem Town (tracker, Phase 5).
- [ ] Once `carry-over` merges, **the base ROM's visual overhaul**, compared
  with Ian's own base ROM where anything looks off: the title screen's logo;
  the new Pokemon sprites front and back in battle, sitting at the right
  height on their platforms (the heights came with the sprites); a shiny with
  a custom palette where one turns up (the test kit can make one); the new
  battle backgrounds and platforms on grass, in a cave and indoors; the HP
  box's colours; the party menu's colours; the four new box wallpapers; and,
  post-game, May, Steven, Red and Gold showing their own battle sprites.
  Shadow Force's animation carries one changed byte nobody has explained;
  note anything odd about it.

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
  later. A stub effect does its damage and skips its extra, or says "But
  nothing happened!"; that is expected. Autotomize prints no "became nimble!",
  as Ian ruled.
- [ ] **Element 5, the Abilities menu** (two pages, Neutralizing Gas last): one
  entry per ability that shows itself, each with its own wild foe. For
  Neutralizing Gas: Galarian Weezing against a wild Chansey given Pressure
  shows the entry message as Weezing comes in, no extra PP is spent while the
  gas is out, and switching Weezing out prints the exit message followed by
  Chansey's Pressure message again.
- [ ] **The staples rulings, the Modern rules menu** (22 entries): Sturdy as a
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
- [ ] **One calculator roll** (the encounter tool, M8): in a battle, note an
  attacker's and a defender's level and stats and the damage a move does, enter
  the same two in the encounter tool's calculator, and check the damage falls
  in its range.
- [ ] **Element 8, hidden abilities and restored items** (the last three
  Modern rules entries):
  "Hidden ability gift" gives a Lv. 15 Litten whose summary reads
  Intimidate, not Blaze; one Rare Candy makes a Torracat that still reads
  Intimidate. "Hidden ability wild" opens with the wild Litten's Intimidate
  lowering your lead's Attack; the flag clears itself after that one use.
  "Items restored": Mew eats its Sitrus Berry after Belly Drum, and has it
  back in its summary after the battle.

## 3. The ordinary ROM, early game (Twinleaf to Hearthome)

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
- [ ] Level caps: before Roark nothing passes Lv. 16, from battle or candy;
  after beating him the badge message plays as before and Lv. 26 is the new
  ceiling. The Day Care man's level and price stop at the cap too.
- [ ] The options menu reads UNLOCK FPS, with OFF, BATTLE and ALWAYS (see the
  known crash above before choosing ALWAYS).
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
- [ ] Honey trees at one badge: slather a tree and check the species and levels
  against table 1 of `res/field/encounters/encounters_honey_tree.json`. The
  Munchlax trees are gone.
- [ ] Valley Windworks: the Drifloon balloon no longer appears.
- [ ] The Hearthome Fan Club member only says goodbye, with no starter gift.
- [ ] The starter's summary reads met at "Rowan's Briefcase", not Route 201.
- [ ] Once `carry-over` and `carry-over-abra` merge, the base ROM's overworld
  sprites and the teleporting Abra's removal: no Abra stands outside Sandgem's
  Pokemon Center or in any other town, on Routes 207, 221 or 224, on Mt.
  Coronet or Stark Mountain, or in Turnback Cave. The gym shortcut Abra still
  stand at the entrance and by the leader of the Canalave, Pastoria,
  Snowpoint, Veilstone and Sunyshore gyms, draw as an Abra, and face and
  turn properly when talked to. Later in the game, May at the Resort Area,
  Steven in Stark Mountain's first room, and Ethan and Red on Mt. Coronet's
  north and south slopes draw as themselves.

## 4. The ordinary ROM, mid-game

- [ ] **(live)** Gardenia's Cherrim with Sunny Day: the same AI check as Camper
  Zackary's.
- [ ] Honey trees at five badges: check against table 5.
- [ ] The Pocket PC in places vanilla's Vs. Seeker never reached, now that it
  works everywhere but a gauntlet: the Great Marsh, the Underground, the
  Distortion World, and the Battle Frontier's lobbies. Each should either open
  the PC and return cleanly or refuse; note anything that breaks the area's
  own rules (healing mid-challenge, losing Safari Balls).
- [ ] Iron Island: Riley's egg hatches as a random species, one of eight lines.
- [ ] Snowpoint City: Mindy takes a Snover and gives a Suicune, which is shiny.
- [ ] **(live)** Worker Jackson's Wormadam-Trash (level 49, Relaxed, every IV 27)
  shows 131 HP, 85 Attack, 122 Defense, 85 Sp. Atk, 111 Sp. Def and 47 Speed.
- [ ] Galactic HQ, Saturn: the battle opens with "The dimensions became
  distorted!", the slower Pokemon moves first all fight, "The twisted dimensions
  returned to normal!" never appears, a Trick Room from either side fails, and
  Saturn's AI never chooses it.
- [ ] Level caps through the story: beating Gardenia lifts the cap to 33,
  Fantina to 39, Maylene to 44, Wake to 53, Byron to 56, Candice to 60, Saturn
  at Galactic HQ to 65, Cyrus in the Distortion World to 68, and Volkner to 78.
- [ ] **(live)** Element 6's Phase 4 catch-up (`docs/oxide/battle-ai/README.md`),
  in Volkner's battle: lead with a Lightning Rod Pokemon (Electrike's line or
  Rhyhorn's), break at the end of `TrainerAI_MainSingles` and read
  `moveScore`. Every Electric attack reads 12 or more below its score against
  another lead, and Thunder Wave, if he has it, 10 below. Until the battle has
  recorded the ability the AI guesses between the species' two, so the drop
  shows on about half the turns; take several turns before calling it.
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

## 5. The ordinary ROM, after the League

On a save with the National Dex and the game beaten:

- [ ] No level cap is left after beating Cynthia: a Pokemon at 78 gains Exp.
  and takes Rare Candies again.

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
