#!/usr/bin/env python3
"""improve-system: mine your own Claude Code prompt history for what keeps going wrong.

The history on disk is evidence. Once or twice a week, read it for
  1. CORRECTIONS that recur (Claude got the same thing wrong more than once)
  2. REPEATED ASKS (a job typed again and again = a skill that should exist), with the nearest skill
  3. RE-PASTED CONTEXT (the same paste in several sessions = a fact your setup should already hold)
  4. TIME SINKS (hours of active prompting on one kind of job = a candidate to automate)

Reads ~/.claude/history.jsonl (every prompt you typed into Claude Code, with session and folder) and
~/.claude/paste-cache/. Read-only on both. Writes a dated report to ~/.claude/logs/improve-system/
(override with IMPROVE_SYSTEM_DIR). Needs only Python 3, no extra packages.

Usage:
  python3 improve-system.py [--days 7] [--topic REGEX] [--min-sessions 2] [--json]
  --topic narrows to sessions whose folder or any prompt matches REGEX (e.g. 'newsletter|email').
"""
import argparse, collections, datetime, glob, json, os, re, sys, time

HOME = os.path.expanduser("~")
HIST = f"{HOME}/.claude/history.jsonl"
PASTE = f"{HOME}/.claude/paste-cache"
SKILLS = f"{HOME}/.claude/skills"
OUTDIR = os.environ.get("IMPROVE_SYSTEM_DIR") or f"{HOME}/.claude/logs/improve-system"

# A correction is you telling Claude it got something wrong. Each pattern is a phrase people use
# when pushing back, not a generic negative word.
CORRECTION = re.compile(
    r"\b(that'?s (wrong|not (right|what i))|not what i (asked|said|meant|wanted)|i (already |just )?(said|told you|asked)"
    r"|i'?ve (said|told you)|why (did|are|is|have) you|you (didn'?t|did not|haven'?t|forgot|missed|keep|still)"
    r"|(still|again) (wrong|broken|not|the same)|stop (doing|using|adding)|how many times|no,? (that|it|this|you)"
    r"|this is (wrong|not right|broken)|it'?s (wrong|broken|not working)|doesn'?t (work|look right)|i don'?t (want|like)"
    r"|never (do|use|again)|we('ve| have) (been through|talked about)|you were supposed)\b", re.I)

# Prompts that are plumbing, not asks: delegation boilerplate, hook echoes, empty acks.
NOISE = re.compile(r"^(do the job in |\[pasted text|<|y$|yes$|ok$|okay$|go$|continue$|thanks?)", re.I)
STOP = set("""a an the and or but so to of in on for with at by from is are was were be been it this that these those
i you we he she they me my your our his her their its im ive id dont didnt cant can could would should will just
do does did done have has had not no yes ok okay please now then there here what which who how why when where all
any some more most very really also get got make made let lets can like want need one two see look into about
up out over again still if as than them us claude yeah yes sure think thing things know maybe going good great bit
because actually really something kind sort probably fine looks look looking feel feels gonna wanna lot little much
right well way time today tomorrow back try trying said say saying tell told think thought mean means use using
honestly guess even though only every each other another same new old first last next better best idea image""".split())

DOMAINS = [("writing / content", r"\bpost\b|caption|linkedin|newsletter|blog|article|copy\b|headline|script|tweet|instagram|tiktok|youtube"),
           ("email / messages", r"email|gmail|inbox|reply|outlook|\bdm\b|message"),
           ("visuals / design", r"design|graphic|image|slide|deck|carousel|thumbnail|canva|figma|logo|layout"),
           ("data / reports", r"spreadsheet|excel|sheet|csv|report|dashboard|analytics|numbers|chart"),
           ("research", r"research|competitor|summari[sz]e|find out|look up|sources?"),
           ("website / code", r"website|landing page|html|css|deploy|bug|code|app\b"),
           ("docs / admin", r"notion|doc\b|docs|meeting|calendar|invoice|proposal|contract|client"),
           ("claude setup", r"hook|skill|claude\.md|memory|plugin|mcp|settings|agent")]


def load(days, topic):
    if not os.path.exists(HIST):
        sys.exit(f"improve-system: no history found at {HIST}. Use Claude Code for a few days, then run this again.")
    cut = (time.time() - days * 86400) * 1000
    rows = []
    for line in open(HIST, encoding="utf-8", errors="replace"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("timestamp", 0) < cut:
            continue
        rows.append(d)
    if rows and sum(1 for r in rows if not r.get("sessionId")) > len(rows) / 2:
        print("!! Your history has no session ids. Session counts, repeated asks and re-pasted context cannot be measured.",
              file=sys.stderr)
    if topic:
        # Pasted text counts for TOPIC membership only. Corrections read your own words, never a
        # pasted brief or transcript (someone else's text would flood the detector with false hits).
        rx = re.compile(topic, re.I)
        hit = lambda r: rx.search(r.get("project") or "") or rx.search(r.get("display") or "") or rx.search(pasted_text(r))
        keep = {r["sessionId"] for r in rows if r.get("sessionId") and hit(r)}
        # A row with no session id joins only on its own match, never through a shared empty id.
        rows = [r for r in rows if (r["sessionId"] in keep if r.get("sessionId") else hit(r))]
    return rows


def pasted_text(r):
    out = []
    for p in (r.get("pastedContents") or {}).values():
        if p.get("content"):
            out.append(p["content"])
        elif p.get("contentHash") and os.path.exists(f"{PASTE}/{p['contentHash']}.txt"):
            out.append(open(f"{PASTE}/{p['contentHash']}.txt", encoding="utf-8", errors="replace").read(20000))
    return " ".join(out)


def words(text):
    text = re.sub(r"(https?://|/Users/|/home/|~/)\S+", " ", text)
    return [w for w in re.findall(r"[a-z][a-z'-]+", text.lower()) if w.replace("'", "") not in STOP and len(w) > 2]


def day(ts):
    return datetime.datetime.fromtimestamp(ts / 1000).strftime("%d/%m")


# A REPEAT is a correction that says the mistake came back. These are the ones a rule or hook should already stop.
REPEAT = re.compile(r"\b(again|still|haven'?t|keep|how many times|i (already|just) (said|told)|i'?ve (said|told)|"
                    r"we('ve| have) (been through|talked about)|every time|once more|same (thing|mistake))\b", re.I)


def session_domains(rows):
    text = collections.defaultdict(list)
    for r in rows:
        if r.get("sessionId"):  # rows with no id cannot be grouped into a session
            text[r["sessionId"]].append(r.get("display") or "")
    return {sid: domain_of(" ".join(t)) for sid, t in text.items()}


def corrections(rows):
    sdom = session_domains(rows)
    hits = [r for r in rows if CORRECTION.search(r.get("display") or "") and not NOISE.search(r["display"])]
    by_dom = collections.defaultdict(list)
    for r in hits:
        by_dom[sdom.get(r.get("sessionId"), "other")].append(r)
    out = []
    for dom, rs in by_dom.items():
        reps = [r for r in rs if REPEAT.search(r["display"])]
        out.append({"domain": dom, "count": len(rs), "repeats": len(reps),
                    "sessions": len({r["sessionId"] for r in rs if r.get("sessionId")}),
                    "repeat_quotes": [f'{day(r["timestamp"])} "{r["display"][:220]}"' for r in reps],
                    "quotes": [f'{day(r["timestamp"])} "{r["display"][:220]}"' for r in rs]})
    out.sort(key=lambda d: (-d["repeats"], -d["count"]))
    return hits, out


def skill_index():
    idx = {}
    for f in glob.glob(f"{SKILLS}/*/SKILL.md"):
        name = os.path.basename(os.path.dirname(f))
        if name.startswith("_"):
            continue
        head = open(f, encoding="utf-8", errors="replace").read(1500).lower()
        idx[name] = set(words(name.replace("-", " ") + " " + head))
    return idx


def repeated_asks(rows, min_sessions):
    groups = collections.defaultdict(list)
    for r in rows:
        t = (r.get("display") or "").strip()
        if not t or NOISE.search(t) or t.startswith("/") or len(t) < 15:
            continue
        key = " ".join(words(t)[:3])
        if len(key.split()) >= 3:
            groups[key].append(r)
    idx = skill_index()
    out = []
    for key, rs in groups.items():
        sess = {r["sessionId"] for r in rs if r.get("sessionId")}
        if len(sess) < max(3, min_sessions):
            continue
        kw = set(key.split())
        best = max(idx.items(), key=lambda kv: len(kw & kv[1]), default=(None, set()))
        overlap = len(kw & best[1]) if best[0] else 0
        out.append({"ask": key, "sessions": len(sess), "times": len(rs),
                    "example": rs[-1]["display"][:160],
                    "nearest_skill": best[0] if overlap >= 2 else None})
    out.sort(key=lambda a: -a["sessions"])
    slash = collections.Counter(r["display"].split()[0] for r in rows if (r.get("display") or "").startswith("/"))
    return out[:12], slash.most_common(10)


def repasted(rows, min_sessions):
    # Key on the normalised text, not the hash: the same paste can arrive inline in one session
    # and through the paste cache in another, and must count as one paste.
    seen = collections.defaultdict(set)
    for r in rows:
        for p in (r.get("pastedContents") or {}).values():
            text = p.get("content") or ""
            h = p.get("contentHash")
            if not text and h and os.path.exists(f"{PASTE}/{h}.txt"):
                text = open(f"{PASTE}/{h}.txt", encoding="utf-8", errors="replace").read(2000)
            key = re.sub(r"\s+", " ", text).strip()[:300] or (f"hash:{h}" if h else "")
            if key and r.get("sessionId"):
                seen[key].add(r["sessionId"])
    out = []
    for key, sess in seen.items():
        if len(sess) < min_sessions:
            continue
        out.append({"sessions": len(sess), "preview": "(paste not cached)" if key.startswith("hash:") else key[:200]})
    out.sort(key=lambda p: -p["sessions"])
    return out[:10]


def domain_of(text):
    hits = collections.Counter()
    for name, rx in DOMAINS:
        hits[name] += len(re.findall(rx, text, re.I))
    best = hits.most_common(1)
    return best[0][0] if best and best[0][1] else "other"


def time_sinks(rows):
    """Active hours per domain. A session's gaps over 15 min do not count; its domain is the one its prompts name most."""
    by_sess = collections.defaultdict(list)
    for r in rows:
        if r.get("sessionId"):
            by_sess[r["sessionId"]].append(r)
    buckets = collections.defaultdict(lambda: {"minutes": 0.0, "sessions": 0, "corrections": 0})
    for rs in by_sess.values():
        rs.sort(key=lambda r: r["timestamp"])
        gaps = ((b["timestamp"] - a["timestamp"]) / 60000 for a, b in zip(rs, rs[1:]))
        mins = sum(g for g in gaps if g <= 15)
        b = buckets[domain_of(" ".join(r.get("display") or "" for r in rs))]
        b["minutes"] += mins
        b["sessions"] += 1
        b["corrections"] += sum(1 for r in rs if CORRECTION.search(r.get("display") or ""))
    out = [{"domain": k, "hours": round(v["minutes"] / 60, 1), "sessions": v["sessions"], "corrections": v["corrections"]}
           for k, v in buckets.items()]
    out.sort(key=lambda b: -b["hours"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=float, default=7)
    ap.add_argument("--topic")
    ap.add_argument("--min-sessions", type=int, default=2)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    rows = load(a.days, a.topic)
    if not rows:
        sys.exit(f"improve-system: no prompts in the last {a.days:g} days" + (f" for topic /{a.topic}/" if a.topic else ""))
    hits, themes = corrections(rows)
    asks, slash = repeated_asks(rows, a.min_sessions)
    pastes = repasted(rows, a.min_sessions)
    sinks = time_sinks(rows)
    sessions = len({r["sessionId"] for r in rows if r.get("sessionId")})
    rep = {"generated": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), "days": a.days, "topic": a.topic,
           "prompts": len(rows), "sessions": sessions, "correction_count": len(hits),
           "correction_rate": round(100 * len(hits) / len(rows), 1), "correction_themes": themes,
           "corrections": [{"date": day(r["timestamp"]), "text": r["display"][:240]} for r in hits[-40:]],
           "repeated_asks": asks, "slash_commands": slash, "repasted_context": pastes, "time_sinks": sinks}

    os.makedirs(OUTDIR, exist_ok=True)
    stem = datetime.datetime.now().strftime("%Y-%m-%d") + (f"-{re.sub(r'[^a-z0-9]+', '-', a.topic.lower()).strip('-')[:30]}" if a.topic else "")
    json.dump(rep, open(f"{OUTDIR}/{stem}.json", "w"), indent=1)
    md = render(rep)
    open(f"{OUTDIR}/{stem}.md", "w").write(md)
    print(json.dumps(rep, indent=1) if a.json else md)
    print(f"\nreport: {OUTDIR}/{stem}.md", file=sys.stderr)


def render(r):
    L = [f"# improve-system: {r['generated']}",
         f"Window: last {r['days']:g} days" + (f", topic /{r['topic']}/" if r["topic"] else "") +
         f". {r['prompts']} prompts across {r['sessions']} sessions.",
         f"Corrections: {r['correction_count']} ({r['correction_rate']}% of prompts).", "",
         "## 1. Corrections by domain (REPEAT = the mistake came back, a rule or hook should already stop it)"]
    for t in r["correction_themes"]:
        L.append(f"### {t['domain']}: {t['count']} corrections, {t['repeats']} repeats, {t['sessions']} sessions")
        L += [f"- REPEAT {q}" for q in t["repeat_quotes"][:10]]
        L += [f"- {q}" for q in t["quotes"] if q not in t["repeat_quotes"]][:6]
    L += ["", "## 2. Repeated asks (3+ sessions) = skill candidates"]
    L += [f"- \"{a['ask']}\": {a['sessions']} sessions. Nearest skill (keyword guess): {a['nearest_skill'] or 'NONE'}. e.g. {a['example']}"
          for a in r["repeated_asks"]] or ["- none"]
    L += ["", "Slash commands used: " + ", ".join(f"{c} {n}" for c, n in r["slash_commands"])]
    L += ["", "## 3. Context pasted into 2+ sessions = should live in the system"]
    L += [f"- {p['sessions']} sessions: {p['preview']}" for p in r["repasted_context"]] or ["- none"]
    L += ["", "## 4. Time sinks (active hours by domain)"]
    L += [f"- {s['domain']}: {s['hours']}h over {s['sessions']} sessions, {s['corrections']} corrections" for s in r["time_sinks"]] or ["- none"]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    main()
