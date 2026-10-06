# The plugins installed on 2026-10-06, and what Oxide takes from them

Ian installed six plugins from the Anthropic plugin directory on 2026-10-06
and asked which features the project should adopt. These are the Overseer's
verdicts and his answers. The next `/docs-pass` or `/qa-pass` reviews them
again (the tracker's Scheduled list), to adopt or drop what is marked "later".

## Done on 2026-10-06

**superpowers is off for this project** (Ian's yes). Its start-up hook injects
about 500 words headed "EXTREMELY_IMPORTANT" into every new, cleared or
compacted session, in every project: invoke a skill before any reply, run its
2,600-word brainstorming interview before any plan, announce each skill used.
Here that competes with the `oxide-session` skill and with how Ian wants
questions brought to him, and it costs tokens at every start and compaction.
`.claude/settings.json` sets `"superpowers@anthropic-plugin-directory": false`
under `enabledPlugins`. The check: a new session in this repo lists no
`superpowers:` skills and carries no "You have superpowers" text. Ian may
bring over anything else of value later.

**Two of its ideas kept by hand.** Its verification skill's "evidence before
claims" (no claim of done, fixed or passing without the output in hand) is
now part of the standing rule on framing work as checks (Ian's yes). Its
debugging skill's "root cause before fix" is already how the `debug-live`
skill works.

## For the next docs or QA pass

| Plugin | What it offers | Verdict |
|---|---|---|
| feature-dev | three agents: code explorer, code architect, code reviewer | later: try the reviewer as a local second read of C changes before a landing; never built into a procedure without Ian's word, as with the cloud review |
| claude-md-management | an audit skill for CLAUDE.md files, and a command that writes a session's learnings into CLAUDE.md | later, occasionally: it overlaps `/docs-pass` and the prompt audit of 2026-10-02; its learnings command must respect the rule that durable facts go to the design doc and rulings to the standing rulings |
| skill-creator | skill writing, with evals of whether a skill triggers when it should | later: evals could test whether the project's skills (`oxide-session` first) fire when they should |
| code-review | a command that reviews a GitHub pull request | no: Oxide lands branches with `merge-branch.sh`, not pull requests |
| code-simplifier | an agent that tidies recently changed code | no need now |
| superpowers, the rest | planning, plan execution, subagent-driven work, worktrees, finishing a branch, test-driven development | covered by the project's own skills (`land-branch`, `merge-branch.sh`, the scoring track's per-fix checks); revisit only if Ian asks |
