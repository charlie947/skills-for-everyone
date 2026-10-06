#!/usr/bin/env python3
"""Print every message the user typed in a Claude Code session.

    python3 session-turns.py [SESSION-ID | path/to/session.jsonl] [--craft] [--friction] [--full]

  --craft     show only messages that carry feedback on writing, tone, style or visuals
  --friction  show only messages where the session cost the user: they corrected, asked
              again, chased, were confused or were frustrated, each with its tags
  --full   print each message in full instead of the first 400 characters

With no argument it reads the current session (Claude Code sets CLAUDE_CODE_SESSION_ID).

Why this exists: the obvious way to read a transcript (records where type is "user")
misses two kinds of message, and both often carry the most important feedback.
  * Messages sent while Claude was still working. They are stored as
    "queue-operation" records, not "user" records.
  * Messages sent beside an image. Their text starts with "[Image #1]", and a naive
    reader skips the whole message.
A close-out that reads only some of the messages and reports a full sweep is the failure.
"""
import glob
import json
import os
import re
import sys

PROJECTS = os.path.expanduser("~/.claude/projects")

CRAFT = re.compile(
    r"too long|shorter|longer|repeat|bland|formulaic|generic|sounds? (so )?(ai|robotic)|"
    r"phrasing|wording|sentence|tone|style|voice|too much text|structure|"
    r"i don'?t (like|love)|doesn'?t feel|not what i (envisioned|had in mind)|prefer|"
    r"the way i had it|before was (better|perfect)|layout|font|spacing|colou?r|"
    r"bigger|smaller|too (big|small)|cluttered|messy|clarity|"
    r"never (use|say|call)|don'?t (call|say|use|write)|we never|\balways\b|"
    r"\b(green|blue|red|pink|grey)\b", re.I)

SYSTEM_PREFIXES = ("<system-reminder", "<command-", "<local-command", "<task-notification>",
                   "[SYSTEM NOTIFICATION", "<user-prompt", "Base directory for this skill:",
                   "This session is being continued from a previous conversation",  # auto-summary, not the user
                   "Stop hook feedback:", "<agent-message", "<cross-session-message",
                   "Another Claude session sent a message", "[Subagent hand-back]")  # other agents, not the user

# Messages where the session cost the user a turn. The tags are a guess from wording only.
FRICTION = {
    "CORRECTED": re.compile(
        r"^\s*(?:no|nope)\b|\bwait,? no\b|that'?s (?:not|wrong)|not what i|\bwrong\b|"
        r"i (?:said|told you|asked)|you (?:missed|forgot|ignored|didn'?t)|\bstill (?:not|wrong|broken|there)|"
        r"\bagain\b|\binstead\b|why (?:are|did|have|is|would) (?:you|it|this)|\bstop\b|"
        r"\bundo\b|\brevert\b|go back to", re.I),
    "FRUSTRATED": re.compile(
        r"annoy|frustrat|come on|\bugh\b|seriously|how many times|\bwtf\b|rubbish|useless|"
        r"waste of|!!|falling down|not good enough", re.I),
    "CONFUSED": re.compile(
        r"what do you mean|i don'?t (?:understand|get it|follow)|confus|what does (?:this|that) mean|"
        r"lost me|explain (?:that|this) again", re.I),
    "CHASED": re.compile(
        r"have you (?:done|added|fixed|sent|finished|checked)|did you (?:do|add|fix|check|run)|"
        r"is (?:it|this|that) (?:done|live|finished|fixed)|any update|are you sure|"
        r"you said you would|still waiting|waiting for you|don'?t (?:just )?give up", re.I),
}


def friction_tags(t, earlier):
    """Tag one message. RE-ASKED: half or more of its longer words were already in one earlier message."""
    tags = [k for k, rx in FRICTION.items() if rx.search(t)]
    words = set(re.findall(r"[a-z]{4,}", t.lower()))
    if len(words) >= 6 and any(len(words & e) / len(words) >= 0.5 for e in earlier):
        tags.append("RE-ASKED")
    earlier.append(words)
    return tags


def text_of(content):
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    return "".join(p.get("text", "") for p in content
                   if isinstance(p, dict) and p.get("type") == "text")


def turns(path):
    # A mid-turn message is logged as an "enqueue" record, again as a "remove" record, and
    # may come back as a "user" record when it is delivered. Count it once. Match on the
    # text, one user record per enqueue, so a "yes" the user really typed twice still shows twice.
    queued = {}
    with open(path, encoding="utf-8", errors="ignore") as source:
        for line in source:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            kind = d.get("type")
            if kind == "queue-operation":                   # sent while Claude was working
                if d.get("operation", "enqueue") != "enqueue":
                    continue
                c = d.get("content")
                t = c if isinstance(c, str) else text_of(c)
            elif kind == "user":
                m = d.get("message") or {}
                if m.get("role") != "user":
                    continue
                t = text_of(m.get("content"))
            else:
                continue
            t = re.sub(r"\[Image[^\]]*\]", "", t).strip()   # keep the words beside an image
            if not t or t.lstrip().startswith(SYSTEM_PREFIXES):
                continue
            if kind == "user":
                if queued.get(t):                         # already shown as a mid-turn message
                    queued[t] -= 1
                    continue
                queued.clear()  # a new typed message closes the delivery window, so a later "yes" still counts
            if kind == "queue-operation":
                queued[t] = queued.get(t, 0) + 1
            yield kind, t


def find_transcript(ref):
    if ref and os.path.isfile(ref):
        return ref, "the path you passed"
    sid = ref or os.environ.get("CLAUDE_CODE_SESSION_ID", "").strip()
    if sid:
        name = sid if sid.endswith(".jsonl") else sid + ".jsonl"
        hits = glob.glob(os.path.join(PROJECTS, "*", name))
        if hits:
            return max(hits, key=os.path.getmtime), "session id " + sid
        if ref:
            sys.exit(f"No transcript named {name} under {PROJECTS}. Nothing was read. Do not report a sweep.")
    files = glob.glob(os.path.join(PROJECTS, "*", "*.jsonl"))
    if not files:
        sys.exit(f"No Claude Code transcripts found under {PROJECTS}. Nothing was read.")
    path = max(files, key=os.path.getmtime)
    why = (f"Session id {sid} has no transcript here" if sid else "No session id was set")
    print(f"!! {why}, so this read the most recently changed transcript.\n"
          "   If you run several sessions at once, it may not be yours. Check the path below.\n",
          file=sys.stderr)
    return path, "newest transcript on disk (a guess)"


def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        print(__doc__.split("Why this exists")[0].strip())
        return
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    path, how = find_transcript(args[0] if args else None)
    craft_only, full = "--craft" in sys.argv, "--full" in sys.argv
    friction_only = "--friction" in sys.argv
    n = mid = craft = 0
    earlier, pain, total = [], {}, 0
    for kind, t in turns(path):
        total += 1
        is_craft = bool(CRAFT.search(t))
        hits = friction_tags(t, earlier)
        for k in hits:
            pain[k] = pain.get(k, 0) + 1
        if craft_only and not is_craft:
            continue
        if friction_only and not hits:
            continue
        n += 1
        mid += kind == "queue-operation"
        craft += is_craft
        tags = ("CRAFT " if is_craft else "") + ("(sent mid-turn) " if kind == "queue-operation" else "")
        if friction_only:
            tags = "+".join(hits) + " " + ("(sent mid-turn) " if kind == "queue-operation" else "")
        print(f"[{n}] {tags}{t if full else t[:400]}")
    sys.stdout.flush()
    if total == 0:
        print("!! 0 messages found. That is almost never true. Check the path below before reporting a sweep.",
              file=sys.stderr)
    if friction_only:
        print("\nFRICTION: " + (", ".join(f"{k} {v}" for k, v in sorted(pain.items(), key=lambda x: -x[1]))
                                or "none found")
              + "\nEach tag is a guess from wording. Read the message and the reply before it.", file=sys.stderr)
    print(f"\n{n} messages, {mid} sent mid-turn, {craft} carry craft feedback\n{path}\nfound via: {how}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
