## What it does

Puts the finished thing in front of you as a page in your browser, before Claude says a word about it. Plans, comparisons, reports and options all become one self-contained HTML file that opens on your screen.

It treats "described" and "delivered" as different things. A picture written out in prose is Claude's idea of the picture, not the picture. A file path in the chat is not the page either. The skill is only finished when the page is open in front of you.

## When to reach for it

Type `/show-me`, or Claude reaches for it whenever it is about to describe something visual, or ask you to choose between options. "Show me", "let me see it" and "which one" all fire it.

| You want | Use |
| --- | --- |
| To see a plan, report or comparison | `show-me` |
| To pick between directions | `show-me` (it builds a board of three or more) |

## The four modes

- **Show.** One thing, or a stack of versions with the newest on top.
- **Pick.** At least three genuinely different options side by side, each with a button that copies your choice.
- **History.** After two rejections, every direction tried so far on one page, each labelled with what you said about it.
- **Copy.** When the question is about words, the words, laid out as they will be read.

## Common questions

**The page opened behind my other windows.**
On a Mac, the skill uses a short AppleScript that brings the browser forward and selects the new tab, then reads the address back to check. The plain "open" command can leave the tab hidden.

**Why does it keep bringing my browser to the front?**
It should do that once per page. Updates to the same page reload quietly.

## It's working if

- You stop reading descriptions of layouts and start clicking a pick button.
- Every choice you make is between three or more things you can see.
- The chat reply after a page is one or two lines long.

## Where it fits

A reach-for-it-anytime standalone. Other skills in the pack hand their reports to it: [improve-system](./improve-system.md) shows its findings as a page, and [close](./close.md) can too.
