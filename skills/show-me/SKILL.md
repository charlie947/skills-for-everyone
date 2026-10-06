---
name: show-me
description: >-
  Put the finished thing in front of the user instead of describing it. Renders plans,
  comparisons, options, layouts, reports and drafts as a self-contained HTML page and opens it in
  their browser before saying a word about it. Use when the user says "show me", "let me see it",
  "can I see it", "what does it look like", "give me options", "which one", "I don't see
  anything", or any moment you are about to describe a layout, a plan, a comparison or a design in
  prose. Always use it before asking the user to pick, approve or judge anything visual.
license: MIT
---

# Show me

**A render they have not seen does not exist.**

This skill closes the gap between finishing something and actually handing it over. Describing a picture in prose is not showing it. Printing a file path is not showing it. Both feel like delivery and neither one is.

There is nothing to install. You write the HTML, you open it, they look at it.

## When this fires

Any time the answer is visual and you are about to type it out instead:

- a plan, a structure, a roadmap, a set of steps
- a comparison between two or more things
- a layout, a page, a design, a wireframe, a chart
- a report, a review, a dashboard, a summary of where you got to
- **any moment the user has to choose between options**

If they would have to read it twice, draw it once.

## Mode 1: SHOW

One thing, or a stack of versions of one thing.

1. Write a **complete, self-contained HTML file** into the current project folder (or ~/Documents if there is none). Inline CSS, no external requests, no CDN links, no web fonts. It has to render with the network off.
2. Include `<meta charset="utf-8">`. Without it every apostrophe becomes three characters of gibberish.
3. For a stack of versions, put the newest at the top, full size, with a one-line label on each saying what changed.
4. Open it (see "Opening it properly").
5. Only then say anything about it.

Done when: the active tab's URL is your file, read back with the check command.

## Mode 2: PICK

Two or more directions the user has to choose between.

**Three minimum.** Two options is a yes-or-no in disguise. Three is where someone starts seeing what they actually want, and the answer is often a piece of the first inside the shape of the third.

Lay them side by side on one page, each with a short label and a one-line description of the argument it makes. Not the decoration, the argument. Then ask.

**Never ask someone to choose between visual options described in words.** A text description of a layout is your picture of it, not the thing itself. You get a ruling on the wrong object, or no ruling at all. Render first, ask second.

### Before you render: the one-sentence test

Describe each direction in one sentence. **If the same sentence fits two of them, you restyled one idea instead of designing two.** Go back. A board of three variations on one idea wastes the choice, because whatever they pick, you have learned nothing.

### The board

Build this. It is deliberately plain so the options are the only thing with any visual weight. Every card carries a button that copies the pick, so they answer by clicking rather than by typing out which one they meant.

```html
<!doctype html><meta charset="utf-8"><title>Pick a direction</title>
<style>
 :root{--bg:#fff;--fg:#14171a;--mut:#5d6b7a;--line:#e3e8ef;--card:#f7f9fb;--accent:#c2410c}
 @media (prefers-color-scheme:dark){
   :root{--bg:#0f1418;--fg:#eef2f6;--mut:#9aa8b6;--line:#243039;--card:#161d23;--accent:#fb923c}}
 *{box-sizing:border-box}
 body{margin:0;background:var(--bg);color:var(--fg);padding:40px 32px 80px;
      font:16px/1.55 ui-sans-serif,-apple-system,"Segoe UI",Roboto,sans-serif}
 h1{font-size:26px;margin:0 0 6px}
 p.lede{margin:0 0 30px;color:var(--mut);max-width:70ch}
 .grid{display:grid;gap:22px;grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}
 .card{border:1px solid var(--line);border-radius:12px;background:var(--card);
       padding:18px;display:flex;flex-direction:column;gap:10px}
 .card img,.card svg{width:100%;display:block;border-radius:7px;border:1px solid var(--line)}
 h2{font-size:17px;margin:0}
 .angle{color:var(--mut);font-size:14px;margin:0;flex:1}
 button{font:inherit;font-size:14px;padding:9px 14px;border-radius:7px;cursor:pointer;
        border:1px solid var(--accent);background:transparent;color:var(--accent)}
 button:hover{background:var(--accent);color:var(--bg)}
</style>
<h1>Pick a direction</h1>
<p class="lede">One line on what to judge, and what to ignore.</p>
<div class="grid">
  <div class="card">
    <!-- the render: <img src="data:image/png;base64,...">, an <svg>, or live HTML -->
    <h2>A: name of the idea</h2>
    <p class="angle">The argument this one makes, in one line.</p>
    <button onclick="navigator.clipboard.writeText('A').then(()=>this.textContent='Copied. Paste it back',()=>this.textContent='Type A back to me')">Pick A</button>
  </div>
  <div class="card">
    <h2>B: name of the idea</h2>
    <p class="angle">The argument this one makes, in one line.</p>
    <button onclick="navigator.clipboard.writeText('B').then(()=>this.textContent='Copied. Paste it back',()=>this.textContent='Type B back to me')">Pick B</button>
  </div>
  <div class="card">
    <h2>C: name of the idea</h2>
    <p class="angle">The argument this one makes, in one line.</p>
    <button onclick="navigator.clipboard.writeText('C').then(()=>this.textContent='Copied. Paste it back',()=>this.textContent='Type C back to me')">Pick C</button>
  </div>
</div>
```

Three rules that keep a board honest:

- **Name the idea, not the decoration.** "Timeline down the left" is an idea. "Blue version" is decoration, and it means you built the same thing twice.
- **Embed every image.** An `<img src="/some/local/path.png">` shows as a broken icon the moment the file moves. Turn it into base64 inside the page, or draw it in inline SVG or HTML.
- **Judging shape? Render it in greyscale and say so in the lede.** Colour decides the argument before they have looked at the structure.

Done when: the active tab's URL is your file, read back with the check command.

## Mode 3: HISTORY

Use this when the user has turned down two or more directions in a row and your next attempt would be a guess.

**Do not draw three new options.** Build one page with every direction tried so far, one example of each, in the order you made them, each labelled with what the user said about it. Apply any fix you made after a rejection, so they see the fixed version.

Why it beats a fresh set: a rejected direction often carries the one thing they did like, and a direction fixed after it was turned down has usually never been shown again. A new set throws both away.

**The test before you draw anything after a rejection:** have they seen every direction tried so far, side by side, with the fixes applied? If not, that page is the next thing you show.

## Mode 4: COPY

When the thing under discussion is words, show the words, not a picture.

If the last thing talked about was phrasing, a headline, a caption or a line length, "show me" means the text. Render it as a clean page that looks like where it will be read, with the character count beside each line and the total at the top. Do not show them the graphic again when they asked about the caption.

## Opening it properly

**`open -a "Google Chrome" file.html` does not reliably show them anything.** It creates the tab but may not bring the browser forward, so the page stacks up behind whatever they are looking at. On macOS use this instead:

```bash
osascript <<'EOF'
tell application "Google Chrome"
  activate
  set w to front window
  make new tab at end of tabs of w with properties {URL:"file:///ABSOLUTE/PATH"}
  set active tab index of w to (count of tabs of w)
end tell
EOF
```

`activate` brings the window forward and setting `active tab index` selects the new tab. You need both. If they use Safari or another browser, `open /ABSOLUTE/PATH.html` opens it in their default browser. On Windows, `start C:\PATH\TO\FILE.html` does the same, and on Linux `xdg-open /ABSOLUTE/PATH.html`.

If Chrome has no open window, add `if (count of windows) = 0 then make new window` before `set w`. The first run triggers a macOS permission prompt: tell them to click OK.

**Then check it worked.** Read the active tab's address back and confirm it is yours:

```bash
osascript -e 'tell application "Google Chrome" to return URL of active tab of front window'
```

A command that finishes without an error proves it ran. It never proves they saw it.

**Bring the browser forward once per page, never again.** The first time you show a page, bring it to the front. When you update the same page, reload it quietly and tell them it changed. Grabbing their screen on every small edit pulls them out of whatever they were typing. To reload without bringing Chrome forward:

```bash
osascript -e 'tell application "Google Chrome"' -e 'repeat with t in tabs of front window' -e 'if URL of t is "file:///ABSOLUTE/PATH" then reload t' -e 'end repeat' -e 'end tell'
```

## What renders as HTML, and what must not

**HTML** for anything they will look at or share: plans, reviews, comparisons, reports, dashboards, option grids, session summaries.

**Plain text** for anything they will paste into another tool: social posts, newsletter bodies, emails, docs, settings files, instruction files. HTML there breaks the paste. In an instruction file it costs tokens in every future session and buys nothing.

Decide which one you are producing before you build it.

## Two things that ruin it

**No background grid or texture on anything text-heavy.** It looks good on a dashboard and makes a dense document hard to read.

**Look at it yourself first.** Take a screenshot with headless Chrome and open the image. If that fails or hangs, say 'not verified: I have not seen the render' before showing it. A render you have not opened is a render you cannot describe honestly, and it is how a broken page gets presented as a candidate.

## What you say around it

The render does the explaining. Your words around it should be almost nothing.

**Lead with the verdict, not the process.** First line: what they are looking at and what you think of it. Never open with what you are about to do or how you got there.

**Print the full path of the file on its own line**, so they can find it again later.

**End with one next thing**, on its own line, doable now:

```
Next: pick a direction and I will build it out.
```

One next step, not a menu. Not "let me know if you want changes". If there is nothing next, say the work is done and stop.

**Say the verdict out loud, including the failures.** "This one is broken, the other two are worth looking at" beats silence, and it beats presenting a broken page as a candidate.

## Do not guess

The failure that wastes the most time is not a bad render. It is a confident one built on something nobody checked.

If you do not know a filename, a number, a status, a path or what a link points to, **go and check it**. Read the file, run the query, open the page.

If you cannot check, say **"not verified"** in those words and name what is missing. Never fill a gap with something that merely sounds right, and never report the result of a check you did not run.

Placeholder text in a mock-up is labelled as placeholder, never a figure that reads as real.

## What this does not do

- It does not decide for them. It puts the options in front of them and asks.
- It does not publish anything. The page lives on their computer.
- It does not turn paste-out copy into HTML. Text that goes into another tool stays as text.

## The check before you speak

One question: **have they seen this, with their own eyes, in this session?**

If no, you are not finished, however done the work is.
