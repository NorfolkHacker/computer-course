---
letter: O
title: The Shell
level: 3
image: psych-up
---

## What went wrong

*Psych's flat. Psych is typing very fast.*

**Psych:** I've made a shortcut. Now `update` does the whole system upgrade. One word. Arch, by the way.

**Otic:** How?

**Psych:** `alias update='sudo pacman -Syu'`. *He types* `update`. *It works.* Not a problem.

*He closes the terminal, opens a new one, and types* `update`.

```
bash: update: command not found
```

**Otic:** *(the cow on his shirt)* MOOOOO!

**Psych:** It's been stolen. *He opens* `~/.bashrc` *in nano, selects everything, and deletes it to "start fresh".* There. Clean.

*He opens a new terminal. The prompt is plain grey. Nothing has colour. Nothing works the way it did.*

*He reaches for the Whudonk Stick.*

## The Operator says

Luser list, entry 512: made an alias, closed the window, reported a theft.

The shell is the program that reads what you type. It has a memory, but it's a goldfish's memory: anything you set in a terminal dies with that terminal, unless you write it into the shell's start-up file. Learn where that file is, how to change it safely, and how to keep a spare. Then your shortcuts survive, and you never have to explain to me why your prompt went grey.

## The Mender's way

The terminal is just a window. The **shell** is the program running inside it: it reads your command, finds the program, runs it and shows you the result.

### Which shell you have

Mint, Ubuntu, Fedora and Arch all give new users the same shell: **bash** (the "Bourne Again SHell"). Check yours:

```bash
echo $SHELL
```

```
/bin/bash
```

Other shells exist. **zsh** is popular and very configurable; **fish** is friendly, with suggestions as you type. Both are in every family's repositories. This course uses bash, because it's the default everywhere and almost every guide assumes it.

### Variables

A **variable** is a named box holding a bit of text. Make one with a name, `=`, and a value, with **no spaces** around the `=`:

```bash
pet="a cow"
echo "Otic has $pet"
```

The `$` in front of the name means "put the value here". `echo` prints whatever follows it.

### Environment variables

Some variables are set for you and passed to every program you start. These are **environment variables**, written in capitals by convention:

```bash
echo $HOME
echo $USER
env | less
```

`env` lists them all; `less` lets you scroll (press <kbd>q</kbd> to quit).

A variable you make yourself stays inside the current shell. To pass it on to programs you run from it, **export** it:

```bash
export EDITOR=nano
```

Now any program that asks "which editor does this person like?" gets `nano`.

### PATH: where commands live

When you type `ls`, the shell doesn't search the whole disk. It looks in a list of folders stored in `PATH`, separated by colons:

```bash
echo $PATH
```

```
/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin
```

To see which file a command actually runs, use `which` or `type`:

```bash
which nano
type ls
type cd
```

`which` shows the program's path. `type` is a bash command that tells you more: whether something is a program, an **alias** (a nickname, below) or a **builtin** (part of bash itself, like `cd`).

### The start-up files

Every time bash starts, it reads hidden files in your home folder. The important one is **`~/.bashrc`**: it's read every time you open a terminal window. A second file is read only when you **log in** (at the login screen or over SSH), and its name differs by family.

### On Debian / Ubuntu / Mint

The login file is `~/.profile`. It runs `~/.bashrc` for you. Your `.bashrc` also loads `~/.bash_aliases` if it exists, so you can keep aliases in their own file.

### On Fedora

The login file is `~/.bash_profile`. It runs `~/.bashrc`, which also loads any files in the folder `~/.bashrc.d/` if you make one.

### On Arch / Manjaro

The login file is `~/.bash_profile`. It runs `~/.bashrc`. Arch's `.bashrc` is very short; you add what you want.

### The rule

On all three: **put your own settings in `~/.bashrc`**. Leave the login file alone unless a guide specifically says otherwise.

### Back it up first

Before you touch `.bashrc`, make a copy:

```bash
cp ~/.bashrc ~/.bashrc.bak
```

If you ever break it, put the copy back and open a new terminal:

```bash
cp ~/.bashrc.bak ~/.bashrc
```

### Aliases

An **alias** is a short name for a longer command:

```bash
alias ll='ls -lh'
```

Now `ll` runs `ls -lh`. Type `alias` on its own to list the ones you have. Mint and Ubuntu already include a few, such as `ll`.

An alias typed in the terminal disappears when you close the window. To keep it:

1. Open the file: `nano ~/.bashrc`
2. Go to the very bottom (<kbd>Ctrl</kbd> + <kbd>End</kbd>).
3. Add your line, for example `alias ll='ls -lh'`
4. Save with <kbd>Ctrl</kbd> + <kbd>O</kbd>, <kbd>Enter</kbd>, and exit with <kbd>Ctrl</kbd> + <kbd>X</kbd>.

### source: reload without closing

New terminals read the file automatically. To load your changes into the terminal you're already in, use `source`, which runs a file in the current shell:

```bash
source ~/.bashrc
```

### History

bash remembers what you've typed.

- <kbd>↑</kbd> and <kbd>↓</kbd> step through recent commands.
- `history` lists them, numbered.
- <kbd>Ctrl</kbd> + <kbd>R</kbd> searches backwards: press it, type part of an old command, and it appears. Press <kbd>Ctrl</kbd> + <kbd>R</kbd> again for older matches, <kbd>Enter</kbd> to run it, or <kbd>Esc</kbd> to put it on the line without running it.

```bash
history | grep apt
```

### A nicer prompt (briefly)

The prompt's look is stored in a variable called `PS1`. Try this in a terminal (it only lasts until you close it):

```bash
PS1='\u@\h \w \$ '
```

`\u` is your user name, `\h` the computer's name, `\w` the folder you're in, and `\$` shows `$` (or `#` when you're root). If you like it, add the line to `~/.bashrc`.

## Do it now

1. Back up your start-up file: `cp ~/.bashrc ~/.bashrc.bak`
2. Run `echo $SHELL`, `echo $HOME` and `type cd`, and read the answers.
3. Open `~/.bashrc` in nano and add this line at the bottom:
   `alias now='date "+%H:%M on %A"'`
4. Save, exit, then run `source ~/.bashrc`.
5. Type `now`. You should see the time and day.
6. Close the terminal, open a new one and type `now` again.
7. Press <kbd>Ctrl</kbd> + <kbd>R</kbd>, type `source`, and press <kbd>Esc</kbd> to see your earlier command come back.

You've done it when `now` works in a brand-new terminal. To undo, run `cp ~/.bashrc.bak ~/.bashrc`.

## Quiz

```quiz
- q: Psych made an alias, closed the terminal, and it was gone. Why?
  options:
    - Arch deletes aliases on purpose
    - He typed it in the terminal but didn't add it to ~/.bashrc
    - Aliases only last for one command
  answer: 1
  why: Anything set in a terminal only lasts for that terminal. Write it into ~/.bashrc to keep it.
- q: You've just edited ~/.bashrc. How do you load the change into the terminal you're using?
  options:
    - source ~/.bashrc
    - Delete ~/.bashrc and start fresh
    - sudo reboot
  answer: 0
  why: source runs the file in the current shell. A new terminal also reads it automatically.
- q: What does PATH hold?
  options:
    - Your home folder
    - The last folder you visited
    - The list of folders the shell searches for commands
  answer: 2
  why: When you type a command, bash looks for it in each folder listed in PATH, in order.
```

## Scribble watch

The Scribble loves a forum post that says "add this to your `.bashrc`". A line there runs every single time you open a terminal, and one that quietly changes `PATH` can make `sudo` run a fake program. Before you add anything, make a backup with `cp ~/.bashrc ~/.bashrc.bak`, read the line, and only add it if you understand what it does.
