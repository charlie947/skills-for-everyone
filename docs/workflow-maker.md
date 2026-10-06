## What it does

Turns an idea or a reference into a prompt pack a stranger can paste and run. You get numbered steps, one paste-able prompt per step, a line under each step saying what good output looks like, and an honest run time. Every pack is written for one named tool: ChatGPT, Gemini, the Claude app, Cowork or Claude Code.

Every tool, menu, setting and command a step names is checked against the vendor's live docs before the pack is finished. Anything that will not verify gets cut, not hedged. That check is what separates a pack that runs from a list of clever prompts.

## When to reach for it

Type `/workflow-maker`, or Claude reaches for it when you say "turn this into a workflow", "build me a prompt pack" or "write it so anyone can run it".

| You want | Use |
| --- | --- |
| A pack someone else runs to produce a report, an email or a cleaned file | `/workflow-maker` |
| A reusable job for yourself inside Claude Code | A skill, not a pack. Ask Claude Code to write one with you |

It writes the pack. It does not run the workflow or do the job itself.

## What you need first

Nothing to write the pack. In Claude Code, a small script also turns the pack into a self-contained web page with a Copy button on every prompt. In the Claude app you get the markdown instead.

## What good looks like

The line under each step is the heart of the pack. It has to be a check the reader could fail: "every action has one owner and a date" passes, "a good result" does not. It is what lets someone working alone tell whether an odd-looking output is normal.

The pack scores itself out of 100 before you see it. 95 passes. Anything less goes back for another pass.

## Common questions

**Why does it re-check facts its own reference files already state?**
Because those files go stale without anyone noticing. Products change their plans, platforms and menus every month. A confident note about which systems a tool runs on was once months out of date, and only the live-docs check caught it.

**Why does it not default to Claude?**
Many people you hand a pack to do not use Claude. A pack that needs a tool they do not have will never get run. So it asks which tool they already use.

**Why does the run time matter so much?**
An outcome line that promises 20 minutes for a 60-minute workflow loses the reader at minute 25, before they reach the good part.

## It's working if

- Someone who has never spoken to you runs the pack and reaches the promised output.
- No reader writes back asking where a menu or setting is.
- Every prompt pastes into the chat box without editing.

## Where it fits

A reach-for-it-anytime standalone, for when a process you run should become something other people can run. Use [show-me](./show-me.md) to put the finished pack page in front of you.
