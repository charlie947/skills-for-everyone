## What it does

Push-check runs before anything you built goes to GitHub. It says in plain English what is about to leave, runs the repo's own checks, then sweeps for the faults a passing check cannot see: leaked API keys, a tracked `.env` file, your own home folder written into a file, files too big for GitHub, and links to files that are not there. A second Claude reads the changes cold, with no memory of the session, and then the skill rehearses on a fresh copy exactly what a new user would do first.

It pushes only after two full passes in a row come back clean with nothing changed between them. One pass is not enough, because every fix changes the repo and the next pass sees what the fix exposed.

## When to reach for it

Type `/push-check`, or say "push this", "ship it" or "put it on GitHub".

| Situation | Use |
| --- | --- |
| You are about to put a project on GitHub for the first time | `push-check` |
| You changed something other people already download | `push-check` |
| You just want to save your work privately and nobody else uses it | Plain `git push` is fine |

## What it never does

It never makes a repo public without your yes, never force-pushes or rewrites history, never prints a secret it finds, and never sends the announcement. If there is something for people to do, it drafts a three-line note and you send it.

## Try it

Make a test repo with a fake key in it, then ask Claude to push it:

```
mkdir push-test && cd push-test && git init
echo "key=sk-ant-api03-$(printf 'x%.0s' {1..30})" > config.txt   # a fake key, built when you run it
git add -A && git commit -m test
```

Push-check stops before the push, names `config.txt` line 1, and does not print the key.
