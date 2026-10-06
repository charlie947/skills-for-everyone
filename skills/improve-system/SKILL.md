---
name: improve-system
description: >-
  Mine your own Claude Code history for what keeps going wrong, then fix it at the source. Finds
  corrections you had to give more than once (a rule should have stopped them), jobs you keep
  typing by hand (a missing skill), context you keep pasting in (a missing fact), and the kinds of
  work eating the most hours. Use when the user says "improve the system", "improve my setup",
  "what am I correcting", "what keeps going wrong", "mine my history", "what skills should I
  build", "why do I keep repeating myself", or once or twice a week as a routine. Also use with a
  topic to audit one kind of work that has drifted ("my emails got worse"). For the lessons of one session, use `close`.
license: MIT
---

# improve-system

You correct Claude, it improves for one chat, and next week you give the same correction again. Your own history already records every one of those moments. This skill reads it, finds what keeps coming back, and fixes it in the right place so you stop repeating yourself.

## Step 1: Run the miner

The miner is a small Python script that ships with this skill. It reads the prompts you typed into Claude Code (`~/.claude/history.jsonl`). It changes nothing.

Run the miner from this skill's folder:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/improve-system.py" --days 7
python3 "${CLAUDE_SKILL_DIR}/scripts/improve-system.py" --days 7 --topic 'email|inbox|reply'
```

`${CLAUDE_SKILL_DIR}` is the folder this skill is installed in, so the command works for a plugin install and a copied folder alike. If it comes up empty (outside Claude Code), use the path of the folder this SKILL.md sits in.

The first is the whole setup. The second narrows it to one kind of work. It finishes in a second or two and writes a dated report, plus a `.json` file with every correction quote, to `~/.claude/logs/improve-system/`. Read the JSON, not just the summary.

If it says there is no history, the user has not used Claude Code on this computer yet. Stop and tell them to come back after a week of normal use.

The correction detector is a phrase list. It catches most pushback and some false alarms. Treat each quote as a claim, and drop the ones that are not really a correction.

Done when: the report and JSON paths are printed and you have read the JSON.

## Step 2: Turn quotes into findings

For each area of work, read the REPEAT quotes first. A repeat ("still", "again", "haven't", "how many times") means a mistake came back after it was already corrected. That is the most valuable finding, because something should already have stopped it.

Group quotes by MEANING, not by word. One finding is one failure, with:

- the quotes that prove it (date and words), and how many sessions it hit
- what in their setup should already prevent it. Search their `CLAUDE.md` files, memory files and skills for it
- the verdict:
  - **NO RULE.** Nothing tells Claude this. Write one.
  - **RULE NOT WORKING.** A rule exists and sessions still miss it. It needs to be shorter, moved somewhere Claude reads first, or turned into an automatic check.
  - **RULE WRONG.** The rule itself caused the problem. Fix or remove it.

Rank by sessions hit times repeats. Report every finding. The user decides what matters, so never cap the list.

Done when: every correction quote sits in a finding with a verdict, or is dropped as not a correction.

## Step 3: The other three sections

- **Repeated asks.** A job typed in 3 or more sessions with no skill behind it is a skill to write. The "nearest skill" column is only a keyword guess. Open that skill before saying it already covers the ask. Ignore prompts like 'test' or 'hello' that you typed to check something worked.
- **Re-pasted context.** The same paste in 2 or more sessions is a fact the setup should already hold. Put it where Claude will find it (see the table below).
- **Time sinks.** Hours and corrections per area of work. An area with high hours AND high corrections is where a skill or a better instruction pays off most. Name the step that eats the time. Domains are a keyword guess. Merge sessions that are the same job before ranking time sinks.

Done when: every repeated ask, re-pasted paste and time sink has a line in your findings.

## Step 4: Fix, do not just list

Each fix goes in the smallest place that works:

| What you found | Where the fix goes |
| --- | --- |
| A rule for every session, everywhere | `~/.claude/CLAUDE.md`, as 1 to 3 plain lines |
| A rule for one project folder | `CLAUDE.md` in that folder |
| A rule for one kind of job | The skill that does that job, or a new skill |
| A fact Claude keeps needing (a price, a name, a process) | A memory note, or a short reference file the right skill points to |
| A job typed again and again | A new skill. Use the built-in skill creator if it is available |

Rules for fixing:

- Show each proposed change before you make it, and back the file up first: `cp <file> "<file>.$(date +%Y%m%d-%H%M).bak"`.
- Never delete an existing rule without asking. It may be there for a reason this week's history does not show.
- Keep every new line short. A long CLAUDE.md is read less carefully, which is how rules stop working.
- Taste stays theirs: tone, design, what to post. You fix the setup, not their judgement.

Done when: every approved fix is in its file with a dated backup beside it, and you have read the file back.

## Step 5: Report

Show the user one page (use the `show-me` skill if it is installed): the ranked findings, what was fixed and where, and what needs their decision. Print the report's file path on its own line.

Done when: the user has the page in front of them and the report path is printed.

Run it again in a few days. The test that it worked: the same correction does not come back.

## What this does not do

- It reads only your Claude Code folder: prompt history, pasted text, skills, CLAUDE.md and memory files.
- It does not send your history anywhere. The script runs on your computer and only writes a local report.
- It does not change anything without showing you first.
