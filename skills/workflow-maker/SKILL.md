---
name: workflow-maker
description: >-
  Turn a process you run (or one you want someone else to run) into a prompt pack a stranger can
  paste and run. Numbered steps,
  one paste-able prompt per step, a line under each saying what good output looks like, and an
  honest run time, all written for one named tool (ChatGPT, Gemini, the Claude app, Cowork or
  Claude Code). Every tool, menu and setting a step names gets checked against live docs first.
  Use when the user wants to hand a process to a teammate, a client or a VA, write down how a job
  gets done so it stops living in their head, or hands over an idea and wants the exact prompts and
  run order. Triggers
  on "make a workflow", "workflow maker", "turn this into a workflow", "build me a prompt pack",
  "make this shareable", "give me the prompts for this", "write it so anyone can run it". It
  writes the pack. It does not run the workflow. To write and grade one single prompt, use
  `prompt-lab` instead.
license: MIT
---

# Workflow maker

Most shared prompt packs fail at step 2. A step names a menu that moved, a feature that needs a paid plan nobody mentioned, or an output the reader cannot judge. Alone at 9pm, with nobody to ask whether the odd-looking result is normal, they give up.

This skill builds the pack properly: numbered steps, one prompt each, a check the reader can fail under every step, an honest run time, and every named feature verified against live docs. It writes the pack. It does not run the workflow, spend credits, or do the job itself.

## Hard rules

1. **Verify before you ship.** Every tool, command, menu path, setting or toggle named in a step is checked against the vendor's live docs in this session. If it will not verify, cut it or replace it. Never ship it with a hedge: a caveat in a step hands the doubt to a reader who cannot resolve it.
2. **Name the tool from the reference, never from the look.** If the idea comes with a screenshot or video, read the on-screen app name, model name and UI text. A visual style is not evidence of which tool made it.
3. **One surface per pack.** A prompt that tells Claude to save a file breaks in a chat window. A prompt that says "now copy the output" wastes Claude Code. Pick one and write for it.
4. **One prompt per step, and it pastes clean.** One continuous paragraph, or intentional numbered points. Never hard-wrap a prompt: line breaks mid-sentence survive the paste.
5. **Every step gets a check the reader can fail.** "You get a numbered list where every action has one owner and a date" is a check. "You get a good result" is decoration.
6. **The run time is honest.** If it takes 40 minutes, say 40 minutes. An outcome line that promises 20 makes the reader feel lied to at minute 25.
7. **Files mean a safety line.** If any step points a tool at the reader's own files, the pack tells them to work on a copy first. Cowork and Claude Code can edit and delete inside a folder they have been given.
8. **It runs with nothing but the named tool.** No private skills, connectors or files the reader does not have.

## Step 1: Collect the inputs

You need three things. Ask only for what is missing, and never three questions when one will do.

1. **The idea or reference.** Required.
2. **What the runner ends with.** A weekly report, a cleaned spreadsheet, a client onboarding email, a proposal, a set of meeting actions. Be specific.
3. **The surface.** The tool the reader will run it in. For a pack going to someone else, ask which tool they already use. Do not assume they are on Claude.

If the idea makes the output or surface obvious, infer it and confirm at the end.

**Done when:** you can name the idea, the end output and the surface in one line each.

## Step 2: Lock the outcome

Write one line: what the runner has at the start, and what they have at the end. If you cannot state a clean before and after, the idea is not ready. Sharpen it with the user first.

**Done when:** the before and after fit in one sentence, with no "and also".

## Step 3: Shape it for the output and the surface

Write the structure of the finished thing first: its sections, its length, what it must contain. Then build the steps toward it, working backwards from the end.

If the user already does this job, ask them to walk you through the last time they did it, step by step. The real order and the real checks come from that, not from how the job "should" go.

Then read [references/surfaces.md](references/surfaces.md) for what the named surface can and cannot assume.

**Done when:** you have the structure of the finished output, and a list of what the surface can do.

## Step 4: Write the steps

Number them. One paste-able prompt per step, written for the named surface. Each prompt must survive a cold paste: assume the reader has only the surface and their own idea.

- **Carry-forward slot.** When a step needs an earlier step's output, use one line that works in a fresh chat or the same chat: `[PASTE THE ACTION LIST FROM STEP 2, or if you are in the same chat, write: the actions above]`.
- **Setup steps are the one exception.** Creating a project, uploading a file, choosing a folder: give the exact clicks plus any text to paste. "Set up your project as needed" is not a step.
- **Judge depth by reader effort, not step count.** A Cowork step does more than a chat step, so the same job takes fewer steps.
- **Fill "Before you start".** What they need, stating free versus paid plainly, and what to have to hand. Anything that would stop them at step 1 goes here, not at step 4.

**Done when:** every step is a full prompt or exact clicks, and no step refers to something the reader cannot see.

## Step 5: Add what good looks like, and the run time

Under every step, one line telling the reader how to know it worked. Make each one checkable: a count, a length, a named section, a file that appears.

Then add up the run time end to end, including reading and pasting. State it plainly at the top.

**Done when:** every step has a check the reader could fail, and the outcome line and run time agree.

## Step 6: Verify every named thing

Go through the pack line by line. For every tool, model name, menu path, setting, command or plan tier, find it in the vendor's current docs and note the page. Fix or cut anything that does not verify. For Claude Code commands, check `code.claude.com/docs`. If a vendor's page blocks the fetch, search limited to that vendor's own site and quote the result. If that fails too, name the one fact and ask the user to confirm it on their own screen.

Treat this skill's own reference files as briefings, not proof. Products change monthly, and a confident note goes stale without anyone noticing.

**Done when:** every named feature has a docs page from this session behind it, or has been cut.

## Step 7: Package it

Fill [references/pack-template.md](references/pack-template.md). Ask the user where to keep their packs. If they have no preference, use a `workflow-packs/<slug>/` folder in the current project. The slug is 3 to 5 words, input to output: `call-transcript-to-client-update`. Save it as `pack.md`.

In Claude Code, turn it into a clean, self-contained web page:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/build_pack.py" workflow-packs/<slug>/pack.md
```

`${CLAUDE_SKILL_DIR}` is the folder this skill is installed in, so the command works for a plugin install and a copied folder alike. If it comes up empty (outside Claude Code), use the path of the folder this SKILL.md sits in.

It writes `pack.html` next to the markdown. The markdown is the source. Never edit the HTML by hand, regenerate it. In the Claude app, skip the script and give the user the markdown.

Then look at the page, not the markdown. If you can view it, check that no prompt block runs off the edge. If you cannot, ask the user to open `pack.html` and check that one thing.

**Done when:** `pack.md` and `pack.html` exist, and someone has looked at the rendered page.

## Step 8: Score it before the user sees it

Sweep for `TODO`, `PLACEHOLDER`, `NEEDS:`, `NOT RUN` and any unfilled `{{UPPER_CASE}}` template token first. A merge tag such as `{{ first_name }}` that the reader's tool needs is content, not a token. None of them reach the user. Then score honestly:

| # | Check | Points |
| --- | --- | --- |
| 1 | Every step is a full paste-able prompt, or exact clicks for a setup step. No gaps | 20 |
| 2 | Tool named from the reference. Every tool, command and setting verified in this session | 20 |
| 3 | Runs on the named surface with nothing private required | 15 |
| 4 | Every step has a check the reader could fail | 15 |
| 5 | Every prompt pastes clean, with no line breaks mid-sentence | 10 |
| 6 | A reader following the steps reaches the promised outcome | 10 |
| 7 | Run time honest. "Before you start" complete, with the safety line where files are involved | 5 |
| 8 | Plain, short sentences in everything around the prompts | 5 |

95 passes. 94 goes back for another pass. A rewrite voids the old score.

Then ask the harder question: would this work for someone with none of your context? A pack that scores 95 and still leaves the reader stuck at step 4 has failed. Close that gap before you hand it over.

**Done when:** the pack scores 95 or more, and you can name the step a stranger is most likely to stall on and what you did about it.

## Step 9: Hand it over for a real test

Give the user both file paths and the score, with the rows that lost points. Tell them to run the pack once themselves, cold, before they share it. If a step is weak in their test, fix `pack.md`, regenerate the page and hand it back.

**Done when:** they have both paths and know to run it once before sharing.

## The shape of a finished step

````markdown
### Step 2: Pull out the actions

Paste this into ChatGPT:

```
Here are my meeting notes: [PASTE THE CLEANED NOTES FROM STEP 1, or if you are in the same chat, write: the notes above]. List every action agreed in the meeting. For each one give the task in under 12 words, one owner by name, and a due date. If the notes give no date, write "no date set" rather than guessing one. Number them.
```

What good looks like: a numbered list where every line has a task, one name and either a date or "no date set". No line has two owners.
````

## What this does not do

- It does not run the workflow, test it with real credits, or do the job itself.
- It does not publish or host the pack. Where it goes is the user's call.
- It does not write one pack for several surfaces or several outputs. One of each, done properly.
- It does not trust its own reference files over live docs.
