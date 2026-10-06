## What it does

Reads the prompts you typed into Claude Code over the last week, finds the corrections you keep giving, and fixes each one in the right file. It also finds jobs you type again and again (a skill waiting to be written) and context you keep pasting in (a fact your setup should already hold).

The best findings are repeats. "Still", "again" and "how many times" mark a mistake that came back after you corrected it. Something should already have stopped it, so the fix is in the setup, not in the next prompt.

## When to reach for it

You type `/improve-system`, once or twice a week. Add a topic to audit one kind of work: "improve-system for my emails".

| You want | Use |
| --- | --- |
| The lessons of one session | [close](./close.md) |
| Your patterns across weeks | `improve-system` |

## What you need first

Claude Code, and about a week of normal use. The miner script reads your local prompt history and writes a dated report. Nothing leaves your computer.

## Three verdicts

Each finding gets one: **no rule** (write one), **rule not working** (shorten it, move it, or turn it into an automatic check), or **rule wrong** (the rule caused the problem).

## Common questions

**It flagged something that was not a correction.**
The detector is a phrase list, so it raises some false alarms. The skill treats each quote as a claim and drops the ones that are not real corrections.

## It's working if

- The same correction stops showing up in next week's report.
- New rules are one to three lines long.
- You approve each change before it lands.

## Where it fits

Weekly maintenance. It follows [close](./close.md), which learns from one session, by learning from a whole week.
