# Working on this repo

Skills sit flat under `skills/<name>/`, one `SKILL.md` each. Extra files sit beside it only when the skill points at them: `references/` for material loaded on demand, `scripts/` for code the skill runs.

Every skill must have all four of these, kept in step:

1. A row in the top-level `README.md` reference table, linked to its `SKILL.md`, in the right group (you ask for it, or Claude reaches for it). The group must match `allow_implicit_invocation` in the skill's `agents/openai.yaml`.
2. An entry in `.claude-plugin/plugin.json` under `skills`.
3. A docs page at `docs/<name>.md` with these sections, in this order: What it does, When to reach for it, an optional What you need first, one or two free sections in the skill's own words, Common questions (only questions with evidence), It's working if, Where it fits. No install commands on a docs page.
4. `skills/<name>/agents/openai.yaml` with a display name, a short description and whether Claude may run it unprompted.

Frontmatter carries only `name`, `description` and `license`. The Claude app rejects other keys on upload. A description stays under 1,024 characters, says what the skill does and when to use it, and names the sibling skill for any job it could be confused with.

A skill opens on the failure it fixes, has numbered steps that each end on a "Done when" check, and ends with "What this does not do".

Writing rules: British English. Short sentences. No em dashes. No semicolons in prose. Plain words a non-developer would not need to look up. Never: leverage (as a verb), unlock, game-changer, deep dive, landscape, steal.

Nothing in a skill may depend on one person's setup: no personal paths, names, IDs or private tools. Run these before every commit and expect no hits:

```bash
grep -rn -i -E '/Use[r]s/|~/bi[n]|~/Deskto[p]|drive\.goog[l]e|notion\.s[o]' skills docs
grep -rn '—' skills docs README.md
python3 -c "import yaml,glob;[yaml.safe_load(open(f).read().split('---')[1]) for f in glob.glob('skills/*/SKILL.md')];print('frontmatter ok')"
claude plugin validate .
```

## The ship gate

A skill goes in the pack only when all three are true. Anything short of that waits in a held-back folder outside the repo.

1. It meets all 12 lines of QUALITY-BAR.md.
2. A stranger's cold run, on a fresh install with invented inputs, returns PASS with no open findings. "PASS WITH FIXES" means fix, then run it again.
3. It does a job no other skill in the pack already does.
