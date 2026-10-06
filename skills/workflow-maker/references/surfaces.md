# Surfaces: where the reader runs the workflow

The surface changes the prompts a lot. Read the section for the named surface before writing any step.

**This file is a briefing, not proof.** These products change every month. A confident note here can be months out of date. Re-check every fact a step depends on against the vendor's live docs before it goes in a pack.

The thing to resist: one pack called "works anywhere". A prompt that asks Claude to save a file breaks in a chat window. A prompt that says "now copy the output" wastes Claude Code. Pick one surface and write for it.

## Consumer tools: ChatGPT, Gemini and others

The usual choice for a pack aimed at an audience, because most people already have one of these. Use whichever tool the idea is actually about.

Check before writing a single step:

- **The feature exists on the plan the reader probably has.** A workflow that quietly needs the top paid plan is not a free resource. Name the plan in "Before you start".
- **The exact menu path, from the current docs.** These products move their menus often. A stale click path is the most common way a pack dies at step 1.
- **The model or mode name as it appears on screen today.**

## The Claude app (web, desktop, mobile)

Widest Claude audience, no setup, works on any device.

Can do:

- Long conversations with uploaded files (PDF, Word, images, CSV).
- **Projects**: standing instructions and files that carry across chats. The best tool in a chat-only workflow. Put the reusable context in a Project once, and each step becomes a short prompt.
- **Artifacts**: documents and simple apps shown beside the chat.
- **Connectors** such as Gmail, Google Drive or Notion, if the reader has set them up. Treat these as optional. A required connector breaks the pack for most readers.

Cannot do:

- Touch files on the reader's computer.
- Run commands or scripts on their machine.
- Work unattended. Every step needs the reader to paste and read.

How the prompts change:

- Each step ends with the reader carrying the output to the next step, so say that plainly.
- Keep outputs small enough to copy comfortably. If a step produces 3,000 words the reader must paste back in, restructure it.
- Use the carry-forward slot for every step that depends on an earlier one: `[PASTE THE ACTION LIST FROM STEP 2, or if you are in the same chat, write: the actions above]`. It works whether or not the reader opened a fresh chat.
- If three or more steps need the same background (writing samples, brand rules, examples), make a Project the first setup step and keep each prompt short.

## Cowork (Claude desktop app)

Anthropic's agent for people who do not use a terminal. It works on files in folders the reader gives it.

Can do:

- Read, edit and create files in a folder the reader chooses.
- Run a multi-step task from start to finish.
- Produce real documents, spreadsheets and PDFs.

Check at build time, and put the answers in "Before you start":

- Which plans include it. If it needs a paid plan, say so before step 1.
- Which operating systems it runs on today.
- How quickly it uses up plan limits compared with chat.

**Safety line, always:** Cowork can edit and permanently delete files in a folder it has been given. Every Cowork pack tells the reader to work on a copy, before step 1.

How the prompts change: stop telling the reader to copy anything. Steps become instructions about files and folders: "Point Cowork at the folder with your meeting notes and paste this." One Cowork step can replace three chat steps. Say up front which folder to set up.

## Claude Code (terminal, desktop app or IDE)

Full power, smallest audience. Most non-developers have never opened a terminal.

Can do: read and write files, run commands, and use skills and connectors.

How the prompts change:

- Steps can name real file paths and commands. Check every command against `code.claude.com/docs` before it goes in.
- Include the install and first-run steps. A reader new to the terminal needs the way in, not only the clever part.
- **Safety line, always**, as for Cowork.

Consider two tiers: the Claude app version as the main path, and the Claude Code version as a clearly marked upgrade at the end. The basics then stay open to everyone.

## Choosing when nobody has said

Ask. It is one question, and the answer changes every step.

If the user wants a recommendation:

| Situation | Surface |
| --- | --- |
| A free resource for a broad audience | The consumer tool that audience already uses, or the Claude app |
| The job needs the reader's own files, or would be heavy copy and paste in chat | Cowork |
| The point of the pack is to show what Claude Code can do | Claude Code |
