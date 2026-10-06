---
name: push-check
description: >-
  Check everything before work goes to GitHub, then push it. Runs the repo's own checks, a sweep
  for leaked keys, personal paths, oversized files and dead links, a second Claude reading the
  changes cold, and a fresh-copy rehearsal of what a new user does first. Pushes only after two
  clean passes in a row, then drafts the short note to send people, if there is anything for them
  to do. Use when the user says "push", "push this", "ship it", "put it on GitHub", "release",
  "send it to them", "is it ready to push", or is about to share a repo other people will download.
license: MIT
---

# push-check

A push feels finished before it is. The checks pass, the files look fine, and the faults turn up
when someone else downloads the work: a leaked key, a link to a file that is not there, a setup
step that only works on your machine. None of it is hard to find. Nothing looked for it.

**A push is a sequence, not a command.** Every step below runs, in order, before `git push`.
The step that "obviously will pass" is the one that catches something.

Talk to the user in plain English the whole way through. They may not know git. Say what you
found and what you did about it, never which command printed it.

---

## Step 1. Say what is about to leave

```bash
git status --short
git log --oneline @{u}..HEAD 2>/dev/null || git log --oneline -10
git diff --stat @{u}..HEAD 2>/dev/null
```

Tell the user in one or two lines what this push contains: which files, and what changed for
someone who downloads it. If there is no remote yet, say so and ask where it should go before
going further. Never create a public repo without a yes. Public is the default risk.

## Step 2. Run the repo's own checks

```bash
ls tools/ scripts/ 2>/dev/null | grep -iE 'check|test|verify|validate|lint'
cat package.json 2>/dev/null | grep -A5 '"scripts"'
```

Run whatever the repo already has and **read the last line of the output**, not the first few.
A summary at the bottom that says FAIL is easy to miss when you skim from the top. If the repo
has no checks of its own, say so. That is a finding, not a pass.

## Step 3. Sweep for what a passing check cannot see

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/push-sweep.sh" .
```

`${CLAUDE_SKILL_DIR}` is the folder this skill is installed in. If it comes up empty, use the
folder this SKILL.md sits in. Exit 0 is clean, 1 means problems, 3 means it could not scan
anything, which is never a pass.

| Check | Why it matters |
|---|---|
| **Secrets** | An API key in a public repo is found by bots within minutes. The script prints the file and line, never the key itself |
| **A tracked `.env`** | The usual home of every password in the project |
| **Your home folder** | A path like `/Users/yourname/...` works for you and for nobody else |
| **Files over 50MB** | GitHub warns at 50MB and refuses anything over 100MB |
| **Dead links** | A README pointing at a file that is not in the repo is the first thing a new user hits |

If `gitleaks` is installed, run it on the commits about to leave as a second net:
`gitleaks git . --redact --no-banner --log-opts="@{u}..HEAD"`. If it is not, say NOT RUN. Never
skip it silently.

**A key that has already been pushed is leaked, even after you delete it.** Tell the user to
rotate it at the provider first. Cleaning the history comes second.

## Step 4. A second reader, cold

The person who wrote the change is the worst person to review it. Start a fresh subagent with
no memory of this session and give it only the diff and one line on what the change is meant to
do:

> Read this diff as someone about to download the repo. List anything that is broken, untrue,
> confusing or missing for a new user. Quote the file and line for each one. Do not fix anything.

Then **check each finding against the file before acting on it.** Reviewers are sometimes wrong.
Report the count both ways: found, fixed, and rejected with the reason. If nothing is ever
rejected, you are copying the review, not checking it.

## Step 5. Rehearse on a fresh copy

This is the step that catches what every other step misses, because it runs somewhere your
setup is not.

```bash
rm -rf "${TMPDIR:-/tmp}/push-rehearsal"
git clone -q . "${TMPDIR:-/tmp}/push-rehearsal" && cd "${TMPDIR:-/tmp}/push-rehearsal"
```

Then follow the README exactly as a stranger would: the install step, then the first thing it
tells a new user to run. It has to work. Then run the thing this change was about and check the
output is what you meant. Say plainly what this cannot prove: other computers, other operating
systems, other versions.

## Step 6. Loop until two passes in a row come back clean

Every fix changes the repo, and the next pass sees what the fix exposed. So the exit condition
is not "the checks passed once". It is:

> **Two full passes of steps 2 to 5 with nothing found, and nothing changed between them.**

If you fixed anything, the pass that found it does not count. Stop after five loops. If it is
still finding things, the repo has a problem you have not understood yet. Say so instead of
pushing.

## Step 7. Push

```bash
git push
```

Then confirm it arrived: `git status` should say the branch is up to date with the remote. For a
public repo, open the repo page and check the README renders.

## Step 8. Tell people only if they have something to do

Draft a message only when someone needs to download the update, something they use now behaves
differently, or something they reported is fixed. A note with nothing to do in it teaches people
to stop reading your notes.

Three lines at most: the instruction, what it fixes in their words, and the one thing that now
behaves differently, if there is one.

```
Quick one when you get a sec: download the latest version.
It fixes the broken setup link Sam spotted.
Nothing else changes for you.
```

**Show the user the draft. Never send it.** They send it.

## What this skill does not do

- Push to a public repo, or make a private one public, without the user saying yes.
- Force-push, rewrite history or delete a branch.
- Print a secret it found.
- Send the announcement.
