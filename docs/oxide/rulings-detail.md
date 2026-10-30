# The long standing rulings, in full

Four of Ian's standing rulings grew long enough that every session and helper loading them at start cost a few thousand tokens each time. On 2026-10-22 Ian approved moving their full text here; `.claude/rules/standing-rulings.md` keeps a short form of each, which points to this page. Nothing below changed in the move. Read the section a task touches before it starts: the scorer before running or changing it, the move rulings before changing a move, the learnset rulings before changing a level-up list, and the trainer rulings before designing a team. The `balance-rules` skill points here too.

## How the fight scorer reads a fight

How the fight scorer reads a fight (Ian, 2026-09-30, on the trainer-scoring
handoff). The aim is to beat the game: a win that loses a Pokemon is still a
win, but each loss takes away later team-building options. Lines are ranked
by win rate first and average faints second (Ian, 2026-10-02, refining
"clean wins come first"): a line that always wins with one sacrifice beats
one that wins cleanly nine times in ten and loses the tenth, since one
unlucky turn there ends the run. Options that win about equally often (within
the estimate's noise) are then ranked by fewest faints; the clean rate is
reported, not optimised. A boss is read
over a spread of rolled boxes, so that its answers do not narrow to one
Pokemon. A box offers each pre-evolution held back as well as evolved on
time wherever holding it back reaches a move sooner than its evolution
does, or one its evolution never gets, so the team search can weigh a
Starly kept for Brave Bird by Maylene's split (Ian, 2026-10-15). Which
holds count depends on the Pokemon and the move, never a power threshold
(Ian, 2026-10-21: Fletchling held for Will-O-Wisp before Gardenia, Popplio
for Flip Turn before Byron, Venonat to 37 for Zen Headbutt before Maylene),
so status moves, pivots and coverage count, and the team search judges
which matter in each fight. Since the screen weighs damage and speed alone,
each of the race's finalists is also played with every held version of
its members, and the simulator keeps whichever wins more (Ian,
2026-10-21, trying it "to see how it plays out"; landed on 2026-10-21). So that a hold's cost counts, each box seed is one run through
the game, every fight's box that run's catches by its split, each area
rolled once at the run's first visit among the options open then, so
boxes keep today's sizes and nobody waits for Surf or a rod; and a
held-back version is offered at a fight only if no earlier fight of the
seed used the catch in a form the hold rules out; once a reading uses
one, the seed's later fights see the line as the hold left it, so each
seed's fights read in play order. A hold that would weaken an earlier
fight on purpose is listed in the reading, not modelled, since testing
it means reading that fight again (Ian, 2026-10-15). To measure what
holds change, a box whose chosen six uses a held-back version is read a
second time without holds, and the reading reports both (Ian, 2026-10-15;
the trigger narrowed on 2026-10-21 from the screen's top sixes, which
held versions filled from Barry 3 on). A catch's versions share one slot
in the team search (Ian, 2026-10-21): the on-time version and each held
one compete for one place in a six, so the screen counts sixes of catches
and holds do not multiply them. Ties between equal AI picks break at random. Every fight is
simulated at the game's real odds, with no luck budget (Ian, 2026-10-02):
the three numbers are then
true frequencies with bad luck inside them, and the planner's caution
comes from how heavily a position values a faint, weighing each chance at
its true odds. The stress test that replaces the budget (Ian, 2026-10-02)
replays the chosen line at disadvantage: every status and crit check, the
trainer's and the player's, rolls twice and keeps the result worse for the
player (the trainer's 1-in-24 crit lands about 1 in 12 and a 10% status
about 19%; the player's own crits and secondary effects land less often,
and its full-paralysis and confusion checks go against it). Quick Claw
and Focus Band roll against the player too (Ian, 2026-10-06). Its three
numbers are reported beside the real-odds ones, as a very unlucky fight.
Each trainer is read on 100 simulated fights: 75 at real odds and 25 very
unlucky (Ian, 2026-10-02, replacing 200 of each as too costly). A fight's
single difficulty number, shown in the OxiDex's Trainers tab, is its
average faints plus 40 times its losing rate at real odds (Ian,
2026-10-07, relayed by the encounter track). The
scorer's job is to order every fight in the game correctly by difficulty;
it need not win as a person would, and close enough is good enough while
that order is broadly right (Ian, 2026-10-02). For a boss the scorer
chooses the six and their moves itself, in three stages: a screen by
matchups with no simulated fights, a race among the screen's best sixes,
and the full reading of the two or three left (Ian, 2026-10-02). The
play-out planner runs at budget 64, and finalists whose win rates lie
within 5 points count as equal before faints decide (Ian, 2026-10-03).
An ordinary trainer is read blind: each simulated fight draws a random six
from the stronger half of the box, never one held below the cap (Ian,
2026-10-04). Targets (Ian, 2026-10-04): an ordinary trainer is won cleanly
80 to 85 percent of the time (replacing the provisional 70 to 80); no boss
reads above 95 percent won, save the Galactic officers, whose fights may
read close to 100 percent won so long as their death rate is not trivial,
and which read no harder than their commander, Hesperid likely excepted
(Ian, 2026-10-21, adding that this may shift later in the game); a boss's
difficulty spikes or drops with how
important it is, and Oxide's hardest bosses top out around the easiest of
Kaizo's read on the same box (about 80 percent won). The numbers order
fights rather than measure them absolutely, and Oxide is not meant to be
beaten on a first run. A trainer that trends a little hard, or reads as an
outlier, is fine while it approximates its band (Ian, 2026-10-06).
Cyrus 3, the biggest boss but Cynthia, may read harder than the rest
(Ian, 2026-10-06: "if any fight can be excused for being too hard, the
biggest boss fight of the game (save Cynthia) surely has that claim").
From about Cyrus 3 on, a boss may carry two or three legendaries where its
team needs them, against one before (Ian, 2026-10-06).
Two soft guides, for judging a reading and never as bars or gate checks
(Ian, 2026-10-13). The barometer for "unsolvably hard" is box 3 of the
first reading of Ian's six-member Gardenia (27 percent won, difficulty
34.7): Ian found a line close to winning it by hand, so a fight reading
clearly below it is likely beyond a planning player, and one near it is
hard but fair. And only a few fights may read as hard as that whole first
reading did (52 percent won over the three boxes): the Cyrus fights, the
Elite Four and Cynthia as a gauntlet, and perhaps a Galactic fight such
as the Mars and Jupiter double. Small changes swing a fight hard,
speed above all (Ian, 2026-10-13): Gardenia went from 52 to 96 percent
won on three small dials, two of which moved her members under Golbat's
Speed. Speed control is very strong for a trainer and for the player, so
any change to a fight is read against the speed tiers of the player's
likely answers before it is judged.
Boss levels spike by importance (Ian, 2026-10-06): gym leaders, rivals,
Cyrus and the League keep their aces at the cap, while officers and the
other mini-bosses sit a few levels under it and earn their difficulty
from sharper sets. Concretely (Ian, 2026-10-07): an officer's or
mini-boss's ace sits a few (2 to 4) under the cap (the four Ian named at 3
under: Saturn 1 and Mars 2 at 53, Saturn 2 at 57, Lucas and Dawn 3 at 68), and the Elite Four's aces rise from 72 to
78 (Aaron 72, Bertha 73, Flint 74, Lucian 75, Cynthia 78) under the
engine's single League cap of 78. A mid-split boss is read with the
player's box at its ace's level, extending the interim soft caps. Cyrus 3 is today's team raised to the cap's levels.
Across
the spread of boxes it reports which encounters its sixes always take and
which they never take, since both mark encounter balance to work on (Ian,
2026-10-02). When a fight reads too hard, the player's move pools are the first
candidate for change, since they are sparse in interesting options and lack
many modern moves. A fight is judged on three numbers read together, never
the clean rate alone (Ian, 2026-10-01): the clean rate, the share of
simulated fights won with no Pokemon fainting; the win rate, the share won
at all (no wipe); and the death count, the average number of the player's
Pokemon that faint per simulated fight, which separates the hardest fights
(Gardenia, Wake, Cyrus 3, Cynthia) where few runs win cleanly. The
scorer's good play must arise on its own (Ian, 2026-10-01): it decides
turn by turn by simulating its options in the real simulator against the
exactly known trainer AI, and values a position by its state (HP,
survivors, items, weather turns, PP, stat stages). A play it misses is
fixed in that general machinery, never by adding a named behaviour, since
a scorer that plays only what its rules name would need a rule for every
team in the game. The planning ideas of the three-gym run are its exam,
not its rules.

## Move numbers and the move reworks

Move numbers follow the later games (Ian, 2026-09-26, the staples survey's
answer 1), priority included (2026-09-27), and the base ROM's own values
stay. Setup stays expensive: every stat-raising setup move is at 1 to 3 PP,
and the stat-lowering status moves at 3 to 6 (Sweet Scent 2, Defog 1,
Memento left as it is; Ian, 2026-10-02), which applies to any move added
later too. Sleep moves, powders, Thunder Wave, Dark Void
and Swagger keep their Generation 4 accuracy. Kaizo's changes come in only
as `docs/oxide/kaizo-comparison.md` lists (Ian's answers, 2026-09-27).
The rampage moves become one-turn moves, since a two- or three-turn lock
is too dangerous in a permadeath run (Ian, 2026-10-06): Thrash, Petal
Dance and Outrage take Kaizo's versions (Thrash 120 with a 20% paralysis
chance and a third of the damage as recoil; Petal Dance 100 with a 20%
confusion chance; Outrage 140 with half as recoil), and Uproar and Raging
Fury, which Kaizo lacks, get one-turn versions on the same pattern.
The other move reworks, as the learnset rewrite's report recommended
(Ian, 2026-10-06): Hyper Beam, Giga Impact, Rock Wrecker and Roar of
Time at 180, 100%, no recharge, half the damage as recoil; Blast Burn,
Frenzy Plant and Hydro Cannon without recharge, at 95% with Kaizo's
recoil and status; Sky Attack one turn (120, a third as recoil, 20%
paralysis); Dig 60 and Dive 80 one turn; Fly, Bounce, Phantom Force and
Shadow Force kept two-turn; every two-to-five-hit move at 25 a hit;
Fury Cutter as three rising hits (10, 20 and 30 since 2026-10-12, with
Triple Kick on the same effect at 20, 30 and 40, Ian); Psywave cut for Psybeam;
Spite at 5 PP; Uproar one turn at 100 with 20% confusion; Raging Fury
one turn at 120 with a third as recoil and 20% confusion.
Later the same day: one two-to-five-hit move per type. Normal keeps Fury
Swipes and Cinccino's Tail Slap; Double Slap, Comet Punch, Barrage and
Spike Cannon leave the game, their learners taking Fury Swipes or their
own type's multi-hit move; Bone Rush goes to 100%. The trainer AI rates a
multi-hit move on its expected hits (about 3.1, or 5 with Skill Link).
Uproar and Raging Fury hit one chosen foe.
Poison Fang takes Kaizo's 90 power and 40% chance to badly poison (Ian,
2026-10-06).

## Level-up lists

A level-up list may take any working move in Oxide that fits the line
(Ian, 2026-10-06, relayed by the balance track): "You should look at the
total pool of available moves for possible additions; future gen
learnsets (either via hg-engine or via looking them up) should be used as
inspiration, not as pick lists." A move a later game, Generation 4 or
Kaizo gives the line weighs in its favour; its absence there does not
rule it out. For alpha 1's rewrite Ian accepted two narrowings of the
generator (2026-10-06): a status move it adds must already be linked to
the line (canon, Kaizo or Oxide's lists), an unlinked attack comes in only
to fill a gap a rule asks for, and the attacks and utility moves it adds
keep under per-split ceilings, his answer 8 of 2026-09-27 (no ceiling on
coverage power) set aside for this pass.
From the learnset exam (Ian, 2026-10-06): a move meant only for trainers
never lands in a wild catch's four (it goes on the egg list, the trainers'
palette); two branches of one line are close in worth at the split where
the player chooses between them; a strong move below a line's catch level
moves to or after it; and Eevee's evolutions are the exception to the
stone rule's late, sparse lists, each learning a full moveset from 20, the
level Bebe's Eevee is held at.

## Trainer design

Trainer design at about 6/10 of Platinum Kaizo (Ian's answers to the Kaizo
team study, 2026-09-29). Bosses keep Kaizo's structure at reduced
lethality; an ordinary trainer carries one idea. One-hit KO moves never go
on a trainer, and evasion setups are rare. Trapping (the abilities, Mean
Look or Block with Perish Song, the binding moves) is allowed but rare. A
boss carries at most one forced trade (Explosion, Self-Destruct, Destiny
Bond), none before Fantina, and an ordinary trainer carries none. Custap
Berry and enemy priority are fair tools beside a trade: the player plays
around Custap with their own priority, and enemy priority is part of
planning (Ian, 2026-10-06, dropping the earlier "never made certain by
Custap or priority"). The 90 percent accuracy bar of the learnset rules
(R37) is for the player's movesets only, since the player plans around
low accuracy; trainers are welcome to moves like Sing and Zap Cannon (Ian,
2026-10-06). Luck items are allowed on trainers: Quick Claw, Focus Band,
King's Rock, Razor Fang and the like, his own teams' Quick Claws included
(Ian, 2026-10-06); the evasion items (BrightPowder, Lax Incense) stay
under the evasion-is-rare rule. A Focus Sash may go on a lead that carries
the boss's trade (Ian, 2026-10-06). No level-1 Focus Sash and Endeavor sets.
No overlevelled optional trainers. Every Pokemon on an enemy team holds
its own item and has its own nature, with no repeats within the team
(Ian, 2026-10-12). Oxide adds some double battles. An
ordinary trainer carries 3 to 5 Pokemon (6 is fine from Gardenia's split
on), team sizes vary from fight to fight, and ordinary trainers are
genuinely dangerous: two-Pokemon teams are too trivial (Ian, 2026-10-04).
Trainers may use TM and tutor moves freely (Ian, 2026-10-04). A move cut
from the TM list for the player's sake stays in the trainer palette of
every species that learned it by TM before the TM pass, as egg moves do,
and from Cyrus 3's split (Galactic) on a trainer's move need not be legal
for the species at all: late teams are "basically no holds barred" (Ian,
2026-10-07; the Overseer set the line at that split). A move on a team Ian
builds that its species cannot have at that level goes on the egg list of
the line's first stage, without asking him, and a level-up list never
moves for it, since that would change what the player gets (Ian,
2026-10-29: "just add it to their egg moves instead of asking for
permission"; "Don't shift move levels for what the player gets"). Each
goes in `learnrewrite.IAN_EGG_MOVES` too, so a generator write keeps it. Protect,
Detect, Double Team and every one-hit KO move leave every player-accessible list,
level-up, TM and tutor alike, and the one-hit KO moves leave every
moveset or become other moves (Ian, 2026-10-06). Teams
are judged against Oxide's box, not Kaizo's. Ian plans a boss by baiting
matchups in the order he wants, so the main tax on him is moveset overlap
and coverage, then switching or staying in by fight. A lead may be wholly
countered by one Pokemon, or by a whole type, when that answer draws in a
member that beats it and carries a setup move: a plan built on that answer
is untenable, since its switch out hands the setup member a free turn of
Swords Dance or Calm Mind (Ian, 2026-10-29, on Fantina's Runerigus). So a
lead, or any member, is judged by what its counters draw in after it, not
by how many counters it has. A trainer who turns, spins or walks (a
spinner) counts as optional, not mandatory, however its sight line falls,
and spinners are allowed to be harder than other ordinary trainers (Ian,
2026-10-29, on the mandatory fights of Fantina's and Maylene's splits,
which count 10 to 15 non-boss fights a split, gym trainers apart).
From Gardenia's redesign (Ian, 2026-10-13): a conditional move such as
Solar Beam may always be considered for a boss, with his okay when it
comes early (he kept it off his own sun team because its Drought sun
never ends, which makes it unconditional); a member may sit under its
evolution level, though not egregiously early; a trainer may know a
level-up move its species learns just after the split without any list
changing (Exeggutor's Egg Bomb at 27 in Gardenia's split); and a team may
be weaker than optimal on purpose (a Timid Solrock, a physical Exeggutor
on a lesser nature). A trainer's six IVs are one value, its iv_scale, so
a trainer's Hidden Power can only be Fighting or Dark.
The named Galactic fights are mostly anything goes, so long as each is
fun, interesting and thematic (Ian, 2026-10-13): their designs may break
the limits above (forced trades, Choice items and the rest) on purpose,
as Hesperid's and the Tyche and Hermes double's do. Each keeps its theme
across its fights, rising in power.
