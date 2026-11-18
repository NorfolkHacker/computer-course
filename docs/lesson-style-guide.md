# Lesson style guide

Read this, the spec (`docs/superpowers/specs/2026-11-18-computer-course-design.md`) and the
exemplar `main/A-parts-of-a-computer.md` before writing a lesson.

## Who it's for

An adult who is an absolute beginner, working alone at a Windows 11 PC with an Android
phone next to him. He is not stupid; he has just never been shown. He should finish each
lesson able to *do* the thing, not just know about it.

## The golden rule

**Jokes go in the framing. Instructions are plain.** What went wrong, the Operator and the
Scribble watch can be as daft as you like. The Mender's steps, Do it now and the quiz
explanations must be literal, accurate and calm. A beginner must never have to decode a
joke to learn a step.

## Cast and voices

- **The Operator** (narrator): a dry, gleefully menacing sysadmin in the BOFH tradition.
  He is an original character: never name BOFH, Simon Travaglia, "the PFY" or any
  character from those stories. He keeps a "luser list", has an excuse calendar,
  despises printers, threatens dire consequences he never carries out, and secretly
  wants the learner to succeed: he is the one user the Operator grudgingly respects.
  Never actually insult the learner. First person, short sentences, deadpan.
- **Psych**: shaved head, black T-shirt, jeans. Carries the Whudonk Stick (a big purple
  mallet that glows and crackles). Confident, impatient; when technology resists, he
  reaches for the Stick. Says things like "Not a problem..."
- **Otic**: Psych's brother, red T-shirt with a cow on it. Curious, a bit nervous. When
  something scary happens (a pop-up, a warning, a loud noise) the cow on his shirt goes
  **MOOOOO!** He asks the questions the learner is thinking.
- **The Mender** (of small weathers): a quiet stitched figure with button eyes. Calm,
  kind, few words. Gives the real method. Sometimes tidies a bit of Scribble into a jar.
- **The Scribble**: a black tangle of scribbled lines. The villain: scams, viruses, junk,
  clutter, lost files. It is never quite gone; a small bit always survives.
- **Propellor Boy & Unicorn Boy**: the cautionary tales. They click the link, give the
  password to the nice man on the phone, buy the miracle cleaner. They usually end up
  launched into space.

## Sections

### What went wrong (80–150 words)
A tiny script. Psych & Otic try the lesson's task and go wrong in a cartoonish but
*realistic* way: the mistake must be one real beginners make (double-clicking too slowly,
holding the power button to shut down, typing the website into the search box...).
Stage directions in *italics* on their own line; dialogue as `**Name:** line`. Comic sound
effects in capitals (WHUDONK!, MOOOOO!). End on the moment it goes wrong.

### The Operator says (60–120 words)
First person, deadpan. One or two jokes, then the real reason this lesson matters. Can
start with a line like "Rule one." or an entry from the luser list.

### The Mender's way
The lesson proper. Most of the word count lives here.
- Short intro sentence or two, in the Mender's calm voice (no jokes).
- **Bold** every on-screen name exactly as it appears: **Start**, **Settings**, **Save as**.
- Keys as `<kbd>Ctrl</kbd> + <kbd>C</kbd>`.
- Numbered steps, one action each. Say where to look ("bottom-left of the screen").
- Use `### ` sub-headings to split topics. When a topic is done differently on the PC and
  the phone, put the two versions next to each other as `### On Windows` and
  `### On Android` (exactly that wording at the start; anything after is fine, e.g.
  `### On Android (your phone)`). The site shows them side by side.
- Define every new word the first time, plainly: "The **browser** is the app you use to
  look at websites."
- A small table is fine for "what is what" lists.
- Accurate to Windows 11 (24H2) and Android 14/15. Android menus vary by maker; say so,
  give the Google/Pixel wording, and give the fallback "open **Settings** and use the
  search bar at the top".
- UK English. "Mobile" or "phone", "programme" only for TV (it's "program"/"app" here).

### Do it now
One concrete, safe exercise on his own computer or phone, with numbered steps if needed
and a clear finishing check: "You've done it when...". Never anything that could lose
data, cost money or contact strangers.

### Quiz
Exactly three questions in the fenced `quiz` YAML block. 3–4 options each. `answer` is
the 0-based index of the right option. `why` is one or two plain sentences. Wrong options
should be the real mistakes from What went wrong, not silly ones. Quote any value that has
a colon in it.

### Scribble watch (40–80 words)
One safety habit relevant to the lesson, framed as the Scribble trying something. Ends
with exactly what to do.

## Front matter

```yaml
---
letter: B
title: The Mouse
image: psych-up
---
```

`image` is optional; choose from: `psych`, `psych-up`, `psych-smash`, `otic`,
`propellor-boy`, `unicorn-boy`, `mender`, `scribble`, `jar`, `woods`, `whudonk`, `mooo`,
`ohno`, `poof`, `shloop`, `whoosh`, `clink`, `huh`. Vary them across lessons.

## Length and checks

700–1200 words per lesson. After writing, run `.venv/bin/python build.py` from the repo
root; it must print `Built N lessons`.
