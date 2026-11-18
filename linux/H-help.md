---
letter: H
title: Help
level: 2
image: huh
---

## What went wrong

*The woods. Otic is staring at his Mint laptop. Red text fills the screen.*

**Otic's shirt:** MOOOOO!

**Otic:** It says something went wrong. I don't know what any of it means.

**Psych:** Easy. Search for it. *He types into his browser:* `linux broken help`

*Four million results. The first is from 2009 and about a printer.*

**Psych:** This one. *He copies a command from the page and pastes it into Otic's terminal.* `sudo pacman -Syu`

**Otic's terminal:** `sudo: pacman: command not found`

**Otic's shirt:** MOOOOOOOOO!

**Psych:** Your computer's broken in a *new* way now. *He reaches for the Whudonk Stick.*

*The Mender, still sitting on his stump, quietly points at the first line of the red text. Nobody looks.*

## The Operator says

When someone rings me with "it's broken", I ask: "What does the message say?" Silence. They never read it.

The secret of every Linux expert: we don't remember everything. We look things up, fast, in the right places. The manual is already on your machine, the error message usually says what's wrong, and the words you search with decide whether you get the answer or a printer from 2009.

This lesson makes you self-sufficient. So you stop ringing me. Everybody wins.

## The Mender's way

Every command comes with its own instructions. Learn to read them and you'll never be stuck for long.

### --help: the quick version

Most commands print a short summary of their options if you add `--help`:

```bash
ls --help
```

It's a fast reminder of which letter does what. If it scrolls off the screen, scroll the terminal window up.

### man: the full manual

`man` (**manual**) opens a command's manual page, or **man page**:

```bash
man ls
```

The page opens in a viewer that fills the terminal. You move around with the keyboard:

| Key | Does |
|---|---|
| <kbd>Space</kbd> or <kbd>Page Down</kbd> | Next screen |
| <kbd>b</kbd> or <kbd>Page Up</kbd> | Back a screen |
| Arrow keys | One line at a time |
| <kbd>/</kbd> then a word, then <kbd>Enter</kbd> | Search forward for that word |
| <kbd>n</kbd> / <kbd>Shift</kbd> + <kbd>n</kbd> | Next / previous match |
| <kbd>g</kbd> / <kbd>Shift</kbd> + <kbd>g</kbd> | Jump to the top / bottom |
| <kbd>q</kbd> | Quit and go back to the terminal |

A man page has standard parts: **NAME** (what it does), **SYNOPSIS** (how to type it; anything in `[square brackets]` is optional), **DESCRIPTION** (every option) and often **EXAMPLES**: search `/EXAMPLES` to jump there.

### Man page sections

The manual is split into numbered **sections**. The ones you'll use most:

| Section | Contains |
|---|---|
| 1 | Commands anyone can run (`ls`, `cp`) |
| 5 | File formats (what goes inside a config file) |
| 8 | Admin commands, usually run with `sudo` |

Some names exist in more than one section. `passwd` is a command (section 1) and also a file, `/etc/passwd` (section 5). Put the number first to choose:

```bash
man 5 passwd
```

When you see `passwd(5)` written in a guide, that's what it means.

### Installing the manual

Most distros come with man pages ready. Arch installs the bare minimum, so you add them yourself. `tldr` (a friendlier helper, explained below) needs installing on every family.

### On Debian / Ubuntu / Mint

Man pages are already there. To add `tldr`:

```bash
sudo apt install tldr
```

### On Fedora

Man pages are already there. To add `tldr`:

```bash
sudo dnf install tldr
```

### On Arch / Manjaro

Install the man page viewer, the pages themselves, and `tealdeer` (a fast version of `tldr`; the command it gives you is still called `tldr`):

```bash
sudo pacman -S man-db man-pages tealdeer
```

### tldr: just show me examples

`tldr` ("too long; didn't read") shows a handful of common, real examples instead of the whole manual. The first time, it may need to download its pages:

```bash
tldr --update
tldr tar
```

You get a handful of ready-made `tar` commands, each explained in one line. Use `tldr` for "how do I usually do this?" and `man` for "what exactly does this option do?".

### Searching the manual: apropos and man -k

If you don't know a command's name, search the one-line descriptions of every man page. These two do exactly the same thing:

```bash
apropos copy
man -k copy
```

You'll see a list like `cp (1) - copy files and directories`. If it says `nothing appropriate` for everything, the search index hasn't been built yet. Build it once with `sudo mandb` (it needs `sudo` because the index lives in a system folder).

### info, briefly

Some GNU programs have longer manuals in a viewer called `info`: try `info coreutils`. Arrow keys move, <kbd>Enter</kbd> follows a menu entry, <kbd>q</kbd> quits. You'll rarely need it.

### The Arch Wiki (for everyone)

The **Arch Wiki** (`wiki.archlinux.org`) is the best Linux manual on the web, and most of it applies to every distro: the programs are the same, only the install commands differ. Where it says `pacman -S something`, use your own family's command (lesson L). Fedora's docs (`docs.fedoraproject.org`) and the Ubuntu and Mint forums are good too.

### Reading error messages

Error messages are usually short and literal. Read them left to right:

```
cp: cannot stat 'notes.tx': No such file or directory
```

- `cp:` is the program that's complaining.
- `cannot stat 'notes.tx'` is what it tried to do, and to what. ("stat" means "look up the details of".)
- `No such file or directory` is why it failed. Here: a typo, `.tx` instead of `.txt`.

Three common ones: `command not found` (typo, or the program isn't installed, or it's a different family's command), `Permission denied` (you need different rights; lesson K) and `No such file or directory` (wrong name or wrong folder; check with `pwd` and `ls`).

When there's a long wall of red, the **first** error is usually the cause. Later lines are often knock-on effects.

### Searching the web well

Put three things into the search box:

1. Your distro and version: `Fedora 42`, `Mint 22`, `Arch`.
2. The program's name.
3. The exact error, copied, in quotes: `"No such file or directory"`.

Leave out your username and anything personal. Prefer recent answers for your family, and check what a command does with `man` or `tldr` before you paste it.

## Do it now

Nothing changes on your system except installing `tldr`.

1. Install the man pages (Arch only) and `tldr` for your family, using the commands above. Then run `tldr --update`.
2. Open `man ls`. Search with `/human` and press <kbd>Enter</kbd>. Find what `-h` does. Press <kbd>q</kbd>.
3. Run `man -k directory` and find the command that makes directories.
4. Run `tldr cp`. Find the example that copies a folder.
5. Run `cp nothing-here.txt ~/practice/` (the file doesn't exist). Read the error left to right and say out loud what each part means.

You've done it when you can tell someone what `ls -h` does, which command makes directories, and what was wrong in step 5, without searching the web.

## Quiz

```quiz
- q: You're reading a man page. How do you search it for the word "recursive"?
  options:
    - Press Ctrl+F and type recursive
    - Type /recursive and press Enter
    - Press q and run man recursive
  answer: 1
  why: In man, / starts a search. n jumps to the next match and q quits.
- q: Otic has an error on Mint. Which web search is most likely to find the answer?
  options:
    - linux broken help
    - "Mint 22 apt \"Unable to locate package\""
    - The fix that Psych pastes from an Arch page
  answer: 1
  why: The distro, the program and the exact error in quotes find people who had the same problem on the same system.
- q: You don't know which command copies files. What helps?
  options:
    - "man -k copy"
    - "man 5 copy"
    - Paste the first command from any forum
  answer: 0
  why: man -k (the same as apropos) searches every man page's description for a word.
```

## Scribble watch

The Scribble writes helpful forum answers: "Fixed it for me! Just run this:", then a long unreadable line with `sudo` in it. Before you run any command from the web, look up each part with `tldr` or `man`. If you still can't explain what it does, don't run it. Ask on your distro's official forum instead.
