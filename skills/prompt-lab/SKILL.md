---
name: prompt-lab
description: >-
  Turn an idea for a prompt into a finished, tested prompt in one turn. You type the idea, and the
  prompt comes back in a code block, graded out of 100 against Anthropic's current published
  prompting guidance (fetched live every run) and a plain bar any reader can run. The pass mark is
  95, and Claude runs the prompt itself before handing it over whenever it can. Use when the user
  wants a prompt written, improved or checked. Triggers on "prompt lab", "write me a prompt",
  "make this prompt better", "grade this prompt", "score this prompt", "is this prompt any good",
  "make this prompt expert level". To package a whole multi-step process for other people, use
  `workflow-maker`.
license: MIT
---

# Prompt lab

Most prompts that get shared were never run. They were graded, if at all, against rules someone remembered, and prompting advice moves every time a model ships. So the prompt reads well, then falls over the first time a stranger pastes it into a fresh chat.

This skill writes one prompt properly: graded against guidance fetched this turn, held to a bar a non-developer can run, and run by Claude before you see it. It makes one prompt. It does not package a whole process for an audience (that is `workflow-maker`).

## Hard rules

1. **The finished prompt comes back in the same turn, in a code block.** Never a template to fill in, never a command for the user to run. Ask a question only when two readings of the idea would produce materially different prompts. Otherwise state your assumption in one line and write it.
2. **Fetch Anthropic's guidance live, every run.** Never grade from memory or from a list baked into this skill. Techniques fall in and out of favour between model releases, so a remembered rubric becomes the stale advice it was meant to catch. If URL 1 fails, the Anthropic half is NOT RUN, and there is no total out of 100. If only URL 3 fails, grade from URL 1 and name the URL that failed.
3. **Every point lost has a reason.** A score with no evidence behind it is a guess.
4. **Run it before you hand it over, whenever you can.** If the prompt needs nothing you lack (a file, a connector, a paid tool, a person), run it on a realistic sample input and check the output against every finish line. If you cannot run it, write TEST RUN: NOT RUN and the reason.
5. **The pass mark is 95.** Below it, fix and re-grade. Never round a 93 up, and never call a prompt finished that scored under 95.
6. **Quote, never invent.** Every Anthropic row quotes a sentence from a page you fetched in this run.

## Step 1: Pin the job

From the idea, settle four things. Infer them. Do not interview the user.

| Question | Default if the idea does not say |
| --- | --- |
| Who runs it? | A busy person who uses AI daily and does not code |
| Where? | Any chat assistant (Claude, ChatGPT, Gemini) on a free or entry plan |
| What do they bring? | The smallest input that does the job: a paste, a link, a short answer |
| What do they get back? | One concrete thing they can use straight away |

Write the outcome as one plain sentence: what the prompt does for the person running it.

**Done when:** the outcome sentence is under 25 words and a stranger would know whether they need this prompt.

## Step 2: Fetch the guidance

Fetch these in this run. In the Claude app this needs web search or web fetch switched on.

1. `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices`, the living reference for current models.
2. Its model-specific section, if the prompt is meant for one particular model.
3. `https://claude.com/blog/best-practices-for-prompt-engineering`, the general craft post.

From what you fetched, list the general techniques the page currently recommends for every prompt. Quote one sentence per technique. Include a technique only if the page presents it as applying to all prompts. Leave out sections that only apply to tools, code, agents or long documents unless this prompt needs them. If the pages disagree, the platform docs page wins. Leave out any technique a chat user cannot do, such as prefilling or setting a system prompt. List each one you left out, with the reason, under the grade. Then split 50 points as evenly as you can across that list, in whole numbers that add up to 50.

**Done when:** you hold a list of techniques, each with a quoted sentence and a point value, adding to 50, plus a list of what you left out and why. Or the half is marked NOT RUN, with the URL that failed.

## Step 3: Write the prompt

Write it to the techniques you fetched. Where the page and this starting shape disagree, the page wins.

```text
You are [one sentence: who the model is being for this job].

<context>
[Who is running this and what they are trying to get done. Say why it matters, so the model can handle cases you did not list.]
</context>

<task>
[What to do. Numbered when the order matters. Say what to do rather than a list of don'ts.]
</task>

<output_format>
[The shape: a table with named columns, a word limit, a number of bullets. "Something useful" is not a shape.]
</output_format>

<examples>
<example>[A short worked example]</example>
<example>[A second example that differs in topic and length]</example>
<example>[A third example, different again, so the model does not copy one pattern]</example>
</examples>

Ask me for [the input] and wait for my reply before you start.
```

Then hold it to the portable bar, which Step 4 grades:

- **Runnable by a non-developer.** No code, no terminal, no files or tools the reader does not have. If it needs a paid plan or a connector, say which on the first line of "Before you start".
- **Safe to paste cold.** It works in a brand new chat with no memory, no custom instructions and no earlier messages. No line breaks in the middle of a sentence, because they survive a paste badly. Every slot the reader fills is in [square brackets]. It asks for its input and waits, so the model does not invent something to work on. Output placeholders inside the prompt use <angle brackets>, so square brackets only ever mean 'you fill this in'.
- **A checkable finish line per step.** Under the prompt, one line per step saying what good output looks like. It must be specific enough to be wrong. "It should be helpful" fails. "A table with exactly 5 rows, each with a price and a source link" passes.
- **Plain words.** Short sentences. No word a non-developer would have to look up.

A prompt with more than one step gets one code block per step, each with its own finish line.

**Done when:** the prompt is in a code block, and every step has a finish line under it.

## Step 4: Grade it

First, calibrate. Grade this weak prompt silently: `Write me a marketing email.` It should land under 40. If your grading gives it more, you are scoring too kindly. Tighten before you grade the real one.

Then grade the real prompt. Each row is PASS (full points), PARTIAL (half, rounded down) or FAIL (zero).

**Half A: Anthropic's guidance (50).** One row per technique from Step 2. In a chat paste, grade the role row on the prompt's first line.

**Half B: the portable bar (50).**

| Item | Points | Fails when |
| --- | --- | --- |
| Runnable by a non-developer | 15 | It needs code, a terminal, a file or tool the reader lacks, or an unnamed paid plan |
| Safe to paste cold | 15 | It leans on earlier chat, memory or files, breaks mid-sentence, or starts work without asking for its input |
| A checkable finish line per step | 10 | Any step has no finish line, or a finish line could never be wrong |
| Plain words | 10 | Any word a non-developer would look up, or sentences that run past about 25 words |

Under 95: fix the lowest-scoring rows, then grade again. After three rounds still under 95, stop and hand over with the label BELOW THE BAR and the one thing blocking it.

**Done when:** every row has a status, points and a reason, and the total is 95 or more, or labelled BELOW THE BAR.

## Step 5: Run it

If Rule 4 allows, write a realistic sample input (not a perfect one), run the prompt on it, and check the output against each finish line and against the outcome sentence from Step 1. If it meets every finish line but would not do the job, a finish line is missing: add it.

- **In Claude Code:** send the prompt alone to a fresh subagent and check it asks and waits. Then send the prompt, a line 'My reply:' and the sample input as one message to a second fresh subagent. Say the run was near-cold, because a subagent still loads your CLAUDE.md, and ignore any lines it adds about who sent the input.
- **In the Claude app:** run it inside your own reply, and say the run was not cold, because you could see this conversation.

If a finish line fails, the prompt is wrong, not the run. Fix the prompt, then go back to Step 4.

**Done when:** every finish line is marked MET or MISSED against a real output, or the run is NOT RUN with a reason.

## Step 6: Hand it over

Use this shape. Nothing before it except, at most, the one-line assumption from Rule 1.

````text
**[Name of the prompt]**: [the outcome sentence]

```text
[the prompt, exactly what gets pasted, nothing else inside the block]
```

**Before you start:** [plan or tool, and what to have ready]

**What good looks like:**
1. [finish line for step 1]

**Grade: 96/100** (Anthropic 47/50, portable 49/50)

| Row | Points | Status | Why |
| --- | --- | --- | --- |
| [technique, with the quoted line] | 8/8 | PASS | [evidence from the prompt] |

**Left out of the grade:** [technique]: [reason, for example a chat user cannot set a system prompt]. Or: none.

**Test run:** PASS, every finish line met on a sample [describe input]. Or: NOT RUN, [reason].
**Guidance fetched:** [URLs], [date]
````

If the Anthropic half was NOT RUN, replace the grade line with `Grade: portable half 48/50. Anthropic half NOT RUN, [URL] did not load. No total.`

## When the user brings an existing prompt

| They say | Do this |
| --- | --- |
| "grade this prompt", "is this any good" | Skip Step 3. Grade it as it stands, run it if you can, then give the improved version underneath with its own grade |
| "make this better", "make it expert level" | Keep their intent and their wording where it works. Rewrite the rest through Steps 3 to 6 |
| "write me a prompt that..." | The full run, Steps 1 to 6 |

## What this does not do

- It does not keep a library of prompts or track which ones you used.
- It does not package a multi-step process for other people to run. That is `workflow-maker`.
- It does not audit your CLAUDE.md, custom instructions or skills.
- It does not spend money or run anything that needs your login.
