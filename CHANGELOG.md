# Changelog

## 1.0.0

The first public release: 7 skills in two groups.

- Work with Claude: `show-me`, `answer-first`, `close`, `improve-system`, `prompt-lab`, `workflow-maker`.
- Deals and clients: `machiavelli`.
- 16 more skills were built and tested, then cut to keep only the strongest.
- Every skill was run cold on a fresh install with invented data, fixed, and run again before it went in.
- Scripts find their own folder through `${CLAUDE_SKILL_DIR}`, so they work for a plugin install and a copied folder alike.
- A docs page for every skill under `docs/`, and Codex display metadata in `agents/openai.yaml`.

## 0.1.0

- First five skills: `show-me`, `answer-first`, `close`, `improve-system`, `setup-auditor`.
- Installs as a Claude Code plugin, by copying the files, or with `npx skills`.
