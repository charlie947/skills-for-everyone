---
name: close
description: >-
  End a good session properly. Banks what the session taught into Claude's memory so the next
  session starts smarter, finishes every loose end it can, proves the changes actually landed, and
  hands back only what genuinely needs you. Four phases, in order: LEARN, FIX, PROVE, REPORT. Use
  when the user says "close", "/close", "close out", "wrap this up", "are we good to close?",
  "what's still open?", "anything left?", "did we miss anything", "save progress", "bank what we
  learned", "remember this for next time", "lock in our corrections", or otherwise signals a
  session is ending. Not for handing work to another person. To find mistakes that repeat across many sessions, use `improve-system`.
license: MIT
---

# Close

**One skill, four phases, in this order: LEARN, FIX, PROVE, REPORT.**

Two failures, one fix. The first: you correct Claude all session, close the window, and next week it makes the same mistakes, because nothing wrote the lessons down. The second: the session ends with a nine-item list of things you now have to do. Remembering every loose end and handing them all back has moved the work sideways, not forward.

So the job is: bank what is worth keeping, finish every loose end you can, prove it, and hand back only what is genuinely theirs. Then say plainly whether anything is still open.

## Only run LEARN on a session that went well

This skill turns what happened into standing instructions. On a bad session it writes the WRONG behaviour into memory, and every future session inherits it.

**The test: would the user be happy for the next session to work the same way?** If no, say so. Skip the banking in PHASE 1, still run FIX and PROVE, and say in the report that nothing was banked because the session was not one to learn from. **Still run 1.4, the friction sweep.** A bad session is where the friction is, and fixing its cause is the one lesson it does teach.

---

# PHASE 1: LEARN. Bank what the session taught, and reject most of it.

## 1.1 Find where memory lives

On a standard Claude Code install, memory lives in these places. Check which exist before writing anything.

| File | What it is for |
| --- | --- |
| `~/.claude/CLAUDE.md` | Rules for every session, in every folder |
| `./CLAUDE.md` in the project folder | Rules for this project only |
| `~/.claude/projects/<project>/memory/MEMORY.md` plus topic files | Claude Code's auto memory, if it is switched on. `MEMORY.md` is an index, one line per memory. Only its first 200 lines load at the start of a session, so keep it short. The folder name is the project's full path with every / turned into - |
| A skill's own `SKILL.md` | Rules for one kind of job |

If you cannot tell which project the session belonged to, ask before writing. Writing to the wrong memory is worse than writing nothing.

## 1.2 Read the WHOLE conversation, not your memory of it

A summary of the conversation is not evidence. Read the user's actual messages. This skill ships a script that finds all of them:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/session-turns.py"            # every message in this session
python3 "${CLAUDE_SKILL_DIR}/scripts/session-turns.py" --craft    # only feedback on writing, tone or visuals
```

`--craft` is a filter, not the sweep. Read the full list too.

`${CLAUDE_SKILL_DIR}` is the folder this skill is installed in, so the command works for a plugin install and a copied folder alike. If it comes up empty (outside Claude Code), use the path of the folder this SKILL.md sits in.

Use the script, not a quick hand-made reader. A quick reader misses messages the user sent while you were still working, and messages sent beside an image. In real sessions that is often half of everything they said, and it includes the most important notes. If the script cannot run, read the transcript yourself and say which messages you could not check.

## 1.3 Sweep craft feedback separately

Process failures announce themselves: a command errored, a file was missing. They get banked. **Craft feedback arrives as a reaction to one sentence or one picture, is worded softly, and looks like it applied only to that one passage.** It is the half that gets lost.

So run a second pass over the user's messages, looking only for craft: "too long", "sounds like AI", "I prefer how it was", "wrong tone", "too much text", "I don't love this".

**The test that separates a craft rule from a one-off:** would they give the same note on a DIFFERENT piece? "This paragraph is too long" is a one-off. "Don't open sentences with a bare list of nouns" is a rule, and it earns a sweep across the whole piece.

## 1.4 Sweep the friction: where did this session cost them?

1.2 and 1.3 find what the user taught. Neither looks for where they had to push: a correction, the same ask twice, a chase, a "what do you mean", an "ugh". Each of those is a turn they should not have had to spend, and the cause sits in the setup, not in them.

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/session-turns.py" --friction   # tagged CORRECTED, RE-ASKED, CHASED, CONFUSED or FRUSTRATED
```

The tags are a guess from wording. Read each tagged message and the reply before it, drop the false hits, and group the real ones by cause. Then write one line for each pain point:

| They had to | Messages | Cause | Fix at the source |
|---|---|---|---|
| their words, quoted | n | the rule, skill or habit that let it happen | the edit that stops it next time |

**The cause is never "the user was unclear".** If they had to explain twice, the first reply missed what was in front of it. Name the step that missed it: a rule nobody reads, a skill that does not ask, a default that guessed, a check that passed something wrong.

Fix each real pain point in PHASE 2: a skill edit, or a memory rule (it still has to pass the admission test in 1.6). A pain point fixed only in this session's output is not fixed. One that already has a rule which did not work needs a stronger mechanism, not firmer wording.

Done when: every tagged message is confirmed with a cause and a fix, or dropped as a false hit.

## 1.5 Sort each candidate into one of four buckets

| Bucket | What it is | Where it goes |
| --- | --- | --- |
| **Durable rule** | Should apply to every future job of this kind | CLAUDE.md, or the skill that owns that job |
| **One-off override** | True for THIS piece only | Nowhere permanent. Mention it in the report |
| **Project state** | What shipped, what is open, what you are waiting on | Project notes or the project's CLAUDE.md |
| **Lesson** | A mistake that should not repeat | Memory, phrased as a warning |

**The safeguard, before anything becomes a rule:** "Would they want this applied to every future job?" If no, it is an override. Promoting a one-time choice into a permanent rule is the most damaging mistake this skill can make. It stays invisible for weeks, then every output carries a preference they expressed once, about one thing.

## 1.6 The admission test: the default is REJECT

A candidate earns a place only if it passes all five:

1. **It would have CHANGED AN ACTION.** Name the moment. If you cannot, it is an observation. Cut it.
2. **It is NOT obvious** from reading the files, the output or the error.
3. **It RECURS.** It describes a kind of situation, not one artefact.
4. **It is TESTABLE.** You can say what would show it was broken.
5. **It has NO EXISTING HOME.** Search memory first. If a rule already covers the subject, update that one.

Then one more question: **could this be an automatic check instead of a rule?** A rule only works if a future session reads it and chooses to follow it. If a script, a checklist inside a skill, or a setting can enforce it, suggest that instead.

**Say in the report what you REJECTED and why.** A pass that admits everything has not run.

## 1.7 Write without wrecking what is there

1. **Read the target file first.** Always.
2. **Update in place.** If an entry on the same subject exists, add to it. Never create a second entry on the same subject.
3. **Never delete or weaken an existing rule on your own.** If a new lesson contradicts an old rule, quote the old rule back to the user and ask: keep it, replace it, or keep both with a condition that separates them. Rewording is yours. Dropping is theirs.
4. **Retire, do not stack.** When a new rule replaces an old one (with their yes), mark the old one retired in place, naming what replaced it.
5. **Keep it short.** One to three lines per rule. A long memory file is read less carefully, which is how rules stop working.
6. **Watch for parallel sessions.** If they run several sessions at once, list the most recently changed memory files and skim any that overlap before writing.

Done when: every candidate is banked or listed as REJECTED with the test it failed.

---

# PHASE 2: FIX. Close every loose end you can.

## 2.1 Find them. They hide in eight places.

1. **Promises you made.** Search your own replies for "I'll", "next step", "worth fixing", "separate job", "your call", "later", "still open".
2. **Blocked or failed steps.** A permission denial, a failed command, a timeout you moved past.
3. **Unsaved work.** Uncommitted changes in any git folder you touched.
4. **Temporary files that should be kept.** Anything in a temp folder that someone will need next week.
5. **Work that never reached them.** A report written but never opened, a file built but its path never printed.
6. **Checks marked NOT RUN, or claims nobody verified**, in anything you delivered.
7. **Old versions your work replaced**, still sitting next to the new ones. List them under YOURS with your recommendation. Never delete them yourself.
8. **Earlier notes this session made untrue.** A memory records what was true when it was written.

## 2.2 Sort by one test

**Is it reversible, and does it follow from what they already asked for?** Then it is yours. Do it now, without asking.

**It is theirs, and only theirs, when it:** spends money, sends something to another person, publishes anything, deletes something real, needs a login or password only they have, was blocked by a permission prompt (hand back the exact command), or is a matter of taste.

## 2.3 Do them, and fix the whole class

If you fix one broken link, one stray file or one stale note, **check whether the same fault exists elsewhere before calling it done.** Fixing one of five and reporting "fixed" is how the same problem comes back next week.

If a loose end turns out to be a real project, do not start it. Name it in the report.

Done when: every loose end from 2.1 is closed with evidence, or listed under YOURS or PARKED with the reason.

---

# PHASE 3: PROVE. Check the files before you write the report.

**A report of what you did is a claim. The files are the evidence.**

- For every file you say you changed, check it on disk: `ls -l <file>` shows a fresh modified time, and reading it back shows your change.
- In a git folder, `git status` and `git diff --stat` show what changed.
- A step counts as closed only when a result from THIS session shows it closed. "I ran it and it looked fine" is not evidence.
- If you cannot prove a change landed, it goes in the report as NOT VERIFIED, not as done.

## The second pass

Before the verdict, check your own close-out against this list. Every line is PASS or FAIL, with the evidence. A line you could not check is FAIL. Fix every FAIL, then check the whole list again.

1. Every request the user made this session is done, dropped by them, or listed for them.
2. Every promise you made is kept or listed.
3. Nothing they need is left only in a temp folder or only in the chat.
4. No background job is still running with its result uncollected.
5. Every change to something live (a document, a page, an upload) was read back after the write.
6. Every file you claim to have changed shows the change on disk.
7. Every new memory entry passed the admission test, and no existing rule was dropped without their yes.

Done when: every line of the second pass reads PASS, with its evidence from this session.

---

# PHASE 4: REPORT. One table, then the verdict.

```
CLOSE-OUT: <session topic>

WHERE THIS SESSION COST YOU (n)
  ✗ <what you had to do, your words>: <n> messages. Cause: <the step that missed it>. Fixed in: <file>

BANKED (n)
  ✓ <lesson>: <file it went into>, <what it replaced, or "new">
  ✗ REJECTED: <candidate>: <which test it failed>

CLOSED (n)
  ✓ <what>: <evidence: the file, the result, the read-back>

YOURS (n): nothing here could be done for you
  → <what>: <why it is yours: spends money / needs your login / your taste>
    <the exact command, or the one decision>

PARKED (n)
  · <what>: <why it can wait>

Nothing else is open.
```

The line "Nothing else is open." only goes in when it is true.

Rows under YOURS are handed back, not open. If only YOURS rows remain, the verdict is 'Good to close, ready to close.'

**Write every YOURS row for a person, not a machine.** Say what happens in their world, not the technical mechanism. Say what it costs them to say no. Give your recommendation. If they have to ask what a row means, the row failed, not them.

Then name **one** next action for them, the most important item from YOURS, as something they can do in about two minutes.

## The verdict line

The very last line is a bare verdict, alone, with nothing after it:

```
Good to close, ready to close.
```

It is only written when it is true. When something is genuinely open, same shape, same place:

```
Not ready to close: <the one thing>.
```

When they ask "can we close?" and the report is already printed, check again, then make the verdict line the WHOLE reply. A second report reads as not having listened.

Done when: the report is printed and its last line is the bare verdict, with nothing after it.

## What this does not do

- It does not hand work to another person or send anyone a message.
- It does not start new work. A loose end that turns out to be a project gets named, not begun.
- It does not ask permission for a reversible step. If you are asking, you already decided it was safe, so do it and report.
- It does not run by itself. You invoke it, so a quiet session writes nothing.
