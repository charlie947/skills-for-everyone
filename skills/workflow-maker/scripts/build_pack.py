#!/usr/bin/env python3
"""
Turn a filled workflow-maker pack (markdown) into a clean, self-contained HTML page.

Usage:
    python3 build_pack.py <path-to-pack.md>

Writes <same-name>.html next to the markdown. Python 3 standard library only.
Handles: headings, fenced code blocks, bold, inline code, links, unordered and
ordered lists, horizontal rules, HTML comments (stripped) and paragraphs.
An ordered list that restarts after a code block keeps its numbering, and lines
indented 2+ spaces under a list item join that item. Exits 1, writing nothing,
if an unfilled {{UPPER_CASE}} token is left outside an HTML comment.
"""

import html
import re
import sys
from pathlib import Path


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def inline(text: str) -> str:
    text = esc(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(
        r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
        lambda m: f'<a href="{m.group(2).replace(chr(34), "%22")}">{m.group(1)}</a>',
        text,
    )
    return text


def is_continuation(line: str) -> bool:
    """An indented text line under a list item: 2+ leading spaces, not a new
    list marker and not a code fence."""
    if not re.match(r"^ {2,}\S", line):
        return False
    s = line.strip()
    return not (s.startswith("```") or re.match(r"^([-*]|\d+\.)\s", s))


def unfilled_tokens(md: str) -> list:
    """Line numbers and text of any {{UPPER_CASE}} template token left outside an HTML comment.
    A merge tag such as {{ first_name }} is the reader's content and passes."""
    no_comments = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), md, flags=re.DOTALL)
    return [(k, ln.strip()) for k, ln in enumerate(no_comments.split("\n"), 1) if re.search(r"\{\{[A-Z0-9_]+\}\}", ln)]


def md_to_html(md: str) -> str:
    md = re.sub(r"<!--.*?-->", "", md, flags=re.DOTALL)
    lines = md.split("\n")
    out = []
    list_kind = None
    gap_before = False  # a blank line sat between the last item and this line
    i = 0
    n = len(lines)

    def close_list():
        nonlocal list_kind
        if list_kind:
            out.append(f"</{list_kind}>")
            list_kind = None

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Fenced code block. Prompt blocks are the product, so keep them verbatim.
        if stripped.startswith("```"):
            close_list()
            i += 1
            code = []
            while i < n and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1  # skip the closing fence
            out.append(
                '<div class="prompt"><button type="button" class="copy">Copy</button>'
                "<pre><code>" + esc("\n".join(code)) + "</code></pre></div>"
            )
            continue

        if stripped == "":
            # A blank line between items of the same list keeps the list open,
            # so "1. 2. 3." with gaps does not restart at 1 each time. So does
            # an indented continuation line under the last item.
            j = i + 1
            while j < n and lines[j].strip() == "":
                j += 1
            raw_next = lines[j] if j < n else ""
            nxt = raw_next.strip()
            same = (list_kind == "ol" and re.match(r"^\d+\.\s", nxt)) or (
                list_kind == "ul" and re.match(r"^[-*]\s", nxt)) or (
                list_kind and is_continuation(raw_next))
            if not same:
                close_list()
            else:
                gap_before = True
            i += 1
            continue

        # A line indented 2+ spaces under a list item belongs to that item.
        if list_kind and out and out[-1].endswith("</li>") and is_continuation(line):
            joiner = "<br>" if gap_before else " "
            out[-1] = out[-1][: -len("</li>")] + joiner + inline(stripped) + "</li>"
            gap_before = False
            i += 1
            continue
        gap_before = False

        if stripped == "---":
            close_list()
            out.append("<hr>")
            i += 1
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            close_list()
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
            continue

        m = re.match(r"^[-*]\s+(.*)$", stripped)
        if m:
            if list_kind != "ul":
                close_list()
                out.append("<ul>")
                list_kind = "ul"
            out.append(f"<li>{inline(m.group(1))}</li>")
            i += 1
            continue

        m = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if m:
            if list_kind != "ol":
                close_list()
                start = int(m.group(1))
                # Keep the real number when a list resumes after a code block.
                out.append("<ol>" if start == 1 else f'<ol start="{start}">')
                list_kind = "ol"
            out.append(f"<li>{inline(m.group(2))}</li>")
            i += 1
            continue

        close_list()
        out.append(f"<p>{inline(stripped)}</p>")
        i += 1

    close_list()
    return "\n".join(out)


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  :root {{
    --bg: #ffffff;
    --ink: #1a1d23;
    --muted: #5f6672;
    --line: #e3e6eb;
    --soft: #f4f5f7;
    --code-bg: #1a1d23;
    --code-ink: #e9ecf1;
    --accent: #2f6fde;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg: #14161a;
      --ink: #e9ecf1;
      --muted: #a0a7b3;
      --line: #2a2e35;
      --soft: #1f2228;
      --code-bg: #0b0c0e;
      --code-ink: #e9ecf1;
      --accent: #7aa7ff;
    }}
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    color: var(--ink);
    background: var(--bg);
    line-height: 1.65;
    font-size: 17px;
    max-width: 760px;
    margin: 0 auto;
    padding: 48px 16px 96px;
  }}
  h1 {{ font-size: 34px; line-height: 1.15; margin: 0 0 14px; }}
  h2 {{ font-size: 24px; margin: 44px 0 12px; padding-bottom: 8px; border-bottom: 1px solid var(--line); }}
  h3 {{ font-size: 19px; margin: 32px 0 10px; }}
  p, ul, ol {{ margin: 12px 0; }}
  ul, ol {{ padding-left: 22px; }}
  li {{ margin: 6px 0; }}
  hr {{ border: none; border-top: 1px solid var(--line); margin: 36px 0; }}
  a {{ color: var(--accent); }}
  code {{
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: 14px;
    background: var(--soft);
    padding: 2px 6px;
    border-radius: 4px;
  }}
  .prompt {{ position: relative; margin: 14px 0; }}
  pre {{
    background: var(--code-bg);
    border-radius: 10px;
    padding: 44px 20px 20px;
    margin: 0;
    overflow-x: auto;
  }}
  pre code {{
    background: none; color: var(--code-ink); padding: 0;
    font-size: 14.5px; line-height: 1.6;
    white-space: pre-wrap; word-break: break-word;
  }}
  .copy {{
    position: absolute; top: 10px; right: 10px;
    font: 600 13px/1 -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    color: var(--code-ink); background: transparent;
    border: 1px solid #4a505a; border-radius: 6px;
    padding: 6px 10px; cursor: pointer;
  }}
</style>
</head>
<body>
{body}
<script>
  document.querySelectorAll('.copy').forEach(function (btn) {{
    btn.addEventListener('click', function () {{
      var text = btn.parentElement.querySelector('code').innerText;
      var done = function () {{ btn.textContent = 'Copied'; setTimeout(function () {{ btn.textContent = 'Copy'; }}, 1500); }};
      if (navigator.clipboard) {{
        navigator.clipboard.writeText(text).then(done, function () {{ btn.textContent = 'Select and copy'; }});
      }} else {{
        btn.textContent = 'Select and copy';
      }}
    }});
  }});
</script>
</body>
</html>
"""


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 build_pack.py <path-to-pack.md>")
        sys.exit(1)
    src = Path(sys.argv[1])
    if not src.is_file():
        print(f"File not found: {src}")
        sys.exit(1)
    md = src.read_text(encoding="utf-8")
    left = unfilled_tokens(md)
    if left:
        for k, text in left:
            print(f"Unfilled {{{{ token on line {k}: {text}")
        sys.exit(1)
    title_match = re.search(r"^#\s+(.*)$", md, flags=re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "Workflow pack"
    out_path = src.with_suffix(".html")
    out_path.write_text(PAGE.format(title=esc(title), body=md_to_html(md)), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
