# Quality bar

Internal file. Remove it before this pack is published.

Two public skill packs were read in full on 05/10/2026 to set this bar: an engineering pack (277k stars) and a design pack (43k stars). Both are MIT. This is what they do that this pack must match, and how this pack is scored against each line.

## What the reference packs do

| # | What they do | How we match it |
|---|---|---|
| 1 | One folder per skill under `skills/`, one `SKILL.md` each, extra files beside it only when the skill loads them | Same layout. Scripts sit in `skills/<name>/scripts/` |
| 2 | README opens with one line on who it is for and the problem it fixes, before any install step | First lines name the reader (non-developers) and the gap (every other pack is for engineers) |
| 3 | A "Reference" list: every skill on one line, linked to its `SKILL.md` | Same, plus the exact words to type for each |
| 4 | Install is one or two copy-paste commands in code blocks, near the top | "Install in 2 minutes", each command followed by what you should see |
| 5 | A plugin manifest (`.claude-plugin/plugin.json` and `marketplace.json`) so the pack installs as one bundle | Both files present, pass `claude plugin validate`, and install through `/plugin` |
| 6 | Each `description` says what it does AND when to use it, with the trigger phrases a user would type | Every description carries both, under the 1,536 character listing cap |
| 7 | The skill body opens with the failure it fixes, in one or two lines, then the method | Every skill opens on the failure |
| 8 | Hard rules and a numbered workflow, each step with a clear finish line | Numbered phases or steps in every skill |
| 9 | Says what the skill does NOT do, and points to the right tool instead | A "What this does not do" or "Break these rules when" section in every skill |
| 10 | Small and composable. No dependency on the author's private setup | No personal paths, names, IDs, hooks or private skills. Works on a fresh install |
| 11 | MIT licence file at the root | LICENSE present (licence choice is Charlie's to confirm) |
| 12 | Worked examples and paste-able templates inside the skill, not described in prose | Board template (show-me), ledger (close), report table (improve-system), pack template (workflow-maker) |

## Ship gate (added 06/10/2026)

The 12 lines are the floor, not the bar. The reference packs are trusted because their skills have been run many times. So every skill here also needs a clean cold run by a stranger before it ships. A skill that cannot pass is held back, not shipped weaker. See CONTRIBUTING.md.

How a finding closes: a BLOCKER is fixed, then re-run against the exact case that failed. A MINOR finding is closed when the tester's own fix is applied as written, or reworded only where the literal fix would break something, with the reason recorded.

## Where this pack goes further, for its reader

- Plain English throughout. No assumption that the reader writes code.
- Every install command says what you should see, so a non-developer knows it worked.
- Frontmatter uses only `name`, `description` and `license`, so each skill also works as a claude.ai upload.

## Score (06/10/2026, 7 skills, from the files on disk)

| # | Result | Evidence |
|---|---|---|
| 1 | PASS | 7 skill folders, 3 scripts, 2 skills with bundled references |
| 2 | PASS | README hero names the reader and the gap |
| 3 | PASS | "Which skill do I need?" table, 7 rows, one per skill. The Reference list links each skill |
| 4 | PASS | Copy route into a fake home folder: 7 of 7 skills installed |
| 5 | PASS | `claude plugin validate . --strict` passed. Marketplace add and install in an isolated config: 7 SKILL.md files installed |
| 6 | PASS | Descriptions 547 to 915 characters, all parse with a strict YAML parser, keys name, description and license only |
| 7 | PASS | Each skill opens on the failure it fixes |
| 8 | PASS | Numbered steps or phases in all 7 |
| 9 | PASS | A "does not do" section in all 7 |
| 10 | PASS | Sweep of skills/ and docs/ for personal paths, team names, IDs and private tools: none. The README carries the public author byline only |
| 11 | PASS | MIT LICENSE at the root. answer-first also ships its own copy, so a single-folder install keeps the third-party credit |
| 12 | PASS | Templates and worked examples sit inside each skill's references/ folder |

Cold runs: three rounds, each by a fresh agent with an invented business and a fake home folder, no live connectors. Round 3 found blockers in workflow-maker and improve-system, and in two skills since cut. Each was fixed and re-run against the case that failed. Every minor finding was applied using the tester's own wording.

Gaps found during scoring and fixed: the plugin name started with `claude-`, which Anthropic reserves (renamed). The `close` description broke YAML parsing, so one installer skipped it (fixed). The npx install route the reference packs offer was missing (added and tested).

Not matched on purpose: a newsletter sign-up link in the README. That is Charlie's call.
