# {{WORKFLOW_TITLE}}

**Makes:** {{END_OUTPUT}}
**Runs in:** {{SURFACE}}, {{PLAN}}
**Run time:** {{RUN_TIME}}

<!-- SURFACE: the app only, for example Claude app or Claude Code, because the step blocks paste into it.
PLAN: the plan it needs, for example free plan or Pro plan. -->

## What you start with
{{START_STATE}}

## What you end with
{{END_STATE}}

---

## Before you start

- {{WHAT_THEY_NEED}}
- {{WHAT_TO_HAVE_TO_HAND}}

{{SAFETY_LINE}}

<!-- WHAT_THEY_NEED: the account, app or plan. Say plainly what is free and what is paid. A reader
who finds out at step 4 that they need a subscription feels tricked.
SAFETY_LINE: required whenever a step points a tool at the reader's own files. Cowork and Claude
Code can edit and permanently delete inside a folder they have been given. Tell them to work on a
copy. Delete this line only when the workflow never touches the reader's files. -->

---

## The workflow

### Step 1: {{STEP_1_TITLE}}

Paste this into {{SURFACE}}:

```
{{STEP_1_PROMPT}}
```

What good looks like: {{STEP_1_CHECK}}

### Step 2: {{STEP_2_TITLE}}

Paste this into {{SURFACE}}:

```
{{STEP_2_PROMPT}}
```

What good looks like: {{STEP_2_CHECK}}

### Step 3: {{STEP_3_TITLE}}

Paste this into {{SURFACE}}:

```
{{STEP_3_PROMPT}}
```

What good looks like: {{STEP_3_CHECK}}

<!-- Add or remove step blocks to fit the workflow. Keep the same shape: a title, one paste-able
prompt in a code block, one "what good looks like" line. Every check must be one the reader could
fail: "every action has one owner and a date" works, "a good result" does not. -->

<!-- A setup step, for when the reader has to click something in the app before or after the
paste. Copy it out of this comment, fill it in, and number it with the other steps.

### Step 1: {{SETUP_TITLE}}

1. {{CLICK}}
2. Paste the prompt below.

```
{{SETUP_PROMPT}}
```

3. {{CLICK}}

What good looks like: {{SETUP_CHECK}}
-->

---

## Going further (optional)

{{GOING_FURTHER}}

<!-- Optional. A short note on a faster or deeper version, for example the same job in Claude Code.
Never required to run the pack. Delete this block if it adds nothing. -->

---

{{SIGN_OFF}}

<!-- Optional. The author's name and one link, if the pack is shared publicly. Delete if not needed. -->
