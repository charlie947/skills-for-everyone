## What it does

Ends a good session properly, in four phases: LEARN, FIX, PROVE, REPORT. It saves the lessons worth keeping into Claude's memory, finds every point where you had to correct, repeat or chase Claude and fixes the cause, finishes the loose ends it can, checks the files to prove each change landed, and hands back only what needs you.

Its default is to reject. Most things that happen in a session are one-offs. A lesson only gets saved if it would have changed an action, is not obvious, will come up again, can be tested, and has no existing home. The report lists what it rejected and why.

## When to reach for it

You type `/close`, or say "wrap this up", "are we good to close?" or "save progress". Claude will not run it on its own.

Do not run it on a session that went badly. It would save the wrong habits as rules.

## What you need first

Claude Code. The skill ships a small script that reads every message you sent in the session, including ones sent while Claude was busy and ones sent beside an image. A hand-made reader misses both.

## The verdict line

Every close ends on one bare line: `Good to close, ready to close.` or `Not ready to close: <the one thing>.` The first only appears when it is true. Items handed back to you under "yours" do not count as open.

## Common questions

**Why did it reject most of my corrections?**
Because most corrections are about one piece of work. Saving "make this paragraph shorter" as a permanent rule would shorten every future paragraph. Only notes you would give on a different piece become rules.

**Will it delete my old rules?**
No. It can reword a rule. Dropping one is always your call.

## It's working if

- Next week's session does not repeat this week's corrections.
- The report's "yours" section is short and every row says why it needs you.
- The memory file gets sharper rather than longer.

## Where it fits

The last step of any session worth keeping. For mistakes that repeat across many sessions, run [improve-system](./improve-system.md) once or twice a week.
