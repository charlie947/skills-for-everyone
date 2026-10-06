## What it does

You type the idea for a prompt. A finished prompt comes back in the same turn, in a code block, graded out of 100 and run by Claude before you see it.

It never grades from memory. Half the score comes from Anthropic's current prompting guidance, which it fetches fresh every run, because that advice changes when a new model ships. If the fetch fails, that half is reported as NOT RUN and there is no total. The other half is a plain bar: a non-developer can run it, it works pasted cold into a new chat, every step has a finish line, and the words are plain. The pass mark is 95.

## When to reach for it

You type `/prompt-lab` and the idea, or say "grade this prompt". Claude will not reach for it on its own.

| You want | Use |
| --- | --- |
| One prompt, written or fixed | `/prompt-lab` |
| A whole process packaged for other people to run | [workflow-maker](./workflow-maker.md) |

## The finish line

Every step of a prompt gets one line saying what good output looks like, written so it could be wrong. "It should be helpful" never fails, so it tells you nothing. "A table with exactly 5 rows, each with a price and a source" fails the moment the output drifts. Claude runs the prompt on a sample input and marks each finish line met or missed. In Claude Code, the run goes to fresh helpers with no other context. That is close to a cold paste, though a helper still loads your CLAUDE.md.

## Common questions

**Why does it say NOT RUN instead of a score?**
The live fetch of Anthropic's guidance failed, or the prompt needs something Claude does not have, such as your login or a paid tool. A score built on remembered rules would look finished and be wrong. In the Claude app, switch on web search and run it again.

## It's working if

- Each prompt you paste into a new chat works first time, with no follow-up questions.
- Every point lost in the grade table has a reason you can see in the prompt.
- The guidance line at the bottom shows today's date.

## Where it fits

A reach-for-it-anytime standalone. When one good prompt grows into a process other people will follow, hand it to [workflow-maker](./workflow-maker.md).
