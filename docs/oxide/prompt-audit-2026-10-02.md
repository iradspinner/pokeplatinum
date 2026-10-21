# Prompt audit of the Claude Code configuration, 2026-10-02

Run by the Oxide Overseer against the bundled `claude-api` skill's prompt-audit guide. Ian approved the diff the same day and it was applied whole, H1 to H9 and M1 to M7 (6f5d91eaed); the full audit, with its evidence and the diff, is this file in git history at 219576bd49. Cut to this record in the docs pass of 2026-10-21.

The five low findings were left flagged for Ian, and each still stands on 2026-10-21:

| # | Where | What |
|---|---|---|
| L1 | `.claude/skills/cloud-job/SKILL.md`, the model line | names a model and effort per job ("Opus 5.5 at Medium for a data pass"); state the criteria instead, or keep it as a dated choice |
| L2 | `.claude/skills/land-branch/SKILL.md`, its opening | "(under a minute)" for the merged build; landings run several minutes end to end |
| L3 | `.claude/skills/balance-rules/SKILL.md`, its opening | "Ian's rulings that until 2026-09-27 lived only in the Overseer's local memory", harmless history |
| L4 | `.claude/rules/standing-rulings.md`, the user settings ruling | Ian chose another route on 2026-10-02 for one install (the session builds the file, he approves it in `/permissions`), recorded only in local memory; whether the standing rule changes is his call |
| L5 | `CLAUDE.md`, Cloud sessions | "The environment passed its smoke test on 2026-09-25", a dated result in the always-loaded file |
