# Computer Course: Design

Date: 2026-11-18
Status: awaiting review

## Purpose

An A–Z computer-literacy course for an absolute beginner (the author's brother),
told in a humorous style: the dry, gleefully menacing sysadmin voice of the
BOFH stories, starring the cast of the felt cartoon *Psych and Otic*.

Success: someone starting from zero can work through it alone, at the computer,
and come out able to use a Windows 11 PC and an Android phone safely and
confidently.

## Scope

Two separate courses in one repo, built one after the other:

1. **Main course** (`main/`): Windows 11 + Android, zero to computer-literate. Built first.
2. **Linux course** (`linux/`): standalone, beginner to experienced. Separate later pass, own plan.

## Cast

| Character | Role |
|---|---|
| **The Operator** | Narrator. A BOFH-style sysadmin (an original character, not BOFH himself): dry, menacing, keeps a luser list, has an excuse for everything. |
| **Psych** | Student. Tries things first, gets them wrong; reaches for the Whudonk Stick when technology resists. |
| **Otic** | Student. Cow T-shirt; the cow goes MOOOOO at pop-ups and scary messages. |
| **The Mender** | Calm voice of the correct method. Delivers the actual instructions. |
| **The Scribble** | Recurring villain: scams, malware, clutter, lost files. Never quite gone. |
| **Propellor Boy & Unicorn Boy** | Cautionary tales: they clicked the link. |

The humour sits in the framing; the instructions themselves stay plain, accurate
and easy to follow. A beginner must never have to decode a joke to learn the step.

## Main course: A–Z

| | Lesson |
|---|---|
| A | The parts of a computer; switching on and off properly |
| B | The mouse: pointing, clicking, double-clicking, right-clicking, dragging |
| C | The keyboard and typing |
| D | Desktop, windows, Start menu, taskbar |
| E | Files and folders |
| F | Finding things: search, Downloads, Recent |
| G | Getting online: Wi-Fi and the web browser |
| H | Hunting: searching the web well, judging what you find |
| I | Inbox: email |
| J | Junk and scams: phishing, fake pop-ups, phone scams (the Scribble) |
| K | Keys: passwords, a password manager, two-factor authentication |
| L | Lifeboats: backups and the cloud (OneDrive / Google) |
| M | Mobile: Android basics |
| N | Notifications and settings (Windows + Android) |
| O | Office: writing documents (Word / Google Docs) |
| P | Printing, PDFs, scanning |
| Q | Quick keys: shortcuts |
| R | Running programs: installing and removing apps safely |
| S | Security: updates, Windows Security |
| T | Troubleshooting ("have you tried turning it off and on again") |
| U | USB, Bluetooth, plugging things in |
| V | Video calls |
| W | Web money: shopping and banking safely |
| X | eXtra care: privacy, social media, AI tools |
| Y | Your accounts: Microsoft / Google accounts and recovery |
| Z | Zen: maintenance, asking for help well, final exam |

### Lesson template

Every lesson has the same sections:

1. **Cold open**: a short scene where Psych & Otic get it wrong.
2. **The Operator says**: a grim one-paragraph summary of why this matters.
3. **The Mender's way**: numbered steps; Windows and Android side by side where both apply.
4. **Do it now**: a hands-on practice task.
5. **Quiz**: 3 multiple-choice questions, with the answer and explanation.
6. **Scribble watch**: one safety tip.

## Linux course (later, outline only)

Four tiers: **Desktop** (install, get comfortable) → **Terminal** (files,
permissions, packages) → **Power user** (scripting, processes, networking, SSH)
→ **Sysadmin** (services, logs, a home server: the student becomes the Operator).
It gets its own design pass and plan once the main course ships.

## Technical design

- **Repo**: `NorfolkHacker/computer-course`, public.
- **Source of truth**: one Markdown file per lesson, `main/<LETTER>-<slug>.md`,
  with YAML front matter (letter, title) and the quiz in a fenced `quiz` block
  (question, options, answer index, explanation).
- **Build**: `build.py` (Python, no heavy dependencies) reads the lessons and writes
  - `site/index.html`, `site/<letter>.html`: the web course. Lesson menu,
    clickable quizzes, a progress tick per lesson stored in `localStorage`
    (wrapped in try/catch; the site works without it). Works on phone width.
  - `site/handbook.html`: every lesson on one print-styled page, ready to print or
    save as PDF; `handbook.pdf` produced from it (headless Chromium) and committed.
- **Hosting**: GitHub Pages from the built `site/` via a GitHub Actions workflow,
  at `norfolkhacker.github.io/computer-course`.
- **Pictures**: character stills from the felt library / Psych and Otic film
  (`~/Documents/felt`), copied into `site/img/`. Original art only.

## Testing

- `build.py` fails loudly on a lesson missing a template section or with a malformed quiz.
- A check script confirms all 26 lessons exist and every link in the built site resolves.
- Manual pass: open the site in the browser at desktop and phone width; print-preview the handbook.

## Out of scope

- Accounts, server-side tracking, or a backend.
- Video.
- macOS / iPhone.
